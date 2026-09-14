# Tự xây RAG cho Behind the Pipeline

Bộ hướng dẫn thực hành theo từng phase. Bạn bắt đầu bằng một backend chạy được RAG giống ví dụ WebBaseLoader, sau đó nâng cấp chính backend đó. LLM xuyên suốt là **`qwen3:4b-instruct` qua Ollama**; Chroma là vector store.

Các file này là hướng dẫn và code để bạn tự triển khai, chưa phải backend đã được cài đặt trong repo. Thư mục `guides/` nằm ngoài `docs/` để tài liệu học không bị đưa vào corpus hoặc website một cách vô ý.

## Học theo thứ tự

| Phase | Đầu ra | Thay đổi chính |
| --- | --- | --- |
| [01 — Backend và RAG tối giản](01-backend-rag-toi-gian.md) | Gọi `/chat` bằng curl, hỏi về bài web mẫu | Backend, toàn bộ RAG trong một file |
| [02 — Dùng tài liệu dự án](02-tai-lieu-du-an.md) | Hỏi đáp tiếng Việt về bốn bài hiện có | Đổi loader và embedding |
| [03 — Lưu chỉ mục](03-luu-chi-muc.md) | Khởi động backend không embedding lại tài liệu | Tách ingest khỏi serving, lưu Chroma |
| [04 — Heading và nguồn](04-heading-va-nguon.md) | Câu trả lời có nguồn đến đúng mục | Làm sạch nội dung, chia theo heading/token, kiểm tra mã dẫn nguồn |
| [05 — Đánh giá và hybrid search](05-danh-gia-hybrid-search.md) | Đo retrieval trước/sau cải tiến | Bộ câu hỏi, BM25 + vector + RRF |
| [06 — Chat trên MkDocs](06-chat-tren-mkdocs.md) | Hỏi ngay trên website local | Giao diện, CORS, lỗi và trạng thái chờ |

**Bạn có thể dừng sau phase 01:** lúc đó đã có RAG hoạt động đầy đủ với tài liệu web mẫu. Mỗi phase sau đều bắt đầu từ code đã hoàn thành của phase trước; không cần làm hết mới thấy kết quả.

## Quy ước khi làm theo

- Lệnh shell dành cho Linux/WSL/macOS, dùng `uv` và Python 3.12.
- “Tại root repo” nghĩa là thư mục chứa `mkdocs.yml`. “Tại backend” nghĩa là đã `cd backend`.
- Khối ghi **tạo file** hoặc **thay toàn bộ file** có nội dung đầy đủ. Khối ghi **thay hàm** chỉ thay hàm có cùng tên; giữ phần còn lại.
- Mỗi phase giữ nguyên endpoint `/chat`, nhưng bổ sung trường trả về khi cần. Chỉ thêm frontend sau khi hình dạng response ổn định.
- Backend dùng `backend/pyproject.toml`, `backend/uv.lock` và môi trường riêng; MkDocs tiếp tục dùng môi trường tại root.
- Không thay đổi LLM giữa các phase để dễ biết cải tiến nào gây ra khác biệt.
- Mỗi lần đổi corpus, model embedding hoặc cách chia đoạn, phải tạo lại chỉ mục. Cùng số chiều vector không có nghĩa là hai model tương thích.

## Những khái niệm sẽ gặp

| Khái niệm | Hiểu trong bài thực hành |
| --- | --- |
| Document | Văn bản cùng metadata như bài viết, đường dẫn |
| Chunk | Một đoạn nhỏ được đem đi tìm kiếm |
| Embedding | Vector biểu diễn nội dung; không phải câu trả lời |
| Retriever | Nhận câu hỏi, trả các đoạn liên quan |
| Context | Các đoạn được đặt vào prompt của LLM |
| Generation | LLM viết câu trả lời từ câu hỏi và context |
| Grounding | Câu trả lời được hỗ trợ bởi tài liệu đã tìm |
| Ingestion | Đọc, chia, embedding và lưu tài liệu |

## Mức độ kiểm chứng

API và tag model được đối chiếu với tài liệu chính thức khi viết ngày 2026-09-14. Các phase có lệnh chạy, tiêu chí hoàn thành và cách chẩn đoán. Không coi việc code có cú pháp hợp lệ là bằng chứng chất lượng RAG; bạn cần chạy các kiểm tra ở từng phase trên máy có Ollama và model.

Đã kiểm tra khi biên soạn:

- Cú pháp 23 khối Python, cú pháp JavaScript, JSON/JSONL và liên kết nội bộ của series.
- Parser phase 04 chạy trên bốn bài thật: 129 section, 184 chunk qua tokenizer E5; mọi chunk đạt kiểm tra không quá 512 token. Con số thay đổi khi nội dung được cập nhật.
- Nhãn section trong bộ câu hỏi mẫu khớp với corpus hiện tại.
- Logic mã dẫn nguồn hợp lệ/sai/thiếu/từ chối và logic gộp, loại trùng hybrid được kiểm tra bằng đầu vào giả có kiểm soát.

Chưa chạy toàn bộ backend với embedding weights, Chroma và Qwen, chưa kiểm tra UI trong trình duyệt và chưa có số liệu chất lượng trả lời. Các kiểm tra trên không thay thế bước chạy end-to-end ở từng phase.

Sau khi cài dependency thành công, lưu `backend/uv.lock` trong Git để tái lập môi trường bằng `uv sync --locked`. Lần `uv add` đầu tiên giải quyết phiên bản tại thời điểm bạn thực hành, không phải một bộ phiên bản đã được benchmark sẵn.

## Sau phase 06

Các bài tập tiếp theo, chưa bắt buộc và chưa triển khai trong series này:

1. Reranker: chỉ thêm khi hybrid còn xếp sai nguồn; so sánh chất lượng và thời gian chạy.
2. Hội thoại nhiều lượt: viết lại câu hỏi theo lịch sử ngắn, rồi retrieve lại; câu trả lời trước không phải nguồn chứng cứ.
3. Cập nhật tăng dần: hash từng bài, upsert đoạn mới và xóa đoạn cũ; hiện tại rebuild cả corpus nhỏ.
4. Public deployment: backend HTTPS, giới hạn request/đồng thời, reverse proxy, monitoring và cơ chế bảo vệ tài nguyên.

Không cần agent, tool calling hay fine-tuning để hoàn thành các phase hiện tại.
