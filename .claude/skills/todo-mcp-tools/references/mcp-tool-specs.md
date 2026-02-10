# MCP Tool Specifications for Task Management

This document defines the exact specifications for the 5 MCP tools that manage tasks in the Phase III Todo application.

## Tool Registration

All tools must be registered with the MCP server using the Official MCP SDK. Each tool must be discoverable via MCP protocol.

## Common Requirements

### User Isolation
- **CRITICAL**: Every tool MUST accept `user_id` as a required parameter
- **CRITICAL**: Every database query MUST filter by `user_id`
- Users can ONLY access their own tasks
- Attempting to access another user's tasks must fail gracefully

### Database Interaction
- Use SQLModel with the Task table
- Task model fields:
  - `id`: UUID (primary key, auto-generated)
  - `user_id`: UUID (indexed, required)
  - `title`: str (1-255 chars, required)
  - `description`: Optional[str] (max 1000 chars)
  - `completed`: bool (default False)
  - `created_at`: datetime (auto-generated)
  - `updated_at`: datetime (auto-updated)

### Error Handling
- Return structured error responses with `status` and `error` fields
- Common error types:
  - `invalid_user_id`: User ID format is invalid
  - `task_not_found`: Task does not exist or user lacks access
  - `validation_error`: Input validation failed
  - `database_error`: Database operation failed

### Response Format
All successful responses must include:
```json
{
  "status": "success",
  "data": { ... }
}
```

All error responses must include:
```json
{
  "status": "error",
  "error": "error_type",
  "message": "Human-readable error message"
}
```

---

## Tool 1: add_task

**Description**: Create a new task for a specific user

**Parameters**:
```json
{
  "user_id": "string (UUID format, required)",
  "title": "string (1-255 chars, required)",
  "description": "string (max 1000 chars, optional)",
  "completed": "boolean (optional, default: false)"
}
```

**Returns**:
```json
{
  "status": "success",
  "data": {
    "id": "uuid",
    "user_id": "uuid",
    "title": "string",
    "description": "string or null",
    "completed": false,
    "created_at": "ISO 8601 datetime",
    "updated_at": "ISO 8601 datetime"
  }
}
```

**Example Success**:
```json
{
  "status": "success",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2026-02-09T10:30:00Z",
    "updated_at": "2026-02-09T10:30:00Z"
  }
}
```

**Example Error**:
```json
{
  "status": "error",
  "error": "validation_error",
  "message": "Title is required and must be 1-255 characters"
}
```

---

## Tool 2: list_tasks

**Description**: Retrieve all tasks for a specific user

**Parameters**:
```json
{
  "user_id": "string (UUID format, required)",
  "completed": "boolean (optional, filter by completion status)"
}
```

**Returns**:
```json
{
  "status": "success",
  "data": {
    "tasks": [
      {
        "id": "uuid",
        "user_id": "uuid",
        "title": "string",
        "description": "string or null",
        "completed": boolean,
        "created_at": "ISO 8601 datetime",
        "updated_at": "ISO 8601 datetime"
      }
    ],
    "count": integer
  }
}
```

**Example Success**:
```json
{
  "status": "success",
  "data": {
    "tasks": [
      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "user_id": "123e4567-e89b-12d3-a456-426614174000",
        "title": "Buy groceries",
        "description": "Milk, eggs, bread",
        "completed": false,
        "created_at": "2026-02-09T10:30:00Z",
        "updated_at": "2026-02-09T10:30:00Z"
      },
      {
        "id": "660e8400-e29b-41d4-a716-446655440001",
        "user_id": "123e4567-e89b-12d3-a456-426614174000",
        "title": "Finish report",
        "description": null,
        "completed": true,
        "created_at": "2026-02-08T14:20:00Z",
        "updated_at": "2026-02-09T09:15:00Z"
      }
    ],
    "count": 2
  }
}
```

**Example Error**:
```json
{
  "status": "error",
  "error": "invalid_user_id",
  "message": "User ID must be a valid UUID"
}
```

---

## Tool 3: complete_task

**Description**: Mark a task as completed or uncompleted

**Parameters**:
```json
{
  "user_id": "string (UUID format, required)",
  "task_id": "string (UUID format, required)",
  "completed": "boolean (required)"
}
```

**Returns**:
```json
{
  "status": "success",
  "data": {
    "id": "uuid",
    "user_id": "uuid",
    "title": "string",
    "description": "string or null",
    "completed": boolean,
    "created_at": "ISO 8601 datetime",
    "updated_at": "ISO 8601 datetime"
  }
}
```

**Example Success**:
```json
{
  "status": "success",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": true,
    "created_at": "2026-02-09T10:30:00Z",
    "updated_at": "2026-02-09T11:45:00Z"
  }
}
```

**Example Error**:
```json
{
  "status": "error",
  "error": "task_not_found",
  "message": "Task not found or access denied"
}
```

---

## Tool 4: delete_task

**Description**: Permanently delete a task

**Parameters**:
```json
{
  "user_id": "string (UUID format, required)",
  "task_id": "string (UUID format, required)"
}
```

**Returns**:
```json
{
  "status": "success",
  "data": {
    "message": "Task deleted successfully",
    "task_id": "uuid"
  }
}
```

**Example Success**:
```json
{
  "status": "success",
  "data": {
    "message": "Task deleted successfully",
    "task_id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

**Example Error**:
```json
{
  "status": "error",
  "error": "task_not_found",
  "message": "Task not found or access denied"
}
```

---

## Tool 5: update_task

**Description**: Update task title, description, or completion status

**Parameters**:
```json
{
  "user_id": "string (UUID format, required)",
  "task_id": "string (UUID format, required)",
  "title": "string (1-255 chars, optional)",
  "description": "string (max 1000 chars, optional)",
  "completed": "boolean (optional)"
}
```

**Note**: At least one of title, description, or completed must be provided.

**Returns**:
```json
{
  "status": "success",
  "data": {
    "id": "uuid",
    "user_id": "uuid",
    "title": "string",
    "description": "string or null",
    "completed": boolean,
    "created_at": "ISO 8601 datetime",
    "updated_at": "ISO 8601 datetime"
  }
}
```

**Example Success**:
```json
{
  "status": "success",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Buy groceries and household items",
    "description": "Milk, eggs, bread, paper towels",
    "completed": false,
    "created_at": "2026-02-09T10:30:00Z",
    "updated_at": "2026-02-09T12:00:00Z"
  }
}
```

**Example Error**:
```json
{
  "status": "error",
  "error": "validation_error",
  "message": "At least one field (title, description, or completed) must be provided"
}
```

---

## Tool Chaining Examples

### Example 1: Create and Complete
```
1. add_task(user_id="...", title="Review PR")
   → Returns task with id="abc-123"
2. complete_task(user_id="...", task_id="abc-123", completed=true)
   → Returns updated task with completed=true
```

### Example 2: List, Update, Delete
```
1. list_tasks(user_id="...", completed=false)
   → Returns list of incomplete tasks
2. update_task(user_id="...", task_id="xyz-789", title="Updated title")
   → Returns updated task
3. delete_task(user_id="...", task_id="xyz-789")
   → Returns success message
```

---

## Implementation Checklist

- [ ] All 5 tools registered with MCP server
- [ ] Each tool accepts user_id parameter
- [ ] Database queries filter by user_id
- [ ] UUID validation for user_id and task_id
- [ ] Structured error responses with status/error/message
- [ ] Structured success responses with status/data
- [ ] Task model matches SQLModel schema
- [ ] Timestamps auto-update on modifications
- [ ] Tools are discoverable via MCP protocol
- [ ] Error handling covers all edge cases
