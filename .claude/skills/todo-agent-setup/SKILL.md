---
name: todo-agent-setup
description: "Configure and initialize OpenAI Agents SDK agent (TodoChatAgent) connected to MCP task management tools. Use this skill when: (1) Setting up the TodoChatAgent for Phase III chatbot integration, (2) Connecting OpenAI Agents SDK to MCP server tools, (3) Configuring agent behavior and system prompts, (4) Implementing the agent runner with tool call support, (5) Integrating the agent with FastAPI chat endpoints. This skill provides agent behavior specifications, initialization templates, and integration patterns for creating a conversational AI agent that manages tasks through natural language."
---

# Todo Agent Setup Guide

Configure the OpenAI Agents SDK agent (TodoChatAgent) with MCP tool integration for Phase III.

## Core Components

### 1. Agent Identity
- **Name**: TodoChatAgent
- **Role**: Personal task management assistant
- **Model**: GPT-4 (or compatible)
- **Tools**: 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)

### 2. Key Features
- Natural language task interpretation
- Multi-tool orchestration in single turn
- User isolation enforcement
- Conversational and friendly responses
- Error handling with helpful suggestions

## Implementation Workflow

### Step 1: Review Agent Behavior Specification
Read `references/agent-behavior.md` to understand:
- Agent personality and conversational style
- Tool interpretation patterns
- Multi-tool chaining examples
- Error handling strategies
- System prompt template

### Step 2: Initialize Agent with MCP Connection
Use the template in `scripts/agent_template.py` as a starting point:

```python
from openai import OpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class TodoChatAgent:
    def __init__(self, mcp_server_path: str, model: str = "gpt-4"):
        self.model = model
        self.mcp_server_path = mcp_server_path
        self.client = OpenAI()
        self.tools = []

    async def initialize_mcp_tools(self):
        # Connect to MCP server and load tools
        pass
```

### Step 3: Configure System Prompt
Set the agent's behavior using the system prompt:

```python
SYSTEM_PROMPT = """You are TodoChatAgent, a helpful personal task management assistant.

You have access to these tools:
- add_task, list_tasks, complete_task, delete_task, update_task

Guidelines:
1. Be friendly, concise, and proactive
2. Interpret user intent flexibly
3. Chain multiple tools when needed
4. Confirm actions clearly
5. Handle errors gracefully
6. NEVER access other users' tasks
7. Extract user_id from conversation context
"""
```

### Step 4: Implement Tool Execution Loop
Support multi-tool calls in a single turn:

```python
async def run(self, user_id: str, message: str, conversation_history: list = None):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.append({"role": "user", "content": f"[user_id: {user_id}]\n{message}"})

    response = self.client.chat.completions.create(
        model=self.model,
        messages=messages,
        tools=self.tools,
        tool_choice="auto"
    )

    # Handle tool calls (loop for multi-tool scenarios)
    while response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            # Inject user_id into tool arguments
            tool_args["user_id"] = user_id
            # Execute via MCP
            result = await self.execute_tool(tool_name, tool_args)
            # Add result to messages

        # Get next response
        response = self.client.chat.completions.create(...)

    return response_message.content
```

### Step 5: Integrate with FastAPI Endpoint
Connect the agent to the `/api/{user_id}/chat` endpoint:

```python
@router.post("/api/{user_id}/chat")
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    current_user_id: str = Depends(get_current_user)
):
    # Validate user_id matches authenticated user
    if user_id != current_user_id:
        raise HTTPException(status_code=403)

    # Run agent
    response = await agent.run(
        user_id=user_id,
        message=request.message,
        conversation_history=request.conversation_history
    )

    return ChatResponse(response=response)
```

## Critical Requirements

### User Isolation
- **ALWAYS** inject `user_id` into tool arguments
- Extract `user_id` from endpoint path parameter
- Validate `user_id` matches authenticated user
- Never allow cross-user data access

### Tool Call Handling
- Support multiple tool calls in one turn
- Handle tool call loops (agent → tool → agent → tool)
- Pass tool results back to agent for next decision
- Format tool results as messages with `role: "tool"`

### MCP Integration
- Initialize MCP client session on startup
- Convert MCP tool schemas to OpenAI function format
- Execute tools via MCP `call_tool()` method
- Handle MCP connection errors gracefully

