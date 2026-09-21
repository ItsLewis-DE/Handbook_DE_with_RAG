---
title: Memory và Fault Tolerance trong Spark
description: Heap, overhead, unified memory, cache, spill, lineage, checkpoint và cơ chế phục hồi của Spark.
---

<header class="airflow-article-hero spark-article-hero">
  <div class="spark-chapter-hero" data-chapter="07" data-reading-minutes="11">
    <div class="airflow-article-hero__eyebrow">
      <a href="../overview/">SPARK HANDBOOK</a>
      <span>CHAPTER 07 / RESILIENCE</span>
    </div>
    <h1>Memory và<br><em>Fault Tolerance</em></h1>
    <p class="airflow-article-hero__dek">Nối per-task working set, unified memory, spill, lineage và retry thành một mô hình chẩn đoán thống nhất.</p>
    <div class="airflow-article-hero__meta" aria-label="Thông tin chương">
      <span>RESILIENCE</span><span>11 PHÚT ĐỌC</span><span>SPARK 4.2.0</span>
    </div>
  </div>
</header>

> **Phạm vi:** Apache Spark 4.2.0. Con số mặc định phụ thuộc version/deployment; luôn đối chiếu configuration của application đang chạy.

“Executor có 16 GB” không có nghĩa một Task có 16 GB heap, và cũng không có nghĩa Spark có thể giữ 16 GB dữ liệu serialized. Memory phải phục vụ nhiều vùng đồng thời, còn container/pod limit bao gồm cả phần ngoài JVM heap.

## 1. Bản đồ memory của Executor

```text
Container / pod memory limit
├── JVM heap
│   ├── Spark managed memory
│   │   ├── execution: join, aggregate, sort, shuffle
│   │   └── storage: cache, broadcast blocks
│   ├── user memory: object/user code/metadata
│   └── reserved region
└── non-heap / overhead
    ├── JVM metaspace, thread stacks, direct buffers
    ├── native libraries
    └── Python worker processes (đặc biệt quan trọng với PySpark)
```

Hai failure khác nhau:

- `java.lang.OutOfMemoryError`: JVM heap hoặc một vùng JVM cụ thể cạn.
- container/pod bị kill vì vượt memory limit: tổng RSS gồm heap + overhead/native/Python vượt giới hạn, dù heap chưa báo OOM.

Vì vậy tăng `spark.executor.memory` mà không tăng memory overhead có thể làm container limit vẫn thiếu, thậm chí giảm headroom cho Python/native workload.

## 2. Unified memory

Spark dùng một vùng thống nhất cho execution và storage. `spark.memory.fraction` xác định phần heap sau reserved region dành cho managed memory; `spark.memory.storageFraction` đặt vùng storage có mức bảo vệ tương đối bên trong đó.

Execution có thể evict cached blocks để lấy chỗ trong giới hạn memory manager; storage không thể luôn đẩy execution ra. Ý nghĩa vận hành:

- cache không phải vùng RAM cố định;
- một join/sort lớn có thể làm cache bị evict và phải recompute;
- cache hit thấp có thể do cạnh tranh execution, không chỉ do dataset quá lớn;
- thay các fraction là tuning nâng cao, không phải bước đầu tiên.

## 3. Cache và persist

`cache()` là shorthand cho storage level mặc định theo API; `persist(level)` cho phép chọn memory/disk/serialization/replication. Cache là lazy: block chỉ được materialize khi action đọc partition đó.

Cache có lợi khi:

`cost_to_recompute × reuse_count > cost_to_materialize + memory_pressure + eviction_cost`

Ứng viên tốt:

- dataset sau filter/join đắt được dùng nhiều action;
- iterative algorithm đọc cùng working set;
- interactive analysis lặp trên cùng intermediate.

Ứng viên kém:

- dataset chỉ dùng một lần;
- dữ liệu lớn hơn nhiều so với storage memory và liên tục thrash;
- cache trước filter/projection khiến footprint quá lớn;
- source/table format đã có cache hiệu quả ở tầng khác.

