"""Conversation model for Phase III AI Chatbot Integration.

Represents a chat conversation between a user and the AI assistant.
Each conversation belongs to exactly one user and contains an ordered
sequence of messages.
"""
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .message import Message


class Conversation(SQLModel, table=True):
    """
    Represents a chat conversation between a user and the AI assistant.

    Each conversation belongs to exactly one user and contains an ordered
    sequence of messages. Conversations persist across sessions and server
    restarts to enable conversation history and context.
    """
    __tablename__ = "conversations"

    # Primary Key
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    # Foreign Keys
    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)

    # Attributes
    title: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    deleted: bool = Field(default=False, nullable=False)

    # Relationships
    user: Optional["User"] = Relationship(back_populates="conversations")
    messages: List["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Task management conversation",
                "created_at": "2026-02-09T10:30:00Z",
                "updated_at": "2026-02-09T10:35:00Z",
                "deleted": False
            }
        }
