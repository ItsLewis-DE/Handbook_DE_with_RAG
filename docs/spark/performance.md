---
title: Quan sát và tối ưu Spark Application
description: Phương pháp đọc Spark UI, phân loại bottleneck và kiểm chứng thay đổi hiệu năng bằng metrics.
---

<header class="airflow-article-hero spark-article-hero">
  <div class="spark-chapter-hero" data-chapter="09" data-reading-minutes="11">
    <div class="airflow-article-hero__eyebrow">
      <a href="../overview/">SPARK HANDBOOK</a>
      <span>CHAPTER 09 / PERFORMANCE</span>
    </div>
    <h1>Quan sát và tối ưu<br><em>Spark Application</em></h1>
    <p class="airflow-article-hero__dek">Đi từ critical path và Task distribution đến thay đổi nhỏ có giả thuyết, số đo và điều kiện rollback.</p>
    <div class="airflow-article-hero__meta" aria-label="Thông tin chương">
      <span>SPARK UI</span><span>11 PHÚT ĐỌC</span><span>SPARK 4.2.0</span>
    </div>
  </div>
</header>

> **Phạm vi:** Apache Spark 4.2.0. UI field thay đổi theo workload/version; nguyên tắc là nối query operator → Stage → Task distribution → Executor/failure event.

Tuning không phải danh sách “best config”. Một thay đổi hợp lý chỉ tồn tại khi có bottleneck, giả thuyết, metric trước/sau và kiểm tra tính đúng của output.

## 1. Gói bằng chứng tối thiểu

Mỗi run cần lưu:

- application ID, Spark/runtime/connector version;
- code/artifact commit và effective SparkConf đã redaction;
- input snapshot hoặc partition range, bytes và row count;
- logical/physical/adaptive final plan;
- event log, Driver/Executor log và cluster events;
- output row count/checksum/data-quality checks;
- wall time, resource-hours và chi phí nếu có.

So sánh hai run khác input hoặc cluster load mà không ghi nhận khác biệt dễ dẫn đến kết luận giả.

## 2. Bản đồ Spark UI

### Jobs

Cho biết action/job nào chiếm wall time, Job có fail/retry hay nằm chờ Stage. Bắt đầu ở đây để khoanh vùng thay vì đọc log tuyến tính.

### Stages

Đây là trang quan trọng nhất cho distribution. Đọc:

- task time distribution, không chỉ average;
- input/output records và bytes;
- shuffle read/write;
- memory/disk spill;
- GC time, scheduler delay, fetch wait;
- số failed/retried/speculative attempts.

### SQL/DataFrame

Nối query tới physical operators và Stage IDs. Tìm scan, `Exchange`, sort, aggregate, join strategy, Python UDF và adaptive initial/final plan. Operator metrics cho biết số row/bytes qua từng node.

### Executors

So sánh active/dead Executor, task time, failed tasks, GC, input/shuffle, storage memory và log. Một Executor khác biệt rõ có thể là noisy/bad node; mọi Executor cùng pattern thường là workload/plan.

### Storage

Xác nhận dataset nào thực sự cache, bao nhiêu partition materialized, footprint memory/disk và replication. Gọi `cache()` trong code không bảo đảm cache đã được sử dụng.

### Environment

Kiểm tra effective properties, classpath và runtime. UI/config có thể chứa dữ liệu nhạy cảm; cần ACL và redaction.

## 3. Phân loại bottleneck

