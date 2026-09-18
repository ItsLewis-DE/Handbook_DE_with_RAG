---
title: Triển khai Apache Spark
description: Cluster manager, deploy mode, resource sizing, dynamic allocation, security và checklist production cho Spark.
---

# Triển khai Apache Spark

> **Phạm vi:** Apache Spark 4.2.0. Managed services có thể đổi tên hoặc ẩn một số cấu hình; nguyên lý Driver/Executor và resource boundary vẫn cần được kiểm chứng trên nền tảng cụ thể.

Deployment là bài toán đặt các process Spark vào một resource scheduler, bảo đảm network/storage/security, rồi sizing sao cho application có parallelism nhưng không phá quota của cluster hay downstream.

## 1. Cluster manager và deploy mode là hai trục riêng

| Cluster manager | Đơn vị cấp tài nguyên | Điểm mạnh | Điểm cần vận hành |
| --- | --- | --- | --- |
| Standalone | Worker/Executor process | Đơn giản, đi kèm Spark | HA master, isolation, autoscaling, ecosystem integration |
| YARN | ApplicationMaster/container | Tích hợp Hadoop, queue/capacity | YARN resource model, local files/log aggregation, queue policy |
| Kubernetes | Driver/Executor pod | Isolation/image/declarative scheduling | RBAC, service account, image, volume, pod scheduling/network |

Deploy mode:

- **client:** Driver chạy tại process submit. Hợp với shell/notebook; submit host phải sống, có network hai chiều phù hợp và gần cluster.
- **cluster:** Driver chạy trong cluster. Thường phù hợp scheduled production job vì vòng đời tách khỏi máy submit.

Một notebook ở laptop chạy client mode qua internet là topology dễ mất Driver–Executor connectivity và khó bảo vệ credential; không phải chỉ là lựa chọn UX.

## 2. Sizing từ Task working set

Không bắt đầu bằng “mỗi Executor 32 GB”. Bắt đầu từ:

1. bytes/records của partition lớn ở operator nặng nhất;
2. expansion khi decompress/deserialize/hash/sort;
3. số Task đồng thời trên mỗi Executor;
4. cache/broadcast/Python/native overhead;
5. target waves và SLA.

Xấp xỉ:

`executor_peak ≈ concurrent_tasks × peak_memory_per_task + cache + broadcast + runtime_overhead`

Đây không phải công thức Spark bảo đảm; nó buộc thiết kế tính concurrency. Tăng cores per Executor làm nhiều Task chạy chung heap hơn. Executor quá lớn có blast radius cao và GC pause dài; Executor quá nhỏ làm overhead process/broadcast/shuffle connection tăng.

## 3. CPU và parallelism

Tổng core hữu ích bị giới hạn bởi partition count của Stage. Một cluster 500 cores không tăng tốc Stage chỉ có 40 partitions. Ngược lại, 50.000 partitions trên 100 cores tạo nhiều wave và scheduling overhead.

CPU-heavy UDF, compression hay serialization có thể cần ít cores/Executor để giảm contention. I/O-bound workload có thể chịu concurrency khác. Đo executor CPU time, GC, I/O wait và Task duration distribution trước khi đổi.

## 4. Static và dynamic allocation

Static allocation dễ dự đoán: số Executor cố định suốt application. Nó phù hợp workload ổn định hoặc khi cache locality quan trọng.

Dynamic allocation tăng/giảm Executor dựa trên backlog/idle timeout trong giới hạn min–initial–max. Điều kiện hỗ trợ shuffle preservation tùy mode/version, chẳng hạn external shuffle service hoặc shuffle tracking/cơ chế tương ứng.

Trade-off:

- scale-up có startup latency; short job có thể kết thúc trước khi nhận đủ Executor;
- scale-down có thể evict cache và tác động shuffle/state theo cơ chế đang dùng;
- max quá cao có thể gây burst vào object store/JDBC sink;
- min quá thấp làm streaming query không giữ được throughput ổn định;
- scheduler quota vẫn là trần dù Spark yêu cầu thêm.

## 5. Kubernetes-specific concerns

