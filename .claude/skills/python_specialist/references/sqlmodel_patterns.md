# SQLModel Patterns and Database Best Practices

## Model Definitions

### Basic Model
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    completed: bool = False
    due_date: Optional[datetime] = None

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Foreign key relationships
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")

class TaskRead(TaskBase):
    id: int
    created_at: datetime

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None
```

## Relationships

### One-to-Many
```python
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    tasks: List["Task"] = Relationship(back_populates="user")

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="tasks")
```

### Many-to-Many
```python
# Link table for many-to-many relationship
class TeamUserLink(SQLModel, table=True):
    team_id: Optional[int] = Field(default=None, foreign_key="team.id", primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    users: List["User"] = Relationship(
        back_populates="teams",
        link_model=TeamUserLink
    )

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    teams: List["Team"] = Relationship(
        back_populates="users",
        link_model=TeamUserLink
    )
```

## Async Session Management

### Database Setup
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlmodel.ext.asyncio.session import AsyncSession as SQLModelSession
from sqlalchemy.pool import NullPool
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:pass@localhost/db")

engine = create_async_engine(
    DATABASE_URL,
    poolclass=NullPool,  # Use NullPool for async applications
    echo=False  # Set to True for SQL debugging
)

async def get_session() -> AsyncSession:
    async with SQLModelSession(engine) as session:
        yield session
```

## Query Patterns

### Select Queries
```python
from sqlmodel import select, func
from sqlalchemy.exc import NoResultFound

# Simple select
statement = select(Task).where(Task.id == task_id)
result = await session.execute(statement)
task = result.scalar_one_or_none()

# With joins
statement = select(Task, User).join(User).where(Task.user_id == User.id)
result = await session.execute(statement)
task_user = result.first()

# Aggregation
count_statement = select(func.count(Task.id)).where(Task.completed == True)
count_result = await session.execute(count_statement)
completed_count = count_result.scalar()
```

### Insert/Update/Delete
```python
# Insert
new_task = Task(title="New task", description="Description")
session.add(new_task)
await session.commit()
await session.refresh(new_task)

# Update
task.title = "Updated title"
await session.commit()

# Delete
await session.delete(task)
await session.commit()
```

## Connection Pooling and Configuration

### Production Settings
```python
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import QueuePool

engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,  # Number of connections to maintain
    max_overflow=30,  # Additional connections beyond pool_size
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=3600,  # Recycle connections after 1 hour
    echo=False  # Set to True for debugging
)
```

## Migration Patterns

### Alembic Integration
```python
# In alembic/env.py
from sqlmodel import SQLModel
from alembic import context

target_metadata = SQLModel.metadata

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()
```

## Error Handling

### Common Exception Handling
```python
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound

try:
    session.add(new_task)
    await session.commit()
except IntegrityError as e:
    await session.rollback()
    # Handle duplicate entry or constraint violations
    raise HTTPException(status_code=400, detail="Data integrity error")
except NoResultFound:
    # Handle case where no record is found
    raise HTTPException(status_code=404, detail="Record not found")
```