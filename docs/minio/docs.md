---
title: MinIO và Object Storage
description: "Tổng quan về MinIO, vai trò trong Data Pipeline và các khái niệm cơ bản của Object Storage."
lang: vi
hide:
  - navigation
---

<header class="airflow-article-hero storage-article-hero minio-article-hero">
  <div class="airflow-article-hero__eyebrow">
    <a href="../../">BEHIND THE PIPELINE</a>
    <span>ARTICLE / 007</span>
  </div>
  <h1>MinIO<br><em>&amp; Object Storage</em></h1>
  <p class="airflow-article-hero__dek">
    Tổng quan về MinIO, vai trò trong Data Pipeline và các khái niệm
    Bucket, Object, Object Key, Prefix.
  </p>
  <div class="airflow-article-hero__meta" aria-label="Thông tin bài viết">
    <span>DATA ARCHITECTURE</span>
    <span>EDITION 07 · 2026</span>
  </div>
</header>

## 1. MinIO là gì?

**MinIO** là một hệ thống lưu trữ đối tượng (**Object Storage**) hiệu năng cao, tương thích với Amazon S3 API. Hệ thống được thiết kế để lưu trữ và quản lý lượng lớn dữ liệu phi cấu trúc như hình ảnh, video, tệp log, JSON, CSV hay Parquet, và có thể được sử dụng làm nền tảng lưu trữ cho Data Lake.

MinIO được thành lập vào năm **2014 tại Thung lũng Silicon (Mỹ)** bởi Anand Babu Periasamy, Garima Kapoor và Harshavardhana, trong bối cảnh lượng dữ liệu phi cấu trúc như hình ảnh, video và tài liệu ngày càng tăng mạnh. Khi đó, Amazon S3 đã trở thành một dịch vụ lưu trữ đối tượng phổ biến, nhưng các tổ chức vẫn có nhu cầu xây dựng hệ thống lưu trữ riêng mà không phụ thuộc hoàn toàn vào nhà cung cấp đám mây.

Xuất phát từ nhu cầu ấy, MinIO chính thức được giới thiệu vào năm **2015** như một giải pháp Object Storage mã nguồn mở, tương thích với Amazon S3 API, giúp các nhà phát triển tự triển khai và quản lý hệ thống lưu trữ dữ liệu với khả năng mở rộng linh hoạt.

## 2. Vai trò của MinIO trong Data Pipeline

Trong một **Data Pipeline**, MinIO thường đóng vai trò là **lớp lưu trữ dữ liệu (Storage Layer)**, nơi tiếp nhận và lưu trữ dữ liệu được thu thập từ nhiều nguồn như API, cơ sở dữ liệu, tệp log hoặc các hệ thống bên ngoài.

Dữ liệu sau khi được trích xuất (**Extract**) có thể được đưa vào MinIO dưới dạng các tệp CSV, JSON hoặc Parquet để lưu trữ trước khi xử lý. Tiếp theo, các công cụ xử lý dữ liệu như **Apache Spark** có thể đọc trực tiếp dữ liệu từ MinIO thông qua giao thức tương thích S3, thực hiện các tác vụ làm sạch, biến đổi (**Transform**) và ghi kết quả trở lại MinIO hoặc nạp vào Data Warehouse để phục vụ phân tích.

<figure class="minio-article-figure">
  <a href="../../assets/images/minio/Hand-Drawn%20Data%20Pipeline%20Flowchart.png" title="Xem ảnh kích thước gốc">
    <img src="../../assets/images/minio/Hand-Drawn%20Data%20Pipeline%20Flowchart.png" alt="Luồng dữ liệu từ API, cơ sở dữ liệu và tệp log qua Extract, MinIO và Spark đến MinIO hoặc Data Warehouse" loading="lazy" width="1774" height="887">
  </a>
  <figcaption>Hình 2. MinIO lưu trữ dữ liệu sau bước Extract; Spark đọc và xử lý dữ liệu, sau đó ghi kết quả trở lại MinIO hoặc nạp vào Data Warehouse.</figcaption>
