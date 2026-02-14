"""Tool definitions for Phase III AI Chatbot Integration.

Defines all 6 MCP tools in Cohere ToolV2 format for the TodoChatAgent.
"""
import cohere
from typing import List


def get_tool_definitions() -> List[cohere.ToolV2]:
    """Get all tool definitions in Cohere ToolV2 format.

    Returns:
        List of ToolV2 objects for Cohere agent
    """
    return [
        # Tool 1: add_task
        cohere.ToolV2(
            type="function",
            function={
                "name": "add_task",
                "description": "Create a new task for the user. Use this when the user wants to add, create, or make a new task.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Task title (1-255 characters, required)"
                        },
                        "description": {
                            "type": "string",
                            "description": "Task description (optional, can be empty string)"
                        },
                        "completed": {
                            "type": "boolean",
                            "description": "Initial completion status (default: false)"
                        }
                    },
                    "required": ["title"]
                }
            }
        ),

        # Tool 2: list_tasks
        cohere.ToolV2(
            type="function",
            function={
                "name": "list_tasks",
                "description": "Retrieve all tasks for the user. Can filter by completion status. Use this when the user wants to see, show, list, or view their tasks.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "completed": {
                            "type": "boolean",
                            "description": "Filter by completion status. If true, show only completed tasks. If false, show only pending tasks. If omitted, show all tasks."
                        }
                    }
                }
            }
        ),

        # Tool 3: complete_task
        cohere.ToolV2(
            type="function",
            function={
                "name": "complete_task",
                "description": "Mark a task as complete or incomplete. Use this when the user wants to complete, finish, mark as done, or toggle the completion status of a task.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "UUID of the task to update (required)"
                        },
                        "completed": {
                            "type": "boolean",
                            "description": "New completion status (default: true)"
                        }
                    },
                    "required": ["task_id"]
                }
            }
        ),

        # Tool 4: delete_task
        cohere.ToolV2(
            type="function",
            function={
                "name": "delete_task",
                "description": "Permanently delete a task. Use this when the user wants to delete, remove, or get rid of a task.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "UUID of the task to delete (required)"
                        }
                    },
                    "required": ["task_id"]
                }
            }
        ),

        # Tool 5: update_task
        cohere.ToolV2(
            type="function",
            function={
                "name": "update_task",
                "description": "Update a task's title or description. Use this when the user wants to change, update, edit, or modify a task.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "UUID of the task to update (required)"
                        },
                        "title": {
                            "type": "string",
                            "description": "New task title (optional, 1-255 characters)"
                        },
                        "description": {
                            "type": "string",
                            "description": "New task description (optional)"
                        }
                    },
                    "required": ["task_id"]
                }
            }
        ),

        # Tool 6: navigate
        cohere.ToolV2(
            type="function",
            function={
                "name": "navigate",
                "description": "Navigate to a different page in the application. Use this when the user wants to go to, open, visit, or navigate to a page. Available pages: dashboard, tasks, calendar, analytics, settings, evaluations.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "page": {
                            "type": "string",
                            "description": "Name of the page to navigate to (e.g., 'dashboard', 'tasks', 'calendar', 'analytics', 'settings', 'evaluations')"
                        }
                    },
                    "required": ["page"]
                }
            }
        ),
    ]


__all__ = ["get_tool_definitions"]
