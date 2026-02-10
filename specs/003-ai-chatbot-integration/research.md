# Research: MCP SDK Integration with FastAPI and Cohere

**Feature**: AI Chatbot Integration for Todo Management
**Date**: 2026-02-09
**Status**: Complete
**Related Documents**: [spec.md](spec.md), [plan.md](plan.md)

## Executive Summary

This research document provides concrete implementation patterns for integrating the Official MCP (Model Context Protocol) SDK with FastAPI and Cohere API for Phase III chatbot functionality. Key findings:

1. **MCP SDK is NOT installed** - Must be added to requirements.txt
2. **Cohere SDK v5.20.1 is installed** - ClientV2 supports tool calling
3. **MCP uses decorator-based tool registration** - Clean integration with FastAPI
4. **User context passing requires custom implementation** - MCP tools don't natively support user_id scoping
5. **Stateless architecture is achievable** - Store conversation history in database, pass to Cohere on each request

## Research Areas

### 1. Official MCP SDK Integration with FastAPI

#### Installation

**Finding**: MCP SDK is NOT currently installed in the project.

**Action Required**:
```bash
pip install "mcp[cli]"
# or
uv add "mcp[cli]"
```

Add to `requirements.txt`:
```
mcp[cli]>=1.0.0
```

#### MCP Server Setup Pattern

**Modern API (Recommended)**:
```python
from mcp.server.mcpserver import MCPServer

# Create MCP server instance
mcp = MCPServer("todo-mcp-server")

# Register tools using decorators
@mcp.tool()
def add_task(user_id: str, title: str, description: str = "") -> dict:
    """Create a new task for a specific user"""
    # Implementation here
    return {"status": "success", "data": {...}}

# Run the server
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```

**Key Features**:
- Decorator-based tool registration (`@mcp.tool()`)
- Automatic schema generation from type hints
- Support for sync and async functions
- Built-in JSON response formatting

#### Integration with FastAPI

**Challenge**: MCP SDK provides its own server runtime, but we need to integrate with existing FastAPI application.

**Solution**: Two approaches identified:

**Approach 1: Embedded MCP Server (Recommended for Phase III)**
```python
# backend/src/mcp/server.py
from mcp.server.mcpserver import MCPServer
from sqlmodel import Session
from ..database.session import get_session
from ..models.task import Task

# Create MCP server instance
mcp_server = MCPServer("todo-mcp-server")

# Tools can access database through dependency injection pattern
def get_db_session():
    """Helper to get database session for MCP tools"""
    with Session(engine) as session:
        return session

@mcp_server.tool()
async def add_task(user_id: str, title: str, description: str = "", completed: bool = False) -> dict:
    """Create a new task for a specific user"""
    session = get_db_session()
    # Implementation using existing Task model
    # ...
    return {"status": "success", "data": {...}}

# Export for use in agent
def get_mcp_tools():
    """Get list of MCP tools for Cohere agent"""
    return mcp_server.list_tools()
```

**Approach 2: Direct Tool Implementation (Alternative)**

Instead of running MCP as a separate server, implement tools as regular Python functions and manually convert them to Cohere tool format:

```python
# backend/src/mcp/tools/add_task.py
from sqlmodel import Session
from uuid import UUID
from ..models.task import Task

async def add_task_impl(session: Session, user_id: UUID, title: str, description: str = "") -> dict:
    """Implementation of add_task tool"""
    # Create task in database
    new_task = Task(
        user_id=user_id,
        title=title,
        description=description,
        completed=False
    )
    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    return {
        "status": "success",
        "data": {
            "id": str(new_task.id),
            "title": new_task.title,
            "description": new_task.description,
            "completed": new_task.completed
        }
    }

# Tool definition for Cohere
ADD_TASK_TOOL = {
    "type": "function",
    "function": {
        "name": "add_task",
        "description": "Create a new task for a specific user",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "User UUID"},
                "title": {"type": "string", "description": "Task title (1-255 chars)"},
                "description": {"type": "string", "description": "Task description (optional)"},
                "completed": {"type": "boolean", "description": "Completion status (default: false)"}
            },
            "required": ["user_id", "title"]
        }
    }
}
```

