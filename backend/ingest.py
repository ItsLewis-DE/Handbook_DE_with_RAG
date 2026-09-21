import hashlib
import json
import uuid

from langchain_chroma import Chroma

from outline import OutlineCatalog, make_outlines
from rag import INDEX_SPEC, load_documents, make_embeddings, split_documents
from storage import CHROMA_DIR, DATA_DIR, MANIFEST_PATH


def json_bytes(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True).encode("utf-8")


def record(doc):
    return {"content": doc.page_content, "metadata": doc.metadata}


def main():
    sections = load_documents()
    outlines = make_outlines(sections)
    chunks = split_documents(sections)
    if not chunks:
        raise RuntimeError("Không có body chunk để index.")
    OutlineCatalog(outlines, chunks)  # Kiểm tra quan hệ trước khi publish.
    corpus_hash = hashlib.sha256(json_bytes({
        "chunks": [record(d) for d in chunks],
        "outlines": [record(d) for d in outlines],
    })).hexdigest()

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    collection_name = f"handbook_{uuid.uuid4().hex}"
    store = Chroma(
        collection_name=collection_name,
        persist_directory=str(CHROMA_DIR), embedding_function=make_embeddings(),
    )
    ids = [d.metadata["chunk_id"] for d in chunks]
    if len(set(ids)) != len(ids):
        raise ValueError("chunk_id trùng")
    for start in range(0, len(chunks), 64):
        store.add_documents(chunks[start:start + 64], ids=ids[start:start + 64])
    if len(store.get(include=["metadatas"])["ids"]) != len(chunks):
        raise RuntimeError("Số chunk không khớp; chưa đổi manifest.")

    payload = json_bytes({
        "schema_version": 1, "collection": collection_name,
        "corpus_hash": corpus_hash, "outlines": [record(d) for d in outlines],
    })
    outline_path = DATA_DIR / f"{collection_name}.outlines.json"
    pending_outline = outline_path.with_suffix(".tmp")
    pending_outline.write_bytes(payload)
    pending_outline.replace(outline_path)

    manifest = {
        "collection": collection_name, "spec": INDEX_SPEC,
        "corpus_hash": corpus_hash, "chunk_count": len(chunks),
        "outline_file": outline_path.name, "outline_count": len(outlines),
        "outline_sha256": hashlib.sha256(payload).hexdigest(),
    }
    # Tên tạm riêng cho mỗi writer; manifest được thay sau cùng.
    pending_manifest = DATA_DIR / f"{collection_name}.manifest.tmp"
    pending_manifest.write_bytes(json_bytes(manifest))
    pending_manifest.replace(MANIFEST_PATH)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()