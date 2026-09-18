# Phase 05 — Đo chất lượng rồi thêm hybrid search

[Trước](04-heading-va-nguon.md) · [Lộ trình](README.md) · [Tiếp](06-chat-tren-mkdocs.md)

## Mục tiêu

Phase 04 đã có nguồn. Bây giờ đo xem retriever có chọn đúng section không, rồi thử thêm tìm từ khóa. Giữ nguyên corpus, cách chunk, embedding, LLM và prompt để so sánh tác động của **retrieval**.

Vector search có thể hiểu cách diễn đạt khác nhau, nhưng tên như `shared_buffers`, `B+tree` hoặc `LocalExecutor` cũng cần khớp chính xác. Hybrid ở đây kết hợp:

```text
                   → vector search: tối đa 8 đoạn ─┐
câu hỏi ───────────┤                              ├→ RRF → 4 đoạn → LLM
                   → BM25: tối đa 8 đoạn ──────────┘
```

Không mặc định hybrid tốt hơn. Nếu baseline tốt hơn trên câu hỏi quan trọng, giữ baseline và tìm nguyên nhân.

## 1. Tạo bộ câu hỏi có nhãn

Tạo thư mục `backend/evals`, rồi tạo `backend/evals/questions.jsonl`. Mỗi dòng là một JSON độc lập:

```jsonl
{"id":"airflow-critical","question":"Vì sao các scheduler cần Critical Section?","expected":[{"source":"airflow/architecture.md","heading_contains":"Critical Section"}]}
{"id":"airflow-local","question":"LocalExecutor thực thi task ở đâu?","expected":[{"source":"airflow/architecture.md","heading_contains":"LocalExecutor"}]}
{"id":"pg-schema","question":"Một schema có thư mục riêng trên ổ đĩa không?","expected":[{"source":"postgres/postgres.md","heading_contains":"Vị trí lưu trữ của schema"}]}
{"id":"pg-buffer","question":"shared_buffers dùng để làm gì?","expected":[{"source":"postgres/postgres.md","heading_contains":"shared_buffers"}]}
{"id":"index-prefix","question":"Vì sao thứ tự cột trong composite index quan trọng?","expected":[{"source":"index/index.md","heading_contains":"Quy tắc tiền tố trái"}]}
{"id":"index-plus","question":"B+tree tổ chức nút lá thế nào?","expected":[{"source":"index/index.md","heading_contains":"B+tree: cấu trúc page"}]}
{"id":"disk-compare","question":"Shared-disk và shared-nothing vận hành khác nhau ra sao?","expected":[{"source":"architecture/shared-disk-vs-shared-nothing.md","heading_contains":"Shared-disk vận hành"},{"source":"architecture/shared-disk-vs-shared-nothing.md","heading_contains":"Shared-nothing vận hành"}]}
{"id":"outside-weather","question":"Thời tiết Paris ngay bây giờ thế nào?","expected":[]}
{"id":"outside-private","question":"Mật khẩu database production của tôi là gì?","expected":[]}
```

Nhãn chỉ ra section kỳ vọng, không phải câu trả lời mẫu. Hãy đọc section để kiểm tra nhãn trước khi đo. Một câu hỏi có thể có nhiều section hợp lệ; bổ sung nhãn nếu retriever tìm được nguồn khác thực sự trả lời được câu hỏi.

Chín câu chỉ đủ smoke test. Mở rộng lên khoảng 30–50 câu, thêm tiếng Việt không dấu, diễn đạt gián tiếp, câu có nhiều chủ đề và câu ngoài phạm vi. Giữ một phần câu hỏi chưa dùng khi điều chỉnh tham số để hạn chế tối ưu quá mức trên tập nhỏ.

### Tập phát triển và tập kiểm tra giữ riêng

Chia câu hỏi thành `evals/dev.jsonl` để điều chỉnh và `evals/heldout.jsonl` để nghiệm thu, ví dụ 30 câu và 10 câu. Các biến thể diễn đạt của cùng một câu phải ở cùng tập; không dùng câu giữ riêng để chọn model hoặc tham số. Chín câu mẫu ở trên chỉ là điểm khởi đầu, không phải benchmark đầy đủ.

Mỗi câu bổ sung các trường sau để người chấm kiểm tra bằng chứng, không chỉ tên heading:

```json
{
  "id": "pg-buffer-evidence",
  "question": "shared_buffers dùng để làm gì?",
  "category": "term",
  "expected": [{"source": "postgres/postgres.md", "heading_contains": "shared_buffers"}],
  "expected_answer": "Vùng bộ nhớ dùng chung để cache các page dữ liệu PostgreSQL.",
  "required_evidence": ["Chứa các page dữ liệu", "Được các backend PostgreSQL dùng chung"],
  "should_abstain": false
}
```

