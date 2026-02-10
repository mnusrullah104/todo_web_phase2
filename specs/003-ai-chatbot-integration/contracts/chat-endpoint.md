# API Contract: Chat Endpoint

**Feature**: AI Chatbot Integration for Todo Management
**Date**: 2026-02-09
**Status**: Design
**Related Documents**: [spec.md](../spec.md), [plan.md](../plan.md), [data-model.md](../data-model.md)

## Overview

The chat endpoint provides a stateless, conversational interface for todo management. Users send natural language messages, and the AI assistant responds with task operations and friendly confirmations.

## Endpoint Specification

### POST /api/{user_id}/chat

Send a message to the AI assistant and receive a response.

**Path Parameters:**
- `user_id` (string, UUID): The authenticated user's ID

**Authentication:**
- Required: JWT Bearer token in Authorization header
- Token must contain valid user_id matching path parameter

**Request Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "message": "string (required, 1-2000 chars)",
  "conversation_id": "string (optional, UUID)"
}
```

**Response Status Codes:**
- `200 OK`: Message processed successfully
- `400 Bad Request`: Invalid request format or parameters
- `401 Unauthorized`: Missing or invalid JWT token
- `403 Forbidden`: user_id mismatch with authenticated user
- `404 Not Found`: Conversation not found
- `422 Unprocessable Entity`: Validation error
- `503 Service Unavailable`: AI service temporarily unavailable

**Success Response (200 OK):**
```json
{
  "conversation_id": "string (UUID)",
  "response": "string",
  "tool_calls": [
    {
      "tool": "string",
      "arguments": {}
    }
  ],
  "timestamp": "string (ISO 8601)"
}
```

**Error Response:**
```json
{
  "detail": "string (error message)"
}
```

## Request Schema

### ChatRequest

```typescript
interface ChatRequest {
  message: string;           // User's message (1-2000 chars)
  conversation_id?: string;  // Optional conversation UUID
}
```

**Field Constraints:**
- `message`: Required, non-empty, max 2000 characters
- `conversation_id`: Optional, must be valid UUID if provided

**Validation Rules:**
1. Message cannot be empty or whitespace-only
2. Message length must be between 1 and 2000 characters
3. If conversation_id provided, must be valid UUID format
4. If conversation_id provided, must belong to authenticated user

## Response Schema

### ChatResponse

```typescript
interface ChatResponse {
  conversation_id: string;   // UUID of the conversation
  response: string;          // AI assistant's response
  tool_calls: ToolCall[];    // Tools executed (may be empty)
  timestamp: string;         // ISO 8601 timestamp
}

interface ToolCall {
  tool: string;              // Tool name (e.g., "add_task")
  arguments: Record<string, any>;  // Tool arguments
}
```

**Field Descriptions:**
- `conversation_id`: UUID of the conversation (created if not provided in request)
- `response`: Natural language response from AI assistant
- `tool_calls`: Array of tools executed during this turn (empty if no tools used)
- `timestamp`: UTC timestamp when response was generated

## Authentication & Authorization

### JWT Token Requirements

The endpoint requires a valid JWT token issued by Better Auth:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Token Claims:**
- `user_id`: UUID of the authenticated user
- `exp`: Token expiration timestamp
- `iat`: Token issued at timestamp

### Authorization Flow

1. Extract JWT from Authorization header
2. Validate token signature and expiration
3. Extract user_id from token claims
4. Compare token user_id with path parameter user_id
5. Reject request if mismatch (403 Forbidden)

### Security Requirements

- All requests MUST include valid JWT token
- Path user_id MUST match token user_id
- Conversation access MUST be validated (user owns conversation)
- Tool execution MUST enforce user_id scoping
- No cross-user data access permitted

## Request Examples

### Example 1: New Conversation - Add Task

**Request:**
```http
POST /api/123e4567-e89b-12d3-a456-426614174000/chat HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "message": "Add a task to buy groceries"
}
```

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "response": "I've added 'buy groceries' to your task list.",
  "tool_calls": [
    {
      "tool": "add_task",
      "arguments": {
        "title": "buy groceries",
        "description": "",
        "completed": false
      }
    }
  ],
  "timestamp": "2026-02-09T10:30:00Z"
}
```

### Example 2: Continue Conversation - List Tasks

**Request:**
```http
POST /api/123e4567-e89b-12d3-a456-426614174000/chat HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "message": "What's on my list?",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "response": "You have 3 tasks:\n1. buy groceries (pending)\n2. call dentist (pending)\n3. finish report (completed)",
  "tool_calls": [
    {
      "tool": "list_tasks",
      "arguments": {}
    }
  ],
  "timestamp": "2026-02-09T10:31:00Z"
}
```

### Example 3: Multi-Tool Operation

**Request:**
```http
POST /api/123e4567-e89b-12d3-a456-426614174000/chat HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "message": "Add a task to call dentist and mark buy groceries as done",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "response": "Done! I've added 'call dentist' to your list and marked 'buy groceries' as complete.",
  "tool_calls": [
    {
      "tool": "add_task",
      "arguments": {
        "title": "call dentist",
        "description": "",
        "completed": false
      }
    },
    {
      "tool": "complete_task",
      "arguments": {
        "task_id": "660e8400-e29b-41d4-a716-446655440001"
      }
    }
  ],
  "timestamp": "2026-02-09T10:32:00Z"
}
```

### Example 4: Ambiguous Request - Clarification

**Request:**
```http
POST /api/123e4567-e89b-12d3-a456-426614174000/chat HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "message": "Delete the report task",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response (Multiple Matches):**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "response": "I found 3 tasks with 'report' in the title:\n1. finish report (completed)\n2. submit report (pending)\n3. review report draft (pending)\n\nWhich one would you like to delete?",
  "tool_calls": [
    {
      "tool": "list_tasks",
      "arguments": {}
    }
  ],
  "timestamp": "2026-02-09T10:33:00Z"
}
```

