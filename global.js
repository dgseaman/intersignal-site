/* Private Intersignal analytics dashboard. Data comes only from our API. */
(() => {
  "use strict";
  const API = "https://stats.relay.intersignal.org";
  const $ = (id) => document.getElementById(id);
  const number = (value) => new Intl.NumberFormat().format(Number(value) || 0);
  const svgNS = "http://www.w3.org/2000/svg";
  let selectedDays = 7;
  let mapFeatures = null;
  let refreshTimer = null;
  let requestSerial = 0;

  async function api(path, options = {}) {
    const response = await fetch(API + path, {
      credentials: "include", mode: "cors", cache: "no-store", ...options,
    });
    let body = {};
    try { body = await response.json(); } catch { /* an empty response */ }
    if (!response.ok) {
      const error = new Error(body.error || `Request failed (${response.status})`);
      error.status = response.status;
      throw error;
    }
    return body;
  }

  function showLogin() {
    $("login-screen").hidden = false;
    $("dashboard").hidden = true;
    $("account-name").hidden = true;
    $("signout").hidden = true;
    if (refreshTimer) clearInterval(refreshTimer);
    refreshTimer = null;
  }

  function showDashboard(username) {
    $("account-name").textContent = username;
    $("account-name").hidden = false;
    $("signout").hidden = false;
    $("login-screen").hidden = true;
    $("dashboard").hidden = false;
    if (refreshTimer) clearInterval(refreshTimer);
    refreshTimer = setInterval(loadSummary, 60_000);
    loadSummary();
  }

  function rankList(id, rows, labelKey, valueKey, emptyMessage) {
    const list = $(id);
    list.replaceChildren();
    if (!rows.length) {
      const item = document.createElement("li");
      item.className = "empty-list";
      item.textContent = emptyMessage;
      list.append(item);
      return;
    }
    const max = Math.max(1, Number(rows[0][valueKey]) || 0);
    rows.forEach((row, index) => {
      const item = document.createElement("li");
      const label = document.createElement("span");
      const value = document.createElement("span");
      const bar = document.createElement("span");
      label.className = "rank-label";
      label.textContent = `${String(index + 1).padStart(2, "0")}  ${row[labelKey] || "Unknown"}`;
      label.title = row[labelKey] || "Unknown";
      value.className = "rank-value";
      value.textContent = number(row[valueKey]);
      bar.className = "rank-bar";
      bar.style.width = `${Math.max(1, (Number(row[valueKey]) || 0) / max * 100)}%`;
      item.append(label, value, bar);
      list.append(item);
    });
  }

  function renderTrend(rows, days) {
    const chart = $("trend-chart");
    chart.replaceChildren();
    const byDay = new Map(rows.map((row) => [row.day, Number(row.visits) || 0]));
    const dates = [];
    const end = new Date();
    end.setUTCHours(0, 0, 0, 0);
    const bars = days === 1 ? 2 : days;
    for (let offset = bars - 1; offset >= 0; offset--) {
      const date = new Date(end.getTime() - offset * 86_400_000);
      dates.push(date.toISOString().slice(0, 10));
    }
    const max = Math.max(1, ...dates.map((date) => byDay.get(date) || 0));
    dates.forEach((date) => {
      const count = byDay.get(date) || 0;
      const bar = document.createElement("div");
      bar.className = "trend-bar";
      bar.style.height = `${Math.max(1, count / max * 100)}%`;
      bar.title = `${date}: ${number(count)} visits`;
      chart.append(bar);
    });
    chart.setAttribute("aria-label", `${days} day visit trend; ${rows.reduce((sum, row) => sum + (Number(row.visits) || 0), 0)} visits`);
    const dateLabel = (date) => new Date(`${date}T12:00:00Z`).toLocaleDateString(undefined, {month: "short", day: "numeric", timeZone: "UTC"});
    $("trend-labels").replaceChildren();
    for (const text of [dateLabel(dates[0]), dateLabel(dates[dates.length - 1])]) {
      const span = document.createElement("span");
      span.textContent = text;
      $("trend-labels").append(span);
    }
  }

  function mapPoint(point) {
    const longitude = Math.max(-180, Math.min(180, Number(point[0]) || 0));
    const latitude = Math.max(-90, Math.min(90, Number(point[1]) || 0));
    return [((longitude + 180) / 360) * 1000, ((90 - latitude) / 180) * 500];
  }

  function ringPath(ring) {
    return ring.map((point, index) => {
      const [x, y] = mapPoint(point);
      return `${index ? "L" : "M"}${x.toFixed(2)},${y.toFixed(2)}`;
    }).join(" ") + " Z";
  }

  function geometryPath(geometry) {
    if (geometry.type === "Polygon") return geometry.coordinates.map(ringPath).join(" ");
    if (geometry.type === "MultiPolygon") return geometry.coordinates.flatMap((polygon) => polygon.map(ringPath)).join(" ");
    return "";
  }

  async function loadMap() {
    if (mapFeatures) return mapFeatures;
    const response = await fetch("/assets/analytics-world.geojson", {cache: "force-cache"});
    if (!response.ok) throw new Error("Map asset could not be loaded");
    const collection = await response.json();
    mapFeatures = collection.features;
    return mapFeatures;
  }

  async function renderMap(countries) {
    const features = await loadMap();
    const svg = $("world-map");
    svg.replaceChildren();
    const visitCounts = new Map(countries.map((row) => [row.code, Number(row.visits) || 0]));
    const max = Math.max(1, ...visitCounts.values());
    for (const latitude of [-60, -30, 0, 30, 60]) {
      const line = document.createElementNS(svgNS, "path");
      const y = mapPoint([0, latitude])[1];
      line.setAttribute("d", `M0,${y} H1000`);
      line.setAttribute("class", "map-graticule");
      svg.append(line);
    }
    for (const longitude of [-120, -60, 0, 60, 120]) {
      const line = document.createElementNS(svgNS, "path");
      const x = mapPoint([longitude, 0])[0];
      line.setAttribute("d", `M${x},0 V500`);
      line.setAttribute("class", "map-graticule");
      svg.append(line);
    }
    for (const feature of features) {
      const visits = visitCounts.get(feature.id) || 0;
      let shape;
      if (feature.geometry.type === "Point") {
        const [x, y] = mapPoint(feature.geometry.coordinates);
        shape = document.createElementNS(svgNS, "circle");
        shape.setAttribute("cx", x);
        shape.setAttribute("cy", y);
        shape.setAttribute("r", visits ? "3.5" : "1.6");
      } else {
        shape = document.createElementNS(svgNS, "path");
        shape.setAttribute("d", geometryPath(feature.geometry));
        shape.setAttribute("fill-rule", "evenodd");
      }
      shape.setAttribute("class", "map-country");
      if (visits) {
        shape.setAttribute("data-visits", String(visits));
        shape.setAttribute("data-level", String(Math.min(3, Math.max(1, Math.ceil(visits / max * 3)))));
      }
      const title = document.createElementNS(svgNS, "title");
      title.textContent = `${feature.properties.name}: ${number(visits)} visits`;
      shape.append(title);
      svg.append(shape);
    }
  }

  function appendCell(row, main, secondary = "", className = "") {
    const cell = document.createElement("td");
    const primary = document.createElement("span");
    primary.className = className;
    primary.textContent = main;
    cell.append(primary);
    if (secondary) {
      const small = document.createElement("span");
      small.className = "secondary";
      small.textContent = secondary;
      cell.append(small);
    }
    row.append(cell);
  }

  function renderRecent(visits) {
    const body = $("recent-body");
    body.replaceChildren();
    if (!visits.length) {
      const row = document.createElement("tr");
      const cell = document.createElement("td");
      cell.className = "empty-table";
      cell.colSpan = 6;
      cell.textContent = "No visits in this period";
      row.append(cell);
      body.append(row);
      return;
    }
    for (const visit of visits) {
      const row = document.createElement("tr");
      const when = new Date(visit.started_at * 1000);
      appendCell(row, when.toLocaleString(), `${number(visit.pageviews)} ${visit.pageviews === 1 ? "pageview" : "pageviews"}`);
      appendCell(row, visit.ip_address || "Unknown", visit.country_name || "Unknown", "ip");
      appendCell(row, visit.browser || "Unknown", visit.operating_system || "Unknown");
      appendCell(row, visit.first_path || "/", visit.last_path !== visit.first_path ? `Last: ${visit.last_path}` : "", "truncate");
      appendCell(row, visit.referrer_url || "Direct / unknown", "", "truncate");
      const visitCell = document.createElement("td");
      const badge = document.createElement("span");
      badge.className = "return-pill";
      badge.textContent = visit.visit_number > 1 ? `Return #${visit.visit_number - 1}` : "First visit";
      visitCell.append(badge);
      row.append(visitCell);
      body.append(row);
    }
  }

  function renderSummary(data) {
    const metrics = data.metrics;
    for (const [id, key] of [["metric-active", "active_now"], ["metric-visitors", "visitors"], ["metric-visits", "visits"], ["metric-return", "return_visits"], ["metric-pages", "pageviews"]]) {
      $(id).textContent = number(metrics[key]);
    }
    rankList("countries-list", data.countries, "name", "visits", "No country data yet");
    rankList("pages-list", data.pages, "path", "pageviews", "No pageviews yet");
    rankList("sources-list", data.referrers, "url", "visits", "No referrers yet");
    rankList("browsers-list", data.browsers, "name", "visits", "No browser data yet");
    rankList("systems-list", data.operating_systems, "name", "visits", "No operating system data yet");
    renderTrend(data.trend, data.days);
    renderRecent(data.recent);
    renderMap(data.countries).catch((error) => {
      $("map-note").textContent = error.message;
    });
    $("updated-at").textContent = `Updated ${new Date(data.generated_at * 1000).toLocaleTimeString()}`;
  }

  async function loadSummary() {
    const serial = ++requestSerial;
    try {
      const data = await api(`/api/summary?days=${selectedDays}`);
      if (serial !== requestSerial) return;
      $("dashboard-error").hidden = true;
      renderSummary(data);
    } catch (error) {
      if (error.status === 401) return showLogin();
      $("dashboard-error").textContent = `Could not load stats: ${error.message}`;
      $("dashboard-error").hidden = false;
    }
  }

  $("login-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const button = $("login-form").querySelector("button");
    const errorText = $("login-error");
    errorText.hidden = true;
    button.disabled = true;
    try {
      const result = await api("/api/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username: $("username").value, password: $("password").value}),
      });
      $("password").value = "";
      showDashboard(result.username);
    } catch (error) {
      errorText.textContent = error.message;
      errorText.hidden = false;
    } finally {
      button.disabled = false;
    }
  });

  $("signout").addEventListener("click", async () => {
    try { await api("/api/logout", {method: "POST"}); } catch { /* close local view */ }
    showLogin();
  });

  for (const button of document.querySelectorAll("[data-days]")) {
    button.addEventListener("click", () => {
      selectedDays = Number(button.dataset.days);
      for (const candidate of document.querySelectorAll("[data-days]")) {
        candidate.setAttribute("aria-pressed", String(candidate === button));
      }
      loadSummary();
    });
  }

  api("/api/me").then((result) => showDashboard(result.username)).catch(showLogin);
})();
