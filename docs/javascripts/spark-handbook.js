(() => {
  const chapters = [
    ["when-to-use", "Chọn Spark"],
    ["architecture", "Kiến trúc"],
    ["data-abstractions", "Abstraction"],
    ["execution-model", "Execution"],
    ["query-planning", "Query plan"],
    ["partition-shuffle", "Shuffle"],
    ["memory-fault-tolerance", "Memory"],
    ["deployment", "Deployment"],
    ["performance", "Performance"],
    ["structured-streaming", "Streaming"],
  ];

  const chapterHref = (slug) => `../${slug}/`;

  function buildSeriesProgress(currentIndex) {
    const nav = document.createElement("nav");
    nav.className = "spark-series-progress";
    nav.setAttribute("aria-label", "Tiến độ trong Spark Handbook");

    const heading = document.createElement("div");
    heading.className = "spark-series-progress__heading";
    heading.innerHTML = `<span>Spark Handbook</span><strong>${String(currentIndex + 1).padStart(2, "0")} / ${chapters.length}</strong>`;

    const track = document.createElement("ol");
    track.className = "spark-series-progress__track";
    chapters.forEach(([slug, label], index) => {
      const item = document.createElement("li");
      const link = document.createElement("a");
      link.href = chapterHref(slug);
      link.innerHTML = `<b>${String(index + 1).padStart(2, "0")}</b><span>${label}</span>`;
      if (index === currentIndex) {
        item.className = "is-current";
        link.setAttribute("aria-current", "step");
      } else if (index < currentIndex) {
        item.className = "is-complete";
      }
      item.append(link);
      track.append(item);
    });

    nav.append(heading, track);
    return nav;
  }

  function buildChapterNavigation(currentIndex) {
    const nav = document.createElement("nav");
    nav.className = "spark-series-nav";
    nav.setAttribute("aria-label", "Điều hướng chương Spark Handbook");

    const previous = currentIndex > 0
      ? { href: chapterHref(chapters[currentIndex - 1][0]), label: chapters[currentIndex - 1][1], eyebrow: "Chương trước" }
      : { href: "../overview/", label: "Spark toàn cảnh", eyebrow: "Quay lại" };
    const next = currentIndex < chapters.length - 1
      ? { href: chapterHref(chapters[currentIndex + 1][0]), label: chapters[currentIndex + 1][1], eyebrow: "Chương tiếp" }
      : { href: "../overview/", label: "Spark toàn cảnh", eyebrow: "Hoàn tất series" };

    [previous, next].forEach((item, index) => {
      const link = document.createElement("a");
      link.href = item.href;
      link.className = index === 0 ? "spark-series-nav__previous" : "spark-series-nav__next";
      link.innerHTML = `<span>${item.eyebrow}</span><strong>${index === 0 ? "←" : ""} ${item.label} ${index === 1 ? "→" : ""}</strong>`;
      nav.append(link);
    });

    return nav;
  }

  function initialiseSparkChapter() {
    const marker = document.querySelector(".spark-chapter-hero");
    if (!marker || marker.dataset.enhanced === "true") return;

    marker.dataset.enhanced = "true";
    const currentIndex = Number.parseInt(marker.dataset.chapter, 10) - 1;
    if (!Number.isInteger(currentIndex) || !chapters[currentIndex]) return;

    const hero = marker.closest(".spark-article-hero");
    const article = marker.closest(".md-content__inner");
    if (!hero || !article) return;

    hero.insertAdjacentElement("afterend", buildSeriesProgress(currentIndex));

    const sourcesHeading = Array.from(article.querySelectorAll("h2"))
      .find((heading) => heading.textContent.trim() === "Tài liệu chính thức");
    const chapterNav = buildChapterNavigation(currentIndex);
    if (sourcesHeading) article.insertBefore(chapterNav, sourcesHeading);
    else article.append(chapterNav);

    document.querySelectorAll(".spark-reading-progress").forEach((node) => node.remove());
    const progress = document.createElement("div");
    progress.className = "spark-reading-progress";
    progress.setAttribute("role", "progressbar");
    progress.setAttribute("aria-label", "Tiến độ đọc chương");
    progress.setAttribute("aria-valuemin", "0");
    progress.setAttribute("aria-valuemax", "100");
    progress.innerHTML = "<span></span>";
    document.body.append(progress);

    if (window.sparkHandbookScrollController) window.sparkHandbookScrollController.abort();
    window.sparkHandbookScrollController = new AbortController();
    const signal = window.sparkHandbookScrollController.signal;

    const updateReadingProgress = () => {
      const scrollable = document.documentElement.scrollHeight - window.innerHeight;
      const ratio = scrollable > 0 ? Math.min(1, Math.max(0, window.scrollY / scrollable)) : 1;
      const value = Math.round(ratio * 100);
      progress.style.setProperty("--spark-reading-progress", `${value}%`);
      progress.setAttribute("aria-valuenow", String(value));
    };

    updateReadingProgress();
    window.addEventListener("scroll", updateReadingProgress, { passive: true, signal });
    window.addEventListener("resize", updateReadingProgress, { passive: true, signal });
  }

  if (typeof document$ !== "undefined") document$.subscribe(initialiseSparkChapter);
  else if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", initialiseSparkChapter);
  else initialiseSparkChapter();
})();