## Error Examples

### Error 1: Missing JWT Token

**Request:**
```http
POST /api/123e4567-e89b-12d3-a456-426614174000/chat HTTP/1.1
Host: api.example.com
Content-Type: application/json

{
  "message": "Add a task"
}
```

**Response:**
```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "detail": "Not authenticated"
}
```

### Error 2: User ID Mismatch

**Request:**
```http
POST /api/999e9999-e99b-99d9-a999-999999999999/chat HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "message": "Add a task"
}
```

**Response:**
```http
HTTP/1.1 403 Forbidden
Content-Type: application/json

{
  "detail": "Not authorized to access this user's chat"
}
```

### Error 3: Invalid Conversation ID

**Request:**
```http
POST /api/123e4567-e89b-12d3-a456-426614174000/chat HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "message": "What's on my list?",
  "conversation_id": "invalid-uuid"
}
```

**Response:**
```http
HTTP/1.1 422 Unprocessable Entity
Content-Type: application/json

{
  "detail": [
    {
      "loc": ["body", "conversation_id"],
      "msg": "value is not a valid uuid",
      "type": "type_error.uuid"
    }
  ]
}
```

### Error 4: Conversation Not Found

**Request:**
```http
POST /api/123e4567-e89b-12d3-a456-426614174000/chat HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "message": "What's on my list?",
  "conversation_id": "999e9999-e99b-99d9-a999-999999999999"
}
```

**Response:**
```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{
  "detail": "Conversation not found"
}
```

### Error 5: Message Too Long

**Request:**
```http
POST /api/123e4567-e89b-12d3-a456-426614174000/chat HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "message": "Lorem ipsum dolor sit amet... [2001 characters]"
}
```

**Response:**
```http
HTTP/1.1 422 Unprocessable Entity
Content-Type: application/json

{
  "detail": [
    {
      "loc": ["body", "message"],
      "msg": "ensure this value has at most 2000 characters",
      "type": "value_error.any_str.max_length",
      "ctx": {"limit_value": 2000}
    }
  ]
}
```

### Error 6: AI Service Unavailable

**Request:**
```http
POST /api/123e4567-e89b-12d3-a456-426614174000/chat HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "message": "Add a task"
}
```

**Response:**
```http
HTTP/1.1 503 Service Unavailable
Content-Type: application/json

{
  "detail": "AI service temporarily unavailable. Please try again in a moment."
}
```

## Stateless Design

### No Server-Side Session State

The endpoint is completely stateless:
- No session storage on server
- All conversation context loaded from database on each request
- No in-memory conversation state
- Horizontal scaling supported

### Request Processing Flow

1. **Authenticate**: Validate JWT and extract user_id
2. **Authorize**: Verify user_id matches path parameter
3. **Load Context**: Retrieve conversation history from database
4. **Process**: Send message + history to Cohere agent
5. **Execute Tools**: Run tool calls with user_id scoping
6. **Persist**: Save user message and assistant response to database
7. **Respond**: Return assistant response to client

### Conversation History Management

- History loaded from database on each request
- Recent 50 messages included in context by default
- Older messages available via pagination (future enhancement)
- No conversation state cached on server

## Performance Characteristics

### Expected Response Times

- **Simple query (no tools)**: 1-3 seconds
- **Single tool call**: 2-4 seconds
- **Multiple tool calls**: 3-5 seconds
- **Conversation history load**: <200ms

### Rate Limiting

- Per user: 60 requests/minute
- Per IP: 100 requests/minute
- Burst: 10 requests/second

### Timeout Configuration

- Request timeout: 30 seconds
- Cohere API timeout: 10 seconds
- Database query timeout: 5 seconds

## Idempotency

The chat endpoint is **NOT idempotent**:
- Each request creates new messages in the database
- Duplicate requests will create duplicate messages
- Clients should implement retry logic with exponential backoff
- Consider adding idempotency keys in future enhancement

## Versioning

**Current Version**: v1

**API Path**: `/api/{user_id}/chat`

**Future Versioning Strategy**:
- Breaking changes: New version path (e.g., `/api/v2/{user_id}/chat`)
- Non-breaking changes: Same path, backward compatible
- Deprecation: 6-month notice period

## Testing Checklist

### Functional Tests
- [ ] Create new conversation with first message
- [ ] Continue existing conversation
- [ ] Handle multiple tool calls in single turn
- [ ] Handle ambiguous requests (clarification)
- [ ] Handle tool execution errors gracefully
- [ ] Validate conversation history persistence

### Security Tests
- [ ] Reject requests without JWT token
- [ ] Reject requests with invalid JWT token
- [ ] Reject requests with expired JWT token
- [ ] Reject requests with user_id mismatch
- [ ] Prevent access to other users' conversations
- [ ] Validate tool execution enforces user_id

### Error Handling Tests
- [ ] Invalid request format (400)
- [ ] Missing authentication (401)
- [ ] Forbidden access (403)
- [ ] Conversation not found (404)
- [ ] Validation errors (422)
- [ ] AI service unavailable (503)

### Performance Tests
- [ ] Response time under load (100 concurrent users)
- [ ] Database query performance (<200ms)
- [ ] Conversation history loading (50 messages)
- [ ] Rate limiting enforcement

## Related Documents

- [spec.md](../spec.md) - Feature requirements (FR-001 to FR-042)
- [plan.md](../plan.md) - Architecture decisions
- [data-model.md](../data-model.md) - Database schema
- [tool-contracts.md](tool-contracts.md) - MCP tool specifications