| Dấu hiệu | Khả năng cao | Bằng chứng bổ sung |
| --- | --- | --- |
| Max Task lâu hơn median rất nhiều, bytes cũng lớn | Data skew | Key distribution, skewed partition, final AQE plan |
| Task bytes gần nhau nhưng một node chậm | Straggler/node/GC | Executor host, GC, cluster event, retry/speculation |
| Shuffle read/write lớn | Join/aggregate/repartition | `Exchange`, join strategy, filter selectivity |
| Spill lớn trên mọi Task | Partition working set/memory | Peak Task size, operator, executor concurrency |
| Nhiều Task cực ngắn | Over-partition/small files | Scheduler delay, file count, task duration |
| CPU thấp, fetch/read wait cao | I/O/network/storage | Source metrics, object-store latency, shuffle fetch wait |
| GC chiếm tỷ lệ cao | Object pressure/heap/concurrency | Heap dump/GC log, serialization path, UDF |
| Driver OOM hoặc lag | Collect/metadata/plan quá lớn | Driver log, result size, task/file count |
| Executor pending | Scheduler/quota/topology | YARN/K8s events, requests, affinity, quota |

Correlation không tự động là causation. Ví dụ spill và chậm cùng xuất hiện có thể đều do skew; tăng memory chỉ giảm spill mà không sửa tail partition.

## 4. Quy trình tối ưu có kiểm soát

1. **Định nghĩa mục tiêu:** wall time, throughput, freshness, cost hay stability.
2. **Chọn run đại diện:** giữ input và external load đủ ổn định.
3. **Tìm critical path:** Job/Stage/operator chiếm thời gian.
4. **Phân loại bottleneck:** CPU, I/O, shuffle, skew, memory, scheduling hay downstream.
5. **Đưa một giả thuyết:** ví dụ “dimension đủ nhỏ để broadcast, sẽ loại 600 GB shuffle”.
6. **Thay một nhóm biến:** tránh đổi code, partition và cluster size cùng lúc.
7. **Đo lại distribution:** median và p95/max, không chỉ tổng time.
8. **Kiểm tra output:** row count, key uniqueness, null/domain và checksum/sample reconciliation.
9. **Ghi quyết định/rollback:** config theo workload chứ không biến thành global folklore.

## 5. Ba ca điển hình

### Ca A: Join còn một Task chạy 40 phút

Quan sát: median Task 50 giây, max 40 phút; max shuffle read gấp 80 lần median; key `UNKNOWN` chiếm phần lớn.

Không hiệu quả: tăng toàn cluster hoặc bật speculation.

Hướng xử lý: xác định semantics của null/unknown; filter nếu invalid, tách hot key, pre-aggregate, salt có kiểm chứng, hoặc dùng AQE skew join nếu plan/threshold phù hợp.

### Ca B: Scan 500.000 file nhỏ

Quan sát: planning/listing lâu, hàng trăm nghìn Task ngắn, scheduler overhead cao, bytes/task rất nhỏ.

Không hiệu quả: tăng shuffle partitions.

Hướng xử lý: compaction, tối ưu table metadata/layout, kiểm soát output file size ở producer; tune file partition discovery chỉ sau khi xử lý nguyên nhân.

### Ca C: Driver OOM ở cuối Job

Quan sát: Executor hoàn thành bình thường; Driver fail tại `toPandas()`/`collect()`.

Không hiệu quả: tăng executor memory.

Hướng xử lý: aggregate/limit có kiểm chứng, ghi distributed output, lấy sample có kiểm soát, hoặc tăng Driver chỉ khi result thực sự bounded và requirement hợp lệ.

## 6. Configuration theo bằng chứng

| Cấu hình/đòn bẩy | Chỉ cân nhắc khi | Rủi ro |
| --- | --- | --- |
| `spark.sql.shuffle.partitions` | Task sau shuffle quá lớn/nhỏ | Global value không hợp mọi query; AQE thay đổi kết quả |
| Auto broadcast threshold/hint | Build side bounded, đủ memory | OOM và regression khi dimension tăng |
| Executor memory/overhead | Xác định đúng vùng cạn | Che skew/object issue, tăng cost/GC |
| Executor cores | Đã hiểu per-Task memory/CPU | Nhiều concurrent Task cạnh tranh heap |
| Dynamic allocation bounds | Workload có phase/backlog thay đổi | Startup lag, cache churn, downstream burst |
| Cache/persist | Reuse thực sự và recompute đắt | Eviction/thrash, giữ memory vô ích |

