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