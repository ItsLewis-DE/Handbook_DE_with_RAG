---
title: Cơ chế hoạt động của Git
description: "Từ Working Directory, Staging Area và Object Database đến cách Git tạo commit, quản lý nhánh và cập nhật HEAD."
lang: vi
hide:
  - navigation
---

<header class="airflow-article-hero git-article-hero">
  <div class="airflow-article-hero__eyebrow">
    <a href="../../">BEHIND THE PIPELINE</a>
    <span>ARTICLE / 008</span>
  </div>
  <h1>Cơ chế hoạt động<br><em>của Git</em></h1>
  <p class="airflow-article-hero__dek">
    Từ Working Directory, Staging Area và Object Database đến cách Git tạo commit,
    quản lý nhánh và cập nhật HEAD.
  </p>
  <div class="airflow-article-hero__meta" aria-label="Thông tin bài viết">
    <span>DEVELOPER TOOLS</span>
    <span>EDITION 08 · 2026</span>
  </div>
</header>

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

## Ba khu vực làm việc trong Git

Trong Git, một tệp tin di chuyển qua ba khu vực:

- **Working Directory (cây làm việc):** Nơi bạn thao tác trực tiếp với các tệp tin trên hệ điều hành.
- **Staging Area (Index):** Nơi đăng ký trước các thay đổi dự kiến sẽ được lưu vào lịch sử.
- **Repository (`.git/`):** Nơi lưu trữ các snapshot (commit) dưới dạng cơ sở dữ liệu đối tượng (Object Database).

## Điều gì xảy ra khi chạy `git add`?

Khi bạn chạy câu lệnh `git add <file>`, Git đọc nội dung tệp từ Working Directory, thêm header, tính toán mã băm SHA rồi nén toàn bộ bằng thuật toán zlib. Mã băm SHA này được sử dụng làm **Object ID**. Sau khi tính SHA và xác định Object ID, Git có thể kiểm tra xem object tương ứng đã tồn tại trong Object Database hay chưa:

- **Nếu chưa tồn tại:** Git lưu Blob Object mới.
- **Nếu đã tồn tại:** Git có thể tái sử dụng object cũ mà không cần lưu thêm bản sao.

Ví dụ, với tệp `hello.txt` chứa `Hello Git`, Git tạo dữ liệu logic cho Blob Object như sau:

```text
blob 9\0Hello Git
```

Git tính SHA trên toàn bộ dữ liệu này để tạo Object ID. Cuối cùng, Git cập nhật Staging Area, hay còn gọi là Index, bằng cách ghi vào tệp nhị phân `.git/index`.

### Object Database là gì?

**Object Database (ODB)** của Git là một kho lưu trữ đối tượng bất biến (Immutable Object Store), hoạt động theo mô hình **Content-Addressable Storage**. Có thể hiểu đây là một cơ sở dữ liệu Key-Value, thường nằm tại thư mục `.git/objects/`. Trong đó, Key là Object ID, còn Value là Git Object tương ứng.

ODB lưu trữ bốn loại Git Object cốt lõi:

- **Blob:** Chứa nội dung của tệp dưới dạng dữ liệu byte, không lưu tên tệp hay đường dẫn.
- **Tree:** Biểu diễn cấu trúc thư mục, chứa các entry ánh xạ tên tệp hoặc thư mục đến Object ID của Blob hoặc Tree tương ứng, cùng thông tin file mode.
- **Commit:** Đại diện cho một snapshot của repository, lưu tham chiếu đến Root Tree và các Parent Commit (nếu có), cùng thông tin tác giả (Author), người tạo commit (Committer), thời gian và Commit Message.
- **Tag (Annotated Tag):** Là Git Object dùng để gắn nhãn cho một object khác, thường là Commit. Nó chứa Object ID của đối tượng được tham chiếu, tên tag, thông tin người tạo, thông điệp và có thể kèm chữ ký số.

Do tính chất Immutable, các Git Object không bị chỉnh sửa trực tiếp sau khi được tạo. Khi nội dung thay đổi, Git tạo ra object mới với Object ID tương ứng thay vì ghi đè object cũ.

### Tại sao Git ghi vào Object Database ngay khi `git add`?

- **Bảo vệ dữ liệu tức thì (Data Durability):** Ngay khi lệnh `git add` kết thúc, nội dung tệp tại thời điểm đó đã được lưu trong `.git/objects/`.
- **Giữ cho Staging Area gọn nhẹ:** Tệp `.git/index` chỉ cần lưu thông tin tham chiếu, giúp việc truy cập nhanh hơn.
- **Tối ưu hóa hiệu năng của `git commit`:** Các công đoạn đọc đĩa, tính toán mã băm và nén zlib đã được chia nhỏ và xử lý ở bước `git add`.

Vì vậy, khi chạy `git commit`, Git không cần quét lại nội dung các tệp. Git chỉ cần ghi nhận trạng thái của `.git/index` thành các Tree Object và tạo một Commit Object trỏ tới Root Tree.

## Tệp nhị phân `.git/index` là gì?

Tệp `.git/index` là một bảng mục lục nhị phân phẳng, ánh xạ giữa cây thư mục vật lý trên ổ đĩa với các đối tượng bên trong Git Object Database. Cấu trúc của một tệp Index:

```text
+-----------------------------------------------------------------------+
| 1. Header (12 bytes)                                                  |
+-----------------------------------------------------------------------+
| 2. Index Entries (Nhiều bản ghi nối tiếp nhau)                        |
|    - Stat Metadata (mtime, ctime, inode, size, mode, uid, gid)        |
|    - Mã SHA của Blob (20 bytes hoặc 32 bytes)                         |
|    - Flags (Stage flag, độ dài path...)                               |
|    - Path name (Đường dẫn tương đối của tệp)                          |
+-----------------------------------------------------------------------+
| 3. Extensions (Tùy chọn: Cached Tree, Untracked Cache...)             |
+-----------------------------------------------------------------------+
| 4. Checksum (20 hoặc 32 bytes cuối tệp)                               |
+-----------------------------------------------------------------------+
```

