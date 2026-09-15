import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

from rag import build_chain, build_retriever

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


class ChatResponse(BaseModel):
    answer: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.retriever = build_retriever()
    app.state.chain = build_chain(app.state.retriever)
    yield


app = FastAPI(title="Behind the Pipeline RAG", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in os.getenv(
            "CORS_ALLOW_ORIGINS",
            "http://127.0.0.1:8000,http://localhost:8000",
        ).split(",")
        if origin.strip()
    ],
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
        answer = request.app.state.chain.invoke(body.question)
        return ChatResponse(answer=answer)
    except Exception as exc:
        logger.exception("RAG request failed")
        raise HTTPException(503, "Không tạo được câu trả lời; xem log backend.") from exc
