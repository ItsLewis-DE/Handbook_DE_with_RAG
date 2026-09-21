import json
import re
import unicodedata
from collections import defaultdict

from langchain_core.documents import Document


def make_outlines(sections):
    children = defaultdict(list)
    for section in sections:
        children[section.metadata["parent_id"]].append(section)
    outlines = []
    for section in sections:
        metadata = section.metadata
        direct = sorted(
            children[metadata["section_id"]],
            key=lambda child: child.metadata["sibling_order"],
        )
        lines = [
            f"Bài viết: {metadata['title']}",
            f"Mục: {metadata['heading']}",
            "Phạm vi: cách bài viết tổ chức heading; không phải taxonomy chuẩn "
            "hay số tiến trình/component bắt buộc của mọi phiên bản.",
            f"Danh sách đầy đủ {len(direct)} mục con trực tiếp, theo thứ tự bài:",
        ]
        lines.extend(f"{i}. {child.metadata['label']}" for i, child in enumerate(direct, 1))
        if not direct:
            lines.append("Không có heading con trực tiếp; điều này không chứng minh "
                         "đối tượng ngoài thực tế không có thành phần con.")
        outlines.append(Document(page_content="\n".join(lines), metadata={
            **metadata, "record_type": "outline", "outline_complete": True,
            "chunk_index": 0, "chunk_count": 1,
            "chunk_id": f"{metadata['section_id']}:outline",
            "child_count": len(direct),
            "child_ids_json": json.dumps([d.metadata["section_id"] for d in direct]),
        }))
    return outlines


#Dùng để xóa dấu tiếng việt
def fold(text):
    text = unicodedata.normalize("NFD", text.casefold().replace("đ", "d"))
    return "".join(c for c in text if unicodedata.category(c) != "Mn")


STOP = set("trong co bao nhieu cac nhung gom la gi va cua ve cho hay liet ke "
           "tom tat tong quan bai viet muc theo nao phan duoc thanh "
           "how many list summarize overview the in of are does have".split())


def terms(text):
    text = fold(text)
    text = re.sub(r"\bthanh phan\b", "component", text)
    text = re.sub(r"\bcomponents\b", "component", text)
    return set(re.findall(r"[a-z0-9]+", text)) - STOP


def overview_intent(question):
    q = fold(question)
    if re.search(r"\b(bao nhieu|how many)\b", q):
        return "count"
    if re.search(r"\b(liet ke|gom nhung|cac .+ la gi|list)\b", q):
        return "list"
    if re.search(r"\b(tom tat|tong quan|summarize|overview)\b", q):
        return "summary"
    return None


