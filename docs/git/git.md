## Mở đầu

Bạn thường xuyên sử dụng Git và GitHub, nhưng công việc hằng ngày chỉ xoay quanh vài câu lệnh quen thuộc như `git add .`, `git commit` rồi `git push`? Mọi thứ vẫn ổn cho đến khi cần chỉnh cấu hình, chuyển nhánh hoặc gặp một thông báo lỗi mà bạn chẳng biết bắt đầu xử lý từ đâu. Bạn nhờ AI, chạy theo hướng dẫn và cuối cùng cũng giải quyết được, nhưng vẫn chưa hiểu chuyện gì vừa xảy ra.

Nếu thấy mình trong đó, bài viết này dành cho bạn.

Để hiểu Git, hãy bắt đầu từ những thao tác bạn vẫn làm mỗi ngày: `git add` thực sự lưu những gì? Khi chạy `git commit`, Git ghi lại trạng thái dự án như thế nào? Một branch là gì, và vì sao chuyển nhánh lại có thể làm nội dung trong thư mục thay đổi?

Bài viết sẽ lần lượt giải thích những cơ chế này, từ Working Directory, Staging Area và Repository đến cách Git lưu dữ liệu, liên kết các commit và xác định nhánh hiện tại thông qua HEAD. Khi hiểu điều gì diễn ra phía sau mỗi câu lệnh, bạn sẽ có cơ sở để tự tìm nguyên nhân khi gặp lỗi và hiểu được những hướng dẫn mà mình đang làm theo.

## Git và GitHub là gì?

### Git là gì?

Git là một hệ thống quản lý phiên bản phân tán, giúp bạn ghi lại lịch sử thay đổi của dự án. Nhờ đó, bạn có thể xem lại những phiên bản trước, so sánh nội dung giữa các lần thay đổi và phối hợp làm việc với người khác.

Sở dĩ nó được gọi là phân tán là vì mỗi khi bạn nhân bản (clone) một dự án, máy tính của bạn sẽ lưu trữ một bản sao hoàn chỉnh 100% của toàn bộ dự án — bao gồm tất cả lịch sử commit, các nhánh (branches), nhãn (tags) và cơ sở dữ liệu phiên bản từ ngày đầu tiên — chứ không chỉ là phiên bản mã nguồn mới nhất.

Trong Git, một commit ghi nhận trạng thái của dự án tại một thời điểm, kèm thông tin như tác giả, thông điệp mô tả và liên kết đến commit cha nếu có. Những liên kết này giúp Git lần ngược lại lịch sử của dự án.

### GitHub là gì?

GitHub là một nền tảng lưu trữ các kho Git trực tuyến và hỗ trợ cộng tác phát triển phần mềm. Khi đưa dự án lên GitHub, bạn có thể chia sẻ mã nguồn, theo dõi vấn đề qua Issues và đề xuất thay đổi để mọi người cùng xem xét qua Pull Requests.

Git quản lý phiên bản; GitHub cung cấp nơi lưu trữ kho Git và các công cụ để làm việc cùng nhau. Bạn có thể sử dụng Git trên máy mà không cần có tài khoản GitHub.

Ví dụ, khi chạy `git add` và `git commit`, bạn đang thao tác với Git trên máy mình. Commit vừa tạo vẫn nằm trong kho cục bộ. Khi chạy `git push` đến một kho trên GitHub, bạn mới gửi các commit lên đó để người khác có thể truy cập theo quyền được cấp.

Vậy trước khi tìm hiểu chuyện gì xảy ra trên GitHub, hãy bắt đầu với điều xảy ra ngay trên máy bạn khi chạy `git add`.

Trong git 1 tệp tin trong git di chuyển qua 3 khu vực:
Working Directory (Cây làm việc): Nơi bạn thao tác trực tiếp với các tệp tin trên hệ điều hành. 
Staging Area (Index): Nơi đăng ký trước các thay đổi dự kiến sẽ được lưu vào lịch sử. 
Repository (.git/): Nơi lưu trữ vĩnh viễn các snapshot (commits) dưới dạng cơ sở dữ liệu đối tượng (Object Database). 

Khi bạn chạy câu lệnh git add <file>:
	git đọc nội dung file từ working directory sau đó gán thêm header, tính toán mã băm SHA sau đó nén toàn bộ bằng thuật toán zlib, mã băm SHA này sẽ được sử dụng làm ObjectID. Sau khi tính SHA và xác định Object ID, Git có thể kiểm tra xem object tương ứng đã tồn tại trong Object Database hay chưa.
- Nếu chưa tồn tại: Git lưu Blob Object mới.
- Nếu đã tồn tại: Git có thể tái sử dụng object cũ mà không cần lưu thêm bản sao.Ví dụ, bạn có file hello.txt chứa:Hello Git, Git sẽ tạo dữ liệu logic cho Blob Object như sau:
        blob 9\0Hello Git, Git tính SHA trên toàn bộ dữ liệu này để tạo Object ID
Cuối cùng, cập nhật vào staging area hay còn được gọi là index (ghi vào tệp nhị phân .git/index).

Object Database là gì?
Object Database (ODB) của Git là một kho lưu trữ đối tượng bất biến (Immutable Object Store), hoạt động theo mô hình Content-Addressable Storage, có thể được hiểu như một cơ sở dữ liệu Key-Value, thường nằm tại thư mục .git/objects/.Trong đó, Key là Object ID, còn Value là Git Object tương ứng.
ODB lưu trữ 4 loại Git Object cốt lõi:

Blob: Chứa nội dung của file dưới dạng dữ liệu byte, không lưu tên file hay đường dẫn.

Tree: Biểu diễn cấu trúc thư mục, chứa các entry ánh xạ tên file hoặc thư mục đến Object ID của Blob hoặc Tree tương ứng, cùng thông tin file mode.

Commit: Đại diện cho một snapshot của repository, lưu tham chiếu đến Root Tree và các Parent Commit (nếu có), cùng thông tin tác giả (Author), người tạo commit (Committer), thời gian và Commit Message.

Tag (Annotated Tag): Là Git Object dùng để gắn nhãn cho một object khác, thường là Commit. Nó chứa Object ID của đối tượng được tham chiếu, tên tag, thông tin người tạo, thông điệp và có thể kèm chữ ký số.

Do tính chất Immutable, các Git Object không bị chỉnh sửa trực tiếp sau khi được tạo. Khi nội dung thay đổi, Git tạo ra object mới với Object ID tương ứng thay vì ghi đè object cũ.