/* Intersignal first-party page counter. No third-party requests or fingerprinting. */
(() => {
  "use strict";
  const script = document.currentScript;
  const endpoint = script && script.dataset.endpoint;
  if (!endpoint || navigator.globalPrivacyControl === true ||
      navigator.doNotTrack === "1" || navigator.doNotTrack === "yes") return;

  const visitorKey = "intersignal.analytics.visitor.v1";
  const visitKey = "intersignal.analytics.visit.v1";
  const optOutKey = "intersignal.analytics.optout";
  const visitIdleMs = 30 * 60 * 1000;
  const visitorLifeMs = 400 * 24 * 60 * 60 * 1000;
  const id = () => crypto.randomUUID();

  function read(key) {
    try { return JSON.parse(localStorage.getItem(key) || "null"); }
    catch { return null; }
  }
  function save(key, value) {
    try { localStorage.setItem(key, JSON.stringify(value)); } catch { /* storage disabled */ }
  }
  function referrer() {
    try {
      const url = new URL(document.referrer);
      return url.origin + url.pathname; // Never transmit query strings or fragments.
    } catch { return ""; }
  }
  function identities() {
    const now = Date.now();
    let visitor = read(visitorKey);
    if (!visitor || typeof visitor.id !== "string" || visitor.expires < now) {
      visitor = { id: id(), expires: now + visitorLifeMs };
      save(visitorKey, visitor);
    }
    let visit = read(visitKey);
    if (!visit || typeof visit.id !== "string" || now - visit.last > visitIdleMs) {
      visit = { id: id(), last: now };
    } else {
      visit.last = now;
    }
    save(visitKey, visit);
    return { visitor_id: visitor.id, visit_id: visit.id };
  }
  function track() {
    try {
      if (localStorage.getItem(optOutKey) === "1") return;
    } catch { /* storage disabled */ }
    const payload = JSON.stringify({
      type: "pageview", event_id: id(), ...identities(),
      path: location.pathname, referrer: referrer(),
    });
    const body = new Blob([payload], { type: "text/plain" });
    if (!navigator.sendBeacon || !navigator.sendBeacon(endpoint, body)) {
      fetch(endpoint, { method: "POST", body, mode: "cors", keepalive: true }).catch(() => {});
    }
  }

  let lastPath = location.pathname;
  function routeChanged() {
    if (location.pathname === lastPath) return;
    lastPath = location.pathname;
    track();
  }
  for (const method of ["pushState", "replaceState"]) {
    const original = history[method];
    history[method] = function (...args) {
      const result = original.apply(this, args);
      routeChanged();
      return result;
    };
  }
  window.addEventListener("popstate", routeChanged);
  window.addEventListener("pageshow", (event) => { if (event.persisted) track(); });
  track();
})();