</figure>

## 3. Mô hình lưu trữ Object Storage

Trong các hệ thống máy tính truyền thống, hệ điều hành thường lưu trữ dữ liệu bằng **Block Storage**, nơi dữ liệu được quản lý dưới dạng các khối lưu trữ. Khi làm việc với khối lượng dữ liệu phi cấu trúc hoặc bán cấu trúc rất lớn, đặc biệt trong môi trường Cloud Computing và Data Engineering, **Object Storage** trở thành một mô hình lưu trữ quan trọng.

### Thành phần của một object

Object Storage lưu trữ dữ liệu dưới dạng các đơn vị độc lập gọi là **object**. Mỗi object bao gồm:

- **Data:** Nội dung thực tế như hình ảnh, video, tệp CSV, JSON, Parquet hoặc dữ liệu nhị phân.
- **Metadata:** Thông tin mô tả object như `Content-Type`, kích thước, thời điểm chỉnh sửa hoặc metadata do người dùng định nghĩa.
- **Object Key:** Tên định danh dùng để xác định và truy xuất object trong một bucket.

### Ví dụ trong MinIO

Một object `customers.json` được lưu trong bucket `data-lake`:

```text
Bucket: data-lake
Object: customers.json

OBJECT KEY
raw/2026/customers.json

METADATA
Content-Type: application/json

DATA
{"customer_id": 101, "name": "An"}
```

### Cấu trúc logic qua Prefix

Object Storage sử dụng không gian tên phẳng (**Flat Namespace**) để quản lý các object, thay vì tổ chức chúng theo cấu trúc thư mục phân cấp như hệ thống tệp truyền thống. Ví dụ, với Object Key `raw/2026/customers.csv`, các thành phần `raw` và `2026` chỉ đóng vai trò mô phỏng thư mục thông qua **Prefix (tiền tố)** và ký tự phân cách `/`. Về mặt logic, đây là một Object Key hoàn chỉnh, không tồn tại mối quan hệ thư mục cha–con thực sự.

## 4. Các khái niệm cơ bản trong MinIO

| Khái niệm | Mô tả | Ví dụ |
| --- | --- | --- |
| **Bucket** | Nơi chứa và tổ chức các object. | `data-lake` |
| **Object** | Đơn vị dữ liệu cơ bản trong MinIO, tương tự một tệp trên máy tính. | `customers.json` |
| **Object Key** | Định danh của một object trong phạm vi một bucket. | `raw/2026/data.parquet` |
| **Prefix** | Chuỗi ký tự nằm ở đầu object key, dùng để mô phỏng cấu trúc thư mục. | `raw/2026/` hoặc `raw/` |
| **Node** | Một máy chủ chạy MinIO Server. | `server1` |
| **Drive** | Các ổ đĩa mà MinIO dùng để lưu trữ dữ liệu. | Ổ cứng 4 TB trên mỗi server. |
| **Erasure Set** | Tập hợp gồm **4–16 ổ đĩa** nằm rải rác trên nhiều máy chủ. Khi tải dữ liệu lên, MinIO chạy thuật toán băm trên object key để xác định Erasure Set lưu trữ đối tượng dữ liệu đó. | Erasure Set có 16 ổ đĩa. |
| **Server Pool** | Tập hợp gồm các máy chủ và ổ đĩa giống hệt nhau. Một cụm MinIO có thể gồm nhiều Server Pool hợp lại. Khi cụm sắp hết dung lượng, có thể bổ sung một Server Pool để mở rộng. | Server Pool 1 gồm 4 server, mỗi server gắn 4 ổ cứng 4 TB. |

### Ví dụ mở rộng Server Pool

#### Giai đoạn 1: Triển khai Server Pool 1 (năm 2024)

Một cụm MinIO được triển khai để lưu trữ với cấu hình:

- **Số lượng máy:** 4 server (`server1`, `server2`, `server3`, `server4`).
- **Ổ đĩa:** Mỗi server gắn 4 ổ cứng 4 TB.
- **Tổng số đĩa:** 16 đĩa, tương đương 64 TB thô.

