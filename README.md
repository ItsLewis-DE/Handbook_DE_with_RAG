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

### Yêu cầu

- Python 3.12 trở lên;
- [uv](https://docs.astral.sh/uv/).

### Cài đặt dependency

```bash
uv sync
```

### Khởi chạy development server

```bash
uv run mkdocs serve
```

Sau đó truy cập `http://127.0.0.1:8000` để xem handbook.

### Kiểm tra bản build

```bash
uv run mkdocs build --strict
```

Website sau khi build được tạo trong thư mục `site/`.

## Cấu trúc dự án

```text
.
├── docs/
│   ├── index.md                 # Landing page
│   ├── architecture/
│   │   └── shared-disk-vs-shared-nothing.md
│   ├── airflow/
│   │   └── architecture.md      # Kiến trúc Apache Airflow
│   └── stylesheets/
│       └── landing.css          # Giao diện landing page
├── mkdocs.yml                   # Cấu hình website
├── pyproject.toml               # Dependency của dự án
└── uv.lock                      # Phiên bản dependency được khóa
```
---

Behind the Pipeline được xây dựng với mục tiêu biến những kiến thức rời rạc trong công việc hằng ngày thành một hệ thống kiến thức rõ ràng, có thể tra cứu và tiếp tục mở rộng.
