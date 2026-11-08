// Light/dark toggle for the mockups. Loaded in <head> so the saved theme applies
// before first paint. Any element with [data-theme-toggle] flips the theme.
(function () {
  var STORAGE_KEY = "deh-theme";
  var root = document.documentElement;

  try {
    var saved = localStorage.getItem(STORAGE_KEY);
    if (saved === "light" || saved === "dark") {
      root.dataset.theme = saved;
    }
  } catch (error) {
    // Storage can be blocked (private mode); the system theme still applies.
  }

  function isDark() {
    if (root.dataset.theme) {
      return root.dataset.theme === "dark";
    }
    return window.matchMedia("(prefers-color-scheme: dark)").matches;
  }

  document.addEventListener("click", function (event) {
    var toggle = event.target.closest("[data-theme-toggle]");
    if (!toggle) {
      return;
    }
    var next = isDark() ? "light" : "dark";
    root.dataset.theme = next;
    try {
      localStorage.setItem(STORAGE_KEY, next);
    } catch (error) {
      // Ignore: the theme still changes for this page view.
    }
  });
})();
