# Data Model: Conversation Persistence

**Feature**: AI Chatbot Integration for Todo Management
**Date**: 2026-02-09
**Status**: Design
**Related Documents**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md)

## Overview

This document defines the database schema for conversation persistence in Phase III. The design supports stateless chat endpoints by storing all conversation history in PostgreSQL, enabling conversation resumption across sessions and server restarts.

## Design Principles

1. **Stateless Architecture**: All conversation state stored in database, no server-side session state
2. **User Isolation**: Every conversation and message belongs to exactly one user
3. **Efficient Retrieval**: Optimized indexes for fast conversation history loading
4. **Chronological Ordering**: Messages ordered by sequence number for consistent display
5. **Soft Deletion**: Support for conversation archival without data loss
6. **Audit Trail**: Track creation and update timestamps for all entities

## Entity Relationship Diagram

```
User (existing)
  ├── id: UUID (PK)
  ├── email: str
  └── ...

Task (existing)
  ├── id: UUID (PK)
  ├── user_id: UUID (FK → User.id)
  ├── title: str
  ├── description: str
  ├── completed: bool
  └── ...

Conversation (new)
  ├── id: UUID (PK)
  ├── user_id: UUID (FK → User.id)
  ├── title: str (optional, auto-generated from first message)
  ├── created_at: datetime
  ├── updated_at: datetime
  └── deleted: bool (soft delete)

Message (new)
  ├── id: UUID (PK)
  ├── conversation_id: UUID (FK → Conversation.id)
  ├── sequence_number: int (ordering within conversation)
  ├── role: str (enum: "user", "assistant", "tool")
  ├── content: str (message text or tool result JSON)
  ├── tool_calls: JSON (optional, for assistant messages with tool calls)
  ├── tool_call_id: str (optional, for tool result messages)
  ├── created_at: datetime
  └── deleted: bool (soft delete)
```

## Relationships

- **User → Conversation**: One-to-Many (one user can have multiple conversations)
- **Conversation → Message**: One-to-Many (one conversation contains multiple messages)
- **User → Task**: One-to-Many (existing relationship, unchanged)

## SQLModel Definitions

### Conversation Model

```python
# backend/src/models/conversation.py
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, List

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
```

### Message Model

```python
# backend/src/models/message.py
from sqlmodel import SQLModel, Field, Relationship, Column, JSON
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum

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
```

### Updated User Model

```python
# backend/src/models/user.py (additions only)
from typing import List

class User(SQLModel, table=True):
    # ... existing fields ...

    # New Relationship (add to existing User model)
    conversations: List["Conversation"] = Relationship(back_populates="user")
```

## Database Indexes

### Critical Indexes for Performance

```sql
-- Composite index for efficient message retrieval
CREATE INDEX idx_messages_conversation_sequence
ON messages (conversation_id, sequence_number)
WHERE deleted = false;

-- Index for user's conversations
CREATE INDEX idx_conversations_user_updated
ON conversations (user_id, updated_at DESC)
WHERE deleted = false;

-- Index for conversation lookup
CREATE INDEX idx_conversations_id_user
ON conversations (id, user_id)
WHERE deleted = false;
```

### Index Rationale

1. **idx_messages_conversation_sequence**: Enables fast retrieval of messages in chronological order for a conversation. Partial index excludes soft-deleted messages.

2. **idx_conversations_user_updated**: Supports listing user's conversations sorted by most recent activity. Partial index for active conversations only.

3. **idx_conversations_id_user**: Optimizes conversation lookup with user validation in a single index scan.

## Alembic Migration

```python
# backend/alembic/versions/003_add_conversation_models.py
"""Add conversation and message models for Phase III

Revision ID: 003
Revises: 002
Create Date: 2026-02-09
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

# revision identifiers
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('deleted', sa.Boolean(), nullable=False, server_default='false'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('conversation_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('sequence_number', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tool_calls', postgresql.JSON(), nullable=True),
        sa.Column('tool_call_id', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('deleted', sa.Boolean(), nullable=False, server_default='false'),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
    )

    # Create indexes
    op.create_index(
        'idx_conversations_user_id',
        'conversations',
        ['user_id']
    )

    op.create_index(
        'idx_conversations_user_updated',
        'conversations',
        ['user_id', sa.text('updated_at DESC')],
        postgresql_where=sa.text('deleted = false')
    )

    op.create_index(
        'idx_conversations_id_user',
        'conversations',
        ['id', 'user_id'],
        postgresql_where=sa.text('deleted = false')
    )

    op.create_index(
        'idx_messages_conversation_id',
        'messages',
        ['conversation_id']
    )

    op.create_index(
        'idx_messages_conversation_sequence',
        'messages',
        ['conversation_id', 'sequence_number'],
        postgresql_where=sa.text('deleted = false')
    )

def downgrade() -> None:
    # Drop indexes
    op.drop_index('idx_messages_conversation_sequence', table_name='messages')
    op.drop_index('idx_messages_conversation_id', table_name='messages')
    op.drop_index('idx_conversations_id_user', table_name='conversations')
    op.drop_index('idx_conversations_user_updated', table_name='conversations')
    op.drop_index('idx_conversations_user_id', table_name='conversations')

    # Drop tables
    op.drop_table('messages')
    op.drop_table('conversations')
```

## Query Patterns

### Create Conversation

```python
def create_conversation(session: Session, user_id: UUID, title: Optional[str] = None) -> Conversation:
    """Create a new conversation for a user"""
    conversation = Conversation(
        user_id=user_id,
        title=title
    )
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation
```

