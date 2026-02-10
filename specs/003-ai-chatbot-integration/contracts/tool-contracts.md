# Tool Contracts: MCP Task Management Tools

**Feature**: AI Chatbot Integration for Todo Management
**Date**: 2026-02-09
**Status**: Design
**Related Documents**: [spec.md](../spec.md), [plan.md](../plan.md), [data-model.md](../data-model.md)

## Overview

This document defines the contracts for the 5 MCP (Model Context Protocol) tools used by the AI assistant to manage tasks. These tools are invoked by the Cohere agent based on natural language commands and provide structured task operations.

## Design Principles

1. **User Isolation**: Every tool MUST accept and validate user_id
2. **Stateless**: Tools have no session state, all data from database
3. **Idempotent**: Where possible, tools should be safe to retry
4. **Structured Responses**: Consistent JSON format for success and errors
5. **Validation**: Input validation before database operations
6. **Error Handling**: Clear error messages for all failure modes

## Tool Response Format

All tools return structured JSON responses:

### Success Response
```json
{
  "status": "success",
  "data": {
    // Tool-specific data
  }
}
```

### Error Response
```json
{
  "status": "error",
  "error": "error_code",
  "message": "Human-readable error message"
}
```

### Error Codes

- `validation_error`: Invalid input parameters
- `not_found`: Resource not found
- `permission_denied`: User not authorized
- `database_error`: Database operation failed
- `internal_error`: Unexpected error

## Tool 1: add_task

Create a new task for the authenticated user.

### Tool Definition

```python
{
  "type": "function",
  "function": {
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
}
```

### Parameters

- **title** (string, required): Task title, 1-255 characters
- **description** (string, optional): Task description, default empty string
- **completed** (boolean, optional): Initial completion status, default false

**Note**: `user_id` is injected by ToolExecutor, not passed by LLM

### Success Response

```json
{
  "status": "success",
  "data": {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "title": "buy groceries",
    "description": "",
    "completed": false,
    "created_at": "2026-02-09T10:30:00Z",
    "updated_at": "2026-02-09T10:30:00Z"
  }
}
```

### Error Responses

**Validation Error - Empty Title:**
```json
{
  "status": "error",
  "error": "validation_error",
  "message": "Task title cannot be empty"
}
```

**Validation Error - Title Too Long:**
```json
{
  "status": "error",
  "error": "validation_error",
  "message": "Task title must be 255 characters or less"
}
```

### Examples

**Example 1: Simple Task**
```json
// Input
{
  "title": "buy groceries"
}

// Output
{
  "status": "success",
  "data": {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "title": "buy groceries",
    "description": "",
    "completed": false,
    "created_at": "2026-02-09T10:30:00Z",
    "updated_at": "2026-02-09T10:30:00Z"
  }
}
```

**Example 2: Task with Description**
```json
// Input
{
  "title": "finish report",
  "description": "needs charts and data analysis"
}

// Output
{
  "status": "success",
  "data": {
    "id": "770e8400-e29b-41d4-a716-446655440002",
    "title": "finish report",
    "description": "needs charts and data analysis",
    "completed": false,
    "created_at": "2026-02-09T10:31:00Z",
    "updated_at": "2026-02-09T10:31:00Z"
  }
}
```

**Example 3: Pre-completed Task**
```json
// Input
{
  "title": "review draft",
  "completed": true
}

// Output
{
  "status": "success",
  "data": {
    "id": "880e8400-e29b-41d4-a716-446655440003",
    "title": "review draft",
    "description": "",
    "completed": true,
    "created_at": "2026-02-09T10:32:00Z",
    "updated_at": "2026-02-09T10:32:00Z"
  }
}
```

---

## Tool 2: list_tasks

Retrieve tasks for the authenticated user with optional filtering.

### Tool Definition

```python
{
  "type": "function",
  "function": {
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
}
```

### Parameters

- **completed** (boolean, optional): Filter by completion status
  - `true`: Show only completed tasks
  - `false`: Show only pending tasks
  - `null/undefined`: Show all tasks

**Note**: `user_id` is injected by ToolExecutor, not passed by LLM

### Success Response

```json
{
  "status": "success",
  "data": {
    "tasks": [
      {
        "id": "660e8400-e29b-41d4-a716-446655440001",
        "title": "buy groceries",
        "description": "",
        "completed": false,
        "created_at": "2026-02-09T10:30:00Z",
        "updated_at": "2026-02-09T10:30:00Z"
      }
    ],
    "count": 1,
    "filter": "all"
  }
}
```

### Examples

**Example 1: List All Tasks**
```json
// Input
{}

// Output
{
  "status": "success",
  "data": {
    "tasks": [
      {
        "id": "660e8400-e29b-41d4-a716-446655440001",
        "title": "buy groceries",
        "description": "",
        "completed": false,
        "created_at": "2026-02-09T10:30:00Z",
        "updated_at": "2026-02-09T10:30:00Z"
      },
      {
        "id": "770e8400-e29b-41d4-a716-446655440002",
        "title": "finish report",
        "description": "needs charts",
        "completed": true,
        "created_at": "2026-02-09T09:00:00Z",
        "updated_at": "2026-02-09T10:00:00Z"
      }
    ],
    "count": 2,
    "filter": "all"
  }
}
```

