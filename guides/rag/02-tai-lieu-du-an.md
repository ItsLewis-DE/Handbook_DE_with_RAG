# Phase 02 — Đọc tài liệu dự án và hỏi bằng tiếng Việt

[Trước](01-backend-rag-toi-gian.md) · [Lộ trình](README.md) · [Tiếp](03-luu-chi-muc.md)

## Điểm xuất phát và mục tiêu

Bạn đã hoàn thành phase 01. Backend hiện trả lời về một bài tiếng Anh ngoài dự án. Phase này chỉ đổi **nguồn dữ liệu** và **embedding**; giữ nguyên chain, Ollama, endpoint và cách chạy.

Corpus gồm bốn bài đang được cấu hình trong `mkdocs.yml`, không bao gồm `docs/index.md` là landing page. Đặc biệt, `docs/index/index.md` là bài về database index và phải được giữ lại.

## 1. Thay loader trong `backend/rag.py`

Thêm hai import ở đầu file:

```python
from pathlib import Path
from langchain_core.documents import Document
```

Thêm các hằng số cấp module, phía trên các hàm:

```python
REPO_ROOT = Path(__file__).resolve().parents[1]
EMBEDDING_MODEL = "intfloat/multilingual-e5-small"
ARTICLE_PATHS = (
    "airflow/architecture.md",
    "architecture/shared-disk-vs-shared-nothing.md",
    "postgres/postgres.md",
    "index/index.md",
)
```

Thay toàn bộ hàm `load_documents`:

```python
def load_documents():
    documents = []
    for relative_path in ARTICLE_PATHS:
        path = REPO_ROOT / "docs" / relative_path
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            raise RuntimeError(f"Bài viết rỗng: {relative_path}")
        documents.append(Document(
            page_content=text,
            metadata={"source": relative_path},
        ))
    return documents
```

Không nhận đường dẫn hoặc URL tùy ý từ request `/chat`. Corpus được chọn bằng code, phù hợp website tài liệu công khai hiện tại. Danh sách tường minh cũng giúp tránh nạp nhầm hướng dẫn học, CSS, JavaScript và bản build trong `site/`.

Có thể xóa import `bs4`, `WebBaseLoader` và dòng đặt `USER_AGENT` vì loader mới không dùng chúng. Giữ `import os` vì `make_llm` vẫn đọc biến môi trường.

## 2. Thay hàm embedding

Thay toàn bộ `make_embeddings`:

```python
def make_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={
            "normalize_embeddings": True,
            "prompt": "passage: ",
        },
        query_encode_kwargs={
            "normalize_embeddings": True,
            "prompt": "query: ",
        },
    )
```

E5 hỗ trợ nhiều ngôn ngữ và yêu cầu prefix `passage: ` cho tài liệu, `query: ` cho câu hỏi, kể cả văn bản không phải tiếng Anh. Tham số `prompt` ở đây là prefix cho embedding, không phải system prompt của LLM. LangChain truyền hai nhóm cấu hình đến lúc encode tài liệu và encode câu hỏi tương ứng. [E5 model card](https://huggingface.co/intfloat/multilingual-e5-small), [implementation HuggingFaceEmbeddings](https://github.com/langchain-ai/langchain/blob/master/libs/partners/huggingface/langchain_huggingface/embeddings/huggingface.py)

Trong `build_retriever`, đổi `collection_name="rag_phase_01"` thành `collection_name="rag_phase_02"`. Dừng rồi khởi động process mới để không giữ collection của bài trước trong bộ nhớ.

## 3. Thay câu hỏi chạy trực tiếp

Trong khối `if __name__ == "__main__":`, đổi dòng `question` thành:

```python
question = "Critical Section của Airflow Scheduler dùng để làm gì?"
```

Tại `backend`:

```bash
uv run python rag.py
uv run uvicorn app:app --host 127.0.0.1 --port 8001
```

Lệnh đầu kết thúc rồi mới chạy lệnh thứ hai. Thử từ terminal khác:

```bash
curl --fail-with-body http://127.0.0.1:8001/chat \
  -H 'Content-Type: application/json' \
  -d '{"question":"Schema trong PostgreSQL có phải là một thư mục trên ổ đĩa không?"}'
```

## 4. Quan sát retrieval thay vì chỉ đọc đáp án

Tạo file mới `backend/inspect_retrieval.py`:

```python
import sys

from rag import build_retriever

question = " ".join(sys.argv[1:]) or "shared_buffers dùng để làm gì?"
retriever = build_retriever()
for rank, doc in enumerate(retriever.invoke(question), start=1):
    print(f"\n#{rank} {doc.metadata}")
    print(doc.page_content)
```

Tại `backend`:

```bash
uv run python inspect_retrieval.py "shared_buffers dùng để làm gì?"
uv run python inspect_retrieval.py "B-tree khác B+tree thế nào?"
uv run python inspect_retrieval.py "Dữ liệu bị phân phối lệch giữa các node gây vấn đề gì?"
```

Mỗi lệnh phase này vẫn embedding lại corpus. Sau phase 03, cùng script sẽ đọc chỉ mục đã lưu.

Ghi lại câu hỏi, source của từng đoạn, đoạn có đủ thông tin không và đáp án có bám nguồn không. Đây là baseline để so sánh các phase sau; không mặc định model đa ngôn ngữ sẽ làm đúng mọi câu hỏi.

## Giới hạn cố ý giữ lại

- Loader đang đọc Markdown thô, còn HTML trang trí và front matter. Phase 04 sẽ xử lý cấu trúc thật của repo.
- Vẫn chia 1000 ký tự, overlap 200. E5 cắt đầu vào quá 512 token; ký tự và token không tương đương, nhất là với tiếng Việt. Phase 04 sẽ chia theo tokenizer và kiểm tra chiều dài sau khi thêm tiêu đề.
- Nguồn mới chỉ có tên file; chưa có link đến heading.
- Chưa lưu dữ liệu hội thoại. Mỗi request độc lập: hãy viết câu hỏi đầy đủ.

**Hoàn thành phase khi:** câu hỏi tiếng Việt retrieve được đoạn trong đúng bài; backend dùng đúng `qwen3:4b-instruct` và không còn đọc bài web mẫu.
