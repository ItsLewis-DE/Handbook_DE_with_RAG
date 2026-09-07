Sơ đồ phân cấp từ cao đến thấp của postgres
$$\text{Database Cluster (Instance)} \rightarrow \text{Database (Catalog)} \rightarrow \text{Schema (Namespace)} \rightarrow \text{SQL Objects (Tables, Views, Indexes,...)}$$.
Database Cluster (Instance): là một tiến trình PostgresSql chạy trên máy chủ vật lí hoặc container, mỗi database cluster sẽ có một vùng nhớ chung (shared_buffers) trên RAM và một thư mục dữ liệu (PgData) trên ổ đĩa. Các dữ liệu của các database sẽ được lưu trong folder base/ 
shared_buffers là gì? là dung lượng RAm mà một instance sẽ sử dụng để làm bộ nhớ đệm, có mục đích chính là giảm thiểu việc đọc/ghi xuống ổ đĩa.
Bộ đệm này được chia thành hàng ngàn khối nhỏ bằng nhau, mỗi khối đúng 8KB (bằng kích thước của một Data Page trên đĩa).
Dataabse: trong một database cluster sẽ có thể chứa nhiều database, các database này không thể truy vấn chéo nhau được (trừ khi bạn sử dụng các công cụ bên ngoài), mỗi database sẽ có một thư mục riêng của mình nằm trong thư mục PGDATA của database cluster.
Schema: nằm trong database, một database có thể có nhiều schema, trái ngược với database thì các bảng trong schema khác nhau có thể truy vấn lẫn nhau được. Về vật lí, schema không có một nơi để lưu trữ riêng biệt, mà mọi Schema trong cùng một Database đều nằm chung một chỗ ngay tại thư mục:
PGDATA/base/<db_oid>/ #note db_oid là mã được hệ thống sỉnh ra mỗi khi bạn gọi CREATE DATABASe

HÌnh ảnh minh họa một thư mục PGDATA: 
PGDATA/                          <-- Thư mục gốc của toàn bộ Cluster (Instance)
├── pg_wal/                      <-- Chứa các file Write-Ahead Log (WAL)
├── pg_xact/                     <-- Chứa trạng thái commit giao dịch (CLOG)
├── global/                      <-- Chứa bảng hệ thống chung toàn cluster (pg_database, pg_authid,...)
└── base/                        <-- Thư mục chứa dữ liệu của TẤT CẢ các Database
    ├── 1/                       <-- Thư mục của Database 'template1' (OID = 1)
    ├── 13745/                   <-- Thư mục của Database 'postgres' (OID = 13745)
    └── 16384/                   <-- Thư mục của Database 'my_sales_db' do bạn tạo (OID = 16384)
        ├── 16388                <-- Tệp chứa các trang dữ liệu (Heap) của Table A
        ├── 16388_fsm            <-- Bản đồ không gian trống (Free Space Map) của Table A
        └── 16390                <-- Tệp chứa chỉ mục B-Tree (Index) của Table A


Tại sao hệ thống phải thiết kế nhiều schema trong database để làm gì?
    - Nếu nhiều người sử dụng chung 1 database, việc chia thành các schema riêng biệt giúp tránh việc trùng tên bảng của nhau. Ví dụ schema A có bảng là order, schema B có bảng cũng là order. Nhưng lúc này hệ thống vẫn chấp nhận do bảng cùng tên nhưng nằm ở schema khác nhau.
    - Việc đểnhiều người sử dunngj chung một database sẽ giúp tiết kiệm tài nguyên hơn là để mỗi người sử dụng database riêng. 
    - Thay vì phải cấp quyền cho từng bảng (sẽ là một việc rất khó khăn khi hệ thống phình to lên), khi sử dụng schema ta chỉ cần gắn quyền của một role cho schema đó.

Ràng buộc toàn vẹn (Integrity Constraints) là tập hợp các quy tắc logic nhằm đảm bảo dữ liệu luôn chính xác, hợp lệ và nhất quán. Ràng buộc không chỉ là quy tắc nghiệp vụ mà nó còn là công cụ để Query Optimizer hiểu rõ phân phối dữ liệu.