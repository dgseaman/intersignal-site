# Intersignal Global

This is an owner-controlled web counter for `intersignal.org` and the legacy `fulcrumnews.com` site. Intersignal serves `global.html` as an unlisted, `noindex` sign-in page. Raw stats are returned only by the authenticated API at `https://stats.relay.intersignal.org`; `noindex` is not the access control.

The tracker sends page paths, referrer URLs without query strings or fragments, a random browser ID, and a 30-minute visit ID. The collector records the visitor IP, IP-derived country, browser, and operating system. It honors browser DNT and Global Privacy Control signals and the site opt-out setting. It does not call a third-party analytics service or map tile provider.

The collector derives each event's site from its browser `Origin`, then stores `intersignal` or `fulcrumnews` with visitors, visits, and pageviews. It accepts `https://intersignal.org`, `https://www.intersignal.org`, `https://fulcrumnews.com`, and `https://www.fulcrumnews.com` by default. Set `ANALYTICS_FULCRUM_ORIGINS` to a comma-separated list of exact HTTPS origins if the legacy site's canonical address changes; an empty value disables collection from it. Dashboard sign-in and sign-out accept Intersignal origins only. The authenticated `/api/summary` endpoint defaults to `site=intersignal` and also accepts `site=fulcrumnews` or `site=all`. Existing single-site database rows are automatically assigned to `intersignal` on startup.

SQLite lives on the DigitalOcean relay droplet at `/var/lib/intersignal-analytics/analytics.sqlite3`, outside GitHub and Render. The dashboard requires individual username/password accounts. Session cookies are Secure, HttpOnly, SameSite Lax, and expire after seven days. Raw visit/pageview data is purged after 90 days; browser IDs and cumulative visit counts after 400 days. The daily systemd timer in `deploy/` applies retention.

## Service layout

- `app.py`: Flask collector, sign-in, and summary API.
- `tracker.js`: first-party browser counter used by public pages.
- `deploy/`: systemd, nginx, and HAProxy configuration used on the droplet.
- `../global.*`: dashboard shell, styling, and client code.
- `../assets/analytics-world.geojson`: local Natural Earth country shapes.

The existing HAProxy TLS router keeps its relay backends. Its SNI route for `stats.relay.intersignal.org` forwards ordinary HTTPS to loopback nginx with PROXY v1; nginx terminates HTTPS and overwrites `X-Real-IP` using the trusted PROXY address before forwarding to Gunicorn on loopback. A more specific SNI + `acme-tls/1` route forwards Let's Encrypt validation to a temporary lego listener, without PROXY protocol. This issues and renews the stats certificate through the already-open port 443. Do not expose ports 8443, 8444, or 8788 externally, and do not forward an untrusted client-supplied `X-Real-IP`. Nginx access logging is disabled because the analytics database already contains the needed IP data.

## Stats HTTPS on the relay

The deployment files target the relay's existing HAProxy TCP frontend on `:443`, Ubuntu's `lego` v4 CLI, and nginx. No port 80 listener or firewall change is needed.

1. Confirm that DNS for `stats.relay.intersignal.org` resolves to the droplet. Check both A and AAAA records; every published address must reach the same HAProxy TLS frontend. Keep the current relay backends and their SNI rules.
2. Add the two `use_backend` lines from `deploy/haproxy-stats.snippet` to the frontend that already inspects TLS ClientHello, before any broader SNI/default route. Add its two backend blocks. The ACME backend points to `127.0.0.1:8444` with **no** `send-proxy`; the ordinary stats backend points to nginx at `127.0.0.1:8443` **with** `send-proxy`. Validate with `haproxy -c -f /etc/haproxy/haproxy.cfg` before reloading HAProxy. The ACME listener exists only while lego issues or renews; it needs no health check.
3. Install `deploy/intersignal-analytics-cert.sh` as `/usr/local/sbin/intersignal-analytics-cert` with mode `0755`. Install the matching `.service` and `.timer` in `/etc/systemd/system/` with mode `0644`, then run `systemctl daemon-reload`. The service uses apt's `/usr/bin/lego` v4 and its `--tls.port 127.0.0.1:8444` option. Create `/etc/intersignal-analytics/acme.env`, owned by root with mode `0600`, containing `ANALYTICS_ACME_EMAIL=<working contact email>`. Its certificate and private key stay in the root-owned `/etc/intersignal-analytics-acme/production` directory, which must exist with mode `0700` before starting the service.
4. The relay already has successful staging and production certificates in `/etc/intersignal-analytics-acme/staging` and `/etc/intersignal-analytics-acme/production`, respectively. For a fresh deployment, optionally issue a **staging** certificate with lego's `--server https://acme-staging-v02.api.letsencrypt.org/directory`, `--tls --tls.port 127.0.0.1:8444`, and a separate `--path /etc/intersignal-analytics-acme/staging`. Do not point nginx at a staging certificate. Once the challenge succeeds, run `systemctl start intersignal-analytics-cert.service` to issue the production certificate; on the current relay, this performs a renewal check against the existing certificate.
5. Install `deploy/nginx-stats.conf` as `/etc/nginx/sites-available/intersignal-analytics-stats.conf`, then link it in `/etc/nginx/sites-enabled/`. Do this **after** the production certificate exists. Disable Ubuntu's default nginx site if it is still enabled, so nginx does not also bind port 80; confirm its only listener is the intended loopback `127.0.0.1:8443`. Validate with `nginx -t`, then enable and start nginx so it survives reboot. Enable `intersignal-analytics-cert.timer` so lego checks renewal daily. After a changed certificate, the script checks its name and expiry, validates nginx, and reloads it. A failed reload is retried on the next timer run.
6. Verify `https://stats.relay.intersignal.org/health` and recheck the existing relay hostnames over HTTPS after the HAProxy reload. A failed renewal leaves nginx serving its previous certificate and the timer retries the next day; inspect `journalctl -u intersignal-analytics-cert.service` if a renewal fails.

The certificate pair is `/etc/intersignal-analytics-acme/production/certificates/stats.relay.intersignal.org.{crt,key}`. lego's `.crt` includes the issuing chain. Keep the state directories mode `0700`; nginx's root master process reads the key. Back up the lego account and certificate state securely so renewal survives a droplet replacement.

Create or rotate dashboard credentials on the droplet with:

```sh
sudo -u intersignal-analytics env ANALYTICS_DB_PATH=/var/lib/intersignal-analytics/analytics.sqlite3 /opt/intersignal-analytics/.venv/bin/python /opt/intersignal-analytics/app.py create-user <username>
```

`ANALYTICS_COLLECTOR_PER_MINUTE` defaults to 180 accepted events per IP. `ANALYTICS_GEO_DB` points to an updated local GeoIP2Fast country file from the project's [public release](https://github.com/rabuchaim/geoip2fast/releases/tag/LATEST); refresh it periodically and restart the service. Country location is approximate. A browser ID can be reset if a visitor clears site storage, changes browser, or opts out; it is not a person identity.

## Local checks

```sh
python3.12 -m venv analytics/.venv
analytics/.venv/bin/pip install -r analytics/requirements.txt
analytics/.venv/bin/python -m unittest discover -s analytics/tests -v
node --check analytics/tracker.js
node --check global.js
```

The raw IP and persistent browser ID make this data sensitive. Keep the droplet backed up with restricted access, keep the credentials separate per human user, and update the site's visitor notice if collection or retention changes.
