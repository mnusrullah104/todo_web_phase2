"""Tool Executor for Phase III AI Chatbot Integration.

Executes MCP tools with user context injection and error handling.
"""
from typing import Dict, Any, Callable, Awaitable
from sqlmodel import Session
from uuid import UUID
import logging

logger = logging.getLogger(__name__)


class ToolExecutor:
    """Executes MCP tools with user context.

    This class manages tool registration and execution, automatically
    injecting user_id into all tool calls to enforce user isolation.
    """

    def __init__(self, session: Session, user_id: UUID):
        """Initialize ToolExecutor.

        Args:
            session: Database session for tool operations
            user_id: UUID of the authenticated user
        """
        self.session = session
        self.user_id = user_id
        self.tools: Dict[str, Callable[..., Awaitable[Dict[str, Any]]]] = {}

    def register_tool(
        self,
        name: str,
        func: Callable[..., Awaitable[Dict[str, Any]]]
    ) -> None:
        """Register a tool function.

        Args:
            name: Tool name (e.g., "add_task")
            func: Async function that implements the tool
        """
        self.tools[name] = func
        logger.info(f"Registered tool: {name}")

    async def execute(
        self,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a tool with user context.

        Args:
            tool_name: Name of the tool to execute
            arguments: Tool arguments from LLM

        Returns:
            Tool execution result in structured format
        """
        if tool_name not in self.tools:
            logger.error(f"Unknown tool: {tool_name}")
            return {
                "status": "error",
                "error": "unknown_tool",
                "message": f"Tool '{tool_name}' not found"
            }

        # Inject user_id into arguments (critical for user isolation)
        arguments["user_id"] = self.user_id

        try:
            logger.info(f"Executing tool: {tool_name} for user: {self.user_id}")
            result = await self.tools[tool_name](
                session=self.session,
                **arguments
            )
            logger.info(f"Tool {tool_name} executed successfully")
            return result
        except Exception as e:
            logger.error(f"Tool execution error ({tool_name}): {str(e)}", exc_info=True)
            return {
                "status": "error",
                "error": "execution_error",
                "message": f"Failed to execute {tool_name}: {str(e)}"
            }

    def get_registered_tools(self) -> list[str]:
        """Get list of registered tool names.

        Returns:
            List of tool names
        """
        return list(self.tools.keys())
