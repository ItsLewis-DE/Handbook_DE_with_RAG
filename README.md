<div align="center">
  <img src="docs/assets/images/brand/behind-the-pipeline-logo.svg" alt="Behind the Pipeline" width="88">
  <h1>Behind the Pipeline</h1>
  <p><strong>Hiểu sâu thế giới Data Engineering.</strong></p>
  <p>Cẩm nang tiếng Việt về kiến trúc hệ thống dữ liệu, database internals<br>và những cơ chế phía sau các công cụ bạn sử dụng hằng ngày.</p>
  <a href="https://itslewis-de.github.io/behind-the-pipeline/">
    <img src="https://img.shields.io/badge/🌐_KHÁM_PHÁ_WEBSITE-GitHub_Pages-ed6840?style=for-the-badge&amp;labelColor=17302d" alt="Khám phá website trên GitHub Pages">
  </a>
  <p>
    <a href="https://itslewis-de.github.io/behind-the-pipeline/#thu-vien">Thư viện bài viết</a> ·
    <a href="#chatbot-đọc-cùng-bạn">Chatbot</a> ·
    <a href="#chạy-trên-máy-cá-nhân">Chạy tại local</a>
  </p>
</div>

> [!IMPORTANT]
> **[→ MỞ WEBSITE: itslewis-de.github.io/behind-the-pipeline](https://itslewis-de.github.io/behind-the-pipeline/)**
>
> Đọc bài viết, khám phá sơ đồ kiến trúc và tìm hiểu cách các hệ thống dữ liệu hoạt động từ bên trong.

[![Giao diện trang chủ Behind the Pipeline](assets/readme/website-desktop.png)](https://itslewis-de.github.io/behind-the-pipeline/)

## Về dự án

**Behind the Pipeline** đi từ bài toán thực tế đến kiến trúc, cơ chế vận hành và những đánh đổi khi thiết kế hệ thống. Dự án dành cho người đang học hoặc làm Data Engineering, muốn hiểu vì sao một công cụ tồn tại và khi nào nên sử dụng nó.

- **Kiến thức bằng tiếng Việt:** giải thích theo mạch bài toán → khái niệm → kiến trúc → vận hành → giới hạn.
- **Minh họa trực quan:** sơ đồ, hình ảnh và ví dụ gắn với nội dung bài viết.
- **Thư viện tương tác:** thẻ bài viết có thể lật bằng nút, phím mũi tên hoặc thao tác kéo.
- **Trải nghiệm đọc:** mục lục, tìm kiếm, liên kết tới từng phần và sao chép đoạn mã.
- **Chatbot RAG:** hỏi đáp trên tài liệu dự án, trả lời bằng tiếng Việt và dẫn nguồn về bài viết.

## Nội dung trong thư viện

| Chủ đề | Nội dung chính | Đọc trên website |
| --- | --- | --- |
| Data Architecture | Shared-disk, shared-nothing, data locality, shuffle, skew và mở rộng hệ thống | [Shared-disk vs. shared-nothing](https://itslewis-de.github.io/behind-the-pipeline/architecture/shared-disk-vs-shared-nothing/) |
| Apache Airflow | DAG, Scheduler, DAG File Processor, Executor và High Availability | [Kiến trúc Airflow](https://itslewis-de.github.io/behind-the-pipeline/airflow/architecture/) |
| PostgreSQL | Database cluster, schema, `shared_buffers` và cấu trúc lưu trữ | [Phân cấp & lưu trữ](https://itslewis-de.github.io/behind-the-pipeline/postgres/postgres/) |
| Database Index | Full table scan, cấu trúc index và cách database tìm bản ghi | [Index trong cơ sở dữ liệu](https://itslewis-de.github.io/behind-the-pipeline/index/) |
| Apache Spark | Kiến trúc, execution model, partition, shuffle, query planning, tuning và streaming | [Bộ bài Apache Spark](https://itslewis-de.github.io/behind-the-pipeline/spark/overview/) |

**Trong lộ trình:** Apache Kafka, dbt, Docker và Kubernetes cho Data Engineer.

## Thiết kế website

Giao diện sử dụng nền giấy sáng, màu xanh trầm và điểm nhấn cam; kết hợp họa tiết bản vẽ kỹ thuật với thẻ bài viết dạng chồng giấy. Trang bài viết dành nhiều không gian cho nội dung, mục lục và hình minh họa. Bố cục thích ứng với desktop và điện thoại, cùng font được lưu trong dự án.

![Trang bài viết Airflow với mục lục và robot mở chatbot](assets/readme/article-and-mascot.png)

*Ảnh chụp giao diện thật từ bản build của dự án: trang chủ ở phía trên và trang đọc bài Airflow cùng robot Pip.*

## Chatbot đọc cùng bạn

<p align="center">
  <img src="assets/readme/chatbot-panel.png" alt="Khung chat Tuất Danh Bình với ngữ cảnh bài Airflow, lời chào và câu hỏi gợi ý" width="460">
</p>

**Tuất Danh Bình** là trợ lý đọc tài liệu, được mở qua robot **Pip** ở góc trang bài viết. Khung chat hiển thị tên bài đang đọc, các gợi ý câu hỏi và ô nhập để trao đổi với backend RAG.

- Tìm nội dung liên quan bằng tìm kiếm ngữ nghĩa kết hợp BM25.
- Sinh câu trả lời tiếng Việt bằng Ollama với model `qwen3:4b-instruct`.
- Đính kèm nguồn tham khảo, liên kết tới đúng phần trong bài viết.
- Có xử lý trường hợp thiếu bằng chứng, lỗi kết nối và thời gian chờ.
- Hỗ trợ `Enter` để gửi, `Shift + Enter` để xuống dòng và `Escape` để thu nhỏ.

Ví dụ câu hỏi: “Executor trong Airflow làm gì?”, “Shared-disk khác shared-nothing thế nào?” hoặc “shared_buffers có vai trò gì trong PostgreSQL?”.

> [!NOTE]
> GitHub Pages phục vụ website tĩnh. Chatbot hiện mặc định gọi `http://127.0.0.1:8001/chat` và cần backend chạy riêng; chưa có API công khai được cấu hình sẵn. Ảnh trên là giao diện chào của chatbot, không phải một phiên trả lời trực tuyến. Chỉ mục hiện bao gồm bài Airflow, Shared-disk vs. shared-nothing, PostgreSQL và Index; bộ bài Spark chưa được đưa vào RAG.

## Công nghệ

| Thành phần | Công nghệ |
| --- | --- |
| Website | MkDocs Material, Markdown, HTML, CSS, JavaScript |
| Xuất bản | GitHub Pages |
| API chatbot | Python, FastAPI, Uvicorn |
| RAG | LangChain, Chroma, BM25 |
| Embedding | `intfloat/multilingual-e5-small` |
| Mô hình trả lời | Ollama · `qwen3:4b-instruct` |
| Quản lý dependency | uv |

## Chạy trên máy cá nhân

### Website

Cần **Python 3.12+** và [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/ItsLewis-DE/behind-the-pipeline.git
cd behind-the-pipeline
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

Giữ cả website và backend đang chạy. Mở một bài viết trên website local, bấm robot Pip và nhập câu hỏi. Có thể kiểm tra API tại **http://127.0.0.1:8001/health** hoặc **http://127.0.0.1:8001/docs**.

Khi triển khai chatbot cho website công khai, cần một backend HTTPS, cấu hình `pip-chat-endpoint` trong thẻ meta của trang và thêm origin `https://itslewis-de.github.io` vào CORS tại `backend/app.py`. GitHub Pages chỉ lưu trữ phần giao diện.

## Cấu trúc dự án

```text
.
├── docs/                 # Bài viết, landing page, hình ảnh, CSS và JavaScript
├── backend/              # API chatbot, ingestion, retrieval và đánh giá RAG
├── overrides/            # Tùy biến template MkDocs Material
├── assets/readme/        # Ảnh chụp website và chatbot cho README
├── scripts/              # Công cụ hỗ trợ phát triển
├── mkdocs.yml            # Điều hướng và cấu hình website
├── pyproject.toml        # Dependency cho website
└── uv.lock               # Phiên bản dependency được khóa
```

## Đóng góp

Bạn có thể [mở issue](https://github.com/ItsLewis-DE/behind-the-pipeline/issues) để báo lỗi, góp ý cách giải thích hoặc đề xuất chủ đề. Với thay đổi nội dung, hãy ghi rõ nguồn tham khảo, kiểm tra hình ảnh và liên kết, sau đó chạy `uv run mkdocs build --strict` trước khi gửi pull request.

---

<p align="center">
  <strong>Behind the Pipeline — từ sử dụng công cụ đến hiểu hệ thống.</strong><br>
  <a href="https://itslewis-de.github.io/behind-the-pipeline/">Khám phá thư viện →</a>
</p>
