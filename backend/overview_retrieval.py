from threading import Lock


class OverviewRetriever:
    def __init__(self, catalog, detail_factory, budget):
        self.catalog = catalog
        self.detail_factory = detail_factory
        self.budget = budget
        self._detail = None
        self._lock = Lock()

    def retrieve_with_trace(self, question):
        resolved = self.catalog.resolve(question)
        if resolved:
            intent, section_id = resolved
            passages, report = self.catalog.expand(
                question, section_id, intent, self.budget.fits,
            )
        else:
            # Reranker/decomposer chỉ khởi tạo nếu thực sự cần nhánh chi tiết.
            with self._lock:
                if self._detail is None:
                    self._detail = self.detail_factory()
            passages = self.budget.pack(question, self._detail.invoke(question))
            report = {"route": "detail", "reason": "no_unambiguous_outline"}
        report["context_input_tokens"] = self.budget.input_tokens(question, passages)
        report["selected_chunk_ids"] = [d.metadata["chunk_id"] for d in passages]
        return passages, report

    def invoke(self, question):
        return self.retrieve_with_trace(question)[0]