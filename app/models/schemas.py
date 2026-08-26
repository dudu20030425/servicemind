from typing import Literal

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)


class ChatResponse(BaseModel):
    answer: str
    provider: str
    model: str


class IntentResponse(BaseModel):
    intent: Literal[
        "order_query",
        "refund_query",
        "product_query",
        "general_chat",
    ]
    order_id: str | None = None
    need_tool: bool

class RetrieveRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int = Field(default=3, ge=1, le=10)


class RetrievalResult(BaseModel):
    id: str
    chunk_id: str
    text: str
    category: str
    source: str
    score: float


class RetrieveResponse(BaseModel):
    query: str
    results: list[RetrievalResult]


class RagRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int = Field(default=3, ge=1, le=10)


class RagSource(BaseModel):
    id: str
    text: str
    source: str
    score: float


class RagResponse(BaseModel):
    query: str
    answer: str
    provider: str | None
    model: str | None
    sources: list[RagSource]