(function () {
  var buttons = Array.prototype.slice.call(document.querySelectorAll(".blog-filter"));
  var cards = Array.prototype.slice.call(document.querySelectorAll(".blog-card"));
  var empty = document.getElementById("blog-empty");
  var count = document.getElementById("blog-count");

  function requestedFilter() {
    var hash = (window.location.hash || "").replace(/^#/, "");
    var query = new URLSearchParams(window.location.search).get("project") || "";
    var value = query || hash;
    if (!value || value === "all") return "all";
    return value;
  }

  function applyFilter(project, push) {
    var visible = 0;
    cards.forEach(function (card) {
      var match = project === "all" || card.getAttribute("data-project") === project;
      card.hidden = !match;
      card.classList.toggle("is-hidden-card", !match);
      if (match) visible += 1;
    });
    if (empty) empty.hidden = visible !== 0;
    if (count) {
      var label = project === "all" ? "writings" : "writings in this project";
      count.textContent = visible + " " + label;
    }
    buttons.forEach(function (btn) {
      btn.classList.toggle("is-active", btn.getAttribute("data-filter") === project);
    });
    if (push) {
      var url = new URL(window.location.href);
      if (project === "all") {
        url.searchParams.delete("project");
        history.replaceState(null, "", url.pathname + url.search);
      } else {
        url.searchParams.set("project", project);
        history.replaceState(null, "", url.pathname + url.search);
      }
    }
  }

  buttons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      applyFilter(btn.getAttribute("data-filter"), true);
    });
  });

  applyFilter(requestedFilter(), false);
})();
