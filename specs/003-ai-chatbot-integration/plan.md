# Implementation Plan: AI Chatbot Integration for Todo Management

**Branch**: `003-ai-chatbot-integration` | **Date**: 2026-02-09 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/003-ai-chatbot-integration/spec.md`

**Note**: This plan follows the SDD workflow: Constitution → Specify → Clarify → **Plan** → Tasks → Implement

## Summary

Integrate a natural language AI chatbot into the existing full-stack Todo application, enabling users to manage tasks (add, list, complete, delete, update) through conversational commands. The chatbot uses Cohere API for natural language understanding, connects to 5 MCP tools for task operations, persists conversation history in the database, and maintains strict user isolation. The implementation extends the existing Phase II backend without breaking any existing functionality.

**Core Flow**: User opens chat interface → types natural language command → stateless /chat endpoint loads conversation history → Cohere agent interprets intent → calls appropriate MCP tools with user_id → updates database → saves conversation → returns friendly response

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript/JavaScript (frontend - existing Next.js 14+)
**Primary Dependencies**:
- Backend: FastAPI, SQLModel, Official MCP SDK, Cohere Python SDK, Better Auth (existing), Neon Postgres driver
- Frontend: Next.js 14+ (existing), ChatKit or custom chat component, existing auth integration

**Storage**: Neon Serverless PostgreSQL (existing) - extend with Conversation and Message tables
**Testing**: pytest (backend), Jest/React Testing Library (frontend - existing)
**Target Platform**: Web application (Linux server backend, modern browsers frontend)
**Project Type**: Web (backend + frontend)
**Performance Goals**:
- Chat endpoint response: < 5 seconds (95th percentile)
- Conversation history load: < 1 second
- Support 100 concurrent chat users
- MCP tool execution: < 500ms per tool call

**Constraints**:
- Stateless chat endpoint (no server-side session state)
- Strict user isolation (user_id in every operation)
- Zero breaking changes to existing Phase I/II functionality
- Cohere API only (no other LLM providers)
- Must use Official MCP SDK for tool implementation

**Scale/Scope**:
- Initial: 100 concurrent users
- Average: < 1000 messages per user conversation history
- 5 MCP tools total
- Single chat endpoint

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Core Principles Compliance

✅ **I. Spec-First Development**: Complete specification exists at specs/003-ai-chatbot-integration/spec.md with 42 functional requirements, 6 user stories, and clear acceptance criteria.

✅ **II. Zero Manual Coding Rule**: All code will be generated via Claude Code following this plan and task breakdown.

✅ **III. Phase Isolation Principle**: Phase III only - adds chatbot functionality without modifying Phase I/II code. Existing Task CRUD, auth, and database schema remain unchanged. New models (Conversation, Message) are additive only.

✅ **IV. Deterministic Architecture**: Stateless chat endpoint with explicit contracts. MCP tools have defined input/output schemas. Cohere agent behavior governed by system prompt specification.

✅ **V. AI-Native Design**: Chatbot is first-class feature using Cohere API, Official MCP SDK, and ChatKit. Agent behavior defined in specification with clear tool contracts.

✅ **VI. Cloud-Native Readiness**: Stateless architecture enables horizontal scaling. Configuration via environment variables (COHERE_API_KEY, DATABASE_URL). Container-ready design.

### Engineering Standards Compliance

✅ **I. Code Quality**: Modular structure (separate modules for MCP tools, agent, chat endpoint, database models). Clean separation of concerns. No hardcoded secrets.

✅ **II. API Design**: REST endpoint POST /api/{user_id}/chat follows existing patterns. JWT authentication required. User isolation enforced. Stateless design.

✅ **III. Database Discipline**: New Conversation and Message models documented in spec. Migrations will be reproducible. No DB logic in frontend.

✅ **IV. Security Baseline**: JWT authentication enforced. User_id validation on every request. Secrets in environment variables. Strict user isolation in all MCP tools.

✅ **V. Observability Ready**: Logging for chat requests, tool calls, errors. Human-readable error messages. Ready for Phase IV+ monitoring.

### Phase III Specific Standards Compliance

✅ **MCP Server Implementation**: Will use Official MCP SDK with exactly 5 tools (add_task, list_tasks, complete_task, delete_task, update_task). All tools accept user_id and enforce isolation.

✅ **Agent Behavior Requirements**: Cohere API for all LLM operations. Friendly, conversational responses. Handles ambiguity intelligently. Never hallucinates data.

✅ **Chat API Contract**: POST /api/{user_id}/chat is stateless. Validates JWT. Persists conversation history. Loads history from database. Enforces user isolation.

✅ **Database Models**: Conversation and Message models will be implemented. History persists across restarts. Supports resumption.

✅ **Frontend Integration**: ChatKit UI will be integrated. Existing Task CRUD UI remains functional. Seamless experience between traditional and chat interfaces.

**GATE STATUS**: ✅ PASS - All constitution requirements satisfied. No violations. Ready for Phase 0 research.

## Project Structure

### Documentation (this feature)

```text
specs/003-ai-chatbot-integration/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file (in progress)
├── research.md          # Phase 0 output (to be generated)
├── data-model.md        # Phase 1 output (to be generated)
├── quickstart.md        # Phase 1 output (to be generated)
├── contracts/           # Phase 1 output (to be generated)
│   └── chat-api.yaml    # OpenAPI spec for chat endpoint
├── checklists/
│   └── requirements.md  # Spec quality checklist (complete)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── task.py           # Existing - DO NOT MODIFY
│   │   ├── user.py           # Existing - DO NOT MODIFY
│   │   ├── conversation.py   # NEW - Conversation model
│   │   └── message.py        # NEW - Message model
│   ├── api/
│   │   ├── tasks.py          # Existing - DO NOT MODIFY
│   │   ├── auth.py           # Existing - DO NOT MODIFY
│   │   └── chat.py           # NEW - Chat endpoint
│   ├── mcp/
│   │   ├── server.py         # NEW - MCP server setup
│   │   └── tools/            # NEW - MCP tool implementations
│   │       ├── add_task.py
│   │       ├── list_tasks.py
│   │       ├── complete_task.py
│   │       ├── delete_task.py
│   │       └── update_task.py
│   ├── agent/
│   │   ├── cohere_client.py  # NEW - Cohere API integration
│   │   ├── todo_agent.py     # NEW - TodoChatAgent implementation
│   │   └── system_prompt.py  # NEW - Agent behavior rules
│   ├── services/
│   │   └── conversation.py   # NEW - Conversation CRUD helpers
│   ├── auth/
│   │   └── jwt.py            # Existing - reuse for chat endpoint
│   ├── database/
│   │   └── session.py        # Existing - reuse
│   ├── config/
│   │   └── settings.py       # Existing - extend with COHERE_API_KEY
│   └── main.py               # Existing - register chat router
└── tests/
    ├── test_mcp_tools.py     # NEW - Unit tests for MCP tools
    ├── test_chat_endpoint.py # NEW - Integration tests for chat API
    ── test_agent.py         # NEW - Agent behavior tests
    └── test_conversation.py  # NEW - Conversation persistence tests