Luôn `unpersist()` khi vòng tái sử dụng kết thúc trong application dài. Theo dõi Storage tab: fraction cached, size in memory/disk và số partition đã materialize.

## 4. Spill không đồng nghĩa failure

Sort, hash aggregate và shuffle có thể spill khi working set không vừa memory. Spill đổi rủi ro OOM lấy disk I/O/CPU merge; một lượng spill có thể hoàn toàn chấp nhận được.

Đáng lo khi:

- spill bytes rất lớn so với input;
- local disk gần đầy hoặc throughput thấp;
- một vài Task spill cực lớn do skew;
- GC time tăng cùng object-heavy representation;
- nhiều Task đồng thời cạnh tranh memory trên Executor.

Giảm partition size, dùng built-in SQL operator, pre-aggregate, sửa skew hoặc giảm concurrency per Executor thường có ý nghĩa hơn tăng heap mù quáng.

## 5. Driver memory

Driver giữ plan, scheduler metadata và result/metadata từ Task. Các anti-pattern gây Driver OOM:

- `collect()`, `toPandas()`, `collect_list` trên cardinality lớn;
- millions of partitions/tasks/files;
- query plan cực lớn từ code-generated unions/projections;
- broadcast được tạo/thu thập ở Driver quá lớn;
- giữ reference tới nhiều DataFrame/cache/session object không cần thiết.

`spark.driver.maxResultSize` là guardrail cho serialized result của action, không bảo vệ mọi loại Driver memory. Cách sửa chủ yếu là giữ computation phân tán và ghi result ra durable storage.

## 6. Lineage và recomputation

RDD/DataFrame plan mô tả cách tạo partition. Khi cached partition mất, Spark có thể recompute từ ancestor còn tồn tại. Với narrow lineage, chỉ một nhánh partition có thể cần chạy lại; với shuffle dependency, mất map output có thể buộc chạy lại upstream map partition/stage liên quan.

Lineage dài gây:

- plan/scheduler overhead;
- recomputation đắt sau failure;
- debugging khó;
- stack/serialization pressure trong một số pattern lặp.

## 7. Checkpoint và local checkpoint

Checkpoint materialize dữ liệu tới reliable storage và cắt lineage. Nó phù hợp khi lineage rất dài, iterative/stateful computation cần điểm phục hồi ổn định hoặc recovery từ đầu quá đắt.

`localCheckpoint` dùng Executor local storage và đánh đổi fault tolerance để nhanh hơn; mất block có thể làm dữ liệu không phục hồi được từ reliable checkpoint. Không dùng hai khái niệm như nhau chỉ vì cùng “cắt lineage”.

Checkpoint có chi phí I/O và cần action để materialize. Chọn storage location có durability, throughput, quyền truy cập và lifecycle policy phù hợp.

## 8. Ma trận phục hồi

| Sự cố | Spark có thể làm gì | Phần ứng dụng phải bảo đảm |
| --- | --- | --- |
| Task exception tạm thời | Retry Task attempt | Function deterministic, lỗi thật sự transient |
| Executor mất | Schedule lại Task; recompute cache/shuffle cần thiết | Cluster còn capacity, source vẫn đọc được |
| Shuffle fetch failure | Retry fetch hoặc rerun upstream map output | Local disk/network ổn định, không che lỗi kéo dài bằng retry |
| Driver mất | Application thường mất control state | Cluster-mode recovery/supervision; output idempotent |
| Output commit không rõ | Retry/abort tùy connector | Transaction/commit protocol và deduplication |
| Streaming restart | Khôi phục offset/state từ checkpoint | Checkpoint durable, code/schema compatible |

Fault tolerance của Spark không tạo exactly-once cho arbitrary side effect. Nếu Task gọi HTTP endpoint rồi timeout sau khi endpoint đã commit, retry có thể duplicate.

