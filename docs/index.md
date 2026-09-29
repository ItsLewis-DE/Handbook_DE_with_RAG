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
      <h1 id="landing-title">
        <span>Hiểu sâu thế giới</span>
        <em>Data Engineering.</em>
      </h1>
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

            <article class="article-sheet article-sheet--spark" data-article-title="Kiến trúc Apache Spark (phần 1)" data-deck-position="next">
              <div class="article-sheet__art" aria-hidden="true">
                <img src="assets/images/spark/card-art.jpg" alt="" loading="lazy">
              </div>
              <div class="article-sheet__meta"><span>DISTRIBUTED COMPUTING</span><b>02 / 08</b></div>
              <div class="article-sheet__body">
                <span class="article-sheet__status article-sheet__status--published">Đã xuất bản</span>
                <h2>Kiến trúc<br>Apache Spark (phần 1)</h2>
                <p>Từ Driver và Executor đến luồng thực thi Job, Stage, Task và cơ chế shuffle.</p>
              </div>
              <div class="article-sheet__foot">
                <span>DISTRIBUTED COMPUTING</span>
                <a href="spark/archi/">Mở bài viết <b aria-hidden="true">↗</b></a>
              </div>
            </article>

            <article class="article-sheet article-sheet--spark" data-article-title="Kiến trúc Apache Spark (phần 2)" data-deck-position="back">
              <div class="article-sheet__art" aria-hidden="true">
                <img src="assets/images/spark/card-art.jpg" alt="" loading="lazy">
              </div>
              <div class="article-sheet__meta"><span>DISTRIBUTED COMPUTING</span><b>03 / 08</b></div>
              <div class="article-sheet__body">
                <span class="article-sheet__status article-sheet__status--published">Đã xuất bản</span>
                <h2>Kiến trúc<br>Apache Spark (phần 2)</h2>
                <p>Các chiến lược Join, vai trò của RDD, giao tiếp PySpark và quản lý bộ nhớ Driver, Executor.</p>
              </div>
              <div class="article-sheet__foot">
                <span>DISTRIBUTED COMPUTING</span>
                <a href="spark/p2/">Mở bài viết <b aria-hidden="true">↗</b></a>
              </div>
            </article>

            <article class="article-sheet article-sheet--index" data-article-title="Index trong cơ sở dữ liệu" data-deck-position="hidden">
              <div class="article-sheet__art" aria-hidden="true">
                <img src="assets/images/index/card-art.jpg" alt="" loading="lazy">
              </div>
              <div class="article-sheet__meta"><span>DATABASE INTERNALS</span><b>04 / 08</b></div>
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

            <article class="article-sheet article-sheet--postgres" data-article-title="PostgreSQL (phần 1): Phân cấp, tiến trình và bộ nhớ" data-deck-position="hidden">
              <div class="article-sheet__art" aria-hidden="true">
                <img src="assets/images/postgres/card-art.jpg" alt="" loading="lazy">
              </div>
              <div class="article-sheet__meta"><span>DATABASE INTERNALS</span><b>05 / 08</b></div>
              <div class="article-sheet__body">
                <span class="article-sheet__status article-sheet__status--published">Đã xuất bản</span>
                <h2>PostgreSQL (phần 1)<br>Phân cấp, tiến trình &amp; bộ nhớ</h2>
                <p>Cluster, database, schema, kết nối, cơ chế khóa và bộ nhớ phục vụ truy vấn.</p>
              </div>
              <div class="article-sheet__foot">
                <span>DATABASE INTERNALS</span>
                <a href="postgres/postgres/">Mở bài viết <b aria-hidden="true">↗</b></a>
              </div>
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
          <span><b>05</b> bài đã mở</span>
          <span><b>03</b> bài sắp tới</span>
          <span class="article-deck__count"><b>05</b> / 08</span>
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
        <h2 id="library-title">4 bài viết mới nhất</h2>
      </div>
    </div>

    <div class="published-articles" aria-label="4 bài viết mới nhất">
      <article class="published-article published-article--spark">
        <span class="published-article__number" aria-hidden="true">06</span>
        <div class="published-article__header">
          <p class="published-article__meta">DISTRIBUTED COMPUTING · ED. 06</p>
        </div>
        <svg class="published-article__illustration" viewBox="0 0 360 196" fill="none" aria-hidden="true" focusable="false">
          <path class="diagram-route" d="M90 65V95H180V125M270 65V95H180"/>
          <g class="diagram-node"><rect x="40" y="35" width="100" height="30" rx="6"/><text x="90" y="54">TABLE A</text></g>
          <g class="diagram-node"><rect x="220" y="35" width="100" height="30" rx="6"/><text x="270" y="54">TABLE B</text></g>
          <g class="diagram-node diagram-node--accent"><rect x="130" y="125" width="100" height="30" rx="6"/><text x="180" y="144">JOIN</text></g>
          <circle class="diagram-signal" cx="180" cy="95" r="4"/>
        </svg>
        <h3>Kiến trúc<br>Apache Spark (phần 2)</h3>
        <p>Các chiến lược Join, vai trò của RDD, giao tiếp PySpark và quản lý bộ nhớ Driver, Executor.</p>
        <a href="spark/p2/" aria-label="Đọc bài viết: Kiến trúc Apache Spark (phần 2)">Đọc bài viết <b aria-hidden="true"><svg viewBox="0 0 24 24" fill="none"><path d="M6 18 18 6M6 6h12v12"/></svg></b></a>
      </article>

      <article class="published-article published-article--spark">
        <span class="published-article__number" aria-hidden="true">05</span>
        <div class="published-article__header">
          <p class="published-article__meta">DISTRIBUTED COMPUTING · ED. 05</p>
        </div>
        <svg class="published-article__illustration" viewBox="0 0 360 196" fill="none" aria-hidden="true" focusable="false">
          <path class="diagram-route" d="M180 45V70M60 95V70H300V95M180 70V95M60 125V149M180 125V149M300 125V149"/>
          <g class="diagram-node diagram-node--accent"><rect x="132" y="15" width="96" height="30" rx="6"/><text x="180" y="34">DRIVER</text></g>
          <g class="diagram-node"><rect x="12" y="95" width="96" height="30" rx="6"/><text x="60" y="114">Executor</text></g>
          <g class="diagram-node"><rect x="132" y="95" width="96" height="30" rx="6"/><text x="180" y="114">Executor</text></g>
          <g class="diagram-node"><rect x="252" y="95" width="96" height="30" rx="6"/><text x="300" y="114">Executor</text></g>
          <g class="diagram-node diagram-node--accent"><rect x="24" y="149" width="72" height="28" rx="6"/><text x="60" y="167">TASKS</text></g>
          <g class="diagram-node diagram-node--accent"><rect x="144" y="149" width="72" height="28" rx="6"/><text x="180" y="167">TASKS</text></g>
          <g class="diagram-node diagram-node--accent"><rect x="264" y="149" width="72" height="28" rx="6"/><text x="300" y="167">TASKS</text></g>
          <circle class="diagram-signal" cx="180" cy="70" r="4"/>
        </svg>
        <h3>Kiến trúc<br>Apache Spark (phần 1)</h3>
        <p>Từ Driver và Executor đến luồng thực thi Job, Stage, Task và cơ chế shuffle.</p>
        <a href="spark/archi/" aria-label="Đọc bài viết: Kiến trúc Apache Spark (phần 1)">Đọc bài viết <b aria-hidden="true"><svg viewBox="0 0 24 24" fill="none"><path d="M6 18 18 6M6 6h12v12"/></svg></b></a>
      </article>

      <article class="published-article published-article--postgres">
        <span class="published-article__number" aria-hidden="true">04</span>
        <div class="published-article__header">
          <p class="published-article__meta">DATABASE INTERNALS · PHẦN 2</p>
        </div>
        <svg class="published-article__illustration" viewBox="0 0 360 196" fill="none" aria-hidden="true" focusable="false">
          <path class="diagram-route" d="M98 49H130M230 49H260M310 64V107H180V137"/>
          <g class="diagram-node"><rect x="8" y="34" width="90" height="30" rx="6"/><text x="53" y="53">PARSER</text></g>
          <g class="diagram-node"><rect x="130" y="34" width="100" height="30" rx="6"/><text x="180" y="53">PLANNER</text></g>
          <g class="diagram-node diagram-node--accent"><rect x="260" y="34" width="96" height="30" rx="6"/><text x="308" y="53">EXECUTOR</text></g>
          <g class="diagram-node diagram-node--accent"><rect x="118" y="137" width="124" height="30" rx="6"/><text x="180" y="156">BUFFERS / WAL</text></g>
          <circle class="diagram-signal" cx="180" cy="107" r="4"/>
        </svg>
        <h3>PostgreSQL (phần 2)<br>Truy vấn, lưu trữ &amp; phục hồi</h3>
        <p>Hành trình SQL qua Parser, Planner, Executor đến bộ đệm, WAL, PGDATA và TOAST.</p>
        <a href="postgres/p2/" aria-label="Đọc bài viết: PostgreSQL (phần 2): Truy vấn, lưu trữ và phục hồi">Đọc bài viết <b aria-hidden="true"><svg viewBox="0 0 24 24" fill="none"><path d="M6 18 18 6M6 6h12v12"/></svg></b></a>
      </article>

      <article class="published-article published-article--postgres">
        <span class="published-article__number" aria-hidden="true">04</span>
        <div class="published-article__header">
          <p class="published-article__meta">DATABASE INTERNALS · PHẦN 1</p>
        </div>
        <svg class="published-article__illustration" viewBox="0 0 360 196" fill="none" aria-hidden="true" focusable="false"><path class="diagram-route" d="M180 45V64M70 82V64H290V82M180 64V82M70 112V137M180 112V137M290 112V137"/><g class="diagram-node diagram-node--accent"><rect x="128" y="15" width="104" height="30" rx="6"/><text x="180.0" y="34">CLUSTER</text></g><g class="diagram-node"><rect x="28" y="82" width="84" height="30" rx="6"/><text x="70.0" y="101">database</text></g><g class="diagram-node"><rect x="138" y="82" width="84" height="30" rx="6"/><text x="180.0" y="101">database</text></g><g class="diagram-node"><rect x="248" y="82" width="84" height="30" rx="6"/><text x="290.0" y="101">database</text></g><g class="diagram-node"><path d="M46 146v16c0 10 48 10 48 0v-16"/><ellipse cx="70" cy="146" rx="24" ry="8"/></g><g class="diagram-node"><path d="M156 146v16c0 10 48 10 48 0v-16"/><ellipse cx="180" cy="146" rx="24" ry="8"/></g><g class="diagram-node"><path d="M266 146v16c0 10 48 10 48 0v-16"/><ellipse cx="290" cy="146" rx="24" ry="8"/></g><circle class="diagram-signal" cx="180" cy="64" r="4"/></svg>
        <h3>PostgreSQL (phần 1)<br>Phân cấp, tiến trình &amp; bộ nhớ</h3>
        <p>Cluster, database, schema, kết nối, cơ chế khóa và bộ nhớ phục vụ truy vấn.</p>
        <a href="postgres/postgres/" aria-label="Đọc bài viết: PostgreSQL (phần 1): Phân cấp, tiến trình và bộ nhớ">Đọc bài viết <b aria-hidden="true"><svg viewBox="0 0 24 24" fill="none"><path d="M6 18 18 6M6 6h12v12"/></svg></b></a>
      </article>
    </div>

    <p class="library-section__all"><a href="library/">Xem tất cả bài viết <span aria-hidden="true">↗</span></a></p>

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
        <span class="writing-section__lead-label">PHƯƠNG PHÁP TRÌNH BÀY · 3 NGUYÊN TẮC</span>
        <p class="writing-section__lead">
          Mỗi bài viết được biên soạn theo mạch truyền tải có chủ đích: khơi gợi từ câu hỏi
          bản chất, trực quan hóa luồng vận hành bên trong, và đúc kết tư duy đánh đổi thực tế.
        </p>
      </div>
    </div>

    <div class="blueprint-dag-stream" aria-hidden="true">
      <div class="dag-node dag-node--source"><span>ORIGIN</span><i class="dag-portal dag-portal--source"></i></div>
      <div class="dag-connector"></div>
      <div class="dag-node dag-node--active dag-node--step-1"><span>01 · PRINCIPLE</span><i></i></div>
      <div class="dag-connector"></div>
      <div class="dag-node dag-node--active dag-node--step-2"><span>02 · VISUALIZE</span><i></i></div>
      <div class="dag-connector"></div>
      <div class="dag-node dag-node--active dag-node--step-3"><span>03 · TRADE-OFF</span><i></i></div>
      <div class="dag-connector"></div>
      <div class="dag-node dag-node--production"><span>INTUITION</span><i class="dag-portal dag-portal--production"></i></div>

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

    <div class="writing-principles" role="list" aria-label="3 nguyên tắc trình bày của tác giả">
      <article class="writing-card" data-step-number="01" role="listitem">
        <header class="writing-card__header">
          <div class="writing-card__stamp" aria-hidden="true">
            <small>BƯỚC</small><b>01</b>
          </div>
          <div class="writing-card__meta">
            <span class="writing-card__stage">GÓC NHÌN / ĐẶT VẤN ĐỀ</span>
          </div>
        </header>

        <div class="writing-card__flow">
          <span class="writing-card__flow-badge">WHY OVER WHAT</span>
        </div>

        <h3 class="writing-card__title">Khởi đầu từ câu hỏi bản chất</h3>
        <p class="writing-card__question">“Vì sao công nghệ này bắt buộc phải tồn tại?”</p>
        <p class="writing-card__desc">
          Thay vì liệt kê định nghĩa khô khan, bài viết luôn bắt đầu bằng bài toán thực tế
          và bối cảnh lịch sử. Đặt người đọc vào vị trí của người thiết kế để thấu hiểu
          động lực gốc rễ trước khi chạm vào cú pháp.
        </p>

        <footer class="writing-card__tags" aria-label="Khía cạnh phân tích">
          <span>First Principles</span>
          <span>Problem Context</span>
          <span>Design Motivation</span>
        </footer>
      </article>

      <article class="writing-card" data-step-number="02" role="listitem">
        <header class="writing-card__header">
          <div class="writing-card__stamp" aria-hidden="true">
            <small>BƯỚC</small><b>02</b>
          </div>
          <div class="writing-card__meta">
            <span class="writing-card__stage">MINH HỌA / BÓC TÁCH</span>
          </div>
        </header>

        <div class="writing-card__flow">
          <span class="writing-card__flow-badge">SHOW DON'T TELL</span>
        </div>

        <h3 class="writing-card__title">Trực quan hóa luồng vận hành</h3>
        <p class="writing-card__question">“Làm sao để người đọc nhìn thấy chuyển động của dữ liệu?”</p>
        <p class="writing-card__desc">
          Kiến trúc phức tạp được đơn giản hóa bằng sơ đồ luồng dữ liệu tự thiết kế và các phép
          ẩn dụ gần gũi. Tác giả biến những cơ chế trừu tượng thành hình ảnh mạch lạc, giúp
          người đọc nắm bắt trọn vẹn đường đi của hệ thống.
        </p>

        <footer class="writing-card__tags" aria-label="Khía cạnh phân tích">
          <span>Visual First</span>
          <span>Data Modeling</span>
          <span>Intuitive Diagrams</span>
        </footer>
      </article>

      <article class="writing-card" data-step-number="03" role="listitem">
        <header class="writing-card__header">
          <div class="writing-card__stamp" aria-hidden="true">
            <small>BƯỚC</small><b>03</b>
          </div>
          <div class="writing-card__meta">
            <span class="writing-card__stage">PHẢN BIỆN / ĐÁNH ĐỔI</span>
          </div>
        </header>

        <div class="writing-card__flow">
          <span class="writing-card__flow-badge">NO SILVER BULLET</span>
        </div>

        <h3 class="writing-card__title">Đúc kết ranh giới &amp; Đánh đổi</h3>
        <p class="writing-card__question">“Cái giá phải trả và giới hạn thực tế là gì?”</p>
        <p class="writing-card__desc">
          Không thần thánh hóa bất kỳ công cụ nào. Bài viết luôn khép lại bằng góc nhìn phản biện:
          chỉ rõ ranh giới phù hợp, cái giá phải trả và các điểm đánh đổi kinh điển, giúp người đọc
          tự tin ra quyết định kiến trúc độc lập.
        </p>

        <footer class="writing-card__tags" aria-label="Khía cạnh phân tích">
          <span>Trade-off Mindset</span>
          <span>Critical Thinking</span>
          <span>Practical Limits</span>
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
