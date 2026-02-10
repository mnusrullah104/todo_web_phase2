"""Delete task tool for Phase III AI Chatbot Integration.

Implements the delete_task MCP tool for permanently removing tasks via chat.
"""
from sqlmodel import Session, select
from uuid import UUID
from typing import Dict, Any
import logging

from ...models.task import Task

logger = logging.getLogger(__name__)


async def delete_task_impl(
    session: Session,
    user_id: UUID,
    task_id: str
) -> Dict[str, Any]:
    """Implementation of delete_task tool.

    Permanently deletes a task for the specified user.

    Args:
        session: Database session
        user_id: UUID of the user (injected by ToolExecutor)
        task_id: UUID string of the task to delete

    Returns:
        Structured response with deletion confirmation or error
    """
    # Validate and parse task_id
    try:
        task_uuid = UUID(task_id)
    except (ValueError, AttributeError):
        logger.warning(f"delete_task: Invalid task_id format: {task_id}")
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
            logger.warning(f"delete_task: Task {task_id} not found for user {user_id}")
            return {
                "status": "error",
                "error": "not_found",
                "message": "Task not found"
            }

        # Store task info before deletion
        task_title = task.title
        task_id_str = str(task.id)

        # Delete task
        session.delete(task)
        session.commit()

        logger.info(f"delete_task: Deleted task {task_id} ('{task_title}') for user {user_id}")

        return {
            "status": "success",
            "data": {
                "id": task_id_str,
                "title": task_title,
                "message": "Task deleted successfully"
            }
        }

    except Exception as e:
        logger.error(f"delete_task: Database error: {str(e)}", exc_info=True)
        session.rollback()
        return {
            "status": "error",
            "error": "database_error",
            "message": "Failed to delete task"
        }
