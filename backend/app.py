import logging
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field, field_validator

from answering import answer_question, build_answerer
from rag import build_retriever
from fastapi.middleware.cors import CORSMiddleware
logger = logging.getLogger(__name__)


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)

    @field_validator("question")
    @classmethod
    def reject_blank(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Câu hỏi không được để trống.")
        return value


class Source(BaseModel):
    id: str
    title: str
    heading: str
    url: str
    chunk_id: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]
    status: Literal["answered", "insufficient_evidence", "generation_error"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.retriever = build_retriever()
    app.state.answerer = build_answerer()
    yield


app = FastAPI(title="Behind the Pipeline RAG", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000"],
    allow_credentials=False,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

@app.get("/health")
def health():
    return {"status": "ready"}


@app.post("/chat", response_model=ChatResponse)
def chat(body: ChatRequest, request: Request):
    try:
        result = answer_question(
            body.question, request.app.state.retriever, request.app.state.answerer
        )
        return ChatResponse(**result)
    except Exception as exc:
        logger.exception("RAG request failed")
        raise HTTPException(503, "Không tạo được câu trả lời; xem log backend.") from exc
