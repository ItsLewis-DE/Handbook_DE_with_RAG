---
hide:
  - navigation
  - toc
---

<div class="landing-page">
  <section class="landing-hero" aria-labelledby="landing-title">
    <div class="blueprint-watermark blueprint-watermark--hero" aria-hidden="true">
      <img src="assets/images/blueprint-hero.svg" alt="" loading="lazy">
    </div>

    <div class="landing-hero__copy">
      <div class="landing-kicker">
        <span class="landing-kicker__mark" aria-hidden="true"></span>
        <span class="landing-brand"><strong>Behind the</strong><b>Pipeline</b></span>
        <small>Est. 2026</small>
      </div>

      <h1 id="landing-title">Một bản đồ sống cho thế giới <em>Data Engineering.</em></h1>
      <p class="landing-hero__lead">
        Tập hợp những bài viết đi từ <strong>lý do một công cụ tồn tại</strong>
        đến cách nó vận hành bên trong — để chúng ta không chỉ biết dùng tool,
        mà còn biết mình đang xây điều gì.
      </p>

      <div class="landing-actions">
        <a class="landing-button landing-button--primary" href="#thu-vien">
          Chọn bài để đọc <span aria-hidden="true">↘</span>
        </a>
      </div>

      <p class="landing-hero__note">
        <span aria-hidden="true">✦</span> Viết bằng tiếng Việt · Cập nhật theo hành trình học và làm
      </p>
    </div>

    <div class="landing-hero__visual" aria-label="Những bài viết nên đọc trong Behind the Pipeline">
      <div class="reading-callout" aria-hidden="true">
        <span>Những bài viết<br>nên đọc</span>
        <svg viewBox="0 0 180 220" role="presentation">
          <path d="M5 12C55 5 78 20 84 49C92 88 108 143 157 177"></path>
          <path d="M151 165L160 179L144 182"></path>
        </svg>
      </div>

      <div class="stack-card">
        <div class="stack-card__topbar">
          <span>FIELD MAP / 001</span>
          <span class="stack-card__live"><i></i> ONGOING</span>
        </div>

        <div class="article-deck-shell">
          <div class="article-deck" tabindex="0" aria-label="Chồng 7 bài viết. Kéo tờ giấy sang trái để xem bài tiếp theo." aria-describedby="article-deck-help">
            <article class="article-sheet article-sheet--airflow" data-article-title="Kiến trúc Apache Airflow" data-deck-position="current">
              <div class="article-sheet__meta"><span>ORCHESTRATION</span><b>01 / 07</b></div>
              <div class="article-sheet__body">
                <span class="article-sheet__status article-sheet__status--published">Đã xuất bản</span>
                <h2>Hiểu kiến trúc<br>Apache Airflow</h2>
                <p>Từ nhu cầu điều phối đến Scheduler, Executor và High Availability.</p>
              </div>
              <div class="article-sheet__foot">
                <span>Tác giả · Phong Thanh</span>
                <a href="airflow/architecture/">Mở bài viết <b aria-hidden="true">↗</b></a>
              </div>
            </article>

            <article class="article-sheet article-sheet--storage" data-article-title="Shared-disk vs shared-nothing" data-deck-position="next">
              <div class="article-sheet__meta"><span>DATA ARCHITECTURE</span><b>02 / 07</b></div>
              <div class="article-sheet__body">
                <span class="article-sheet__status article-sheet__status--published">Đã xuất bản</span>
                <h2>Shared-disk vs<br>shared-nothing</h2>
                <p>Chọn topology dữ liệu từ góc nhìn Data Engineer: query, shuffle và failure.</p>
              </div>
              <div class="article-sheet__foot">
                <span>Tác giả · AI Research</span>
                <a href="architecture/shared-disk-vs-shared-nothing/">Mở bài viết <b aria-hidden="true">↗</b></a>
              </div>
            </article>

            <article class="article-sheet article-sheet--index" data-article-title="Index trong cơ sở dữ liệu" data-deck-position="back">
              <div class="article-sheet__meta"><span>DATABASE INTERNALS</span><b>03 / 07</b></div>
              <div class="article-sheet__body">
                <span class="article-sheet__status article-sheet__status--published">Bài mới nhất</span>
                <h2>Index trong<br>cơ sở dữ liệu</h2>
                <p>Từ full table scan đến cấu trúc dữ liệu giúp database tìm bản ghi nhanh hơn.</p>
              </div>
              <div class="article-sheet__foot">
                <span>Tác giả · Phong Thanh</span>
                <a href="index/">Mở bài viết <b aria-hidden="true">↗</b></a>
              </div>
            </article>

            <article class="article-sheet article-sheet--planned" data-article-title="Apache Spark internals" data-deck-position="hidden">
              <div class="article-sheet__meta"><span>PROCESSING</span><b>04 / 07</b></div>
              <div class="article-sheet__body">
                <span class="article-sheet__status">Trong lộ trình</span>
                <h2>Apache Spark<br>internals</h2>
                <p>Partition, DAG execution, shuffle và cách một job thật sự chạy qua cluster.</p>
              </div>
              <div class="article-sheet__foot"><span>Dự kiến</span><em>Đang lên dàn ý</em></div>
            </article>

            <article class="article-sheet article-sheet--planned article-sheet--clay" data-article-title="Apache Kafka internals" data-deck-position="hidden">
              <div class="article-sheet__meta"><span>STREAMING</span><b>05 / 07</b></div>
              <div class="article-sheet__body">
                <span class="article-sheet__status">Trong lộ trình</span>
                <h2>Apache Kafka<br>internals</h2>
                <p>Log phân tán, partition ownership và những đánh đổi của delivery semantics.</p>
              </div>
              <div class="article-sheet__foot"><span>Dự kiến</span><em>Chờ nghiên cứu</em></div>
            </article>

            <article class="article-sheet article-sheet--planned article-sheet--blue" data-article-title="dbt: từ SQL đến lineage" data-deck-position="hidden">
              <div class="article-sheet__meta"><span>TRANSFORMATION</span><b>06 / 07</b></div>
              <div class="article-sheet__body">
                <span class="article-sheet__status">Trong lộ trình</span>
                <h2>dbt: từ SQL<br>đến lineage</h2>
                <p>Compiler, materialization và cách tổ chức transformation thành sản phẩm dữ liệu.</p>
              </div>
              <div class="article-sheet__foot"><span>Dự kiến</span><em>Chờ nghiên cứu</em></div>
            </article>

            <article class="article-sheet article-sheet--planned article-sheet--ink" data-article-title="Docker và Kubernetes cho Data Engineer" data-deck-position="hidden">
              <div class="article-sheet__meta"><span>INFRASTRUCTURE</span><b>07 / 07</b></div>
              <div class="article-sheet__body">
                <span class="article-sheet__status">Trong lộ trình</span>
                <h2>Docker &amp; Kubernetes<br>cho Data Engineer</h2>
                <p>Từ một container đến workload dữ liệu có thể deploy, quan sát và phục hồi.</p>
              </div>
              <div class="article-sheet__foot"><span>Dự kiến</span><em>Chờ nghiên cứu</em></div>
            </article>
          </div>

          <div class="article-deck__controls">
            <span class="article-deck__swipe-icon" aria-hidden="true"><i></i></span>
            <p id="article-deck-help"><b>Kéo sang trái</b> để lật bài</p>
          </div>
          <p class="article-deck__announcement" aria-live="polite" aria-atomic="true"></p>
        </div>

        <div class="stack-card__footer">
          <span><b>03</b> bài đã mở</span>
          <span><b>04</b> bài sắp tới</span>
          <span class="article-deck__count"><b>01</b> / 07</span>
        </div>
      </div>

      <span class="hero-orbit hero-orbit--one" aria-hidden="true"></span>
      <span class="hero-orbit hero-orbit--two" aria-hidden="true"></span>
    </div>
  </section>

  <section class="library-section" id="thu-vien" aria-labelledby="library-title">
    <div class="section-heading section-heading--split">
      <div>
        <p class="section-eyebrow">THE KNOWLEDGE SHELF / 01</p>
        <h2 id="library-title">Hôm nay bạn muốn<br>tìm hiểu điều gì?</h2>
      </div>
    </div>

    <div class="library-browser">
      <div class="blueprint-watermark blueprint-watermark--shelf" aria-hidden="true">
        <img src="assets/images/blueprint-shelf.svg" alt="" loading="lazy">
      </div>

      <div class="tool-shelf" aria-label="Các nhóm công cụ">
        <p class="tool-shelf__label">DANH MỤC BÀI VIẾT</p>

        <button class="tool-choice tool-choice--active" type="button" data-preview="airflow" aria-pressed="true">
          <span class="tool-choice__number">01</span>
          <span class="tool-choice__copy">
            <small>ORCHESTRATION</small>
            <strong>Apache Airflow</strong>
          </span>
          <span class="tool-choice__status">Đang chọn</span>
        </button>

        <button class="tool-choice" type="button" data-preview="storage" aria-pressed="false">
          <span class="tool-choice__number">02</span>
          <span class="tool-choice__copy">
            <small>DATA ARCHITECTURE</small>
            <strong>Shared-disk vs shared-nothing</strong>
          </span>
          <span class="tool-choice__status">Đã mở</span>
        </button>

        <button class="tool-choice" type="button" data-preview="databaseIndex" data-inactive-status="Bài mới nhất" aria-pressed="false">
          <span class="tool-choice__number">03</span>
          <span class="tool-choice__copy">
            <small>DATABASE INTERNALS</small>
            <strong>Index trong cơ sở dữ liệu</strong>
          </span>
          <span class="tool-choice__status">Bài mới nhất</span>
        </button>

        <button class="tool-choice tool-choice--soon" type="button" data-preview="spark">
          <span class="tool-choice__number">04</span>
          <span class="tool-choice__copy"><small>PROCESSING</small><strong>Apache Spark</strong></span>
          <span class="tool-choice__status">Sắp tới</span>
        </button>

        <button class="tool-choice tool-choice--soon" type="button" data-preview="kafka">
          <span class="tool-choice__number">05</span>
          <span class="tool-choice__copy"><small>STREAMING</small><strong>Apache Kafka</strong></span>
          <span class="tool-choice__status">Sắp tới</span>
        </button>

        <button class="tool-choice tool-choice--soon" type="button" data-preview="dbt">
          <span class="tool-choice__number">06</span>
          <span class="tool-choice__copy"><small>TRANSFORMATION</small><strong>dbt</strong></span>
          <span class="tool-choice__status">Sắp tới</span>
        </button>

        <button class="tool-choice tool-choice--soon" type="button" data-preview="infrastructure">
          <span class="tool-choice__number">07</span>
          <span class="tool-choice__copy"><small>INFRASTRUCTURE</small><strong>Docker &amp; Kubernetes</strong></span>
          <span class="tool-choice__status">Sắp tới</span>
        </button>
      </div>

      <article class="featured-article" id="featured-article" data-preview-number="01" data-preview-label="FEATURED / 01">
        <header class="featured-article__header">
          <div class="featured-article__stamp" aria-hidden="true">
            <small>FIELD NOTE</small><b id="featured-stamp-number">01</b>
          </div>
          <div>
            <p id="featured-meta">APACHE AIRFLOW · LONG READ</p>
            <span id="featured-publication">Đã xuất bản · 01 bài</span>
          </div>
          <span class="featured-article__edition" id="featured-edition">ED. 01</span>
        </header>

        <div class="featured-article__body">
          <p class="featured-article__overline" id="featured-overline">BÀI VIẾT NỔI BẬT</p>
          <h3 id="featured-title">Hiểu kiến trúc Airflow từ nhu cầu điều phối.</h3>
          <p id="featured-summary">
            Bắt đầu với một pipeline Bash và Cron, rồi lần lượt mở từng lớp của
            Airflow: DAG, Task, Scheduler, Executor, HA và Critical Section.
          </p>
          <div class="article-tags" id="featured-tags" aria-label="Chủ đề trong bài viết">
            <span>Architecture</span><span>Scheduler</span><span>Executor</span><span>High Availability</span>
          </div>
          <a class="article-read-button" id="featured-read-button" href="airflow/architecture/">
            <span id="featured-action">Đọc toàn bộ bài viết</span><b aria-hidden="true">↗</b>
          </a>
        </div>

        <div class="article-chapters">
          <p id="featured-chapters-label">ĐỌC THEO LỘ TRÌNH</p>
          <div id="featured-chapters">
            <a href="airflow/architecture/#tai-sao-can-airflow"><span>CHƯƠNG 01</span><strong>Tại sao cần Airflow?</strong><b aria-hidden="true">↗</b></a>
            <a href="airflow/architecture/#nhung-khai-niem-nen-tang"><span>CHƯƠNG 02</span><strong>Khái niệm nền tảng</strong><b aria-hidden="true">↗</b></a>
            <a href="airflow/architecture/#cac-component-trong-airflow"><span>CHƯƠNG 03</span><strong>Kiến trúc bên trong</strong><b aria-hidden="true">↗</b></a>
          </div>
        </div>
      </article>
    </div>
  </section>

  <section class="writing-section" id="cach-viet" aria-labelledby="writing-title">
    <div class="blueprint-watermark blueprint-watermark--writing" aria-hidden="true">
      <img src="assets/images/blueprint-writing.svg" alt="" loading="lazy">
    </div>

    <div class="writing-section__intro">
      <div>
        <div class="writing-section__kicker">
          <span class="writing-section__kicker-mark" aria-hidden="true"></span>
          <p class="section-eyebrow">HOW THESE NOTES ARE MADE / 02</p>
        </div>
        <h2 id="writing-title">Không học thuộc tool.<br><em>Học cách nó suy nghĩ.</em></h2>
      </div>
      <div class="writing-section__lead-box">
        <span class="writing-section__lead-label">QUY TRÌNH BIÊN SOẠN · 3 GIAI ĐOẠN</span>
        <p class="writing-section__lead">
          Mỗi bài viết được xây như một cuộc điều tra nhỏ: bắt đầu bằng câu hỏi
          “vì sao”, đi vào phần lõi, rồi quay lại với quyết định trong thực tế.
        </p>
      </div>
    </div>

    <div class="blueprint-dag-stream" aria-hidden="true">
      <div class="dag-node"><span>SOURCE</span><i></i></div>
      <div class="dag-connector"></div>
      <div class="dag-node dag-node--active"><span>01 · PROBLEM</span><i></i></div>
      <div class="dag-connector"></div>
      <div class="dag-node dag-node--active"><span>02 · INTERNALS</span><i></i></div>
      <div class="dag-connector"></div>
      <div class="dag-node dag-node--active"><span>03 · TRADE-OFF</span><i></i></div>
      <div class="dag-connector"></div>
      <div class="dag-node"><span>PRODUCTION</span><i></i></div>
    </div>

    <div class="writing-principles" role="list" aria-label="Quy trình 3 bước mổ xẻ kiến trúc">
      <article class="writing-card" data-step-number="01" role="listitem">
        <header class="writing-card__header">
          <div class="writing-card__stamp" aria-hidden="true">
            <small>BƯỚC</small><b>01</b>
          </div>
          <div class="writing-card__meta">
            <span class="writing-card__stage">ORIGIN / NGUYÊN DO</span>
          </div>
        </header>

        <div class="writing-card__flow">
          <span class="writing-card__flow-badge">PROBLEM</span>
        </div>

        <h3 class="writing-card__title">Bắt đầu từ vấn đề</h3>
        <p class="writing-card__question">“Tại sao giải pháp này cần phải ra đời?”</p>
        <p class="writing-card__desc">
          Trước mỗi component luôn là một bài toán thực tế: điểm nghẽn cổ chai,
          giới hạn mở rộng hoặc sự sụp đổ của những cách tiếp cận cũ.
        </p>

        <footer class="writing-card__tags" aria-label="Khía cạnh phân tích">
          <span>Root Problem</span>
          <span>Why it exists</span>
          <span>Failure Modes</span>
        </footer>
      </article>

      <article class="writing-card" data-step-number="02" role="listitem">
        <header class="writing-card__header">
          <div class="writing-card__stamp" aria-hidden="true">
            <small>BƯỚC</small><b>02</b>
          </div>
          <div class="writing-card__meta">
            <span class="writing-card__stage">INTERNALS / BÊN TRONG</span>
          </div>
        </header>

        <div class="writing-card__flow">
          <span class="writing-card__flow-badge">CORE MECHANISM</span>
        </div>

        <h3 class="writing-card__title">Mở chiếc hộp đen</h3>
        <p class="writing-card__question">“Bên dưới nắp máy thật sự vận hành ra sao?”</p>
        <p class="writing-card__desc">
          Bóc tách từng tầng kiến trúc, luồng dữ liệu (data flow) và trạng thái
          phân tán, thay vì dừng lại ở các câu lệnh cấu hình bề mặt.
        </p>

        <footer class="writing-card__tags" aria-label="Khía cạnh phân tích">
          <span>Architecture</span>
          <span>Data Flow</span>
          <span>State &amp; Locks</span>
        </footer>
      </article>

      <article class="writing-card" data-step-number="03" role="listitem">
        <header class="writing-card__header">
          <div class="writing-card__stamp" aria-hidden="true">
            <small>BƯỚC</small><b>03</b>
          </div>
          <div class="writing-card__meta">
            <span class="writing-card__stage">SYNTHESIS / THỰC CHIẾN</span>
          </div>
        </header>

        <div class="writing-card__flow">
          <span class="writing-card__flow-badge">PRODUCTION</span>
        </div>

        <h3 class="writing-card__title">Nối lại với thực tế</h3>
        <p class="writing-card__question">“Đánh đổi điều gì khi đưa vào vận hành?”</p>
        <p class="writing-card__desc">
          Hiểu rõ giới hạn chịu tải, chi phí vận hành và ranh giới phù hợp để
          đưa ra quyết định kiến trúc chuẩn xác cho hệ thống thực tế.
        </p>

        <footer class="writing-card__tags" aria-label="Khía cạnh phân tích">
          <span>Trade-offs</span>
          <span>Failure Modes</span>
          <span>Production Limits</span>
        </footer>
      </article>
    </div>

    <span class="writing-orbit" aria-hidden="true"></span>
  </section>

  <section class="author-section" id="nguoi-viet" aria-labelledby="author-title">
    <div class="blueprint-watermark blueprint-watermark--author" aria-hidden="true">
      <img src="assets/images/blueprint-author.svg" alt="" loading="lazy">
    </div>

    <div class="author-section__masthead">
      <p>PERSONAL LOG / 001</p>
      <span>PEOPLE BEHIND THE NOTES</span>
    </div>

    <div class="author-primary-card">
      <span class="author-primary-card__watermark" aria-hidden="true">TOGETHER</span>
      <figure class="author-photo">
        <div class="author-photo__frame">
          <img src="assets/images/phong-thanh-at-the-sea.webp" alt="Người viết đứng bên bờ biển" width="1920" height="1296" loading="lazy">
        </div>
        <figcaption><span>OFFLINE / PHAN THIET</span><span>© 28.08.2026</span></figcaption>
      </figure>

      <div class="author-note">
        <p class="section-eyebrow">A NOTE FROM THE AUTHOR / ĐÔI LỜI</p>
        <h2 id="author-title">Chào bạn,<br>cảm ơn vì đã ghé qua.</h2>
        <p class="author-note__lead">
          <span class="author-principle-label">AUTHOR'S PRINCIPLE / 01</span>
          <span class="author-principle-text">Mình tin rằng <strong>hiểu sâu</strong> một công cụ là cách tốt nhất để dùng nó đơn giản hơn.</span>
        </p>
        <div class="author-note__body">
          <p>
            Trang này bắt đầu từ một nhu cầu rất đơn giản: mình muốn lưu lại những
            lần phải đào sâu để hiểu một công cụ thực sự vận hành ra sao — không
            chỉ là vài câu lệnh đủ để nó chạy.
          </p>
          <p>
            Kiến thức <strong class="author-keyword">Data Engineering</strong> thường nằm rải rác giữa documentation,
            source code và những lần hệ thống gặp sự cố. Mình gom chúng lại ở đây,
            bằng thứ ngôn ngữ mà chính mình cũng muốn đọc khi mới bắt đầu.
          </p>
          <p>
            Thư viện bắt đầu với <strong class="author-keyword">Airflow</strong> và các nền tảng kiến trúc dữ liệu. Mình hy vọng
            mỗi lần quay lại, bạn sẽ tìm thấy thêm một mảnh ghép hữu ích cho hệ thống
            mà bạn đang xây.
          </p>
        </div>
        <div class="author-signoff">
          <span aria-hidden="true">Author</span>
          <div><strong>Phong Thanh</strong><small>Học, làm, rồi ghi lại.</small></div>
        </div>
      </div>
    </div>

    <article class="coauthor-card" aria-labelledby="coauthor-title">
      <div class="coauthor-card__copy">
        <div class="coauthor-card__index" aria-hidden="true">
          <span>COLLABORATOR FILE</span><b>02</b>
        </div>
        <p class="section-eyebrow">A SECOND POINT OF VIEW / ĐỒNG TÁC GIẢ</p>
        <h3 id="coauthor-title">Thêm một góc nhìn,<br>thêm một lớp rõ ràng.</h3>
        <p class="coauthor-card__lead">
          <span class="author-principle-label">CO-AUTHOR'S PRINCIPLE / 02</span>
          <span class="author-principle-text">Một ghi chú tốt không chỉ cần được <strong>viết kỹ</strong> — nó còn cần một người
          sẵn sàng hỏi lại những điều tưởng như đã hiển nhiên.</span>
        </p>
        <p class="coauthor-card__body">
          Danh đồng hành cùng Behind the Pipeline trong vai trò đồng tác giả: trao đổi
          <strong class="author-keyword">hướng tiếp cận</strong>, rà lại mạch giải thích và giúp mỗi bài viết gần hơn
          với <strong class="author-keyword">trải nghiệm của người đọc</strong>.
        </p>
        <div class="coauthor-card__signoff">
          <span aria-hidden="true">Co-author</span>
          <div><strong>Danh</strong><small>Cùng đọc, cùng chất vấn, cùng hoàn thiện.</small></div>
        </div>
      </div>

      <figure class="coauthor-card__photo">
        <div class="coauthor-card__photo-frame">
          <img src="assets/images/danh.png" alt="Đồng tác giả Danh đứng bên bờ biển" width="460" height="460" loading="lazy">
          <span class="coauthor-card__photo-number" aria-hidden="true">02</span>
        </div>
        <figcaption><span>CO-AUTHOR PORTRAIT</span><span>BEHIND THE PIPELINE / 2026</span></figcaption>
      </figure>
    </article>
  </section>

  <footer class="landing-footer">
    <p class="landing-footer__brand"><strong>BEHIND THE</strong> <b>PIPELINE</b></p>
    <p>Built slowly. Understood deeply.</p>
    <a href="#landing-title">Lên đầu trang <span aria-hidden="true">↑</span></a>
  </footer>
</div>
