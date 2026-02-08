"""
Basic tests for Python specialist patterns
"""

import pytest
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Field as SQLField


def test_pydantic_model_creation():
    """Test creating a basic Pydantic model following best practices"""

    class TaskCreate(BaseModel):
        title: str = Field(..., min_length=1, max_length=100)
        description: Optional[str] = None
        completed: bool = False

    # Test valid creation
    task = TaskCreate(title="Test task", description="A test task")
    assert task.title == "Test task"
    assert task.description == "A test task"
    assert task.completed is False

    # Test validation
    with pytest.raises(ValueError):
        TaskCreate(title="", description="Too short title")


def test_sqlmodel_definition():
    """Test creating a basic SQLModel following best practices"""

    class Task(SQLModel, table=True):
        id: Optional[int] = SQLField(default=None, primary_key=True)
        title: str = SQLField(sa_column_kwargs={"nullable": False})
        description: Optional[str] = None
        completed: bool = False
        created_at: datetime = SQLField(default_factory=datetime.utcnow)

    # Test model creation
    task = Task(title="Test task")
    assert task.title == "Test task"
    assert task.completed is False
    assert isinstance(task.created_at, datetime)


def test_union_types():
    """Test Python 3.10+ union type syntax"""

    def process_input(value: int | str | None) -> str:
        if value is None:
            return "none"
        return str(value).upper()

    assert process_input(42) == "42"
    assert process_input("hello") == "HELLO"
    assert process_input(None) == "none"


if __name__ == "__main__":
    # Run basic tests
    test_pydantic_model_creation()
    test_sqlmodel_definition()
    test_union_types()
    print("All tests passed!")