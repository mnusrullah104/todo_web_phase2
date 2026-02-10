# Implementation Quickstart: Phase III Chatbot

**Feature**: AI Chatbot Integration for Todo Management
**Date**: 2026-02-09
**Status**: Design
**Related Documents**: [spec.md](spec.md), [plan.md](plan.md), [data-model.md](data-model.md)

## Overview

This quickstart guide provides a step-by-step implementation path for Phase III chatbot integration. Follow these steps in order to build the conversational AI assistant for todo management.

## Prerequisites

Before starting implementation:

- [ ] Phase I and Phase II are fully functional
- [ ] Python 3.13+ installed
- [ ] PostgreSQL database accessible (Neon Serverless)
- [ ] Cohere API key obtained
- [ ] Better Auth JWT system working
- [ ] All existing tests passing

## Implementation Phases

### Phase 0: Setup and Dependencies ✅ COMPLETE

**Goal**: Install required packages and configure environment

**Tasks**:
1. Add dependencies to requirements.txt
2. Configure environment variables
3. Verify installations

**Dependencies to Add**:
```txt
# requirements.txt additions
cohere>=5.20.0
# mcp[cli]>=1.0.0  # Optional - not needed for direct tool implementation
```

**Environment Variables**:
```env
# .env additions
COHERE_API_KEY=your-cohere-api-key-here
```

**Verification**:
```bash
# Install dependencies
uv pip install -r requirements.txt

# Verify Cohere SDK
python -c "import cohere; print(cohere.__version__)"

# Test Cohere API connection
python -c "import cohere; co = cohere.ClientV2(api_key='your-key'); print('Connected')"
```

---

### Phase 1: Database Models ⏭️ NEXT

**Goal**: Create Conversation and Message models with migrations

**Files to Create**:
- `backend/src/models/conversation.py`
- `backend/src/models/message.py`
- `backend/alembic/versions/003_add_conversation_models.py`

**Implementation Steps**:

