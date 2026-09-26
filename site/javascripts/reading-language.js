(() => {
  // Both editions share section IDs, so switching keeps the current section.
  document.querySelectorAll("a[data-reading-language]").forEach((link) => {
    const target = new URL(link.href);
    const update = () => {
      target.hash = window.location.hash;
      link.href = target.href;
    };
    update();
    window.addEventListener("hashchange", update);
  });
})();
