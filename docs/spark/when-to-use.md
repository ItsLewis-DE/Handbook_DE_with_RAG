---
title: Khi nào nên dùng Apache Spark?
description: Khung quyết định chọn Spark dựa trên workload, latency, data movement và chi phí vận hành.
---

<header class="airflow-article-hero spark-article-hero">
  <div class="spark-chapter-hero" data-chapter="01" data-reading-minutes="10">
    <div class="airflow-article-hero__eyebrow">
      <a href="../overview/">SPARK HANDBOOK</a>
      <span>CHAPTER 01 / DECISION</span>
    </div>
    <h1>Khi nào nên dùng<br><em>Apache Spark?</em></h1>
    <p class="airflow-article-hero__dek">Chọn distributed compute từ hình dạng workload, SLA và data movement — không từ kích thước dữ liệu đứng riêng lẻ.</p>
    <div class="airflow-article-hero__meta" aria-label="Thông tin chương">
      <span>DECISION FRAMEWORK</span><span>10 PHÚT ĐỌC</span><span>SPARK 4.2.0</span>
    </div>
  </div>
</header>

> **Phạm vi:** Apache Spark 4.2.0. Bài viết đánh giá Spark như một distributed compute engine, không mặc định gắn nó với một storage format hay một cluster manager cụ thể.

“Dữ liệu lớn” không phải tiêu chí đủ để chọn Spark. Một bảng có vài terabyte nhưng đã được partition tốt và chỉ cần một câu SQL đơn giản có thể được warehouse xử lý hiệu quả hơn. Ngược lại, một working set vài trăm gigabyte với nhiều join, nhiều bước tái sử dụng trung gian hoặc thuật toán lặp có thể là workload phù hợp cho Spark.

Quyết định nên bắt đầu từ **hình dạng computation** và **SLA**, rồi mới đến dung lượng dữ liệu.

## 1. Mô hình chi phí thực tế

Thời gian hoàn thành một application có thể hình dung gần đúng:

`T_total = T_queue + T_startup + T_read + T_compute + T_shuffle + T_spill + T_write`

Spark chủ yếu giảm `T_compute` bằng parallelism. Nó không tự động làm `T_queue`, `T_startup`, network shuffle hay storage I/O biến mất. Với job nhỏ, chi phí dựng Driver/Executor, lập lịch Task và serialize dữ liệu có thể lớn hơn phần computation hữu ích.

Ba câu hỏi có giá trị hơn “dữ liệu có lớn không?” là:

1. Công việc có thể chia thành nhiều partition độc lập đủ lớn để bù scheduling overhead không?
2. Có bao nhiêu dữ liệu phải di chuyển giữa các partition so với lượng dữ liệu thực sự được tính toán?
3. SLA ưu tiên throughput theo phút/giờ hay latency tương tác theo mili giây?

## 2. Workload phù hợp

### ETL/ELT theo lô

Spark phù hợp với scan, filter, projection, join, aggregate và ghi lại dataset lớn trên object storage/HDFS. DataFrame/SQL cho optimizer đủ thông tin để column pruning, predicate pushdown và lựa chọn join strategy.

Điều kiện thuận lợi:

- input có thể đọc song song;
- transform đủ nặng hoặc dataset đủ lớn;
- output là file/table phân tích thay vì hàng nghìn point update;
- pipeline chấp nhận startup latency và completion time theo giây/phút.

### Phân tích và feature engineering phân tán

Spark thích hợp khi một feature pipeline phải kết hợp nhiều nguồn, tạo window, aggregation hoặc tái sử dụng intermediate dataset. MLlib hữu ích khi chính thuật toán cần chạy phân tán; không nên chọn Spark chỉ để bọc một thư viện single-node rồi truyền toàn bộ dữ liệu về Driver.

### Xử lý stream theo mô hình bảng

Structured Streaming hợp lý khi team muốn dùng cùng DataFrame/SQL semantics cho batch và stream, chấp nhận micro-batch là chế độ mặc định, và có thể thiết kế checkpoint/state/watermark rõ ràng. Đây không phải lựa chọn tự động cho mọi hệ thống event-by-event có latency cực thấp.

### Reprocessing và backfill

