from typing import Literal

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):

    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, description="用户问题")
    history: list[ChatMessage] = Field(default_factory=list)
