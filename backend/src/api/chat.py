"""Chat API endpoint for Phase III AI Chatbot Integration.

Provides stateless chat interface for todo management via natural language.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from uuid import UUID
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
import logging

from ..database.session import get_session
from ..services.conversation import ConversationService
from ..mcp.tool_executor import ToolExecutor
from ..mcp.tools.add_task import add_task_impl
from ..mcp.tools.list_tasks import list_tasks_impl
from ..mcp.tools.complete_task import complete_task_impl
from ..mcp.tools.delete_task import delete_task_impl
from ..mcp.tools.update_task import update_task_impl
from ..mcp.tools.navigate import navigate
from ..agent.cohere_client import get_cohere_client
from ..agent.todo_agent import TodoChatAgent
from ..models.message import MessageRole

logger = logging.getLogger(__name__)

router = APIRouter(tags=["chat"])


# Request/Response Models
class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(..., min_length=1, max_length=2000, description="User's message")
    conversation_id: Optional[str] = Field(None, description="Optional conversation UUID")


class ToolCallInfo(BaseModel):
    """Information about a tool call."""
    tool: str = Field(..., description="Tool name")
    arguments: dict = Field(..., description="Tool arguments")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    conversation_id: str = Field(..., description="Conversation UUID")
    response: str = Field(..., description="AI assistant's response")
    tool_calls: List[ToolCallInfo] = Field(default_factory=list, description="Tools executed")
    timestamp: str = Field(..., description="ISO 8601 timestamp")


# TODO: Implement JWT authentication dependency
# For now, using a placeholder that extracts user_id from path
async def get_current_user(user_id: str) -> UUID:
    """Get current authenticated user.

    TODO: Replace with actual JWT authentication from Better Auth.
    For now, this is a placeholder that trusts the user_id from the path.
    """
    try:
        return UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )


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

    Args:
        user_id: User ID from path (must match authenticated user)
        request: Chat request with message and optional conversation_id
        current_user_id: Authenticated user ID from JWT
        session: Database session

    Returns:
        ChatResponse with assistant's response and metadata

    Raises:
        HTTPException: 403 if user_id mismatch, 404 if conversation not found,
                      503 if AI service unavailable
    """
    # Validate user_id matches authenticated user
    if str(current_user_id) != user_id:
        logger.warning(f"User ID mismatch: {current_user_id} != {user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's chat"
        )

    try:
        # Initialize services
        conversation_service = ConversationService(session)
        tool_executor = ToolExecutor(session, current_user_id)

        # Register all 6 tools (Phase III - Complete + Navigation)
        tool_executor.register_tool("add_task", add_task_impl)
        tool_executor.register_tool("list_tasks", list_tasks_impl)
        tool_executor.register_tool("complete_task", complete_task_impl)
        tool_executor.register_tool("delete_task", delete_task_impl)
        tool_executor.register_tool("update_task", update_task_impl)
        tool_executor.register_tool("navigate", navigate)

        # Get Cohere client
        try:
            cohere_client = get_cohere_client()
        except ValueError as e:
            logger.error(f"Cohere client initialization failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="AI service configuration error. Please contact support."
            )

        agent = TodoChatAgent(cohere_client, tool_executor)

        # Load or create conversation
        conversation = None
        conversation_history = []

        if request.conversation_id:
            try:
                conversation_uuid = UUID(request.conversation_id)
                conversation = conversation_service.get_conversation(
                    conversation_uuid,
                    current_user_id
                )
                if not conversation:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Conversation not found"
                    )
                # Load message history
                messages = conversation_service.get_messages(conversation.id)
                conversation_history = [
                    {"role": msg.role.value, "content": msg.content}
                    for msg in messages
                ]
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Invalid conversation ID format"
                )
        else:
            # Create new conversation
            conversation = conversation_service.create_conversation(current_user_id)

        # Save user message
        conversation_service.add_message(
            conversation.id,
            MessageRole.USER,
            request.message
        )

        # Process with agent
        logger.info(f"Processing chat message for user {current_user_id}")
        agent_response = await agent.chat(request.message, conversation_history)

        # Check for errors
        if "error" in agent_response:
            if agent_response["error"] == "cohere_api_error":
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="AI service temporarily unavailable. Please try again in a moment."
                )

        # Save assistant response
        # Convert UUIDs to strings in tool_calls for JSON serialization
        tool_calls_serializable = None
        if agent_response.get("tool_calls"):
            tool_calls_serializable = []
            for tc in agent_response["tool_calls"]:
                serializable_tc = {"tool": tc["tool"], "arguments": {}}
                for key, value in tc["arguments"].items():
                    if isinstance(value, UUID):
                        serializable_tc["arguments"][key] = str(value)
                    else:
                        serializable_tc["arguments"][key] = value
                tool_calls_serializable.append(serializable_tc)

        conversation_service.add_message(
            conversation.id,
            MessageRole.ASSISTANT,
            agent_response["response"],
            tool_calls=tool_calls_serializable
        )

        # Return response
        return ChatResponse(
            conversation_id=str(conversation.id),
            response=agent_response["response"],
            tool_calls=[
                ToolCallInfo(tool=tc["tool"], arguments=tc["arguments"])
                for tc in agent_response.get("tool_calls", [])
            ],
            timestamp=datetime.utcnow().isoformat()
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )
