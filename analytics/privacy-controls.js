(() => {
  "use strict";
  const button = document.getElementById("optout-button");
  const status = document.getElementById("optout-status");
  const key = "intersignal.analytics.optout";
  function refresh() {
    const optedOut = localStorage.getItem(key) === "1";
    button.textContent = optedOut ? "Resume website counting" : "Opt out of website counting";
    status.textContent = optedOut ? "Website counting is off in this browser." : "Website counting is on in this browser, unless your browser sends a privacy signal.";
  }
  button.addEventListener("click", () => {
    try {
      if (localStorage.getItem(key) === "1") {
        localStorage.removeItem(key);
      } else {
        localStorage.setItem(key, "1");
        localStorage.removeItem("intersignal.analytics.visitor.v1");
        localStorage.removeItem("intersignal.analytics.visit.v1");
      }
      refresh();
    } catch {
      status.textContent = "This browser blocked the setting. Use Do Not Track or Global Privacy Control instead.";
    }
  });
  try { refresh(); } catch { status.textContent = "This browser does not allow local storage."; }
})();