### Add Message

```python
def add_message(
    session: Session,
    conversation_id: UUID,
    role: MessageRole,
    content: str,
    tool_calls: Optional[Dict] = None,
    tool_call_id: Optional[str] = None
) -> Message:
    """Add a message to a conversation"""
    # Get next sequence number
    max_seq = session.exec(
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
    session.add(message)

    # Update conversation timestamp
    conversation = session.get(Conversation, conversation_id)
    conversation.updated_at = datetime.utcnow()

    session.commit()
    session.refresh(message)
    return message
```

### Get Conversation History

```python
def get_conversation_history(
    session: Session,
    conversation_id: UUID,
    user_id: UUID,
    limit: int = 50,
    offset: int = 0
) -> List[Message]:
    """
    Get conversation history with pagination.

    Returns messages in chronological order (oldest first).
    Enforces user isolation by validating conversation ownership.
    """
    # Validate conversation belongs to user
    conversation = session.exec(
        select(Conversation)
        .where(Conversation.id == conversation_id)
        .where(Conversation.user_id == user_id)
        .where(Conversation.deleted == False)
    ).first()

    if not conversation:
        raise ValueError("Conversation not found or access denied")

    # Get messages
    messages = session.exec(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .where(Message.deleted == False)
        .order_by(Message.sequence_number)
        .offset(offset)
        .limit(limit)
    ).all()

    return messages
```

### List User Conversations

```python
def list_user_conversations(
    session: Session,
    user_id: UUID,
    limit: int = 20,
    offset: int = 0
) -> List[Conversation]:
    """List user's conversations, most recent first"""
    conversations = session.exec(
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .where(Conversation.deleted == False)
        .order_by(Conversation.updated_at.desc())
        .offset(offset)
        .limit(limit)
    ).all()

    return conversations
```

## Data Constraints

### Conversation Constraints

- `id`: UUID, primary key, auto-generated
- `user_id`: UUID, foreign key to users.id, NOT NULL, indexed
- `title`: String(255), nullable, auto-generated from first message if not provided
- `created_at`: DateTime, NOT NULL, default=now()
- `updated_at`: DateTime, NOT NULL, default=now(), updated on message add
- `deleted`: Boolean, NOT NULL, default=false

### Message Constraints

- `id`: UUID, primary key, auto-generated
- `conversation_id`: UUID, foreign key to conversations.id, NOT NULL, indexed
- `sequence_number`: Integer, NOT NULL, indexed, unique per conversation
- `role`: Enum("user", "assistant", "tool"), NOT NULL
- `content`: Text, NOT NULL
- `tool_calls`: JSON, nullable (only for assistant messages with tool calls)
- `tool_call_id`: String(255), nullable (only for tool result messages)
- `created_at`: DateTime, NOT NULL, default=now()
- `deleted`: Boolean, NOT NULL, default=false

### Business Rules

1. **Sequence Number Uniqueness**: Within a conversation, sequence_number must be unique and sequential
2. **Tool Call Linking**: Tool messages must have tool_call_id matching an assistant message's tool call
3. **User Isolation**: All queries must filter by user_id to prevent cross-user access
4. **Soft Deletion**: Use deleted flag instead of hard deletes to preserve audit trail
5. **Conversation Title**: Auto-generate from first user message if not provided (max 50 chars from message)

## Performance Considerations

### Expected Load

- Average conversation: 20-50 messages
- Active users: 100 concurrent
- Message creation rate: ~200/minute peak
- Conversation history queries: ~500/minute peak

### Optimization Strategies

1. **Composite Indexes**: Use (conversation_id, sequence_number) for fast message retrieval
2. **Partial Indexes**: Index only non-deleted records to reduce index size
3. **Pagination**: Limit message retrieval to recent 50 messages by default
4. **Connection Pooling**: Use SQLModel's connection pool for concurrent requests
5. **Query Optimization**: Use select() with specific columns instead of loading full objects when possible

### Performance Targets

- Conversation creation: <50ms
- Message insertion: <100ms
- History retrieval (50 messages): <200ms
- Conversation list (20 items): <150ms

## Testing Strategy

### Unit Tests

- Model validation (field types, constraints)
- Relationship integrity (cascade deletes)
- Sequence number generation
- Soft deletion behavior

### Integration Tests

- Conversation CRUD operations
- Message ordering and retrieval
- User isolation enforcement
- Pagination correctness
- Index usage verification (EXPLAIN ANALYZE)

### Performance Tests

- Load test: 100 concurrent users creating conversations
- Stress test: 1000 messages in single conversation
- Query performance: Verify <200ms for 50 message retrieval

## Migration Checklist

- [ ] Create Alembic migration file
- [ ] Add Conversation and Message models to backend/src/models/
- [ ] Update User model with conversations relationship
- [ ] Create database indexes
- [ ] Run migration in development environment
- [ ] Verify foreign key constraints
- [ ] Test cascade deletes
- [ ] Verify index usage with EXPLAIN ANALYZE
- [ ] Run integration tests
- [ ] Document rollback procedure

## Rollback Plan

If migration fails or issues are discovered:

1. Run `alembic downgrade -1` to revert migration
2. Verify tables and indexes are dropped
3. Check for orphaned data
4. Fix migration script
5. Re-run upgrade

## Related Documents

- [spec.md](spec.md) - Feature requirements (FR-023 to FR-027)
- [plan.md](plan.md) - Architecture decisions (AD-004: Database-only state)
- [research.md](research.md) - Conversation persistence patterns
- [API Contracts](contracts/) - Chat endpoint specifications
