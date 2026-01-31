#!/usr/bin/env python3
"""
Script to initialize a new AI MCP project with OpenAI Agents and Chatkit integration
"""

import os
import sys
from pathlib import Path
import json

def create_project_structure(project_name):
    """Create the basic project structure"""
    base_path = Path(project_name)
    base_path.mkdir(exist_ok=True)

    # Create directories
    (base_path / "backend").mkdir(exist_ok=True)
    (base_path / "backend" / "mcp_server").mkdir(exist_ok=True)
    (base_path / "backend" / "agents").mkdir(exist_ok=True)
    (base_path / "backend" / "api").mkdir(exist_ok=True)
    (base_path / "frontend").mkdir(exist_ok=True)
    (base_path / "frontend" / "components").mkdir(exist_ok=True)
    (base_path / "frontend" / "pages").mkdir(exist_ok=True)
    (base_path / "tests").mkdir(exist_ok=True)
    (base_path / "docs").mkdir(exist_ok=True)

    return base_path

def create_requirements(base_path):
    """Create requirements.txt"""
    requirements_content = '''openai>=1.0.0
mcp-sdk>=1.0.0
fastapi>=0.104.1
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
python-dotenv>=1.0.0
asyncio>=3.4.3
requests>=2.31.0
websockets>=12.0
sse-starlette>=1.6.5
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
sqlalchemy>=2.0.23
asyncpg>=0.29.0
redis>=5.0.1
'''

    with open(base_path / "requirements.txt", "w") as f:
        f.write(requirements_content)

def create_backend_main(base_path):
    """Create the main backend application"""
    main_content = '''from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from typing import Optional
import os

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AI MCP Task Manager",
    description="An AI-powered task management system with MCP integration",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "AI MCP Task Manager API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Include API routes
from backend.api.chat_routes import router as chat_router
from backend.api.task_routes import router as task_router

app.include_router(chat_router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(task_router, prefix="/api/v1/tasks", tags=["tasks"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
'''

    with open(base_path / "backend" / "main.py", "w") as f:
        f.write(main_content)

def create_mcp_server(base_path):
    """Create MCP server implementation"""
    mcp_content = '''from mcp.server import Server
from mcp.types import DiscoveryResult, TextContent, Prompt, Tool
from typing import List, Dict, Any
import asyncio
import uuid
from datetime import datetime

# Simple in-memory task storage (use database in production)
TASK_STORAGE = {}

server = Server("ai-task-mcp-server")

@server.discovery()
def handle_discovery() -> DiscoveryResult:
    """Handle discovery requests to advertise server capabilities."""
    return DiscoveryResult(
        tools=[
            Tool(
                name="add_task",
                description="Add a new task to the task list",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "The name of the task"},
                        "description": {"type": "string", "description": "Detailed description of the task"}
                    },
                    "required": ["name"]
                }
            ),
            Tool(
                name="list_tasks",
                description="List all available tasks",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            ),
            Tool(
                name="complete_task",
                description="Mark a task as completed",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "The ID of the task to complete"}
                    },
                    "required": ["task_id"]
                }
            ),
            Tool(
                name="delete_task",
                description="Delete a task from the task list",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "The ID of the task to delete"}
                    },
                    "required": ["task_id"]
                }
            )
        ]
    )

@server.call("tools/add_task")
async def handle_add_task(context, arguments) -> Dict[str, Any]:
    """Handle add_task operation."""
    task_name = arguments.get("name")
    task_description = arguments.get("description", "")

    # Validate input
    if not task_name or len(task_name.strip()) == 0:
        raise ValueError("Task name is required")

    # Create new task
    task_id = str(uuid.uuid4())
    task = {
        "id": task_id,
        "name": task_name.strip(),
        "description": task_description.strip(),
        "completed": False,
        "created_at": datetime.now().isoformat()
    }

    TASK_STORAGE[task_id] = task

    return {
        "result": {
            "id": task_id,
            "name": task_name,
            "message": f"Task '{task_name}' added successfully"
        }
    }

@server.call("tools/list_tasks")
async def handle_list_tasks(context, arguments) -> Dict[str, Any]:
    """Handle list_tasks operation."""
    tasks = list(TASK_STORAGE.values())
    return {
        "result": {
            "tasks": tasks,
            "count": len(tasks)
        }
    }

@server.call("tools/complete_task")
async def handle_complete_task(context, arguments) -> Dict[str, Any]:
    """Handle complete_task operation."""
    task_id = arguments.get("task_id")

    if not task_id or task_id not in TASK_STORAGE:
        return {
            "result": {
                "success": False,
                "message": f"Task with ID {task_id} not found"
            }
        }

    TASK_STORAGE[task_id]["completed"] = True
    TASK_STORAGE[task_id]["completed_at"] = datetime.now().isoformat()

    return {
        "result": {
            "success": True,
            "message": f"Task with ID {task_id} marked as completed"
        }
    }

@server.call("tools/delete_task")
async def handle_delete_task(context, arguments) -> Dict[str, Any]:
    """Handle delete_task operation."""
    task_id = arguments.get("task_id")

    if not task_id or task_id not in TASK_STORAGE:
        return {
            "result": {
                "success": False,
                "message": f"Task with ID {task_id} not found"
            }
        }

    del TASK_STORAGE[task_id]

    return {
        "result": {
            "success": True,
            "message": f"Task with ID {task_id} deleted successfully"
        }
    }

def run_server():
    """Run the MCP server."""
    import sys
    from mcp.server.stdio import stdio_server

    with stdio_server(sys.stdin, sys.stdout, server) as server:
        server.run()

if __name__ == "__main__":
    run_server()
'''

    with open(base_path / "backend" / "mcp_server" / "server.py", "w") as f:
        f.write(mcp_content)

