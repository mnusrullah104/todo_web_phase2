"""Add task tool for Phase III AI Chatbot Integration.

Implements the add_task MCP tool for creating new tasks via chat.
"""
from sqlmodel import Session
from uuid import UUID
from typing import Dict, Any
import logging

from ...models.task import Task

logger = logging.getLogger(__name__)


async def add_task_impl(
    session: Session,
    user_id: UUID,
    title: str,
    description: str = "",
    completed: bool = False
) -> Dict[str, Any]:
    """Implementation of add_task tool.

    Creates a new task for the specified user.

    Args:
        session: Database session
        user_id: UUID of the user (injected by ToolExecutor)
        title: Task title (1-255 characters)
        description: Optional task description
        completed: Initial completion status (default: False)

    Returns:
        Structured response with task data or error
    """
    # Validate title
    if not title or not title.strip():
        logger.warning("add_task: Empty title provided")
        return {
            "status": "error",
            "error": "validation_error",
            "message": "Task title cannot be empty"
        }

    if len(title) > 255:
        logger.warning(f"add_task: Title too long ({len(title)} chars)")
        return {
            "status": "error",
            "error": "validation_error",
            "message": "Task title must be 255 characters or less"
        }

    try:
        # Create task
        new_task = Task(
            user_id=user_id,
            title=title.strip(),
            description=description.strip() if description else "",
            completed=completed
        )

        session.add(new_task)
        session.commit()
        session.refresh(new_task)

        logger.info(f"add_task: Created task {new_task.id} for user {user_id}")

        return {
            "status": "success",
            "data": {
                "id": str(new_task.id),
                "title": new_task.title,
                "description": new_task.description,
                "completed": new_task.completed,
                "created_at": new_task.created_at.isoformat(),
                "updated_at": new_task.updated_at.isoformat()
            }
        }

    except Exception as e:
        logger.error(f"add_task: Database error: {str(e)}", exc_info=True)
        session.rollback()
        return {
            "status": "error",
            "error": "database_error",
            "message": "Failed to create task"
        }
