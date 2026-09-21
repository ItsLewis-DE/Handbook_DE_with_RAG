# Behind the Pipeline

> Cẩm nang kiến thức cốt lõi về những công cụ Data Engineer sử dụng hằng ngày.

Behind the Pipeline là một dự án tài liệu mở, tập trung giải thích cách các công cụ trong hệ sinh thái Data Engineering hoạt động từ bên trong. Nội dung không chỉ hướng dẫn *cách sử dụng*, mà còn trả lời những câu hỏi quan trọng hơn: công cụ đó giải quyết vấn đề gì, vì sao nó tồn tại, kiến trúc của nó được thiết kế như thế nào và khi nào chúng ta nên sử dụng nó.

Tài liệu được viết bằng tiếng Việt và xuất bản dưới dạng website với MkDocs Material.

## Mục tiêu

Behind the Pipeline hướng đến việc giúp Data Engineer:

- nắm vững các khái niệm nền tảng thay vì chỉ ghi nhớ câu lệnh;
- hiểu kiến trúc và cơ chế vận hành bên trong mỗi công cụ;
- nhận biết giới hạn, trade-off và trường hợp sử dụng phù hợp;
- kết nối kiến thức giữa orchestration, processing, storage, streaming và infrastructure;
- có một nguồn tài liệu ngắn gọn để tra cứu trong công việc hằng ngày.

Mỗi chủ đề sẽ cố gắng đi theo một mạch kiến thức thống nhất:

```text
Bài toán thực tế
    → Khái niệm cốt lõi
    → Kiến trúc bên trong
    → Cơ chế vận hành
    → Khả năng mở rộng và giới hạn
    → Kinh nghiệm sử dụng thực tế
```

## Nội dung hiện có

### Data Architecture

- Shared-disk và shared-nothing khác nhau ở quyền sở hữu memory/storage như thế nào?
- Distribution key, data locality, shuffle và skew tác động tới ETL/ELT ra sao?
- Khi thêm hoặc mất node, coordination, replication và rebalance diễn ra ở đâu?
- Oracle RAC, Db2 pureScale, Teradata, Citus, Greenplum và Snowflake nằm ở vị trí nào trong taxonomy?

Đọc tài liệu tại [Shared-disk và shared-nothing dưới góc nhìn Data Engineer](docs/architecture/shared-disk-vs-shared-nothing.md).

### Apache Airflow

- Vì sao cần Airflow thay vì chỉ sử dụng Bash và Cron?
- DAG, Task, Task Instance, Schedule và Dependency.
- Scheduler và scheduling loop.
- DAG File Processor.
- HA Scheduler và Critical Section.
- Pool, Executor và các nút thắt khi mở rộng.

Đọc tài liệu tại [Kiến trúc Apache Airflow](docs/airflow/architecture.md).

## Chạy tài liệu trên máy cá nhân

### Website

Cần **Python 3.12+** và [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/ItsLewis-DE/pipeline-rag.git
cd pipeline-rag
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

Bạn có thể [mở issue](https://github.com/ItsLewis-DE/pipeline-rag/issues) để báo lỗi, góp ý cách giải thích hoặc đề xuất chủ đề. Với thay đổi nội dung, hãy ghi rõ nguồn tham khảo, kiểm tra hình ảnh và liên kết, sau đó chạy `uv run mkdocs build --strict` trước khi gửi pull request.

---

<p align="center">
  <strong>Pipeline RAG — hỏi từ tài liệu, trả lời có nguồn.</strong><br>
  <a href="https://itslewis-de.github.io/pipeline-rag/">Khám phá thư viện →</a>
</p>
