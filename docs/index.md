---
hide:
  - navigation
  - toc
---

<div class="landing-page">
  <section class="landing-hero" aria-labelledby="landing-title">
    <div class="blueprint-watermark blueprint-watermark--hero" aria-hidden="true">
      <img src="assets/images/home/blueprint-hero.svg" alt="" width="1440" height="900">
      <span class="blueprint-signal blueprint-signal--hero"></span>
    </div>

    <div class="landing-hero__copy">
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
          <div class="article-deck" tabindex="0" aria-label="Chồng 8 bài viết. Dùng nút điều hướng, phím mũi tên hoặc kéo tờ giấy sang trái để xem bài tiếp theo." aria-describedby="article-deck-help">
            <article class="article-sheet article-sheet--airflow" data-article-title="Kiến trúc Apache Airflow" data-deck-position="current">
              <div class="article-sheet__art" aria-hidden="true">
                <img src="assets/images/airflow/card-art.jpg" alt="" loading="lazy">
              </div>
              <div class="article-sheet__meta"><span>ORCHESTRATION</span><b>01 / 08</b></div>
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
              <div class="article-sheet__art" aria-hidden="true">
                <img src="assets/images/disk/card-art.jpg" alt="" loading="lazy">
              </div>
              <div class="article-sheet__meta"><span>DATA ARCHITECTURE</span><b>02 / 08</b></div>
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
              <div class="article-sheet__art" aria-hidden="true">
                <img src="assets/images/index/card-art.jpg" alt="" loading="lazy">
              </div>
              <div class="article-sheet__meta"><span>DATABASE INTERNALS</span><b>03 / 08</b></div>
              <div class="article-sheet__body">
                <span class="article-sheet__status article-sheet__status--published">Đã xuất bản</span>
                <h2>Index trong<br>cơ sở dữ liệu</h2>
                <p>Từ full table scan đến cấu trúc dữ liệu giúp database tìm bản ghi nhanh hơn.</p>
              </div>
              <div class="article-sheet__foot">
                <span>Tác giả · Phong Thanh</span>
                <a href="index/">Mở bài viết <b aria-hidden="true">↗</b></a>
              </div>
            </article>

            <article class="article-sheet article-sheet--postgres" data-article-title="Phân cấp &amp; Lưu trữ PostgreSQL" data-deck-position="hidden">
              <div class="article-sheet__art" aria-hidden="true">
                <img src="assets/images/postgres/card-art.jpg" alt="" loading="lazy">
              </div>
              <div class="article-sheet__meta"><span>DATABASE INTERNALS</span><b>04 / 08</b></div>
              <div class="article-sheet__body">
                <span class="article-sheet__status article-sheet__status--published">Bài mới nhất</span>
                <h2>PostgreSQL<br>Phân cấp &amp; lưu trữ</h2>
                <p>Database cluster, bộ đệm shared_buffers, database, schema và cấu trúc thư mục PGDATA.</p>
              </div>
              <div class="article-sheet__foot">
                <span>DATABASE INTERNALS</span>
                <a href="postgres/postgres/">Mở bài viết <b aria-hidden="true">↗</b></a>
              </div>
            </article>

            <article class="article-sheet article-sheet--planned" data-article-title="Apache Spark internals" data-deck-position="hidden">
              <div class="article-sheet__art" aria-hidden="true">
                <img src="assets/images/spark/card-art.jpg" alt="" loading="lazy">
              </div>
              <div class="article-sheet__meta"><span>PROCESSING</span><b>05 / 08</b></div>
              <div class="article-sheet__body">
                <span class="article-sheet__status">Trong lộ trình</span>
                <h2>Apache Spark<br>internals</h2>
                <p>Partition, DAG execution, shuffle và cách một job thật sự chạy qua cluster.</p>
              </div>
              <div class="article-sheet__foot"><span>Dự kiến</span><em>Đang lên dàn ý</em></div>
            </article>

            <article class="article-sheet article-sheet--planned article-sheet--clay" data-article-title="Apache Kafka internals" data-deck-position="hidden">
              <div class="article-sheet__art" aria-hidden="true">
                <img src="assets/images/kafka/card-art.jpg" alt="" loading="lazy">
              </div>
              <div class="article-sheet__meta"><span>STREAMING</span><b>06 / 08</b></div>
              <div class="article-sheet__body">
                <span class="article-sheet__status">Trong lộ trình</span>
                <h2>Apache Kafka<br>internals</h2>
                <p>Log phân tán, partition ownership và những đánh đổi của delivery semantics.</p>
              </div>
              <div class="article-sheet__foot"><span>Dự kiến</span><em>Chờ nghiên cứu</em></div>
            </article>

            <article class="article-sheet article-sheet--planned article-sheet--blue" data-article-title="dbt: từ SQL đến lineage" data-deck-position="hidden">
              <div class="article-sheet__art" aria-hidden="true">
                <img src="assets/images/dbt/card-art.jpg" alt="" loading="lazy">
              </div>
              <div class="article-sheet__meta"><span>TRANSFORMATION</span><b>07 / 08</b></div>
              <div class="article-sheet__body">
                <span class="article-sheet__status">Trong lộ trình</span>
                <h2>dbt: từ SQL<br>đến lineage</h2>
                <p>Compiler, materialization và cách tổ chức transformation thành sản phẩm dữ liệu.</p>
              </div>
              <div class="article-sheet__foot"><span>Dự kiến</span><em>Chờ nghiên cứu</em></div>
            </article>

            <article class="article-sheet article-sheet--planned article-sheet--ink" data-article-title="Docker và Kubernetes cho Data Engineer" data-deck-position="hidden">
              <div class="article-sheet__art" aria-hidden="true">
                <img src="assets/images/docker/card-art.jpg" alt="" loading="lazy">
              </div>
              <div class="article-sheet__meta"><span>INFRASTRUCTURE</span><b>08 / 08</b></div>
              <div class="article-sheet__body">
                <span class="article-sheet__status">Trong lộ trình</span>
                <h2>Docker &amp; Kubernetes<br>cho Data Engineer</h2>
                <p>Từ một container đến workload dữ liệu có thể deploy, quan sát và phục hồi.</p>
              </div>
              <div class="article-sheet__foot"><span>Dự kiến</span><em>Chờ nghiên cứu</em></div>
            </article>
          </div>

          <div class="article-deck__controls">
            <button class="article-deck__control" type="button" data-deck-action="previous" aria-label="Xem bài trước">←</button>
            <p id="article-deck-help"><b>Lật bài</b> bằng nút, phím mũi tên hoặc kéo sang trái</p>
            <button class="article-deck__control" type="button" data-deck-action="next" aria-label="Xem bài tiếp theo">→</button>
          </div>
          <p class="article-deck__announcement" aria-live="polite" aria-atomic="true"></p>
        </div>

        <div class="stack-card__footer">
          <span><b>04</b> bài đã mở</span>
          <span><b>04</b> bài sắp tới</span>
          <span class="article-deck__count"><b>04</b> / 08</span>
        </div>
      </div>

      <span class="hero-orbit hero-orbit--one" aria-hidden="true"></span>
      <span class="hero-orbit hero-orbit--two" aria-hidden="true"></span>
    </div>
  </section>

  <section class="library-section" id="thu-vien" aria-labelledby="library-title">
    <div class="blueprint-watermark blueprint-watermark--shelf" aria-hidden="true">
      <img src="assets/images/home/blueprint-shelf.svg" alt="" width="1200" height="700" loading="lazy">
    </div>
    <div class="section-heading section-heading--split">
      <div>
        <p class="section-eyebrow">THE KNOWLEDGE SHELF / 01</p>
        <h2 id="library-title">Hôm nay bạn muốn<br>tìm hiểu điều gì?</h2>
      </div>
    </div>

    <div class="published-articles" aria-label="Bốn bài viết đã xuất bản">
      <article class="published-article published-article--latest published-article--postgres">
        <span class="published-article__number" aria-hidden="true">04</span>
        <div class="published-article__header">
          <svg class="published-article__illustration" viewBox="0 0 360 196" fill="none" aria-hidden="true" focusable="false"><path class="diagram-route" d="M180 45V64M70 82V64H290V82M180 64V82M70 112V137M180 112V137M290 112V137"/><g class="diagram-node diagram-node--accent"><rect x="128" y="15" width="104" height="30" rx="6"/><text x="180.0" y="34">CLUSTER</text></g><g class="diagram-node"><rect x="28" y="82" width="84" height="30" rx="6"/><text x="70.0" y="101">database</text></g><g class="diagram-node"><rect x="138" y="82" width="84" height="30" rx="6"/><text x="180.0" y="101">database</text></g><g class="diagram-node"><rect x="248" y="82" width="84" height="30" rx="6"/><text x="290.0" y="101">database</text></g><g class="diagram-node"><path d="M46 146v16c0 10 48 10 48 0v-16"/><ellipse cx="70" cy="146" rx="24" ry="8"/></g><g class="diagram-node"><path d="M156 146v16c0 10 48 10 48 0v-16"/><ellipse cx="180" cy="146" rx="24" ry="8"/></g><g class="diagram-node"><path d="M266 146v16c0 10 48 10 48 0v-16"/><ellipse cx="290" cy="146" rx="24" ry="8"/></g><circle class="diagram-signal" cx="180" cy="64" r="4"/></svg>
          <p class="published-article__meta">DATABASE INTERNALS · ED. 04</p>
          <span class="published-article__status">Bài mới nhất</span>
        </div>
        <h3>PostgreSQL<br>Phân cấp &amp; lưu trữ</h3>
        <p>Database cluster, bộ đệm shared_buffers, database, schema và cấu trúc thư mục PGDATA.</p>
        <a href="postgres/postgres/">Đọc bài viết <b aria-hidden="true"><svg viewBox="0 0 24 24" fill="none"><path d="M6 18 18 6M6 6h12v12"/></svg></b></a>
      </article>

      <article class="published-article published-article--index">
        <span class="published-article__number" aria-hidden="true">03</span>
        <div class="published-article__header">
          <svg class="published-article__illustration" viewBox="0 0 360 196" fill="none" aria-hidden="true" focusable="false"><path class="diagram-route" d="M180 43V63H80V82M180 63H280V82M80 112V134H38V148M80 134H125V148M280 112V134H235V148M280 134H322V148"/><path class="diagram-route diagram-route--accent" d="M180 43V63H280V82M280 112V134H235V148"/><g class="diagram-node diagram-node--accent"><rect x="149" y="13" width="62" height="30" rx="6"/><text x="180.0" y="32">42</text></g><g class="diagram-node"><rect x="49" y="82" width="62" height="30" rx="6"/><text x="80.0" y="101">18</text></g><g class="diagram-node diagram-node--accent"><rect x="249" y="82" width="62" height="30" rx="6"/><text x="280.0" y="101">67</text></g><g class="diagram-node"><rect x="8" y="148" width="60" height="30" rx="6"/><text x="38.0" y="167">08 · 12</text></g><g class="diagram-node"><rect x="95" y="148" width="60" height="30" rx="6"/><text x="125.0" y="167">24 · 36</text></g><g class="diagram-node diagram-node--accent"><rect x="205" y="148" width="60" height="30" rx="6"/><text x="235.0" y="167">51 · 58</text></g><g class="diagram-node"><rect x="292" y="148" width="60" height="30" rx="6"/><text x="322.0" y="167">73 · 91</text></g><circle class="diagram-signal" cx="235" cy="134" r="4"/></svg>
          <p class="published-article__meta">DATABASE INTERNALS · ED. 03</p>
        </div>
        <h3>Index trong<br>cơ sở dữ liệu</h3>
        <p>Từ full table scan đến cấu trúc dữ liệu giúp database tìm bản ghi nhanh hơn.</p>
        <a href="index/">Đọc bài viết <b aria-hidden="true"><svg viewBox="0 0 24 24" fill="none"><path d="M6 18 18 6M6 6h12v12"/></svg></b></a>
      </article>

      <article class="published-article published-article--airflow">
        <span class="published-article__number" aria-hidden="true">01</span>
        <div class="published-article__header">
          <svg class="published-article__illustration" viewBox="0 0 360 196" fill="none" aria-hidden="true" focusable="false"><path class="diagram-route" d="M69 94H110V40H145M110 94V148H145M215 40H249V94H289M215 148H249V94M215 94H289M110 94H145"/><g class="diagram-node diagram-node--accent"><rect x="7" y="79" width="62" height="30" rx="6"/><text x="38.0" y="98">DAG</text></g><g class="diagram-node"><rect x="145" y="25" width="70" height="30" rx="6"/><text x="180.0" y="44">extract</text></g><g class="diagram-node"><rect x="145" y="79" width="70" height="30" rx="6"/><text x="180.0" y="98">check</text></g><g class="diagram-node"><rect x="145" y="133" width="70" height="30" rx="6"/><text x="180.0" y="152">load</text></g><g class="diagram-node diagram-node--accent"><rect x="289" y="79" width="64" height="30" rx="6"/><text x="321.0" y="98">ready</text></g><circle class="diagram-signal" cx="110" cy="94" r="4"/><circle class="diagram-signal diagram-signal--late" cx="249" cy="94" r="4"/></svg>
          <p class="published-article__meta">ORCHESTRATION · ED. 01</p>
        </div>
        <h3>Hiểu kiến trúc<br>Apache Airflow</h3>
        <p>Từ nhu cầu điều phối đến Scheduler, Executor và High Availability.</p>
        <a href="airflow/architecture/">Đọc bài viết <b aria-hidden="true"><svg viewBox="0 0 24 24" fill="none"><path d="M6 18 18 6M6 6h12v12"/></svg></b></a>
      </article>

      <article class="published-article published-article--storage">
        <span class="published-article__number" aria-hidden="true">02</span>
        <div class="published-article__header">
          <svg class="published-article__illustration" viewBox="0 0 360 196" fill="none" aria-hidden="true" focusable="false"><path class="diagram-divider" d="M180 15V176"/><path class="diagram-route" d="M45 58V90H135V58M90 90V116M225 58V116M315 58V116"/><g class="diagram-node"><rect x="18" y="28" width="54" height="30" rx="6"/><text x="45.0" y="47">CPU</text></g><g class="diagram-node"><rect x="108" y="28" width="54" height="30" rx="6"/><text x="135.0" y="47">CPU</text></g><g class="diagram-node"><rect x="198" y="28" width="54" height="30" rx="6"/><text x="225.0" y="47">CPU</text></g><g class="diagram-node"><rect x="288" y="28" width="54" height="30" rx="6"/><text x="315.0" y="47">CPU</text></g><g class="diagram-node diagram-node--accent"><path d="M63 125v23c0 12 54 12 54 0v-23"/><ellipse cx="90" cy="125" rx="27" ry="9"/></g><g class="diagram-node diagram-node--accent"><path d="M198 125v23c0 12 54 12 54 0v-23"/><ellipse cx="225" cy="125" rx="27" ry="9"/></g><g class="diagram-node diagram-node--accent"><path d="M288 125v23c0 12 54 12 54 0v-23"/><ellipse cx="315" cy="125" rx="27" ry="9"/></g><text class="diagram-caption" x="90" y="181">SHARED DISK</text><text class="diagram-caption" x="270" y="181">SHARED NOTHING</text><circle class="diagram-signal" cx="90" cy="90" r="4"/></svg>
          <p class="published-article__meta">DATA ARCHITECTURE · ED. 02</p>
        </div>
        <h3>Shared-disk vs<br>shared-nothing</h3>
        <p>Chọn topology dữ liệu từ góc nhìn Data Engineer: query, shuffle và failure.</p>
        <a href="architecture/shared-disk-vs-shared-nothing/">Đọc bài viết <b aria-hidden="true"><svg viewBox="0 0 24 24" fill="none"><path d="M6 18 18 6M6 6h12v12"/></svg></b></a>
      </article>
    </div>

  </section>

  <section class="writing-section" id="cach-viet" aria-labelledby="writing-title">
    <div class="blueprint-watermark blueprint-watermark--writing" aria-hidden="true">
      <img src="assets/images/home/blueprint-writing.svg" alt="" width="1440" height="600" loading="lazy">
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
      <div class="dag-node dag-node--source"><span>SOURCE</span><i class="dag-portal dag-portal--source"></i></div>
      <div class="dag-connector"></div>
      <div class="dag-node dag-node--active dag-node--step-1"><span>01 · PROBLEM</span><i></i></div>
      <div class="dag-connector"></div>
      <div class="dag-node dag-node--active dag-node--step-2"><span>02 · INTERNALS</span><i></i></div>
      <div class="dag-connector"></div>
      <div class="dag-node dag-node--active dag-node--step-3"><span>03 · TRADE-OFF</span><i></i></div>
      <div class="dag-connector"></div>
      <div class="dag-node dag-node--production"><span>PRODUCTION</span><i class="dag-portal dag-portal--production"></i></div>

      <div class="dag-track-runner">
        <div class="dag-vehicle">
          <div class="dag-vehicle__chassis">
            <img class="dag-vehicle__body" src="assets/images/home/chicken-car.webp" alt="" width="56" height="44" />
            <img class="dag-vehicle__wheel dag-vehicle__wheel--rear" src="assets/images/home/chicken-wheel.webp" alt="" width="13" height="13" />
            <img class="dag-vehicle__wheel dag-vehicle__wheel--front" src="assets/images/home/chicken-wheel.webp" alt="" width="13" height="13" />
          </div>
        </div>
      </div>
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
      <img src="assets/images/home/blueprint-author.svg" alt="" width="1440" height="600" loading="lazy">
    </div>

    <div class="author-section__masthead">
      <p>PERSONAL LOG / 001</p>
      <span>PEOPLE BEHIND THE NOTES</span>
    </div>

    <div class="author-primary-card">
      <span class="author-primary-card__watermark" aria-hidden="true">TOGETHER</span>
      <figure class="author-photo">
        <div class="author-photo__frame">
          <img src="assets/images/home/phong-thanh-at-the-sea.webp" alt="Người viết đứng bên bờ biển" width="1920" height="1296" loading="lazy">
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
          <img src="assets/images/home/danh.png" alt="Đồng tác giả Danh đứng bên bờ biển" width="460" height="460" loading="lazy">
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
