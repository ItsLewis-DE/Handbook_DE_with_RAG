---
title: Data Lake, Data Warehouse và Data Mart
lang: vi
translation_key: lake-warehouse-mart
hide:
  - navigation
---

<header class="airflow-article-hero storage-article-hero">
  <div class="airflow-article-hero__eyebrow">
    <a href="../../">BEHIND THE PIPELINE</a>
    <span>ARTICLE / 006</span>
  </div>
  <h1>Data Lake, Data Warehouse<br><em>&amp; Data Mart</em></h1>
  <p class="airflow-article-hero__dek">
    Từ đặc trưng của Big Data đến cách các nền tảng lưu trữ dữ liệu vận hành,
    khác biệt và hội tụ trong kiến trúc Data Lakehouse.
  </p>
  <div class="airflow-article-hero__meta" aria-label="Thông tin bài viết">
    <span>DATA ARCHITECTURE</span>
    <span>EDITION 06 · 2026</span>
  </div>
</header>

> **Lưu ý trước khi đọc:** Đây là một bài viết dài, cần nhiều hơn vài phút đọc lướt. Bạn hãy dành thời gian, chuẩn bị một ly nước và giữ sự tập trung để theo dõi nội dung.

## Vì sao cần phân biệt các mô hình lưu trữ dữ liệu?

Một doanh nghiệp có thể cùng lúc thu thập đơn hàng, lượt nhấp trên website, log ứng dụng và hình ảnh. Tất cả đều là dữ liệu, nhưng không phải loại nào cũng nên được lưu và khai thác theo cùng một cách. Khi lượng dữ liệu tăng lên, câu hỏi không chỉ là **lưu ở đâu**, mà còn là **ai sẽ dùng dữ liệu và dùng để làm gì**.

Bài viết bắt đầu từ các đặc trưng của Big Data, sau đó đi qua Data Lake, Data Warehouse và Data Mart để làm rõ vai trò, điểm mạnh và giới hạn của từng mô hình. Cuối cùng, chúng ta sẽ xem Data Lakehouse kết hợp những khả năng đó như thế nào.

## 1. Đặt vấn đề và định nghĩa Big Data

### 1.1. Bối cảnh bùng nổ dữ liệu

Trong kỷ nguyên số, lượng dữ liệu được tạo ra mỗi ngày trên thế giới tăng với tốc độ rất nhanh. Internet, mạng xã hội, thiết bị di động, hệ thống cảm biến và các dịch vụ trực tuyến liên tục tạo ra lượng dữ liệu khổng lồ.

Ví dụ, trong một phút có 12 triệu người gửi iMessage, 6 triệu người mua sắm trực tuyến; người dùng YouTube phát trực tuyến 694.000 video và người dùng TikTok xem 167 triệu video.

Doanh nghiệp thu thập dữ liệu từ nhiều nguồn khác nhau:

- Hành vi người dùng trên website, như lượt nhấp chuột và thời gian xem trang.
- Dữ liệu GPS từ điện thoại.
- Lịch sử mua hàng.
- Bình luận trên mạng xã hội.

### 1.2. Big Data là gì?

**Big Data (dữ liệu lớn)** là thuật ngữ chỉ những tập dữ liệu có kích thước rất lớn và phức tạp, khó quản lý hoặc phân tích bằng các công cụ xử lý dữ liệu truyền thống, đặc biệt là bảng tính và hệ thống xử lý dữ liệu thông thường.

#### Phân loại dữ liệu

- **Dữ liệu có cấu trúc:** Có thể lưu trữ theo lược đồ xác định rõ, chẳng hạn trong cơ sở dữ liệu; có thể biểu diễn thành bảng gồm hàng và cột. Ví dụ: bảng tính Excel và cơ sở dữ liệu SQL.
- **Dữ liệu phi cấu trúc:** Không có cấu trúc dễ nhận dạng nên không thể tổ chức theo cách thông thường trong cơ sở dữ liệu quan hệ dưới dạng hàng và cột. Dữ liệu không tuân theo một định dạng, trình tự, ngữ nghĩa hoặc quy tắc cụ thể. Ví dụ: hình ảnh và video.
- **Dữ liệu bán cấu trúc:** Không được lưu trữ đơn thuần dưới dạng hàng và cột như trong cơ sở dữ liệu quan hệ. Dữ liệu chứa thẻ, phần tử hoặc siêu dữ liệu để nhóm và sắp xếp theo hệ thống phân cấp. Ví dụ: tệp XML và JSON.