**Example 2: List Pending Tasks**
```json
// Input
{
  "completed": false
}

// Output
{
  "status": "success",
  "data": {
    "tasks": [
      {
        "id": "660e8400-e29b-41d4-a716-446655440001",
        "title": "buy groceries",
        "description": "",
        "completed": false,
        "created_at": "2026-02-09T10:30:00Z",
        "updated_at": "2026-02-09T10:30:00Z"
      }
    ],
    "count": 1,
    "filter": "pending"
  }
}
```

**Example 3: List Completed Tasks**
```json
// Input
{
  "completed": true
}

// Output
{
  "status": "success",
  "data": {
    "tasks": [
      {
        "id": "770e8400-e29b-41d4-a716-446655440002",
        "title": "finish report",
        "description": "needs charts",
        "completed": true,
        "created_at": "2026-02-09T09:00:00Z",
        "updated_at": "2026-02-09T10:00:00Z"
      }
    ],
    "count": 1,
    "filter": "completed"
  }
}
```

**Example 4: No Tasks Found**
```json
// Input
{}

// Output
{
  "status": "success",
  "data": {
    "tasks": [],
    "count": 0,
    "filter": "all"
  }
}
```

---

## Tool 3: complete_task

Mark a task as complete or incomplete.

### Tool Definition

```python
{
  "type": "function",
  "function": {
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
}
```

### Parameters

- **task_id** (string, required): UUID of the task to update
- **completed** (boolean, optional): New completion status, default true

**Note**: `user_id` is injected by ToolExecutor, not passed by LLM

### Success Response

```json
{
  "status": "success",
  "data": {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "title": "buy groceries",
    "description": "",
    "completed": true,
    "created_at": "2026-02-09T10:30:00Z",
    "updated_at": "2026-02-09T10:35:00Z"
  }
}
```

### Error Responses

**Task Not Found:**
```json
{
  "status": "error",
  "error": "not_found",
  "message": "Task not found"
}
```

**Invalid Task ID:**
```json
{
  "status": "error",
  "error": "validation_error",
  "message": "Invalid task ID format"
}
```

**Permission Denied:**
```json
{
  "status": "error",
  "error": "permission_denied",
  "message": "Task does not belong to user"
}
```

### Examples

**Example 1: Mark Task Complete**
```json
// Input
{
  "task_id": "660e8400-e29b-41d4-a716-446655440001"
}

// Output
{
  "status": "success",
  "data": {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "title": "buy groceries",
    "description": "",
    "completed": true,
    "created_at": "2026-02-09T10:30:00Z",
    "updated_at": "2026-02-09T10:35:00Z"
  }
}
```

**Example 2: Mark Task Incomplete**
```json
// Input
{
  "task_id": "660e8400-e29b-41d4-a716-446655440001",
  "completed": false
}

// Output
{
  "status": "success",
  "data": {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "title": "buy groceries",
    "description": "",
    "completed": false,
    "created_at": "2026-02-09T10:30:00Z",
    "updated_at": "2026-02-09T10:36:00Z"
  }
}
```

---

## Tool 4: delete_task

Permanently delete a task.

### Tool Definition

```python
{
  "type": "function",
  "function": {
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
}
```

### Parameters

- **task_id** (string, required): UUID of the task to delete

**Note**: `user_id` is injected by ToolExecutor, not passed by LLM

### Success Response

```json
{
  "status": "success",
  "data": {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "deleted": true
  }
}
```

### Error Responses

**Task Not Found:**
```json
{
  "status": "error",
  "error": "not_found",
  "message": "Task not found"
}
```

**Invalid Task ID:**
```json
{
  "status": "error",
  "error": "validation_error",
  "message": "Invalid task ID format"
}
```

**Permission Denied:**
```json
{
  "status": "error",
  "error": "permission_denied",
  "message": "Task does not belong to user"
}
```

### Examples

**Example 1: Delete Task**
```json
// Input
{
  "task_id": "660e8400-e29b-41d4-a716-446655440001"
}

// Output
{
  "status": "success",
  "data": {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "deleted": true
  }
}
```

**Example 2: Task Not Found**
```json
// Input
{
  "task_id": "999e9999-e99b-99d9-a999-999999999999"
}

// Output
{
  "status": "error",
  "error": "not_found",
  "message": "Task not found"
}
```

---

## Tool 5: update_task

Update task title or description.

### Tool Definition

```python
{
  "type": "function",
  "function": {
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
}
```

### Parameters

- **task_id** (string, required): UUID of the task to update
- **title** (string, optional): New task title, 1-255 characters
- **description** (string, optional): New task description

**Note**: At least one of `title` or `description` must be provided

**Note**: `user_id` is injected by ToolExecutor, not passed by LLM

### Success Response

```json
{
  "status": "success",
  "data": {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "title": "buy groceries and household items",
    "description": "milk, bread, cleaning supplies",
    "completed": false,
    "created_at": "2026-02-09T10:30:00Z",
    "updated_at": "2026-02-09T10:40:00Z"
  }
}
```