Mỗi tệp được theo dõi bởi một Index Entry. Các entry được sắp xếp theo thứ tự tên đường dẫn để khi chạy `git add` với một tệp cụ thể, thuật toán tìm kiếm nhị phân (Binary Search) có thể nhanh chóng xác định vị trí tệp đó trong Index.

Trong đó:

- **Header:** Cho Git biết tệp có đúng định dạng Index không, phiên bản bao nhiêu và có bao nhiêu entry.
- **Index Entries:** Chứa thông tin của từng đường dẫn, bao gồm đường dẫn tương đối, Object ID, metadata và flags.
- **Extensions:** Các cấu trúc bổ sung dùng để tối ưu hóa hoặc lưu thông tin đặc biệt.
- **Checksum:** Kiểm tra tính toàn vẹn của nội dung Index.

Index không lưu trực tiếp nội dung của các tệp mà lưu con trỏ SHA đến các đối tượng trong Object Database. Trong mục Path Name của Index Entry, đường dẫn không được chia thành cấu trúc thư mục mà được lưu dưới dạng một đường dẫn phẳng, ví dụ: `src/source`.

## Điều gì xảy ra khi chạy `git commit`?

Khi bạn chạy `git commit`, Git thực hiện các bước sau:

1. **Xây dựng Tree Objects từ Git Index.** Khi thực hiện `git commit` thông thường, Git sử dụng trạng thái đã được staging trong Index để xây dựng một snapshot của repository dưới dạng hệ thống Tree Objects.

    Dựa vào đó, Git xây dựng cấu trúc phân cấp: các Tree Objects đại diện cho thư mục, chứa các entry tham chiếu đến Blob Objects hoặc các Tree Objects con, cùng với tên và file mode tương ứng.

    Cuối cùng, Git xác định Object ID của Root Tree Object đại diện cho toàn bộ snapshot của repository. Những Tree Objects có nội dung không thay đổi có thể được tái sử dụng từ các commit trước.

2. **Xác định commit cha.** Git mở tệp `.git/HEAD` để xem bạn đang ở nhánh nào. Sau đó, Git đọc tệp tham chiếu của nhánh, chẳng hạn `.git/refs/heads/main`, để lấy mã SHA của commit hiện tại. Mã SHA này được chỉ định làm Parent của commit chuẩn bị tạo. Nếu đây là commit đầu tiên của dự án, commit sẽ không có Parent.
3. **Tạo nội dung Commit Object.** Git tạo chuỗi văn bản hoàn chỉnh cho Commit Object.
4. **Lưu Commit Object.** Git tính toán mã băm SHA, nén lại và ghi xuống Object Database.
5. **Cập nhật con trỏ nhánh.** Git ghi mã SHA của commit vừa tạo vào tệp tham chiếu của nhánh hiện tại.

## Nhánh trong Git

Một **nhánh (Branch)** trong Git là một tham chiếu có thể thay đổi (Movable Reference), trỏ đến một Commit Object cụ thể thông qua Object ID (SHA-1 hoặc SHA-256), thay vì lưu một bản sao hoàn chỉnh của dự án.

Mỗi branch được biểu diễn bằng một tệp văn bản nhỏ nằm trong thư mục `.git/refs/heads/`. Ví dụ, khi tạo nhánh `feature` từ `main`, Git có thể tạo tệp `.git/refs/heads/feature` chứa Object ID của commit mà `main` đang trỏ đến.

Ban đầu, cả hai branch cùng tham chiếu đến một Commit Object, do đó Git không cần sao chép các Blob Objects, Tree Objects hay Commit Objects. Khi bạn tạo một commit mới trên nhánh `feature`, Git tạo Commit Object mới trỏ ngược về commit cha trước đó và tự động cập nhật mã băm trong `.git/refs/heads/feature` để trỏ tới commit mới này.

### Chuyển nhánh với `git switch` và vai trò của HEAD

Lệnh `git switch` dùng để di chuyển con trỏ **HEAD** từ branch này sang branch khác, đồng thời cập nhật Working Directory và Staging Area (Index) tương ứng. Cơ chế hoạt động như sau:

1. **Kiểm tra thay đổi chưa commit.** Git kiểm tra xem Working Tree và Index có thay đổi chưa commit nào xung đột với branch đích không. Ví dụ, nếu `app.py` có thay đổi chưa commit và việc chuyển nhánh sẽ ghi đè các thay đổi đó, Git dừng lại và yêu cầu bạn commit trước khi chuyển nhánh. Nếu `app.py` ở cả hai nhánh giống nhau, Git có thể cho phép chuyển nhánh mà không báo lỗi.
2. **Đồng bộ thư mục làm việc.** Sau khi kiểm tra, Git đọc Tree Object của nhánh đích để cập nhật thư mục làm việc.
3. **Cập nhật HEAD.** Git cập nhật con trỏ trong tệp `.git/HEAD`. Thông thường, HEAD là một symbolic reference trỏ đến branch hiện tại, ví dụ: `ref: refs/heads/main`.

<footer class="airflow-article-end git-article-end">
  <div>
    <span>BEHIND THE PIPELINE / 008</span>
    <strong>Hiểu hệ thống,<br>không chỉ cú pháp.</strong>
  </div>
  <a href="../../library/">Trở về thư viện <span aria-hidden="true">→</span></a>
</footer>
