import os
from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from content import chunk_sections, read_sections

REPO_ROOT = Path(__file__).resolve().parents[1]
EMBEDDING_MODEL = "intfloat/multilingual-e5-small"
INDEX_SPEC = {
    "embedding_model": EMBEDDING_MODEL,
    "embedding_prefixes": "passage/query",
    "normalize_embeddings": True,
    "chunking": "raw-markdown-char-1000-overlap-200-v1",
}
ARTICLE_PATHS = (
    "airflow/architecture.md",
    "architecture/shared-disk-vs-shared-nothing.md",
    "postgres/postgres.md",
    "index/index.md",
)

def load_documents():
    return read_sections(REPO_ROOT, ARTICLE_PATHS)

def split_documents(documents):
    return chunk_sections(documents, EMBEDDING_MODEL)

def make_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={
            "normalize_embeddings": True,
            "prompt": "passage: ",
        },
        query_encode_kwargs={
            "normalize_embeddings": True,
            "prompt": "query: ",
        },
    )


def build_retriever(mode=None):
    from context_budget import get_budget
    from overview_retrieval import OverviewRetriever
    from retrieval import make_retriever
    from storage import open_snapshot

    mode = mode or os.getenv("RETRIEVAL_MODE", "hierarchical")
    store, catalog, manifest = open_snapshot(make_embeddings(), INDEX_SPEC)
    if mode != "hierarchical":
        return make_retriever(store, mode=mode, k=8)
    retriever = OverviewRetriever(
        catalog=catalog,
        detail_factory=lambda: make_retriever(
            store, mode="hybrid_decompose_rerank", k=8,
        ),
        budget=get_budget(),
    )
    retriever.manifest = manifest
    return retriever


def make_llm(num_predict=256):
    return ChatOllama(
        model="qwen3:4b-instruct",
        base_url=os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434"),
        temperature=0,
        num_ctx=8192,
        num_predict=num_predict,
        client_kwargs={"timeout": 180.0},
    )