class OutlineCatalog:
    def __init__(self, outlines, chunks):
        self.nodes = {d.metadata["section_id"]: d for d in outlines}
        if len(self.nodes) != len(outlines):
            raise ValueError("section_id trùng")
        self.children = defaultdict(list)
        self.bodies = defaultdict(list)
        for node in outlines:
            m = node.metadata
            parent_id = m["parent_id"]
            if parent_id:
                parent = self.nodes[parent_id].metadata
                if parent["source"] != m["source"] or parent["level"] >= m["level"]:
                    raise ValueError("Quan hệ cha/con không hợp lệ")
                if parent["section_order"] >= m["section_order"]:
                    raise ValueError("Cha phải đứng trước con")
                self.children[parent_id].append(m["section_id"])
        for sid, node in self.nodes.items():
            self.children[sid].sort(key=lambda c: self.nodes[c].metadata["sibling_order"])
            direct = self.children[sid]
            if direct != json.loads(node.metadata["child_ids_json"]):
                raise ValueError("Outline không khớp danh sách con")
            if len(direct) != node.metadata["child_count"]:
                raise ValueError("Sai child_count")
        for chunk in chunks:
            m = chunk.metadata
            node = self.nodes[m["section_id"]].metadata
            if m["source"] != node["source"] or m["parent_id"] != node["parent_id"]:
                raise ValueError("Chunk và outline không cùng section")
            self.bodies[m["section_id"]].append(chunk)
        for bodies in self.bodies.values():
            bodies.sort(key=lambda d: d.metadata["chunk_index"])

    def resolve(self, question):
        # Định tuyến bảo thủ cho corpus nhỏ, không dùng LLM để suy ra cây.
        intent = overview_intent(question)
        query = terms(question)
        if not intent or not query:
            return None
        candidates = []
        for sid, node in self.nodes.items():
            if not self.children[sid]:
                continue
            m = node.metadata
            title_terms = terms(m["title"])
            label_terms = terms(m["label"])
            target = query - title_terms
            #Đảm bảo các từ chính trong query nằm trong heading
            if not query <= (title_terms | label_terms):
                continue
            if not target:
                if not m["is_page_root"]:
                    continue
                score = (0, 0)
            else:
                if m["is_page_root"] or not target <= label_terms:
                    continue
                score = (len(target), -len(label_terms - target - title_terms))
            candidates.append((score, sid))
        candidates.sort(reverse=True)
        if not candidates or (len(candidates) > 1 and candidates[0][0] == candidates[1][0]):
            return None
        return intent, candidates[0][1]

    def subtree(self, section_id):
        yield section_id
        for child in self.children[section_id]:
            yield from self.subtree(child)

    def structural_answer(self, section_id):
        node = self.nodes[section_id]
        labels = [self.nodes[c].metadata["label"] for c in self.children[section_id]]
        return (
            f"Theo bài “{node.metadata['title']}”, mục “{node.metadata['heading']}” "
            f"có {len(labels)} mục con trực tiếp: {', '.join(labels)}. "
            "Đây là cách phân mục của bài viết, không khẳng định danh sách thành phần "
            "chuẩn cho mọi phiên bản."
        )

    def expand(self, question, section_id, intent, fits, max_chunks=24):
        # Outline đầy đủ luôn đứng đầu, không tham gia top-k rerank body.
        root = self.nodes[section_id].model_copy(deep=True)
        root.metadata.update(retrieval_intent=intent, selected_outline=True)
        if intent in {"count", "list"}:
            root.metadata["structural_answer"] = self.structural_answer(section_id)
        selected = [root]
        report = {
            "route": "outline", "intent": intent, "section_id": section_id,
            "direct_child_ids": self.children[section_id],
            "covered_child_ids": [], "missing_child_ids": [],
            "budget_rejected": [], "outline_complete": True,
        }
        if not fits(question, selected):
            report.update(reason="outline_over_budget", outline_complete=False)
            return [], report
        # Một hàng đợi cho mỗi nhánh: body cha, rồi body các hậu duệ.
        # Scheduler không có body vẫn tìm được body của HA/parse/... trong cây.
        branches = self.children[section_id]
        queues = {
            child: [d for sid in self.subtree(child) for d in self.bodies[sid]]
            for child in branches
        }
        #Kết quả của queues là một Dictionary: { ID_nhánh: [danh_sách_mẩu_text] }
        covered = set()
        seen_sections = set()
        for child in branches:
            for doc in queues[child]:
                if len(selected) >= max_chunks:
                    break
                if fits(question, selected + [doc]):
                    selected.append(doc)
                    seen_sections.add(doc.metadata["section_id"])
                    covered.add(child)
                    break
                report["budget_rejected"].append(doc.metadata["chunk_id"])
        # Sau vòng phủ nhánh mới thêm body của mục cha và chi tiết khác.
        extra = list(self.bodies[section_id])
        for child in branches:
            extra.extend(queues[child])
        for doc in extra:
            if len(selected) >= max_chunks:
                break
            sid = doc.metadata["section_id"]
            if sid in seen_sections:
                continue
            if fits(question, selected + [doc]):
                selected.append(doc)
                seen_sections.add(sid)
        report["covered_child_ids"] = [c for c in branches if c in covered]
        report["missing_child_ids"] = [c for c in branches if c not in covered]
        report["selected_chunk_ids"] = [d.metadata["chunk_id"] for d in selected]
        return selected, report