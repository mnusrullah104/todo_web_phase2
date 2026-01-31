<!-- SYNC IMPACT REPORT
Version change: N/A -> 1.0.0
Modified principles: None (new constitution)
Added sections: All sections from user input
Removed sections: Template placeholder sections
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated
  - .specify/templates/spec-template.md ✅ updated
  - .specify/templates/tasks-template.md ✅ updated
  - .specify/templates/commands/*.md ⚠ pending
Follow-up TODOs: None
-->

# Hackathon II — Evolution of Todo Constitution

## Core Principles

### I. Spec-First Development
No implementation may begin without a written specification. Specs are the single source of truth. Code must strictly follow specs. If behavior is unclear → update spec before coding.

### II. Zero Manual Coding Rule
Human must not write application code manually. All code must be generated via Claude Code or AI agents. Only specs, prompts, and architecture definitions may be written by human.

### III. Phase Isolation Principle
Each phase must only implement features allowed by that phase. No future-phase features allowed prematurely. Backward compatibility must be preserved.

### IV. Deterministic Architecture
Same spec must always produce same behavior. Avoid ambiguous logic. Prefer explicit contracts over assumptions.

### V. AI-Native Design
Treat AI agents as first-class system components. MCP tools, Agents SDK, and ChatKit must be treated as production interfaces. Agent behavior must be governed by written rules.

### VI. Cloud-Native Readiness
Every service must be container-ready. Stateless services preferred. Externalize configuration via environment variables. Design for horizontal scalability.

## Engineering Standards

### I. Code Quality
Follow clean architecture principles. Separation of concerns is mandatory. Modular folder structure required. No hardcoded secrets.

### II. API Design
REST endpoints must be predictable and consistent. Use proper HTTP status codes. All protected endpoints require authentication. User isolation is mandatory.

### III. Database Discipline
Every schema change must be documented in specs. Migrations must be reproducible. No direct DB logic inside UI layer.

### IV. Security Baseline
JWT authentication required from Phase II onward. Secrets stored in environment variables. No tokens in frontend localStorage without encryption. Backend must verify identity independently.

### V. Observability Ready
All services must log important actions. Errors must be human readable. Phase IV+ must support monitoring hooks.

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

Skipping steps is not allowed.

## Phase Consistency Rules

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

## Quality Gates

A phase is considered COMPLETE only when:

- All specs implemented
- All acceptance criteria satisfied
- No manual code present
- Authentication works correctly (Phase II+)
- Agent tools function correctly (Phase III+)
- Deployment reproducible (Phase IV+)
- Events flow correctly (Phase V)

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

This constitution applies globally to ALL phases.

## Governance

When generating code:

- Prefer correctness over speed
- Reject ambiguous instructions
- Ask for spec clarification if required
- Never invent missing requirements
- Never bypass architecture rules

**Version**: 1.0.0 | **Ratified**: 2026-01-24 | **Last Amended**: 2026-01-24