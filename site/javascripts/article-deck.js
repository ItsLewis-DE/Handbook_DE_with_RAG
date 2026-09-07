(() => {
  const FLIP_DURATION = 620;
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  function initialiseDeck(deck) {
    if (deck.dataset.deckReady === "true") return;

    const shell = deck.closest(".article-deck-shell");
    const counter = shell?.parentElement?.querySelector(".article-deck__count b");
    const announcement = shell?.querySelector(".article-deck__announcement");
    const cards = Array.from(deck.querySelectorAll(".article-sheet"));

    if (!shell || cards.length < 2) return;

    const readingOrder = ["article-sheet--index", "article-sheet--storage", "article-sheet--airflow"];
    let order = cards.slice().sort((left, right) => {
      const leftPriority = readingOrder.findIndex((name) => left.classList.contains(name));
      const rightPriority = readingOrder.findIndex((name) => right.classList.contains(name));
      return (leftPriority === -1 ? readingOrder.length : leftPriority)
        - (rightPriority === -1 ? readingOrder.length : rightPriority);
    });
    let flipping = false;
    let pointerId = null;
    let startX = 0;
    let startY = 0;
    let currentX = 0;
    let startedAt = 0;
    let dragging = false;
    let suppressNextClick = false;

    const positions = ["current", "next", "back"];

    function render({ announce = false } = {}) {
      order.forEach((card, index) => {
        card.dataset.deckPosition = positions[index] || "hidden";
        card.setAttribute("aria-hidden", index === 0 ? "false" : "true");

        card.querySelectorAll("a").forEach((link) => {
          link.tabIndex = index === 0 ? 0 : -1;
        });
      });

      const pageNumber = order[0].querySelector(".article-sheet__meta b")?.textContent.split("/")[0].trim();
      if (counter && pageNumber) counter.textContent = pageNumber.padStart(2, "0");

      if (announce && announcement) {
        announcement.textContent = `Đang xem: ${order[0].dataset.articleTitle}`;
      }
    }

    function clearDragStyles() {
      deck.classList.remove("is-dragging");
      deck.style.removeProperty("--drag-x");
      deck.style.removeProperty("--drag-rotate");
      deck.style.removeProperty("--drag-progress");
      dragging = false;
      pointerId = null;
    }

    function flip(direction = "next") {
      if (flipping) return;

      flipping = true;
      const outgoing = direction === "next" ? order[0] : order.at(-1);
      deck.classList.remove("is-dragging");
      if (direction === "next") outgoing.classList.add("is-flipping");

      window.setTimeout(() => {
        outgoing.classList.remove("is-flipping");
        order = direction === "next"
          ? [...order.slice(1), outgoing]
          : [outgoing, ...order.slice(0, -1)];
        clearDragStyles();
        render({ announce: true });
        flipping = false;
      }, reducedMotion.matches ? 20 : FLIP_DURATION);
    }

    function cancelDrag() {
      if (!dragging) {
        pointerId = null;
        return;
      }

      suppressNextClick = true;
      clearDragStyles();
    }

    deck.addEventListener("pointerdown", (event) => {
      if (event.button !== 0 || flipping) return;

      pointerId = event.pointerId;
      startX = event.clientX;
      startY = event.clientY;
      currentX = startX;
      startedAt = performance.now();
      deck.setPointerCapture?.(event.pointerId);
    });

    deck.addEventListener("pointermove", (event) => {
      if (event.pointerId !== pointerId || flipping) return;

      const deltaX = event.clientX - startX;
      const deltaY = event.clientY - startY;

      if (!dragging && Math.abs(deltaY) > Math.abs(deltaX) && Math.abs(deltaY) > 8) {
        pointerId = null;
        return;
      }

      if (!dragging && deltaX > -4) return;

      dragging = true;
      currentX = event.clientX;
      const deckWidth = deck.getBoundingClientRect().width;
      const limitedX = Math.max(deltaX, -deckWidth * 0.78);
      const progress = Math.min(Math.max(-limitedX / deckWidth, 0), 1);

      deck.classList.add("is-dragging");
      deck.style.setProperty("--drag-x", `${limitedX}px`);
      deck.style.setProperty("--drag-rotate", `${progress * -58}deg`);
      deck.style.setProperty("--drag-progress", progress.toFixed(3));
      event.preventDefault();
    });

    deck.addEventListener("pointerup", (event) => {
      if (event.pointerId !== pointerId) return;

      const elapsed = Math.max(performance.now() - startedAt, 1);
      const deltaX = currentX - startX;
      const velocity = deltaX / elapsed;
      const threshold = deck.getBoundingClientRect().width * 0.22;
      const shouldFlip = dragging && (deltaX < -threshold || velocity < -0.5);

      suppressNextClick = dragging;
      shouldFlip ? flip() : cancelDrag();
    });

    deck.addEventListener("pointercancel", cancelDrag);
    deck.addEventListener("lostpointercapture", () => {
      if (!flipping && pointerId !== null) cancelDrag();
    });

    deck.addEventListener("click", (event) => {
      if (!suppressNextClick) return;
      event.preventDefault();
      event.stopPropagation();
      suppressNextClick = false;
    }, true);

    deck.addEventListener("keydown", (event) => {
      if (!["ArrowLeft", "ArrowRight", "Enter"].includes(event.key)) return;
      event.preventDefault();
      flip(event.key === "ArrowLeft" ? "previous" : "next");
    });

    shell.querySelectorAll("[data-deck-action]").forEach((control) => {
      control.addEventListener("click", () => flip(control.dataset.deckAction));
    });

    render();
    deck.dataset.deckReady = "true";
  }

  function initialiseAllDecks() {
    document.querySelectorAll(".article-deck").forEach(initialiseDeck);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialiseAllDecks, { once: true });
  } else {
    initialiseAllDecks();
  }
})();