Spark đặc biệt mạnh ở throughput và khả năng chạy lại một khoảng dữ liệu lớn. Một pipeline streaming thường vẫn cần đường backfill; dùng cùng transformation logic trên batch input giúp giảm sai lệch nghiệp vụ nếu code được tổ chức đúng.

## 3. Khi không nên chọn Spark

| Nhu cầu | Vì sao Spark thường không phù hợp | Hướng thay thế thường gặp |
| --- | --- | --- |
| OLTP, point read/write, transaction ngắn | Spark không phải serving database, không cung cấp index/transaction model cho request path | PostgreSQL, MySQL, key-value/document database |
| API cần p99 vài chục mili giây | Startup, scheduling và distributed execution tạo latency không phù hợp | Service chuyên dụng, database/serving store |
| Dataset vừa RAM một máy, transform đơn giản | Chi phí cluster và data movement lớn hơn lợi ích parallelism | DuckDB, Polars, pandas, database SQL |
| BI query đã nằm trong cloud warehouse | Di chuyển dữ liệu ra khỏi warehouse có thể đắt và làm mất optimizer/storage locality | SQL engine của warehouse |
| Event processing độ trễ rất thấp, state phức tạp | Micro-batch có floor latency; operational model khác event-at-a-time | Flink, Kafka Streams hoặc engine tương ứng |
| Hàng triệu cập nhật bản ghi nhỏ tới OLTP sink | Parallel writers dễ gây lock/contention và vượt connection budget | CDC, bulk load, staging + merge |

Các tên công nghệ trong bảng là nhóm lựa chọn, không phải kết luận tuyệt đối. Ví dụ Spark có continuous processing với semantics khác, nhưng cần kiểm chứng feature support và delivery guarantee của phiên bản đang dùng thay vì suy diễn từ micro-batch.

## 4. Ma trận quyết định

Chấm từng tiêu chí từ 0 đến 2. Điểm cao không “chứng minh” phải dùng Spark, nhưng giúp lộ ra giả định cần benchmark.

| Tiêu chí | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Working set | Vừa thoải mái trên một máy | Gần giới hạn một máy | Cần nhiều máy |
| Parallelism tự nhiên | Tuần tự/phụ thuộc mạnh | Chia được một phần | Partition độc lập rõ ràng |
| Transformation | Lookup/CRUD | Một vài scan/aggregate | Nhiều join, window, aggregate |
| SLA | Millisecond | Vài giây | Phút/giờ, ưu tiên throughput |
| Reprocessing | Hiếm, dữ liệu nhỏ | Theo partition | Backfill lớn/thường xuyên |
| Năng lực vận hành | Không có cluster/data ops | Managed platform | Team đã vận hành Spark |

Trước khi quyết định, chạy một representative slice đủ lớn để biểu hiện shuffle, skew và spill. Benchmark một input quá nhỏ chỉ đo startup overhead; benchmark một sample ngẫu nhiên có thể xóa mất key skew vốn quyết định hiệu năng production.

## 5. Các quyết định kiến trúc thường bị bỏ sót

### Compute phải ở gần data

Đọc hàng terabyte qua region hoặc cloud boundary có thể làm mất toàn bộ lợi ích parallelism. Hãy tính network egress, throughput của source và concurrency limit của object store/database trước khi tăng Executor.

### Downstream phải chịu được mức song song

Spark có thể tạo hàng trăm writer đồng thời. JDBC sink, REST API hoặc OLTP database thường không chịu được mức fan-out này. Giới hạn partition trước sink, dùng bulk interface hoặc ghi staging rồi merge là quyết định kiến trúc, không chỉ là tuning.

### File/table layout quyết định chi phí lần chạy sau

Một job chạy nhanh nhưng tạo hàng trăm nghìn file nhỏ đã chuyển chi phí sang metadata listing và query tiếp theo. Chọn partition column, target file size và compaction policy cùng lúc với code transform.

### Distributed execution làm side effect khó hơn

Task có thể retry. Bất kỳ side effect nào bên trong `mapPartitions`/UDF — gửi email, gọi API, ghi ngoài transaction — có thể xảy ra nhiều lần. Thiết kế idempotency key hoặc tách side effect khỏi distributed transform.

