import argparse
import json
import math
import os
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda
from rank_bm25 import BM25Okapi

from answering import answer_question, build_answerer
from decomposition import QueryPlan, build_decomposer
from rag import INDEX_SPEC, make_embeddings
from reranking import RERANKER_MAX_LENGTH, RERANKER_MODEL, Reranker
from retrieval import CANDIDATE_K, tokenize
from storage import MANIFEST_PATH, open_store


DEFAULT_QUESTION = "trong airflow có bao nhiêu component"
DEFAULT_MODE = "hybrid_decompose_rerank"
FINAL_K = 8
RRF_CONSTANT = 60
SUPPORTED_MODES = {
    "vector",
    "hybrid",
    "hybrid_rerank",
    "hybrid_decompose_rerank",
}


def document_record(document, **extra):
    return {
        **extra,
        "chunk_id": document.metadata["chunk_id"],
        "source": document.metadata["source"],
        "title": document.metadata["title"],
        "heading": document.metadata["heading"],
        "url": document.metadata["url"],
        "text": document.page_content,
    }


def load_corpus(store):
    data = store.get(include=["documents", "metadatas"])
    return [
        Document(page_content=text, metadata=metadata)
        for text, metadata in zip(data["documents"], data["metadatas"])
    ]


def trace_vector(store, question, k):
    started = perf_counter()
    hits = store.similarity_search(question, k=k)
    return hits, {
        "seconds": perf_counter() - started,
        "results": [
            document_record(document, rank=rank)
            for rank, document in enumerate(hits, start=1)
        ],
    }


def trace_hybrid(store, corpus, bm25, question, k):
    started = perf_counter()
    vector_started = perf_counter()
    vector_hits = store.similarity_search(
        question, k=min(CANDIDATE_K, len(corpus))
    )
    vector_seconds = perf_counter() - vector_started

    lexical_started = perf_counter()
    query_tokens = tokenize(question)
    lexical_scores = bm25.get_scores(query_tokens)
    ranked_indices = sorted(
        range(len(corpus)), key=lambda index: (-float(lexical_scores[index]), index)
    )
    lexical_hits = [
        (corpus[index], float(lexical_scores[index]))
        for index in ranked_indices
        if lexical_scores[index] > 0
    ][:CANDIDATE_K]
    lexical_seconds = perf_counter() - lexical_started

    fusion_started = perf_counter()
    rrf_scores = defaultdict(float)
    by_id = {}
    branch_ranks = defaultdict(dict)
    for branch, hits in (
        ("vector", [(document, None) for document in vector_hits]),
        ("bm25", lexical_hits),
    ):
        seen = set()
        for rank, (document, _) in enumerate(hits, start=1):
            chunk_id = document.metadata["chunk_id"]
            if chunk_id in seen:
                continue
            seen.add(chunk_id)
            rrf_scores[chunk_id] += 1.0 / (RRF_CONSTANT + rank)
            branch_ranks[chunk_id][branch] = rank
            by_id[chunk_id] = document

    ordered_ids = sorted(
        rrf_scores, key=lambda chunk_id: (-rrf_scores[chunk_id], chunk_id)
    )
    fused = [by_id[chunk_id] for chunk_id in ordered_ids]

    selected = []
    seen_sections = set()
    selected_ids = set()
    for document in fused:
        section_key = (document.metadata["source"], document.metadata["url"])
        if section_key in seen_sections:
            continue
        seen_sections.add(section_key)
        selected.append(document)
        selected_ids.add(document.metadata["chunk_id"])
        if len(selected) == k:
            break
    fusion_seconds = perf_counter() - fusion_started

    return selected, {
        "query": question,
        "query_tokens": query_tokens,
        "seconds": perf_counter() - started,
        "fusion_seconds": fusion_seconds,
        "vector": {
            "seconds": vector_seconds,
            "results": [
                document_record(document, rank=rank)
                for rank, document in enumerate(vector_hits, start=1)
            ],
        },
        "bm25": {
            "seconds": lexical_seconds,
            "results": [
                document_record(document, rank=rank, score=score)
                for rank, (document, score) in enumerate(lexical_hits, start=1)
            ],
        },
        "rrf": {
            "constant": RRF_CONSTANT,
            "ranking": [
                document_record(
                    by_id[chunk_id],
                    rank=rank,
                    score=rrf_scores[chunk_id],
                    branch_ranks=branch_ranks[chunk_id],
                    selected_after_section_dedup=chunk_id in selected_ids,
                )
                for rank, chunk_id in enumerate(ordered_ids, start=1)
            ],
        },
        "after_section_dedup": [
            document_record(document, rank=rank)
            for rank, document in enumerate(selected, start=1)
        ],
    }


