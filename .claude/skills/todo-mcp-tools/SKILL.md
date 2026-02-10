---
name: todo-mcp-tools
description: "Implement stateless, user-scoped MCP tools for task management using Official MCP SDK with FastAPI and SQLModel. Use this skill when: (1) Building or setting up an MCP server for task operations, (2) Implementing or fixing the 5 core task tools (add_task, list_tasks, complete_task, delete_task, update_task), (3) Ensuring proper user isolation and database integration, (4) Debugging MCP tool registration or tool call handling. This skill provides exact specifications, implementation templates, and validation checklists for creating production-ready MCP tools that are stateless, database-driven, and strictly enforce user_id scoping."
---

# Todo MCP Tools Implementation Guide

Implement the 5 MCP tools for task management using the Official MCP SDK with FastAPI and SQLModel.

## Core Requirements

### Stateless Design
- No server-side session state
- All context passed in each request
- Database is the single source of truth
- Tools are independently callable

### User Isolation (CRITICAL)
- Every tool MUST accept `user_id` parameter
- Every database query MUST filter by `user_id`
- Users can ONLY access their own tasks
- Validate UUID format for all IDs

### Database Integration
- Use SQLModel with Task table
- Task model fields: id, user_id, title, description, completed, created_at, updated_at
- Auto-update timestamps on modifications
- Handle database errors gracefully

## Implementation Workflow

### Step 1: Review Specifications
Read the complete tool specifications in `references/mcp-tool-specs.md` to understand:
- Exact parameter schemas for each tool
- Expected return formats (success and error)
- User isolation requirements
- Tool chaining examples

### Step 2: Set Up MCP Server
Use the template in `scripts/mcp_server_template.py` as a starting point:

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server

app = Server("todo-mcp-server")

@app.list_tools()
async def list_tools() -> list[Tool]:
    # Register all 5 tools
    pass

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    # Route to appropriate handler
    pass
```

### Step 3: Implement Each Tool
For each of the 5 tools, follow this pattern:

1. **Validate inputs**
   - Convert user_id and task_id to UUID
   - Validate string lengths (title: 1-255, description: max 1000)
   - Check required fields

2. **Query database with user_id filter**
   ```python
   statement = select(Task).where(
       Task.user_id == user_uuid,
       # Additional filters as needed
   )
   ```

3. **Perform operation**
   - Create, read, update, or delete task
   - Update timestamps for modifications

4. **Return structured response**
   - Success: `{"status": "success", "data": {...}}`
   - Error: `{"status": "error", "error": "error_type", "message": "..."}`

### Step 4: Test Tool Registration
Verify all tools are discoverable:
```python
# Tools should appear in MCP protocol discovery
tools = await app.list_tools()
assert len(tools) == 5
assert "add_task" in [t.name for t in tools]
```

### Step 5: Test Tool Execution
Test each tool with valid and invalid inputs:
- Valid user_id and parameters → success response
- Invalid UUID format → validation error
- Non-existent task → task_not_found error
- Wrong user_id → task_not_found (access denied)

## Tool Implementation Checklist

Use this checklist for each tool:

- [ ] Tool registered in `list_tools()` with correct schema
- [ ] Handler function created in `call_tool()`
- [ ] user_id parameter validated and converted to UUID
- [ ] task_id parameter validated (if applicable)
- [ ] Database query filters by user_id
- [ ] Input validation matches spec (string lengths, required fields)
- [ ] Success response matches spec format
- [ ] Error responses cover all edge cases
- [ ] Timestamps updated on modifications
- [ ] Tool tested with valid inputs
- [ ] Tool tested with invalid inputs
- [ ] Tool tested with wrong user_id (access control)

## Common Patterns

### UUID Validation
```python
def validate_uuid(value: str, field_name: str) -> uuid.UUID:
    try:
        return uuid.UUID(value)
    except (ValueError, AttributeError):
        raise ValueError(f"{field_name} must be a valid UUID")
```

### Response Formatting
```python
def success_response(data: dict) -> dict:
    return {"status": "success", "data": data}

def error_response(error_type: str, message: str) -> dict:
    return {"status": "error", "error": error_type, "message": message}
```

### User-Scoped Query
```python
# Always include user_id filter
statement = select(Task).where(
    Task.id == task_uuid,
    Task.user_id == user_uuid  # CRITICAL: Enforce user isolation
)
task = session.exec(statement).first()

if not task:
    return error_response("task_not_found", "Task not found or access denied")
```

## Error Types

Use these standard error types:
- `validation_error`: Invalid input (format, length, missing required field)
- `invalid_user_id`: User ID is not a valid UUID
- `task_not_found`: Task doesn't exist or user lacks access
- `database_error`: Database operation failed
- `internal_error`: Unexpected server error

## Quality Standards

### Must Have
- All 5 tools implemented and registered
- Strict user_id enforcement in every query
- Structured responses (status + data/error)
- UUID validation for all IDs
- Input validation per spec

### Must Not Have
- Hardcoded user IDs or task IDs
- Queries without user_id filter
- Unstructured error messages
- Missing error handling
- Tools that access other users' data

## Integration with Existing Code

If integrating with existing FastAPI backend:

1. **Import existing models**
   ```python
   from backend.src.models.task import Task
   from backend.src.database.session import get_session
   ```

2. **Reuse validation logic**
   - Leverage existing Pydantic/SQLModel schemas
   - Use existing database session management

3. **Maintain consistency**
   - Match existing error response formats
   - Follow existing naming conventions
   - Use existing timestamp handling

## Debugging Tips

### Tool Not Discoverable
- Check tool is in `list_tools()` return value
- Verify inputSchema is valid JSON Schema
- Ensure tool name matches in `call_tool()` router

### Tool Call Fails
- Log arguments received in `call_tool()`
- Verify UUID conversion succeeds
- Check database query returns expected results
- Validate response format matches spec

### Access Control Issues
- Confirm user_id filter in ALL queries
- Test with different user_ids
- Verify task_not_found returned for wrong user

## Reference Materials

- **Complete Tool Specs**: See `references/mcp-tool-specs.md` for detailed parameter schemas, return formats, examples, and tool chaining patterns
- **Implementation Template**: See `scripts/mcp_server_template.py` for a working MCP server structure with all 5 tool handlers

## Success Criteria

Implementation is complete when:
- [ ] All 5 tools registered and discoverable via MCP
- [ ] Each tool accepts user_id and enforces user isolation
- [ ] Database queries use SQLModel Task table
- [ ] Responses match spec format (status + data/error)
- [ ] UUID validation works for all IDs
- [ ] Error handling covers all edge cases
- [ ] Tools can be chained (create → complete → delete)
- [ ] No user can access another user's tasks
- [ ] Timestamps auto-update on modifications
- [ ] Server runs without errors
