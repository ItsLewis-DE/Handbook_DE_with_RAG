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