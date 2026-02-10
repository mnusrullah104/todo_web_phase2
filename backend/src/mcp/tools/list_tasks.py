"""List tasks tool for Phase III AI Chatbot Integration.

Implements the list_tasks MCP tool for retrieving tasks via chat.
"""
from sqlmodel import Session, select
from uuid import UUID
from typing import Dict, Any, Optional
import logging

from ...models.task import Task

logger = logging.getLogger(__name__)


async def list_tasks_impl(
    session: Session,
    user_id: UUID,
    completed: Optional[bool] = None
) -> Dict[str, Any]:
    """Implementation of list_tasks tool.

    Retrieves tasks for the specified user with optional filtering.

    Args:
        session: Database session
        user_id: UUID of the user (injected by ToolExecutor)
        completed: Optional filter by completion status
                  - True: show only completed tasks
                  - False: show only pending tasks
                  - None: show all tasks

    Returns:
        Structured response with task list or error
    """
    try:
        # Build query with user_id filter (CRITICAL for user isolation)
        statement = select(Task).where(Task.user_id == user_id)

        # Apply completion filter if specified
        if completed is not None:
            statement = statement.where(Task.completed == completed)

        # Order by created_at descending (most recent first)
        statement = statement.order_by(Task.created_at.desc())

        # Execute query
        tasks = session.exec(statement).all()

        # Determine filter label
        filter_label = "all"
        if completed is True:
            filter_label = "completed"
        elif completed is False:
            filter_label = "pending"

        logger.info(f"list_tasks: Retrieved {len(tasks)} {filter_label} tasks for user {user_id}")

        # Format task data
        task_data = [
            {
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
            for task in tasks
        ]

        return {
            "status": "success",
            "data": {
                "tasks": task_data,
                "count": len(tasks),
                "filter": filter_label
            }
        }

    except Exception as e:
        logger.error(f"list_tasks: Database error: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error": "database_error",
            "message": "Failed to retrieve tasks"
        }
