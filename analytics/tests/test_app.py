"""Behavioral checks for the private collector and dashboard API."""

from __future__ import annotations

import os
import sys
import tempfile
import time
import unittest
import uuid
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
_data_dir = tempfile.TemporaryDirectory()
os.environ["ANALYTICS_DB_PATH"] = str(Path(_data_dir.name) / "initial.sqlite3")
import app as analytics  # noqa: E402


SITE = "https://intersignal.org"
API = "https://stats.intersignal.org"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) "
      "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15")


class AnalyticsTests(unittest.TestCase):
    def setUp(self):
        self.db_path = Path(_data_dir.name) / f"{uuid.uuid4()}.sqlite3"
        analytics.DB_PATH = self.db_path
        analytics.init_db()
        self.client = analytics.app.test_client()
        self.visitor_id = str(uuid.uuid4())
        self.visit_id = str(uuid.uuid4())

    def event(self, **changes):
        event = {
            "type": "pageview",
            "event_id": str(uuid.uuid4()),
            "visitor_id": self.visitor_id,
            "visit_id": self.visit_id,
            "path": "/story?secret=discard",
            "referrer": "https://search.example/results?q=private#fragment",
        }
        event.update(changes)
        return event

    def collect(self, event=None, headers=None, remote_addr="127.0.0.1"):
        return self.client.post(
            "/collect", json=event or self.event(), base_url=API,
            headers={"Origin": SITE, "User-Agent": UA, "X-Real-IP": "8.8.8.8", **(headers or {})},
            environ_overrides={"REMOTE_ADDR": remote_addr},
        )

    def db_row(self, sql, params=()):
        with analytics.connect() as db:
            return db.execute(sql, params).fetchone()

    def create_user(self):
        salt = b"0123456789abcdef"
        with analytics.connect() as db:
            db.execute(
                "INSERT INTO users(username,salt,password_hash,created_at) VALUES(?,?,?,?)",
                ("council", salt, analytics.password_digest("long-secret-password", salt), int(time.time())),
            )

    def login(self):
        return self.client.post(
            "/api/login", json={"username": "council", "password": "long-secret-password"},
            headers={"Origin": SITE}, base_url=API,
        )

    def test_returning_visitor_and_duplicate_pageview(self):
        first = self.event()
        self.assertEqual(self.collect(first).status_code, 204)
        self.assertEqual(self.collect(first).status_code, 204)
        self.assertEqual(self.collect(self.event(path="/second")).status_code, 204)
        self.assertEqual(self.db_row("SELECT COUNT(*) FROM pageviews")[0], 2)
        visit = self.db_row("SELECT first_path,last_path,referrer_url,ip_address,visit_number,pageviews FROM visits")
        self.assertEqual(tuple(visit), (
            "/story", "/second", "https://search.example/results", "8.8.8.8", 1, 2,
        ))
        self.visit_id = str(uuid.uuid4())
        self.assertEqual(self.collect().status_code, 204)
        self.assertEqual(self.db_row("SELECT COUNT(*) FROM visitors")[0], 1)
        self.assertEqual(self.db_row("SELECT visit_count FROM visitors")[0], 2)
        self.assertEqual(self.db_row("SELECT visit_number FROM visits ORDER BY started_at DESC, rowid DESC LIMIT 1")[0], 2)

    def test_origin_privacy_bot_and_conflicting_visit(self):
        self.assertEqual(self.collect(headers={"Origin": "https://evil.example"}).status_code, 403)
        self.assertEqual(self.collect(headers={"DNT": "1"}).status_code, 204)
        self.assertEqual(self.collect(headers={"Sec-GPC": "1"}).status_code, 204)
        self.assertEqual(self.collect(headers={"User-Agent": "ExampleBot/1.0"}).status_code, 204)
        self.assertEqual(self.db_row("SELECT COUNT(*) FROM pageviews")[0], 0)
        self.assertEqual(self.collect().status_code, 204)
        self.assertEqual(self.collect(self.event(visitor_id=str(uuid.uuid4()))).status_code, 400)
        self.assertEqual(self.db_row("SELECT COUNT(*) FROM pageviews")[0], 1)

    def test_proxy_ip_trust_and_referrer_sanitization(self):
        self.assertEqual(self.collect(remote_addr="198.51.100.10").status_code, 204)
        self.assertEqual(self.db_row("SELECT ip_address FROM visits")[0], "198.51.100.10")
        self.assertEqual(
            analytics.clean_referrer("https://user:password@[2001:db8::1]:8443/path?token=123#top"),
            "https://[2001:db8::1]:8443/path",
        )
        self.assertEqual(analytics.clean_referrer("javascript:alert(1)"), "")

    def test_collector_rate_cap(self):
        original = analytics.COLLECTOR_PER_MINUTE
        analytics.COLLECTOR_PER_MINUTE = 2
        try:
            for _ in range(3):
                self.assertEqual(self.collect().status_code, 204)
            self.assertEqual(self.db_row("SELECT COUNT(*) FROM pageviews")[0], 2)
            self.assertEqual(self.db_row("SELECT hits FROM collector_rate")[0], 2)
        finally:
            analytics.COLLECTOR_PER_MINUTE = original

    def test_authentication_and_summary(self):
        self.assertEqual(self.client.get("/api/summary", base_url=API).status_code, 401)
        self.create_user()
        bad = self.client.post(
            "/api/login", json={"username": "council", "password": "incorrect"},
            headers={"Origin": SITE}, base_url=API,
        )
        self.assertEqual(bad.status_code, 401)
        logged_in = self.login()
        self.assertEqual(logged_in.status_code, 200)
        self.assertIn("Secure", logged_in.headers["Set-Cookie"])
        self.assertIn("HttpOnly", logged_in.headers["Set-Cookie"])
        self.assertEqual(self.client.get("/api/me", base_url=API).json["username"], "council")
        self.assertEqual(self.collect().status_code, 204)
        summary = self.client.get("/api/summary?days=7", base_url=API).json
        self.assertEqual(summary["metrics"]["visitors"], 1)
        self.assertEqual(summary["metrics"]["visits"], 1)
        self.assertEqual(summary["metrics"]["pageviews"], 1)
        self.assertEqual(summary["metrics"]["return_visits"], 0)
        self.assertEqual(summary["countries"][0]["code"], "US")
        self.assertEqual(summary["pages"][0]["path"], "/story")
        self.assertEqual(summary["recent"][0]["referrer_url"], "https://search.example/results")
        self.assertEqual(self.client.post("/api/logout", headers={"Origin": SITE}, base_url=API).status_code, 204)
        self.assertEqual(self.client.get("/api/me", base_url=API).status_code, 401)

    def test_login_limit_across_usernames(self):
        for index in range(20):
            result = self.client.post(
                "/api/login", json={"username": f"guess{index}", "password": "invalid"},
                headers={"Origin": SITE}, base_url=API,
            )
            self.assertEqual(result.status_code, 401)
        blocked = self.client.post(
            "/api/login", json={"username": "guess20", "password": "invalid"},
            headers={"Origin": SITE}, base_url=API,
        )
        self.assertEqual(blocked.status_code, 429)

    def test_trend_counts_pageviews_by_event_time(self):
        self.create_user()
        self.assertEqual(self.login().status_code, 200)
        self.assertEqual(self.collect().status_code, 204)
        with analytics.connect() as db:
            db.execute("UPDATE visits SET started_at=?", (int(time.time()) - 2 * 86400,))
        summary = self.client.get("/api/summary?days=1", base_url=API).json
        self.assertEqual(summary["metrics"]["visits"], 0)
        self.assertEqual(summary["metrics"]["pageviews"], 1)
        self.assertEqual(summary["trend"][-1]["visits"], 0)
        self.assertEqual(summary["trend"][-1]["pageviews"], 1)

    def test_purge_removes_expired_raw_data_but_retains_recent_visitor(self):
        self.assertEqual(self.collect().status_code, 204)
        old = int(time.time()) - 91 * 86400
        with analytics.connect() as db:
            db.execute("UPDATE visits SET started_at=?,last_seen=?", (old, old))
            db.execute("UPDATE pageviews SET occurred_at=?", (old,))
        analytics.purge()
        self.assertEqual(self.db_row("SELECT COUNT(*) FROM visits")[0], 0)
        self.assertEqual(self.db_row("SELECT COUNT(*) FROM pageviews")[0], 0)
        self.assertEqual(self.db_row("SELECT COUNT(*) FROM visitors")[0], 1)


if __name__ == "__main__":
    unittest.main()
