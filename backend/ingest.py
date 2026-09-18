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