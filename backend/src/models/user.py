from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
import uuid
from datetime import datetime

if TYPE_CHECKING:
    from .conversation import Conversation

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True, max_length=255)

class User(UserBase, table=True):
    __tablename__ = "users"

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships (Phase III - AI Chatbot)
    conversations: List["Conversation"] = Relationship(back_populates="user")

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
