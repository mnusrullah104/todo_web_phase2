"""TodoChatAgent for Phase III AI Chatbot Integration.

Conversational agent for todo management using Cohere API.
"""
import cohere
from typing import List, Dict, Any, Optional
import json
import logging

from ..mcp.tool_executor import ToolExecutor
from ..mcp.tools import get_tool_definitions

logger = logging.getLogger(__name__)


class TodoChatAgent:
    """Conversational agent for todo management using Cohere.

    This agent interprets natural language commands and executes
    appropriate tools to manage tasks.
    """

    def __init__(self, cohere_client: cohere.ClientV2, tool_executor: ToolExecutor):
        """Initialize TodoChatAgent.

        Args:
            cohere_client: Configured Cohere ClientV2 instance
            tool_executor: ToolExecutor for executing tools with user context
        """
        self.client = cohere_client
        self.tool_executor = tool_executor
        self.tools = get_tool_definitions()
        self.system_prompt = self._get_system_prompt()

    def _get_system_prompt(self) -> str:
        """Get system prompt for agent behavior.

        Returns:
            System prompt string defining agent personality and guidelines
        """
        return """You are a helpful task management assistant. You help users manage their todo list and navigate the application through natural conversation.

Your capabilities:
- Add new tasks (e.g., "Add task: Buy groceries")
- List tasks (e.g., "Show my tasks", "What's on my list?")
- Mark tasks as complete or incomplete (e.g., "Complete task: Buy milk")
- Delete tasks (e.g., "Delete the groceries task")
- Update task details (e.g., "Update task: Change deadline")
- Navigate to pages (e.g., "Go to dashboard", "Open tasks page", "Take me to profile")

Available pages: dashboard, tasks, calendar, analytics, settings, evaluations

Guidelines:
- Be friendly and conversational
- Confirm actions clearly (e.g., "I've added 'buy milk' to your list")
- Ask for clarification when commands are ambiguous
- Never hallucinate or invent task data - always use the tools to get real data
- When listing tasks, format them clearly with numbers
- If a task operation fails, explain why in a helpful way
- When multiple tasks match a description, list them and ask which one the user means
- For navigation requests, use the navigate tool to provide the route

Always use the provided tools to interact with the task database and navigate. Never make up task information."""

    async def chat(
        self,
        message: str,
        conversation_history: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Process a chat message and return response.

        Args:
            message: User's message
            conversation_history: Optional list of previous messages

        Returns:
            Dict containing response text and tool calls
        """
        # Build messages array
        messages = []

        # Add conversation history if provided
        if conversation_history:
            for msg in conversation_history:
                messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })

        # Add current user message
        messages.append({"role": "user", "content": message})

        try:
            # Initial chat request with tools
            logger.info(f"Sending message to Cohere: {message[:100]}...")
            response = self.client.chat(
                model="command-r-08-2024",
                messages=messages,
                tools=self.tools
            )

            # Handle tool calls if present
            tool_calls_info = []
            if response.message.tool_calls:
                logger.info(f"Agent requested {len(response.message.tool_calls)} tool calls")
                tool_results = []

                for tool_call in response.message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = tool_call.function.arguments

                    # Parse arguments if they're a JSON string
                    if isinstance(tool_args, str):
                        tool_args = json.loads(tool_args)

                    logger.info(f"Executing tool: {tool_name}")

                    # Execute tool
                    result = await self.tool_executor.execute(tool_name, tool_args)

                    # Store tool call info for response
                    tool_calls_info.append({
                        "tool": tool_name,
                        "arguments": tool_args
                    })

                    # Add tool result for next turn
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

                logger.info("Getting final response from Cohere with tool results")
                response = self.client.chat(
                    model="command-r-08-2024",
                    messages=messages,
                    tools=self.tools
                )

            # Extract response text
            response_text = ""
            if response.message.content:
                if isinstance(response.message.content, list):
                    response_text = response.message.content[0].text if response.message.content else ""
                else:
                    response_text = str(response.message.content)

            if not response_text:
                response_text = "I'm sorry, I couldn't process that request."

            logger.info(f"Agent response: {response_text[:100]}...")

            return {
                "response": response_text,
                "tool_calls": tool_calls_info
            }

        except Exception as e:
            logger.error(f"Unexpected error in chat: {str(e)}", exc_info=True)
            return {
                "response": "I encountered an unexpected error. Please try again.",
                "tool_calls": [],
                "error": "unexpected_error"
            }
