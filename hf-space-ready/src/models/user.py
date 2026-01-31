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

class UserCreate(SQLModel):
    email: str = Field(max_length=255)
    password: str = Field(min_length=6, max_length=100)

class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class UserLogin(SQLModel):
    email: str
    password: str