**Recommendation**: Use **Approach 2 (Direct Tool Implementation)** for Phase III because:
- Simpler integration with existing FastAPI app
- No need to run separate MCP server process
- Direct access to FastAPI dependencies (database session, auth)
- Easier to enforce user isolation
- MCP SDK can still be used for tool schema validation

### 2. Tool Registration and Discovery Patterns

#### MCP Tool Schema

MCP tools are defined with:
- **name**: Unique identifier (e.g., "add_task")
- **description**: What the tool does
- **inputSchema**: JSON Schema for parameters
- **Implementation**: Python function that executes the tool

**Example from template**:
```python
Tool(
    name="add_task",
    description="Create a new task for a specific user",
    inputSchema={
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "User UUID"},
            "title": {"type": "string", "description": "Task title (1-255 chars)"},
            "description": {"type": "string", "description": "Task description (optional)"},
            "completed": {"type": "boolean", "description": "Completion status (default: false)"}
        },
        "required": ["user_id", "title"]
    }
)
```

#### Converting MCP Tools to Cohere Format

Cohere uses `ToolV2` format:
```python
import cohere

cohere_tool = cohere.ToolV2(
    type="function",
    function={
        "name": "add_task",
        "description": "Create a new task for a specific user",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "User UUID"},
                "title": {"type": "string", "description": "Task title (1-255 chars)"},
                "description": {"type": "string", "description": "Task description (optional)"},
                "completed": {"type": "boolean", "description": "Completion status (default: false)"}
            },
            "required": ["user_id", "title"]
        }
    }
)
```

**Conversion Pattern**:
```python
def mcp_tool_to_cohere(mcp_tool: Tool) -> cohere.ToolV2:
    """Convert MCP tool definition to Cohere ToolV2 format"""
    return cohere.ToolV2(
        type="function",
        function={
            "name": mcp_tool.name,
            "description": mcp_tool.description,
            "parameters": mcp_tool.inputSchema
        }
    )
```

### 3. Tool Execution Patterns

#### MCP Tool Execution

MCP tools return structured responses:
```python
{
    "status": "success",
    "data": {
        "id": "uuid",
        "title": "Task title",
        ...
    }
}

# Or for errors:
{
    "status": "error",
    "error": "validation_error",
    "message": "Human-readable error message"
}
```

#### Cohere Tool Calling Flow

**Step 1: Initial Chat Request with Tools**
```python
import cohere

co = cohere.ClientV2(api_key="your-api-key")

tools = [
    cohere.ToolV2(
        type="function",
        function={
            "name": "add_task",
            "description": "Create a new task",
            "parameters": {...}
        }
    ),
    # ... other tools
]

response = co.chat(
    model="command-r-plus",
    messages=[
        {"role": "user", "content": "Add a task to buy groceries"}
    ],
    tools=tools
)
```

**Step 2: Handle Tool Calls in Response**
```python
if response.message.tool_calls:
    # Cohere decided to use tools
    for tool_call in response.message.tool_calls:
        tool_name = tool_call.function.name
        tool_args = tool_call.function.arguments

        # Execute the tool
        result = await execute_tool(tool_name, tool_args)

        # Store tool call and result for next turn
        tool_results.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)
        })
```

**Step 3: Continue Conversation with Tool Results**
```python
# Send tool results back to Cohere
response = co.chat(
    model="command-r-plus",
    messages=[
        {"role": "user", "content": "Add a task to buy groceries"},
        {"role": "assistant", "tool_calls": response.message.tool_calls},
        *tool_results  # Tool results from step 2
    ],
    tools=tools
)

# Now response.message.content contains the final answer
print(response.message.content[0].text)
# "I've added 'buy groceries' to your task list."
```

#### Complete Tool Execution Pattern