Tất cả 4 máy này hợp thành **Server Pool 1**.

#### Giai đoạn 2: Mở rộng khi cụm gần đầy dung lượng (năm 2026)

Sau 2 năm, cụm đã sử dụng 95% dung lượng và cần mở rộng.

Lúc này, trên thị trường đã có ổ 16 TB. Thay vì tiếp tục mua ổ 4 TB, có thể triển khai một nhóm máy mới với dung lượng lớn hơn để tạo thành **Server Pool 2**:

- **Số lượng máy mới:** 4 server (`server5`, `server6`, `server7`, `server8`).
- **Ổ đĩa mới:** Mỗi server gắn 4 ổ cứng 16 TB, lớn gấp 4 lần ổ cũ.
- **Tổng số đĩa mới:** 16 đĩa, tương đương 256 TB thô.

4 máy mới này hợp thành **Server Pool 2**.

Sau đó, chỉ cần thêm cấu hình Server Pool mới vào cụm MinIO, hệ thống sẽ tự động gộp dung lượng và hoạt động liền mạch trên cả hai pool.

## 5. Kiến trúc của MinIO

MinIO sử dụng **kiến trúc đối xứng hoàn toàn**. Trong toàn bộ cụm (cluster), mọi node và drive đều có vai trò, trách nhiệm và cấu trúc phần mềm giống hệt nhau, không có sự phân cấp thứ bậc.

Khác với các hệ thống lưu trữ phân tán khác, MinIO không sử dụng cơ sở dữ liệu bên ngoài để lưu trữ metadata. Metadata của từng object được ghi vào tệp nhị phân `xl.meta` và lưu trên các ổ đĩa bên cạnh dữ liệu.

## 6. Cơ chế lưu trữ của MinIO

### Cấu trúc thư mục trên ổ đĩa

Dưới tầng hệ điều hành, MinIO lưu trữ dữ liệu dưới dạng cấu trúc thư mục. Mỗi bucket tương ứng với một thư mục cùng tên ở thư mục gốc của ổ đĩa. Ví dụ, với tệp `raw-data/metrics.parquet`, cấu trúc bên dưới ổ đĩa như sau:

```text
/mnt/disk-1/
└── my-bucket/                         # Tương đương Bucket "my-bucket"
    └── raw-data/                      # Prefix (thư mục ảo trong S3)
        └── metrics.parquet/           # Object name được biểu diễn thành thư mục
            ├── xl.meta                # Metadata, thông tin versioning, checksum
            └── part.1
```

### Phân bố dữ liệu trong Erasure Set

Với mỗi object key, ví dụ `lake/orders.parquet`, MinIO tạo một thư mục con tương ứng trên tất cả các đĩa thuộc Erasure Set. Tệp `xl.meta` được lưu trong thư mục này.

Khi tải một tệp lên `lake/orders.parquet`, MinIO băm object key để xác định Erasure Set lưu trữ object đó. Sau đó, hệ thống sử dụng kỹ thuật **Reed–Solomon Erasure Coding** để chia object thành `K` mảnh dữ liệu (**Data Shards**) và `M` mảnh mã sửa lỗi.

Đối với một object thông thường, mỗi drive giữ một shard. Tất cả các mảnh này không được lưu chung trong một drive vì nếu drive đó bị hỏng, toàn bộ các mảnh dữ liệu sẽ bị mất. Mỗi drive lưu metadata của object trong tệp `xl.meta` riêng. Kỹ thuật Reed–Solomon Erasure Coding được trình bày kỹ hơn ở phần bên dưới.