#### Đặc trưng của Big Data: mô hình 5V

- **Volume (khối lượng):** Lượng dữ liệu cần xử lý rất lớn, có thể từ hàng chục terabyte (TB) đến hàng trăm petabyte (PB).
- **Velocity (tốc độ):** Dữ liệu được tạo ra và truyền đến hệ thống rất nhanh, thậm chí trong thời gian thực.
- **Variety (đa dạng):** Dữ liệu có nhiều dạng, từ dữ liệu có cấu trúc đến phi cấu trúc, như văn bản, âm thanh và video. Một số dạng cần xử lý bổ sung để rút ra ý nghĩa và hỗ trợ siêu dữ liệu.
- **Veracity (độ tin cậy):** Mức độ chính xác, đáng tin cậy, chất lượng và tính toàn vẹn của dữ liệu.
- **Value (giá trị):** Giá trị doanh nghiệp có thể khai thác khi chuyển dữ liệu thành thông tin hữu ích.

## 2. Các nền tảng lưu trữ dữ liệu

### 2.1. Data Lake (hồ dữ liệu) — “Cái phễu hứng mọi thứ”

**Khái niệm:** Data Lake là kho lưu trữ tập trung, cho phép lưu dữ liệu ở mọi quy mô: dữ liệu có cấu trúc như bảng SQL, bán cấu trúc như JSON và XML, cũng như phi cấu trúc như hình ảnh, video, tệp âm thanh và PDF. Các công cụ như Minio, AWS S3,..

#### Đặc điểm cốt lõi

- **Lưu trữ dữ liệu thô:** Dữ liệu được giữ nguyên từ nguồn, không qua quá trình transform.
- **Khả năng mở rộng lớn:** Data Lake thường được xây dựng trên các hệ thống lưu trữ đám mây như Amazon S3, Google Cloud Storage và Azure Data Lake Storage. Chi phí lưu trữ thấp cho phép lưu lượng dữ liệu ở quy mô petabyte.
- **Đa dạng kiểu dữ liệu:** Có thể tiếp nhận mọi loại dữ liệu từ có cấu trúc đến không có cấu trúc.
- **Tách biệt lưu trữ và tính toán:** Dữ liệu được lưu ở một nơi; khi cần xử lý mới sử dụng cụm máy tính toán như Spark hoặc Presto.

#### Hạn chế

- **Nguy cơ thành “Data Swamp” (đầm lầy dữ liệu):** Nếu không kiểm soát chặt lược đồ, phân loại dữ liệu, gắn siêu dữ liệu (*metadata*), xác định quyền sở hữu và kiểm soát chất lượng đầu vào, dữ liệu sẽ khó quản lý.
- **Thiếu giao dịch ACID:** Data Lake truyền thống không tự cung cấp đầy đủ các tính năng như đối với Data Warehouse.
- **Thiếu phiên bản dữ liệu:** Không có sẵn cơ chế truy vấn các phiên bản dữ liệu trong quá khứ.
- **Truy vấn chậm hơn Data Warehouse:** Hệ thống chủ yếu phục vụ lưu trữ, chưa tối ưu truy vấn như cơ sở dữ liệu.

### 2.2. Data Warehouse (kho dữ liệu) — “Thư viện đã phân loại”

**Khái niệm:** Data Warehouse là hệ thống lưu trữ dữ liệu trung tâm, tích hợp dữ liệu từ nhiều nguồn, hầu như các Data Warehouse hiện nay đều lưu trữ dữ liệu dạng cột. Nhằm tối ưu cho các truy vấn cần lấy nhiều dòng.

**Các công cụ như:** Snowflake, Google BigQuery và Amazon Redshift,..

#### Đặc điểm cốt lõi

