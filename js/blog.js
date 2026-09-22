(function () {
  var eraButtons = Array.prototype.slice.call(document.querySelectorAll(".blog-filter"));
  var tagButtons = Array.prototype.slice.call(document.querySelectorAll(".blog-tag-filter"));
  var cards = Array.prototype.slice.call(document.querySelectorAll(".blog-card"));
  var empty = document.getElementById("blog-empty");
  var count = document.getElementById("blog-count");

  function requested() {
    var params = new URLSearchParams(window.location.search);
    var hash = (window.location.hash || "").replace(/^#/, "");
    var era = params.get("project") || hash || "all";
    var tag = params.get("tag") || "all";
    if (!era) era = "all";
    if (!tag) tag = "all";
    return { era: era, tag: tag };
  }

  function cardTags(card) {
    return (card.getAttribute("data-tags") || "").trim().split(/\s+/).filter(Boolean);
  }

  function applyFilters(era, tag, push) {
    var visible = 0;
    cards.forEach(function (card) {
      var eraMatch = era === "all" || card.getAttribute("data-project") === era;
      var tagMatch = tag === "all" || cardTags(card).indexOf(tag) !== -1;
      var match = eraMatch && tagMatch;
      card.hidden = !match;
      card.classList.toggle("is-hidden-card", !match);
      if (match) visible += 1;
    });
    if (empty) empty.hidden = visible !== 0;
    if (count) {
      var label = "writings";
      if (era !== "all" && tag !== "all") label = "writings in this era and topic";
      else if (era !== "all") label = "writings in this era";
      else if (tag !== "all") label = "writings on this topic";
      count.textContent = visible + " " + label;
    }

    eraButtons.forEach(function (btn) {
      btn.classList.toggle("is-active", btn.getAttribute("data-filter") === era);
    });
    tagButtons.forEach(function (btn) {
      btn.classList.toggle("is-active", btn.getAttribute("data-tag") === tag);
    });

    if (push) {
      var url = new URL(window.location.href);
      if (era === "all") url.searchParams.delete("project");
      else url.searchParams.set("project", era);
      if (tag === "all") url.searchParams.delete("tag");
      else url.searchParams.set("tag", tag);
      history.replaceState(null, "", url.pathname + url.search);
    }
  }

  function current() {
    var activeEra = document.querySelector(".blog-filter.is-active");
    var activeTag = document.querySelector(".blog-tag-filter.is-active");
    return {
      era: (activeEra && activeEra.getAttribute("data-filter")) || "all",
      tag: (activeTag && activeTag.getAttribute("data-tag")) || "all",
    };
  }

  eraButtons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      applyFilters(btn.getAttribute("data-filter"), current().tag, true);
    });
  });
  tagButtons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      applyFilters(current().era, btn.getAttribute("data-tag"), true);
    });
  });

  cards.forEach(function (card) {
    var link = card.querySelector("h3 a");
    if (!link) return;
    card.addEventListener("click", function (event) {
      if (event.target.closest("a")) return;
      window.location.href = link.getAttribute("href");
    });
  });

  var start = requested();
  applyFilters(start.era, start.tag, false);
})();
