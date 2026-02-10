"""Message model for Phase III AI Chatbot Integration.

Represents a single message in a conversation between user and AI assistant.
Messages are ordered by sequence_number within a conversation.
"""
from sqlmodel import SQLModel, Field, Relationship, Column, JSON
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, Dict, Any, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from .conversation import Conversation


class MessageRole(str, Enum):
    """Message role types in conversation"""
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class Message(SQLModel, table=True):
    """
    Represents a single message in a conversation.

    Messages are ordered by sequence_number within a conversation. Three types:
    - USER: Messages from the user
    - ASSISTANT: Responses from the AI assistant
    - TOOL: Tool execution results (internal, not displayed to user)

    Tool calls are stored in the tool_calls field for assistant messages that
    invoke tools. Tool results are stored as separate TOOL messages with
    tool_call_id linking back to the assistant message.
    """
    __tablename__ = "messages"

    # Primary Key
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    # Foreign Keys
    conversation_id: UUID = Field(
        foreign_key="conversations.id",
        nullable=False,
        index=True
    )

    # Attributes
    sequence_number: int = Field(nullable=False, index=True)
    role: MessageRole = Field(nullable=False)
    content: str = Field(nullable=False)
    tool_calls: Optional[Dict[str, Any]] = Field(
        default=None,
        sa_column=Column(JSON)
    )
    tool_call_id: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    deleted: bool = Field(default=False, nullable=False)

    # Relationships
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "660e8400-e29b-41d4-a716-446655440001",
                "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
                "sequence_number": 1,
                "role": "user",
                "content": "Add a task to buy groceries",
                "tool_calls": None,
                "tool_call_id": None,
                "created_at": "2026-02-09T10:30:00Z",
                "deleted": False
            }
        }
