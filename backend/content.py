import hashlib
from pathlib import Path
from tempfile import TemporaryDirectory

from bs4 import BeautifulSoup
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from mkdocs.commands.build import build
from mkdocs.config import load_config
from mkdocs.structure.files import get_files
from transformers import AutoTokenizer

HEADINGS = {f"h{level}" for level in range(1, 7)}


def stable_id(source, key):
    return hashlib.sha256(f"{source}\0{key}".encode()).hexdigest()[:24]


def article_blocks(container):
    for node in container.children:
        name = getattr(node, "name", None)
        if name is None or name == "hr":
            continue
        if name not in HEADINGS and node.find(list(HEADINGS)) is not None:
            yield from article_blocks(node)
        else:
            yield node

def extract_sections(html, source, page_url):
    soup = BeautifulSoup(html, "html.parser")
    article = soup.select_one("article.md-content__inner")
    if article is None:
        raise RuntimeError(f"Không tìm thấy vùng bài viết: {source}")
    for node in article.select(".headerlink"):
        node.decompose()
    title_node = article.find("h1")
    title = title_node.get_text(" ", strip=True) if title_node else source
    for node in article.select(
        "header, footer, script, style, "
        ".airflow-opening-comic, .airflow-closing-comic"
    ):
        node.decompose()

    # Page root là node kỹ thuật; không giả làm một heading trong bài.
    root = Document(page_content="", metadata={
        "source": source, "title": title, "heading": title,
        "label": title, "url": page_url, "anchor": "",
        "section_id": stable_id(source, "page"), "parent_id": "",
        "level": 0, "section_order": 0, "sibling_order": 0,
        "is_page_root": True, "record_type": "section",
    })
    sections = [root] #Lưu tất cả các Document
    stack = [root] #Dùng để làm heading
    child_counts = {}
    seen_ids = {root.metadata["section_id"]}
    current = root
    blocks = []

    def flush():
        # Node đã được tạo ngay khi gặp heading, kể cả khi text rỗng.
        current.page_content = "\n\n".join(blocks).strip()

    for node in article_blocks(article):
        if node.name not in HEADINGS:
            text = node.get_text(strip=True)
            if text:
                blocks.append(text)
            continue
        flush()
        blocks = []
        level = int(node.name[1])
        while stack[-1].metadata["level"] >= level:
            stack.pop()
        parent = stack[-1]
        parent_id = parent.metadata["section_id"]
        label = node.get_text(" ", strip=True)
        anchor = node.get("id", "")
        order = len(sections)
        key = f"anchor:{anchor}" if anchor else f"no-anchor:{order}"
        section_id = stable_id(source, key)
        if section_id in seen_ids:
            raise ValueError(f"Anchor trùng trong {source}: {anchor}")
        seen_ids.add(section_id)
        sibling_order = child_counts.get(parent_id, 0)
        child_counts[parent_id] = sibling_order + 1
        labels = [s.metadata["label"] for s in stack[1:]] + [label]
        current = Document(page_content="", metadata={
            "source": source, "title": title, "heading": " > ".join(labels),
            "label": label, "url": page_url + (f"#{anchor}" if anchor else ""),
            "anchor": anchor, "section_id": section_id, "parent_id": parent_id,
            "level": level, "section_order": order, "sibling_order": sibling_order,
            "is_page_root": False, "record_type": "section",
        })
        sections.append(current)
        stack.append(current)
    flush()
    return sections


def read_sections(repo_root, article_paths):
    documents = []
    with TemporaryDirectory(prefix="handbook-rag-") as output_dir:
        config = load_config(
            config_file=str(repo_root / "mkdocs.yml"), site_dir=output_dir,
        )
        files = get_files(config)
        pages = {path: files.get_file_from_path(path) for path in article_paths}
        if any(page is None for page in pages.values()):
            raise RuntimeError("Có bài không xuất hiện trong tập file MkDocs.")
        build(config)
        for source, page in pages.items():
            html = (Path(output_dir) / page.dest_uri).read_text(encoding="utf-8")
            documents.extend(extract_sections(html, source, page.url))
    if not documents:
        raise RuntimeError("Không trích xuất được section nào.")
    return documents


def chunk_sections(documents, embedding_model):
    tokenizer = AutoTokenizer.from_pretrained(embedding_model)
    splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
        tokenizer, chunk_size=320, chunk_overlap=48,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = []
    for section in documents:
        if not section.page_content.strip():
            continue
        parts = splitter.split_documents([section])
        for index, part in enumerate(parts):
            raw = part.page_content
            part.metadata.update(
                record_type="body", chunk_index=index, chunk_count=len(parts),
                chunk_id=stable_id(
                    section.metadata["section_id"], f"body:{index}:{raw}",
                ),
            )
            prefix = f"{part.metadata['title']}\n{part.metadata['heading']}\n\n"
            part.page_content = prefix + raw #Thêm prefix vào page_contnent để kiểm tra heading tót hơn
            length = len(tokenizer.encode("passage: " + part.page_content))
            if length > 512:
                raise RuntimeError(f"Chunk vượt 512 token ({length}): {part.metadata['url']}")
            chunks.append(part)
    return chunks