### Error Responses

**Task Not Found:**
```json
{
  "status": "error",
  "error": "not_found",
  "message": "Task not found"
}
```

**No Fields to Update:**
```json
{
  "status": "error",
  "error": "validation_error",
  "message": "At least one field (title or description) must be provided"
}
```

**Invalid Task ID:**
```json
{
  "status": "error",
  "error": "validation_error",
  "message": "Invalid task ID format"
}
```

**Title Too Long:**
```json
{
  "status": "error",
  "error": "validation_error",
  "message": "Task title must be 255 characters or less"
}
```

**Permission Denied:**
```json
{
  "status": "error",
  "error": "permission_denied",
  "message": "Task does not belong to user"
}
```

### Examples

**Example 1: Update Title**
```json
// Input
{
  "task_id": "660e8400-e29b-41d4-a716-446655440001",
  "title": "buy groceries and household items"
}

// Output
{
  "status": "success",
  "data": {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "title": "buy groceries and household items",
    "description": "",
    "completed": false,
    "created_at": "2026-02-09T10:30:00Z",
    "updated_at": "2026-02-09T10:40:00Z"
  }
}
```

**Example 2: Update Description**
```json
// Input
{
  "task_id": "660e8400-e29b-41d4-a716-446655440001",
  "description": "milk, bread, cleaning supplies"
}

// Output
{
  "status": "success",
  "data": {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "title": "buy groceries",
    "description": "milk, bread, cleaning supplies",
    "completed": false,
    "created_at": "2026-02-09T10:30:00Z",
    "updated_at": "2026-02-09T10:41:00Z"
  }
}
```

**Example 3: Update Both Fields**
```json
// Input
{
  "task_id": "660e8400-e29b-41d4-a716-446655440001",
  "title": "buy groceries and household items",
  "description": "milk, bread, cleaning supplies"
}

// Output
{
  "status": "success",
  "data": {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "title": "buy groceries and household items",
    "description": "milk, bread, cleaning supplies",
    "completed": false,
    "created_at": "2026-02-09T10:30:00Z",
    "updated_at": "2026-02-09T10:42:00Z"
  }
}
```

---

## Tool Chaining Examples

The AI assistant can invoke multiple tools in a single conversation turn.

### Example 1: Add and Complete

**User Message**: "Add a task to call dentist and mark it as done"

**Tool Calls**:
```json
[
  {
    "tool": "add_task",
    "arguments": {
      "title": "call dentist"
    }
  },
  {
    "tool": "complete_task",
    "arguments": {
      "task_id": "{{new_task_id}}",
      "completed": true
    }
  }
]
```

### Example 2: List and Delete

**User Message**: "Show me my completed tasks and delete the first one"

**Tool Calls**:
```json
[
  {
    "tool": "list_tasks",
    "arguments": {
      "completed": true
    }
  },
  {
    "tool": "delete_task",
    "arguments": {
      "task_id": "{{first_task_id}}"
    }
  }
]
```

### Example 3: Add Multiple Tasks

**User Message**: "Add three tasks: buy milk, walk dog, pay bills"

**Tool Calls**:
```json
[
  {
    "tool": "add_task",
    "arguments": {
      "title": "buy milk"
    }
  },
  {
    "tool": "add_task",
    "arguments": {
      "title": "walk dog"
    }
  },
  {
    "tool": "add_task",
    "arguments": {
      "title": "pay bills"
    }
  }
]
```

## Implementation Requirements

### User Isolation

**CRITICAL**: Every tool implementation MUST:
1. Accept `user_id` parameter (injected by ToolExecutor)
2. Validate `user_id` is valid UUID
3. Filter all database queries by `user_id`
4. Reject operations on tasks not belonging to user

### Validation

All tools MUST validate:
- Parameter types and formats
- UUID format for IDs
- String length constraints
- Required fields presence

### Error Handling

All tools MUST:
- Return structured error responses
- Use appropriate error codes
- Provide helpful error messages
- Log errors for debugging

### Database Operations

All tools MUST:
- Use SQLModel session from dependency injection
- Commit transactions on success
- Rollback transactions on error
- Handle database exceptions gracefully

## Testing Checklist

### Unit Tests (Per Tool)
- [ ] Valid input returns success
- [ ] Invalid input returns validation error
- [ ] Missing required fields returns error
- [ ] User isolation enforced
- [ ] Database errors handled

### Integration Tests
- [ ] Tool execution through ToolExecutor
- [ ] User_id injection works correctly
- [ ] Database transactions commit/rollback
- [ ] Tool chaining works correctly

### Security Tests
- [ ] Cannot access other users' tasks
- [ ] Invalid user_id rejected
- [ ] SQL injection prevented
- [ ] Input sanitization works

## Related Documents

- [spec.md](../spec.md) - Feature requirements (FR-006 to FR-018)
- [plan.md](../plan.md) - Architecture decisions (AD-002: Direct tool implementation)
- [chat-endpoint.md](chat-endpoint.md) - Chat API specification
- [data-model.md](../data-model.md) - Database schema
