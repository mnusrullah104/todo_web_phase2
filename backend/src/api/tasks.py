from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
import uuid
from datetime import datetime

from ..models.task import Task, TaskCreate, TaskUpdate, TaskPatchComplete, TaskRead
from ..schemas.task import TaskListResponse
from ..auth.jwt import get_current_user
from ..database.session import get_session

router = APIRouter(tags=["tasks"])

@router.get("/tasks", response_model=List[TaskRead])
async def get_tasks(
    user_id: str = None,  # This will be extracted from the path via the prefix
    current_user_id: uuid.UUID = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for a specific user from database.
    Validates that the user_id in the URL matches the authenticated user.
    """
    # Validate that the user_id in URL matches the authenticated user
    if str(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's tasks"
        )

    # Query database for user's tasks
    statement = select(Task).where(Task.user_id == current_user_id)
    tasks = session.exec(statement).all()

    return tasks


@router.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_create: TaskCreate,
    user_id: str = None,  # This will be extracted from the path via the prefix
    current_user_id: uuid.UUID = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task in database for the specified user.
    Validates that the user_id in the URL matches the authenticated user.
    """
    # Validate that the user_id in URL matches the authenticated user
    if str(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks for this user"
        )

    # Create new task in database
    new_task = Task(
        user_id=current_user_id,
        title=task_create.title,
        description=task_create.description,
        completed=task_create.completed if task_create.completed is not None else False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    return new_task


@router.get("/tasks/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: str,
    user_id: str = None,  # This will be extracted from the path via the prefix
    current_user_id: uuid.UUID = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task from database for the specified user.
    Validates that the user_id in the URL matches the authenticated user.
    """
    # Validate that the user_id in URL matches the authenticated user
    if str(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's tasks"
        )

    # Query database for task with ownership verification
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )

    statement = select(Task).where(Task.id == task_uuid, Task.user_id == current_user_id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put("/tasks/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: str,
    task_update: TaskUpdate,
    user_id: str = None,  # This will be extracted from the path via the prefix
    current_user_id: uuid.UUID = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific task in database for the specified user.
    Validates that the user_id in the URL matches the authenticated user.
    """
    # Validate that the user_id in URL matches the authenticated user
    if str(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user's tasks"
        )

    # Query database for task with ownership verification
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )

    statement = select(Task).where(Task.id == task_uuid, Task.user_id == current_user_id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update task fields
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(task, field, value)

    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: str,
    user_id: str = None,  # This will be extracted from the path via the prefix
    current_user_id: uuid.UUID = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task from database for the specified user.
    Validates that the user_id in the URL matches the authenticated user.
    """
    # Validate that the user_id in URL matches the authenticated user
    if str(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user's tasks"
        )

    # Query database for task with ownership verification
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )

    statement = select(Task).where(Task.id == task_uuid, Task.user_id == current_user_id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    session.delete(task)
    session.commit()

    return {"message": "Task deleted successfully"}


@router.patch("/tasks/{task_id}/complete")
async def update_task_completion(
    task_id: str,
    task_patch_complete: TaskPatchComplete,
    user_id: str = None,  # This will be extracted from the path via the prefix
    current_user_id: uuid.UUID = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update the completion status of a specific task in database.
    Validates that the user_id in the URL matches the authenticated user.
    """
    # Validate that the user_id in URL matches the authenticated user
    if str(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user's task status"
        )

    # Query database for task with ownership verification
    try:
        task_uuid = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )

    statement = select(Task).where(Task.id == task_uuid, Task.user_id == current_user_id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update completion status
    task.completed = task_patch_complete.completed
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)

    return {"message": "Task completion status updated successfully", "task": task}
