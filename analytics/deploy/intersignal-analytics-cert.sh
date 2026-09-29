#!/bin/sh
# Issue or renew the stats certificate using only the relay's existing :443.
set -eu
umask 077

domain=stats.relay.intersignal.org
state=/etc/intersignal-analytics-acme/production
certificate="$state/certificates/$domain.crt"
key="$state/certificates/$domain.key"
nginx_site=/etc/nginx/sites-enabled/intersignal-analytics-stats.conf
served_digest="$state/nginx-served-cert.sha256"

if [ -z "${ANALYTICS_ACME_EMAIL:-}" ]; then
    echo 'Set ANALYTICS_ACME_EMAIL in /etc/intersignal-analytics/acme.env' >&2
    exit 1
fi

if [ -e "$certificate" ] || [ -e "$key" ]; then
    if [ ! -s "$certificate" ] || [ ! -s "$key" ]; then
        echo 'Incomplete certificate pair; inspect the lego state before retrying' >&2
        exit 1
    fi
    /usr/bin/lego --email "$ANALYTICS_ACME_EMAIL" --domains "$domain" \
        --tls --tls.port 127.0.0.1:8444 --path "$state" renew --days 30
else
    /usr/bin/lego --email "$ANALYTICS_ACME_EMAIL" --domains "$domain" \
        --tls --tls.port 127.0.0.1:8444 --path "$state" --accept-tos run
fi

# Do not reload nginx with a missing, wrong-host, or near-expiry certificate.
/usr/bin/openssl x509 -in "$certificate" -noout -checkhost "$domain"
/usr/bin/openssl x509 -in "$certificate" -noout -checkend 604800

if [ -e "$nginx_site" ]; then
    current_digest=$(/usr/bin/sha256sum "$certificate" "$key")
    previous_digest=$(/usr/bin/cat "$served_digest" 2>/dev/null || true)
    if [ "$current_digest" != "$previous_digest" ]; then
        /usr/sbin/nginx -t
        /usr/bin/systemctl reload-or-restart nginx.service
        printf '%s\n' "$current_digest" > "$served_digest"
    fi
else
    echo 'Certificate ready; enable the nginx stats site to serve it'
fi