def create_openai_agent(base_path):
    """Create OpenAI agent implementation"""
    agent_content = '''import openai
from typing import List, Dict, Any
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TaskAgent:
    def __init__(self, api_key: str = None, model: str = "gpt-4-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")

        self.client = openai.OpenAI(api_key=self.api_key)
        self.model = model
        self.tools = self._define_tools()

    def _define_tools(self) -> List[Dict[str, Any]]:
        """Define available tools for the agent."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Add a new task to the task list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The name of the task"
                            },
                            "description": {
                                "type": "string",
                                "description": "Detailed description of the task"
                            }
                        },
                        "required": ["name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List all available tasks",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as completed",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "string",
                                "description": "The ID of the task to complete"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task from the task list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "string",
                                "description": "The ID of the task to delete"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            }
        ]

    async def process_message(self, message: str, user_context: Dict[str, Any] = None) -> str:
        """Process a user message and return a response."""
        messages = [
            {
                "role": "system",
                "content": "You are a helpful task management assistant. Use the available tools to manage tasks for the user. Be concise and helpful."
            },
            {
                "role": "user",
                "content": message
            }
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.tools,
            tool_choice="auto"
        )

        # Process the response
        return self._process_response(response)

    def _process_response(self, response) -> str:
        """Process the OpenAI response."""
        message = response.choices[0].message

        # If there are tool calls, execute them
        if message.tool_calls:
            # In a real implementation, you would execute the tools and get results
            # For this example, we'll return a message indicating tool calls were made
            tool_calls = []
            for tool_call in message.tool_calls:
                tool_calls.append({
                    "name": tool_call.function.name,
                    "arguments": json.loads(tool_call.function.arguments)
                })

            return f"I've processed your request using these tools: {[call['name'] for call in tool_calls]}"
        else:
            # Return the assistant's direct response
            return message.content or "I processed your request."

    def get_available_tools(self) -> List[str]:
        """Get list of available tools."""
        return [tool["function"]["name"] for tool in self.tools]
'''

    with open(base_path / "backend" / "agents" / "task_agent.py", "w") as f:
        f.write(agent_content)

def create_chat_routes(base_path):
    """Create chat API routes"""
    chat_routes_content = '''from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict, Any
from backend.agents.task_agent import TaskAgent
import os

router = APIRouter()

class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: Optional[str] = None
    tool_used: Optional[str] = None

@router.post("/message", response_model=ChatResponse)
async def chat_message(chat_message: ChatMessage):
    """Handle a chat message and return AI response."""
    try:
        # Initialize the agent
        agent = TaskAgent()

        # Process the message
        response = await agent.process_message(chat_message.message)

        return ChatResponse(
            response=response,
            session_id=chat_message.session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@router.get("/capabilities")
async def get_capabilities():
    """Get the capabilities of the chat system."""
    try:
        agent = TaskAgent()
        tools = agent.get_available_tools()

        return {
            "capabilities": [
                "Natural language task management",
                "Task creation, listing, completion, and deletion",
                "Context-aware responses"
            ],
            "available_tools": tools,
            "model": os.getenv("OPENAI_MODEL", "gpt-4-turbo")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting capabilities: {str(e)}")
'''

    with open(base_path / "backend" / "api" / "chat_routes.py", "w") as f:
        f.write(chat_routes_content)

def create_task_routes(base_path):
    """Create task API routes"""
    task_routes_content = '''from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime

router = APIRouter()

# Simple in-memory storage (use database in production)
TASKS = {}

class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskResponse(TaskBase):
    id: str
    completed: bool
    created_at: str
    completed_at: Optional[str] = None

@router.get("/", response_model=List[TaskResponse])
async def get_tasks():
    """Get all tasks."""
    return [TaskResponse(**task) for task in TASKS.values()]

@router.post("/", response_model=TaskResponse)
async def create_task(task: TaskCreate):
    """Create a new task."""
    task_id = str(uuid.uuid4())
    new_task = {
        "id": task_id,
        "name": task.name,
        "description": task.description or "",
        "completed": False,
        "created_at": datetime.now().isoformat()
    }

    TASKS[task_id] = new_task
    return TaskResponse(**new_task)

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    """Get a specific task."""
    if task_id not in TASKS:
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskResponse(**TASKS[task_id])

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, task_update: TaskUpdate):
    """Update a specific task."""
    if task_id not in TASKS:
        raise HTTPException(status_code=404, detail="Task not found")

    task = TASKS[task_id]

    # Update fields if provided
    if task_update.name is not None:
        task["name"] = task_update.name
    if task_update.description is not None:
        task["description"] = task_update.description
    if task_update.completed is not None:
        task["completed"] = task_update.completed
        if task_update.completed and not task.get("completed_at"):
            task["completed_at"] = datetime.now().isoformat()

    return TaskResponse(**task)

@router.delete("/{task_id}")
async def delete_task(task_id: str):
    """Delete a specific task."""
    if task_id not in TASKS:
        raise HTTPException(status_code=404, detail="Task not found")

    del TASKS[task_id]
    return {"message": "Task deleted successfully"}
'''

    with open(base_path / "backend" / "api" / "task_routes.py", "w") as f:
        f.write(task_routes_content)