```python
# backend/src/agent/tool_executor.py
from typing import Dict, Any
from sqlmodel import Session
from uuid import UUID
import json

class ToolExecutor:
    """Executes MCP tools with user context"""

    def __init__(self, session: Session, user_id: UUID):
        self.session = session
        self.user_id = user_id
        self.tools = {
            "add_task": self._add_task,
            "list_tasks": self._list_tasks,
            "complete_task": self._complete_task,
            "delete_task": self._delete_task,
            "update_task": self._update_task,
        }

    async def execute(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool with user context"""
        if tool_name not in self.tools:
            return {
                "status": "error",
                "error": "unknown_tool",
                "message": f"Tool '{tool_name}' not found"
            }

        # Inject user_id into arguments
        arguments["user_id"] = str(self.user_id)

        try:
            result = await self.tools[tool_name](**arguments)
            return result
        except Exception as e:
            return {
                "status": "error",
                "error": "execution_error",
                "message": str(e)
            }

    async def _add_task(self, user_id: str, title: str, description: str = "", completed: bool = False) -> Dict[str, Any]:
        """Implementation of add_task tool"""
        # Validate user_id matches
        if str(self.user_id) != user_id:
            return {
                "status": "error",
                "error": "permission_denied",
                "message": "User ID mismatch"
            }

        # Create task using existing logic
        from ..models.task import Task
        new_task = Task(
            user_id=self.user_id,
            title=title,
            description=description,
            completed=completed
        )
        self.session.add(new_task)
        self.session.commit()
        self.session.refresh(new_task)

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

    # ... other tool implementations
```

### 4. User Context Passing (user_id)

#### Challenge

MCP tools don't have built-in support for user context. Every tool must explicitly accept and validate `user_id`.

#### Solution: Dependency Injection Pattern

**Pattern 1: Tool Executor with User Context (Recommended)**

```python
# In chat endpoint
@router.post("/chat")
async def chat_endpoint(
    message: str,
    current_user_id: UUID = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Create tool executor with user context
    tool_executor = ToolExecutor(session, current_user_id)

    # Create agent with tool executor
    agent = TodoChatAgent(cohere_client, tool_executor)

    # Process message
    response = await agent.chat(message)
    return response
```

**Pattern 2: Middleware Injection**

```python
# Alternative: Use FastAPI dependency to inject user_id into tool calls
class UserContextMiddleware:
    def __init__(self, user_id: UUID):
        self.user_id = user_id

    def wrap_tool(self, tool_func):
        async def wrapped(**kwargs):
            # Automatically inject user_id
            kwargs["user_id"] = str(self.user_id)
            return await tool_func(**kwargs)
        return wrapped
```

#### User Isolation Enforcement

**Critical Requirements**:
1. Every tool MUST accept `user_id` parameter
2. Every database query MUST filter by `user_id`
3. Validate `user_id` matches authenticated user
4. Never trust `user_id` from tool arguments alone

**Example**:
```python
async def list_tasks(user_id: str, completed: bool = None) -> Dict[str, Any]:
    """List tasks for a specific user"""
    # Validate user_id format
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        return {"status": "error", "error": "invalid_user_id", "message": "Invalid UUID format"}

    # Query with user_id filter (CRITICAL for isolation)
    statement = select(Task).where(Task.user_id == user_uuid)
    if completed is not None:
        statement = statement.where(Task.completed == completed)

    tasks = session.exec(statement).all()

    return {
        "status": "success",
        "data": {
            "tasks": [task.dict() for task in tasks],
            "count": len(tasks)
        }
    }
```

### 5. Integration with Cohere Agent

#### Cohere ClientV2 Setup

```python
# backend/src/agent/cohere_client.py
import cohere
from ..config.settings import get_settings

settings = get_settings()

def get_cohere_client() -> cohere.ClientV2:
    """Get configured Cohere client"""
    return cohere.ClientV2(api_key=settings.cohere_api_key)
```

#### TodoChatAgent Implementation