- **Hướng chủ đề (subject-oriented):** Dữ liệu được tổ chức quanh các chủ đề chính của doanh nghiệp như khách hàng, bán hàng và sản phẩm.
- **Tích hợp (integrated):** Dữ liệu từ nhiều nguồn được làm sạch và thường được chuẩn hóa về định dạng thống nhất trước khi nạp vào kho.
- **Biến đổi theo thời gian (time-variant):** Kho thường lưu lịch sử lâu dài tùy vào cấu hình, để so sánh và phân tích xu hướng.
- **Không biến động (non-volatile):** Dữ liệu đã nạp thường ít bị người dùng cuối thay đổi hoặc xóa; khi có thay đổi, dữ liệu mới thường được thêm bên cạnh dữ liệu cũ. Dữ liệu chủ yếu được đọc để phân tích.

#### Hạn chế

- Chỉ tối ưu trong việc lưu dữ liệu dạng có cấu trúc.
- Độ trễ dữ liệu, vì thường phải qua những bước transform dữ liệu.
- Khó khăn cho các thư viện học máy, học sâu truy vấn.

### 2.3. Data Mart

**Khái niệm:** Trong kiến trúc kho dữ liệu truyền thống, Data Mart là kho dữ liệu tập trung vào một chủ đề hoặc một đơn vị kinh doanh cụ thể trong tổ chức.

#### Đặc điểm cốt lõi

- **Phạm vi tập trung:** Khác với Data Warehouse bao phủ toàn doanh nghiệp, Data Mart chỉ chứa dữ liệu của một lĩnh vực như bán hàng, tài chính hoặc marketing.
- **Kích thước nhỏ gọn:** Vì chỉ chứa dữ liệu chuyên biệt, Data Mart thường nhỏ hơn kho dữ liệu tổng, giúp truy vấn nhanh hơn.
- **Cấu trúc dữ liệu tối ưu:** Dữ liệu thường được mô hình hóa theo dạng dễ hiểu với người dùng cuối, chẳng hạn mô hình ngôi sao (*Star Schema*), để phục vụ trực tiếp công cụ BI (*Business Intelligence*).

### 2.4. Hình dung luồng dữ liệu như một nhà hàng

Bạn có thể hình dung toàn bộ hệ thống dữ liệu giống như một nhà hàng lớn.

Đầu tiên, Data Lake giống như kho nguyên liệu tổng của nhà hàng. Ở đây, mọi loại nguyên liệu đều được đưa vào và lưu trữ gần như nguyên trạng: rau, thịt, hải sản, gia vị… thậm chí có cả những nguyên liệu chưa được sơ chế. Kho này không kén chọn, cứ có là nhận, miễn là còn chỗ chứa.

Tiếp theo, Data Pipeline (ETL/ELT) đóng vai trò như quy trình vận chuyển và sơ chế nguyên liệu. Nguyên liệu từ kho sẽ được mang vào bếp, rửa sạch, cắt gọt, phân loại và chuẩn bị theo tiêu chuẩn nhất định trước khi chế biến.

Sau đó, Data Warehouse chính là khu bếp trung tâm của nhà hàng. Tại đây, nguyên liệu đã được xử lý sẽ được nấu nướng, sắp xếp và chuẩn hóa thành các món ăn hoàn chỉnh, đảm bảo chất lượng và sẵn sàng phục vụ khách hàng.

Cuối cùng, Data Mart giống như các quầy phục vụ riêng trong nhà hàng, ví dụ như quầy món Á, quầy món Âu hay quầy tráng miệng. Mỗi quầy chỉ phục vụ một nhóm món ăn cụ thể, giúp khách hàng dễ dàng lựa chọn và lấy đúng thứ mình cần mà không phải đi qua toàn bộ khu bếp.

![Minh họa Data Lake là kho nguyên liệu, Pipeline sơ chế, Data Warehouse là bếp trung tâm và Data Mart là các quầy phục vụ riêng](../assets/images/ware_lake_lw/flow.png){ loading=lazy }

*Hình minh họa vai trò của từng lớp.*

## 3. ETL và ELT

Lúc nãy ta có nhắc đến ETL/ELT, vậy thì nó là gì?

### 3.1. ETL — Extract → Transform → Load

ETL là quy trình xử lý dữ liệu theo thứ tự:

```text
Nguồn dữ liệu → Extract → Transform → Load → Data Warehouse
```