## 7. Benchmark đúng

- Warm cache và cold cache là hai scenario khác nhau.
- Chạy nhiều lần để phân biệt variance của platform.
- Dùng production-like skew và file layout.
- Tách startup/queue time khỏi executor compute time.
- Đo cost per successful output, không chỉ runtime.
- Với streaming, đo input rate, processed rate, batch duration, state size và end-to-end lag.

## 8. Điều kiện kết thúc tuning

Tối ưu nên dừng khi đạt SLA/cost guardrail với margin, kết quả đúng, không làm downstream xấu đi và complexity bổ sung có owner/observability. Giảm thêm 5% runtime không đáng nếu salting/custom UDF làm pipeline khó kiểm chứng và dễ sai.

## 9. Thực chiến: lập hồ sơ điều tra cho một Stage chậm

Một tuning ticket tốt không bắt đầu bằng “tăng executor memory”. Nó bắt đầu bằng một evidence packet đủ để người khác tái lập kết luận:

- application ID, Spark version, artifact/config version và cluster shape;
- input snapshot hoặc partition range, row/byte count và file layout;
- initial/final physical plan cùng Stage ID trên critical path;
- Task metrics dạng phân phối: min, p50, p95, max — không chỉ average;
- output invariants/checksum và cost của lần chạy;
- một hypothesis, một thay đổi, một rollback condition.

Giả sử Stage 23 có p50 là 52 giây, p95 là 61 giây nhưng max là 1.460 giây; Task cuối đọc shuffle gấp 34 lần median. Đây là tail problem, không phải thiếu tổng CPU. Tăng Executor có thể làm 399 Task vốn đã nhanh chạy sớm hơn, nhưng application vẫn đợi straggler.

| Vòng thử | Thay đổi | Kỳ vọng trước khi chạy | Cổng chấp nhận |
| --- | --- | --- | --- |
| Baseline | Không | Khóa variance và output | Ba lần chạy trong dải ổn định |
| A | Pre-aggregate trước exchange | Giảm shuffle bytes và hot partition | Output bằng baseline; max/median giảm |
| B | AQE/skew strategy phù hợp | Split partition lệch ở final plan | Không tăng spill/cost ngoài guardrail |
| C | Sizing lại sau khi sửa plan | Giảm waves, giữ per-task memory an toàn | SLA đạt với ít nhất 20% headroom |

Mỗi vòng chỉ thay một nhóm biến để giữ quan hệ nhân quả. Lưu screenshot là hữu ích cho trao đổi, nhưng event log và dữ liệu metrics mới có thể so sánh tự động. Nếu run B nhanh hơn nhưng input cache ấm trong khi baseline cache lạnh, comparison không hợp lệ.

Sau tối ưu, thêm regression guardrail: cảnh báo khi max/median Task duration, shuffle bytes/row, small-file count hoặc end-to-end cost vượt ngưỡng. Performance không phải một lần “tuning xong”; data distribution, statistics và connector behavior thay đổi theo thời gian.

## Kết luận

Spark UI là bản đồ thực thi, không phải dashboard trang trí. Cách làm đáng tin cậy là đi từ critical path đến Task distribution, nối lại physical plan và chỉ thay đổi khi metric dự đoán được kết quả.

**Đọc tiếp:** [Query planning](query-planning.md) · [Partitioning và Shuffle](partition-shuffle.md) · [Memory và Fault Tolerance](memory-fault-tolerance.md)

## Tài liệu chính thức

- [Spark Web UI](https://spark.apache.org/docs/4.2.0/web-ui.html)
- [Monitoring and Instrumentation](https://spark.apache.org/docs/4.2.0/monitoring.html)
- [SQL Performance Tuning](https://spark.apache.org/docs/4.2.0/sql-performance-tuning.html)
