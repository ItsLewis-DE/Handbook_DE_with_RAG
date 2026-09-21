---
title: RDD, DataFrame và Dataset trong Spark
description: Semantics, optimizer visibility, partitioning và chi phí qua ranh giới JVM–Python của các abstraction dữ liệu Spark.
---

<header class="airflow-article-hero spark-article-hero">
  <div class="spark-chapter-hero" data-chapter="03" data-reading-minutes="11">
    <div class="airflow-article-hero__eyebrow">
      <a href="../overview/">SPARK HANDBOOK</a>
      <span>CHAPTER 03 / ABSTRACTIONS</span>
    </div>
    <h1>RDD, DataFrame<br><em>và Dataset</em></h1>
    <p class="airflow-article-hero__dek">Mỗi abstraction là một hợp đồng thông tin khác nhau giữa code của bạn và execution engine.</p>
    <div class="airflow-article-hero__meta" aria-label="Thông tin chương">
      <span>DATA MODEL</span><span>11 PHÚT ĐỌC</span><span>SPARK 4.2.0</span>
    </div>
  </div>
</header>

> **Phạm vi:** Apache Spark 4.2.0. Mục tiêu không phải so API theo cú pháp, mà phân tích lượng thông tin mỗi abstraction cung cấp cho execution engine.

RDD, DataFrame và Dataset đều biểu diễn dữ liệu phân tán, bất biến theo nghĩa transformation tạo collection mới. Khác biệt quan trọng là Spark **biết gì** về dữ liệu và computation trước khi chạy.

## 1. RDD: partition, dependency và function

RDD là collection gồm các partition. Mỗi RDD giữ đủ thông tin để tính partition của nó: danh sách parent dependency, hàm compute và partitioner nếu có. Transformation là lazy; action kích hoạt computation.

```python
lines = sc.textFile("s3://lake/events/")
errors = (
    lines
    .filter(lambda line: '\"level\":\"ERROR\"' in line)
    .map(lambda line: (extract_service(line), 1))
    .reduceByKey(lambda left, right: left + right)
)
print(errors.take(20))
```

Spark thấy dependency graph, nhưng Python lambda là logic gần như hộp đen với SQL optimizer. Engine không thể tự suy ra field nào cần đọc từ JSON, đẩy biểu thức vào Parquet scan hay đổi thứ tự join dựa trên biểu thức tùy ý.

RDD hữu ích khi:

- cần custom partition-level algorithm không biểu đạt tốt bằng structured operator;
- xử lý unstructured object/legacy API;
- cần kiểm soát partitioner hoặc dependency ở tầng thấp;
- xây thư viện nền tảng thay vì pipeline analytics thông thường.

Với aggregation theo key, ưu tiên phép kết hợp phía map như `reduceByKey`/`aggregateByKey` thay vì `groupByKey` nếu không cần toàn bộ values; mục tiêu là giảm bytes trước shuffle.

## 2. DataFrame: schema là đầu vào của optimizer

DataFrame là `Dataset[Row]` trong Scala, gồm cột có tên và kiểu. Biểu thức DataFrame/SQL được biểu diễn thành logical plan thay vì một chuỗi opaque functions.

```python
from pyspark.sql import functions as F

result = (
    spark.read.parquet("s3://lake/orders/")
    .where((F.col("status") == "PAID") & (F.col("order_date") >= "2026-09-01"))
    .groupBy("country")
    .agg(F.sum("amount").alias("revenue"))
)
```

Schema và expression tree cho phép Spark:

- chỉ đọc các cột cần thiết;
- push filter xuống data source khi connector hỗ trợ;
- constant folding và null propagation;
- chọn/đổi join strategy theo statistics;
- sinh physical code cho nhiều operator;
- điều chỉnh plan lúc chạy qua AQE.

DataFrame không bảo đảm optimizer luôn làm được mọi điều trên. Data source capability, expression, statistics và configuration quyết định plan thật; `explain()` là cách kiểm chứng.

## 3. Dataset: typed boundary của Scala/Java