- **Extract (Trích xuất):** Lấy dữ liệu từ nhiều nguồn khác nhau như database, API, file CSV/JSON,...
- **Transform (Biến đổi):** Làm sạch, chuẩn hóa, xử lý và kết hợp dữ liệu.
- **Load (Nạp):** Sau khi dữ liệu đã được xử lý xong thì mới đưa vào Data Warehouse.

còn ELT là:

### 3.2. ELT — Extract → Load → Transform

ELT thay đổi thứ tự thành:

```text
Nguồn dữ liệu → Extract → Load → Transform
```

- **Extract:** Lấy dữ liệu từ các nguồn.
- **Load:** Đưa dữ liệu raw vào hệ thống lưu trữ trước tiêu biểu như AWS S3.
- **Transform:** Sau đó mới xử lý dữ liệu khi cần sử dụng.

## 4. Xu hướng tương lai

### 4.1. Data Lakehouse

Một xu hướng trong kiến trúc dữ liệu là **Data Lakehouse**. Mô hình này được Databricks giới thiệu như sự kết hợp giữa Data Warehouse và Data Lake, xuất phát từ ưu điểm và hạn chế của từng mô hình:

- Data Warehouse lưu dữ liệu theo cấu trúc rõ ràng, nhưng dữ liệu thường tập trung vào một số dạng như số liệu và bảng biểu.
- Trong bối cảnh LLM và AI phát triển, việc huấn luyện mô hình đòi hỏi nhiều loại dữ liệu, không thể chỉ dựa vào một dạng duy nhất.
- Data Lake lưu được nhiều loại dữ liệu như một chiếc phễu, nhưng dữ liệu thiếu cấu trúc sẽ khó quản lý. Data Lake truyền thống cũng thiếu độ tin cậy khi chưa có cơ chế kiểm soát ghi và đọc đồng thời (*concurrency control*).

Data Lakehouse tận dụng tính linh hoạt của Data Lake, đồng thời bổ sung thêm một lớp quản lý dữ liệu như Iceberg hay Delta. Nhờ đó khi sử dụng Data Lake bạn không cần phải lo tình trạng data swap nữa. Cung cấp các tính năng quản lý dữ liệu mạng mẽ như Data Warehouse như ACID, data versioning,...

ACID là gì?

### 4.2. Giao dịch ACID trong Data Lakehouse

Data Lakehouse còn hỗ trợ các tính chất ACID:

- **A — Atomicity (tính nguyên tử):** Giao dịch hoặc thành công toàn bộ hoặc không có hiệu lực. Ví dụ, nếu quá trình ghi thất bại giữa chừng và log cuối cùng chưa được ghi, lần ghi đó được xem như chưa từng xảy ra.
- **C — Consistency (tính nhất quán):** Dữ liệu tuân theo quy tắc và lược đồ. Ví dụ, cột `age` yêu cầu số thì không thể chèn chuỗi vào cột này.
- **I — Isolation (tính cô lập):** Nhiều người ghi cùng lúc không làm các giao dịch ảnh hưởng lẫn nhau. Ví dụ, bạn đang ghi dựa trên phiên bản 10, nhưng một người khác đã ghi và tạo phiên bản 11; lần ghi dựa trên phiên bản 10 sẽ thất bại và cần thử lại.
- **D — Durability (tính bền vững):** Dữ liệu đã ghi thành công sẽ không bị mất.

---

## Lời kết

Không có một nơi lưu trữ phù hợp cho mọi loại dữ liệu và mọi người dùng. Khi thiết kế nền tảng dữ liệu, hãy bắt đầu từ dạng dữ liệu cần lưu, cách dữ liệu được xử lý và nhu cầu truy vấn của từng nhóm: khám phá dữ liệu thô, lập báo cáo chung hay phân tích cho một phòng ban. Từ đó, bạn sẽ thấy Data Lake, Data Warehouse, Data Mart và Data Lakehouse có thể đảm nhận những vai trò khác nhau trong cùng một kiến trúc.

Cảm ơn bạn đã đọc đến cuối! Hẹn gặp lại ở những bài viết tiếp theo.

<footer class="airflow-article-end ware-lake-article-end">
  <div>
    <span>BEHIND THE PIPELINE / 006</span>
    <strong>Hiểu hệ thống,<br>không chỉ cú pháp.</strong>
  </div>
  <a href="../../">Trở về thư viện <span aria-hidden="true">→</span></a>
</footer>