## 6. Checklist trước khi phê duyệt

- Xác định rõ SLA về completion time, freshness và chi phí.
- Ước lượng input bytes, output bytes, cardinality và join selectivity.
- Liệt kê wide operations dự kiến: join, group, distinct, repartition, window.
- Kiểm tra key skew trên dữ liệu thật, không chỉ schema.
- Xác nhận source/sink throughput và quota khi có nhiều Task đồng thời.
- Chọn batch hay streaming từ semantics, không từ tên gọi “real time”.
- Định nghĩa retry/idempotency cho output và side effect.
- Lập kế hoạch quan sát: event log, Spark UI, application metrics và cost tags.
- So sánh với phương án đơn giản hơn bằng cùng dataset và SLA.

## 7. Thực chiến: có nên chuyển pipeline doanh thu sang Spark?

Giả sử pipeline hiện tại đọc 1,8 TB Parquet mỗi ngày, join với bảng khách hàng 4 GB, tổng hợp theo quốc gia rồi ghi khoảng 3 GB kết quả. Job chạy trên một máy 95 phút; SLA là 45 phút. Đây chưa phải bằng chứng đủ để chọn Spark. Ta cần tách giới hạn hiện tại thành các phần đo được.

| Câu hỏi | Bằng chứng cần thu | Ý nghĩa quyết định |
| --- | --- | --- |
| Scan có chia song song được không? | Số file, kích thước file, partition pruning và throughput object storage | Spark chỉ giúp nếu nhiều Task có thể đọc độc lập |
| Join có làm phình dữ liệu không? | Cardinality trước/sau join, duplicate key và kích thước build side | Join sai grain có thể làm mọi engine chậm và cho kết quả sai |
| Một máy nghẽn ở đâu? | CPU, memory peak, spill, disk/network throughput | Nếu source đã đạt quota, thêm Executor không tăng scan rate |
| Đích chịu được bao nhiêu writer? | Request quota, commit latency, target file size | Parallelism phải bị chặn bởi downstream capacity |
| Backfill có thường xuyên không? | RPO, số ngày phải chạy lại và cửa sổ vận hành | Đây thường là nơi distributed throughput tạo giá trị lớn nhất |

Chạy ba benchmark trên cùng snapshot: engine hiện tại, Spark với DataFrame/SQL, và phương án warehouse nếu dữ liệu đã nằm trong warehouse. Giữ nguyên logic nghiệp vụ, kiểm tra equality của row count, key uniqueness, tổng doanh thu và null distribution. Với Spark, lưu `explain`, Spark event log, scan bytes, shuffle bytes, p50/p95 Task duration và tổng chi phí compute.

Quyết định **go** khi Spark rút completion time xuống dưới SLA với headroom hợp lý, throughput tăng khi scale trong giới hạn source/sink, và team có thể vận hành event log, retry, data quality cùng chi phí. Quyết định **no-go** khi phần lớn 95 phút nằm ở một API đích tuần tự, một hot key không thể chia, cross-region I/O hoặc thời gian khởi tạo/queue. Trong các trường hợp đó, sửa data layout, business grain hay vị trí compute có giá trị hơn đổi engine.

> **Điểm kiểm soát:** quyết định công nghệ phải kèm một workload fixture, một bảng số đo và tiêu chí dừng. “Dữ liệu sẽ lớn” không phải acceptance criterion.

## Kết luận

Spark đáng dùng khi parallel compute giải quyết đúng bottleneck và phần chi phí phân tán còn lại có thể kiểm soát. Nếu bottleneck nằm ở database sink, network xuyên vùng, một key cực nóng hoặc SLA request/response, thêm Executor không sửa được mô hình hệ thống.

**Đọc tiếp:** [Kiến trúc Spark](architecture.md) · [Partitioning và Shuffle](partition-shuffle.md) · [Đọc Spark UI và tối ưu](performance.md)

## Tài liệu chính thức

- [Apache Spark 4.2.0 Documentation](https://spark.apache.org/docs/4.2.0/)
- [Cluster Mode Overview](https://spark.apache.org/docs/4.2.0/cluster-overview.html)
- [Structured Streaming](https://spark.apache.org/docs/4.2.0/streaming/index.html)
