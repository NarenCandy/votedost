"""Dataclasses for request and response models."""
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class ChatMessage:
    """Represents a single message in a chat history."""
    role: str
    content: str

@dataclass
class ChatRequest:
    """Represents the incoming chat request structure."""
    message: str
    language: str
    history: List[ChatMessage]
    session_id: Optional[str] = None
