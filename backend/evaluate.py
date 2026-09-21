import argparse
import json
import math
from pathlib import Path
from time import perf_counter

from rag import INDEX_SPEC, make_embeddings
from retrieval import make_retriever
from storage import MANIFEST_PATH, open_store


def matches(document, expected):
    return (
        document.metadata["source"] == expected["source"]
        and expected["heading_contains"].casefold()
        in document.metadata["heading"].casefold()
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["vector", "hybrid","hybrid_rerank","hybrid_decompose_rerank"], default="vector")
    parser.add_argument("--dataset", type=Path, default=Path(__file__).resolve().parent / "evals" / "dev.jsonl")
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    store = open_store(make_embeddings(), INDEX_SPEC)
    retriever = make_retriever(store, mode=args.mode, k=4)
    path = args.dataset
    print(json.dumps({
        "run_id": args.run_id, "mode": args.mode, "dataset": str(path),
        "manifest": json.loads(MANIFEST_PATH.read_text(encoding="utf-8")),
        "k": 4,
    }, ensure_ascii=False))
    cases = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
             if line.strip()]

    # Fail sớm nếu nhãn trỏ đến heading không tồn tại trong snapshot đang đo.
    from langchain_core.documents import Document
    data = store.get(include=["documents", "metadatas"])
    corpus = [Document(page_content=t, metadata=m)
              for t, m in zip(data["documents"], data["metadatas"])]
    for case in cases:
        for expected in case["expected"]:
            if not any(matches(doc, expected) for doc in corpus):
                raise RuntimeError(f"Nhãn không tồn tại: {case['id']} {expected}")

    hit_rates = []
    recalls = []
    reciprocal_ranks = []
    elapsed = []
    for case in cases:
        start = perf_counter()
        hits = retriever.invoke(case["question"])
        duration = perf_counter() - start
        elapsed.append(duration)
        expected = case["expected"]
        record = {
            "id": case["id"], "mode": args.mode, "seconds": round(duration, 3),
            "retrieved": [doc.metadata["url"] for doc in hits],
            "contexts": [{"text": doc.page_content, "metadata": doc.metadata} for doc in hits],
        }
        if expected:
            covered = sum(any(matches(doc, item) for doc in hits) for item in expected)
            first = next((rank for rank, doc in enumerate(hits, start=1)
                          if any(matches(doc, item) for item in expected)), None)
            hit = int(covered > 0)
            recall = covered / len(expected)
            rr = 1 / first if first is not None else 0
            hit_rates.append(hit)
            recalls.append(recall)
            reciprocal_ranks.append(rr)
            record.update(hit_at_4=hit, section_recall_at_4=recall, reciprocal_rank=rr)
        else:
            record["note"] = "Ngoài phạm vi: đánh giá từ chối ở bước generation."
        print(json.dumps(record, ensure_ascii=False))

    if not hit_rates:
        raise RuntimeError("Cần ít nhất một câu hỏi có nhãn nguồn.")
    print(json.dumps({
        "summary": True,
        "mode": args.mode,
        "hit_at_4": sum(hit_rates) / len(hit_rates),
        "section_recall_at_4": sum(recalls) / len(recalls), 
        "mrr_at_4": sum(reciprocal_ranks) / len(reciprocal_ranks),
        "mean_retrieval_seconds": sum(elapsed) / len(elapsed),
        "p95_retrieval_seconds": sorted(elapsed)[math.ceil(0.95 * len(elapsed)) - 1],
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()