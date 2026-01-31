# Data Model: Todo SaaS - Phase 2

**Feature**: Todo SaaS - Phase 2 UI/UX + Auth
**Date**: 2026-01-29
**Status**: Complete

## Overview

This document defines the data model for the Todo SaaS application Phase 2. The model supports multi-user task management with proper authentication and data isolation.

## Entities

### 1. User

**Purpose**: Represents an authenticated user account in the system.

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Auto-generated | Unique identifier for the user |
| email | String(255) | Unique, Not Null, Indexed | User's email address (used for login) |
| hashed_password | String(255) | Not Null | Bcrypt-hashed password |
| created_at | DateTime | Not Null, Auto-generated | Timestamp when user was created |
| updated_at | DateTime | Not Null, Auto-updated | Timestamp when user was last updated |

**Relationships**:
- One-to-Many with Task (one user has many tasks)

**Indexes**:
- Primary: id
- Unique: email

**Validation Rules**:
- Email must be valid email format
- Password must be at least 6 characters (enforced at API level)
- Email is case-insensitive for uniqueness

**SQLModel Definition** (backend/src/models/user.py):
```python
from sqlmodel import SQLModel, Field
from typing import Optional
import uuid
from datetime import datetime

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True, max_length=255)

class User(UserBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
```

**State Transitions**: None (users don't have state transitions)

---

### 2. Task

**Purpose**: Represents a todo item owned by a user.

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Auto-generated | Unique identifier for the task |
| user_id | UUID | Foreign Key (User.id), Not Null, Indexed | Owner of the task |
| title | String(255) | Not Null, Min Length 1 | Task title (required) |
| description | Text | Nullable | Optional task description |
| completed | Boolean | Not Null, Default False | Completion status |
| created_at | DateTime | Not Null, Auto-generated | Timestamp when task was created |
| updated_at | DateTime | Not Null, Auto-updated | Timestamp when task was last updated |

**Relationships**:
- Many-to-One with User (many tasks belong to one user)

**Indexes**:
- Primary: id
- Foreign Key: user_id (indexed for performance)

**Validation Rules**:
- Title must not be empty (min length 1)
- Title max length 255 characters
- Description max length 1000 characters
- Completed defaults to false
- user_id must reference existing User

**SQLModel Definition** (backend/src/models/task.py):
```python
from sqlmodel import SQLModel, Field
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
```

**State Transitions**:
- Created → Active (completed = false)
- Active → Completed (completed = true)
- Completed → Active (completed = false) [toggle back]

---

## Entity Relationships

```
User (1) ----< (Many) Task
  |                      |
  id                     user_id (FK)
```

**Relationship Rules**:
1. Each Task MUST belong to exactly one User
2. Each User MAY have zero or many Tasks
3. Deleting a User should cascade delete their Tasks (not implemented in Phase 2)
4. Tasks are isolated by user_id - users can only access their own tasks

---

## Database Schema

### Table: users

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
```

### Table: tasks

```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
```

---

## Data Access Patterns

### Pattern 1: User Registration
```python
# Create new user
new_user = User(
    email=user_data.email,
    hashed_password=get_password_hash(user_data.password),
    created_at=datetime.utcnow(),
    updated_at=datetime.utcnow()
)
session.add(new_user)
session.commit()
session.refresh(new_user)
```

### Pattern 2: User Authentication
```python
# Find user by email
statement = select(User).where(User.email == email)
user = session.exec(statement).first()

# Verify password
if user and verify_password(password, user.hashed_password):
    # Generate JWT token
    token = create_access_token(data={"sub": str(user.id), "email": user.email})
```

### Pattern 3: Get User's Tasks
```python
# Query tasks for specific user
statement = select(Task).where(Task.user_id == user_id)
tasks = session.exec(statement).all()
```

### Pattern 4: Create Task
```python
# Create new task for user
new_task = Task(
    user_id=user_id,
    title=task_data.title,
    description=task_data.description,
    completed=False,
    created_at=datetime.utcnow(),
    updated_at=datetime.utcnow()
)
session.add(new_task)
session.commit()
session.refresh(new_task)
```

### Pattern 5: Update Task
```python
# Get task and verify ownership
statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
task = session.exec(statement).first()

if task:
    task.title = updated_data.title
    task.description = updated_data.description
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
```

### Pattern 6: Delete Task
```python
# Get task and verify ownership
statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
task = session.exec(statement).first()

if task:
    session.delete(task)
    session.commit()
```

### Pattern 7: Toggle Task Completion
```python
# Get task and verify ownership
statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
task = session.exec(statement).first()

if task:
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
```

---

## Database Initialization

**Script**: backend/init_db.py

```python
from sqlmodel import SQLModel, create_engine
from src.models.user import User
from src.models.task import Task
from src.config.settings import get_settings

def init_database():
    """Initialize database tables"""
    settings = get_settings()
    engine = create_engine(settings.database_url, echo=True)

    # Create all tables
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_database()
```

**Usage**:
```bash
cd backend
python init_db.py
```

---

## Migration Strategy

**Phase 2 Approach**: Direct table creation using SQLModel.metadata.create_all()

**Future Phases**: Consider Alembic migrations for schema changes

**Rationale**: Phase 2 scope doesn't require migration history. Tables are created once during initial setup.

---

## Data Integrity Rules

1. **User Isolation**: All task queries MUST filter by user_id
2. **Ownership Verification**: All task mutations MUST verify user_id matches authenticated user
3. **Referential Integrity**: Task.user_id MUST reference valid User.id
4. **Unique Constraints**: User.email MUST be unique (case-insensitive)
5. **Required Fields**: title, email, hashed_password are NOT NULL

---

## Performance Considerations

1. **Indexing**: user_id indexed on tasks table for fast user-based queries
2. **Connection Pooling**: Use SQLAlchemy connection pool (configured in session.py)
3. **Query Optimization**: Always filter by user_id first to reduce result set
4. **Pagination**: Consider pagination for task lists if user has many tasks (future enhancement)

---

## Security Considerations

1. **Password Storage**: Always hash passwords using bcrypt (never store plain text)
2. **User Isolation**: Backend MUST independently verify user_id from JWT
3. **SQL Injection**: Use SQLModel parameterized queries (automatic protection)
4. **Data Access**: Never expose user_id in frontend URLs (use JWT claims)

---

**Data Model Status**: Complete
**Next Step**: Generate API contracts