Đối chiếu đáp án và từng ý bằng chứng với bài thật trước khi dùng. `required_evidence` là các ý để chấm thủ công, không phải chuỗi bắt buộc model phải lặp nguyên văn. Với câu ngoài phạm vi, dùng `expected=[]`, `should_abstain=true` và ghi rõ lý do trong `expected_answer`.

Phân bố đủ nhóm: thuật ngữ chính xác, không dấu, diễn đạt gián tiếp, so sánh nhiều section, nhiều bài, ngoài phạm vi. Đánh dấu `category="multi_part"` cho nhóm thử decomposition ở phase 08. Câu đơn giản vẫn phải nằm trong tập kiểm tra để phát hiện hồi quy.

## 2. Tạo retriever có hai chế độ

Tại `backend`:

```bash
uv add rank-bm25
```

Tạo `backend/retrieval.py`:

```python
import re
from collections import defaultdict

from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda
from rank_bm25 import BM25Okapi


def tokenize(text):
    # Giữ underscore và các tên như B+tree, B-tree; case-insensitive.
    return re.findall(r"\w+(?:[+_-]\w+)*\+*", text.casefold())


def make_retriever(store, mode="vector", k=4, candidate_k=8):
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
        return [by_id[chunk_id] for chunk_id in ordered[:k]]

    return RunnableLambda(search)
```

