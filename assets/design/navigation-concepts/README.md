# Đề xuất điều hướng — Behind the Pipeline

Đây là bộ hình ý tưởng để so sánh trước khi chọn thiết kế.

## Phương án ưu tiên: 01 — Thư viện mở rộng

Header cố định: **Trang chủ · Thư viện ▾ · Tìm bài viết**.

Bấm Thư viện để mở một bảng chia nhóm bài viết. Header không tăng số nút khi thêm bài. Logo cũng dẫn về trang chủ; có thể bỏ mục Trang chủ nếu cần thêm khoảng trống.

Các nhóm đề xuất dựa trên nội dung hiện có:

- Database Internals: PostgreSQL, Indexing.
- Data Architecture: Shared-disk vs shared-nothing.
- Orchestration: Apache Airflow.
- Distributed Computing: Apache Spark.

Bảng chỉ nên hiển thị một số bài tiêu biểu trong mỗi nhóm và đường dẫn xem toàn bộ nhóm khi thư viện lớn. Trang thư viện dùng danh sách hoặc lưới cùng tìm kiếm/lọc để chứa toàn bộ bài; không đưa mọi bài vào một mega menu dài vô hạn.

Trên điện thoại: logo + tìm kiếm + nút menu, mở bảng toàn chiều rộng với các nhóm có thể đóng/mở.

## So sánh ba mẫu

| Mẫu | Cách hoạt động | Điểm mạnh | Đánh đổi |
| --- | --- | --- | --- |
| 01 — Thư viện mở rộng | Một nút mở bảng bài viết chia nhóm | Hợp trang chủ hiện tại, cân bằng độ gọn và khả năng khám phá | Cần mở bảng trước khi chọn bài |
| 02 — Menu theo chủ đề | Ba nhóm Database, Data Pipeline, Architecture hiện trên header | Thấy phạm vi kiến thức ngay lập tức | Cần giữ số nhóm cấp cao ổn định; tên nhóm dài sẽ tốn chỗ |
| 03 — Ngăn danh mục | Nút Danh mục mở ngăn cạnh có tìm kiếm và danh sách nhóm | Nhiều không gian duyệt bài, chuyển sang mobile tự nhiên | Che một phần nội dung khi mở; cần thêm thao tác |

Các nhãn và cách gom nhóm là đề xuất, không thay đổi cấu trúc nội dung hiện tại. Trong mẫu 02, Data Pipeline gom Airflow và Spark như một nhóm duyệt bài rộng, không coi hai công cụ có cùng chức năng.

## Chi tiết nên giữ khi triển khai

- Giữ xanh trầm `#17302d`, nền giấy `#f3f0e8`, điểm nhấn cam `#ed6840`.
- Dùng chữ sans vừa phải cho các mục menu; để font đậm mang cá tính ở ticker và thương hiệu.
- Bài đang đọc có trạng thái chọn; thêm đường dẫn cấp bậc ở trang bài viết nếu cần.
- Menu mở bằng bấm/chạm, dùng được với bàn phím; Esc đóng và trả focus về nút mở. Xem [mẫu điều hướng disclosure của W3C](https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/examples/disclosure-navigation/).
- Nếu triển khai tìm kiếm, cần kết nối chỉ mục tìm kiếm thực tế; hình chỉ minh họa trạng thái giao diện.
- Bản Việt/Anh là lựa chọn ngôn ngữ của cùng bài, không nhân đôi các nút trên header.
- Tránh kéo dài hàng pill hoặc chỉ thêm nút “More” cho một danh sách ngày càng dài.

## Hình và prompt

- [01 — Thư viện mở rộng](01-library-panel.png)
- [02 — Menu theo chủ đề](02-topic-menus.png)
- [03 — Ngăn danh mục](03-catalog-drawer.png)
- [Trang xem bộ mẫu](index.html)

Tạo bằng công cụ image_gen tích hợp, dùng ảnh `assets/readme/website-desktop.png` làm tham chiếu giao diện và đối chiếu nội dung với mã nguồn hiện tại. Đây là mockup AI, không phải ảnh chụp một tính năng đã triển khai; chữ hoặc chi tiết nhỏ có thể khác khi dựng thật.

Prompt đầy đủ nằm trong các file `*.prompt.txt` cùng thư mục.

