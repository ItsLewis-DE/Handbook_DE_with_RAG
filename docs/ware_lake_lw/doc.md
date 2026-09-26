---
title: Data Lake, Data Warehouse và Data Mart
lang: vi
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

<figure class="airflow-opening-comic">
  <img
    src="../../assets/images/ware_lake_lw/opening.png"
    alt="Truyện tranh vui nhắc người đọc chuẩn bị cho một bài viết dài về các mô hình lưu trữ dữ liệu"
    loading="eager"
  >
  <figcaption>
    <span>LƯU Ý TRƯỚC KHI ĐỌC</span>
    <strong>Một bài viết khá dài</strong>
  </figcaption>
</figure>

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

Sự phát triển của các lĩnh vực sau góp phần khiến dữ liệu bùng nổ:

- Internet và mạng xã hội.
- Thiết bị di động.
- IoT.
- Các nền tảng thương mại điện tử.

### 1.2. Big Data là gì?

**Big Data (dữ liệu lớn)** là thuật ngữ chỉ những tập dữ liệu có kích thước rất lớn và phức tạp, khó quản lý hoặc phân tích bằng các công cụ xử lý dữ liệu truyền thống, đặc biệt là bảng tính và hệ thống xử lý dữ liệu thông thường.

#### Phân loại dữ liệu

- **Dữ liệu có cấu trúc:** Có thể lưu trữ theo lược đồ xác định rõ, chẳng hạn trong cơ sở dữ liệu; nhiều trường hợp có thể biểu diễn thành bảng gồm hàng và cột. Ví dụ: bảng tính Excel và cơ sở dữ liệu SQL.
- **Dữ liệu phi cấu trúc:** Không có cấu trúc dễ nhận dạng nên không thể tổ chức theo cách thông thường trong cơ sở dữ liệu quan hệ dưới dạng hàng và cột. Dữ liệu không tuân theo một định dạng, trình tự, ngữ nghĩa hoặc quy tắc cụ thể. Ví dụ: hình ảnh và video.
- **Dữ liệu bán cấu trúc:** Không được lưu trữ đơn thuần dưới dạng hàng và cột như trong cơ sở dữ liệu quan hệ. Dữ liệu chứa thẻ, phần tử hoặc siêu dữ liệu để nhóm và sắp xếp theo hệ thống phân cấp. Ví dụ: tệp XML và JSON.

#### Đặc trưng của Big Data: mô hình 5V

- **Volume (khối lượng):** Lượng dữ liệu cần xử lý rất lớn, có thể từ hàng chục terabyte (TB) đến hàng trăm petabyte (PB).
- **Velocity (tốc độ):** Dữ liệu được tạo ra và truyền đến hệ thống rất nhanh, thậm chí trong thời gian thực.
- **Variety (đa dạng):** Dữ liệu có nhiều dạng, từ dữ liệu có cấu trúc đến phi cấu trúc, như văn bản, âm thanh và video. Một số dạng cần xử lý bổ sung để rút ra ý nghĩa và hỗ trợ siêu dữ liệu.
- **Veracity (độ tin cậy):** Mức độ chính xác, đáng tin cậy, chất lượng và tính toàn vẹn của dữ liệu.
- **Value (giá trị):** Giá trị doanh nghiệp có thể khai thác khi chuyển dữ liệu thành thông tin hữu ích.

#### Vai trò của Big Data trong doanh nghiệp

- **Hiểu biết sâu hơn (better insights):** Khi có nhiều dữ liệu hơn, tổ chức có thể phân tích sâu và khám phá những thông tin giá trị trước đây khó nhận thấy.
- **Ra quyết định (decision-making):** Những hiểu biết này giúp doanh nghiệp đưa ra quyết định dựa trên dữ liệu, từ đó dự đoán xu hướng và kết quả chính xác hơn.
- **Cá nhân hóa trải nghiệm khách hàng (personalized customer experiences):** Big Data giúp xây dựng hồ sơ khách hàng chi tiết bằng cách kết hợp dữ liệu mua hàng, dữ liệu nhân khẩu học, hành vi trên mạng xã hội và tương tác với các chiến dịch marketing. Từ đó, doanh nghiệp có thể cá nhân hóa trải nghiệm khách hàng.
- **Tăng hiệu quả vận hành (improved operational efficiency):** Phân tích dữ liệu từ nhiều bộ phận giúp phát hiện điểm nghẽn, tối ưu quy trình, giảm lỗi và tiết kiệm chi phí.

#### Thách thức khi xử lý Big Data

