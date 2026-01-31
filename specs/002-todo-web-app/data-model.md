# Data Model: Todo Web Application - Phase II

**Feature**: 002-todo-web-app
**Date**: 2026-01-24

## Overview
Data model for the multi-user Todo Web Application with authentication and persistent storage.

## Database Schema

### Database: Neon Serverless PostgreSQL

#### Tasks Table
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_created_at ON tasks(created_at);
```

#### Indexing Strategy
- Primary index on `id` (UUID) for direct access
- Index on `user_id` for efficient user-based queries (critical for user isolation)
- Index on `completed` for filtering completed/incomplete tasks
- Index on `created_at` for chronological ordering

## SQLModel Implementation

### Task Model
```python
from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional
import uuid
from datetime import datetime

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None

class TaskPatchComplete(SQLModel):
    completed: bool
```

## API Request/Response Models

### Task Creation
**Request**: `POST /api/{user_id}/tasks`
```json
{
  "title": "string (required, min 1, max 255)",
  "description": "string (optional, max 1000)",
  "completed": "boolean (optional, default false)"
}
```

**Response**: `201 Created`
```json
{
  "id": "UUID",
  "user_id": "UUID",
  "title": "string",
  "description": "string or null",
  "completed": "boolean",
  "created_at": "ISO datetime",
  "updated_at": "ISO datetime"
}
```

### Task List
**Request**: `GET /api/{user_id}/tasks`
**Response**: `200 OK`
```json
[
  {
    "id": "UUID",
    "user_id": "UUID",
    "title": "string",
    "description": "string or null",
    "completed": "boolean",
    "created_at": "ISO datetime",
    "updated_at": "ISO datetime"
  }
]
```

### Task Update
**Request**: `PUT /api/{user_id}/tasks/{id}`
```json
{
  "title": "string (required, min 1, max 255)",
  "description": "string (optional, max 1000)",
  "completed": "boolean"
}
```

**Response**: `200 OK`
```json
{
  "id": "UUID",
  "user_id": "UUID",
  "title": "string",
  "description": "string or null",
  "completed": "boolean",
  "created_at": "ISO datetime",
  "updated_at": "ISO datetime"
}
```

## Relationships

### User-Task Relationship
- One-to-Many: One user can have many tasks
- Implemented via `user_id` foreign key in tasks table
- Enforced through application logic and database indexing

## Data Integrity

### Constraints
- `title` is required (NOT NULL) with length validation
- `completed` defaults to FALSE
- `created_at` and `updated_at` automatically managed
- `user_id` is indexed for performance

### Validation
- Server-side validation through SQLModel field constraints
- Additional validation in API layer for business rules
- JWT verification ensures user owns the user_id in the URL

## Migration Strategy

### Initial Migration
```python
# Alembic migration file
def upgrade():
    op.create_table('tasks',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.VARCHAR(length=255), nullable=False),
        sa.Column('description', sa.TEXT(), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('idx_tasks_user_id', 'user_id')
    )

def downgrade():
    op.drop_table('tasks')
```

## Performance Considerations

### Query Optimization
- Queries filtered by `user_id` will use index for performance
- Pagination recommended for large task lists
- Consider read replicas for heavy read operations

### Connection Management
- Use connection pooling for Neon PostgreSQL
- Implement proper session management with SQLModel
- Handle serverless cold start scenarios