<figure class="minio-article-figure">
  <a href="../../assets/images/minio/MinIO%20Erasure%20Coding%20Drive%20Map.png" title="Xem ảnh kích thước gốc">
    <img src="../../assets/images/minio/MinIO%20Erasure%20Coding%20Drive%20Map.png" alt="Một object được chia thành 4 mảnh dữ liệu và 4 mảnh parity, phân bố trên 8 ổ đĩa trong Erasure Set; mỗi ổ lưu metadata trong tệp xl.meta" loading="lazy" width="1536" height="1024">
  </a>
  <figcaption>Hình 3. Ví dụ Erasure Set gồm 8 ổ đĩa với K = 4 và M = 4: mỗi ổ giữ một mảnh của object cùng metadata trong tệp <code>xl.meta</code>. Prefix là cấu trúc logic trong S3, còn phần dưới minh họa cách tổ chức trên ổ đĩa vật lý.</figcaption>
</figure>

### Lưu trữ tệp nhỏ

Với các tệp nhỏ, dưới **128 KB – 256 KB**, MinIO không tạo tệp dữ liệu thô `part.1` riêng biệt mà nhúng trực tiếp dữ liệu vào tệp `xl.meta`.

## 7. Cơ chế dự phòng: Erasure Coding (Reed–Solomon)

MinIO sử dụng thuật toán **Reed–Solomon Erasure Coding**. Trong một Erasure Set có `N` ổ đĩa:

```text
N = K + M
```

Trong đó:

- **`K`:** Số lượng mảnh dữ liệu thực tế (Data Shards).
- **`M`:** Số lượng mảnh dự phòng (Parity Blocks).

`K + M` mảnh này được ghi đồng thời xuống `N` ổ đĩa vật lý khác nhau trong Erasure Set.

Việc chia thành các mảnh nhằm chống mất mát dữ liệu khi một drive bị hỏng. `M` cũng là số mảnh bất kỳ tối đa mà hệ thống có thể mất trong tổng số `N` mảnh.

### Ví dụ khôi phục dữ liệu

Giả sử Erasure Set có **16 ổ đĩa**, cấu hình `K = 12` và `M = 4`:

1. Một tệp 120 MB được chia thành 12 mảnh nhỏ, mỗi mảnh 10 MB.
2. Hệ thống tính thêm 4 mảnh Parity, mỗi mảnh 10 MB.
3. Nếu 4 ổ đĩa hoặc 1 máy chủ gặp sự cố cùng lúc, MinIO chỉ cần lấy 12 mảnh còn hoạt động trên các ổ khác để tái tạo trọn vẹn tệp 120 MB ban đầu.

### Read Quorum và Write Quorum

Trong MinIO, thao tác đọc hoặc ghi dữ liệu phải đáp ứng các điều kiện về số lượng ổ đĩa hoạt động:

- **Read Quorum:** Hệ thống cần tối thiểu `K` ổ đĩa còn hoạt động để tái tạo toàn bộ tệp ban đầu và chịu được việc mất tối đa `M` ổ đĩa cùng lúc.
- **Write Quorum:** Yêu cầu tối thiểu `K + 1` ổ đĩa, hoặc `⌈(K + M) / 2⌉` tùy mức cấu hình nghiêm ngặt, hoạt động để chấp nhận thao tác ghi hoặc xóa mới. Điều kiện này giúp tránh hiện tượng não chia đôi.

Ví dụ, phòng A chứa 8 đĩa, phòng B chứa 8 đĩa. Nếu `K = 8`, cả hai bên đều có thể cho phép ghi, dẫn đến tình trạng cùng ghi vào một tệp. Yêu cầu `K + 1` giúp bên có nhiều ổ đĩa hơn trở thành bên được phép ghi.

### Mở rộng dung lượng

Đối với một Erasure Set đang hoạt động, không thể tăng dung lượng bằng cách lắp thêm ổ đĩa hoặc máy chủ đơn lẻ. Vì vậy, MinIO sử dụng khái niệm Server Pool để doanh nghiệp có thể gia tăng khả năng lưu trữ mà không gây downtime.

## 8. Phân phối yêu cầu với Load Balancer

Trong môi trường production, các hệ thống xử lý dữ liệu như Apache Spark hoặc Trino có thể tạo ra lượng lớn yêu cầu đọc/ghi dữ liệu đến MinIO thông qua S3 API. Nếu tất cả các yêu cầu đều được gửi trực tiếp đến một MinIO Node, node đó có nguy cơ trở thành điểm nghẽn về tài nguyên mạng và khả năng xử lý, dù các node khác vẫn tham gia vào quá trình đọc/ghi dữ liệu nội bộ.