## 9. Quy trình chẩn đoán OOM

1. Xác định Driver, Executor JVM, Python worker hay container bị kill.
2. Lấy exit reason/stack trace và peak memory theo Executor, không chỉ tổng cluster.
3. Nối failure tới Stage/physical operator.
4. So partition max với median để phát hiện skew.
5. Kiểm tra cache footprint, broadcast size, spill, GC và số Task đồng thời.
6. Sửa distribution/plan/object representation trước.
7. Chỉ sau đó sizing lại heap, overhead, cores per Executor và partition count.

## 10. Thực chiến: container OOM dù heap còn trống

Một PySpark Executor được cấu hình heap 8 GiB và memory overhead 2 GiB. Container bị kill ở gần 10 GiB RSS, nhưng GC log cho thấy JVM heap chỉ dùng 5 GiB. Kết luận “Spark báo sai memory” là không đúng: container limit bao quanh nhiều vùng hơn heap, gồm Python worker, direct/native memory, thread stack và overhead khác.

Điều tra theo bản đồ process thay vì chỉ nhìn Storage tab:

1. Xác nhận termination reason từ cluster manager và container peak RSS.
2. Tách JVM heap/non-heap, Python worker RSS, off-heap/direct memory và số Task chạy đồng thời.
3. Nối thời điểm peak với Stage, operator, Arrow/Pandas UDF batch, broadcast và partition lớn nhất.
4. So Executor bình thường với Executor bị kill; nếu chỉ partition cực lớn gây peak, đây là distribution problem trước khi là sizing problem.
5. Giảm một biến mỗi lần: batch size, cores/concurrency, partition working set hoặc cached/broadcast footprint.

| Dấu hiệu | Giả thuyết mạnh hơn | Hành động đầu tiên |
| --- | --- | --- |
| Heap gần đầy, full GC dày | JVM object/execution pressure | Giảm working set, object overhead hoặc concurrency |
| Heap thấp, container RSS cao | Python/native/off-heap/overhead | Đo process con và direct memory; chỉnh batch/overhead có căn cứ |
| Một Executor duy nhất lặp lại OOM | Skew hoặc bad partition | So max/median input và key distribution |
| Mọi Executor OOM sau broadcast | Build side lớn hơn estimate/budget | Bỏ hint, sửa statistics/strategy |
| Driver OOM sau Task hoàn tất | Result/metadata về Driver | Loại `collect`, chia output, giảm Task/plan metadata |

Sau khi sửa, chạy lại cùng input và lưu peak RSS theo Executor, GC time, spill, Task p95 và output equality. Tăng overhead có thể là thay đổi đúng nếu workload hợp lệ thực sự cần vùng non-heap; nhưng nếu peak tăng tuyến tính theo partition hoặc batch, tăng limit chỉ dời ngưỡng thất bại.

Fault tolerance cũng ảnh hưởng memory incident: Executor chết làm cache/shuffle block mất, dẫn đến recomputation và thêm tải. Nếu retry lặp trên cùng partition, dừng việc “cứu” bằng failure count cao hơn; tìm record, key hoặc operator tạo working set không bounded.

## Kết luận

Memory management và fault tolerance liên kết chặt: mất cache/shuffle làm recomputation; lineage dài làm recovery đắt; memory pressure gây Executor loss rồi tạo thêm retry. Tối ưu đúng bắt đầu từ failure domain và per-Task working set, không từ tổng RAM của cluster.

**Đọc tiếp:** [Partitioning và Shuffle](partition-shuffle.md) · [Deployment](deployment.md) · [Performance](performance.md)

## Tài liệu chính thức

- [Spark Tuning Guide](https://spark.apache.org/docs/4.2.0/tuning.html)
- [Spark Configuration](https://spark.apache.org/docs/4.2.0/configuration.html)
- [RDD Persistence](https://spark.apache.org/docs/4.2.0/rdd-programming-guide.html#rdd-persistence)