### Conversation Context
- Accept conversation history from frontend
- Maintain message order (system → history → user → assistant → tool)
- Include user_id context in user messages
- Return updated conversation to frontend

## Agent Behavior Patterns

### Natural Language Interpretation
```
"Add buy milk" → add_task(title="buy milk")
"What's on my list?" → list_tasks()
"Mark groceries as done" → list_tasks() + complete_task()
"Delete the milk task" → list_tasks() + delete_task()
```

### Multi-Tool Chaining
```
"Add X and mark it done" → add_task() + complete_task()
"Show tasks and delete the first" → list_tasks() + delete_task()
"Create three tasks: A, B, C" → add_task() × 3
```

### Error Recovery
```
Task not found → "I couldn't find that task. Here's your current list..."
Ambiguous reference → "I found 3 tasks. Which one did you mean?"
Invalid input → "Could you provide more details?"
```

## Quality Checklist

- [ ] Agent initialized with MCP server connection
- [ ] All 5 tools loaded and available to agent
- [ ] System prompt includes behavior guidelines
- [ ] Tool execution loop handles multi-tool calls
- [ ] user_id injected into every tool call
- [ ] Conversation history maintained correctly
- [ ] Agent responds in friendly, conversational tone
- [ ] Agent interprets natural language flexibly
- [ ] Agent chains tools when appropriate
- [ ] Agent handles errors gracefully
- [ ] Agent never accesses other users' data
- [ ] Integration with FastAPI endpoint complete
- [ ] JWT authentication enforced at endpoint
- [ ] Conversation persistence implemented (if required)

## Testing Strategy

### Unit Tests
- Test agent initialization
- Test MCP tool loading
- Test tool call formatting
- Test user_id injection

### Integration Tests
- Test single tool calls
- Test multi-tool chains
- Test conversation flow
- Test error handling

### End-to-End Tests
- Test via FastAPI endpoint
- Test with real user authentication
- Test conversation persistence
- Test concurrent users

## Common Patterns

### Agent Initialization (Startup)
```python
agent = TodoChatAgent(mcp_server_path="backend/mcp_server.py")
await agent.initialize_mcp_tools()
```

### Single Message Processing
```python
response = await agent.run(
    user_id="123e4567-...",
    message="Add buy groceries"
)
```

### With Conversation History
```python
response = await agent.run(
    user_id="123e4567-...",
    message="Mark it as done",
    conversation_history=[
        {"role": "user", "content": "Add buy groceries"},
        {"role": "assistant", "content": "I've added 'buy groceries' to your list."}
    ]
)
```

## Debugging Tips

### Agent Not Calling Tools
- Verify tools loaded: `print(agent.tools)`
- Check system prompt includes tool descriptions
- Ensure `tool_choice="auto"` in API call

### Wrong User Data Accessed
- Confirm user_id injection in tool arguments
- Verify endpoint validates user_id
- Check MCP tools enforce user_id filtering

### Tool Calls Fail
- Check MCP server is running
- Verify tool arguments match schema
- Log tool execution results

### Multi-Tool Chains Don't Work
- Ensure tool call loop continues while `tool_calls` exist
- Verify tool results added to messages
- Check agent receives tool results before next call

## Reference Materials

- **Agent Behavior Specification**: See `references/agent-behavior.md` for complete behavioral guidelines, conversational patterns, system prompt template, and example interactions
- **Implementation Template**: See `scripts/agent_template.py` for working agent class with MCP integration, tool execution loop, and FastAPI endpoint example

## Success Criteria

Implementation is complete when:
- [ ] Agent initializes and connects to MCP server
- [ ] All 5 tools discoverable by agent
- [ ] Agent processes natural language requests correctly
- [ ] Agent chains multiple tools in single turn
- [ ] Agent enforces user isolation (user_id in all calls)
- [ ] Agent responds conversationally and confirms actions
- [ ] Agent handles errors gracefully with suggestions
- [ ] Integration with FastAPI endpoint works end-to-end
- [ ] JWT authentication enforced
- [ ] Conversation history maintained (if required)
- [ ] No cross-user data leakage
