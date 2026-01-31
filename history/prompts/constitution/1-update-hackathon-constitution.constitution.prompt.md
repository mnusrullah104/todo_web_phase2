---
id: 1
title: Update Hackathon Constitution
stage: constitution
date: 2026-01-24
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: User
command: /sp.constitution
labels: [constitution, governance, hackathon]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```
/sp.constitution

Project: Hackathon II — Evolution of Todo (Spec-Driven AI-Native Development)

Mission:
Build a production-grade Todo platform that evolves from CLI to Web, AI Chatbot, Kubernetes deployment, and Cloud-native distributed system using Spec-Driven Development and Agentic workflows — without manual coding.

────────────────────────────────────
CORE PRINCIPLES
────────────────────────────────────

1. Spec-First Development
- No implementation may begin without a written specification.
- Specs are the single source of truth.
- Code must strictly follow specs.
- If behavior is unclear → update spec before coding.

2. Zero Manual Coding Rule
- Human must not write application code manually.
- All code must be generated via Claude Code or AI agents.
- Only specs, prompts, and architecture definitions may be written by human.

3. Phase Isolation Principle
- Each phase must only implement features allowed by that phase.
- No future-phase features allowed prematurely.
- Backward compatibility must be preserved.

4. Deterministic Architecture
- Same spec must always produce same behavior.
- Avoid ambiguous logic.
- Prefer explicit contracts over assumptions.

5. AI-Native Design
- Treat AI agents as first-class system components.
- MCP tools, Agents SDK, and ChatKit must be treated as production interfaces.
- Agent behavior must be governed by written rules.

6. Cloud-Native Readiness
- Every service must be container-ready.
- Stateless services preferred.
- Externalize configuration via environment variables.
- Design for horizontal scalability.

────────────────────────────────────
ENGINEERING STANDARDS
────────────────────────────────────

1. Code Quality
- Follow clean architecture principles.
- Separation of concerns is mandatory.
- Modular folder structure required.
- No hardcoded secrets.

2. API Design
- REST endpoints must be predictable and consistent.
- Use proper HTTP status codes.
- All protected endpoints require authentication.
- User isolation is mandatory.

3. Database Discipline
- Every schema change must be documented in specs.
- Migrations must be reproducible.
- No direct DB logic inside UI layer.

4. Security Baseline
- JWT authentication required from Phase II onward.
- Secrets stored in environment variables.
- No tokens in frontend localStorage without encryption.
- Backend must verify identity independently.

5. Observability Ready
- All services must log important actions.
- Errors must be human readable.
- Phase IV+ must support monitoring hooks.

────────────────────────────────────
SPEC STRUCTURE RULES
────────────────────────────────────

Every feature spec MUST include:

- Purpose
- User Stories
- Functional Requirements
- Acceptance Criteria
- Edge Cases
- API Contracts (if applicable)
- Data Model Impact
- Error Handling Behavior

────────────────────────────────────
WORKFLOW ENFORCEMENT
────────────────────────────────────

Mandatory Workflow:

1. Write or update spec
2. Validate spec completeness
3. Generate plan from spec
4. Break into implementation tasks
5. Generate code via Claude Code
6. Test behavior
7. Iterate spec if mismatch found

Skipping steps is not allowed.

────────────────────────────────────
PHASE CONSISTENCY RULES
────────────────────────────────────

Phase I (CLI):
- In-memory only
- No database
- No auth
- No network calls

Phase II (Web):
- Persistent database
- REST APIs
- Better Auth JWT integration
- Multi-user isolation

Phase III (AI Chatbot):
- MCP tools only for task actions
- Stateless server
- Conversation persistence
- Agent controlled via tool contracts

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

────────────────────────────────────
QUALITY GATES
────────────────────────────────────

A phase is considered COMPLETE only when:

- All specs implemented
- All acceptance criteria satisfied
- No manual code present
- Authentication works correctly (Phase II+)
- Agent tools function correctly (Phase III+)
- Deployment reproducible (Phase IV+)
- Events flow correctly (Phase V)

────────────────────────────────────
SUCCESS CRITERIA
────────────────────────────────────

Final project must:

- Fully follow spec-driven methodology
- Pass functional testing
- Be deployable end-to-end
- Demonstrate AI-native architecture
- Meet hackathon rubric requirements
- Be production-architecture aligned

────────────────────────────────────
ENFORCEMENT MODE
────────────────────────────────────

When generating code:

- Prefer correctness over speed
- Reject ambiguous instructions
- Ask for spec clarification if required
- Never invent missing requirements
- Never bypass architecture rules

This constitution applies globally to ALL phases.
```

## Response snapshot

Updated the project constitution file (.specify/memory/constitution.md) with the comprehensive constitution document provided by the user. The new constitution includes core principles, engineering standards, spec structure rules, workflow enforcement, phase consistency rules, quality gates, success criteria, and enforcement mode guidelines for the Hackathon II project. The constitution establishes a foundation for spec-driven, AI-native development with cloud-native readiness.

## Outcome

- ✅ Impact: Updated project constitution with comprehensive governance framework
- 🧪 Tests: none
- 📁 Files: 1 file updated (.specify/memory/constitution.md)
- 🔁 Next prompts: Continue with feature specification and planning
- 🧠 Reflection: Constitution now provides clear governance framework for the entire project lifecycle

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin feature specification following constitution guidelines