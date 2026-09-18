from pathlib import Path
from tempfile import TemporaryDirectory

from bs4 import BeautifulSoup
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from mkdocs.commands.build import build
from mkdocs.config import load_config
from mkdocs.structure.files import get_files
from transformers import AutoTokenizer


def read_sections(repo_root, article_paths):
    documents = []
    with TemporaryDirectory(prefix="handbook-rag-") as output_dir:
        config = load_config(
            config_file=str(repo_root / "mkdocs.yml"),
            site_dir=output_dir,
        )
        # File.url và dest_uri theo đúng use_directory_urls của MkDocs.
        files = get_files(config)
        pages = {path: files.get_file_from_path(path) for path in article_paths}
        if any(page is None for page in pages.values()):
            raise RuntimeError("Có bài không xuất hiện trong tập file MkDocs.")
        build(config)

        for source, page in pages.items():
            html = (Path(output_dir) / page.dest_uri).read_text(encoding="utf-8")
            soup = BeautifulSoup(html, "html.parser")
            article = soup.select_one("article.md-content__inner")
            if article is None:
                raise RuntimeError(f"Không tìm thấy vùng bài viết: {source}")
            title_node = article.find("h1")
            title = title_node.get_text(" ", strip=True) if title_node else source

            # Các selector này theo cấu trúc hiện tại của Behind the Pipeline.
            for node in article.select(
                "header, footer, script, style, .headerlink, "
                ".airflow-opening-comic, .airflow-closing-comic"
            ):
                node.decompose() #Giúp dọn sạch các các thẻ rác
            
            #Đóng gói các đoạn văn bản trong cùng 1 mục thành 1 Document    
            headings = []
            anchor = ""
            blocks = []

            def flush():
                text = "\n\n".join(blocks).strip()
                if text:
                    documents.append(Document(
                        page_content=text,
                        metadata={
                            "source": source,
                            "title": title,
                            "heading": " > ".join(label for _, label in headings),
                            # URL tương đối với site root; frontend ghép base URL.
                            "url": page.url + (f"#{anchor}" if anchor else ""),
                        },
                    ))

            for node in article.children:
                name = getattr(node, "name", None)
                if name is None:
                    continue
                if name in {"h1", "h2", "h3", "h4", "h5", "h6"}:
                    flush()
                    blocks = []
                    level = int(name[1])
                    while headings and headings[-1][0] >= level:
                        headings.pop()
                    headings.append((level, node.get_text(" ", strip=True)))
                    anchor = node.get("id", "")
                    continue
                if name in {"hr"}:
                    continue
                if any(c in node.get("class", []) for c in ["mermaid", "highlight"]):
                    continue
                if name == "table" or node.find("table") is not None:
                    table = node if name == "table" else node.find("table")
                    text = "\n".join(
                        " | ".join(cell.get_text(" ", strip=True)
                                   for cell in row.find_all(["th", "td"]))
                        for row in table.find_all("tr")
                    )
                elif name == "pre" or node.find("pre") is not None:
                    pre = node if name == "pre" else node.find("pre")
                    text = "```\n" + pre.get_text().strip() + "\n```"
                else:
                    text = node.get_text(" ", strip=True)
                if text:
                    blocks.append(text)  
            flush()

    if not documents:
        raise RuntimeError("Không trích xuất được section nào.")
    return documents


def chunk_sections(documents, embedding_model):
    tokenizer = AutoTokenizer.from_pretrained(embedding_model)
    splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
        tokenizer,
        chunk_size=320,
        chunk_overlap=48,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(documents)
    for chunk in chunks:
        prefix = f"{chunk.metadata['title']}\n{chunk.metadata['heading']}\n\n"
        chunk.page_content = prefix + chunk.page_content
        length = len(tokenizer.encode("passage: " + chunk.page_content))
        if length > 512:
            raise RuntimeError(
                f"Chunk vượt 512 token ({length}): {chunk.metadata['url']}. "
                "Giảm chunk_size hoặc rút ngắn tiêu đề."
            )
    return chunks