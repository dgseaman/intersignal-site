# Intersignal Global

This is a first-party web counter for `intersignal.org`. The site serves `global.html` as an unlisted, `noindex` sign-in page. Raw stats are returned only by the authenticated API at `https://stats.relay.intersignal.org`; `noindex` is not the access control.

The tracker sends page paths, referrer URLs without query strings or fragments, a random browser ID, and a 30-minute visit ID. The collector records the visitor IP, IP-derived country, browser, and operating system. It honors browser DNT and Global Privacy Control signals and the site opt-out setting. It does not call a third-party analytics service or map tile provider.

SQLite lives on the DigitalOcean relay droplet at `/var/lib/intersignal-analytics/analytics.sqlite3`, outside GitHub and Render. The dashboard requires individual username/password accounts. Session cookies are Secure, HttpOnly, SameSite Lax, and expire after seven days. Raw visit/pageview data is purged after 90 days; browser IDs and cumulative visit counts after 400 days. The daily systemd timer in `deploy/` applies retention.

## Service layout

- `app.py`: Flask collector, sign-in, and summary API.
- `tracker.js`: first-party browser counter used by public pages.
- `deploy/`: systemd, nginx, and HAProxy configuration used on the droplet.
- `../global.*`: dashboard shell, styling, and client code.
- `../assets/analytics-world.geojson`: local Natural Earth country shapes.

The existing HAProxy TLS router keeps its relay backends. Its SNI route for `stats.relay.intersignal.org` forwards TCP to loopback nginx with PROXY v1; nginx terminates HTTPS and overwrites `X-Real-IP` using the trusted PROXY address before forwarding to Gunicorn on loopback. Do not expose port 8788 or 8443 externally, and do not forward an untrusted client-supplied `X-Real-IP`. Nginx access logging is disabled because the analytics database already contains the needed IP data.

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