def timing_summary(trace, total_seconds):
    timings = []

    def add(stage, seconds):
        if seconds is None:
            return
        timings.append({
            "stage": stage,
            "seconds": seconds,
            "percent_of_total": (
                seconds / total_seconds * 100 if total_seconds else 0.0
            ),
        })

    stages = trace["stages"]
    add("initialization", stages["initialization"]["seconds"])
    if "bm25_index" in stages:
        add("bm25_index", stages["bm25_index"]["seconds"])
    if "decomposition" in stages:
        add("decomposition", stages["decomposition"]["seconds"])

    if "vector" in stages:
        add("vector_search", stages["vector"]["seconds"])
    else:
        retrieval_traces = stages.get("retrieval_by_query", [])
        add(
            "vector_search",
            sum(item["vector"]["seconds"] for item in retrieval_traces),
        )
        add(
            "bm25_search",
            sum(item["bm25"]["seconds"] for item in retrieval_traces),
        )
        add(
            "rrf_and_section_dedup",
            sum(item["fusion_seconds"] for item in retrieval_traces),
        )

    if "reranker" in stages:
        add("reranker", stages["reranker"]["seconds"])
    add("answerer_setup", stages["answerer_setup"]["seconds"])
    add("answer_generation", stages["answer_generation"]["seconds"])

    accounted_seconds = sum(item["seconds"] for item in timings)
    other_seconds = max(0.0, total_seconds - accounted_seconds)
    add("other_overhead", other_seconds)
    return {
        "total_seconds": total_seconds,
        "stage_timings": timings,
        "accounted_seconds": sum(item["seconds"] for item in timings),
        "note": (
            "Các stage không chồng lặp. other_overhead gồm việc tạo cấu trúc trace, "
            "hợp nhất candidate và tuần tự hóa dữ liệu trong bộ nhớ; thời gian ghi file "
            "không nằm trong total_seconds."
        ),
    }


def trace_decomposition(question):
    started = perf_counter()
    raw = None
    error = None
    fallback = False
    queries = [question]
    try:
        raw = build_decomposer().invoke({"question": question})
        plan = QueryPlan.model_validate_json(raw)
        seen = {question.strip().casefold()}
        for subquestion in plan.queries:
            key = subquestion.casefold()
            if key not in seen:
                seen.add(key)
                queries.append(subquestion)
    except Exception as exc:
        fallback = True
        error = f"{type(exc).__name__}: {exc}"
    return queries, {
        "seconds": perf_counter() - started,
        "raw_model_output": raw,
        "queries": queries,
        "fallback_to_original": fallback,
        "error": error,
    }


def trace_reranker(question, documents, k):
    started = perf_counter()
    unique = {}
    for document in documents:
        unique.setdefault(document.metadata["chunk_id"], document)
    documents = list(unique.values())
    if not documents:
        return [], {"seconds": 0.0, "model": RERANKER_MODEL, "ranking": []}

    reranker = Reranker()
    pairs = [(question, document.page_content) for document in documents]
    token_counts = []
    for query, passage in pairs:
        input_ids = reranker.model.tokenizer(
            query, passage, truncation=False, add_special_tokens=True
        )["input_ids"]
        token_counts.append(len(input_ids))
        if len(input_ids) > RERANKER_MAX_LENGTH:
            raise ValueError("Cặp câu hỏi–đoạn vượt ngân sách token reranker")

    values = reranker.model.predict(pairs, batch_size=2, show_progress_bar=False)
    scores = [float(value) for value in values]
    if len(scores) != len(documents) or not all(math.isfinite(score) for score in scores):
        raise RuntimeError("Reranker trả điểm không hợp lệ")
    order = sorted(
        range(len(documents)),
        key=lambda index: (-scores[index], documents[index].metadata["chunk_id"]),
    )
    selected = [documents[index] for index in order[:k]]
    selected_ids = {document.metadata["chunk_id"] for document in selected}
    return selected, {
        "seconds": perf_counter() - started,
        "model": RERANKER_MODEL,
        "max_length": RERANKER_MAX_LENGTH,
        "batch_size": 2,
        "ranking": [
            document_record(
                documents[index],
                rank=rank,
                score=scores[index],
                token_count=token_counts[index],
                selected=documents[index].metadata["chunk_id"] in selected_ids,
            )
            for rank, index in enumerate(order, start=1)
        ],
    }