Dataset dùng `Encoder[T]` để chuyển JVM object sang representation nội bộ có cấu trúc. API typed cung cấp compile-time checking ở một số ranh giới, nhưng lambda typed có thể làm optimizer nhìn thấy ít hơn so với built-in SQL expression.

Python và R không có typed Dataset API tương đương. Type hint Python không biến DataFrame thành Dataset và không tạo compile-time guarantee ở Spark engine.

Một lựa chọn thực tế trong Scala là giữ phần lớn transform ở DataFrame/Dataset column expressions, chỉ chuyển sang typed function nơi domain logic thật sự hưởng lợi từ type safety.

## 4. Representation vật lý

Ở tầng execution, Spark SQL không nhất thiết giữ mỗi row như một cây JVM objects. Representation nhị phân nội bộ như `UnsafeRow`, columnar batch và generated code giúp giảm object allocation, cải thiện cache locality và thực hiện operation trực tiếp trên encoded data.

Điều này lý giải vì sao “DataFrame chỉ là API cấp cao” là nhận định thiếu: abstraction cấp cao cho engine quyền chọn representation/operator hiệu quả hơn. Chuyển sớm sang RDD của Python/JVM objects có thể đánh mất lợi thế đó.

## 5. Ranh giới Python

PySpark có Driver Python điều khiển JVM và, khi chạy Python function, các Python worker ở Executor. Có ba nhóm cần phân biệt:

| Cách biểu đạt | Nơi engine hiểu logic | Chi phí điển hình |
| --- | --- | --- |
| Built-in DataFrame/SQL expression | Catalyst/physical engine | Tối ưu tốt nhất, tránh Python per-row |
| Scalar Python UDF | Python worker | Serialization và gọi Python theo batch/row path |
| Pandas UDF / Arrow path | Python worker theo columnar batch | Giảm chi phí truyền so với row-at-a-time, vẫn có memory/process boundary |

Ưu tiên built-in functions. Dùng UDF khi logic không thể biểu đạt rõ bằng built-in expression, rồi đo CPU, batch size, peak memory và null/type semantics. Arrow không làm một thuật toán vốn không vector hóa tự nhiên trở nên miễn phí.

`toPandas()`/`collect()` phá vỡ phân tán bằng cách đưa kết quả về Driver. Chỉ dùng khi đã giới hạn và ước lượng kích thước result; `limit()` không phải lúc nào cũng làm upstream join/aggregate rẻ đi.

## 6. Schema là data contract

Inference thuận tiện cho khám phá nhưng có rủi ro production:

- file mới có type khác làm schema merge đắt hoặc thất bại;
- integer bị nâng thành string/double ngoài dự kiến;
- field vắng mặt trở thành null mà không được phát hiện;
- timestamp timezone/precision khác nhau tạo sai nghĩa;
- CSV/JSON malformed record bị drop/quarantine theo mode mà team không theo dõi.

Pipeline ổn định nên khai báo schema, kiểm tra nullability/domain, version data contract và ghi metric cho corrupt/quarantined records. Schema evolution phải được đánh giá cùng table format và reader compatibility, không chỉ ở lệnh `read`.

## 7. Partition không phải business partition

Cần tách ba khái niệm:

- **Spark partition:** đơn vị dữ liệu mà một Task xử lý trong một Stage.
- **Table/file partition:** layout bền vững theo cột như `event_date=...` để pruning.
- **Kafka partition:** log shard và đơn vị ordering/parallel consumption.

Chúng có thể ảnh hưởng nhau nhưng không đồng nhất. Đọc một table partition có thể tạo nhiều Spark input partitions; một Spark shuffle partition có thể chứa record từ nhiều file partitions.

Một RDD pair có thể mang `Partitioner`, cho phép một số operation tránh reshuffle nếu partitioner tương thích. DataFrame partitioning được biểu diễn trong physical plan (`HashPartitioning`, `RangePartitioning`, `SinglePartition`...) và có thể thay đổi qua `Exchange`.

## 8. Chọn abstraction