- Driver service/DNS phải cho Executor kết nối lại.
- Container image phải chứa đúng Spark, JVM, Python và native dependencies.
- ServiceAccount/RBAC và cloud identity chỉ có quyền cần thiết.
- Requests/limits phản ánh executor memory + overhead, không chỉ heap.
- Local disk/ephemeral storage đủ cho shuffle/spill; node eviction policy được theo dõi.
- Pod template, node selector, affinity/toleration không làm Executor pending hàng loạt.
- Không đưa secret trực tiếp vào image, command line hoặc loggable SparkConf.

## 6. YARN-specific concerns

- Queue capacity/preemption quyết định thời gian chờ và resource thực nhận.
- Executor/Driver memory overhead phải nằm trong container allocation.
- Distributed cache/classpath tránh dependency mismatch.
- Log aggregation và application attempt cần được giữ để post-mortem.
- Keytab/token/credential renewal phải phù hợp job dài.

## 7. Dependency và artifact

Production artifact cần reproducible:

- khóa version Spark-compatible connector và transitive dependency;
- tránh đóng gói trùng Spark/Hadoop classes khi cluster đã cung cấp, tùy deployment model;
- kiểm tra Scala binary version với JAR;
- với Python, đồng bộ interpreter/package trên Driver và Executor;
- smoke test class loading, native library và cloud filesystem connector trên đúng image/runtime.

“Chạy local” không chứng minh cluster classpath đúng. `ClassNotFoundException`, `NoSuchMethodError` và Python version mismatch là ba failure class khác nhau.

## 8. Security và isolation

Production baseline:

- dùng workload identity/service account thay static access key;
- mã hóa traffic và storage theo threat model/nền tảng;
- giới hạn quyền input/output/checkpoint/event log;
- bật authentication/ACL cho UI và History Server;
- cấu hình redaction cho secret trong config/environment;
- tách queue/namespace và resource quota giữa tenant;
- vá Spark/JVM/connector theo quy trình dependency management;
- log audit ai submit artifact/config nào.

## 9. Submission template có chủ đích

```bash
spark-submit \
  --master k8s://https://cluster-endpoint \
  --deploy-mode cluster \
  --conf spark.executor.instances=8 \
  --conf spark.executor.cores=4 \
  --conf spark.executor.memory=8g \
  --conf spark.executor.memoryOverhead=2g \
  --conf spark.eventLog.enabled=true \
  local:///opt/spark/jobs/orders.jar
```

Đây chỉ là minh họa cấu trúc, không phải cấu hình khuyến nghị. Endpoint, image, authentication, storage và sizing phải lấy từ môi trường. Không đặt secret literal trong lệnh vì command có thể xuất hiện trong shell history/UI/log.

## 10. Checklist production

- Chọn cluster/client mode theo failure boundary của Driver.
- Xác nhận network Driver–Executor và Executor–storage/shuffle.
- Sizing heap, overhead và local disk từ metrics đại diện.
- Đặt min/max allocation cùng quota và downstream capacity.
- Bật event log, History Server/observability và log retention.
- Chứng minh output idempotent khi application/task retry.
- Version artifact/image/config và lưu cùng run metadata.
- Thử node/Executor loss và restart, không chỉ happy path.
- Đặt budget/cost attribution và cảnh báo application runaway.

## Kết luận

Deployment tốt không chỉ làm application “submit được”; nó làm resource, identity, network, artifact và failure behavior có thể dự đoán. Sizing phải nối từ per-Task working set tới concurrency, thay vì sao chép một bộ cấu hình chung.

**Đọc tiếp:** [Kiến trúc](architecture.md) · [Memory và Fault Tolerance](memory-fault-tolerance.md) · [Performance](performance.md)

## Tài liệu chính thức

- [Submitting Applications](https://spark.apache.org/docs/4.2.0/submitting-applications.html)
- [Running on Kubernetes](https://spark.apache.org/docs/4.2.0/running-on-kubernetes.html)
- [Running on YARN](https://spark.apache.org/docs/4.2.0/running-on-yarn.html)
- [Job Scheduling](https://spark.apache.org/docs/4.2.0/job-scheduling.html)
