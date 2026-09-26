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
    heading: PostgreSQL<br>Phân cấp &amp; lưu trữ
    summary: Database cluster, bộ đệm shared_buffers, database, schema và cấu trúc thư mục PGDATA.
    footer: DATABASE INTERNALS
  index/index.md:
    order: 1
    variant: index
    art: assets/images/index/card-art.jpg
    heading: Index trong<br>cơ sở dữ liệu
    summary: Từ full table scan đến cấu trúc dữ liệu giúp database tìm bản ghi nhanh hơn.
    footer: Tác giả · Phong Thanh
  architecture/shared-disk-vs-shared-nothing.md:
    order: 2
    variant: disk
    art: assets/images/disk/card-art.jpg
    heading: Shared-disk<br>&amp; shared-nothing
    summary: Ownership, locality, shuffle và những đánh đổi khi mở rộng hệ thống dữ liệu.
    footer: DATA ARCHITECTURE
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
    heading: Kiến trúc<br>Apache Spark
    summary: Từ Driver và Executor đến luồng thực thi Job, Stage, Task và cơ chế shuffle.
    footer: DISTRIBUTED COMPUTING
---
