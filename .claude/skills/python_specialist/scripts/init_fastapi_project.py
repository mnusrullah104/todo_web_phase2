#!/usr/bin/env python3
"""
Script to initialize a new FastAPI project with SQLModel and Neon PostgreSQL
"""

import os
import sys
from pathlib import Path

def create_project_structure(project_name: str):
    """Create the basic project structure"""
    base_path = Path(project_name)
    base_path.mkdir(exist_ok=True)

    # Create directories
    (base_path / "app").mkdir(exist_ok=True)
    (base_path / "app" / "models").mkdir(exist_ok=True)
    (base_path / "app" / "schemas").mkdir(exist_ok=True)
    (base_path / "app" / "routes").mkdir(exist_ok=True)
    (base_path / "app" / "database").mkdir(exist_ok=True)
    (base_path / "tests").mkdir(exist_ok=True)

    return base_path

def create_main_app(base_path: Path):
    """Create the main FastAPI application file"""
    main_content = '''from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database.session import engine
from app.routes import tasks

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    # Create tables if they don't exist
    from app.models.task import Task  # Import here to register table
    from sqlmodel import SQLModel

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield

    # Shutdown
    await engine.dispose()

app = FastAPI(
    title="Todo API",
    description="A simple todo API built with FastAPI and SQLModel",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(tasks.router, prefix="/api/v1", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}
'''

    with open(base_path / "app" / "main.py", "w") as f:
        f.write(main_content)

def create_database_session(base_path: Path):
    """Create database session configuration"""
    session_content = '''from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.pool import NullPool
from sqlmodel.ext.asyncio.session import AsyncSession as SQLModelSession
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:pass@localhost/db")

engine = create_async_engine(
    DATABASE_URL,
    poolclass=NullPool,
    echo=False  # Set to True for SQL debugging
)

async def get_session() -> AsyncSession:
    async with SQLModelSession(engine) as session:
        yield session
'''

    (base_path / "app" / "database").mkdir(exist_ok=True)
    with open(base_path / "app" / "database" / "session.py", "w") as f:
        f.write(session_content)

def create_task_model(base_path: Path):
    """Create the task model"""
    model_content = '''from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    priority: str = Field(default="medium", regex="^(low|medium|high)$")
    completed: bool = Field(default=False)
    due_date: Optional[datetime] = Field(default=None)

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship example (if you have users)
    # user_id: Optional[int] = Field(default=None, foreign_key="user.id")

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int
    created_at: datetime

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None
'''

    with open(base_path / "app" / "models" / "task.py", "w") as f:
        f.write(model_content)

def create_task_routes(base_path: Path):
    """Create task routes"""
    routes_content = '''from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from app.database.session import get_session
from app.models.task import Task, TaskCreate, TaskRead, TaskUpdate
from app.schemas.response import TaskResponse
from typing import List

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskRead)
async def create_task(
    task: TaskCreate,
    session=Depends(get_session)
):
    db_task = Task.model_validate(task)
    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)
    return db_task

@router.get("/", response_model=List[TaskRead])
async def get_tasks(
    skip: int = 0,
    limit: int = 100,
    session=Depends(get_session)
):
    statement = select(Task).offset(skip).limit(limit)
    results = await session.execute(statement)
    tasks = results.scalars().all()
    return tasks

@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: int,
    session=Depends(get_session)
):
    statement = select(Task).where(Task.id == task_id)
    result = await session.execute(statement)
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    session=Depends(get_session)
):
    statement = select(Task).where(Task.id == task_id)
    result = await session.execute(statement)
    db_task = result.scalar_one_or_none()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)

    await session.commit()
    await session.refresh(db_task)
    return db_task

@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    session=Depends(get_session)
):
    statement = select(Task).where(Task.id == task_id)
    result = await session.execute(statement)
    db_task = result.scalar_one_or_none()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    await session.delete(db_task)
    await session.commit()
    return {"message": "Task deleted successfully"}
'''

    with open(base_path / "app" / "routes" / "tasks.py", "w") as f:
        f.write(routes_content)

