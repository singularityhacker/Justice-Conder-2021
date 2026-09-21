(function () {
  // Theme experiments were removed from the public site.
  try {
    document.documentElement.removeAttribute("data-theme");
  } catch (e) {}
  function removeSwitcher() {
    var existing = document.getElementById("look-switcher");
    if (existing && existing.parentNode) existing.parentNode.removeChild(existing);
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", removeSwitcher);
  } else {
    removeSwitcher();
  }
})();