def create_frontend_package_json(base_path):
    """Create frontend package.json"""
    package_json = {
        "name": "ai-mcp-frontend",
        "version": "1.0.0",
        "private": True,
        "scripts": {
            "dev": "next dev",
            "build": "next build",
            "start": "next start",
            "lint": "next lint"
        },
        "dependencies": {
            "next": "^14.0.0",
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "@types/node": "^20.10.0",
            "@types/react": "^18.2.38",
            "@types/react-dom": "^18.2.17",
            "typescript": "^5.3.0",
            "axios": "^1.6.0",
            "openai": "^4.20.0"
        },
        "devDependencies": {
            "@types/axios": "^0.14.0"
        }
    }

    with open(base_path / "frontend" / "package.json", "w") as f:
        json.dump(package_json, f, indent=2)

def create_env_example(base_path):
    """Create .env.example file"""
    env_content = '''# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4-turbo

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Database (if using persistent storage)
DATABASE_URL=sqlite:///./tasks.db

# JWT Secret for authentication
JWT_SECRET=your-super-secret-jwt-key-here
'''

    with open(base_path / ".env.example", "w") as f:
        f.write(env_content)

def create_readme(base_path):
    """Create README.md"""
    readme_content = f'''# {base_path.name}

An AI-powered task management system with Model Context Protocol (MCP) integration.

## Overview

This project combines:
- OpenAI Agents SDK for conversational AI
- Model Context Protocol (MCP) for extensible tool integration
- Task management capabilities through natural language

## Features

- Natural language task management
- MCP server for extensible tools
- OpenAI-powered conversational interface
- RESTful API for task operations
- Real-time chat interface

## Setup

1. Clone the repository:
```bash
git clone {base_path.name}
cd {base_path.name}
```

2. Install backend dependencies:
```bash
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd frontend
npm install
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run the backend server:
```bash
cd backend
python main.py
```

## Architecture

- **Backend**: FastAPI server with MCP integration and OpenAI agents
- **MCP Server**: Stateless server for task operations
- **Agents**: OpenAI agent with task management tools
- **Frontend**: React-based chat interface (to be implemented)

## API Endpoints

### Chat
- `POST /api/v1/chat/message` - Process chat messages
- `GET /api/v1/chat/capabilities` - Get chat system capabilities

### Tasks
- `GET /api/v1/tasks/` - Get all tasks
- `POST /api/v1/tasks/` - Create a new task
- `GET /api/v1/tasks/{id}` - Get specific task
- `PUT /api/v1/tasks/{id}` - Update a task
- `DELETE /api/v1/tasks/{id}` - Delete a task

## MCP Server

The MCP server implements the following tools:
- `add_task` - Add a new task
- `list_tasks` - List all tasks
- `complete_task` - Mark a task as completed
- `delete_task` - Delete a task

## Development

To run the development server:

Backend:
```bash
cd backend
python main.py
```

Frontend (coming soon):
```bash
cd frontend
npm run dev
```

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_MODEL`: Model to use (default: gpt-4-turbo)
- `HOST`: Host address (default: 0.0.0.0)
- `PORT`: Port number (default: 8000)
- `JWT_SECRET`: Secret key for JWT authentication
'''

    with open(base_path / "README.md", "w") as f:
        f.write(readme_content)

def main():
    if len(sys.argv) != 2:
        print("Usage: python init_ai_mcp_project.py <project_name>")
        sys.exit(1)

    project_name = sys.argv[1]

    print(f"Creating new AI MCP project: {project_name}")

    base_path = create_project_structure(project_name)
    create_requirements(base_path)
    create_backend_main(base_path)
    create_mcp_server(base_path)
    create_openai_agent(base_path)
    create_chat_routes(base_path)
    create_task_routes(base_path)
    create_frontend_package_json(base_path)
    create_env_example(base_path)
    create_readme(base_path)

    print(f"Project {project_name} created successfully!")
    print(f"Next steps:")
    print(f"1. cd {project_name}")
    print(f"2. Copy .env.example to .env and update configuration")
    print(f"3. Install dependencies with 'pip install -r requirements.txt'")
    print(f"4. Run the backend with 'cd backend && python main.py'")

if __name__ == "__main__":
    main()