def create_response_schema(base_path: Path):
    """Create response schemas"""
    schema_content = '''from pydantic import BaseModel
from typing import List, Optional
from app.models.task import TaskRead

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    priority: str
    created_at: str

class PaginatedTasks(BaseModel):
    items: List[TaskResponse]
    total: int
    page: int
    size: int
'''

    (base_path / "app" / "schemas").mkdir(exist_ok=True)
    with open(base_path / "app" / "schemas" / "response.py", "w") as f:
        f.write(schema_content)

def create_requirements(base_path: Path):
    """Create requirements.txt"""
    requirements_content = '''fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlmodel==0.0.16
asyncpg==0.29.0
python-multipart==0.0.6
pydantic==2.5.0
pydantic-settings==2.1.0
alembic==1.13.1
SQLAlchemy==2.0.23
httpx==0.25.2
pytest==7.4.3
pytest-asyncio==0.21.1
'''

    with open(base_path / "requirements.txt", "w") as f:
        f.write(requirements_content)

def create_pyproject_toml(base_path: Path):
    """Create pyproject.toml with uv settings"""
    pyproject_content = '''[project]
name = "todo-api"
version = "0.1.0"
description = "A todo API built with FastAPI and SQLModel"
authors = [
    {name = "Developer", email = "dev@example.com"}
]
dependencies = [
    "fastapi>=0.104.1",
    "uvicorn[standard]>=0.24.0",
    "sqlmodel>=0.0.16",
    "asyncpg>=0.29.0",
    "python-multipart>=0.0.6",
    "pydantic>=2.5.0",
    "pydantic-settings>=2.1.0",
    "alembic>=1.13.1",
    "SQLAlchemy>=2.0.23",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.3",
    "pytest-asyncio>=0.21.1",
    "black>=23.10.1",
    "isort>=5.12.0",
]

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["."]
include = ["app*"]

[tool.uv]
dev-dependencies = [
    "pytest>=7.4.3",
    "pytest-asyncio>=0.21.1",
    "black>=23.10.1",
    "isort>=5.12.0",
]
'''

    with open(base_path / "pyproject.toml", "w") as f:
        f.write(pyproject_content)

def create_env_file(base_path: Path):
    """Create .env.example file"""
    env_content = '''# Database
DATABASE_URL=postgresql+asyncpg://username:password@localhost/database_name

# Server
HOST=127.0.0.1
PORT=8000
DEBUG=False

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
'''

    with open(base_path / ".env.example", "w") as f:
        f.write(env_content)

def create_readme(base_path: Path):
    """Create README.md"""
    readme_content = f'''# {base_path.name}

A todo API built with FastAPI and SQLModel.

## Setup

1. Install dependencies:
```bash
uv pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

## Project Structure

- `app/main.py` - Main application entry point
- `app/models/` - Database models
- `app/routes/` - API route definitions
- `app/database/` - Database session and configuration
- `app/schemas/` - Pydantic schemas for request/response validation

## API Endpoints

- `GET /` - Health check
- `POST /api/v1/tasks/` - Create a task
- `GET /api/v1/tasks/` - Get all tasks
- `GET /api/v1/tasks/{{id}}` - Get a specific task
- `PUT /api/v1/tasks/{{id}}` - Update a task
- `DELETE /api/v1/tasks/{{id}}` - Delete a task
'''

    with open(base_path / "README.md", "w") as f:
        f.write(readme_content)

def main():
    if len(sys.argv) != 2:
        print("Usage: python init_fastapi_project.py <project_name>")
        sys.exit(1)

    project_name = sys.argv[1]

    print(f"Creating new FastAPI project: {project_name}")

    base_path = create_project_structure(project_name)
    create_main_app(base_path)
    create_database_session(base_path)
    create_task_model(base_path)
    create_task_routes(base_path)
    create_response_schema(base_path)
    create_requirements(base_path)
    create_pyproject_toml(base_path)
    create_env_file(base_path)
    create_readme(base_path)

    print(f"Project {project_name} created successfully!")
    print(f"Next steps:")
    print(f"1. cd {project_name}")
    print(f"2. Copy .env.example to .env and update configuration")
    print(f"3. Install dependencies with 'uv pip install -r requirements.txt'")
    print(f"4. Run with 'uvicorn app.main:app --reload'")

if __name__ == "__main__":
    main()