Để giải quyết vấn đề này, **Load Balancer** được đặt phía trước MinIO Cluster, cung cấp một S3 Endpoint thống nhất và phân phối các yêu cầu đến những node đang hoạt động. Load Balancer có thể sử dụng các thuật toán như **Round Robin** hoặc **Least Connections** để phân phối lưu lượng, hạn chế tình trạng quá tải tại một node.

Nhờ kiến trúc phân tán không có Master Node (**Masterless**), mọi MinIO Node đều có khả năng tiếp nhận và xử lý yêu cầu từ client. Node nhận yêu cầu sẽ tự phối hợp với các node khác trong cluster khi cần thiết. Điều này giúp hệ thống tận dụng tài nguyên hiệu quả hơn, đồng thời cải thiện khả năng chịu lỗi và tính sẵn sàng của dịch vụ.

<figure class="minio-article-figure">
  <a href="../../assets/images/minio/Distributed%20MinIO%20Cluster%20Architecture.png" title="Xem ảnh kích thước gốc">
    <img src="../../assets/images/minio/Distributed%20MinIO%20Cluster%20Architecture.png" alt="Spark, Trino và các client gửi yêu cầu qua Load Balancer tới các node trong cụm MinIO; các node phối hợp với nhau để đọc và ghi dữ liệu" loading="lazy" width="1774" height="887">
  </a>
  <figcaption>Hình 4. Load Balancer phân phối yêu cầu từ Spark, Trino và các client đến các MinIO Node; mỗi node đều có thể tiếp nhận yêu cầu và phối hợp với các node khác trong cụm.</figcaption>
</figure>

## 9. Ảnh hưởng của nhiều tệp nhỏ đến hiệu năng

MinIO có thể gặp khó khăn khi xử lý quá nhiều tệp nhỏ. Mỗi tệp nhỏ được chia thành `N = K + M` mảnh lưu trên các ổ đĩa. Mỗi ổ đĩa tham gia lưu trữ object phải tạo thêm một tệp `xl.meta`. Số lượng tệp metadata quá lớn có thể làm giảm hiệu năng xử lý của hệ thống.

Trong môi trường Linux, MinIO sử dụng filesystem bên dưới, thường là **XFS**, để lưu trữ dữ liệu. Mỗi thư mục hoặc tệp được tạo mới đều sử dụng một inode. Nếu job Spark xuất ra 1 triệu tệp nhỏ, MinIO sẽ tạo ra ít nhất 2–3 triệu inode trên ổ đĩa.

### Inode là gì?

**Inode** trên hệ điều hành Unix/Linux dùng để lưu trữ toàn bộ siêu dữ liệu (metadata) và vị trí thực tế trên ổ đĩa của một tệp hoặc thư mục. Đối với nhân hệ điều hành Linux, một tệp không được định danh bằng tên tệp mà bằng một số nguyên duy nhất gọi là **Inode Number**.

### Áp lực lên bộ nhớ đệm inode

RAM của Linux có vùng đệm **Inode Cache / Dentry Cache (VFS Cache)** để ghi nhớ vị trí các inode, giúp tra cứu tức thì. Khi số lượng inode tăng lên hàng triệu, RAM không thể chứa hết. Hệ điều hành liên tục phải đẩy inode cũ ra ngoài (**cache eviction**) và đọc inode từ ổ đĩa lên, gây áp lực lên RAM và tăng tải đọc đĩa ngẫu nhiên (**Random Read I/O**).

## 10. Quy trình tìm kiếm và đọc một tệp

### Tiếp nhận yêu cầu

Yêu cầu `GET Object` đi qua Load Balancer và được chuyển đến một MinIO Node bất kỳ. Node này kiểm tra tính hợp lệ của yêu cầu và quyền truy cập theo IAM Policy, sau đó xác định Server Pool và Erasure Set chứa object. Node tiếp nhận yêu cầu phối hợp với các node liên quan thông qua giao thức nội bộ để truy xuất dữ liệu.

