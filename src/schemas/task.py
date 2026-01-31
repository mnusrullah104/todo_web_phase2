from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime

# Base schemas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

# Create schema
class TaskCreate(TaskBase):
    pass

# Read schema
class TaskRead(TaskBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

# Update schema
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

# Patch completion schema
class TaskPatchComplete(BaseModel):
    completed: bool

# List response schema
class TaskListResponse(BaseModel):
    tasks: List[TaskRead]