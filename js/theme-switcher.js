(function () {
  var STORAGE_KEY = "jc-site-theme";
  var DEFAULT_THEME = "classic";

  var THEMES = [
    {
      id: "classic",
      name: "Classic",
      kind: "Original",
      blurb: "The current live site.",
      swatches: ["#282828", "#ffde00", "#ffffff", "#9ea8b6"]
    },
    {
      id: "atelier",
      name: "Atelier",
      kind: "Light",
      blurb: "Warm paper and editorial serif.",
      swatches: ["#f4efe6", "#b5451b", "#1f1a14", "#fffaf3"]
    },
    {
      id: "atelier-night",
      name: "Atelier Night",
      kind: "Dark",
      blurb: "The same editorial voice, lights down.",
      swatches: ["#161310", "#e8a87c", "#f0e6d8", "#221c18"]
    },
    {
      id: "signal",
      name: "Signal",
      kind: "Light",
      blurb: "Clean operator layout, more space.",
      swatches: ["#f7f8fb", "#4f46e5", "#111827", "#ffffff"]
    },
    {
      id: "signal-night",
      name: "Signal Night",
      kind: "Dark",
      blurb: "Midnight indigo with glass cards.",
      swatches: ["#0b1020", "#818cf8", "#e8eaf4", "#141a2e"]
    },
    {
      id: "terminal",
      name: "Terminal",
      kind: "Dark",
      blurb: "CRT green. Hacker default.",
      swatches: ["#070a08", "#3dff8a", "#c8f0d0", "#0d1410"]
    }
  ];

  var ids = THEMES.map(function (theme) {
    return theme.id;
  });

  function isTheme(id) {
    return ids.indexOf(id) !== -1;
  }

  function requestedTheme() {
    try {
      var query = new URLSearchParams(window.location.search).get("theme");
      if (isTheme(query)) return query;
    } catch (e) {}
    try {
      var stored = localStorage.getItem(STORAGE_KEY);
      if (isTheme(stored)) return stored;
    } catch (e) {}
    return DEFAULT_THEME;
  }

  function persistTheme(id) {
    try {
      localStorage.setItem(STORAGE_KEY, id);
    } catch (e) {}
    try {
      var url = new URL(window.location.href);
      if (url.searchParams.has("theme")) {
        if (id === DEFAULT_THEME) url.searchParams.delete("theme");
        else url.searchParams.set("theme", id);
        window.history.replaceState({}, "", url);
      }
    } catch (e) {}
  }

  function applyTheme(id) {
    if (!isTheme(id)) id = DEFAULT_THEME;
    document.documentElement.setAttribute("data-theme", id);
    persistTheme(id);
    syncButtons(id);
  }

  function syncButtons(id) {
    var buttons = document.querySelectorAll("[data-look-id]");
    Array.prototype.forEach.call(buttons, function (button) {
      var active = button.getAttribute("data-look-id") === id;
      button.classList.toggle("is-active", active);
      button.setAttribute("aria-selected", active ? "true" : "false");
    });
  }

  function ensureFonts() {
    if (document.getElementById("jc-look-fonts")) return;
    var link = document.createElement("link");
    link.id = "jc-look-fonts";
    link.rel = "stylesheet";
    link.href =
      "https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&family=Source+Serif+4:opsz,ital,wght@8..60,0,400;8..60,0,600;8..60,1,400&family=Space+Grotesk:wght@500;600;700&display=swap";
    document.head.appendChild(link);
  }

  function swatches(theme) {
    return theme.swatches
      .map(function (color) {
        return '<span class="look-swatch" style="background:' + color + '"></span>';
      })
      .join("");
  }

  function renderPanel() {
    if (document.getElementById("look-switcher")) return;

    var root = document.createElement("div");
    root.id = "look-switcher";
    root.className = "look-switcher";

    var options = THEMES.map(function (theme) {
      return (
        '<button type="button" role="option" class="look-option" data-look-id="' +
        theme.id +
        '" aria-selected="false">' +
        '<span class="look-option-swatches">' +
        swatches(theme) +
        "</span>" +
        '<span class="look-option-copy">' +
        '<span class="look-option-name">' +
        theme.name +
        '</span><span class="look-option-kind">' +
        theme.kind +
        "</span>" +
        '<span class="look-option-blurb">' +
        theme.blurb +
        "</span></span></button>"
      );
    }).join("");

    root.innerHTML =
      '<button type="button" class="look-toggle" aria-expanded="false" aria-controls="look-switcher-panel">' +
      '<span class="look-toggle-mark" aria-hidden="true"></span>' +
      '<span class="look-toggle-label">Looks</span></button>' +
      '<div class="look-panel" id="look-switcher-panel" hidden>' +
      '<div class="look-panel-head">' +
      "<div><p class=\"look-kicker\">Review</p><h2>Site looks</h2>" +
      "<p class=\"look-lede\">Preview redesigns on the live pages. Copy is unchanged. Your pick stays on this device.</p></div>" +
      '<button type="button" class="look-close" aria-label="Close looks panel">Close</button></div>' +
      '<div class="look-list" role="listbox" aria-label="Site looks">' +
      options +
      "</div></div>";

    document.body.appendChild(root);

    var toggle = root.querySelector(".look-toggle");
    var panel = root.querySelector(".look-panel");
    var close = root.querySelector(".look-close");

    function setOpen(open) {
      root.classList.toggle("is-open", open);
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      if (open) panel.removeAttribute("hidden");
      else panel.setAttribute("hidden", "");
    }

    toggle.addEventListener("click", function () {
      setOpen(!root.classList.contains("is-open"));
    });
    close.addEventListener("click", function () {
      setOpen(false);
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") setOpen(false);
    });
    document.addEventListener("click", function (event) {
      if (!root.contains(event.target)) setOpen(false);
    });

    Array.prototype.forEach.call(root.querySelectorAll("[data-look-id]"), function (button) {
      button.addEventListener("click", function () {
        applyTheme(button.getAttribute("data-look-id"));
      });
    });

    syncButtons(document.documentElement.getAttribute("data-theme") || DEFAULT_THEME);
  }

  applyTheme(requestedTheme());
  ensureFonts();

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", renderPanel);
  } else {
    renderPanel();
  }
})();