Tiếp theo, MinIO tương tác với nhân Linux. Tại từng ổ đĩa vật lý, MinIO gọi xuống nhân Linux để đọc cấu trúc thư mục đại diện cho prefix đó. Hệ điều hành trước tiên kiểm tra cache trên RAM.

### Dentry Cache và Inode Cache

Linux duy trì hai vùng đệm quan trọng trên RAM:

- **Dentry Cache (`dcache`):** Bảng băm lưu các cặp ánh xạ `(Thư mục cha + Tên tệp/thư mục con) → Inode Pointer`.
- **Inode Cache (`icache`):** Lưu nội dung các inode đang hoạt động trong RAM.

#### Trường hợp Cache Hit

Nếu thư mục `orders.parquet` và tệp `xl.meta` vừa được ghi hoặc truy cập gần đây, toàn bộ cấu trúc đường dẫn đã nằm trong RAM. Linux chỉ mất vài nano giây để tra cứu bảng băm `O(1)` trong Dentry Cache. Trong trường hợp này, không có thao tác I/O nào xuống ổ đĩa.

#### Trường hợp Cache Miss

Linux phải đọc thư mục cha từ ổ đĩa. XFS thiết kế 4 cấp độ lưu trữ tùy theo số lượng tệp:

- **Shortform Format:** Khi thư mục chỉ chứa vài tệp, dưới khoảng 20 tệp, toàn bộ danh sách tên tệp và số hiệu inode nằm vừa trong phần mở rộng (data fork) của chính inode thư mục cha. Hệ điều hành chỉ cần đọc inode của thư mục cha để tìm thấy tệp, không tốn thêm block đĩa nào.
- **Block Format:** Khi số lượng tệp tăng lên và không còn vừa trong inode cha, XFS cấp phát một block đĩa duy nhất, thường là 4 KB, để chứa bảng danh bạ. Việc tìm kiếm diễn ra bằng cách quét tuyến tính trong block 4 KB đó.
- **Leaf Format:** Khi kích thước danh mục vượt quá một block đĩa, XFS tách danh bạ thành các block chứa tên tệp thực tế và một block Leaf chứa danh sách mã băm (hash values) của tên tệp, được sắp xếp để tìm kiếm nhị phân.
- **Node / B+Tree Format:** Xuất hiện khi thư mục quá lớn. Khi một thư mục hoặc prefix chứa từ hàng chục nghìn đến hàng triệu tệp con, chẳng hạn một bảng dữ liệu Spark bị lỗi partition, một block Leaf không chứa hết các hash entry. XFS chuyển danh mục sang dạng cây B+Tree nhiều tầng. Việc tìm tên tệp lúc này phải duyệt qua các Root, Intermediate và Leaf Node trên đĩa.

### Đọc metadata và dữ liệu

Trước tiên, hệ thống tìm inode của tệp `xl.meta`. Sau khi xác định được tệp, Linux đọc nội dung và chuyển cho MinIO. MinIO phân tích metadata để xác định Object Version cần đọc, thông tin Erasure Coding và vị trí dữ liệu tương ứng, sau đó yêu cầu hệ điều hành truy xuất thư mục dữ liệu đó.

MinIO dùng cờ `O_DIRECT` khi mở tệp để chỉ thị Linux bỏ qua Page Cache. Dữ liệu được đọc trực tiếp từ ổ đĩa vào user space của MinIO, tránh tình trạng làm tràn cache.

Sau đó, các node gửi danh sách cục bộ thu được về coordinator node. MinIO gộp `K` mảnh thành một đối tượng duy nhất rồi trả về cho client.

## 11. Cơ chế Versioning trong MinIO

**MinIO Versioning** là cơ chế lưu trữ nhiều biến thể của cùng một object trong một bucket. Thay vì ghi đè hoặc xóa vĩnh viễn, MinIO gán cho mỗi lần ghi/xóa một mã định danh duy nhất (**Version ID**) để bảo toàn lịch sử dữ liệu.