| Nhu cầu | Lựa chọn mặc định | Lý do |
| --- | --- | --- |
| ETL, join, aggregate, window | DataFrame/SQL | Optimizer nhìn thấy schema và expression |
| Typed domain pipeline JVM | Dataset kết hợp expressions | Type safety ở ranh giới cần thiết |
| Custom low-level distributed algorithm | RDD | Kiểm soát partition/dependency/function |
| Python analytics phân tán | DataFrame + built-ins | Tránh per-row Python boundary |
| Thư viện cần thao tác object đặc thù | Đánh giá Dataset/RDD | Chấp nhận ít optimizer visibility hơn |

Không chuyển abstraction chỉ vì cú pháp ngắn hơn. Hãy kiểm tra physical plan, serialization path, số partition và khả năng observability sau khi chuyển.

## 9. Thực chiến: thay Python UDF bằng expression có cấu trúc

Giả sử pipeline chuẩn hóa mã quốc gia bằng một scalar Python UDF: trim khoảng trắng, đổi thành chữ hoa, rồi ánh xạ giá trị rỗng thành `UNKNOWN`. Logic đơn giản nhưng UDF biến biểu thức thành hộp đen ở ranh giới JVM–Python.

```python
from pyspark.sql import functions as F

normalized = orders.withColumn(
    "country_code",
    F.when(
        F.length(F.trim(F.col("country_code"))) == 0,
        F.lit("UNKNOWN"),
    ).otherwise(F.upper(F.trim(F.col("country_code")))),
)
```

Việc viết lại không chỉ nhằm “tránh Python”. Built-in expression giữ type/null semantics trong logical plan, cho phép code generation và giúp người đọc thấy trực tiếp computation khi dùng `explain`. Tuy nhiên, thay đổi chỉ đúng nếu contract được khóa rõ:

- `NULL` giữ là `NULL` hay cũng trở thành `UNKNOWN`?
- chuỗi chỉ có whitespace có được coi là rỗng không?
- Unicode upper-case và locale có ảnh hưởng mã hợp lệ không?
- input ngoài domain được sửa, loại hay quarantine?
- output column có nullability và độ dài nào?

Trước khi thay, tạo fixture chứa `NULL`, chuỗi rỗng, whitespace, lowercase, Unicode và giá trị sai domain. So sánh output theo từng row, schema và null count. Sau đó so physical plan, Python worker time, serialization metrics và runtime trên partition đại diện. Nếu logic thật sự cần thư viện Python, Pandas UDF có thể giảm overhead truyền dữ liệu theo row nhưng vẫn cần kiểm soát batch memory và semantics.

Quy tắc chọn abstraction trong case này là: dùng expression cấu trúc cho phần engine có thể hiểu; cô lập code opaque ở ranh giới nhỏ nhất; chỉ hạ xuống RDD khi thuật toán cần dependency/partition primitive mà DataFrame không biểu đạt được. Đừng chuyển cả pipeline sang RDD chỉ vì một bước chuẩn hóa khó — bạn sẽ đánh mất column pruning, query planning và phần lớn khả năng quan sát ở SQL tab.

> **Invariant cần giữ:** cùng input contract phải tạo cùng business output. Hiệu năng chỉ được đánh giá sau khi equality và schema contract đã PASS.

## Kết luận

Abstraction là một hợp đồng thông tin với engine. DataFrame/SQL thường nhanh không phải vì API “ma thuật”, mà vì schema và expression tree cho Spark không gian tối ưu lớn hơn. RDD vẫn quan trọng khi bài toán thực sự cần primitive cấp thấp; nó không nên là đường thoát mặc định cho mọi transform khó viết.

**Đọc tiếp:** [Query planning](query-planning.md) · [Partitioning và Shuffle](partition-shuffle.md) · [Memory và Fault Tolerance](memory-fault-tolerance.md)

## Tài liệu chính thức

- [RDD Programming Guide](https://spark.apache.org/docs/4.2.0/rdd-programming-guide.html)
- [Spark SQL, DataFrames and Datasets](https://spark.apache.org/docs/4.2.0/sql-programming-guide.html)
- [Arrow in PySpark](https://spark.apache.org/docs/4.2.0/api/python/user_guide/sql/arrow_pandas.html)