- **Khối lượng dữ liệu lớn:** Dữ liệu tăng rất nhanh, gần như gấp đôi sau mỗi vài năm, gây khó khăn cho việc lưu trữ và quản lý.
- **Xử lý và làm sạch dữ liệu (data curation):** Dữ liệu chỉ có giá trị khi được xử lý và tổ chức hợp lý. Data Scientist thường dành 50–80% thời gian để chuẩn bị dữ liệu.
- **Bảo mật và quyền riêng tư:** Cần mã hóa dữ liệu, phân quyền truy cập và tuân thủ các quy định như GDPR.
- **Văn hóa dữ liệu (data-driven culture):** Có dữ liệu nhưng không sử dụng thì dữ liệu không tạo ra giá trị. Doanh nghiệp cần thay đổi tư duy, đào tạo nhân sự và áp dụng công cụ phân tích.
- **Công nghệ thay đổi nhanh:** Từ Apache Hadoop đến Apache Spark và các hệ thống kết hợp nhiều công nghệ, việc theo kịp thay đổi đòi hỏi cập nhật liên tục.

## 2. Các nền tảng lưu trữ dữ liệu

### 2.1. Data Lake (hồ dữ liệu) — “Cái phễu hứng mọi thứ”

**Khái niệm:** Data Lake là kho lưu trữ tập trung, cho phép lưu dữ liệu ở mọi quy mô: dữ liệu có cấu trúc như bảng SQL, bán cấu trúc như JSON và XML, cũng như phi cấu trúc như hình ảnh, video, tệp âm thanh và PDF.

#### Công cụ thường dùng

- **Lớp lưu trữ (storage):**
    - **Amazon S3:** Dịch vụ lưu trữ đối tượng phổ biến trên đám mây.
    - **Azure Data Lake Storage (ADLS Gen2):** Dịch vụ trong hệ sinh thái Microsoft, có không gian tên phân cấp (*hierarchical namespace*) hỗ trợ các tác vụ Big Data.
    - **Google Cloud Storage (GCS):** Dịch vụ lưu trữ của Google Cloud.
- **Lớp xử lý dữ liệu:**
    - **Apache Spark:** Công cụ xử lý dữ liệu phân tán phổ biến.
    - **Databricks:** Nền tảng phân tích hợp nhất dựa trên Spark.
    - **AWS Glue:** Dịch vụ ETL không cần quản lý máy chủ của Amazon.

#### Đặc điểm cốt lõi

- **Lưu trữ dữ liệu thô:** Dữ liệu được giữ nguyên từ nguồn. Nếu sau này cần thông tin từng định loại bỏ trong quá trình ETL, bạn vẫn có thể quay lại Data Lake để lấy.
- **Khả năng mở rộng lớn:** Data Lake thường được xây dựng trên các hệ thống lưu trữ đám mây như Amazon S3, Google Cloud Storage và Azure Data Lake Storage. Chi phí lưu trữ thấp cho phép lưu lượng dữ liệu ở quy mô petabyte.
- **Đa dạng kiểu dữ liệu:** Có thể tiếp nhận log hệ thống, dữ liệu cảm biến IoT và tệp tài liệu nghiệp vụ.
- **Tách biệt lưu trữ và tính toán:** Dữ liệu được lưu ở một nơi; khi cần xử lý mới sử dụng cụm máy tính toán như Spark hoặc Presto. Sau khi xử lý, có thể dừng cụm máy mà vẫn giữ dữ liệu, qua đó tối ưu chi phí.

#### Đối tượng sử dụng chính

- **Data Scientist:** Sử dụng dữ liệu thô để xây dựng mô hình học máy (Machine Learning) hoặc tìm mối tương quan ẩn mà dữ liệu đã xử lý trong Data Warehouse có thể không còn giữ lại.
- **Data Engineer:** Dùng Data Lake làm vùng đệm (*staging area*) cho quy trình ELT: lấy dữ liệu từ hồ, làm sạch rồi đưa vào Data Warehouse cho người dùng cuối.
- **Data Analyst:** Sử dụng SQL hoặc công cụ như Spark để khám phá dữ liệu trước khi lập báo cáo chính thức.

#### Hạn chế

