import argparse
import json
import os
from pathlib import Path
from time import perf_counter

from langchain_core.runnables import RunnableLambda

from answering import answer_question, build_answerer
from rag import build_retriever
from storage import MANIFEST_PATH


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    retriever = build_retriever()
    answerer = build_answerer()
    print(json.dumps({
        "run_id": args.run_id,
        "mode": os.getenv("RETRIEVAL_MODE", "vector"),
        "manifest": json.loads(MANIFEST_PATH.read_text(encoding="utf-8")),
    }, ensure_ascii=False))
    cases = [json.loads(line) for line in args.dataset.read_text(encoding="utf-8").splitlines()
             if line.strip()]
    for case in cases:
        captured = {}

        def retrieve(question):
            start = perf_counter()
            hits = retriever.invoke(question)
            captured["retrieval_seconds"] = perf_counter() - start
            captured["contexts"] = [
                {"text": doc.page_content, "metadata": doc.metadata} for doc in hits
            ]
            return hits

        start = perf_counter()
        result = answer_question(case["question"], RunnableLambda(retrieve), answerer)
        print(json.dumps({
            "id": case["id"], "question": case["question"],
            "expected_answer": case.get("expected_answer"),
            **result,
            "required_evidence": case.get("required_evidence", []),
            "should_abstain": case.get("should_abstain", not case["expected"]),
            "seconds": perf_counter() - start, **captured,
        }, ensure_ascii=False))


if __name__ == "__main__":
    main()