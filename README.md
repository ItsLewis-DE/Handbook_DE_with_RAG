<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/assets/images/brand/behind-the-pipeline-logo-inverse.svg">
    <img src="docs/assets/images/brand/behind-the-pipeline-logo.svg" alt="Behind the Pipeline — Data Engineering Handbook" width="88">
  </picture>
  <h1>Data Engineering Handbook with RAG</h1>
  <p><strong>Retrieval-Augmented Generation for Data Engineering.</strong></p>
  <p>Hệ thống hỏi đáp tài liệu tiếng Việt với hybrid retrieval, câu trả lời có dẫn nguồn<br>và chatbot tích hợp trong website kiến thức Behind the Pipeline.</p>
  <a href="https://itslewis-de.github.io/Handbook_DE_with_RAG/">
    <img src="https://img.shields.io/badge/🌐_KHÁM_PHÁ_WEBSITE-GitHub_Pages-ed6840?style=for-the-badge&amp;labelColor=17302d" alt="Khám phá website trên GitHub Pages">
  </a>
  <p>
    <a href="https://itslewis-de.github.io/Handbook_DE_with_RAG/library/">Thư viện bài viết</a> ·
    <a href="#chatbot-đọc-cùng-bạn">Chatbot</a> ·
    <a href="#chạy-trên-máy-cá-nhân">Chạy tại local</a>
  </p>
</div>