1. **Create Conversation Model** (`backend/src/models/conversation.py`)
   - Copy from [data-model.md](data-model.md#conversation-model)
   - Add to `backend/src/models/__init__.py`

2. **Create Message Model** (`backend/src/models/message.py`)
   - Copy from [data-model.md](data-model.md#message-model)
   - Add MessageRole enum
   - Add to `backend/src/models/__init__.py`

3. **Update User Model** (`backend/src/models/user.py`)
   - Add conversations relationship
   - See [data-model.md](data-model.md#updated-user-model)

4. **Create Alembic Migration**
   ```bash
   cd backend
   alembic revision -m "Add conversation and message models for Phase III"
   ```
   - Copy migration code from [data-model.md](data-model.md#alembic-migration)
   - Review generated migration file
   - Ensure indexes are created

5. **Run Migration**
   ```bash
   alembic upgrade head
   ```

6. **Verify Migration**
   ```bash
   # Check tables exist
   psql $DATABASE_URL -c "\dt conversations"
   psql $DATABASE_URL -c "\dt messages"

   # Check indexes
   psql $DATABASE_URL -c "\di idx_messages_conversation_sequence"
   psql $DATABASE_URL -c "\di idx_conversations_user_updated"
   ```

**Acceptance Criteria**:
- [ ] Conversation model created with all fields
- [ ] Message model created with MessageRole enum
- [ ] User model updated with relationship
- [ ] Migration runs without errors
- [ ] Tables and indexes created in database
- [ ] Foreign key constraints working

---

### Phase 2: Tool Implementation

**Goal**: Implement 5 MCP tools with user isolation

**Files to Create**:
- `backend/src/mcp/__init__.py`
- `backend/src/mcp/tools/__init__.py`
- `backend/src/mcp/tools/add_task.py`
- `backend/src/mcp/tools/list_tasks.py`
- `backend/src/mcp/tools/complete_task.py`
- `backend/src/mcp/tools/delete_task.py`
- `backend/src/mcp/tools/update_task.py`
- `backend/src/mcp/tool_executor.py`

**Implementation Steps**:

1. **Create Tool Implementations**
   - Reference [tool-contracts.md](contracts/tool-contracts.md)
   - Each tool is an async function
   - Accept session, user_id, and tool-specific parameters
   - Return structured JSON responses

2. **Create ToolExecutor Class** (`backend/src/mcp/tool_executor.py`)
   - Manages tool registry
   - Injects user_id into tool calls
   - Handles tool execution and errors
   - See [research.md](research.md#complete-tool-execution-pattern)

3. **Implement Each Tool**:

   **add_task.py**:
   ```python
   async def add_task_impl(
       session: Session,
       user_id: UUID,
       title: str,
       description: str = "",
       completed: bool = False
   ) -> Dict[str, Any]:
       # Validate title
       if not title or len(title) > 255:
           return {"status": "error", "error": "validation_error", "message": "Invalid title"}

       # Create task
       task = Task(user_id=user_id, title=title, description=description, completed=completed)
       session.add(task)
       session.commit()
       session.refresh(task)

       return {"status": "success", "data": task.dict()}
   ```

   **list_tasks.py**:
   ```python
   async def list_tasks_impl(
       session: Session,
       user_id: UUID,
       completed: Optional[bool] = None
   ) -> Dict[str, Any]:
       # Query with user_id filter
       statement = select(Task).where(Task.user_id == user_id)
       if completed is not None:
           statement = statement.where(Task.completed == completed)

       tasks = session.exec(statement).all()

       return {
           "status": "success",
           "data": {
               "tasks": [task.dict() for task in tasks],
               "count": len(tasks),
               "filter": "completed" if completed is True else "pending" if completed is False else "all"
           }
       }
   ```

   **complete_task.py**:
   ```python
   async def complete_task_impl(
       session: Session,
       user_id: UUID,
       task_id: str,
       completed: bool = True
   ) -> Dict[str, Any]:
       # Validate and get task
       try:
           task_uuid = UUID(task_id)
       except ValueError:
           return {"status": "error", "error": "validation_error", "message": "Invalid task ID"}

       task = session.exec(
           select(Task).where(Task.id == task_uuid).where(Task.user_id == user_id)
       ).first()

       if not task:
           return {"status": "error", "error": "not_found", "message": "Task not found"}

       # Update completion status
       task.completed = completed
       session.commit()
       session.refresh(task)

       return {"status": "success", "data": task.dict()}
   ```

   **delete_task.py**:
   ```python
   async def delete_task_impl(
       session: Session,
       user_id: UUID,
       task_id: str
   ) -> Dict[str, Any]:
       # Validate and get task
       try:
           task_uuid = UUID(task_id)
       except ValueError:
           return {"status": "error", "error": "validation_error", "message": "Invalid task ID"}

       task = session.exec(
           select(Task).where(Task.id == task_uuid).where(Task.user_id == user_id)
       ).first()

       if not task:
           return {"status": "error", "error": "not_found", "message": "Task not found"}

       # Delete task
       session.delete(task)
       session.commit()

       return {"status": "success", "data": {"id": task_id, "deleted": True}}
   ```

   **update_task.py**:
   ```python
   async def update_task_impl(
       session: Session,
       user_id: UUID,
       task_id: str,
       title: Optional[str] = None,
       description: Optional[str] = None
   ) -> Dict[str, Any]:
       # Validate at least one field provided
       if title is None and description is None:
           return {"status": "error", "error": "validation_error", "message": "At least one field required"}

       # Validate and get task
       try:
           task_uuid = UUID(task_id)
       except ValueError:
           return {"status": "error", "error": "validation_error", "message": "Invalid task ID"}

       task = session.exec(
           select(Task).where(Task.id == task_uuid).where(Task.user_id == user_id)
       ).first()

       if not task:
           return {"status": "error", "error": "not_found", "message": "Task not found"}

       # Update fields
       if title is not None:
           if len(title) > 255:
               return {"status": "error", "error": "validation_error", "message": "Title too long"}
           task.title = title
       if description is not None:
           task.description = description

       session.commit()
       session.refresh(task)

       return {"status": "success", "data": task.dict()}
   ```

4. **Create Tool Definitions** (`backend/src/mcp/tools/__init__.py`)
   ```python
   import cohere

   TOOL_DEFINITIONS = [
       cohere.ToolV2(
           type="function",
           function={
               "name": "add_task",
               "description": "Create a new task for the user",
               "parameters": {
                   "type": "object",
                   "properties": {
                       "title": {"type": "string", "description": "Task title"},
                       "description": {"type": "string", "description": "Task description (optional)"},
                       "completed": {"type": "boolean", "description": "Completion status (default: false)"}
                   },
                   "required": ["title"]
               }
           }
       ),
       # ... other tools
   ]
   ```

**Acceptance Criteria**:
- [ ] All 5 tools implemented
- [ ] ToolExecutor class created
- [ ] User_id injection working
- [ ] Tool definitions in Cohere format
- [ ] Unit tests passing for each tool
- [ ] User isolation enforced

---

### Phase 3: Conversation Service

**Goal**: Implement conversation persistence logic

**Files to Create**:
- `backend/src/services/__init__.py`
- `backend/src/services/conversation.py`

**Implementation Steps**:

1. **Create ConversationService** (`backend/src/services/conversation.py`)
   ```python
   from sqlmodel import Session, select, func
   from uuid import UUID
   from typing import List, Optional
   from datetime import datetime

   from ..models.conversation import Conversation
   from ..models.message import Message, MessageRole

   class ConversationService:
       def __init__(self, session: Session):
           self.session = session

       def create_conversation(self, user_id: UUID, title: Optional[str] = None) -> Conversation:
           """Create a new conversation"""
           conversation = Conversation(user_id=user_id, title=title)
           self.session.add(conversation)
           self.session.commit()
           self.session.refresh(conversation)
           return conversation

       def get_conversation(self, conversation_id: UUID, user_id: UUID) -> Optional[Conversation]:
           """Get conversation with user validation"""
           return self.session.exec(
               select(Conversation)
               .where(Conversation.id == conversation_id)
               .where(Conversation.user_id == user_id)
               .where(Conversation.deleted == False)
           ).first()

       def add_message(
           self,
           conversation_id: UUID,
           role: MessageRole,
           content: str,
           tool_calls: Optional[dict] = None,
           tool_call_id: Optional[str] = None
       ) -> Message:
           """Add a message to conversation"""
           # Get next sequence number
           max_seq = self.session.exec(
               select(func.max(Message.sequence_number))
               .where(Message.conversation_id == conversation_id)
           ).first() or 0

           message = Message(
               conversation_id=conversation_id,
               sequence_number=max_seq + 1,
               role=role,
               content=content,
               tool_calls=tool_calls,
               tool_call_id=tool_call_id
           )
           self.session.add(message)

           # Update conversation timestamp
           conversation = self.session.get(Conversation, conversation_id)
           conversation.updated_at = datetime.utcnow()

           self.session.commit()
           self.session.refresh(message)
           return message

       def get_messages(
           self,
           conversation_id: UUID,
           limit: int = 50,
           offset: int = 0
       ) -> List[Message]:
           """Get conversation messages"""
           return self.session.exec(
               select(Message)
               .where(Message.conversation_id == conversation_id)
               .where(Message.deleted == False)
               .order_by(Message.sequence_number)
               .offset(offset)
               .limit(limit)
           ).all()
   ```

**Acceptance Criteria**:
- [ ] ConversationService created
- [ ] Create conversation method working
- [ ] Get conversation with user validation
- [ ] Add message with sequence numbering
- [ ] Get messages with pagination
- [ ] Unit tests passing

---

### Phase 4: Cohere Agent

**Goal**: Implement TodoChatAgent with Cohere integration

**Files to Create**:
- `backend/src/agent/__init__.py`
- `backend/src/agent/cohere_client.py`
- `backend/src/agent/todo_agent.py`

**Implementation Steps**:

1. **Create Cohere Client** (`backend/src/agent/cohere_client.py`)
   ```python
   import cohere
   from ..config.settings import get_settings

   settings = get_settings()

   def get_cohere_client() -> cohere.ClientV2:
       """Get configured Cohere client"""
       return cohere.ClientV2(api_key=settings.cohere_api_key)
   ```

2. **Create TodoChatAgent** (`backend/src/agent/todo_agent.py`)
   - Reference [research.md](research.md#todochatagent-implementation)
   - Implement system prompt
   - Define tool definitions
   - Implement chat method with tool execution loop
   - Handle multi-turn conversations

3. **System Prompt**:
   ```python
   SYSTEM_PROMPT = """You are a helpful task management assistant. You help users manage their todo list through natural conversation.

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
   ```

**Acceptance Criteria**:
- [ ] Cohere client configured
- [ ] TodoChatAgent class created
- [ ] System prompt defined
- [ ] Tool definitions in Cohere format
- [ ] Chat method with tool execution
- [ ] Multi-turn conversation support
- [ ] Integration tests passing

---

### Phase 5: Chat Endpoint

**Goal**: Create stateless chat API endpoint

**Files to Create**:
- `backend/src/api/chat.py`

**Implementation Steps**:

1. **Create Chat Router** (`backend/src/api/chat.py`)
   - Reference [chat-endpoint.md](contracts/chat-endpoint.md)
   - Implement POST /api/{user_id}/chat
   - JWT authentication
   - User_id validation
   - Conversation loading/creation
   - Message persistence
   - Error handling

2. **Request/Response Models**:
   ```python
   from pydantic import BaseModel
   from typing import Optional, List

   class ChatRequest(BaseModel):
       message: str
       conversation_id: Optional[str] = None

   class ToolCallInfo(BaseModel):
       tool: str
       arguments: dict

   class ChatResponse(BaseModel):
       conversation_id: str
       response: str
       tool_calls: List[ToolCallInfo]
       timestamp: str
   ```

3. **Endpoint Implementation**:
   ```python
   @router.post("/{user_id}/chat", response_model=ChatResponse)
   async def chat(
       user_id: str,
       request: ChatRequest,
       current_user_id: UUID = Depends(get_current_user),
       session: Session = Depends(get_session)
   ):
       # Validate user_id
       if str(current_user_id) != user_id:
           raise HTTPException(status_code=403, detail="Not authorized")

       # Initialize services
       conversation_service = ConversationService(session)
       tool_executor = ToolExecutor(session, current_user_id)
       cohere_client = get_cohere_client()
       agent = TodoChatAgent(cohere_client, tool_executor)

       # Load or create conversation
       if request.conversation_id:
           conversation = conversation_service.get_conversation(
               UUID(request.conversation_id), current_user_id
           )
           if not conversation:
               raise HTTPException(status_code=404, detail="Conversation not found")
           history = conversation_service.get_messages(conversation.id)
       else:
           conversation = conversation_service.create_conversation(current_user_id)
           history = []

       # Save user message
       conversation_service.add_message(
           conversation.id, MessageRole.USER, request.message
       )

       # Process with agent
       response = await agent.chat(request.message, history)

       # Save assistant response
       conversation_service.add_message(
           conversation.id,
           MessageRole.ASSISTANT,
           response["response"],
           tool_calls=response.get("tool_calls")
       )

       # Return response
       return ChatResponse(
           conversation_id=str(conversation.id),
           response=response["response"],
           tool_calls=response.get("tool_calls", []),
           timestamp=datetime.utcnow().isoformat()
       )
   ```

4. **Register Router** (`backend/src/api/__init__.py`)
   ```python
   from .chat import router as chat_router

   app.include_router(chat_router, prefix="/api", tags=["chat"])
   ```

**Acceptance Criteria**:
- [ ] Chat endpoint created
- [ ] JWT authentication working
- [ ] User_id validation enforced
- [ ] Conversation persistence working
- [ ] Agent integration working
- [ ] Error handling complete
- [ ] Integration tests passing

---

### Phase 6: Frontend Integration

**Goal**: Add ChatKit UI to existing frontend

**Files to Create/Modify**:
- `frontend/src/components/ChatWidget.tsx`
- `frontend/src/app/layout.tsx` (add chat widget)

**Implementation Steps**:

1. **Install ChatKit** (or use custom component)
   ```bash
   cd frontend
   npm install @chatscope/chat-ui-kit-react
   ```

2. **Create ChatWidget Component**:
   ```tsx
   'use client';

   import { useState } from 'react';
   import { MainContainer, ChatContainer, MessageList, Message, MessageInput } from '@chatscope/chat-ui-kit-react';

   export default function ChatWidget() {
     const [messages, setMessages] = useState([]);
     const [conversationId, setConversationId] = useState(null);

     const handleSend = async (message: string) => {
       // Add user message to UI
       setMessages([...messages, { role: 'user', content: message }]);

       // Send to backend
       const response = await fetch(`/api/${userId}/chat`, {
         method: 'POST',
         headers: {
           'Content-Type': 'application/json',
           'Authorization': `Bearer ${token}`
         },
         body: JSON.stringify({ message, conversation_id: conversationId })
       });

       const data = await response.json();

       // Update conversation ID
       if (!conversationId) {
         setConversationId(data.conversation_id);
       }

       // Add assistant response to UI
       setMessages([...messages, { role: 'assistant', content: data.response }]);
     };

     return (
       <div style={{ position: 'fixed', bottom: 20, right: 20, width: 400, height: 500 }}>
         <MainContainer>
           <ChatContainer>
             <MessageList>
               {messages.map((msg, i) => (
                 <Message key={i} model={{ message: msg.content, sender: msg.role }} />
               ))}
             </MessageList>
             <MessageInput placeholder="Type a message..." onSend={handleSend} />
           </ChatContainer>
         </MainContainer>
       </div>
     );
   }
   ```

3. **Add to Layout**:
   ```tsx
   import ChatWidget from '@/components/ChatWidget';

   export default function RootLayout({ children }) {
     return (
       <html>
         <body>
           {children}
           <ChatWidget />
         </body>
       </html>
     );
   }
   ```

**Acceptance Criteria**:
- [ ] ChatKit installed (or custom component created)
- [ ] ChatWidget component created
- [ ] Chat widget visible in UI
- [ ] Messages send to backend
- [ ] Responses display in UI
- [ ] Conversation persistence working
- [ ] UI tests passing

---

### Phase 7: Testing

**Goal**: Comprehensive test coverage

**Test Files to Create**:
- `backend/tests/test_models_conversation.py`
- `backend/tests/test_tools.py`
- `backend/tests/test_conversation_service.py`
- `backend/tests/test_chat_endpoint.py`
- `backend/tests/test_agent.py`

**Test Categories**:

1. **Unit Tests**:
   - Model validation
   - Tool implementations
   - ConversationService methods
   - ToolExecutor logic

2. **Integration Tests**:
   - Chat endpoint flow
   - Agent + tools integration
   - Database persistence
   - User isolation

3. **Security Tests**:
   - JWT validation
   - User_id enforcement
   - Cross-user access prevention
   - Input sanitization

4. **Performance Tests**:
   - Conversation history loading
   - Concurrent user handling
   - Database query performance

**Acceptance Criteria**:
- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] Security tests passing
- [ ] Performance tests passing
- [ ] Code coverage >80%

---

## Quick Reference

### Key Files

**Backend**:
- Models: `backend/src/models/conversation.py`, `backend/src/models/message.py`
- Tools: `backend/src/mcp/tools/*.py`
- Agent: `backend/src/agent/todo_agent.py`
- Service: `backend/src/services/conversation.py`
- API: `backend/src/api/chat.py`

**Frontend**:
- Chat Widget: `frontend/src/components/ChatWidget.tsx`

**Database**:
- Migration: `backend/alembic/versions/003_add_conversation_models.py`

### Environment Variables

```env
COHERE_API_KEY=your-cohere-api-key
DATABASE_URL=postgresql://...
JWT_SECRET=your-jwt-secret
```

### Common Commands

```bash
# Install dependencies
uv pip install -r requirements.txt

# Run migrations
cd backend && alembic upgrade head

# Run backend
cd backend && uvicorn src.main:app --reload

# Run frontend
cd frontend && npm run dev

# Run tests
cd backend && pytest

# Check database
psql $DATABASE_URL -c "\dt"
```

## Troubleshooting

### Cohere API Errors

**Problem**: `CohereAPIError: Unauthorized`
**Solution**: Check COHERE_API_KEY in .env

**Problem**: `CohereConnectionError`
**Solution**: Check internet connection, verify API endpoint

### Database Errors

**Problem**: Migration fails
**Solution**: Check database connection, review migration SQL

**Problem**: Foreign key constraint violation
**Solution**: Ensure User model exists, check user_id values

### Tool Execution Errors

**Problem**: Tools not found
**Solution**: Check tool registration in ToolExecutor

**Problem**: User isolation not working
**Solution**: Verify user_id injection in ToolExecutor

## Next Steps

After completing implementation:

1. **Run /sp.tasks** to generate detailed task breakdown
2. **Run /sp.implement** to execute implementation
3. **Test thoroughly** with real user scenarios
4. **Deploy** to staging environment
5. **User acceptance testing**
6. **Production deployment**

## Related Documents

- [spec.md](spec.md) - Feature requirements
- [plan.md](plan.md) - Architecture and decisions
- [data-model.md](data-model.md) - Database schema
- [contracts/chat-endpoint.md](contracts/chat-endpoint.md) - API specification
- [contracts/tool-contracts.md](contracts/tool-contracts.md) - Tool specifications
- [research.md](research.md) - Technology research
