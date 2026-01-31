from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import select
from app.models.task import Task, TaskCreate, TaskRead, TaskUpdate
from app.database.session import get_session
from sqlalchemy.exc import NoResultFound

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskRead)
async def create_task(
    task: TaskCreate,
    session=Depends(get_session)
):
    """
    Create a new task
    """
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
    """
    Get a list of tasks with pagination
    """
    statement = select(Task).offset(skip).limit(limit)
    results = await session.execute(statement)
    tasks = results.scalars().all()
    return tasks

@router.get("/{task_id}", response_model=TaskRead)
async def get_task_by_id(
    task_id: int,
    session=Depends(get_session)
):
    """
    Get a specific task by ID
    """
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
    """
    Update a specific task
    """
    statement = select(Task).where(Task.id == task_id)
    result = await session.execute(statement)
    db_task = result.scalar_one_or_none()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update the task with non-None values
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
    """
    Delete a specific task
    """
    statement = select(Task).where(Task.id == task_id)
    result = await session.execute(statement)
    db_task = result.scalar_one_or_none()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    await session.delete(db_task)
    await session.commit()
    return {"message": "Task deleted successfully"}