# Model Context Protocol (MCP) Specification

## Overview

Model Context Protocol (MCP) is a standard for enabling AI models to interact with external systems and tools in a standardized way. It allows AI agents to call external functions, access resources, and perform operations beyond their core reasoning capabilities.

## Core Concepts

### Stateless Server Design
MCP servers should be stateless, meaning each request contains all necessary information for processing. This allows for horizontal scaling and fault tolerance.

### Resource Discovery
MCP servers expose available resources and tools through discovery mechanisms, allowing clients to understand what capabilities are available.

### Standardized Interfaces
MCP defines standard interfaces for common operations like listing resources, reading data, and performing actions.

## MCP Server Implementation

### Basic Server Structure
```python
from mcp.server import Server
from mcp.types import DiscoveryResult, TextContent, Prompt
import asyncio

server = Server("my-mcp-server")

@server.discovery()
def handle_discovery() -> DiscoveryResult:
    """Handle discovery requests to advertise server capabilities."""
    return DiscoveryResult(
        prompts=[
            Prompt(
                name="task_operations",
                description="Operations for managing tasks",
                arguments=[
                    # Define expected arguments
                ]
            )
        ],
        resources=[]  # Define available resources
    )

@server.call("prompts/list_tasks")
async def handle_list_tasks(context, arguments):
    """Handle list_tasks operation."""
    # Implementation for listing tasks
    tasks = get_all_tasks()
    return {
        "result": tasks
    }

@server.call("prompts/add_task")
async def handle_add_task(context, arguments):
    """Handle add_task operation."""
    task_name = arguments.get("name")
    task_description = arguments.get("description", "")
    new_task = create_task(name=task_name, description=task_description)
    return {
        "result": {"id": new_task.id, "name": new_task.name}
    }

if __name__ == "__main__":
    import sys
    from mcp.server.stdio import stdio_server
    with stdio_server(sys.stdin, sys.stdout, server) as server:
        server.run()
```

## MCP Client Integration

### Connecting to MCP Server
```python
from mcp.client import Client
from mcp.config import Config

async def connect_to_mcp_server():
    config = Config.from_dict({
        "servers": {
            "task_server": {
                "command": ["python", "task_server.py"]
            }
        }
    })

    async with Client(config) as client:
        # Discover available resources
        discovery_result = await client.discover()

        # Call specific operations
        result = await client.call_tool("task_server", "prompts/add_task", {
            "name": "Sample task",
            "description": "A sample task description"
        })

        return result
```

## Error Handling in MCP

### Standard Error Responses
MCP servers should return standardized error responses:

```python
from mcp.types import ErrorResponse

def handle_error(error_msg, code="INTERNAL_ERROR"):
    """Standard error response format."""
    return ErrorResponse(
        code=code,
        message=error_msg
    )
```

### Common Error Types
- `INVALID_ARGUMENT`: Arguments provided to the operation are invalid
- `RESOURCE_NOT_FOUND`: Requested resource does not exist
- `PERMISSION_DENIED`: Insufficient permissions to perform operation
- `INTERNAL_ERROR`: Unexpected internal server error

## Task Operations Implementation

### Task Data Model
```python
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Task:
    id: str
    name: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
```

### Task Operation Handlers
```python
from typing import List
import uuid

TASK_STORAGE = {}  # In production, use persistent storage

async def get_all_tasks() -> List[Task]:
    """Retrieve all tasks."""
    return list(TASK_STORAGE.values())

async def create_task(name: str, description: str = "") -> Task:
    """Create a new task."""
    task_id = str(uuid.uuid4())
    task = Task(
        id=task_id,
        name=name,
        description=description
    )
    TASK_STORAGE[task_id] = task
    return task

async def complete_task(task_id: str) -> bool:
    """Mark a task as completed."""
    if task_id in TASK_STORAGE:
        TASK_STORAGE[task_id].completed = True
        return True
    return False

async def delete_task(task_id: str) -> bool:
    """Delete a task."""
    if task_id in TASK_STORAGE:
        del TASK_STORAGE[task_id]
        return True
    return False
```

## MCP Configuration

### Configuration File Format
```json
{
  "mcp": {
    "version": "1.0.0",
    "servers": {
      "task_server": {
        "command": ["python", "task_server.py"],
        "env": {
          "TASK_DB_PATH": "./tasks.db"
        }
      }
    }
  }
}
```

## Security Considerations

### Authentication
MCP servers may require authentication mechanisms for sensitive operations:

```python
# Example of authentication middleware
async def authenticate_request(context):
    """Authenticate incoming requests."""
    auth_header = context.get("authorization")
    if not auth_header or not validate_token(auth_header):
        raise PermissionError("Invalid or missing authentication token")
```

### Input Validation
Always validate inputs to prevent injection attacks:

```python
import re

def validate_task_name(name: str) -> bool:
    """Validate task name format."""
    if not name or len(name) > 100:
        return False
    # Allow alphanumeric, spaces, hyphens, and underscores
    return bool(re.match(r'^[a-zA-Z0-9 _\-]+$', name))
```