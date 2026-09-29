"""First-party visitor analytics for intersignal.org.

The public collector and the authenticated dashboard API are deliberately
separate routes. Run behind HTTPS and a reverse proxy that overwrites
X-Real-IP; see README.md before exposing this service.
"""

from __future__ import annotations

import argparse
import getpass
import hashlib
import hmac
import ipaddress
import json
import os
import re
import secrets
import sqlite3
import time
import uuid
from functools import wraps
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from flask import Flask, g, jsonify, make_response, request
from geoip2fast import GeoIP2Fast
from ua_parser import parse as parse_user_agent


HERE = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get("ANALYTICS_DB_PATH", HERE / "data" / "analytics.sqlite3"))
SITE_ORIGIN = os.environ.get("ANALYTICS_SITE_ORIGIN", "https://intersignal.org").rstrip("/")
COOKIE_NAME = "intersignal_stats_session"
SESSION_SECONDS = 7 * 24 * 3600
RAW_RETENTION_DAYS = int(os.environ.get("ANALYTICS_RAW_RETENTION_DAYS", "90"))
VISITOR_RETENTION_DAYS = int(os.environ.get("ANALYTICS_VISITOR_RETENTION_DAYS", "400"))
COLLECTOR_PER_MINUTE = int(os.environ.get("ANALYTICS_COLLECTOR_PER_MINUTE", "180"))
BOT_RE = re.compile(r"bot|crawl|spider|headless|lighthouse|preview|facebookexternalhit", re.I)
ID_RE = re.compile(r"^[a-f0-9-]{36}$")

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 4096

try:
    GEO = GeoIP2Fast(geoip2fast_data_file=os.environ.get(
        "ANALYTICS_GEO_DB", "geoip2fast-ipv6.dat.gz"
    ))
except Exception:
    GEO = None


def connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(DB_PATH, timeout=10)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    db.execute("PRAGMA busy_timeout=10000")
    db.execute("PRAGMA secure_delete=ON")
    return db


