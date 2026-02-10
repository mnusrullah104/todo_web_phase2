---
id: 2
title: Update Phase III Constitution Standards
stage: constitution
date: 2026-02-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: User
command: /sp.constitution
labels: ["constitution", "phase3", "cohere-api", "mcp-tools", "agent-behavior"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A (constitution document)
---

## Prompt

```
# sp.constitution

Project: Phase III – Todo AI Chatbot Integration

## Core Principles

- Build **on top of** the existing full-stack Todo application (do not break or rewrite existing Task CRUD, authentication, database schema, or business logic)
- Deliver a **natural, reliable and friendly** conversational experience for todo management
- Enforce **strict user isolation** — every operation must belong only to the authenticated user
- Follow **stateless architecture** everywhere (chat endpoint + MCP tools)
- Prioritize **production-grade quality**: clean code, proper error handling, clear user feedback, graceful failure

## Key Standards

- Strictly follow the **Phase III specification** (MCP tools signatures, Agent Behavior, Chat API contract, database models, natural language command mapping)
- Use **Cohere API** (Cohere API key) as the primary LLM provider for the TodoChatAgent
- Implement **MCP Server** using the **Official MCP SDK** exposing exactly these 5 tools:
  - add_task
  - list_tasks
  - complete_task
  - delete_task
  - update_task
- Persist full conversation history in database using **Conversation** and **Message** models
- Integrate **OpenAI ChatKit** UI into the existing frontend
- Always:
  - confirm actions clearly and friendly
  - handle ambiguous requests intelligently (e.g. list tasks first when task is not clearly identified)
  - never hallucinate task data — always read from tools
  - return helpful, concise, natural-language responses

## Constraints

- Extend the **existing Phase 1 + Phase 2 backend** (FastAPI + SQLModel + Better Auth + Neon Serverless PostgreSQL)
- Use **Cohere** models / API key for all agent and tool-calling logic
- Follow **Agentic Dev Stack / SDD workflow strictly**:
  - Constitution → Specify → Clarify → Plan → Tasks → Implement (only via AI coding assistance — no manual coding)
- Chat endpoint and MCP tools must be **completely stateless**
- Always pass and enforce `user_id` (from auth) in every tool call and chat request

## Success Criteria

- User can **fully manage todos** via natural language: add, list (all/pending/completed), complete, delete, update
- Chatbot works **only for the currently logged-in user** (100% isolation)
- Conversation history survives server restarts and is correctly resumed
- All 5 MCP tools are correctly implemented, discoverable and used by the agent
- Agent selects correct tool(s) according to Phase III behavior specification
- Friendly confirmations and proper error messages are always shown
- Clean integration with existing Todo frontend + ChatKit UI
- Project satisfies **all deliverables and requirements** listed in the Phase III document
```

## Response snapshot

Updated constitution from version 1.0.0 to 1.1.0 with comprehensive Phase III standards:

**Added Sections:**
- Phase III Detailed Standards (new comprehensive section covering):
  - MCP Server Implementation requirements (Official MCP SDK, 5 tools, user isolation)
  - Agent Behavior Requirements (Cohere API, conversational style, tool orchestration)
  - Chat API Contract (stateless endpoint, JWT validation, conversation persistence)
  - Database Models (Conversation and Message models)
  - Frontend Integration (ChatKit UI integration)
- Phase III Specific Quality Gates (detailed completion criteria)

**Enhanced Sections:**
- Phase Consistency Rules: Expanded Phase III requirements with Cohere API mandate
- Engineering Standards: Added stateless architecture requirement
- Security Baseline: Emphasized strict user isolation
- Workflow Enforcement: Added explicit SDD workflow reference

**Key Changes:**
- Mandated Cohere API as primary LLM provider (not OpenAI)
- Specified exact 5 MCP tools with signatures
- Required conversation persistence in database
- Emphasized building on top of existing work without breaking functionality
- Added comprehensive quality gates for Phase III completion

## Outcome

- ✅ Impact: Constitution updated to v1.1.0 with comprehensive Phase III guidance
- 🧪 Tests: N/A (constitution is a governance document)
- 📁 Files: 1 file modified (.specify/memory/constitution.md)
- 🔁 Next prompts: Create Phase III feature specification using /sp.specify
- 🧠 Reflection: MINOR version bump appropriate - materially expanded Phase III guidance without changing core principles. Templates already aligned with constitution structure.

## Evaluation notes (flywheel)

- Failure modes observed: None - constitution update completed successfully
- Graders run and results (PASS/FAIL): Manual validation PASS (no unexplained placeholders, proper versioning, dates in ISO format)
- Prompt variant (if applicable): Standard constitution update workflow
- Next experiment (smallest change to try): Proceed with Phase III specification creation to validate constitution standards are actionable
