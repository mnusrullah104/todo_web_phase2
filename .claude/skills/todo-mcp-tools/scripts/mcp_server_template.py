"""
MCP Server Template for Task Management Tools
Uses Official MCP SDK with FastAPI and SQLModel

This template demonstrates the structure for implementing the 5 MCP tools:
- add_task
- list_tasks
- complete_task
- delete_task
- update_task
"""

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from sqlmodel import Session, select
from typing import Optional
import uuid
from datetime import datetime
import json

# Import your Task model and database session
# from your_app.models.task import Task
# from your_app.database.session import get_session


# Initialize MCP Server
app = Server("todo-mcp-server")


def validate_uuid(value: str, field_name: str) -> uuid.UUID:
    """Validate and convert string to UUID"""
    try:
        return uuid.UUID(value)
    except (ValueError, AttributeError):
        raise ValueError(f"{field_name} must be a valid UUID")


def success_response(data: dict) -> dict:
    """Standard success response format"""
    return {
        "status": "success",
        "data": data
    }


def error_response(error_type: str, message: str) -> dict:
    """Standard error response format"""
    return {
        "status": "error",
        "error": error_type,
        "message": message
    }


@app.list_tools()
async def list_tools() -> list[Tool]:
    """Register all 5 MCP tools"""
    return [
        Tool(
            name="add_task",
            description="Create a new task for a specific user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User UUID"},
                    "title": {"type": "string", "description": "Task title (1-255 chars)"},
                    "description": {"type": "string", "description": "Task description (optional, max 1000 chars)"},
                    "completed": {"type": "boolean", "description": "Completion status (default: false)"}
                },
                "required": ["user_id", "title"]
            }
        ),
        Tool(
            name="list_tasks",
            description="Retrieve all tasks for a specific user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User UUID"},
                    "completed": {"type": "boolean", "description": "Filter by completion status (optional)"}
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="complete_task",
            description="Mark a task as completed or uncompleted",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User UUID"},
                    "task_id": {"type": "string", "description": "Task UUID"},
                    "completed": {"type": "boolean", "description": "Completion status"}
                },
                "required": ["user_id", "task_id", "completed"]
            }
        ),
        Tool(
            name="delete_task",
            description="Permanently delete a task",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User UUID"},
                    "task_id": {"type": "string", "description": "Task UUID"}
                },
                "required": ["user_id", "task_id"]
            }
        ),
        Tool(
            name="update_task",
            description="Update task title, description, or completion status",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User UUID"},
                    "task_id": {"type": "string", "description": "Task UUID"},
                    "title": {"type": "string", "description": "New title (optional, 1-255 chars)"},
                    "description": {"type": "string", "description": "New description (optional, max 1000 chars)"},
                    "completed": {"type": "boolean", "description": "New completion status (optional)"}
                },
                "required": ["user_id", "task_id"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls"""

    try:
        if name == "add_task":
            return await handle_add_task(arguments)
        elif name == "list_tasks":
            return await handle_list_tasks(arguments)
        elif name == "complete_task":
            return await handle_complete_task(arguments)
        elif name == "delete_task":
            return await handle_delete_task(arguments)
        elif name == "update_task":
            return await handle_update_task(arguments)
        else:
            result = error_response("unknown_tool", f"Unknown tool: {name}")
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

    except Exception as e:
        result = error_response("internal_error", str(e))
        return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def handle_add_task(args: dict) -> list[TextContent]:
    """Implementation for add_task tool"""
    try:
        # Validate user_id
        user_uuid = validate_uuid(args["user_id"], "user_id")

        # Validate title
        title = args["title"].strip()
        if not title or len(title) > 255:
            result = error_response("validation_error", "Title is required and must be 1-255 characters")
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        # Validate description
        description = args.get("description")
        if description and len(description) > 1000:
            result = error_response("validation_error", "Description must be max 1000 characters")
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        completed = args.get("completed", False)

        # TODO: Get database session
        # session = get_session()

        # TODO: Create task in database
        # new_task = Task(
        #     user_id=user_uuid,
        #     title=title,
        #     description=description,
        #     completed=completed,
        #     created_at=datetime.utcnow(),
        #     updated_at=datetime.utcnow()
        # )
        # session.add(new_task)
        # session.commit()
        # session.refresh(new_task)

        # TODO: Return actual task data
        result = success_response({
            "id": str(uuid.uuid4()),
            "user_id": str(user_uuid),
            "title": title,
            "description": description,
            "completed": completed,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        })

        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    except ValueError as e:
        result = error_response("validation_error", str(e))
        return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def handle_list_tasks(args: dict) -> list[TextContent]:
    """Implementation for list_tasks tool"""
    try:
        # Validate user_id
        user_uuid = validate_uuid(args["user_id"], "user_id")

        completed_filter = args.get("completed")

        # TODO: Get database session and query tasks
        # session = get_session()
        # statement = select(Task).where(Task.user_id == user_uuid)
        # if completed_filter is not None:
        #     statement = statement.where(Task.completed == completed_filter)
        # tasks = session.exec(statement).all()

        # TODO: Return actual task list
        result = success_response({
            "tasks": [],
            "count": 0
        })

        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    except ValueError as e:
        result = error_response("validation_error", str(e))
        return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def handle_complete_task(args: dict) -> list[TextContent]:
    """Implementation for complete_task tool"""
    try:
        # Validate UUIDs
        user_uuid = validate_uuid(args["user_id"], "user_id")
        task_uuid = validate_uuid(args["task_id"], "task_id")

        completed = args["completed"]

        # TODO: Get database session and find task
        # session = get_session()
        # statement = select(Task).where(Task.id == task_uuid, Task.user_id == user_uuid)
        # task = session.exec(statement).first()

        # if not task:
        #     result = error_response("task_not_found", "Task not found or access denied")
        #     return [TextContent(type="text", text=json.dumps(result, indent=2))]

        # TODO: Update task
        # task.completed = completed
        # task.updated_at = datetime.utcnow()
        # session.add(task)
        # session.commit()
        # session.refresh(task)

        # TODO: Return actual task data
        result = success_response({
            "id": str(task_uuid),
            "user_id": str(user_uuid),
            "title": "Example task",
            "description": None,
            "completed": completed,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        })

        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    except ValueError as e:
        result = error_response("validation_error", str(e))
        return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def handle_delete_task(args: dict) -> list[TextContent]:
    """Implementation for delete_task tool"""
    try:
        # Validate UUIDs
        user_uuid = validate_uuid(args["user_id"], "user_id")
        task_uuid = validate_uuid(args["task_id"], "task_id")

        # TODO: Get database session and find task
        # session = get_session()
        # statement = select(Task).where(Task.id == task_uuid, Task.user_id == user_uuid)
        # task = session.exec(statement).first()

        # if not task:
        #     result = error_response("task_not_found", "Task not found or access denied")
        #     return [TextContent(type="text", text=json.dumps(result, indent=2))]

        # TODO: Delete task
        # session.delete(task)
        # session.commit()

        result = success_response({
            "message": "Task deleted successfully",
            "task_id": str(task_uuid)
        })

        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    except ValueError as e:
        result = error_response("validation_error", str(e))
        return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def handle_update_task(args: dict) -> list[TextContent]:
    """Implementation for update_task tool"""
    try:
        # Validate UUIDs
        user_uuid = validate_uuid(args["user_id"], "user_id")
        task_uuid = validate_uuid(args["task_id"], "task_id")

        # Check that at least one field is provided
        title = args.get("title")
        description = args.get("description")
        completed = args.get("completed")

        if title is None and description is None and completed is None:
            result = error_response("validation_error", "At least one field (title, description, or completed) must be provided")
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        # Validate title if provided
        if title is not None:
            title = title.strip()
            if not title or len(title) > 255:
                result = error_response("validation_error", "Title must be 1-255 characters")
                return [TextContent(type="text", text=json.dumps(result, indent=2))]

        # Validate description if provided
        if description is not None and len(description) > 1000:
            result = error_response("validation_error", "Description must be max 1000 characters")
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        # TODO: Get database session and find task
        # session = get_session()
        # statement = select(Task).where(Task.id == task_uuid, Task.user_id == user_uuid)
        # task = session.exec(statement).first()

        # if not task:
        #     result = error_response("task_not_found", "Task not found or access denied")
        #     return [TextContent(type="text", text=json.dumps(result, indent=2))]

        # TODO: Update task fields
        # if title is not None:
        #     task.title = title
        # if description is not None:
        #     task.description = description
        # if completed is not None:
        #     task.completed = completed
        # task.updated_at = datetime.utcnow()
        # session.add(task)
        # session.commit()
        # session.refresh(task)

        # TODO: Return actual task data
        result = success_response({
            "id": str(task_uuid),
            "user_id": str(user_uuid),
            "title": title or "Example task",
            "description": description,
            "completed": completed or False,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        })

        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    except ValueError as e:
        result = error_response("validation_error", str(e))
        return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