> [!IMPORTANT]
> **[→ MỞ WEBSITE: itslewis-de.github.io/Handbook_DE_with_RAG](https://itslewis-de.github.io/Handbook_DE_with_RAG/)**
>
> Khám phá kho kiến thức Behind the Pipeline và giao diện chatbot. Chạy backend local theo hướng dẫn bên dưới để trải nghiệm hỏi đáp RAG.

## Về dự án

**Handbook DE with RAG** kết hợp cẩm nang Data Engineering với hệ thống hỏi đáp tài liệu. **Pipeline RAG** là phần **Retrieval-Augmented Generation (RAG)** cho kho kiến thức Data Engineering bằng tiếng Việt. Hệ thống xử lý tài liệu, tạo chỉ mục, truy xuất các đoạn liên quan và dùng mô hình ngôn ngữ để tạo câu trả lời kèm nguồn tham khảo. **Behind the Pipeline** là website xuất bản tài liệu và giao diện để người đọc tương tác với chatbot.

- **Hybrid retrieval:** kết hợp tìm kiếm vector trong Chroma với BM25 để tìm theo ngữ nghĩa và thuật ngữ kỹ thuật.
- **Truy xuất phân cấp:** chế độ mặc định `hierarchical` xử lý câu hỏi tổng quan qua cấu trúc tài liệu; câu hỏi chi tiết đi qua tách truy vấn, hybrid retrieval và reranking.
- **Xếp hạng lại:** `BAAI/bge-reranker-v2-m3` chấm điểm các đoạn theo câu hỏi gốc trước khi đưa vào ngữ cảnh.
- **Hợp nhất kết quả bằng RRF:** kết hợp thứ hạng của hai bộ tìm kiếm và chọn các section khác nhau làm ngữ cảnh.
- **Trả lời có dẫn nguồn:** liên kết từ câu trả lời về đúng phần trong bài viết; kiểm tra citation và xử lý trường hợp thiếu bằng chứng.
- **Mô hình chạy local:** Ollama phục vụ `qwen3:4b-instruct`; embedding đa ngôn ngữ dùng `intfloat/multilingual-e5-small`.
- **Pipeline có thể đánh giá:** các script và bộ câu hỏi trong `backend/` hỗ trợ đánh giá retrieval và câu trả lời.
- **Giao diện tích hợp:** API FastAPI kết nối chatbot ngay trong trang đọc bài, đi cùng thư viện kiến thức trực quan.

## Luồng hoạt động RAG

```mermaid
flowchart LR
    D[Markdown tài liệu] --> C[Chia đoạn và metadata]
    C --> E[Multilingual E5 embeddings]
    E --> V[(Chroma)]
    V --> B[BM25 trên corpus đã lưu]
    Q[Câu hỏi] --> T{Truy xuất phân cấp}
    T --> O[Ngữ cảnh tổng quan từ cấu trúc tài liệu]
    T --> P[Câu hỏi gốc và câu hỏi con]
    P --> H[Hybrid retrieval: vector + BM25]
    V --> H
    B --> H
    H --> R[RRF và chọn section]
    R --> X[BGE reranker]
    X --> L[Ollama / Qwen3]
    O --> L
    L --> A[Câu trả lời và nguồn tham khảo]
    A --> U[Chatbot trên website]
```

`ingest.py` tạo và lưu chỉ mục; `overview_retrieval.py` điều phối truy xuất phân cấp; `retrieval.py`, `decomposition.py` và `reranking.py` truy xuất ngữ cảnh chi tiết; `answering.py` sinh, kiểm tra câu trả lời và citation; `app.py` cung cấp API `/chat` cho giao diện.

## Chatbot đọc cùng bạn

<p align="center">
  <img src="assets/readme/chatbot.webp" alt="Khung chat Pip đang mở trên trang Airflow, có ngữ cảnh bài và câu hỏi gợi ý" width="960">
</p>

**Pip** là trợ lý đọc tài liệu, được mở qua biểu tượng robot ở góc trang bài viết. Khung chat hiển thị tên bài đang đọc, các gợi ý câu hỏi và ô nhập để trao đổi với backend RAG.

- Tìm nội dung liên quan bằng tìm kiếm ngữ nghĩa kết hợp BM25.
- Sinh câu trả lời tiếng Việt bằng Ollama với model `qwen3:4b-instruct`.
- Đính kèm nguồn tham khảo, liên kết tới đúng phần trong bài viết.
- Có xử lý trường hợp thiếu bằng chứng, lỗi kết nối và thời gian chờ.
- Hỗ trợ `Enter` để gửi, `Shift + Enter` để xuống dòng và `Escape` để thu nhỏ.

Ví dụ câu hỏi: “Executor trong Airflow làm gì?”, “Shared-disk khác shared-nothing thế nào?” hoặc “shared_buffers có vai trò gì trong PostgreSQL?”.

> [!NOTE]
> GitHub Pages phục vụ website tĩnh. Chatbot hiện mặc định gọi `http://127.0.0.1:8001/chat` và cần backend chạy riêng; chưa có API công khai được cấu hình sẵn. Ảnh trên là giao diện chào của chatbot, không phải một phiên trả lời trực tuyến. Chỉ mục hiện bao gồm bài Airflow, Shared-disk vs. shared-nothing, PostgreSQL và Index.

## Nội dung trong thư viện

Thư viện hiện có **6 bài viết tiếng Việt** trong bốn chủ đề. Ba bài Airflow, PostgreSQL và Index còn có bản tiếng Anh. Backend RAG hiện lập chỉ mục **4 bài**: Airflow, Shared-disk vs. shared-nothing, PostgreSQL và Index.

| Chủ đề | Bài viết |
| --- | --- |
| Data Architecture | [Shared-disk vs shared-nothing](https://itslewis-de.github.io/Handbook_DE_with_RAG/architecture/shared-disk-vs-shared-nothing/) · [Data Lake, Data Warehouse và Data Mart](https://itslewis-de.github.io/Handbook_DE_with_RAG/ware_lake_lw/doc/) |
| Database Internals | [Phân cấp & lưu trữ PostgreSQL](https://itslewis-de.github.io/Handbook_DE_with_RAG/postgres/postgres/) · [Index trong cơ sở dữ liệu](https://itslewis-de.github.io/Handbook_DE_with_RAG/index/) |
| Orchestration | [Kiến trúc Apache Airflow](https://itslewis-de.github.io/Handbook_DE_with_RAG/airflow/architecture/) |
| Distributed Computing | [Kiến trúc Apache Spark](https://itslewis-de.github.io/Handbook_DE_with_RAG/spark/archi/) |

**Trong lộ trình:** Apache Kafka, dbt, Docker và Kubernetes cho Data Engineer.

## Hình ảnh demo

Ảnh chụp từ **bản build hiện tại của dự án**. Nhấn vào ảnh để xem lớn hoặc mở trang tương ứng. Các ảnh chatbot chỉ thể hiện giao diện chào; câu trả lời RAG cần backend local.

### Trang chủ và thư viện

[![Trang chủ Behind the Pipeline với bộ bài viết dạng chồng giấy](assets/readme/home.webp)](https://itslewis-de.github.io/Handbook_DE_with_RAG/)

*Trang chủ: bài viết dạng chồng giấy, có thể lật và mở bài.*

[![Thư viện gồm sáu card bài viết, bộ lọc chủ đề và ô tìm kiếm](assets/readme/library.webp)](https://itslewis-de.github.io/Handbook_DE_with_RAG/library/)

*Thư viện: cả card dẫn đến bài viết; có lọc theo chủ đề và tìm theo tiêu đề hoặc nội dung card.*

### Điều hướng và các tính năng

| Chọn bài trên trang chủ | Mở menu Thư viện |
| --- | --- |
| [<img src="assets/readme/home-article-cards.webp" alt="Bốn card bài viết đã xuất bản trên trang chủ" width="680">](assets/readme/home-article-cards.webp) | [<img src="assets/readme/navigation-library.webp" alt="Menu Thư viện chia bài theo bốn chủ đề" width="680">](assets/readme/navigation-library.webp) |
| **Lật bộ bài viết trên trang chủ** | **Tìm bài trong Thư viện** |
| [<img src="assets/readme/home-deck-next.webp" alt="Bộ bài viết trên trang chủ sau khi lật sang bài tiếp theo" width="680">](assets/readme/home-deck-next.webp) | [<img src="assets/readme/library-search.webp" alt="Tìm Spark trong Thư viện và nhận một card kết quả" width="680">](assets/readme/library-search.webp) |
| **Lọc bài trong thư viện** | **Mở tìm kiếm của website** |
| [<img src="assets/readme/library-filter.webp" alt="Thư viện lọc còn hai bài Database Internals" width="680">](assets/readme/library-filter.webp) | [<img src="assets/readme/site-search.webp" alt="Giao diện tìm kiếm toàn website đang mở" width="680">](assets/readme/site-search.webp) |
| **Chatbot Pip trên trang bài viết** | **Đọc bài với mục lục và lựa chọn ngôn ngữ** |
| [<img src="assets/readme/chatbot.webp" alt="Khung chat Pip mở trên trang Airflow, hiển thị ngữ cảnh bài và câu hỏi gợi ý" width="680">](assets/readme/chatbot.webp) | [<img src="assets/readme/article-airflow.webp" alt="Trang Airflow có mục lục và bộ chọn Tiếng Việt hoặc English" width="680">](assets/readme/article-airflow.webp) |

### Sáu trang bài viết

| Data Architecture | Database Internals |
| --- | --- |
| [<img src="assets/readme/article-shared-disk.webp" alt="Trang bài viết Shared-disk vs shared-nothing" width="680">](https://itslewis-de.github.io/Handbook_DE_with_RAG/architecture/shared-disk-vs-shared-nothing/)<br>[Shared-disk vs shared-nothing](https://itslewis-de.github.io/Handbook_DE_with_RAG/architecture/shared-disk-vs-shared-nothing/) | [<img src="assets/readme/article-postgres.webp" alt="Trang bài viết Phân cấp và lưu trữ PostgreSQL" width="680">](https://itslewis-de.github.io/Handbook_DE_with_RAG/postgres/postgres/)<br>[Phân cấp & lưu trữ PostgreSQL](https://itslewis-de.github.io/Handbook_DE_with_RAG/postgres/postgres/) |
| [<img src="assets/readme/article-data-lake.webp" alt="Trang bài viết Data Lake, Data Warehouse và Data Mart" width="680">](https://itslewis-de.github.io/Handbook_DE_with_RAG/ware_lake_lw/doc/)<br>[Data Lake, Data Warehouse và Data Mart](https://itslewis-de.github.io/Handbook_DE_with_RAG/ware_lake_lw/doc/) | [<img src="assets/readme/article-index.webp" alt="Trang bài viết Index trong cơ sở dữ liệu" width="680">](https://itslewis-de.github.io/Handbook_DE_with_RAG/index/)<br>[Index trong cơ sở dữ liệu](https://itslewis-de.github.io/Handbook_DE_with_RAG/index/) |
| **Orchestration** | **Distributed Computing** |
| [<img src="assets/readme/article-airflow.webp" alt="Trang bài viết Kiến trúc Apache Airflow" width="680">](https://itslewis-de.github.io/Handbook_DE_with_RAG/airflow/architecture/)<br>[Kiến trúc Apache Airflow](https://itslewis-de.github.io/Handbook_DE_with_RAG/airflow/architecture/) | [<img src="assets/readme/article-spark.webp" alt="Trang bài viết Kiến trúc Apache Spark" width="680">](https://itslewis-de.github.io/Handbook_DE_with_RAG/spark/archi/)<br>[Kiến trúc Apache Spark](https://itslewis-de.github.io/Handbook_DE_with_RAG/spark/archi/) |

### Ba bản tiếng Anh

| PostgreSQL | Index | Airflow |
| --- | --- | --- |
| [<img src="assets/readme/article-postgres-en.webp" alt="PostgreSQL Hierarchy and Storage in English" width="450">](https://itslewis-de.github.io/Handbook_DE_with_RAG/postgres/postgres.en/) | [<img src="assets/readme/article-index-en.webp" alt="Indexes in Databases in English" width="450">](https://itslewis-de.github.io/Handbook_DE_with_RAG/index/index.en/) | [<img src="assets/readme/article-airflow-en.webp" alt="Apache Airflow Architecture in English" width="450">](https://itslewis-de.github.io/Handbook_DE_with_RAG/airflow/architecture.en/) |

### Giao diện điện thoại

| Trang chủ | Menu Thư viện | Trang Thư viện | Trang đọc bài |
| --- | --- | --- | --- |
| [<img src="assets/readme/mobile-home.webp" alt="Trang chủ trên điện thoại" width="270">](assets/readme/mobile-home.webp) | [<img src="assets/readme/mobile-navigation.webp" alt="Menu Thư viện trên điện thoại" width="270">](assets/readme/mobile-navigation.webp) | [<img src="assets/readme/mobile-library.webp" alt="Trang Thư viện trên điện thoại" width="270">](assets/readme/mobile-library.webp) | [<img src="assets/readme/mobile-article.webp" alt="Trang đọc bài Airflow trên điện thoại" width="270">](assets/readme/mobile-article.webp) |

### Ngôn ngữ đọc bài viết

Bài Airflow, PostgreSQL và Index có bản **Tiếng Việt / English**. Bộ chọn ở đầu bài chuyển giữa hai bản và giữ mục đang đọc theo URL fragment; liên kết vẫn hoạt động khi tắt JavaScript. Các bài chưa dịch có thông báo “Chưa có bản tiếng Anh”. Giao diện chung và chatbot vẫn dùng tiếng Việt.

Bản tiếng Anh giữ thứ tự các mục, ví dụ mã, bảng và sơ đồ của bản tiếng Việt. Ảnh minh họa gốc được giữ nguyên (bao gồm chữ trong ảnh); caption và alt text được dịch sang tiếng Anh.

Để thêm cặp bản dịch, đặt `lang` và cùng một `translation_key` trong front matter, khai báo các đường dẫn trong `extra.article_translations` của `mkdocs.yml`, rồi thêm trang mới vào `nav`. Giữ các heading tương ứng theo đúng thứ tự; hook dùng anchor của bản Việt cho cả hai ngôn ngữ và báo lỗi khi số heading khác nhau. Khi sửa bài gốc, cập nhật bản dịch cùng lúc.

Kiểm tra sau khi build:

```bash
uv run mkdocs build --strict
uv run scripts/check_reading_languages.py
```

## Công nghệ

| Thành phần | Công nghệ |
| --- | --- |
| Website | MkDocs Material, Markdown, HTML, CSS, JavaScript |
| Xuất bản | GitHub Pages |
| API chatbot | Python, FastAPI, Uvicorn |
| RAG | LangChain, Chroma, BM25 |
| Embedding | `intfloat/multilingual-e5-small` |
| Reranker | `BAAI/bge-reranker-v2-m3` |
| Mô hình trả lời | Ollama · `qwen3:4b-instruct` |
| Quản lý dependency | uv |

## Chạy trên máy cá nhân

### Website

Cần **Python 3.12+** và [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/ItsLewis-DE/Handbook_DE_with_RAG.git
cd Handbook_DE_with_RAG
uv sync
uv run mkdocs serve
```

Mở **http://127.0.0.1:8000**. Để kiểm tra bản build:

```bash
uv run mkdocs build --strict
```

Kết quả được tạo trong thư mục `site/`.

### Backend chatbot

Cài [Ollama](https://ollama.com/), khởi động dịch vụ và tải model:

```bash
ollama pull qwen3:4b-instruct
```

Mở terminal khác, từ thư mục gốc dự án:

```bash
cd backend
uv sync
uv run python ingest.py
uv run uvicorn app:app --host 127.0.0.1 --port 8001
```

Lần ingest đầu tiên cần tải model embedding và tạo chỉ mục tại `backend/.data/`. Chạy lại ingest sau khi cập nhật tài liệu trong danh sách `ARTICLE_PATHS` hoặc thay đổi cấu hình chỉ mục, rồi khởi động lại backend.

Luồng truy xuất chi tiết còn tải model reranker ở lần sử dụng đầu tiên.

Giữ cả website và backend đang chạy. Mở một bài viết trên website local, bấm robot Pip và nhập câu hỏi. Có thể kiểm tra API tại **http://127.0.0.1:8001/health** hoặc **http://127.0.0.1:8001/docs**.

Khi triển khai chatbot cho website công khai, cần một backend HTTPS, cấu hình `pip-chat-endpoint` trong thẻ meta của trang và thêm origin `https://itslewis-de.github.io` vào CORS tại `backend/app.py`. GitHub Pages chỉ lưu trữ phần giao diện.

### Xuất bản lên GitHub Pages

Website dùng nhánh `gh-pages` làm nguồn GitHub Pages. Từ thư mục gốc, chạy:

```bash
uv run mkdocs gh-deploy --strict
```

Lệnh này build website và push nội dung tĩnh lên `gh-pages`. Thay đổi mã nguồn và README cần được commit, push riêng lên `main`.

Địa chỉ hiện tại: **https://itslewis-de.github.io/Handbook_DE_with_RAG/**. Đường dẫn `/pipeline-rag/` cũ không còn phục vụ website sau khi repo đổi tên.

## Cấu trúc dự án

```text
.
├── docs/                 # Bài viết, landing page, hình ảnh, CSS và JavaScript
├── backend/              # API chatbot, ingestion, retrieval và đánh giá RAG
├── overrides/            # Tùy biến template MkDocs Material
├── assets/readme/        # Ảnh demo các trang, tính năng và giao diện mobile
├── scripts/              # Công cụ hỗ trợ phát triển
├── mkdocs.yml            # Điều hướng và cấu hình website
├── pyproject.toml        # Dependency cho website
└── uv.lock               # Phiên bản dependency được khóa
```

## Đóng góp

Bạn có thể [mở issue](https://github.com/ItsLewis-DE/Handbook_DE_with_RAG/issues) để báo lỗi, góp ý cách giải thích hoặc đề xuất chủ đề. Với thay đổi nội dung, hãy ghi rõ nguồn tham khảo, kiểm tra hình ảnh và liên kết, sau đó chạy `uv run mkdocs build --strict` trước khi gửi pull request.

---

<p align="center">
  <strong>Pipeline RAG — hỏi từ tài liệu, trả lời có nguồn.</strong><br>
  <a href="https://itslewis-de.github.io/Handbook_DE_with_RAG/">Khám phá thư viện →</a>
</p>
