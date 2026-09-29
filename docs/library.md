---
title: Thư viện bài viết
template: library.html
hide:
- toc
- navigation
cards:
  postgres/postgres.md:
    order: 0
    variant: postgres
    art: assets/images/postgres/card-art.jpg
    heading: PostgreSQL (phần 1)<br>Phân cấp, tiến trình &amp; bộ nhớ
    summary: Cluster, database, schema, kết nối, cơ chế khóa và bộ nhớ phục vụ truy vấn.
    footer: DATABASE INTERNALS
  postgres/p2.md:
    order: 0.5
    variant: postgres
    art: assets/images/postgres/card-art.jpg
    heading: PostgreSQL (phần 2)<br>Truy vấn, lưu trữ &amp; phục hồi
    summary: Hành trình SQL qua Parser, Planner, Executor đến bộ đệm, WAL, PGDATA và TOAST.
    footer: DATABASE INTERNALS
  index/index.md:
    order: 1
    variant: index
    art: assets/images/index/card-art.jpg
    heading: Index trong<br>cơ sở dữ liệu
    summary: Từ full table scan đến cấu trúc dữ liệu giúp database tìm bản ghi nhanh hơn.
    footer: Tác giả · Phong Thanh
  ware_lake_lw/doc.md:
    order: 3
    variant: storage
    art: assets/images/ware_lake_lw/card-art.png
    heading: Data Lake, Warehouse<br>&amp; Data Mart
    summary: Vai trò từng mô hình lưu trữ và cách chúng hội tụ trong kiến trúc Data Lakehouse.
    footer: DATA ARCHITECTURE
  airflow/architecture.md:
    order: 4
    variant: airflow
    art: assets/images/airflow/card-art.jpg
    heading: Hiểu kiến trúc<br>Apache Airflow
    summary: Từ nhu cầu điều phối đến Scheduler, Executor và High Availability.
    footer: Tác giả · Phong Thanh
  spark/archi.md:
    order: 5
    variant: spark
    art: assets/images/spark/card-art.jpg
    heading: Kiến trúc<br>Apache Spark (phần 1)
    summary: Từ Driver và Executor đến luồng thực thi Job, Stage, Task và cơ chế shuffle.
    footer: DISTRIBUTED COMPUTING
  spark/p2.md:
    order: 6
    variant: spark
    art: assets/images/spark/card-art.jpg
    heading: Kiến trúc<br>Apache Spark (phần 2)
    summary: Các chiến lược Join, vai trò của RDD, giao tiếp PySpark và quản lý bộ nhớ Driver, Executor.
    footer: DISTRIBUTED COMPUTING
---