```python
# backend/src/agent/todo_agent.py
import cohere
from typing import List, Dict, Any
from uuid import UUID
import json

class TodoChatAgent:
    """Conversational agent for todo management using Cohere"""

    def __init__(self, cohere_client: cohere.ClientV2, tool_executor: ToolExecutor):
        self.client = cohere_client
        self.tool_executor = tool_executor
        self.tools = self._get_tool_definitions()
        self.system_prompt = self._get_system_prompt()

    def _get_system_prompt(self) -> str:
        """Get system prompt for agent behavior"""
        return """You are a helpful task management assistant. You help users manage their todo list through natural conversation.

Your capabilities:
- Add new tasks
- List tasks (all, pending, or completed)
- Mark tasks as complete or incomplete
- Delete tasks
- Update task details

Guidelines:
- Be friendly and conversational
- Confirm actions clearly (e.g., "I've added 'buy milk' to your list")
- Ask for clarification when commands are ambiguous
- Never hallucinate or invent task data - always use the tools to get real data
- When listing tasks, format them clearly
- If a task operation fails, explain why in a helpful way

Always use the provided tools to interact with the task database. Never make up task information."""

    def _get_tool_definitions(self) -> List[cohere.ToolV2]:
        """Get Cohere tool definitions"""
        return [
            cohere.ToolV2(
                type="function",
                function={
                    "name": "add_task",
                    "description": "Create a new task for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "Task title (1-255 chars)"},
                            "description": {"type": "string", "description": "Task description (optional)"},
                            "completed": {"type": "boolean", "description": "Completion status (default: false)"}
                        },
                        "required": ["title"]
                    }
                }
            ),
            cohere.ToolV2(
                type="function",
                function={
                    "name": "list_tasks",
                    "description": "Retrieve all tasks for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "completed": {"type": "boolean", "description": "Filter by completion status (optional)"}
                        }
                    }
                }
            ),
            # ... other tools
        ]

    async def chat(self, message: str, conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """Process a chat message and return response"""
        # Build messages array
        messages = []

        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)

        # Add current user message
        messages.append({"role": "user", "content": message})

        # Initial chat request
        response = self.client.chat(
            model="command-r-plus",
            messages=messages,
            tools=self.tools,
            preamble=self.system_prompt
        )

        # Handle tool calls
        if response.message.tool_calls:
            tool_results = []

            for tool_call in response.message.tool_calls:
                # Execute tool
                result = await self.tool_executor.execute(
                    tool_call.function.name,
                    tool_call.function.arguments
                )

                # Add tool result
                tool_results.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })

            # Continue conversation with tool results
            messages.append({
                "role": "assistant",
                "tool_calls": response.message.tool_calls
            })
            messages.extend(tool_results)

            # Get final response
            response = self.client.chat(
                model="command-r-plus",
                messages=messages,
                tools=self.tools,
                preamble=self.system_prompt
            )

        # Extract response text
        response_text = response.message.content[0].text if response.message.content else "I'm sorry, I couldn't process that request."

        return {
            "response": response_text,
            "tool_calls": [
                {
                    "tool": tc.function.name,
                    "arguments": tc.function.arguments
                }
                for tc in (response.message.tool_calls or [])
            ]
        }
```

### 6. Stateless Chat Endpoint Design

#### Chat Endpoint Implementation

```python
# backend/src/api/chat.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from uuid import UUID
from typing import Optional
from pydantic import BaseModel

from ..auth.jwt import get_current_user
from ..database.session import get_session
from ..agent.todo_agent import TodoChatAgent
from ..agent.tool_executor import ToolExecutor
from ..agent.cohere_client import get_cohere_client
from ..services.conversation import ConversationService

router = APIRouter(tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    tool_calls: list
    timestamp: str

@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    current_user_id: UUID = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Stateless chat endpoint for todo management.

    - Validates JWT and user_id
    - Loads conversation history from database
    - Processes message with Cohere agent
    - Persists conversation to database
    - Returns response
    """
    # Validate user_id matches authenticated user
    if str(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's chat"
        )

    # Initialize services
    conversation_service = ConversationService(session)
    tool_executor = ToolExecutor(session, current_user_id)
    cohere_client = get_cohere_client()
    agent = TodoChatAgent(cohere_client, tool_executor)

    # Load or create conversation
    if request.conversation_id:
        conversation = conversation_service.get_conversation(
            UUID(request.conversation_id),
            current_user_id
        )
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        conversation_history = conversation_service.get_messages(conversation.id)
    else:
        conversation = conversation_service.create_conversation(current_user_id)
        conversation_history = []

    # Save user message
    conversation_service.add_message(
        conversation.id,
        role="user",
        content=request.message
    )

    # Process with agent
    response = await agent.chat(request.message, conversation_history)

    # Save assistant response
    conversation_service.add_message(
        conversation.id,
        role="assistant",
        content=response["response"],
        tool_calls=response.get("tool_calls")
    )

    # Return response
    from datetime import datetime
    return ChatResponse(
        conversation_id=str(conversation.id),
        response=response["response"],
        tool_calls=response.get("tool_calls", []),
        timestamp=datetime.utcnow().isoformat()
    )
```