def build_trace(question, mode):
    started = perf_counter()
    initialization_started = perf_counter()
    store = open_store(make_embeddings(), INDEX_SPEC)
    corpus = load_corpus(store)
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    initialization_seconds = perf_counter() - initialization_started
    trace = {
        "status": "running",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "question": question,
        "mode": mode,
        "configuration": {
            "final_k": FINAL_K,
            "candidate_k": CANDIDATE_K,
            "rrf_constant": RRF_CONSTANT,
            "corpus_chunks": len(corpus),
            "index_spec": INDEX_SPEC,
        },
        "manifest": manifest,
        "stages": {
            "initialization": {
                "seconds": initialization_seconds,
                "includes": [
                    "embedding_model_setup",
                    "open_chroma_store",
                    "load_corpus",
                    "read_manifest",
                ],
            },
        },
    }

    if mode == "vector":
        final_documents, vector_trace = trace_vector(store, question, FINAL_K)
        trace["stages"]["vector"] = vector_trace
    else:
        bm25_started = perf_counter()
        bm25 = BM25Okapi([tokenize(document.page_content) for document in corpus])
        trace["stages"]["bm25_index"] = {
            "seconds": perf_counter() - bm25_started,
            "documents": len(corpus),
        }

        queries = [question]
        if mode == "hybrid_decompose_rerank":
            queries, decomposition_trace = trace_decomposition(question)
            trace["stages"]["decomposition"] = decomposition_trace

        candidates_by_id = {}
        query_traces = []
        hybrid_k = FINAL_K if mode == "hybrid" else CANDIDATE_K
        for query in queries:
            candidates, query_trace = trace_hybrid(
                store, corpus, bm25, query, hybrid_k
            )
            query_traces.append(query_trace)
            for document in candidates:
                candidates_by_id.setdefault(document.metadata["chunk_id"], document)
        trace["stages"]["retrieval_by_query"] = query_traces
        trace["stages"]["merged_candidates"] = [
            document_record(document, rank=rank)
            for rank, document in enumerate(candidates_by_id.values(), start=1)
        ]

        if mode == "hybrid":
            final_documents = list(candidates_by_id.values())[:FINAL_K]
        else:
            final_documents, reranker_trace = trace_reranker(
                question, list(candidates_by_id.values()), FINAL_K
            )
            trace["stages"]["reranker"] = reranker_trace

    trace["final_contexts"] = [
        document_record(document, rank=rank)
        for rank, document in enumerate(final_documents, start=1)
    ]

    answerer_setup_started = perf_counter()
    answerer = build_answerer()
    trace["stages"]["answerer_setup"] = {
        "seconds": perf_counter() - answerer_setup_started,
    }
    generation_started = perf_counter()
    answer_result = answer_question(
        question,
        RunnableLambda(lambda _: final_documents),
        answerer,
    )
    trace["stages"]["answer_generation"] = {
        "seconds": perf_counter() - generation_started,
    }
    trace["answer_result"] = answer_result

    total_seconds = perf_counter() - started
    trace["status"] = "complete"
    trace["summary"] = timing_summary(trace, total_seconds)
    return trace


def main():
    parser = argparse.ArgumentParser(
        description="Ghi trace retrieval, câu trả lời và timing cho một câu hỏi."
    )
    parser.add_argument("--question", default=DEFAULT_QUESTION)
    parser.add_argument(
        "--mode",
        choices=sorted(SUPPORTED_MODES),
        default=os.getenv("RETRIEVAL_MODE", DEFAULT_MODE),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent
        / "evals"
        / "airflow-components-trace.json",
    )
    args = parser.parse_args()

    payload = {
        "status": "error",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "question": args.question,
        "mode": args.mode,
    }
    try:
        payload = build_trace(args.question, args.mode)
    except Exception as exc:
        payload["error"] = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"Đã ghi trace: {args.output}")


if __name__ == "__main__":
    main()
