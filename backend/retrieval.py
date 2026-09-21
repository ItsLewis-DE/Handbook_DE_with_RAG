import re
from collections import defaultdict

from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda
from rank_bm25 import BM25Okapi


def tokenize(text):
    # Giữ underscore và các tên như B+tree, B-tree; case-insensitive.
    return re.findall(r"\w+(?:[+_-]\w+)*\+*", text.casefold())


def make_base_retriever(store, mode="hybrid", k=4, candidate_k=8):
    if not 1 <= k <= candidate_k:
        raise ValueError("Cần 1 <= k <= candidate_k")
    if mode == "vector":
        return store.as_retriever(search_kwargs={"k": k})
    if mode != "hybrid":
        raise ValueError("mode phải là vector hoặc hybrid")

    # Corpus nhỏ: nạp các chunk một lần để xây BM25 trong RAM.
    data = store.get(include=["documents", "metadatas"])
    documents = [
        Document(page_content=text, metadata=metadata)
        for text, metadata in zip(data["documents"], data["metadatas"])
    ]
    if not documents:
        raise RuntimeError("Không có dữ liệu cho BM25.")
    bm25 = BM25Okapi([tokenize(doc.page_content) for doc in documents])

    def search(question):
        vector_hits = store.similarity_search(question, k=min(candidate_k, len(documents)))
        lexical_scores = bm25.get_scores(tokenize(question))
        ranked_indices = sorted(
            range(len(documents)), key=lambda i: (-float(lexical_scores[i]), i)
        )
        lexical_hits = [
            documents[i] for i in ranked_indices if lexical_scores[i] > 0
        ][:candidate_k]

        scores = defaultdict(float)
        by_id = {}
        for hits in (vector_hits, lexical_hits):
            seen = set()
            for rank, doc in enumerate(hits, start=1):
                chunk_id = doc.metadata["chunk_id"]
                if chunk_id in seen:
                    continue
                seen.add(chunk_id)
                scores[chunk_id] += 1.0 / (60 + rank)
                by_id[chunk_id] = doc
        ordered = sorted(scores, key=lambda chunk_id: (-scores[chunk_id], chunk_id))
        # Duyệt toàn bộ ứng viên theo điểm RRF để mỗi section chỉ chiếm một slot.
        # Chunk đầu tiên của mỗi section có điểm cao nhất; không nối nội dung.
        selected = []
        seen_sections = set()
        for chunk_id in ordered:
            doc = by_id[chunk_id]
            section_key = (doc.metadata["source"], doc.metadata["url"])
            if section_key in seen_sections:
                continue
            seen_sections.add(section_key)
            selected.append(doc)
            if len(selected) == k:
                break
        return selected

    return RunnableLambda(search)


CANDIDATE_K = 12


def make_retriever(store, mode="vector", k=4):
    if mode in {"vector", "hybrid"}:
        return make_base_retriever(store, mode, k=k, candidate_k=CANDIDATE_K)
    if mode not in {"hybrid_rerank", "hybrid_decompose_rerank"}:
        raise ValueError("RETRIEVAL_MODE không hợp lệ")
    from reranking import Reranker

    candidates = make_base_retriever(
        store, "hybrid", k=CANDIDATE_K, candidate_k=CANDIDATE_K
    )
    reranker = Reranker()
    if mode == "hybrid_decompose_rerank":
        from decomposition import build_decomposer, make_decomposed_retriever

        return make_decomposed_retriever(candidates, reranker, build_decomposer(), k=k)
    return RunnableLambda(
        lambda question: reranker.select(question, candidates.invoke(question), k=k)
    )

