"""Complete task tool for Phase III AI Chatbot Integration.

Implements the complete_task MCP tool for marking tasks as complete/incomplete via chat.
"""
from sqlmodel import Session, select
from uuid import UUID
from typing import Dict, Any
import logging

from ...models.task import Task

logger = logging.getLogger(__name__)


async def complete_task_impl(
    session: Session,
    user_id: UUID,
    task_id: str,
    completed: bool = True
) -> Dict[str, Any]:
    """Implementation of complete_task tool.

    Marks a task as complete or incomplete for the specified user.

    Args:
        session: Database session
        user_id: UUID of the user (injected by ToolExecutor)
        task_id: UUID string of the task to update
        completed: New completion status (default: True)

    Returns:
        Structured response with updated task data or error
    """
    # Validate and parse task_id
    try:
        task_uuid = UUID(task_id)
    except (ValueError, AttributeError):
        logger.warning(f"complete_task: Invalid task_id format: {task_id}")
        return {
            "status": "error",
            "error": "validation_error",
            "message": "Invalid task ID format"
        }

    try:
        # Query task with user_id filter (CRITICAL for user isolation)
        statement = select(Task).where(
            Task.id == task_uuid,
            Task.user_id == user_id
        )
        task = session.exec(statement).first()

        if not task:
            logger.warning(f"complete_task: Task {task_id} not found for user {user_id}")
            return {
                "status": "error",
                "error": "not_found",
                "message": "Task not found"
            }

        # Update completion status
        task.completed = completed
        session.add(task)
        session.commit()
        session.refresh(task)

        status_text = "completed" if completed else "incomplete"
        logger.info(f"complete_task: Marked task {task_id} as {status_text} for user {user_id}")

        return {
            "status": "success",
            "data": {
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
        }

    except Exception as e:
        logger.error(f"complete_task: Database error: {str(e)}", exc_info=True)
        session.rollback()
        return {
            "status": "error",
            "error": "database_error",
            "message": "Failed to update task completion status"
        }