RRF cộng điểm dựa trên **thứ hạng**, tránh cộng trực tiếp điểm BM25 với khoảng cách vector. Hằng số 60 là một lựa chọn ban đầu, không phải ngưỡng tin cậy. Hai nhánh dùng cùng chunk và deduplicate bằng `chunk_id`. [Bài báo RRF của tác giả](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf), [rank_bm25](https://github.com/dorianbrown/rank_bm25)

Tokenizer BM25 ở đây chưa tách từ tiếng Việt nhiều âm tiết và chưa xử lý không dấu. Đây là giới hạn cần đo, không phải vấn đề sẽ được vector search tự động giải quyết hoàn toàn. BM25 được tạo lại trong RAM khi backend startup; chưa cần database thứ hai cho corpus nhỏ này.

## 3. Tạo `backend/evaluate.py`

```python
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
    parser.add_argument("--mode", choices=["vector", "hybrid"], default="vector")
    parser.add_argument("--dataset", type=Path, default=Path(__file__).resolve().parent / "evals" / "questions.jsonl")
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
```

Tại `backend`, với chỉ mục phase 04 đã tạo:

```bash
uv run python evaluate.py --mode vector --run-id phase05-vector > evals/vector.jsonl
uv run python evaluate.py --mode hybrid --run-id phase05-hybrid > evals/hybrid.jsonl
```

Hai lệnh dùng cùng snapshot; không ingest giữa hai lần đo. Script không gọi LLM nên bạn có thể sửa retrieval mà chưa phải chờ generation. Thời gian này không bao gồm startup, và lần query đầu có thể chịu ảnh hưởng warm-up; đây chưa phải benchmark tải hệ thống.

Ý nghĩa chỉ số:

- **Hit@4:** có ít nhất một section kỳ vọng trong bốn kết quả hay không.
- **Section recall@4:** bao nhiêu section kỳ vọng được tìm thấy; hữu ích cho câu so sánh cần hai nguồn.
- **MRR@4:** ưu tiên tìm nguồn đúng ở vị trí đầu.

Đây là độ đúng ở mức section được gán nhãn, không chứng minh chunk chứa đầy đủ bằng chứng. Một chunk cùng heading nhưng thiếu câu quan trọng vẫn có thể được tính là hit; hãy đọc các trường hợp đó.

## 4. Nối chế độ tìm kiếm vào backend

Thay toàn bộ `build_retriever` trong `backend/rag.py`:

```python
def build_retriever():
    from retrieval import make_retriever
    from storage import open_store

    store = open_store(make_embeddings(), INDEX_SPEC)
    return make_retriever(
        store,
        mode=os.getenv("RETRIEVAL_MODE", "vector"),
        k=4,
    )
```

Baseline `vector` vẫn là mặc định. Nếu kết quả đánh giá ủng hộ hybrid, restart backend bằng:

```bash
RETRIEVAL_MODE=hybrid uv run uvicorn app:app --host 127.0.0.1 --port 8001
```

Không cần ingest lại vì embedding và chunk không thay đổi. `inspect_retrieval.py` cũng có thể chạy với cùng biến môi trường.

## 5. Đánh giá câu trả lời riêng

Gọi `/chat` cho cùng bộ câu hỏi với từng chế độ. Lưu câu trả lời và nguồn, rồi chấm thủ công:

| Tiêu chí | Cách chấm |
| --- | --- |
| Đúng nội dung | 0: sai; 1: đúng một phần; 2: đúng và đủ cho câu hỏi |
| Bám nguồn | Từng nhận định chính có được đoạn trích hỗ trợ không? |
| Citation | Mã nguồn đúng đoạn và URL đến đúng mục không? |
| Từ chối | Các câu không có dữ liệu có được từ chối đúng không? |
| Thời gian | Đo toàn bộ request, tách khỏi thời gian retrieval |

Hai câu `expected=[]` không được tính vào recall: retriever top-k vẫn thường trả những đoạn gần nhất dù không đoạn nào đủ để trả lời. Khả năng từ chối cần đo ở câu trả lời, không suy ra từ việc có kết quả retrieval.

### Lưu đầu ra từ đúng đường trả lời của backend

Tạo `backend/evaluate_answers.py`. Script gọi cùng `build_retriever`, `build_answerer`, `answer_question` mà API sử dụng; không xây một pipeline đánh giá riêng. Đo này bỏ qua HTTP và UI, nên vẫn phải kiểm tra `/chat` để đo độ trễ người dùng thấy.

```python
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
            "required_evidence": case.get("required_evidence", []),
            "should_abstain": case.get("should_abstain", not case["expected"]),
            "seconds": perf_counter() - start, **captured, **result,
        }, ensure_ascii=False))


if __name__ == "__main__":
    main()
```

Tại `backend`, sau khi đã tạo tập phát triển:

```bash
RETRIEVAL_MODE=vector uv run python evaluate_answers.py --dataset evals/dev.jsonl --run-id phase05-vector-answers > evals/vector-answers.jsonl
RETRIEVAL_MODE=hybrid uv run python evaluate_answers.py --dataset evals/dev.jsonl --run-id phase05-hybrid-answers > evals/hybrid-answers.jsonl
```

Mỗi nhận định chính phải được một context thực sự hỗ trợ. Tính tỷ lệ nhận định có bằng chứng và tỷ lệ từ chối đúng trên câu ngoài phạm vi; đồng thời đếm số câu có đủ dữ liệu nhưng bị từ chối. `invalid_citation` là lỗi tạo câu trả lời, không được tính là từ chối đúng. Mã `[S1]` hợp lệ vẫn có thể dẫn tới đoạn không hỗ trợ nhận định.

### Chấm ngữ nghĩa và quản lý lần chạy

Có thể dùng LLM-as-a-judge hoặc RAGAS để hỗ trợ chấm **context precision/recall**. Hai chỉ số đó đánh giá context, không tự chứng minh đáp án đúng hay bám nguồn. Chấm câu trả lời cần truyền cả đáp án sinh ra, context và đáp án kỳ vọng; đọc lại thủ công các ca sai và một mẫu ca được chấm đúng. Không bắt buộc cài RAGAS trong phase này.

Mỗi lần chạy lưu thêm file ghi chú cạnh JSONL: Git commit của tài liệu/code, hash tập câu hỏi, `backend/uv.lock`, model và revision embedding/reranker/LLM, cấu hình retrieval, prompt, thiết bị, số request đồng thời, warm-up và số lần lặp. Manifest đã ghi corpus/index spec; nó chưa thay thế thông tin về model weights và môi trường. Không ghi đè kết quả lần trước khi đổi tham số.

Đo trên cùng snapshot, cùng top-k cuối là 4, cùng câu hỏi và LLM. Báo cáo theo từng nhóm và toàn bộ tập; ghi trung bình/p95, tách startup và lượt đầu khỏi các lượt đã warm-up khi benchmark chính thức. P95 trên vài chục câu chỉ mang tính tham khảo. Nếu dùng checkpoint, khóa theo cấu hình + corpus hash + dataset hash, không chỉ theo nội dung câu hỏi.

## 6. Quyết định sau khi đo

- Vector bỏ sót thuật ngữ, hybrid cải thiện mà không làm hỏng câu hỏi chính: dùng hybrid.
- Đúng bài nhưng sai đoạn: xem lại chunk/heading trước khi tăng `k`.
- Đúng đoạn nhưng câu trả lời sai: xem prompt và giới hạn model, không sửa retrieval vô cớ.
- Hai nhánh đã tìm được nguồn nhưng xếp hạng kém: lúc đó mới thử [phase 07 — reranker](07-reranker.md).

**Hoàn thành phase khi:** có hai báo cáo thực tế và giải thích được vì sao chọn vector hoặc hybrid. Không ghi số liệu “đẹp” vào tài liệu trước khi chạy.

Sau khi chọn cấu hình trên tập phát triển, chạy lại trên `--dataset evals/heldout.jsonl` với `--run-id` mới. Chỉ tiếp tục [phase 08](08-tach-cau-hoi.md) nếu nhóm câu nhiều vế vẫn thiếu bằng chứng. Mục tiêu là cải thiện ca sai đã quan sát, không thêm thành phần chỉ vì repo tham khảo có chúng.
