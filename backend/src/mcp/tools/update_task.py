"""Update task tool for Phase III AI Chatbot Integration.

Implements the update_task MCP tool for modifying task details via chat.
"""
from sqlmodel import Session, select
from uuid import UUID
from typing import Dict, Any, Optional
import logging

from ...models.task import Task

logger = logging.getLogger(__name__)


async def update_task_impl(
    session: Session,
    user_id: UUID,
    task_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> Dict[str, Any]:
    """Implementation of update_task tool.

    Updates a task's title and/or description for the specified user.

    Args:
        session: Database session
        user_id: UUID of the user (injected by ToolExecutor)
        task_id: UUID string of the task to update
        title: Optional new title (1-255 characters)
        description: Optional new description

    Returns:
        Structured response with updated task data or error
    """
    # Validate that at least one field is provided
    if title is None and description is None:
        logger.warning("update_task: No fields provided for update")
        return {
            "status": "error",
            "error": "validation_error",
            "message": "At least one field (title or description) must be provided"
        }

    # Validate and parse task_id
    try:
        task_uuid = UUID(task_id)
    except (ValueError, AttributeError):
        logger.warning(f"update_task: Invalid task_id format: {task_id}")
        return {
            "status": "error",
            "error": "validation_error",
            "message": "Invalid task ID format"
        }

    # Validate title if provided
    if title is not None:
        if not title.strip():
            logger.warning("update_task: Empty title provided")
            return {
                "status": "error",
                "error": "validation_error",
                "message": "Task title cannot be empty"
            }
        if len(title) > 255:
            logger.warning(f"update_task: Title too long ({len(title)} chars)")
            return {
                "status": "error",
                "error": "validation_error",
                "message": "Task title must be 255 characters or less"
            }

    try:
        # Query task with user_id filter (CRITICAL for user isolation)
        statement = select(Task).where(
            Task.id == task_uuid,
            Task.user_id == user_id
        )
        task = session.exec(statement).first()

        if not task:
            logger.warning(f"update_task: Task {task_id} not found for user {user_id}")
            return {
                "status": "error",
                "error": "not_found",
                "message": "Task not found"
            }

        # Update fields
        updated_fields = []
        if title is not None:
            task.title = title.strip()
            updated_fields.append("title")
        if description is not None:
            task.description = description.strip() if description else ""
            updated_fields.append("description")

        session.add(task)
        session.commit()
        session.refresh(task)

        logger.info(f"update_task: Updated {', '.join(updated_fields)} for task {task_id} (user {user_id})")

        return {
            "status": "success",
            "data": {
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat(),
                "updated_fields": updated_fields
            }
        }

    except Exception as e:
        logger.error(f"update_task: Database error: {str(e)}", exc_info=True)
        session.rollback()
        return {
            "status": "error",
            "error": "database_error",
            "message": "Failed to update task"
        }
