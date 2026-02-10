"""Conversation service for Phase III AI Chatbot Integration.

Provides CRUD operations for conversations and messages.
"""
from sqlmodel import Session, select, func
from uuid import UUID
from typing import List, Optional
from datetime import datetime

from ..models.conversation import Conversation
from ..models.message import Message, MessageRole


class ConversationService:
    """Service for managing conversations and messages."""

    def __init__(self, session: Session):
        self.session = session

    def create_conversation(self, user_id: UUID, title: Optional[str] = None) -> Conversation:
        """Create a new conversation for a user.

        Args:
            user_id: UUID of the user
            title: Optional conversation title

        Returns:
            Created Conversation object
        """
        conversation = Conversation(user_id=user_id, title=title)
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return conversation

    def get_conversation(self, conversation_id: UUID, user_id: UUID) -> Optional[Conversation]:
        """Get conversation with user validation.

        Args:
            conversation_id: UUID of the conversation
            user_id: UUID of the user (for validation)

        Returns:
            Conversation object if found and belongs to user, None otherwise
        """
        return self.session.exec(
            select(Conversation)
            .where(Conversation.id == conversation_id)
            .where(Conversation.user_id == user_id)
            .where(Conversation.deleted == False)
        ).first()

    def add_message(
        self,
        conversation_id: UUID,
        role: MessageRole,
        content: str,
        tool_calls: Optional[dict] = None,
        tool_call_id: Optional[str] = None
    ) -> Message:
        """Add a message to conversation.

        Args:
            conversation_id: UUID of the conversation
            role: Message role (USER, ASSISTANT, or TOOL)
            content: Message content
            tool_calls: Optional tool calls for assistant messages
            tool_call_id: Optional tool call ID for tool result messages

        Returns:
            Created Message object
        """
        # Get next sequence number
        max_seq = self.session.exec(
            select(func.max(Message.sequence_number))
            .where(Message.conversation_id == conversation_id)
        ).first() or 0

        message = Message(
            conversation_id=conversation_id,
            sequence_number=max_seq + 1,
            role=role,
            content=content,
            tool_calls=tool_calls,
            tool_call_id=tool_call_id
        )
        self.session.add(message)

        # Update conversation timestamp
        conversation = self.session.get(Conversation, conversation_id)
        if conversation:
            conversation.updated_at = datetime.utcnow()

        self.session.commit()
        self.session.refresh(message)
        return message

    def get_messages(
        self,
        conversation_id: UUID,
        limit: int = 50,
        offset: int = 0
    ) -> List[Message]:
        """Get conversation messages.

        Args:
            conversation_id: UUID of the conversation
            limit: Maximum number of messages to return
            offset: Number of messages to skip

        Returns:
            List of Message objects in chronological order
        """
        return self.session.exec(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .where(Message.deleted == False)
            .order_by(Message.sequence_number)
            .offset(offset)
            .limit(limit)
        ).all()

    def list_user_conversations(
        self,
        user_id: UUID,
        limit: int = 20,
        offset: int = 0
    ) -> List[Conversation]:
        """List user's conversations, most recent first.

        Args:
            user_id: UUID of the user
            limit: Maximum number of conversations to return
            offset: Number of conversations to skip

        Returns:
            List of Conversation objects ordered by updated_at descending
        """
        return self.session.exec(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .where(Conversation.deleted == False)
            .order_by(Conversation.updated_at.desc())
            .offset(offset)
            .limit(limit)
        ).all()