- **Nguy cơ thành “Data Swamp” (đầm lầy dữ liệu):** Nếu không kiểm soát chặt lược đồ, phân loại dữ liệu, gắn siêu dữ liệu (*metadata*), xác định quyền sở hữu và kiểm soát chất lượng đầu vào, dữ liệu sẽ khó quản lý.
- **Thiếu giao dịch ACID:** Data Lake truyền thống không tự cung cấp đầy đủ Atomicity, Consistency, Isolation và Durability.
- **Thiếu phiên bản dữ liệu:** Không có sẵn cơ chế truy vấn các phiên bản dữ liệu trong quá khứ.
- **Truy vấn chậm hơn Data Warehouse:** Hệ thống chủ yếu phục vụ lưu trữ, chưa tối ưu truy vấn như cơ sở dữ liệu.

### 2.2. Data Warehouse (kho dữ liệu) — “Thư viện đã phân loại”

**Khái niệm:** Data Warehouse là hệ thống lưu trữ dữ liệu trung tâm, tích hợp dữ liệu từ nhiều nguồn như cơ sở dữ liệu giao dịch, ứng dụng CRM và ERP để phục vụ phân tích, báo cáo.

**Công cụ thường dùng:** Snowflake, Google BigQuery và Amazon Redshift.

#### Đặc điểm cốt lõi

- **Hướng chủ đề (subject-oriented):** Dữ liệu được tổ chức quanh các chủ đề chính của doanh nghiệp như khách hàng, bán hàng và sản phẩm.
- **Tích hợp (integrated):** Dữ liệu từ nhiều nguồn được làm sạch và chuẩn hóa về định dạng thống nhất trước khi nạp vào kho. Ví dụ, có thể chuyển mọi đơn vị tiền tệ về USD, hoặc thống nhất hai tên cột `cust_id` và `customer_id`.
- **Biến đổi theo thời gian (time-variant):** Kho thường lưu lịch sử lâu dài, khoảng 5–10 năm, để so sánh và phân tích xu hướng. Đây là một điểm khác biệt với hệ thống xử lý giao dịch OLTP như MySQL.
- **Không biến động (non-volatile):** Dữ liệu đã nạp thường ít bị người dùng cuối thay đổi hoặc xóa; khi có thay đổi, dữ liệu mới thường được thêm bên cạnh dữ liệu cũ. Dữ liệu chủ yếu được đọc để phân tích.

#### Hạn chế

- Xử lý tốt dữ liệu có cấu trúc nhưng không phù hợp với các tệp JSON, video hoặc hình ảnh.
- Vì chủ yếu chứa dữ liệu có cấu trúc, Data Warehouse hạn chế với những bài toán AI/ML cần nhiều loại dữ liệu; hệ thống phù hợp với công việc của Data Analyst.
- Tối ưu truy vấn tốt nhưng chi phí thường cao hơn Data Lake.

#### Đối tượng sử dụng chính

- **Data Analyst:** Dùng SQL để truy vấn dữ liệu, tạo báo cáo và bảng điều khiển (*dashboard*) theo dõi hiệu suất kinh doanh.
- **Kỹ sư BI:** Thiết kế, duy trì hệ thống báo cáo tự động và bảo đảm dữ liệu hiển thị chính xác cho lãnh đạo.
- **Data Scientist:** Sử dụng dữ liệu đã làm sạch để huấn luyện mô hình học máy và dự báo xu hướng.
- **Lãnh đạo doanh nghiệp:** Dựa vào báo cáo từ Data Warehouse để đưa ra chiến lược kinh doanh dựa trên dữ liệu.

### 2.3. Data Mart (chợ dữ liệu) — “Cửa hàng tiện lợi”

**Khái niệm:** Trong kiến trúc kho dữ liệu truyền thống, Data Mart là kho dữ liệu tập trung vào một chủ đề hoặc một đơn vị kinh doanh cụ thể trong tổ chức.

#### Đặc điểm cốt lõi

- **Phạm vi tập trung:** Khác với Data Warehouse bao phủ toàn doanh nghiệp, Data Mart chỉ chứa dữ liệu của một lĩnh vực như bán hàng, tài chính hoặc marketing.
- **Kích thước nhỏ gọn:** Vì chỉ chứa dữ liệu chuyên biệt, Data Mart thường nhỏ hơn kho dữ liệu tổng, giúp truy vấn nhanh hơn.
- **Cấu trúc dữ liệu tối ưu:** Dữ liệu thường được mô hình hóa theo dạng dễ hiểu với người dùng cuối, chẳng hạn mô hình ngôi sao (*Star Schema*), để phục vụ trực tiếp công cụ BI (*Business Intelligence*).

#### Ví dụ về người dùng

