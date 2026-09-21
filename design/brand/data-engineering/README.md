# Đề xuất logo: Behind the Pipeline / Data Engineering

Bộ đề xuất này ưu tiên ba yêu cầu: hiện đại, sang trọng và gợi rõ lĩnh vực Data Engineering. Mở `index.html` trong trình duyệt để so sánh ba hướng trên nền sáng hoặc tối. Toàn bộ biểu tượng được vẽ bằng SVG trong repository; trang trình bày dùng font local có sẵn, không dùng công cụ tạo ảnh hoặc tài nguyên từ dịch vụ bên ngoài.

## Cơ sở từ dự án

- `mkdocs.yml` xác định tên website là **Behind the Pipeline**. `README.md` phân biệt website này với hệ thống hỏi đáp **Pipeline RAG**. Bộ nhận diện dùng tên website làm tên chính và có một mô phỏng ứng dụng cho Pipeline RAG.
- `docs/index.md` đặt Data Engineering ở trung tâm; thư viện bao gồm Airflow, Spark, PostgreSQL và kiến trúc hệ thống dữ liệu. Vì vậy, hình ảnh pipeline và database có cơ sở trực tiếp từ nội dung dự án.
- Logo đang dùng kết hợp sách với các nút nối, thiên về xuất bản kiến thức. Đề xuất chữ P trong thư mục cha gọn hơn nhưng liên tưởng đến dữ liệu còn gián tiếp. Bộ này là một hướng phát triển riêng để ưu tiên khả năng nhận biết lĩnh vực.
- Màu xanh `#17302D`, ngà `#F3F0E8` và font Manrope được kế thừa từ dự án. Điểm nhấn đồng giúp tạo sắc thái trầm và tiết chế.

## Ba hướng

### 01. Pipeline Core — khuyến nghị

Hai ô nguồn dữ liệu đi qua đường nối hội tụ vào một database hình trụ. Hình trụ tạo dấu hiệu lưu trữ quen thuộc; hai nguồn và nhánh hợp thể hiện công việc xây pipeline. Cặp dấu hiệu này phù hợp với toàn bộ thư viện hơn một chữ cái hoặc cuốn sách riêng lẻ.

Đây là hướng cân bằng tốt nhất giữa nhận biết lĩnh vực và hình học tối giản. Dòng phụ **Data Engineering** làm rõ đối tượng khi biểu tượng đi cùng tên thương hiệu. Khả năng người xem nhận ra chính xác ngành nghề chưa được kiểm chứng bằng thử nghiệm người dùng; icon đơn lẻ vẫn có thể gợi tích hợp dữ liệu hoặc database nói chung. Đường nối không có mũi tên nên biểu tượng gợi kết nối và hội tụ, không xác định chiều dữ liệu như sơ đồ kỹ thuật.

### 02. Flow Stack

Luồng dữ liệu đi vào ba lớp hình thoi, gợi lakehouse và data platform. Hình khối có tính kiến trúc, nhưng biểu tượng nhiều lớp cũng có thể được hiểu là hạ tầng phần mềm nói chung.

### 03. DAG Frame

Một nguồn phân nhánh qua hai tác vụ rồi hội tụ, tạo hình thoi cân đối. Hướng này gắn với orchestration và Airflow; đổi lại, người xem có thể liên tưởng tới workflow chung. Đường nối được giản lược, không phải một sơ đồ DAG đầy đủ với mũi tên chỉ hướng.

## Quy cách hướng 01

- **Hình:** hệ tọa độ 96 × 96, nét chính 5 đơn vị, hai nguồn hình vuông bo nhẹ, một đường chia tầng trong database. Biểu tượng nhận nghĩa cả khi chỉ có một màu.
- **Màu sáng:** xanh `#17302D` và đồng `#B38A58` trên nền ngà `#F3F0E8`.
- **Màu tối:** ngà `#F3F0E8` và đồng sáng hơn `#C5A477` trên nền xanh. Đồng chỉ dùng làm điểm nhấn, không dùng cho chữ nội dung nhỏ trên nền ngà.
- **Chữ:** Manrope 450 cho “Behind the”, 650 cho “Pipeline”; IBM Plex Mono cho dòng phụ “Data Engineering”. Các chữ trong bảng trình bày là HTML dùng font local, chưa phải wordmark dạng vector outline.
- **Kích thước:** dùng bản đầy đủ từ 48 px. Từ 24–32 px dùng `pipeline-core-small.svg`; favicon 16/32 px dùng `favicon.svg`. Hai bản nhỏ bỏ đường chia tầng và tăng độ dày nét để tránh dính chi tiết. Ở 16 px, ưu tiên nhận diện hình khối tổng thể; hai nguồn không còn rõ riêng như ở kích thước lớn.
- **Khoảng an toàn:** chừa ít nhất 12 đơn vị ngoài biên viewBox 96 × 96 khi đặt cạnh chữ hoặc biểu tượng khác. Không kéo giãn theo chiều ngang.
- **Phong cách:** màu phẳng, không gradient, hiệu ứng kim loại hoặc bóng đổ. Sắc thái sang trọng đến từ tỷ lệ, độ thoáng và điểm nhấn màu tiết chế.

## Tệp bàn giao

- `pipeline-core.svg`: logo chính, nền trong suốt.
- `pipeline-core-inverse.svg`: phiên bản cho nền tối.
- `pipeline-core-mono.svg`: phiên bản một màu.
- `pipeline-core-small.svg`: phiên bản nhỏ cho header.
- `favicon.svg`: phiên bản 16/32 px có nền xanh.
- `flow-stack.svg`, `dag-frame.svg` và các tệp `-inverse.svg`: hai hướng so sánh trên nền sáng/tối.
- `index.html`, `proposal.css`, `proposal.js`: bảng trình bày tương tác.
- `pipeline-core-preview.png`, `pipeline-core-preview-light.png`: ảnh logo ghép tên thương hiệu.
- `three-directions.png`: ảnh so sánh ba hướng.
- `proposal-desktop.png`, `proposal-mobile.png`: ảnh toàn bộ bảng đề xuất.

## Kiểm tra và phạm vi

Đã kiểm tra chín SVG bằng XML parser, xem ảnh render trong Chromium và kiểm tra bảng trình bày ở chiều rộng 375, 390, 768, 1024 và 1440 px. Cả ba hướng đều chuyển được giữa hai nền; không có tràn ngang, lỗi JavaScript, tài nguyên tải lỗi hoặc request tới dịch vụ bên ngoài. Đã kiểm tra font Manrope local được tải.

Các tệp trong thư mục này là bộ đề xuất độc lập. Logo website, cấu hình MkDocs và bộ đề xuất trong thư mục cha chưa được thay đổi. Khi áp dụng, dùng biểu tượng nhỏ trong header, đồng bộ favicon, đặt khung logo vuông và rà lại cách ghép chữ trong header thực tế.
