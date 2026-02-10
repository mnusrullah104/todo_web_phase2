"""
OpenAI Agents SDK + MCP Tools Integration Template
Demonstrates how to initialize TodoChatAgent with MCP tool access
"""

from openai import OpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
from typing import Optional

# Initialize OpenAI client
client = OpenAI(api_key="your-api-key")

# System prompt for TodoChatAgent
SYSTEM_PROMPT = """You are TodoChatAgent, a helpful personal task management assistant. You help users manage their todo lists through natural conversation.

You have access to these tools:
- add_task: Create new tasks
- list_tasks: View tasks (optionally filter by completion status)
- complete_task: Mark tasks as complete or incomplete
- delete_task: Remove tasks permanently
- update_task: Modify task details

Guidelines:
1. Be friendly, concise, and proactive
2. Interpret user intent flexibly (e.g., "add X" or "create X" both mean add_task)
3. Chain multiple tools when needed (e.g., "add X and mark it done")
4. Confirm actions clearly (e.g., "I've added 'X' to your list")
5. Handle errors gracefully with helpful suggestions
6. NEVER access or mention other users' tasks
7. Extract user_id from the conversation context automatically

When listing tasks, format them clearly with numbers. When completing or deleting tasks, confirm the action. When users are ambiguous, ask for clarification.
"""


class TodoChatAgent:
    """
    OpenAI Agents SDK agent configured with MCP tools for task management
    """

    def __init__(self, mcp_server_path: str, model: str = "gpt-4"):
        """
        Initialize the agent with MCP tools

        Args:
            mcp_server_path: Path to the MCP server script
            model: OpenAI model to use (default: gpt-4)
        """
        self.model = model
        self.mcp_server_path = mcp_server_path
        self.client = OpenAI()
        self.mcp_session: Optional[ClientSession] = None
        self.tools = []

    async def initialize_mcp_tools(self):
        """
        Connect to MCP server and load available tools
        """
        # Configure MCP server parameters
        server_params = StdioServerParameters(
            command="python",
            args=[self.mcp_server_path],
            env=None
        )

        # Create MCP client session
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the session
                await session.initialize()

                # List available tools from MCP server
                tools_list = await session.list_tools()

                # Convert MCP tools to OpenAI function format
                self.tools = self._convert_mcp_tools_to_openai_format(tools_list.tools)

                print(f"Loaded {len(self.tools)} MCP tools: {[t['function']['name'] for t in self.tools]}")

                # Store session for tool execution
                self.mcp_session = session

    def _convert_mcp_tools_to_openai_format(self, mcp_tools):
        """
        Convert MCP tool definitions to OpenAI function calling format

        Args:
            mcp_tools: List of MCP Tool objects

        Returns:
            List of OpenAI function definitions
        """
        openai_tools = []

        for tool in mcp_tools:
            openai_tool = {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema
                }
            }
            openai_tools.append(openai_tool)

        return openai_tools

    async def execute_tool(self, tool_name: str, arguments: dict) -> str:
        """
        Execute an MCP tool and return the result

        Args:
            tool_name: Name of the tool to execute
            arguments: Tool arguments

        Returns:
            Tool execution result as string
        """
        if not self.mcp_session:
            raise RuntimeError("MCP session not initialized. Call initialize_mcp_tools() first.")

        # Call the tool via MCP
        result = await self.mcp_session.call_tool(tool_name, arguments)

        # Extract text content from result
        if result.content and len(result.content) > 0:
            return result.content[0].text

        return "Tool executed successfully"

    async def run(self, user_id: str, message: str, conversation_history: list = None) -> str:
        """
        Run the agent with a user message

        Args:
            user_id: User ID for tool calls (enforces user isolation)
            message: User's message
            conversation_history: Previous conversation messages (optional)

        Returns:
            Agent's response
        """
        # Build messages list
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)

        # Add current user message with user_id context
        messages.append({
            "role": "user",
            "content": f"[user_id: {user_id}]\n{message}"
        })

        # Initial API call with tools
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.tools,
            tool_choice="auto"
        )

        response_message = response.choices[0].message

        # Handle tool calls (may be multiple in one turn)
        while response_message.tool_calls:
            # Add assistant's response to messages
            messages.append(response_message)

            # Execute each tool call
            for tool_call in response_message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = eval(tool_call.function.arguments)  # Parse JSON arguments

                # Inject user_id into tool arguments
                tool_args["user_id"] = user_id

                # Execute tool via MCP
                tool_result = await self.execute_tool(tool_name, tool_args)

                # Add tool result to messages
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": tool_result
                })

            # Get next response from model
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )

            response_message = response.choices[0].message

        # Return final response
        return response_message.content


# Example usage
async def main():
    """
    Example: Initialize agent and process a user message
    """
    # Initialize agent
    agent = TodoChatAgent(
        mcp_server_path="path/to/mcp_server.py",
        model="gpt-4"
    )

    # Load MCP tools
    await agent.initialize_mcp_tools()

    # Process user message
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    message = "Add buy groceries and mark it as done"

    response = await agent.run(user_id, message)
    print(f"Agent: {response}")


# FastAPI endpoint integration example
"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel

router = APIRouter()

# Global agent instance (initialize on startup)
agent: TodoChatAgent = None

@router.on_event("startup")
async def startup_event():
    global agent
    agent = TodoChatAgent(mcp_server_path="backend/mcp_server.py")
    await agent.initialize_mcp_tools()

class ChatRequest(BaseModel):
    message: str
    conversation_history: list = []

class ChatResponse(BaseModel):
    response: str

@router.post("/api/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    current_user_id: str = Depends(get_current_user)
):
    # Validate user_id matches authenticated user
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    # Run agent
    response = await agent.run(
        user_id=user_id,
        message=request.message,
        conversation_history=request.conversation_history
    )

    return ChatResponse(response=response)
"""


if __name__ == "__main__":
    asyncio.run(main())
