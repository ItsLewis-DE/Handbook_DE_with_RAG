# Đề xuất thiết kế trang thư viện

Ba hình mẫu dành cho trang `/library/` của Behind the Pipeline. Mục tiêu: làm từng bài nổi bật, hiện đại và dễ nhận diện hơn. Đây là bộ mẫu để lựa chọn thiết kế.

## Đề xuất: 02 — Lưới thẻ có bìa

Sáu bài hiện có vừa một lưới 3 × 2 trên desktop. Mỗi bài có hình minh họa kỹ thuật cùng phong cách, nhãn chủ đề, tiêu đề và tóm tắt ngắn. Giữ bảng màu xanh `#17302d`, kem `#f3f0e8`, cam `#ed6840`.

| Mẫu | Bố cục | Điểm mạnh | Đánh đổi |
| --- | --- | --- | --- |
| 01 | Một bài nổi bật + năm thẻ nhỏ | Điểm nhìn mạnh, hợp phong cách tạp chí | Cần chọn bài nổi bật |
| 02 | Sáu thẻ có bìa, lưới 3 × 2 | Mỗi bài đều nổi bật, dễ nhận diện | Cần duy trì bộ bìa đồng nhất |
| 03 | Bộ lọc bên trái + danh sách có ảnh nhỏ | Dễ tra cứu, phù hợp khi nhiều bài | Hình ảnh ít nổi bật hơn |

## Nội dung dùng trong mẫu

- Database Internals: Phân cấp & Lưu trữ PostgreSQL; Index trong cơ sở dữ liệu.
- Data Architecture: Shared-disk vs shared-nothing; Data Lake, Data Warehouse và Data Mart.
- Orchestration: Apache Airflow.
- Distributed Computing: Apache Spark.

Tổng cộng 6 bài thuộc 4 chủ đề, đối chiếu với `mkdocs.yml` và nguồn nội dung hiện tại. Các bản dịch không được tính thành bài riêng. Mẫu không đưa số phút đọc hay ngày đăng khi chưa có dữ liệu.

## Khi triển khai mẫu đã chọn

- Toàn bộ thẻ hoặc hàng bài viết là một liên kết, có hover và focus rõ ràng.
- Bộ lọc và tìm kiếm kết hợp trên sáu bài hiện có, có trạng thái không có kết quả.
- Lưới 3 cột chuyển thành 2 rồi 1 cột theo không gian; bộ lọc chuyển thành hàng cuộn hoặc menu trên điện thoại.
- Tóm tắt bám nội dung thật; kiểm tra sơ đồ kỹ thuật và thay chữ giả trong hình bìa trước khi đưa lên trang.
- Header dùng thiết kế gọn đã có.

## Hình và prompt

- [Trang xem cả ba mẫu](index.html)
- [01 — Tạp chí kỹ thuật](01-editorial-feature.png) · [Prompt 01](01-editorial-feature.prompt.txt)
- [02 — Lưới thẻ có bìa](02-visual-card-grid.png) · [Prompt 02](02-visual-card-grid.prompt.txt)
- [03 — Thư viện tra cứu](03-filtered-catalog.png) · [Prompt 03](03-filtered-catalog.prompt.txt)
- [Ảnh giao diện ban đầu](current-library-reference.png)

Tạo bằng **imagegen tích hợp**, dùng ảnh chụp trang từ bản dựng mã nguồn hiện tại làm tham chiếu. Các hình là mockup thiết kế để lựa chọn; sơ đồ trên bìa mang tính minh họa ý tưởng.

