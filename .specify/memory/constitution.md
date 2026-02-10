<!-- SYNC IMPACT REPORT
Version change: 1.0.0 -> 1.1.0
Modified principles: None (principles unchanged)
Added sections:
  - Phase III Detailed Standards (new comprehensive section)
  - Enhanced Phase III requirements in Phase Consistency Rules
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ already aligned
  - .specify/templates/spec-template.md ✅ already aligned
  - .specify/templates/tasks-template.md ✅ already aligned
  - .specify/templates/commands/*.md ⚠ review for Phase III references
Follow-up TODOs: None
Rationale: MINOR bump - materially expanded Phase III guidance with Cohere API requirement,
detailed MCP tool specifications, agent behavior standards, and success criteria.
-->

# Hackathon II — Evolution of Todo Constitution

## Core Principles

### I. Spec-First Development
No implementation may begin without a written specification. Specs are the single source of
truth. Code must strictly follow specs. If behavior is unclear → update spec before coding.

### II. Zero Manual Coding Rule
Human must not write application code manually. All code must be generated via Claude Code or
AI agents. Only specs, prompts, and architecture definitions may be written by human.

### III. Phase Isolation Principle
Each phase must only implement features allowed by that phase. No future-phase features
allowed prematurely. Backward compatibility must be preserved. Build on top of existing work
without breaking prior functionality.

### IV. Deterministic Architecture
Same spec must always produce same behavior. Avoid ambiguous logic. Prefer explicit contracts
over assumptions.

### V. AI-Native Design
Treat AI agents as first-class system components. MCP tools, Agents SDK, and ChatKit must be
treated as production interfaces. Agent behavior must be governed by written rules.

### VI. Cloud-Native Readiness
Every service must be container-ready. Stateless services preferred. Externalize configuration
via environment variables. Design for horizontal scalability.

## Engineering Standards

### I. Code Quality
Follow clean architecture principles. Separation of concerns is mandatory. Modular folder
structure required. No hardcoded secrets. Production-grade quality: clean code, proper error
handling, clear user feedback, graceful failure.

### II. API Design
REST endpoints must be predictable and consistent. Use proper HTTP status codes. All protected
endpoints require authentication. User isolation is mandatory. Stateless architecture required
for all endpoints.

### III. Database Discipline
Every schema change must be documented in specs. Migrations must be reproducible. No direct DB
logic inside UI layer.

### IV. Security Baseline
JWT authentication required from Phase II onward. Secrets stored in environment variables. No
tokens in frontend localStorage without encryption. Backend must verify identity independently.
Strict user isolation — every operation must belong only to the authenticated user.

### V. Observability Ready
All services must log important actions. Errors must be human readable. Phase IV+ must support
monitoring hooks.

## Spec Structure Rules

Every feature spec MUST include:

- Purpose
- User Stories
- Functional Requirements
- Acceptance Criteria
- Edge Cases
- API Contracts (if applicable)
- Data Model Impact
- Error Handling Behavior

## Workflow Enforcement

Mandatory Workflow:

1. Write or update spec
2. Validate spec completeness
3. Generate plan from spec
4. Break into implementation tasks
5. Generate code via Claude Code
6. Test behavior
7. Iterate spec if mismatch found

Skipping steps is not allowed. Follow Agentic Dev Stack / SDD workflow strictly:
Constitution → Specify → Clarify → Plan → Tasks → Implement (only via AI coding assistance).

## Phase Consistency Rules

Phase I (CLI):
- In-memory only
- No database
- No auth
- No network calls

Phase II (Web):
- Persistent database (Neon Serverless PostgreSQL)
- REST APIs (FastAPI + SQLModel)
- Better Auth JWT integration
- Multi-user isolation

Phase III (AI Chatbot):
- Build on top of existing Phase I + Phase II work (do not break or rewrite existing Task
  CRUD, authentication, database schema, or business logic)
- MCP tools only for task actions (5 tools: add_task, list_tasks, complete_task, delete_task,
  update_task)
- Stateless server (chat endpoint and MCP tools completely stateless)
- Conversation persistence (full history in database using Conversation and Message models)
- Agent controlled via tool contracts
- Use Cohere API as primary LLM provider for TodoChatAgent
- Integrate OpenAI ChatKit UI into existing frontend
- Always pass and enforce user_id (from auth) in every tool call and chat request

Phase IV (Kubernetes):
- Dockerized services
- Helm charts
- Minikube deployment
- AI-assisted DevOps allowed

Phase V (Cloud + Kafka):
- Event-driven architecture
- Dapr integration
- Kafka-based messaging
- Cloud deployment with CI/CD

## Phase III Detailed Standards

### MCP Server Implementation
- MUST use Official MCP SDK
- MUST expose exactly 5 tools with precise signatures per Phase III specification:
  - add_task: Create new tasks
  - list_tasks: View all tasks or filter by completion status
  - complete_task: Mark tasks as complete or incomplete
  - delete_task: Remove tasks permanently
  - update_task: Modify task title, description, or status
- All tools MUST accept user_id parameter
- All tools MUST enforce user isolation (filter by user_id in database queries)
- All tools MUST be stateless (no server-side session state)
- All tools MUST interact with SQLModel database

### Agent Behavior Requirements
- MUST use Cohere API (Cohere API key) for all LLM operations
- MUST deliver natural, reliable, and friendly conversational experience
- MUST confirm actions clearly and friendly
- MUST handle ambiguous requests intelligently (e.g., list tasks first when task is not
  clearly identified)
- MUST NEVER hallucinate task data — always read from MCP tools
- MUST return helpful, concise, natural-language responses
- MUST interpret natural language flexibly (various phrasings for same intent)
- MUST support multi-tool orchestration in single turn when appropriate

### Chat API Contract
- Endpoint: POST /api/{user_id}/chat
- MUST be completely stateless
- MUST validate user_id matches authenticated user (JWT)
- MUST persist conversation history to database
- MUST load conversation history from database on each request
- MUST pass user_id to all MCP tool calls
- MUST enforce strict user isolation

### Database Models
- MUST implement Conversation model (links to user, tracks conversation metadata)
- MUST implement Message model (stores individual messages with role, content, timestamps)
- MUST preserve conversation history across server restarts
- MUST support conversation resumption

### Frontend Integration
- MUST integrate OpenAI ChatKit UI into existing Todo frontend
- MUST maintain existing Task CRUD UI functionality
- MUST provide seamless user experience between traditional UI and chat interface
- MUST handle authentication state correctly

## Quality Gates

A phase is considered COMPLETE only when:

- All specs implemented
- All acceptance criteria satisfied
- No manual code present
- Authentication works correctly (Phase II+)
- Agent tools function correctly (Phase III+)
- Deployment reproducible (Phase IV+)
- Events flow correctly (Phase V)

### Phase III Specific Quality Gates

Phase III is complete when:

- User can fully manage todos via natural language: add, list (all/pending/completed),
  complete, delete, update
- Chatbot works only for the currently logged-in user (100% isolation verified)
- Conversation history survives server restarts and is correctly resumed
- All 5 MCP tools are correctly implemented, discoverable, and used by the agent
- Agent selects correct tool(s) according to Phase III behavior specification
- Friendly confirmations and proper error messages are always shown
- Clean integration with existing Todo frontend + ChatKit UI
- Project satisfies all deliverables and requirements listed in Phase III specification
- No existing Phase I or Phase II functionality is broken

## Success Criteria

Final project must:

- Fully follow spec-driven methodology
- Pass functional testing
- Be deployable end-to-end
- Demonstrate AI-native architecture
- Meet hackathon rubric requirements
- Be production-architecture aligned

## Enforcement Mode

When generating code:

- Prefer correctness over speed
- Reject ambiguous instructions
- Ask for spec clarification if required
- Never invent missing requirements
- Never bypass architecture rules
- Always enforce user isolation
- Always validate against specifications

This constitution applies globally to ALL phases.

## Governance

### Amendment Procedure
Constitution changes require:
1. Clear rationale for change
2. Version bump following semantic versioning
3. Sync impact report documenting affected templates
4. Update to dependent artifacts (templates, commands)

### Versioning Policy
- MAJOR: Backward incompatible governance/principle removals or redefinitions
- MINOR: New principle/section added or materially expanded guidance
- PATCH: Clarifications, wording, typo fixes, non-semantic refinements

### Compliance Review
All feature implementations must be validated against current constitution version.
Violations must be corrected before phase completion.

**Version**: 1.1.0 | **Ratified**: 2026-01-24 | **Last Amended**: 2026-02-09
