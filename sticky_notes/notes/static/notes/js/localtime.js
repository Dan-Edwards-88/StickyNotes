// notes/static/notes/js/localtime.js
// Convert <time class="js-localtime" datetime="ISO8601-with-timezone"> to user locale.
// Optional: data-date-style, data-time-style, data-locale.
// Also updates when new nodes are added.


(function () {
  function applyLocalTimes(root = document) {
    root.querySelectorAll("time.js-localtime").forEach((el) => {
      const iso = el.getAttribute("datetime");
      if (!iso) return;
      const dt = new Date(iso); // expects ISO8601 with timezone (Django 'c')
      if (isNaN(dt)) return;

      const dateStyle = el.dataset.dateStyle || "medium";
      const timeStyle = el.dataset.timeStyle || "short";
      const locale = el.dataset.locale || undefined;

      el.textContent = new Intl.DateTimeFormat(locale, { dateStyle, timeStyle }).format(dt);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => applyLocalTimes());
  } else {
    applyLocalTimes();
  }

  new MutationObserver((muts) => {
    for (const m of muts) {
      for (const n of m.addedNodes) {
        if (n.nodeType === 1) applyLocalTimes(n);
      }
    }
  }).observe(document.documentElement, { childList: true, subtree: true });
})();
