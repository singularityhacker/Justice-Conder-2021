(function () {
  var eraButtons = Array.prototype.slice.call(document.querySelectorAll(".blog-filter"));
  var tagButtons = Array.prototype.slice.call(document.querySelectorAll(".blog-tag-filter"));
  var sortButtons = Array.prototype.slice.call(document.querySelectorAll(".blog-sort-btn"));
  var cards = Array.prototype.slice.call(document.querySelectorAll(".blog-card"));
  var list = document.getElementById("blog-list");
  var empty = document.getElementById("blog-empty");
  var count = document.getElementById("blog-count");
  var initialIndex = new Map();
  cards.forEach(function (card, index) {
    initialIndex.set(card, index);
  });

  function requested() {
    var params = new URLSearchParams(window.location.search);
    var hash = (window.location.hash || "").replace(/^#/, "");
    var era = params.get("project") || hash || "all";
    var tag = params.get("tag") || "all";
    var sort = params.get("sort") === "oldest" ? "oldest" : "newest";
    if (!era) era = "all";
    if (!tag) tag = "all";
    return { era: era, tag: tag, sort: sort };
  }

  function cardTags(card) {
    return (card.getAttribute("data-tags") || "").trim().split(/\s+/).filter(Boolean);
  }

  function applyOrder(sort) {
    if (!list) return;
    var ordered = cards.slice().sort(function (a, b) {
      var da = a.getAttribute("data-date") || "";
      var db = b.getAttribute("data-date") || "";
      if (da !== db) {
        if (sort === "oldest") return da < db ? -1 : 1;
        return da > db ? -1 : 1;
      }
      var ia = initialIndex.get(a);
      var ib = initialIndex.get(b);
      return sort === "oldest" ? ib - ia : ia - ib;
    });
    ordered.forEach(function (card) {
      list.appendChild(card);
    });
  }

  function applyFilters(era, tag, sort, push) {
    if (sort !== "oldest") sort = "newest";
    applyOrder(sort);
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
    sortButtons.forEach(function (btn) {
      btn.classList.toggle("is-active", btn.getAttribute("data-sort") === sort);
    });

    if (push) {
      var url = new URL(window.location.href);
      if (era === "all") url.searchParams.delete("project");
      else url.searchParams.set("project", era);
      if (tag === "all") url.searchParams.delete("tag");
      else url.searchParams.set("tag", tag);
      if (sort === "oldest") url.searchParams.set("sort", "oldest");
      else url.searchParams.delete("sort");
      history.replaceState(null, "", url.pathname + url.search);
    }
  }

  function current() {
    var activeEra = document.querySelector(".blog-filter.is-active");
    var activeTag = document.querySelector(".blog-tag-filter.is-active");
    var activeSort = document.querySelector(".blog-sort-btn.is-active");
    return {
      era: (activeEra && activeEra.getAttribute("data-filter")) || "all",
      tag: (activeTag && activeTag.getAttribute("data-tag")) || "all",
      sort: (activeSort && activeSort.getAttribute("data-sort")) || "newest",
    };
  }

  eraButtons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var state = current();
      applyFilters(btn.getAttribute("data-filter"), state.tag, state.sort, true);
    });
  });
  tagButtons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var state = current();
      applyFilters(state.era, btn.getAttribute("data-tag"), state.sort, true);
    });
  });
  sortButtons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var state = current();
      applyFilters(state.era, state.tag, btn.getAttribute("data-sort"), true);
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
  applyFilters(start.era, start.tag, start.sort, false);
})();
