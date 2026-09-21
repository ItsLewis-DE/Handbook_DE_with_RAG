(() => {
  const siteRootUrl = new URL("../", document.currentScript.src);
  const endpoint = document.querySelector('meta[name="pip-chat-endpoint"]')?.content
    || "http://127.0.0.1:8001/chat";

  function robotMarkup(type = "full") {
    const isAvatar = type === "avatar";
    const isReading = type === "reading";
    const viewBox = isAvatar ? "12 -2 108 108" : isReading ? "7 0 106 150" : "0 0 120 150";

    return `<span class="pip-mascot pip-mascot--${type}" aria-hidden="true">
      <svg class="pip-svg" viewBox="${viewBox}" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <!-- 3D Clay Shading for Body -->
          <linearGradient id="pipBody3D_${type}" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#ffffff" />
            <stop offset="50%" stop-color="#f5f0e6" />
            <stop offset="100%" stop-color="#dfd4bf" />
          </linearGradient>
          <!-- 3D Book Gradient -->
          <linearGradient id="pipBook3D_${type}" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#df542b" />
            <stop offset="50%" stop-color="#ed6840" />
            <stop offset="100%" stop-color="#ff7d54" />
          </linearGradient>
          <filter id="pipGlow_${type}" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="1.2" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
          </filter>
        </defs>

        ${!isAvatar ? `<ellipse class="pip-shadow" cx="60" cy="${isReading ? 114 : 139}" rx="25" ry="3.2" fill="#17302d" opacity="0.16" />` : ''}

        <!-- Floating Puppet Rig -->
        <g class="pip-float-wrapper">
          ${isReading ? `
          <!-- Each leg swings from its knee while Pip sits on the bubble edge. -->
          <g class="pip-legs">
            <g class="pip-reading-leg pip-reading-leg--left">
              <path d="M 47 110 Q 43 121 45 136" fill="none" stroke="#22423d" stroke-width="8" stroke-linecap="round" />
              <ellipse cx="43" cy="138" rx="10" ry="6" fill="url(#pipBody3D_${type})" stroke="#52706a" stroke-width="1" />
            </g>
            <g class="pip-reading-leg pip-reading-leg--right">
              <path d="M 73 110 Q 77 121 75 136" fill="none" stroke="#22423d" stroke-width="8" stroke-linecap="round" />
              <ellipse cx="77" cy="138" rx="10" ry="6" fill="url(#pipBody3D_${type})" stroke="#52706a" stroke-width="1" />
            </g>
          </g>
          ` : !isAvatar ? `
          <!-- Legs & Feet -->
          <g class="pip-legs">
            <rect x="42" y="112" width="10" height="18" rx="5" fill="#22423d" />
            <path d="M 37 127 C 37 123, 52 123, 52 127 L 54 135 C 54 137, 35 137, 35 135 Z" fill="url(#pipBody3D_${type})" stroke="rgba(23,48,45,0.2)" stroke-width="1.2" />
            <rect x="35" y="133" width="19" height="3" rx="1.5" fill="#1b332f" />
            <rect x="68" y="112" width="10" height="18" rx="5" fill="#22423d" />
            <path d="M 68 127 C 68 123, 83 123, 83 127 L 85 135 C 85 137, 66 137, 66 135 Z" fill="url(#pipBody3D_${type})" stroke="rgba(23,48,45,0.2)" stroke-width="1.2" />
            <rect x="66" y="133" width="19" height="3" rx="1.5" fill="#1b332f" />
          </g>
          ` : ''}

          <g class="pip-upper-body">
          <!-- Torso Body (Crisp silhouette border) -->
          <g class="pip-torso">
            <rect x="52" y="62" width="16" height="8" rx="4" fill="#22423d" />
            <path d="M 40 70 C 40 64, 80 64, 80 70 C 86 85, 84 112, 60 114 C 36 112, 34 85, 40 70 Z" fill="url(#pipBody3D_${type})" stroke="rgba(23,48,45,0.22)" stroke-width="1.4" />
            <!-- Chest Button -->
            <circle cx="60" cy="88" r="6.5" fill="#ed6840" stroke="#c9441e" stroke-width="0.8" />
            <circle cx="58" cy="86" r="2" fill="#ffffff" opacity="0.85" />
          </g>

          ${!isAvatar ? `
          <!-- Book (Closed State - Held Firmly) -->
          <g class="pip-book-closed" style="transform-origin: 52px 96px;">
            <rect x="42" y="80" width="24" height="28" rx="3.5" fill="url(#pipBook3D_${type})" stroke="#b53e1b" stroke-width="1" />
            <rect x="62" y="82" width="4.5" height="24" rx="1.2" fill="#fffaf0" stroke="rgba(0,0,0,0.12)" stroke-width="0.8" />
            <line x1="48" y1="80" x2="48" y2="108" stroke="rgba(0,0,0,0.15)" stroke-width="1.2" />
          </g>

          <!-- Book (Open State - Reading) -->
          <g class="pip-book-open" style="transform-origin: 60px 96px;">
            <!-- One continuous cover and a shared spine keep the spread joined. -->
            <path d="M 34 80 Q 48 77 60 85 Q 72 77 86 80 L 86 103 Q 72 101 60 112 Q 48 101 34 103 Z" fill="url(#pipBook3D_${type})" stroke="#b53e1b" stroke-width="1" stroke-linejoin="round" />
            <path d="M 36 82 Q 49 80 60 87 L 60 109 Q 49 101 36 101 Z" fill="#fffaf0" />
            <path d="M 60 87 Q 71 80 84 82 L 84 101 Q 71 101 60 109 Z" fill="#f3ead8" />
            <path d="M 60 87 L 60 109" stroke="#c6ad89" stroke-width="1" />
            <path d="M 41 87 Q 48 87 54 90 M 41 92 Q 48 92 54 95 M 43 97 L 52 100 M 66 90 Q 72 87 79 87 M 66 95 Q 72 92 79 92 M 68 100 L 77 97" fill="none" stroke="#52706a" stroke-width="1" stroke-linecap="round" opacity="0.65" />
            ${isReading ? `
            <g class="pip-reading-page">
              <path d="M 60 87 Q 71 79 83 82 L 83 101 Q 71 101 60 109 Z" fill="#fffaf0" stroke="#c6ad89" stroke-width=".8" />
              <path d="M 65 90 Q 73 86 79 87 M 65 95 Q 73 91 79 92 M 66 100 L 76 97" fill="none" stroke="#52706a" stroke-width="1" opacity=".55" />
            </g>` : ''}
          </g>
          ` : ''}

          <!-- Left Arm (Clasping Book in full mode, Resting on hip in avatar mode) -->
          <g class="pip-arm-left" style="transform-origin: 36px 74px;">
            <circle cx="36" cy="74" r="6.5" fill="#22423d" />
            <path d="${isAvatar ? 'M 36 74 C 24 80, 26 90, 38 90' : 'M 36 76 C 26 84, 28 98, 42 98'}" stroke="url(#pipBody3D_${type})" stroke-width="8.5" stroke-linecap="round" fill="none" />
            <path d="${isAvatar ? 'M 36 74 C 24 80, 26 90, 38 90' : 'M 36 76 C 26 84, 28 98, 42 98'}" stroke="rgba(23,48,45,0.18)" stroke-width="1.2" fill="none" />
            <!-- Hand -->
            <ellipse cx="${isAvatar ? 38 : 43}" cy="${isAvatar ? 89 : 98}" rx="5" ry="5.5" fill="#22423d" />
            <!-- Fingers -->
            <circle cx="${isAvatar ? 37 : 45}" cy="${isAvatar ? 85 : 94}" r="2.2" fill="#2a4e48" />
            <circle cx="${isAvatar ? 40 : 46}" cy="${isAvatar ? 87 : 97}" r="2.2" fill="#2a4e48" />
            <circle cx="${isAvatar ? 41 : 45}" cy="${isAvatar ? 90 : 100}" r="2.2" fill="#2a4e48" />
          </g>

          <!-- Head Group (High Contrast & TV Screen) -->
          <g class="pip-head-group" style="transform-origin: 60px 65px;">
            <g class="pip-head-look">
            <!-- Antenna -->
            <g class="pip-antenna">
              <path d="M 60 24 L 60 13" stroke="#22423d" stroke-width="4.5" stroke-linecap="round" />
              <circle cx="60" cy="10" r="7" fill="#ed6840" stroke="#c9441e" stroke-width="0.8" />
              <circle cx="58" cy="8" r="2.2" fill="#ffffff" opacity="0.85" />
            </g>

            <!-- Ear Dials -->
            <rect x="22" y="35" width="6" height="16" rx="3" fill="#ed6840" stroke="#c9441e" stroke-width="0.8" />
            <rect x="92" y="35" width="6" height="16" rx="3" fill="#ed6840" stroke="#c9441e" stroke-width="0.8" />
            <circle cx="25" cy="43" r="5" fill="#22423d" />
            <circle cx="95" cy="43" r="5" fill="#22423d" />

            <!-- TV Head Outer Shell (Clear outline so it NEVER sinks into background) -->
            <rect x="25" y="21" width="70" height="46" rx="18" fill="url(#pipBody3D_${type})" stroke="rgba(23,48,45,0.22)" stroke-width="1.4" />
            <path d="M 38 23 Q 60 21 82 23" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" opacity="0.9" fill="none" />

            <!-- TV Screen (Dark slate teal for maximum contrast) -->
            <rect x="32" y="27" width="56" height="34" rx="12" fill="#102422" stroke="#081412" stroke-width="1" />
            <path d="M 35 29 Q 60 27 85 29 Q 75 35 37 37 Z" fill="#ffffff" opacity="0.14" />

            <!-- Smiling Eyes -->
            <g class="pip-eyes">
              <g class="pip-eye" style="transform-origin: 45px 43px;">
                <path d="M 40 45 Q 45 37 50 45" stroke="#7fe3c5" stroke-width="3.5" stroke-linecap="round" fill="none" filter="url(#pipGlow_${type})" />
              </g>
              <g class="pip-eye" style="transform-origin: 75px 43px;">
                <path d="M 70 45 Q 75 37 80 45" stroke="#7fe3c5" stroke-width="3.5" stroke-linecap="round" fill="none" filter="url(#pipGlow_${type})" />
              </g>
            </g>

            <!-- Coral Cheeks -->
            <circle class="pip-cheeks" cx="39" cy="50" r="3.6" fill="#ed6840" opacity="0.9" />
            <circle class="pip-cheeks" cx="81" cy="50" r="3.6" fill="#ed6840" opacity="0.9" />
            </g>
          </g>

          <!-- Right Arm (Articulated Natural Waving Arm - Angled Outward, completely clear of head) -->
          <g class="pip-arm-right" style="transform-origin: 84px 74px;">
            <!-- Shoulder joint -->
            <circle cx="84" cy="74" r="6.5" fill="#22423d" />
            <!-- Upper arm reaching outward -->
            <path d="M 84 74 L 99 68" stroke="url(#pipBody3D_${type})" stroke-width="8.5" stroke-linecap="round" fill="none" />
            <path d="M 84 74 L 99 68" stroke="rgba(23,48,45,0.18)" stroke-width="1.2" fill="none" />
            <!-- Elbow joint -->
            <circle cx="99" cy="68" r="5" fill="#22423d" />

            <!-- Forearm & Waving Hand (waving freely in the open space to the right) -->
            <g class="pip-forearm" style="transform-origin: 99px 68px;">
              <path d="M 99 68 L 107 50" stroke="url(#pipBody3D_${type})" stroke-width="8" stroke-linecap="round" fill="none" />
              <path d="M 99 68 L 107 50" stroke="rgba(23,48,45,0.18)" stroke-width="1.2" fill="none" />
              <g class="pip-hand">
              <circle cx="107" cy="48" r="6" fill="#22423d" />
              <!-- Open waving fingers -->
              <circle cx="104" cy="41" r="2.2" fill="#2a4e48" />
              <circle cx="108" cy="40" r="2.2" fill="#2a4e48" />
              <circle cx="112" cy="42" r="2.2" fill="#2a4e48" />
              <circle cx="114" cy="46" r="2.2" fill="#2a4e48" />
              </g>
            </g>
          </g>
          </g>
        </g>
      </svg>
    </span>`;
  }

  function createElement(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text) node.textContent = text;
    return node;
  }

  function createMessage(role, text) {
    const message = createElement("div", `pip-message pip-message--${role}`);
    const label = createElement("span", "pip-message__label", role === "bot" ? "Pip" : "Bạn");
    const bubble = createElement("div", "pip-message__bubble", text);
    message.append(label, bubble);
    return message;
  }

  function createAnswerMessage(answer, sources) {
    const message = createMessage("bot", answer);
    if (!sources.length) return message;

    const sourceList = createElement("ul", "pip-sources");
    sourceList.setAttribute("aria-label", "Nguồn tham khảo");
    for (const source of sources) {
      const item = createElement("li", "pip-source");
      const link = createElement("a", "pip-source__link");
      link.href = new URL(source.url, siteRootUrl).href;
      link.textContent = `[${source.id}] ${source.title}${source.heading ? ` · ${source.heading}` : ""}`;
      item.append(link);
      sourceList.append(item);
    }
    message.append(sourceList);
    return message;
  }

  function validSources(sources) {
    if (!Array.isArray(sources)) return false;
    return sources.every((source) => (
      source
      && typeof source.id === "string"
      && typeof source.title === "string"
      && typeof source.heading === "string"
      && typeof source.url === "string"
    ));
  }

  // One bounded gesture at a time; all timers stop while the mascot is hidden.
  function animateMascot(chat, launcher) {
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
    const timers = new Map();
    const readingDuration = 3500;
    const readingRest = 5000;
    const bookTransition = 650;
    chat.style.setProperty("--pip-book-transition", `${bookTransition}ms`);
    const stage = launcher.querySelector(".pip-mascot-wrapper");
    let active = true;
    let nearby = false;
    let focused = false;
    let lastGreeting = -Infinity;
    let pointerFrame = 0;
    let pointer = null;
    const random = (min, max) => min + Math.random() * (max - min);
    const canAnimate = () => active && !document.hidden && !reducedMotion.matches && chat.isConnected;
    const pose = (name) => { chat.dataset.pose = name; };

    function cancel(key) {
      window.clearTimeout(timers.get(key));
      timers.delete(key);
    }

    function after(key, callback, delay) {
      cancel(key);
      if (!canAnimate()) return;
      timers.set(key, window.setTimeout(() => {
        timers.delete(key);
        if (canAnimate()) callback();
      }, delay));
    }

    function blink() {
      chat.classList.toggle("is-double-blink", Math.random() < 0.22);
      chat.classList.add("is-blinking");
      after("blink-end", () => chat.classList.remove("is-blinking", "is-double-blink"), 460);
      after("blink", blink, random(2800, 6200));
    }

    function read() {
      cancel("pose");
      resetGaze();
      pose("reading");
      after("pose", () => {
        rest();
        // Start the full rest period after the closing transition finishes.
        after("reading-cycle", read, bookTransition + readingRest);
      }, readingDuration);
    }

    function rest() {
      pose("idle");
    }

    function greet() {
      if (!canAnimate()) return;
      cancel("entrance");
      if (["greeting", "reading"].includes(chat.dataset.pose)) return;
      cancel("pose");
      // Passing over the hit area repeatedly should not restart the wave.
      if (performance.now() - lastGreeting < 5000) return rest();
      lastGreeting = performance.now();
      pose("greeting");
      after("pose", rest, 2300);
    }

    function resetGaze() {
      chat.style.removeProperty("--pip-look-x");
      chat.style.removeProperty("--pip-look-y");
      chat.style.removeProperty("--pip-look-tilt");
    }

    function updatePointer() {
      pointerFrame = 0;
      if (!pointer || !canAnimate()) return;
      const rect = stage.getBoundingClientRect();
      const dx = pointer.x - (rect.left + rect.width / 2);
      const dy = pointer.y - (rect.top + rect.height * 0.3);
      const wasNearby = nearby;
      nearby = Math.hypot(dx, dy) < 200;
      if (chat.dataset.pose === "reading") return;
      if (nearby) {
        chat.style.setProperty("--pip-look-x", `${Math.max(-3, Math.min(3, dx / 45))}px`);
        chat.style.setProperty("--pip-look-y", `${Math.max(-2, Math.min(2, dy / 65))}px`);
        chat.style.setProperty("--pip-look-tilt", `${Math.max(-4, Math.min(4, dx / 40))}deg`);
        if (!wasNearby) greet();
      } else if (wasNearby) {
        resetGaze();
        if (!focused && !["greeting", "reading"].includes(chat.dataset.pose)) rest();
      }
    }

    function leave() {
      const wasNearby = nearby;
      pointer = null;
      nearby = false;
      window.cancelAnimationFrame(pointerFrame);
      pointerFrame = 0;
      resetGaze();
      if (wasNearby && canAnimate() && !focused && !["greeting", "reading"].includes(chat.dataset.pose)) rest();
    }

    document.addEventListener("pointermove", (event) => {
      if (event.pointerType !== "mouse" || !canAnimate()) return;
      pointer = { x: event.clientX, y: event.clientY };
      if (!pointerFrame) pointerFrame = window.requestAnimationFrame(updatePointer);
    }, { passive: true });
    document.documentElement.addEventListener("pointerleave", leave);
    window.addEventListener("blur", leave);
    window.addEventListener("scroll", leave, { passive: true });
    launcher.addEventListener("focus", () => { focused = true; greet(); });
    launcher.addEventListener("blur", () => {
      focused = false;
      if (canAnimate() && !nearby && !["greeting", "reading"].includes(chat.dataset.pose)) rest();
    });

    function refresh() {
      for (const timer of timers.values()) window.clearTimeout(timer);
      timers.clear();
      window.cancelAnimationFrame(pointerFrame);
      pointerFrame = 0;
      pointer = null;
      nearby = false;
      focused = document.activeElement === launcher;
      resetGaze();
      chat.classList.remove("is-blinking", "is-double-blink");
      chat.classList.toggle("is-paused", !canAnimate());
      pose("idle");
      if (canAnimate()) {
        after("blink", blink, random(1800, 3500));
        // This deadline is independent of hover, focus, and greeting timers.
        after("reading-cycle", read, readingRest);
      }
    }

    document.addEventListener("visibilitychange", refresh);
    reducedMotion.addEventListener("change", refresh);
    refresh();
    after("entrance", greet, 650);
    return { setActive(value) { active = value; refresh(); } };
  }

  function mountChat() {
    if (document.querySelector(".pip-chat") || !document.querySelector(".airflow-article-hero")) return;

    const articleTitle = document.querySelector(".airflow-article-hero h1")?.innerText
      .replace(/\s+/g, " ").trim() || document.title;
    const chat = createElement("aside", "pip-chat");
    const launcher = createElement("button", "pip-launcher");
    launcher.type = "button";
    launcher.setAttribute("aria-label", "Hỏi Pip về bài viết này");
    launcher.setAttribute("aria-expanded", "false");
    launcher.setAttribute("aria-controls", "pip-chat-panel");
    launcher.innerHTML = `
      <div class="pip-speech-bubble" aria-hidden="true">
        <span class="pip-speech-bubble__dot"></span>
        <span class="pip-speech-bubble__text">Hỏi Pip</span>
      </div>
      <div class="pip-mascot-wrapper">${robotMarkup("full")}</div>
    `;

    const panel = createElement("section", "pip-panel");
    panel.id = "pip-chat-panel";
    panel.setAttribute("role", "dialog");
    panel.setAttribute("aria-modal", "false");
    panel.setAttribute("aria-labelledby", "pip-chat-title");
    panel.innerHTML = `
      <header class="pip-panel__head">
        <span class="pip-panel__avatar" role="img" aria-label="Robot Pip">${robotMarkup("avatar")}</span>
        <div><h2 class="pip-panel__title" id="pip-chat-title">Pip · Bạn đọc cùng bạn</h2><span class="pip-panel__status">Sẵn sàng đọc bài</span></div>
        <button class="pip-panel__close" type="button" aria-label="Thu nhỏ khung chat">×</button>
      </header>
      <div class="pip-context">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5v-15Z" stroke="currentColor" stroke-width="2"/><path d="M4 20.5A2.5 2.5 0 0 1 6.5 18H20" stroke="currentColor" stroke-width="2"/></svg>
        Đang đọc <strong></strong>
      </div>
      <div class="pip-messages" aria-live="polite"></div>
      <div class="pip-suggestions" aria-label="Câu hỏi gợi ý"></div>
      <form class="pip-composer">
        <textarea rows="1" maxlength="1000" aria-label="Câu hỏi về bài viết" placeholder="Hỏi về nội dung bài…"></textarea>
        <button class="pip-composer__send" type="submit" aria-label="Gửi câu hỏi">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="m5 12 14-7-4 14-3-6-7-1Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="m12 13 7-8" stroke="currentColor" stroke-width="2"/></svg>
        </button>
      </form>`;

    chat.append(launcher, panel);
    document.body.append(chat);

    const close = panel.querySelector(".pip-panel__close");
    const input = panel.querySelector("textarea");
    const form = panel.querySelector("form");
    const send = panel.querySelector(".pip-composer__send");
    const messages = panel.querySelector(".pip-messages");
    const suggestions = panel.querySelector(".pip-suggestions");
    const status = panel.querySelector(".pip-panel__status");
    let focusTimer;
    const mascot = animateMascot(chat, launcher);

    panel.querySelector(".pip-context strong").textContent = articleTitle;
    messages.append(createMessage("bot", "Mình cùng đọc bài này nhé. Bạn muốn Pip làm rõ phần nào?"));

    ["Tóm tắt bài này", "Giải thích bằng ví dụ", "Nêu ý chính cần nhớ"].forEach((text) => {
      const button = createElement("button", "pip-suggestion", text);
      button.type = "button";
      button.addEventListener("click", () => {
        input.value = text;
        input.focus();
      });
      suggestions.append(button);
    });

    function setOpen(open) {
      window.clearTimeout(focusTimer);
      chat.classList.toggle("is-open", open);
      launcher.setAttribute("aria-expanded", String(open));
      mascot.setActive(!open);
      if (open) {
        focusTimer = window.setTimeout(() => { if (chat.classList.contains("is-open")) input.focus(); }, 220);
      } else {
        launcher.focus();
      }
    }

    launcher.addEventListener("click", () => setOpen(true));
    close.addEventListener("click", () => setOpen(false));
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && chat.classList.contains("is-open")) setOpen(false);
    });

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const question = input.value.trim();
      if (!question || send.disabled) return;
      messages.append(createMessage("user", question));
      input.value = "";
      send.disabled = true;
      suggestions.hidden = true;
      status.textContent = "Đang tìm trong tài liệu";

      const typing = createMessage("bot", "");
      typing.classList.add("pip-message--waiting");
      typing.querySelector(".pip-message__bubble").innerHTML = '<span class="pip-typing" aria-label="Pip đang suy nghĩ"><i></i><i></i><i></i></span>';
      const waitingRow = createElement("div", "pip-waiting-row");
      waitingRow.append(typing.querySelector(".pip-message__bubble"));
      waitingRow.insertAdjacentHTML("beforeend", robotMarkup("reading"));
      typing.append(waitingRow);
      messages.append(typing);
      messages.scrollTop = messages.scrollHeight;

      const controller = new AbortController();
      const timeout = window.setTimeout(() => controller.abort(), 210000);

      try {
        const response = await fetch(endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question }),
          signal: controller.signal,
        });
        if (!response.ok) {
          throw new Error(`Backend trả HTTP ${response.status}.`);
        }

        const data = await response.json();
        if (
          typeof data.answer !== "string"
          || !["answered", "insufficient_evidence", "generation_error"].includes(data.status)
          || !validSources(data.sources)
        ) {
          throw new Error("Backend trả dữ liệu không hợp lệ.");
        }

        typing.remove();
        messages.append(createAnswerMessage(data.answer, data.sources));
        status.textContent = "Sẵn sàng đọc bài";
      } catch (error) {
        typing.remove();
        const message = error?.name === "AbortError"
          ? "Chờ quá lâu. Model có thể đang bận; hãy thử lại sau."
          : `Không gửi được câu hỏi. ${error instanceof Error ? error.message : "Hãy kiểm tra backend."}`;
        messages.append(createMessage("bot", message));
        status.textContent = "Chưa kết nối được backend";
      } finally {
        window.clearTimeout(timeout);
        send.disabled = false;
        messages.scrollTop = messages.scrollHeight;
        if (chat.classList.contains("is-open")) input.focus();
      }
    });

    input.addEventListener("keydown", (event) => {
      if (event.key === "Enter" && !event.shiftKey && !event.isComposing) {
        event.preventDefault();
        form.requestSubmit();
      }
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", mountChat, { once: true });
  else mountChat();
})();