def init_db() -> None:
    with connect() as db:
        db.execute("PRAGMA journal_mode=WAL")
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS visitors (
                id TEXT PRIMARY KEY,
                first_seen INTEGER NOT NULL,
                last_seen INTEGER NOT NULL,
                visit_count INTEGER NOT NULL DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS visits (
                id TEXT PRIMARY KEY,
                visitor_id TEXT NOT NULL REFERENCES visitors(id),
                started_at INTEGER NOT NULL,
                last_seen INTEGER NOT NULL,
                visit_number INTEGER NOT NULL,
                first_path TEXT NOT NULL,
                last_path TEXT NOT NULL,
                referrer_url TEXT NOT NULL,
                ip_address TEXT NOT NULL,
                country_code TEXT NOT NULL,
                country_name TEXT NOT NULL,
                operating_system TEXT NOT NULL,
                browser TEXT NOT NULL,
                device TEXT NOT NULL,
                pageviews INTEGER NOT NULL DEFAULT 0
            );
            CREATE INDEX IF NOT EXISTS visits_started_idx ON visits(started_at);
            CREATE INDEX IF NOT EXISTS visits_visitor_idx ON visits(visitor_id, started_at);
            CREATE INDEX IF NOT EXISTS visits_last_seen_idx ON visits(last_seen);
            CREATE TABLE IF NOT EXISTS pageviews (
                id TEXT PRIMARY KEY,
                visit_id TEXT NOT NULL REFERENCES visits(id) ON DELETE CASCADE,
                occurred_at INTEGER NOT NULL,
                path TEXT NOT NULL,
                referrer_url TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS pageviews_time_idx ON pageviews(occurred_at);
            CREATE INDEX IF NOT EXISTS pageviews_path_idx ON pageviews(path, occurred_at);
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                salt BLOB NOT NULL,
                password_hash BLOB NOT NULL,
                created_at INTEGER NOT NULL
            );
            CREATE TABLE IF NOT EXISTS auth_sessions (
                token_hash TEXT PRIMARY KEY,
                username TEXT NOT NULL REFERENCES users(username) ON DELETE CASCADE,
                expires_at INTEGER NOT NULL
            );
            CREATE INDEX IF NOT EXISTS auth_sessions_expiry_idx ON auth_sessions(expires_at);
            CREATE TABLE IF NOT EXISTS login_failures (
                ip_address TEXT NOT NULL,
                username TEXT NOT NULL,
                occurred_at INTEGER NOT NULL
            );
            CREATE INDEX IF NOT EXISTS login_failures_idx
                ON login_failures(ip_address, username, occurred_at);
            CREATE INDEX IF NOT EXISTS login_failures_ip_idx
                ON login_failures(ip_address, occurred_at);
            CREATE TABLE IF NOT EXISTS collector_rate (
                ip_address TEXT NOT NULL,
                minute INTEGER NOT NULL,
                hits INTEGER NOT NULL,
                PRIMARY KEY (ip_address, minute)
            );
            """
        )


init_db()


def db_for_request() -> sqlite3.Connection:
    if "db" not in g:
        g.db = connect()
    return g.db


@app.teardown_appcontext
def close_db(_error: BaseException | None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def client_ip() -> str:
    peer = request.remote_addr or ""
    try:
        parsed_peer = ipaddress.ip_address(peer)
    except ValueError:
        return "Unknown"
    # Only a local, trusted reverse proxy may supply the real visitor IP.
    if parsed_peer.is_loopback:
        forwarded = request.headers.get("X-Real-IP", "").strip()
        try:
            return str(ipaddress.ip_address(forwarded))
        except ValueError:
            pass
    return str(parsed_peer)


def country_for_ip(ip: str) -> tuple[str, str]:
    try:
        if ipaddress.ip_address(ip).is_private or GEO is None:
            return "ZZ", "Unknown"
        result = GEO.lookup(ip)
        code = result.country_code or "ZZ"
        if len(code) != 2 or not code.isalpha():
            return "ZZ", "Unknown"
        return code.upper(), result.country_name or "Unknown"
    except (ValueError, OSError, AttributeError):
        return "ZZ", "Unknown"


def user_agent_details(value: str) -> tuple[str, str, str]:
    try:
        parsed = parse_user_agent(value[:512])
        os_part = parsed.os
        browser_part = parsed.user_agent
        device_part = parsed.device
        os_name = (os_part.family if os_part else None) or "Unknown"
        if os_part and os_part.major:
            os_name += f" {os_part.major}"
        browser_name = (browser_part.family if browser_part else None) or "Unknown"
        if browser_part and browser_part.major:
            browser_name += f" {browser_part.major}"
        family = (device_part.family if device_part else "") or ""
        if re.search(r"tablet|ipad", family, re.I):
            device = "Tablet"
        elif re.search(r"mobile|iphone|android|phone", family, re.I):
            device = "Mobile"
        else:
            device = "Desktop"
        return os_name[:80], browser_name[:80], device
    except Exception:
        return "Unknown", "Unknown", "Unknown"


def valid_uuid(value: object) -> bool:
    if not isinstance(value, str) or not ID_RE.fullmatch(value):
        return False
    try:
        return str(uuid.UUID(value)) == value
    except ValueError:
        return False


def clean_path(value: object) -> str | None:
    if not isinstance(value, str) or len(value) > 1024 or not value.startswith("/"):
        return None
    path = urlsplit(value).path
    if not path or len(path) > 512 or any(ord(ch) < 32 for ch in path):
        return None
    return path


def clean_referrer(value: object) -> str:
    if not isinstance(value, str) or len(value) > 2048:
        return ""
    try:
        parsed = urlsplit(value)
        if parsed.scheme not in ("http", "https") or not parsed.hostname:
            return ""
        # Query strings, fragments and credentials often contain private data.
        host = parsed.hostname.lower()
        if ":" in host:
            host = f"[{host}]"
        if parsed.port:
            host += f":{parsed.port}"
        return urlunsplit((parsed.scheme, host, parsed.path[:512] or "/", "", ""))[:1024]
    except ValueError:
        return ""


def allowed_origin() -> bool:
    return request.headers.get("Origin", "") == SITE_ORIGIN


@app.after_request
def security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Robots-Tag"] = "noindex, nofollow"
    response.headers["Cache-Control"] = "no-store"
    if allowed_origin():
        response.headers["Access-Control-Allow-Origin"] = SITE_ORIGIN
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Vary"] = "Origin"
    return response


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/collect", methods=["POST", "OPTIONS"])
def collect():
    if request.method == "OPTIONS":
        return ("", 204) if allowed_origin() else ("", 403)
    if not allowed_origin():
        return ("", 403)
    if request.headers.get("DNT") == "1" or request.headers.get("Sec-GPC") == "1":
        return "", 204
    ua = request.headers.get("User-Agent", "")
    if BOT_RE.search(ua):
        return "", 204
    try:
        payload = json.loads(request.get_data(cache=False, as_text=True))
    except (ValueError, UnicodeError):
        return "", 400
    if not isinstance(payload, dict) or payload.get("type") != "pageview":
        return "", 400
    event_id = payload.get("event_id")
    visitor_id = payload.get("visitor_id")
    visit_id = payload.get("visit_id")
    path = clean_path(payload.get("path"))
    if not all(valid_uuid(value) for value in (event_id, visitor_id, visit_id)) or path is None:
        return "", 400
    referrer = clean_referrer(payload.get("referrer", ""))
    ip = client_ip()
    country_code, country_name = country_for_ip(ip)
    operating_system, browser, device = user_agent_details(ua)
    now = int(time.time())
    db = db_for_request()
    try:
        db.execute("BEGIN IMMEDIATE")
        if db.execute("SELECT 1 FROM pageviews WHERE id=?", (event_id,)).fetchone():
            db.rollback()
            return "", 204
        minute = now // 60
        db.execute(
            "INSERT OR IGNORE INTO collector_rate(ip_address, minute, hits) VALUES (?,?,0)",
            (ip, minute),
        )
        if db.execute(
            "UPDATE collector_rate SET hits=hits+1 WHERE ip_address=? AND minute=? AND hits<?",
            (ip, minute, COLLECTOR_PER_MINUTE),
        ).rowcount == 0:
            db.rollback()
            return "", 204
        visit = db.execute("SELECT visitor_id FROM visits WHERE id=?", (visit_id,)).fetchone()
        if visit and visit["visitor_id"] != visitor_id:
            db.rollback()
            return "", 400
        if visit is None:
            visitor = db.execute("SELECT visit_count FROM visitors WHERE id=?", (visitor_id,)).fetchone()
            if visitor is None:
                visit_number = 1
                db.execute(
                    "INSERT INTO visitors(id, first_seen, last_seen, visit_count) VALUES (?,?,?,1)",
                    (visitor_id, now, now),
                )
            else:
                visit_number = visitor["visit_count"] + 1
                db.execute(
                    "UPDATE visitors SET last_seen=?, visit_count=? WHERE id=?",
                    (now, visit_number, visitor_id),
                )
            db.execute(
                """INSERT INTO visits
                   (id, visitor_id, started_at, last_seen, visit_number, first_path,
                    last_path, referrer_url, ip_address, country_code, country_name,
                    operating_system, browser, device, pageviews)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,0)""",
                (visit_id, visitor_id, now, now, visit_number, path, path, referrer,
                 ip, country_code, country_name, operating_system, browser, device),
            )
        else:
            db.execute(
                """UPDATE visits SET last_seen=?, last_path=?, ip_address=?,
                   country_code=?, country_name=?, operating_system=?, browser=?, device=?
                   WHERE id=?""",
                (now, path, ip, country_code, country_name, operating_system, browser,
                 device, visit_id),
            )
            db.execute("UPDATE visitors SET last_seen=? WHERE id=?", (now, visitor_id))
        db.execute(
            "INSERT INTO pageviews(id, visit_id, occurred_at, path, referrer_url) VALUES (?,?,?,?,?)",
            (event_id, visit_id, now, path, referrer),
        )
        db.execute("UPDATE visits SET pageviews=pageviews+1 WHERE id=?", (visit_id,))
        db.commit()
    except sqlite3.Error:
        db.rollback()
        app.logger.exception("Analytics insert failed")
        return "", 500
    return "", 204


def password_digest(password: str, salt: bytes) -> bytes:
    return hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1, dklen=32)


def authenticated_username() -> str | None:
    token = request.cookies.get(COOKIE_NAME, "")
    if not token or len(token) > 128:
        return None
    token_hash = hashlib.sha256(token.encode("ascii", "ignore")).hexdigest()
    row = db_for_request().execute(
        "SELECT username FROM auth_sessions WHERE token_hash=? AND expires_at>?",
        (token_hash, int(time.time())),
    ).fetchone()
    return row["username"] if row else None


def require_auth(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        user = authenticated_username()
        if user is None:
            return jsonify({"error": "Sign in required"}), 401
        return fn(user, *args, **kwargs)
    return wrapped


@app.route("/api/login", methods=["POST", "OPTIONS"])
def login():
    if request.method == "OPTIONS":
        return ("", 204) if allowed_origin() else ("", 403)
    if not allowed_origin():
        return jsonify({"error": "Forbidden"}), 403
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "Invalid request"}), 400
    username = str(payload.get("username", "")).strip().lower()[:64]
    password = payload.get("password", "")
    if not username or not isinstance(password, str) or len(password) > 1024:
        return jsonify({"error": "Invalid request"}), 400
    now = int(time.time())
    ip = client_ip()
    db = db_for_request()
    failures = db.execute(
        "SELECT COUNT(*) FROM login_failures WHERE ip_address=? AND username=? AND occurred_at>?",
        (ip, username, now - 900),
    ).fetchone()[0]
    total_failures = db.execute(
        "SELECT COUNT(*) FROM login_failures WHERE ip_address=? AND occurred_at>?",
        (ip, now - 900),
    ).fetchone()[0]
    if failures >= 5 or total_failures >= 20:
        return jsonify({"error": "Too many attempts. Try again later."}), 429
    user = db.execute("SELECT salt, password_hash FROM users WHERE username=?", (username,)).fetchone()
    salt = user["salt"] if user else b"\0" * 16
    actual = password_digest(password, salt)
    if user is None or not hmac.compare_digest(actual, user["password_hash"]):
        with db:
            db.execute(
                "INSERT INTO login_failures(ip_address, username, occurred_at) VALUES (?,?,?)",
                (ip, username, now),
            )
        return jsonify({"error": "Incorrect username or password"}), 401
    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode("ascii")).hexdigest()
    with db:
        db.execute("DELETE FROM login_failures WHERE ip_address=? AND username=?", (ip, username))
        db.execute(
            "INSERT INTO auth_sessions(token_hash, username, expires_at) VALUES (?,?,?)",
            (token_hash, username, now + SESSION_SECONDS),
        )
    response = make_response(jsonify({"username": username}))
    response.set_cookie(
        COOKIE_NAME, token, max_age=SESSION_SECONDS, secure=True, httponly=True,
        samesite="Lax", path="/",
    )
    return response


@app.route("/api/logout", methods=["POST", "OPTIONS"])
def logout():
    if request.method == "OPTIONS":
        return ("", 204) if allowed_origin() else ("", 403)
    if not allowed_origin():
        return jsonify({"error": "Forbidden"}), 403
    token = request.cookies.get(COOKIE_NAME, "")
    if token:
        with db_for_request() as db:
            db.execute(
                "DELETE FROM auth_sessions WHERE token_hash=?",
                (hashlib.sha256(token.encode("ascii", "ignore")).hexdigest(),),
            )
    response = make_response("", 204)
    response.delete_cookie(COOKIE_NAME, secure=True, httponly=True, samesite="Lax", path="/")
    return response


@app.route("/api/me", methods=["GET"])
@require_auth
def me(username: str):
    return jsonify({"username": username})


def rows_to_dicts(rows):
    return [dict(row) for row in rows]


@app.route("/api/summary", methods=["GET"])
@require_auth
def summary(_username: str):
    try:
        days = int(request.args.get("days", "7"))
    except ValueError:
        return jsonify({"error": "Invalid range"}), 400
    if days not in (1, 7, 30, 90):
        return jsonify({"error": "Invalid range"}), 400
    now = int(time.time())
    cutoff = now - days * 86400
    db = db_for_request()
    metrics = db.execute(
        """SELECT COUNT(*) AS visits, COUNT(DISTINCT visitor_id) AS visitors,
           SUM(CASE WHEN visit_number > 1 THEN 1 ELSE 0 END) AS return_visits
           FROM visits WHERE started_at>=?""", (cutoff,),
    ).fetchone()
    pageviews = db.execute("SELECT COUNT(*) FROM pageviews WHERE occurred_at>=?", (cutoff,)).fetchone()[0]
    active = db.execute("SELECT COUNT(*) FROM visits WHERE last_seen>=?", (now - 300,)).fetchone()[0]
    trend = rows_to_dicts(db.execute(
        """WITH daily_visits AS (
               SELECT date(started_at, 'unixepoch') AS day, COUNT(*) AS visits,
                      COUNT(DISTINCT visitor_id) AS visitors
               FROM visits WHERE started_at>=? GROUP BY day
           ), daily_pageviews AS (
               SELECT date(occurred_at, 'unixepoch') AS day, COUNT(*) AS pageviews
               FROM pageviews WHERE occurred_at>=? GROUP BY day
           ), days AS (
               SELECT day FROM daily_visits UNION SELECT day FROM daily_pageviews
           )
           SELECT days.day, COALESCE(v.visits, 0) AS visits,
                  COALESCE(v.visitors, 0) AS visitors,
                  COALESCE(p.pageviews, 0) AS pageviews
           FROM days LEFT JOIN daily_visits v USING (day)
                     LEFT JOIN daily_pageviews p USING (day)
           ORDER BY days.day""", (cutoff, cutoff),
    ).fetchall())
    countries = rows_to_dicts(db.execute(
        """SELECT country_code AS code, country_name AS name,
           COUNT(*) AS visits, COUNT(DISTINCT visitor_id) AS visitors
           FROM visits WHERE started_at>=? GROUP BY country_code, country_name
           ORDER BY visits DESC, name LIMIT 250""", (cutoff,),
    ).fetchall())
    pages = rows_to_dicts(db.execute(
        """SELECT path, COUNT(*) AS pageviews FROM pageviews WHERE occurred_at>=?
           GROUP BY path ORDER BY pageviews DESC, path LIMIT 12""", (cutoff,),
    ).fetchall())
    referrers = rows_to_dicts(db.execute(
        """SELECT CASE WHEN referrer_url='' THEN 'Direct / unknown'
           ELSE referrer_url END AS url, COUNT(*) AS visits
           FROM visits WHERE started_at>=? GROUP BY url
           ORDER BY visits DESC, url LIMIT 12""", (cutoff,),
    ).fetchall())
    browsers = rows_to_dicts(db.execute(
        """SELECT browser AS name, COUNT(*) AS visits FROM visits WHERE started_at>=?
           GROUP BY browser ORDER BY visits DESC LIMIT 8""", (cutoff,),
    ).fetchall())
    operating_systems = rows_to_dicts(db.execute(
        """SELECT operating_system AS name, COUNT(*) AS visits
           FROM visits WHERE started_at>=? GROUP BY operating_system
           ORDER BY visits DESC LIMIT 8""", (cutoff,),
    ).fetchall())
    recent = rows_to_dicts(db.execute(
        """SELECT id, visitor_id, started_at, last_seen, visit_number,
           first_path, last_path, referrer_url, ip_address, country_code,
           country_name, operating_system, browser, device, pageviews
           FROM visits WHERE started_at>=? ORDER BY started_at DESC LIMIT 60""", (cutoff,),
    ).fetchall())
    return jsonify({
        "days": days, "generated_at": now,
        "metrics": {
            "active_now": active, "visitors": metrics["visitors"],
            "visits": metrics["visits"], "return_visits": metrics["return_visits"] or 0,
            "pageviews": pageviews,
        },
        "trend": trend, "countries": countries, "pages": pages,
        "referrers": referrers, "browsers": browsers,
        "operating_systems": operating_systems, "recent": recent,
    })


def create_user(username: str) -> None:
    username = username.strip().lower()
    if not re.fullmatch(r"[a-z0-9_.-]{2,64}", username):
        raise SystemExit("Username must be 2-64 letters, numbers, dots, dashes, or underscores")
    password = getpass.getpass("New password: ")
    if len(password) < 16:
        raise SystemExit("Use at least 16 characters")
    if password != getpass.getpass("Confirm password: "):
        raise SystemExit("Passwords did not match")
    salt = secrets.token_bytes(16)
    with connect() as db:
        db.execute(
            """INSERT INTO users(username, salt, password_hash, created_at)
               VALUES (?,?,?,?) ON CONFLICT(username) DO UPDATE SET
               salt=excluded.salt, password_hash=excluded.password_hash""",
            (username, salt, password_digest(password, salt), int(time.time())),
        )
        db.execute("DELETE FROM auth_sessions WHERE username=?", (username,))
    print(f"User {username} is ready")


def purge() -> None:
    now = int(time.time())
    raw_cutoff = now - RAW_RETENTION_DAYS * 86400
    visitor_cutoff = now - VISITOR_RETENTION_DAYS * 86400
    with connect() as db:
        db.execute("DELETE FROM pageviews WHERE occurred_at<?", (raw_cutoff,))
        db.execute("DELETE FROM visits WHERE last_seen<?", (raw_cutoff,))
        db.execute("DELETE FROM visitors WHERE last_seen<?", (visitor_cutoff,))
        db.execute("DELETE FROM auth_sessions WHERE expires_at<?", (now,))
        db.execute("DELETE FROM login_failures WHERE occurred_at<?", (now - 900,))
        db.execute("DELETE FROM collector_rate WHERE minute<?", ((now - 86400) // 60,))
    print("Expired analytics and sessions removed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Intersignal analytics administration")
    sub = parser.add_subparsers(dest="command", required=True)
    user_cmd = sub.add_parser("create-user", help="Create or rotate a dashboard login")
    user_cmd.add_argument("username")
    sub.add_parser("purge", help="Apply data retention limits")
    args = parser.parse_args()
    if args.command == "create-user":
        create_user(args.username)
    elif args.command == "purge":
        purge()
