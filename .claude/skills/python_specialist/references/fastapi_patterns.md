  # FastAPI Patterns and Best Practices

## Application Structure

### Basic Setup
```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import AsyncGenerator

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup
    yield
    # Shutdown
    pass

app = FastAPI(lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Dependency Injection

### Security Dependencies
```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated

security = HTTPBearer()

async def get_current_user(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]) -> dict:
    # Validate token and return user
    pass
```

### Database Session
```python
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

async def get_session() -> AsyncSession:
    async with AsyncSession(engine) as session:
        yield session
```

## Request/Response Models

### Using Pydantic
```python
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    priority: Priority = Priority.MEDIUM
    due_date: datetime | None = None

class TaskResponse(TaskCreate):
    id: int
    created_at: datetime
    completed: bool = False
```

## Route Patterns

### CRUD Operations
```python
from fastapi import APIRouter, Depends
from sqlmodel import select

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskResponse)
async def create_task(
    task: TaskCreate,
    session: AsyncSession = Depends(get_session)
) -> TaskResponse:
    db_task = Task.model_validate(task)
    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)
    return db_task

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    session: AsyncSession = Depends(get_session)
) -> TaskResponse:
    statement = select(Task).where(Task.id == task_id)
    result = await session.execute(statement)
    task = result.first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
```

## Error Handling

### Custom Exceptions
```python
from fastapi import status

class TaskNotFoundError(Exception):
    def __init__(self, task_id: int):
        self.task_id = task_id
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = f"Task with id {task_id} not found"

@app.exception_handler(TaskNotFoundError)
async def task_not_found_handler(request, exc: TaskNotFoundError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
```

## Testing
- Use pytest with FastAPI's TestClient
- Mock external dependencies
- Test both success and error cases
- Include integration tests with database