# Đề xuất logo — Behind the Pipeline

Mở `index.html` bằng trình duyệt để xem ba hướng thiết kế, đổi nền sáng/tối và kiểm tra ứng dụng ở kích thước nhỏ. Tất cả hình được dựng bằng SVG trực tiếp; font dùng lại từ dự án, không gọi dịch vụ bên ngoài.

## Cơ sở thiết kế

README phân biệt **Pipeline RAG** (hệ thống hỏi đáp) và **Behind the Pipeline** (website xuất bản). Bộ đề xuất này tập trung vào thương hiệu website theo `mkdocs.yml` và thông điệp trang chủ: tìm hiểu nguyên lý, kiến trúc và cách hệ thống vận hành bên trong. Khi dùng cho sản phẩm RAG, có thể ghép cùng biểu tượng với tên “Pipeline RAG”.

Logo hiện tại có sách, đường nối và ba nút dữ liệu; favicon lại chỉ dùng đường nối. Hướng mới cần một biểu tượng thống nhất ở cả hai vị trí, giảm chi tiết khi thu nhỏ và giữ sự liên tục với màu xanh/ngà hiện tại.

## Ba hướng

| Hướng | Ý tưởng | Phù hợp | Đánh đổi |
| --- | --- | --- | --- |
| **01 · Pipeline Monogram — đề xuất chính** | Chữ P hình học, một đường dữ liệu đi vào lõi | Hiện đại, gọn, dùng cho website và sản phẩm RAG | Cần đi cùng tên đầy đủ trong lần xuất hiện đầu tiên |
| 02 · Layered Portals | Các lớp kiến trúc mở sâu vào hệ thống | Điềm tĩnh, có chất kiến trúc, hình khối rõ | Liên tưởng Data Engineering gián tiếp hơn |
| 03 · Open Folio | Cuốn sách được lược giản, một nét nối giữa hai trang | Giữ liên hệ với nhận diện cũ và nội dung học tập | Ít khác biệt hơn các thương hiệu xuất bản khác |

## Hướng khuyến nghị

- **Biểu tượng:** Pipeline Monogram. Thân P chắc, lòng chữ thoáng, nhánh ngang màu đồng gợi thao tác đi vào bên trong pipeline. Không dùng hiệu ứng kim loại, đổ bóng hoặc gradient.
- **Màu:** xanh `#17302D`, ngà `#F3F0E8`, đồng lì `#B38A58`. Màu đồng dành cho điểm nhấn nhận diện, không dùng cho chữ nhỏ trên nền ngà. Cam `#ED6840` có thể tiếp tục dành cho nút và trạng thái tương tác của website.
- **Chữ:** Manrope 600–650 cho tên thương hiệu; giữ khoảng cách chữ tự nhiên và bố cục thoáng. Lora tiếp tục phù hợp với tiêu đề bài viết, không cần đưa vào biểu tượng.
- **Kích thước:** bản đầy đủ dùng từ 24 px; favicon riêng đã đơn giản hóa cho 16/32 px. Bảng xem thử cho phép kiểm tra trực quan các kích thước này; cần kiểm tra lại trong vị trí tích hợp thực tế trước khi phát hành.
- **Khoảng an toàn:** tối thiểu 12 đơn vị trên hệ tọa độ biểu tượng 96 × 96, tính từ mép hình. Tránh ép biểu tượng vào tỉ lệ ngang của logo cũ.
- **Nền:** bản xanh cho nền sáng, bản ngà cho nền tối; bản một màu cho in ấn. SVG không chứa font hoặc phụ thuộc ngoài.

## Tệp bàn giao

- `pipeline-monogram.svg`: biểu tượng chính, nền trong suốt.
- `pipeline-monogram-inverse.svg`: biểu tượng cho nền tối.
- `pipeline-monogram-mono.svg`: bản một màu.
- `pipeline-favicon.svg`: favicon nền xanh.
- `layered-portals.svg`, `open-folio.svg`: hai hướng so sánh.
- `index.html`: bảng trình bày và mô phỏng ứng dụng; các chữ ghép với logo ở đây là bản xem thử dùng font local.
- `proposal-desktop.png`, `proposal-mobile.png`: ảnh chụp bảng đề xuất trong trình duyệt.
- `pipeline-lockup-preview.png`: bản xem nhanh biểu tượng ghép tên thương hiệu trên nền tối.

Đã kiểm tra bằng Chromium: SVG hợp lệ, ảnh và font local tải được, chuyển ba hướng thiết kế trên hai nền hoạt động, không tràn ngang ở chiều rộng 375/390/768/1440 px và không có lỗi JavaScript. Đã xem ảnh chụp desktop/mobile để rà bố cục.

Đây là bộ đề xuất riêng trong `design/brand/`, chưa thay logo đang dùng trên website. Khi triển khai hướng 01: thay tài nguyên trong `docs/assets/images/brand/`, chỉnh khung logo ở `docs/stylesheets/brand.css` về vuông, đồng bộ tên thương hiệu trong header và kiểm tra desktop/mobile. Không cần thay tên dự án hoặc thiết kế lại toàn bộ giao diện.
