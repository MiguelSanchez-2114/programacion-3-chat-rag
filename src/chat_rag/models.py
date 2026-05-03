from dataclasses import dataclass
from datetime import datetime


@dataclass
class ChatMessage:
    sender: str
    text: str
    created_at: datetime


@dataclass
class Conversation:
    id: int
    username: str
    file_name: str | None
    created_at: datetime
    messages: list[ChatMessage]