### 7. Error Handling Patterns

#### Tool Execution Errors

```python
def handle_tool_error(error: Exception, tool_name: str) -> Dict[str, Any]:
    """Convert exceptions to structured error responses"""
    if isinstance(error, ValueError):
        return {
            "status": "error",
            "error": "validation_error",
            "message": str(error)
        }
    elif isinstance(error, PermissionError):
        return {
            "status": "error",
            "error": "permission_denied",
            "message": "Access denied"
        }
    else:
        return {
            "status": "error",
            "error": "internal_error",
            "message": f"Failed to execute {tool_name}"
        }
```

#### Cohere API Errors

```python
try:
    response = cohere_client.chat(...)
except cohere.CohereAPIError as e:
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="AI service temporarily unavailable"
    )
except cohere.CohereConnectionError as e:
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Could not connect to AI service"
    )
```

## Implementation Recommendations

### Phase III Architecture

```
FastAPI Application
├── Chat Endpoint (/api/{user_id}/chat)
│   ├── JWT Authentication
│   ├── Load Conversation History
│   └── Return Response
│
├── TodoChatAgent (Cohere Integration)
│   ├── System Prompt
│   ├── Tool Definitions (Cohere format)
│   ├── Multi-turn Conversation Handling
│   └── Response Generation
│
├── ToolExecutor (User-scoped)
│   ├── User Context (user_id)
│   ├── Database Session
│   ├── 5 Tool Implementations
│   └── User Isolation Enforcement
│
├── ConversationService
│   ├── Create/Load Conversation
│   ├── Add Messages
│   └── Get History
│
└── Database Models
    ├── Conversation (new)
    ├── Message (new)
    ├── Task (existing)
    └── User (existing)
```

### Key Implementation Steps

1. **Add MCP SDK to requirements** (optional - can implement tools directly)
2. **Implement 5 tool functions** with user_id scoping
3. **Create ToolExecutor class** with user context injection
4. **Implement TodoChatAgent** with Cohere ClientV2
5. **Create Conversation and Message models**
6. **Implement ConversationService** for persistence
7. **Create chat endpoint** with stateless design
8. **Add comprehensive error handling**
9. **Write unit and integration tests**

### Dependencies to Add

```txt
# requirements.txt additions
cohere>=5.20.0  # Already installed
mcp[cli]>=1.0.0  # Optional - for tool schema validation
```

### Environment Variables

```env
# .env additions
COHERE_API_KEY=your-cohere-api-key-here
```

## Conclusion

The research confirms that integrating MCP SDK with FastAPI and Cohere is feasible with the following approach:

1. **Direct Tool Implementation**: Implement tools as Python functions, convert to Cohere format
2. **User Context Injection**: Use ToolExecutor class to inject user_id into all tool calls
3. **Stateless Architecture**: Load conversation history from database on each request
4. **Cohere ClientV2**: Use native tool calling with multi-turn conversation support
5. **Error Handling**: Structured error responses at tool and API levels

This approach provides:
- Clean separation of concerns
- Strong user isolation
- Stateless, scalable architecture
- Integration with existing FastAPI patterns
- Comprehensive error handling

**Next Steps**: Proceed to Phase 1 (Design & Contracts) to create detailed data models and API contracts.
