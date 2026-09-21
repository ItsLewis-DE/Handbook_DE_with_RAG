(() => {
  const header = document.querySelector(".custom-theme-header");
  const nav = header?.querySelector(".custom-header__nav");
  const activeLink = nav?.querySelector(".is-active");

  if (header) {
    const updateHeader = () => {
      document.documentElement.style.setProperty(
        "--site-header-offset", `${Math.ceil(header.getBoundingClientRect().height) + 12}px`,
      );
    };
    new ResizeObserver(updateHeader).observe(header);
    updateHeader();
  }

  if (activeLink) {
    // Reveal the current topic without changing the article's scroll position.
    const revealActiveLink = () => {
      const linkBox = activeLink.getBoundingClientRect();
      const navBox = nav.getBoundingClientRect();
      if (linkBox.left < navBox.left || linkBox.right > navBox.right) {
        nav.scrollLeft += linkBox.left - navBox.left - (navBox.width - linkBox.width) / 2;
      }
    };
    new ResizeObserver(revealActiveLink).observe(nav);
    document.fonts.ready.then(revealActiveLink);
  }

  document.querySelectorAll(".mobile-toc").forEach((toc) => {
    toc.addEventListener("click", (event) => {
      const link = event.target.closest("a");
      if (!link || event.defaultPrevented || event.button !== 0
        || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      // Collapse before the browser calculates the destination's position.
      toc.open = false;
      const target = document.getElementById(decodeURIComponent(link.hash.slice(1)));
      if (target) {
        target.setAttribute("tabindex", "-1");
        target.focus({ preventScroll: true });
      }
    });
  });
})();
