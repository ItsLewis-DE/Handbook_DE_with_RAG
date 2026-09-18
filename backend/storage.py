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