frontend/
├── src/
│   ├── components/
│   │   └── ChatInterface.tsx # NEW - Chat UI component (ChatKit integration)
│   ├── pages/
│   │   └── (existing pages)  # DO NOT MODIFY
│   └── services/
│       └── chatApi.ts        # NEW - Chat API client
└── tests/
    └── ChatInterface.test.tsx # NEW - Chat UI tests
```

**Structure Decision**: Web application structure (backend + frontend). Backend extends existing FastAPI application with new modules for MCP server, Cohere agent, and chat endpoint. Frontend adds chat interface component while preserving all existing UI. Clear separation between new chat functionality and existing Task CRUD ensures zero breaking changes.

## Complexity Tracking

> **Not applicable** - No constitution violations to justify. All requirements align with constitution standards.

## Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│  ┌──────────────────┐         ┌──────────────────────────┐ │
│  │  Existing Todo   │         │  NEW: Chat Interface     │ │
│  │  UI (Phase II)   │         │  (ChatKit or custom)     │ │
│  │  - Task List     │         │  - Message display       │ │
│  │  - Add/Edit Form │         │  - Input field           │ │
│  │  - Auth UI       │         │  - Floating icon         │ │
│  └──────────────────┘         └──────────────────────────┘ │
│           │                              │                   │
│           │ JWT                          │ JWT               │
└───────────┼──────────────────────────────┼───────────────────┘
            │                              │
            ▼                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend (FastAPI)                         │
│  ┌──────────────────┐         ┌──────────────────────────┐ │
│  │  Existing Task   │         │  NEW: Chat Endpoint      │ │
│  │  CRUD Routes     │         │  POST /api/{user_id}/chat│ │
│  │  (Phase II)      │         │  - Load conversation     │ │
│  │  DO NOT MODIFY   │         │  - Persist messages      │ │
│  └──────────────────┘         │  - Run Cohere agent      │ │
│                                │  - Return response       │ │
│                                └────────┬─────────────────┘ │
│                                         │                    │
│                                         ▼                    │
│                          ┌──────────────────────────┐       │
│                          │  TodoChatAgent (Cohere)  │       │
│                          │  - System prompt         │       │
│                          │  - Tool calling          │       │
│                          │  - Multi-tool support    │       │
│                          └────────┬─────────────────┘       │
│                                   │                          │
│                                   ▼                          │
│                          ┌──────────────────────────┐       │
│                          │  MCP Server (Official SDK)│       │
│                          │  - Tool registration     │       │
│                          │  - Tool execution        │       │
│                          └────────┬─────────────────┘       │
│                                   │                          │
│                    ┌──────────────┴──────────────┐          │
│                    ▼                             ▼          │
│         ┌──────────────────┐         ┌──────────────────┐  │
│         │  5 MCP Tools     │         │  Database        │  │
│         │  - add_task      │────────▶│  - Task (exist)  │  │
│         │  - list_tasks    │         │  - User (exist)  │  │
│         │  - complete_task │         │  - Conversation  │  │
│         │  - delete_task   │         │  - Message       │  │
│         │  - update_task   │         │  (Neon Postgres) │  │
│         │  (user_id scoped)│         └──────────────────┘  │
│         └──────────────────┘                                │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

**User Message Flow**:
1. User types message in chat interface
2. Frontend sends POST /api/{user_id}/chat with JWT + message
3. Backend validates JWT, extracts user_id
4. Load or create conversation for user
5. Persist user message to Message table
6. Pass message + conversation history to Cohere agent
7. Agent interprets intent, calls appropriate MCP tool(s)
8. MCP tools execute with user_id, interact with database
9. Tool results returned to agent
10. Agent generates friendly response
11. Persist assistant message to Message table
12. Return response to frontend
13. Frontend displays response in chat

**User Isolation Enforcement**:
- JWT validation at endpoint (user_id from token)
- user_id passed to all MCP tool calls
- MCP tools filter database queries by user_id
- Conversation and Message tables link to user_id
- No cross-user data access possible

## Key Architectural Decisions

### Decision 1: LLM Provider - Cohere API

**Options Considered**:
- OpenAI API with Agents SDK
- Cohere API with native tool calling
- Anthropic Claude API

**Chosen**: Cohere API with native tool calling

**Rationale**:
- Constitution mandates Cohere API for Phase III
- Cohere provides native tool/function calling capabilities
- Avoids dependency on OpenAI ecosystem
- Cohere Command models support multi-tool orchestration

**Tradeoffs**:
- ✅ Aligns with constitution requirements
- ✅ Native tool calling support
- ⚠️ Less ecosystem tooling than OpenAI
- ⚠️ Requires custom agent implementation (not using OpenAI Agents SDK)

### Decision 2: MCP Server Placement - Same FastAPI Application

**Options Considered**:
- Separate microservice for MCP server
- Embed MCP server in existing FastAPI app
- Serverless functions for each tool

**Chosen**: Embed MCP server in existing FastAPI app

**Rationale**:
- Simpler deployment (single application)
- Shared database connection pool
- Easier development and testing
- Lower infrastructure overhead
- Stateless design still enables horizontal scaling

**Tradeoffs**:
- ✅ Simpler architecture
- ✅ Shared resources (DB, auth)
- ✅ Easier local development
- ⚠️ Slightly coupled (but modular code structure mitigates)

### Decision 3: Chat UI Solution - ChatKit with Custom Backend

**Options Considered**:
- OpenAI ChatKit (hosted, custom backend)
- Build custom React chat component
- Use third-party chat library (react-chat-elements, etc.)

**Chosen**: ChatKit with custom backend URL

**Rationale**:
- Faster implementation (pre-built UI)
- Professional chat interface out of the box
- Supports custom backend endpoints
- Matches specification requirement

**Tradeoffs**:
- ✅ Rapid development
- ✅ Professional UI/UX
- ✅ Maintained by OpenAI
- ⚠️ Requires domain allowlist configuration
- ⚠️ Less customization than fully custom component

### Decision 4: Conversation State Storage - Database Only

**Options Considered**:
- Redis for session state + DB for persistence
- Database only (stateless)
- In-memory cache + DB

**Chosen**: Database only (stateless)

**Rationale**:
- Aligns with stateless architecture requirement
- Survives server restarts (requirement)
- Simpler infrastructure (no Redis needed)
- Horizontal scaling without session affinity

**Tradeoffs**:
- ✅ True stateless design
- ✅ Survives restarts
- ✅ Simpler deployment
- ⚠️ Slightly higher DB load (mitigated by indexing)

### Decision 5: Ambiguous Task Reference Handling - Agent Decides

**Options Considered**:
- Always ask user for clarification
- Always list tasks first, then act
- Let agent decide based on context

**Chosen**: Let agent decide (often lists first)

**Rationale**:
- Better user experience (fewer turns)
- Agent can use context to determine if clarification needed
- Cohere's reasoning can handle ambiguity intelligently

**Tradeoffs**:
- ✅ More natural conversation
- ✅ Fewer back-and-forth exchanges
- ⚠️ Depends on Cohere reasoning quality
- ⚠️ May occasionally misinterpret (mitigated by confirmation messages)

### Decision 6: Tool Error Handling - Agent Handles with Friendly Messages

**Options Considered**:
- Return raw error to frontend
- Agent handles and generates friendly message
- Hybrid (some errors to frontend, some to agent)

**Chosen**: Agent handles and generates friendly message

**Rationale**:
- More natural conversation flow
- Consistent error messaging style
- Reduces frontend complexity
- Agent can suggest alternatives

**Tradeoffs**:
- ✅ Better UX (conversational errors)
- ✅ Simpler frontend
- ✅ Agent can provide context-aware help
- ⚠️ Slightly more complex agent logic

## Phase 0: Research & Technology Validation

### Research Areas

1. **Cohere Tool Calling API**
   - How to define tools/functions for Cohere
   - Multi-tool invocation in single request
   - Tool result handling and response generation
   - Error handling patterns

2. **Official MCP SDK Integration**
   - MCP server setup with FastAPI
   - Tool registration and discovery
   - Tool execution patterns
   - User context passing

3. **ChatKit Integration**
   - Custom backend configuration
   - Authentication flow with JWT
   - Message format requirements
   - Domain allowlist setup

4. **Conversation Persistence Patterns**
   - Efficient conversation history loading
   - Message pagination strategies
   - Database indexing for performance
   - Conversation resumption logic

5. **Stateless Chat Endpoint Design**
   - Request/response contract
   - Conversation context passing
   - Horizontal scaling considerations
   - Session-less architecture patterns

### Research Outputs

Research findings will be documented in `research.md` with:
- Technology decisions and rationale
- API patterns and examples
- Integration approaches
- Performance considerations
- Security best practices

## Phase 1: Design & Contracts

### Data Model Design

**New Entities**:

1. **Conversation**
   - id: UUID (primary key)
   - user_id: UUID (foreign key to User, indexed)
   - created_at: datetime
   - updated_at: datetime
   - Relationships: has many Messages

2. **Message**
   - id: UUID (primary key)
   - conversation_id: UUID (foreign key to Conversation, indexed)
   - role: enum ('user', 'assistant')
   - content: text
   - tool_calls: JSON (optional, stores tool invocations)
   - created_at: datetime
   - Relationships: belongs to Conversation

**Existing Entities** (DO NOT MODIFY):
- Task: title, description, completed, user_id, created_at, updated_at
- User: email, password_hash, created_at

### API Contracts

**Chat Endpoint**:
```
POST /api/{user_id}/chat
Authorization: Bearer <JWT>

