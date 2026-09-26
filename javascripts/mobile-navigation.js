(() => {
  const header = document.querySelector(".custom-theme-header");
  const panel = header?.querySelector("#library-panel");
  const toggle = header?.querySelector(".custom-header__library-toggle");
  const closeButton = panel?.querySelector(".library-panel__close");
  const mobileView = window.matchMedia("(max-width: 45rem)");

  if (header) {
    const updateHeader = () => {
      document.documentElement.style.setProperty(
        "--site-header-offset", `${Math.ceil(header.getBoundingClientRect().height) + 12}px`,
      );
    };
    if (window.ResizeObserver) {
      new ResizeObserver(updateHeader).observe(header);
    } else {
      window.addEventListener("resize", updateHeader);
    }
    updateHeader();
  }

  if (panel && toggle && closeButton) {
    const setOpen = (open, returnFocus = false) => {
      panel.hidden = !open;
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Đóng thư viện bài viết" : "Mở thư viện bài viết");
      if (!open && returnFocus) toggle.focus();
    };

    const syncGroups = () => {
      const groups = [...panel.querySelectorAll(".library-panel__group")];
      const selectedGroup = groups.find((group) => group.querySelector('[aria-current="page"]'))
        || groups.find((group) => group.querySelector(".library-panel__group-title")?.textContent.trim() === "Database Internals")
        || groups[0];
      groups.forEach((group) => {
        group.open = !mobileView.matches || group === selectedGroup;
      });
    };

    syncGroups();
    mobileView.addEventListener("change", syncGroups);

    toggle.addEventListener("click", () => setOpen(panel.hidden));
    closeButton.addEventListener("click", () => setOpen(false, true));

    document.addEventListener("pointerdown", (event) => {
      if (!panel.hidden && !panel.contains(event.target) && !toggle.contains(event.target)) {
        setOpen(false);
      }
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && !panel.hidden) {
        event.preventDefault();
        setOpen(false, true);
      }
    });

    panel.addEventListener("click", (event) => {
      if (event.target.closest("a")) setOpen(false);
    });
  }

  const searchLabel = header?.querySelector(".custom-header__search");
  searchLabel?.addEventListener("click", () => {
    requestAnimationFrame(() => {
      if (document.querySelector("#__search")?.checked) {
        header.querySelector(".md-search__input")?.focus();
      }
    });
  });

  searchLabel?.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      event.currentTarget.click();
    }
  });

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
