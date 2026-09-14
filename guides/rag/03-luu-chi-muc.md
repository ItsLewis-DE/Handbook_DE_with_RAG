# Phase 03 — Lưu Chroma và tách ingestion khỏi backend

[Trước](02-tai-lieu-du-an.md) · [Lộ trình](README.md) · [Tiếp](04-heading-va-nguon.md)

## Vấn đề và thay đổi

Ở phase 02, restart backend đồng nghĩa với embedding lại toàn bộ tài liệu. Ta tách hai thao tác:

```text
python ingest.py → tạo một phiên bản collection mới → ghi manifest
uvicorn app:app  → đọc manifest → mở collection đã có → phục vụ câu hỏi
```

Chroma hỗ trợ lưu local bằng `persist_directory`; dữ liệu được lưu tự động, không cần gọi `.persist()` theo các tutorial cũ. [Tích hợp Chroma](https://docs.langchain.com/oss/python/integrations/vectorstores/chroma)

Ở quy mô corpus hiện tại, mỗi lần ingest sẽ rebuild toàn bộ sang collection mới. Cách này xử lý cả tài liệu bị xóa mà chưa cần xây logic cập nhật tăng dần.

## 1. Ghi lại cấu hình ảnh hưởng đến chỉ mục

Trong `backend/rag.py`, thêm hằng số sau phía dưới `EMBEDDING_MODEL`:

```python
INDEX_SPEC = {
    "embedding_model": EMBEDDING_MODEL,
    "embedding_prefixes": "passage/query",
    "normalize_embeddings": True,
    "chunking": "raw-markdown-char-1000-overlap-200-v1",
}
```

Đây là cấu hình kiểm tra tương thích, không phải hash của nội dung. Khi sửa tài liệu, vẫn phải chạy ingest dù `INDEX_SPEC` không đổi.

## 2. Tạo `backend/storage.py`

```python
import json
from pathlib import Path

from langchain_chroma import Chroma

DATA_DIR = Path(__file__).resolve().parent / ".data"
CHROMA_DIR = DATA_DIR / "chroma"
MANIFEST_PATH = DATA_DIR / "manifest.json"


def open_store(embeddings, expected_spec):
    if not MANIFEST_PATH.exists():
        raise RuntimeError("Chưa có chỉ mục. Chạy: uv run python ingest.py")
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest["spec"] != expected_spec:
        raise RuntimeError("Cấu hình chỉ mục đã đổi. Hãy ingest lại rồi restart.")
    store = Chroma(
        collection_name=manifest["collection"],
        persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings,
        create_collection_if_not_exists=False,
    )
    if not store.get(limit=1)["ids"]:
        raise RuntimeError("Collection rỗng. Hãy kiểm tra ingestion.")
    return store
```

`create_collection_if_not_exists=False` tránh lỗi mở sai tên rồi vô tình tạo một collection rỗng. Chỉ mục thiếu hoặc cấu hình sai làm startup thất bại rõ ràng.

## 3. Tạo `backend/ingest.py`

```python
import hashlib
import json
import uuid

from langchain_chroma import Chroma

from rag import INDEX_SPEC, load_documents, make_embeddings, split_documents
from storage import CHROMA_DIR, DATA_DIR, MANIFEST_PATH


def main():
    chunks = split_documents(load_documents())
    if not chunks:
        raise RuntimeError("Không có chunk để index.")

    records = [
        {"content": chunk.page_content, "metadata": chunk.metadata}
        for chunk in chunks
    ]
    corpus_hash = hashlib.sha256(
        json.dumps(records, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    collection_name = f"handbook_{uuid.uuid4().hex}"
    store = Chroma(
        collection_name=collection_name,
        persist_directory=str(CHROMA_DIR),
        embedding_function=make_embeddings(),
    )
    ids = []
    for index, chunk in enumerate(chunks):
        chunk_id = f"{corpus_hash[:12]}-{index}"
        chunk.metadata["chunk_id"] = chunk_id
        ids.append(chunk_id)

    # Batch nhỏ, không giả định backend Chroma nhận được mọi corpus một lần.
    for start in range(0, len(chunks), 64):
        store.add_documents(chunks[start:start + 64], ids=ids[start:start + 64])

    actual_count = len(store.get(include=["metadatas"])["ids"])
    if actual_count != len(chunks):
        raise RuntimeError("Số chunk đã lưu không khớp; không đổi manifest.")

    manifest = {
        "collection": collection_name,
        "spec": INDEX_SPEC,
        "corpus_hash": corpus_hash,
        "chunk_count": len(chunks),
    }
    pending = MANIFEST_PATH.with_suffix(".tmp")
    pending.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    pending.replace(MANIFEST_PATH)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
```

Chỉ đổi manifest sau khi lưu đủ dữ liệu. Ingest lỗi giữa chừng sẽ để lại collection chưa được dùng; manifest cũ vẫn trỏ đến bản trước. Đây là quy trình học local: chỉ chạy **một ingestion tại một thời điểm**, dừng backend trước khi ingest và restart sau đó. Chưa có điều phối nhiều process hoặc hot reload chỉ mục.

## 4. Thay `build_retriever` trong `backend/rag.py`

```python
def build_retriever():
    from storage import open_store

    store = open_store(make_embeddings(), INDEX_SPEC)
    return store.as_retriever(search_kwargs={"k": 4})
```

Giữ nguyên `build_chain`, `make_llm`, `app.py` và `inspect_retrieval.py`. Không gọi `load_documents` trong đường đi của một request nữa.

## 5. Chạy theo thứ tự

Dừng backend cũ bằng Ctrl+C. Tại `backend`:

```bash
uv run python ingest.py
uv run python inspect_retrieval.py "Critical Section của Scheduler là gì?"
uv run uvicorn app:app --host 127.0.0.1 --port 8001
```

Startup vẫn cần load model embedding để biến **câu hỏi** thành vector. Chỉ việc embedding **tài liệu** đã được chuyển ra ngoài. Lần đầu Ollama nhận câu hỏi cũng có thể phải load LLM vào bộ nhớ.

## 6. Kiểm chứng persistence

1. Ghi lại collection và `chunk_count` trong `.data/manifest.json`.
2. Restart backend hai lần. Manifest không thay đổi, không chạy lại ingestion.
3. Sửa một câu trong bài local, ví dụ thêm một câu đánh dấu học tập. Chưa ingest: kết quả vẫn dùng bản cũ.
4. Dừng backend, ingest và restart. Manifest mới có collection và corpus hash mới; câu thêm đã được index.
5. Hoàn tác câu đánh dấu và ingest lại để corpus trở về nội dung gốc.

Nếu xóa một bài thật sự, cũng cập nhật `ARTICLE_PATHS`: loader tường minh sẽ báo lỗi nếu còn trỏ vào file đã xóa. Collection mới chỉ chứa các bài còn trong danh sách.

Không để `.data/` vào Git. Collection cũ chiếm dung lượng; khi cần dọn, dừng backend và dùng `chromadb.PersistentClient(...).delete_collection(name=...)` với **tên collection cũ đã kiểm tra**, giữ collection đang được manifest trỏ đến. Series này không tự xóa để bạn dễ đối chiếu các lần ingest.

## Lỗi thường gặp

- Đổi embedding nhưng giữ chỉ mục: startup báo cấu hình không khớp; ingest lại, không sửa manifest để bỏ qua kiểm tra.
- Restart vẫn tốn thời gian: model embedding vẫn phải load; kiểm tra xem có log chia/embedding tài liệu hay không.
- Sửa `chunk_size` mà quên `INDEX_SPEC`: cập nhật cả nhãn cấu hình để startup nhận biết khác biệt.
- File manifest tồn tại nhưng mất thư mục Chroma: chạy ingestion lại; manifest không chứa vector.

**Hoàn thành phase khi:** startup chỉ mở chỉ mục đã có và bạn phân biệt rõ embedding tài liệu với embedding câu hỏi.