Request:
{
  "message": "string",
  "conversation_id": "uuid | null"  // null creates new conversation
}

Response:
{
  "conversation_id": "uuid",
  "response": "string",
  "tool_calls": [
    {
      "tool": "string",
      "arguments": {},
      "result": {}
    }
  ],
  "timestamp": "ISO 8601"
}

Errors:
- 401: Unauthorized (invalid/missing JWT)
- 403: Forbidden (user_id mismatch)
- 400: Bad Request (invalid message format)
- 500: Internal Server Error (Cohere API failure, DB error)
```

**MCP Tool Contracts**:
All tools follow this pattern:
```
Input: { "user_id": "uuid", ...tool-specific params }
Output: { "status": "success|error", "data": {...} | "error": "..." }
```

Detailed tool schemas will be in `contracts/mcp-tools.yaml`

### Quickstart Guide

Will provide:
- Environment setup (COHERE_API_KEY, DATABASE_URL)
- Database migration commands
- Running the backend server
- Testing the chat endpoint
- Frontend integration steps

## Testing Strategy

### Unit Tests

**MCP Tools** (`tests/test_mcp_tools.py`):
- Each tool with valid inputs → correct output
- User isolation (user A cannot access user B's tasks)
- Error cases (task not found, invalid UUID, empty title)
- Edge cases (no tasks, multiple matches)

**Conversation Service** (`tests/test_conversation.py`):
- Create conversation
- Append messages
- Load conversation history
- Pagination

### Integration Tests

**Chat Endpoint** (`tests/test_chat_endpoint.py`):
- New conversation creation
- Continue existing conversation
- Multi-turn conversation
- JWT validation
- User isolation
- Server restart simulation (history persistence)

**Agent Behavior** (`tests/test_agent.py`):
- Tool selection for various commands
- Multi-tool orchestration
- Ambiguity handling
- Error recovery

### Acceptance Tests

**Golden Command Set**:
- "add task buy groceries" → creates task, confirms
- "show my pending tasks" → lists incomplete tasks
- "mark buy groceries as done" → completes task, confirms
- "delete the old meeting" → removes task, confirms
- "change task 1 to call mom tonight" → updates task, confirms
- "what have I completed?" → lists completed tasks

**Edge Cases**:
- No tasks → "You don't have any tasks yet"
- Invalid task reference → "I couldn't find that task"
- Ambiguous reference → lists matches, asks for clarification
- Empty message → "What would you like to do?"

### Quality Validation

- ✅ 100% user isolation (automated tests)
- ✅ Stateless behavior (any request works independently)
- ✅ All 5 tools discoverable and used correctly
- ✅ Responses are natural, concise, confirmatory
- ✅ No hallucinations (data always from DB/tools)
- ✅ Conversation history persists across restarts
- ✅ Zero breaking changes to Phase I/II (existing tests pass)

## Implementation Phases

### Phase 1: Foundation (Database + MCP Tools)

**Deliverables**:
- Conversation and Message models
- Database migration
- MCP server setup
- 5 MCP tool implementations
- Tool unit tests

**Success Criteria**:
- All tools pass unit tests
- User isolation verified
- Tools discoverable via MCP

### Phase 2: Core Logic (Chat Endpoint + Agent)

**Deliverables**:
- Chat endpoint implementation
- Cohere agent setup
- System prompt configuration
- Conversation persistence logic
- Integration tests

**Success Criteria**:
- Chat endpoint responds correctly
- Agent calls appropriate tools
- Conversation history persists
- Stateless behavior verified

### Phase 3: Integration & Polish (Frontend + UX)

**Deliverables**:
- ChatKit integration
- Floating chat icon
- Frontend API client
- Friendly response formatting
- End-to-end tests

**Success Criteria**:
- Chat UI functional
- Authentication works
- Messages display correctly
- Existing UI unaffected

### Phase 4: Validation (Testing + Refinement)

**Deliverables**:
- Complete test suite
- Golden command validation
- Edge case handling
- Performance testing
- Documentation

**Success Criteria**:
- All acceptance tests pass
- Performance targets met
- Zero breaking changes
- Ready for deployment

## Risk Mitigation

### High Priority Risks

**Risk 1: Cohere API Reliability**
- Mitigation: Implement timeout handling (5s), retry logic (1 retry), friendly error messages
- Fallback: User can still use traditional UI if chat unavailable

**Risk 2: User Isolation Breach**
- Mitigation: Comprehensive testing, code review, automated security tests
- Validation: Test cross-user access attempts in every tool

**Risk 3: Breaking Existing Functionality**
- Mitigation: Run all Phase II tests before/after, avoid modifying existing code
- Validation: Existing test suite must pass 100%

### Medium Priority Risks

**Risk 4: Natural Language Ambiguity**
- Mitigation: Extensive testing with varied phrasings, clarification requests
- Monitoring: Log unhandled commands for improvement

**Risk 5: Conversation History Growth**
- Mitigation: Pagination (load last 50 messages), database indexing
- Monitoring: Track conversation sizes, optimize queries

**Risk 6: Concurrent User Scaling**
- Mitigation: Stateless design, load testing, horizontal scaling ready
- Validation: Test with 100+ concurrent users

## Next Steps

1. ✅ Complete this plan document
2. ⏭️ Execute Phase 0: Generate research.md
3. ⏭️ Execute Phase 1: Generate data-model.md, contracts/, quickstart.md
4. ⏭️ Run /sp.tasks to generate task breakdown
5. ⏭️ Begin implementation via /sp.implement

**Current Status**: Plan complete, ready for Phase 0 research.