### Các trạng thái Versioning

Versioning được quản lý ở cấp độ bucket và có 3 trạng thái:

- **Unversioned (mặc định):** Bucket không quản lý phiên bản. Ghi đè làm mất dữ liệu cũ; xóa là xóa vĩnh viễn.
- **Enabled:** Mọi object thêm mới hoặc ghi đè đều nhận một Version ID dạng UUID, ví dụ `d9426f37-64ec-4fcf-b7d1-04ef963bcfa0`.
- **Suspended (tạm dừng):** Một khi đã bật Versioning, không thể chuyển hoàn toàn về trạng thái Unversioned mà chỉ có thể tạm dừng. Các phiên bản cũ vẫn được giữ nguyên; object mới tải lên có Version ID là `null`, hoặc ghi đè lên phiên bản `null` có sẵn.

### Ghi đè một tệp có sẵn

Hệ thống không xóa hay thay đổi tệp cũ vì object trong MinIO là bất biến. Thay vào đó, hệ thống tạo một thư mục dữ liệu mới cho dữ liệu ghi đè.

Để xác định thư mục dữ liệu cũ và thư mục mới nhất, hệ thống dựa vào tệp `xl.meta`. Bên trong `xl.meta` có một mảng (array) ghi nhận lịch sử của tất cả các version theo thứ tự thời gian. Khi phiên bản mới được ghi xong, bản ghi của nó được đưa lên đầu mảng:

```jsonc
{
  "versions": [
    {
      "version_id": "f47ac10b-2222-...",   // Đỉnh mảng -> Current Version (Mới)
      "created_at": "2026-10-24 10:00:00",
      "data_dir": "f47ac10b-2222-..."       // Trỏ đích danh vào folder mới
    },
    {
      "version_id": "7c8e9b0a-1111-...",   // Bản ghi cũ -> Noncurrent Version
      "created_at": "2026-10-23 09:00:00",
      "data_dir": "7c8e9b0a-1111-..."       // Trỏ vào folder cũ
    }
  ]
}
```

Khi client cần đọc một object, MinIO kiểm tra tệp `xl.meta` và lấy phần tử đầu tiên ở đầu mảng để trả về dữ liệu mới nhất. Chỉ khi người dùng yêu cầu một Version ID cụ thể, hệ thống mới lấy chính xác phiên bản đó.

### Xóa dữ liệu với DELETE

Khi thực hiện lệnh `DELETE`, dữ liệu cũ không bị xóa. MinIO tạo một phiên bản đặc biệt gọi là **Delete Marker** và đặt lên đầu mảng. Khi thấy Delete Marker, MinIO không trả dữ liệu này về cho người dùng. Có thể xóa vĩnh viễn dữ liệu bằng lệnh hard delete.

---

## Lời kết

Từ Bucket, Object đến Erasure Set và Server Pool, các khái niệm trong bài giúp làm rõ cách MinIO tổ chức và mở rộng lưu trữ. Erasure Coding, Load Balancer và Versioning lần lượt thể hiện cách hệ thống bảo vệ dữ liệu, phân phối yêu cầu và quản lý lịch sử phiên bản. Bên cạnh đó, ảnh hưởng của nhiều tệp nhỏ đến inode và bộ nhớ đệm cũng là yếu tố cần lưu ý khi xem xét hiệu năng.

Cảm ơn bạn đã đọc đến cuối! Hy vọng bài viết giúp bạn hiểu rõ hơn về MinIO và vai trò của Object Storage trong Data Pipeline. Hẹn gặp lại ở những bài viết tiếp theo.

<footer class="airflow-article-end minio-article-end">
  <div>
    <span>BEHIND THE PIPELINE / 007</span>
    <strong>Hiểu hệ thống,<br>không chỉ cú pháp.</strong>
  </div>
  <a href="../../">Trở về thư viện <span aria-hidden="true">→</span></a>
</footer>