- **Data Analyst:** Truy cập nhanh dữ liệu sạch, đã chuyển đổi để tạo báo cáo và biểu đồ phục vụ kinh doanh.
- **Các phòng ban:** Bộ phận Marketing theo dõi chiến dịch; bộ phận Tài chính đối soát doanh thu mà không phải lọc hàng tỷ bản ghi không liên quan từ phòng ban khác.
- **Nhà quản lý và lãnh đạo:** Theo dõi nhanh các chỉ số KPI để ra quyết định kịp thời mà không cần chờ truy vấn phức tạp trên kho dữ liệu tổng.

Có thể hình dung **Data Lake** là một hồ lớn chứa nhiều nguồn nước, thậm chí cả cá; **Data Warehouse** là nhà máy xử lý và bể chứa nước trung tâm. Hệ thống ống dẫn từ hồ đến nhà máy là **Data Pipeline** với quy trình ETL/ELT. Nước trong bể được chia theo từng mục đích sử dụng, tương tự các **Data Mart** phục vụ những nhu cầu riêng.

## 3. So sánh Data Lake, Data Warehouse và Data Mart

| Tiêu chí | Data Lake | Data Warehouse | Data Mart |
| --- | --- | --- | --- |
| **Định nghĩa** | Nơi lưu trữ dữ liệu thô. | Kho dữ liệu tập trung, đã xử lý và có cấu trúc. | Một phần của Data Warehouse phục vụ bộ phận cụ thể. |
| **Loại dữ liệu** | Có cấu trúc, phi cấu trúc và bán cấu trúc. | Có cấu trúc (bảng). | Có cấu trúc. |
| **Xử lý lược đồ** | *Schema-on-read*: xử lý sau khi lưu. | *Schema-on-write*: xử lý trước khi lưu. | *Schema-on-write*. |
| **Chi phí lưu trữ** | Thấp nhờ dịch vụ lưu trữ đối tượng như S3. | Cao hơn do tối ưu truy vấn. | Trung bình. |
| **Hiệu năng** | Truy vấn chậm hơn. | Truy vấn nhanh. | Truy vấn rất nhanh. |
| **Ứng dụng** | Log hệ thống, IoT, video. | Báo cáo tài chính, dashboard. | Báo cáo bán hàng cho một phòng ban. |
| **Trường hợp sử dụng tiêu biểu** | Phân tích dữ liệu lớn, ML/NLP, khám phá dữ liệu linh hoạt, streaming (IoT, log). | Báo cáo doanh nghiệp, BI, dashboard, phân tích dữ liệu lịch sử. | Người dùng nghiệp vụ và các phòng ban. |

## 4. Xu hướng tương lai và kết luận

### Data Lakehouse

Một xu hướng trong kiến trúc dữ liệu là **Data Lakehouse**. Mô hình này được Databricks giới thiệu như sự kết hợp giữa Data Warehouse và Data Lake, xuất phát từ ưu điểm và hạn chế của từng mô hình:

- Data Warehouse lưu dữ liệu theo cấu trúc rõ ràng, nhưng dữ liệu thường tập trung vào một số dạng như số liệu và bảng biểu.
- Trong bối cảnh LLM và AI phát triển, việc huấn luyện mô hình đòi hỏi nhiều loại dữ liệu, không thể chỉ dựa vào một dạng duy nhất.
- Data Lake lưu được nhiều loại dữ liệu như một chiếc phễu, nhưng dữ liệu thiếu cấu trúc sẽ khó quản lý. Data Lake truyền thống cũng thiếu độ tin cậy khi chưa có cơ chế kiểm soát ghi và đọc đồng thời (*concurrency control*).

Data Lakehouse tận dụng tính linh hoạt của Data Lake, đồng thời bổ sung cấu trúc và độ tin cậy như Data Warehouse. Các công nghệ tiêu biểu gồm **Delta Lake** và **Apache Iceberg**. Delta Lake dùng tệp `.parquet` để lưu dữ liệu của bảng Delta. Một bảng Delta có hai thành phần chính:

- **Tệp Parquet:** Chứa dữ liệu dưới định dạng `.parquet`.
- **Transaction log:** Lưu lại các thay đổi.

#### Tệp Parquet là gì?

**Apache Parquet** là định dạng tệp lưu dữ liệu dạng bảng, thường dùng trong hệ thống Big Data. Parquet lưu dữ liệu theo cột (*columnar storage*) thay vì theo hàng. Đây là tệp nhị phân, không thể đọc trực tiếp bằng mắt thường; cần dùng công cụ, chẳng hạn Python, để đọc.

Khi cập nhật dữ liệu, không thể sửa trực tiếp nội dung một tệp Parquet. Delta Lake tạo tệp Parquet mới và đánh dấu trong log rằng tệp cũ không còn được sử dụng. Nhờ đó, hệ thống quản lý được các phiên bản dữ liệu.

