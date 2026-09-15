# Phase 07 — Reranker tùy chọn sau hybrid search

[Trước](06-chat-tren-mkdocs.md) · [Lộ trình](README.md) · [Tiếp, tùy chọn](08-tach-cau-hoi.md)

## Khi nào nên làm

Chỉ thử khi phase 05 cho thấy các đoạn đủ bằng chứng có trong tập ứng viên nhưng xếp thấp. Nếu retrieval không tìm được đoạn đó, sửa corpus/chunking hoặc cách truy vấn trước: reranker không tạo ra nguồn mới.

Ý tưởng tham khảo từ [retriever LegalTech](https://github.com/HoangKhang226/Vietnam-Enterprise-LegalTech/blob/3aea00e0cccd6e46816c6a738302e673f460af51/src/retrieval/retriever.py): lấy nhiều ứng viên, rồi chấm lại từng cặp câu hỏi–đoạn. Bài này giữ Chroma, E5, Qwen và hợp đồng `/chat` của phase 04. Không sao chép điểm trộn hoặc ngưỡng “tin cậy” của repo tham khảo.

## 1. Cấu hình thí nghiệm

Luồng mới: BM25 và vector mỗi nhánh tối đa 12 đoạn; RRF giữ tối đa 12 ứng viên; reranker chọn tối đa 4 đoạn. So sánh với hybrid cùng 12 ứng viên nhưng không rerank, để tránh nhầm lợi ích từ mở rộng retrieval với lợi ích của reranker.

Dùng `BAAI/bge-reranker-v2-m3` làm **ứng viên thử nghiệm đa ngôn ngữ**, không phải model đã được chứng minh tốt nhất cho corpus này. Reranker chấm cặp văn bản, khác embedding E5 đang tạo vector cho Chroma. Không cần ingest lại khi chỉ thay reranker. [Model card BGE](https://huggingface.co/BAAI/bge-reranker-v2-m3)

`sentence-transformers` đã có từ phase 01. Lần đầu tải thêm weights; CPU có thể chậm và tăng RAM đáng kể. Bắt đầu batch nhỏ, chỉ một process backend. Lưu revision model thực tế và lockfile cùng báo cáo trước khi so sánh các lần chạy.

## 2. Tách hàm retrieval nền

Trong `backend/retrieval.py` của phase 05, đổi **tên** hàm `make_retriever` thành `make_base_retriever`; giữ thân hàm và chữ ký còn lại:

```python
def make_base_retriever(store, mode="vector", k=4, candidate_k=8):
    # Giữ toàn bộ thân hàm make_retriever ở phase 05.
    ...
```

Khối trên chỉ minh họa đổi tên, không thay thân hàm bằng `...`. Nếu đang dùng bản phase 05 cũ chưa có `candidate_k`, cập nhật theo file phase 05 hiện tại: thay số 8 trong hai nhánh retrieval bằng `candidate_k` và kiểm tra `1 <= k <= candidate_k`.

## 3. Tạo `backend/reranking.py`

```python
import math
from threading import Lock

from sentence_transformers import CrossEncoder

RERANKER_MODEL = "BAAI/bge-reranker-v2-m3"
RERANKER_MAX_LENGTH = 1024


class Reranker:
    def __init__(self):
        self.model = CrossEncoder(
            RERANKER_MODEL,
            device="cpu",
            max_length=RERANKER_MAX_LENGTH,
        )
        self.lock = Lock()

    def select(self, question, documents, k=4):
        if k < 1:
            raise ValueError("k phải dương")
        unique = {}
        for doc in documents:
            unique.setdefault(doc.metadata["chunk_id"], doc)
        documents = list(unique.values())
        if not documents:
            return []
        pairs = [(question, doc.page_content) for doc in documents]
        # Không để model âm thầm cắt mất bằng chứng khi chấm điểm.
        for query, passage in pairs:
            ids = self.model.tokenizer(
                query, passage, truncation=False, add_special_tokens=True
            )["input_ids"]
            if len(ids) > RERANKER_MAX_LENGTH:
                raise ValueError("Cặp câu hỏi–đoạn vượt ngân sách token reranker")
        with self.lock:
            values = self.model.predict(pairs, batch_size=2, show_progress_bar=False)
        scores = [float(value) for value in values]
        if len(scores) != len(documents) or not all(math.isfinite(s) for s in scores):
            raise RuntimeError("Reranker trả điểm không hợp lệ")
        order = sorted(
            range(len(documents)),
            key=lambda index: (-scores[index], documents[index].metadata["chunk_id"]),
        )
        return [documents[index] for index in order[:k]]
```

`CrossEncoder.predict` nhận các cặp văn bản và trả điểm để xếp hạng. Giới hạn 1024 ở đây là ngân sách thí nghiệm; E5 và reranker có tokenizer khác nhau nên phải kiểm tra riêng. Nếu vượt, kiểm tra câu hỏi/chunk, điều chỉnh ngân sách phù hợp model và phần cứng rồi chạy lại đánh giá. [API CrossEncoder](https://www.sbert.net/docs/package_reference/cross_encoder/model.html)

Chỉ dùng thứ tự điểm trong cùng một câu hỏi. Không diễn giải `0.8` là 80% chắc chắn đúng, không cộng trực tiếp với BM25/RRF và không dùng điểm để tự bật web search. Lỗi tải/chạy reranker phải được nhìn thấy: startup lỗi hoặc request trả 503 theo handler hiện tại. Không âm thầm fallback khiến báo cáo mang nhãn reranker nhưng thực chất chỉ chạy hybrid.

## 4. Thêm factory dùng chung cho API và đánh giá

Thêm hằng số và hàm dưới đây vào cuối `backend/retrieval.py`, sau `make_base_retriever`:

```python
CANDIDATE_K = 12


def make_retriever(store, mode="vector", k=4):
    if mode in {"vector", "hybrid"}:
        return make_base_retriever(store, mode, k=k, candidate_k=CANDIDATE_K)
    if mode != "hybrid_rerank":
        raise ValueError("mode phải là vector, hybrid hoặc hybrid_rerank")
    from reranking import Reranker

    candidates = make_base_retriever(
        store, "hybrid", k=CANDIDATE_K, candidate_k=CANDIDATE_K
    )
    reranker = Reranker()
    return RunnableLambda(
        lambda question: reranker.select(question, candidates.invoke(question), k=k)
    )
```

Factory chỉ khởi tạo reranker khi chọn `hybrid_rerank`; `build_retriever` vẫn được gọi một lần trong lifespan. `Lock` chỉ tuần tự hóa inference reranker, không phải giới hạn tải cho toàn hệ thống. Không đổi `build_retriever` trong `rag.py`, `answering.py` hoặc response frontend.

## 5. So sánh trên cùng đường code

Trong `backend/evaluate.py`, đổi `choices=["vector", "hybrid"]` thành `choices=["vector", "hybrid", "hybrid_rerank"]`. Script đã import cùng `make_retriever` mà backend sử dụng.

Tại `backend`, chạy lại cả ba chế độ sau khi sửa factory. Không so trực tiếp kết quả hybrid 8 ứng viên của lần trước với reranker 12 ứng viên:

```bash
uv run python evaluate.py --mode vector --dataset evals/dev.jsonl --run-id phase07-vector > evals/phase07-vector.jsonl
uv run python evaluate.py --mode hybrid --dataset evals/dev.jsonl --run-id phase07-hybrid > evals/phase07-hybrid.jsonl
uv run python evaluate.py --mode hybrid_rerank --dataset evals/dev.jsonl --run-id phase07-rerank > evals/phase07-rerank.jsonl
RETRIEVAL_MODE=hybrid_rerank uv run python evaluate_answers.py --dataset evals/dev.jsonl --run-id phase07-rerank-answers > evals/phase07-rerank-answers.jsonl
RETRIEVAL_MODE=hybrid uv run python evaluate_answers.py --dataset evals/dev.jsonl --run-id phase07-hybrid-answers > evals/phase07-hybrid-answers.jsonl
```

Thêm vào ghi chú lần chạy: `candidate_k=12`, `k=4`, model/revision reranker, `max_length=1024`, batch size 2 và CPU. `--run-id` là nhãn tra cứu, không tự khóa hoặc kiểm tra cấu hình. Thay model phải ghi model mới và chạy lại các phép so sánh liên quan.

Đọc các ca tăng/giảm section recall@4, MRR@4 và bằng chứng trong context. Reranker không được coi là tốt hơn chỉ vì MRR tăng trong khi nguồn thứ hai của câu so sánh biến mất. Đo thời gian retrieval gồm rerank; đo riêng generation và toàn request bằng quy trình phase 05. Nếu muốn tách thời gian hybrid/rerank, đặt bộ đo quanh `candidates.invoke` và `reranker.select` ở factory, không dựng pipeline khác trong script đánh giá.

## 6. Bật hoặc quay lại baseline

Chỉ bật sau khi bộ giữ riêng xác nhận chất lượng tốt hơn, tỷ lệ từ chối/độ bám nguồn không giảm và độ trễ chấp nhận được:

```bash
RETRIEVAL_MODE=hybrid_rerank uv run uvicorn app:app --host 127.0.0.1 --port 8001
```

Nếu không có lợi, dừng backend rồi chạy lại với `RETRIEVAL_MODE=hybrid` hoặc `vector` đã chọn. Không cần ingest lại. Vẫn giữ bài học về reranker trong tài liệu dù cấu hình phục vụ không dùng nó.

Bốn chunk cuối không bảo đảm vừa context Qwen: kiểm tra ngân sách LLM như phase 04, tính cả prompt/output. Không đưa toàn bộ 12 ứng viên vào generation để “tận dụng” retrieval rộng.

**Hoàn thành phase khi:** có báo cáo ba chế độ trên cùng snapshot, cùng bốn đoạn cuối; đã kiểm tra câu ngoài phạm vi, điểm không hợp lệ, lỗi model, cặp quá dài và CPU latency. Chưa chạy weights/benchmark thì ghi rõ chưa kiểm chứng, không điền số liệu dự đoán.
