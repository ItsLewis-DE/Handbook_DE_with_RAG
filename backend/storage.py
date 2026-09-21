import hashlib
import json
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document

from outline import OutlineCatalog

DATA_DIR = Path(__file__).resolve().parent / ".data"
CHROMA_DIR = DATA_DIR / "chroma"
MANIFEST_PATH = DATA_DIR / "manifest.json"


def open_snapshot(embeddings, expected_spec):
    if not MANIFEST_PATH.exists():
        raise RuntimeError("Chưa có chỉ mục. Chạy: uv run python ingest.py")
    # Đọc manifest đúng một lần: graph và collection cùng snapshot.
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest["spec"] != expected_spec:
        raise RuntimeError("Cấu hình chỉ mục đã đổi. Hãy ingest lại rồi restart.")
    expected_name = f"{manifest['collection']}.outlines.json"
    if manifest["outline_file"] != expected_name:
        raise ValueError("Tên outline không khớp snapshot")
    payload = (DATA_DIR / expected_name).read_bytes()
    if hashlib.sha256(payload).hexdigest() != manifest["outline_sha256"]:
        raise ValueError("Checksum outline không khớp")
    data = json.loads(payload)
    if (data["schema_version"] != 1
            or data["collection"] != manifest["collection"]
            or data["corpus_hash"] != manifest["corpus_hash"]):
        raise ValueError("Outline không cùng phiên bản với collection")
    store = Chroma(
        collection_name=manifest["collection"], persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings, create_collection_if_not_exists=False,
    )
    body_data = store.get(include=["documents", "metadatas"])
    if len(body_data["ids"]) != manifest["chunk_count"]:
        raise RuntimeError("Collection rỗng hoặc thiếu chunk")
    chunks = [Document(page_content=text, metadata=metadata) for text, metadata in
              zip(body_data["documents"], body_data["metadatas"], strict=True)]
    outlines = [Document(page_content=r["content"], metadata=r["metadata"])
                for r in data["outlines"]]
    if len(outlines) != manifest["outline_count"]:
        raise ValueError("Thiếu outline")
    catalog = OutlineCatalog(outlines, chunks)
    return store, catalog, manifest

def open_store(embeddings, expected_spec):
    # Tương thích những script cũ chỉ cần body store.
    return open_snapshot(embeddings, expected_spec)[0]
