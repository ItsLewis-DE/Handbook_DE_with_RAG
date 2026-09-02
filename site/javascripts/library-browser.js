(() => {
  const previews = {
    airflow: {
      number: "01",
      label: "FEATURED / 01",
      meta: "APACHE AIRFLOW · LONG READ",
      publication: "Đã xuất bản · 01 bài",
      edition: "ED. 01",
      overline: "BÀI VIẾT NỔI BẬT",
      title: "Hiểu kiến trúc Airflow từ nhu cầu điều phối.",
      summary: "Bắt đầu với một pipeline Bash và Cron, rồi lần lượt mở từng lớp của Airflow: DAG, Task, Scheduler, Executor, HA và Critical Section.",
      tags: ["Architecture", "Scheduler", "Executor", "High Availability"],
      href: "airflow/architecture/",
      action: "Đọc toàn bộ bài viết",
      chaptersLabel: "ĐỌC THEO LỘ TRÌNH",
      chapters: [
        ["01", "Tại sao cần Airflow?", "airflow/architecture/#tai-sao-can-airflow"],
        ["02", "Khái niệm nền tảng", "airflow/architecture/#nhung-khai-niem-nen-tang"],
        ["03", "Kiến trúc bên trong", "airflow/architecture/#cac-component-trong-airflow"],
      ],
    },
    storage: {
      number: "02",
      label: "LATEST / 02",
      meta: "DATA ARCHITECTURE · DEEP RESEARCH",
      publication: "Đã xuất bản · 02 bài",
      edition: "ED. 02",
      overline: "BÀI MỚI NHẤT",
      title: "Shared-disk hay shared-nothing? Chọn topology cho hệ dữ liệu.",
      summary: "Theo dấu ownership, query path, shuffle, rebalance và failure để Data Engineer chọn kiến trúc từ workload thay vì chọn theo nhãn sản phẩm.",
      tags: ["Topology", "Partitioning", "Query path", "Failure mode"],
      href: "architecture/shared-disk-vs-shared-nothing/",
      action: "Đọc bài nghiên cứu",
      chaptersLabel: "ĐỌC THEO LỘ TRÌNH",
      chapters: [
        ["01", "Ai sở hữu dữ liệu?", "architecture/shared-disk-vs-shared-nothing/#bat-dau-tu-cau-hoi-ai-so-huu-du-lieu"],
        ["02", "Hai topology vận hành", "architecture/shared-disk-vs-shared-nothing/#shared-disk-van-hanh-nhu-the-nao"],
        ["03", "Chọn kiến trúc", "architecture/shared-disk-vs-shared-nothing/#chon-kien-truc-nao-cho-data-platform"],
      ],
    },
    databaseIndex: {
      number: "03",
      label: "LATEST / 03",
      meta: "DATABASE INTERNALS · DEEP DIVE",
      publication: "Đã xuất bản · 03 bài",
      edition: "ED. 03",
      overline: "BÀI MỚI NHẤT",
      title: "Index giúp database tìm dữ liệu nhanh hơn như thế nào?",
      summary: "Bắt đầu từ full table scan, rồi tìm hiểu index là gì, database sử dụng index ra sao và vì sao tốc độ truy vấn luôn đi kèm chi phí lưu trữ và ghi dữ liệu.",
      tags: ["Index", "Query optimizer", "Full table scan", "B-tree"],
      href: "index/",
      action: "Đọc bài viết",
      chaptersLabel: "ĐỌC THEO LỘ TRÌNH",
      chapters: [
        ["01", "Index là gì?", "index/#index-la-gi"],
        ["02", "Index lưu những gì?", "index/#index-khong-phai-ban-sao-ay-u-cua-bang"],
        ["03", "Sự đánh đổi của index", "index/#su-anh-oi-cua-index"],
      ],
    },
    spark: {
      number: "04",
      label: "PLANNED / 04",
      meta: "APACHE SPARK · INTERNALS",
      publication: "Trong lộ trình nghiên cứu",
      edition: "PLAN. 04",
      overline: "BÀI VIẾT DỰ KIẾN",
      title: "Apache Spark: một job thật sự chạy qua cluster thế nào?",
      summary: "Từ logical plan đến stage, task, partition và shuffle. Trọng tâm: đọc execution plan và tìm bottleneck thay vì chỉ chỉnh cấu hình.",
      tags: ["DAG", "Partition", "Shuffle", "Spark UI"],
    },
    kafka: {
      number: "05",
      label: "PLANNED / 05",
      meta: "APACHE KAFKA · INTERNALS",
      publication: "Trong lộ trình nghiên cứu",
      edition: "PLAN. 05",
      overline: "BÀI VIẾT DỰ KIẾN",
      title: "Kafka: log phân tán, partition ownership và delivery semantics.",
      summary: "Theo đường đi của record qua producer, broker và consumer group; sau đó bóc tách replication, rebalance và các cam kết giao nhận.",
      tags: ["Log", "Partition", "Consumer group", "Replication"],
    },
    dbt: {
      number: "06",
      label: "PLANNED / 06",
      meta: "DBT · TRANSFORMATION",
      publication: "Trong lộ trình nghiên cứu",
      edition: "PLAN. 06",
      overline: "BÀI VIẾT DỰ KIẾN",
      title: "dbt: từ câu SQL đến lineage và sản phẩm dữ liệu.",
      summary: "Compiler, dependency graph, materialization và cách tổ chức transformation để thay đổi an toàn trong một data warehouse đang lớn dần.",
      tags: ["Compiler", "Lineage", "Materialization", "Testing"],
    },
    infrastructure: {
      number: "07",
      label: "PLANNED / 07",
      meta: "DATA INFRASTRUCTURE · FIELD GUIDE",
      publication: "Trong lộ trình nghiên cứu",
      edition: "PLAN. 07",
      overline: "BÀI VIẾT DỰ KIẾN",
      title: "Docker và Kubernetes cho workload dữ liệu.",
      summary: "Từ image và container đến scheduling, resource limits, observability và recovery cho pipeline chạy trong môi trường production.",
      tags: ["Container", "Scheduling", "Resources", "Operations"],
    },
  };

  function initialiseBrowser(browser) {
    if (browser.dataset.browserReady === "true") return;

    const article = browser.querySelector(".featured-article");
    const choices = Array.from(browser.querySelectorAll("[data-preview]"));
    const fields = {
      stamp: article?.querySelector("#featured-stamp-number"),
      meta: article?.querySelector("#featured-meta"),
      publication: article?.querySelector("#featured-publication"),
      edition: article?.querySelector("#featured-edition"),
      overline: article?.querySelector("#featured-overline"),
      title: article?.querySelector("#featured-title"),
      summary: article?.querySelector("#featured-summary"),
      tags: article?.querySelector("#featured-tags"),
      button: article?.querySelector("#featured-read-button"),
      action: article?.querySelector("#featured-action"),
      chaptersLabel: article?.querySelector("#featured-chapters-label"),
      chapters: article?.querySelector("#featured-chapters"),
    };

    if (!article || choices.length === 0 || Object.values(fields).some((field) => !field)) return;

    let currentKey = "airflow";

    function updateChoiceState(activeChoice) {
      choices.forEach((choice) => {
        const active = choice === activeChoice;
        const status = choice.querySelector(".tool-choice__status");
        choice.classList.toggle("tool-choice--active", active);

        if (choice.matches("a")) {
          active ? choice.setAttribute("aria-current", "true") : choice.removeAttribute("aria-current");
        } else {
          choice.setAttribute("aria-pressed", active ? "true" : "false");
        }

        if (status) {
          status.textContent = active
            ? "Đang chọn"
            : choice.dataset.inactiveStatus || (choice.classList.contains("tool-choice--soon") ? "Sắp tới" : "Đã mở");
        }
      });
    }

    function render(key, activeChoice) {
      const data = previews[key];
      if (!data || key === currentKey && activeChoice.classList.contains("tool-choice--active")) return;

      currentKey = key;
      article.dataset.previewNumber = data.number;
      article.dataset.previewLabel = data.label;
      fields.stamp.textContent = data.number;
      fields.meta.textContent = data.meta;
      fields.publication.textContent = data.publication;
      fields.edition.textContent = data.edition;
      fields.overline.textContent = data.overline;
      fields.title.textContent = data.title;
      fields.summary.textContent = data.summary;

      fields.tags.replaceChildren(...data.tags.map((tag) => {
        const item = document.createElement("span");
        item.textContent = tag;
        return item;
      }));

      const published = Boolean(data.href);
      fields.button.hidden = !published;
      if (published) {
        fields.button.href = data.href;
        fields.action.textContent = data.action;
      }

      fields.chaptersLabel.textContent = published ? data.chaptersLabel : "LỘ TRÌNH BIÊN SOẠN";
      if (published) {
        fields.chapters.replaceChildren(...data.chapters.map(([number, title, href]) => {
          const link = document.createElement("a");
          link.href = href;
          link.innerHTML = `<span>CHƯƠNG ${number}</span><strong>${title}</strong><b aria-hidden="true">↗</b>`;
          return link;
        }));
      } else {
        const stages = [["01", "Research questions"], ["02", "Source mapping"], ["03", "Draft & diagrams"]];
        fields.chapters.replaceChildren(...stages.map(([number, title]) => {
          const step = document.createElement("span");
          step.className = "article-chapters__step";
          step.innerHTML = `<span>BƯỚC ${number}</span><strong>${title}</strong>`;
          return step;
        }));
      }

      updateChoiceState(activeChoice);
      article.classList.remove("is-changing");
      void article.offsetWidth;
      article.classList.add("is-changing");
    }

    choices.forEach((choice) => {
      const activate = () => render(choice.dataset.preview, choice);
      if (choice.matches("button")) choice.addEventListener("click", activate);
    });

    browser.dataset.browserReady = "true";
  }

  function initialiseAllBrowsers() {
    document.querySelectorAll(".library-browser").forEach(initialiseBrowser);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialiseAllBrowsers, { once: true });
  } else {
    initialiseAllBrowsers();
  }
})();