Data Lakehouse cũng giúp mô hình AI/LLM truy cập dữ liệu trực tiếp mà không bị khóa vào một nền tảng. Với Data Warehouse, dữ liệu nằm trong cơ sở dữ liệu; để dùng bằng Python, người dùng thường phải truy vấn, xuất ra tệp rồi nạp lại, gây chậm và tốn chi phí. Với dữ liệu lưu trong tệp Parquet, có thể đọc bằng Python, Spark hoặc công cụ phù hợp khác.

#### Giao dịch ACID trong Data Lakehouse

Data Lakehouse còn hỗ trợ các tính chất ACID:

- **A — Atomicity (tính nguyên tử):** Giao dịch hoặc thành công toàn bộ hoặc không có hiệu lực. Ví dụ, nếu quá trình ghi thất bại giữa chừng và log cuối cùng chưa được ghi, lần ghi đó được xem như chưa từng xảy ra.
- **C — Consistency (tính nhất quán):** Dữ liệu tuân theo quy tắc và lược đồ. Ví dụ, cột `age` yêu cầu số thì không thể chèn chuỗi vào cột này.
- **I — Isolation (tính cô lập):** Nhiều người ghi cùng lúc không làm các giao dịch ảnh hưởng lẫn nhau. Ví dụ, bạn đang ghi dựa trên phiên bản 10, nhưng một người khác đã ghi và tạo phiên bản 11; lần ghi dựa trên phiên bản 10 sẽ thất bại và cần thử lại.
- **D — Durability (tính bền vững):** Dữ liệu đã ghi thành công sẽ không bị mất.

### Tóm tắt

- **Data Lake (hồ dữ liệu):** Lưu dữ liệu thô, phục vụ lưu trữ chi phí thấp và các mô hình AI/Machine Learning phức tạp. Đặc điểm cốt lõi là khả năng mở rộng lớn và tách biệt lưu trữ với tính toán.
- **Data Warehouse (kho dữ liệu):** Lưu dữ liệu đã làm sạch, chuẩn hóa; có các đặc điểm hướng chủ đề (*subject-oriented*), tích hợp (*integrated*), biến đổi theo thời gian (*time-variant*) và không biến động (*non-volatile*).
- **Data Mart (chợ dữ liệu):** Phần dữ liệu nhỏ trích từ Data Warehouse hoặc trực tiếp từ hệ thống nguồn, phục vụ phân tích nhanh cho từng phòng ban như Marketing, Tài chính. Nhờ kích thước nhỏ, cấu trúc dữ liệu có thể được tối ưu theo nhu cầu sử dụng.
- **Data Lakehouse:** Kết hợp ưu điểm của Data Lake và Data Warehouse, cho phép lưu dữ liệu linh hoạt trong định dạng tệp mở như Parquet, đồng thời hỗ trợ quản lý và truy vấn như một hệ cơ sở dữ liệu.

---

## Lời kết

Không có một nơi lưu trữ phù hợp cho mọi loại dữ liệu và mọi người dùng. Khi thiết kế nền tảng dữ liệu, hãy bắt đầu từ dạng dữ liệu cần lưu, cách dữ liệu được xử lý và nhu cầu truy vấn của từng nhóm: khám phá dữ liệu thô, lập báo cáo chung hay phân tích cho một phòng ban. Từ đó, bạn sẽ thấy Data Lake, Data Warehouse, Data Mart và Data Lakehouse có thể đảm nhận những vai trò khác nhau trong cùng một kiến trúc.

<figure class="airflow-closing-comic">
  <img
    src="../../assets/images/ware_lake_lw/ending.png"
    alt="Truyện tranh Shin giới thiệu các mô hình lưu trữ dữ liệu, cảm ơn người đọc và hẹn gặp ở bài viết sau"
    loading="lazy"
  >
  <figcaption>
    <span>LỜI KẾT</span>
    <div>
      <strong>Cảm ơn bạn đã đọc đến cuối!</strong>
      <p>Hẹn gặp lại ở những bài viết tiếp theo.</p>
    </div>
  </figcaption>
</figure>

<footer class="airflow-article-end ware-lake-article-end">
  <div>
    <span>BEHIND THE PIPELINE / 006</span>
    <strong>Hiểu hệ thống,<br>không chỉ cú pháp.</strong>
  </div>
  <a href="../../">Trở về thư viện <span aria-hidden="true">→</span></a>
</footer>
