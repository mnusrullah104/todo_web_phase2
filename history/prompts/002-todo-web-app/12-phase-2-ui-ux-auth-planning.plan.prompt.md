---
id: 12
title: Phase 2 UI/UX Auth Planning
stage: plan
date: 2026-01-29
surface: agent
model: claude-sonnet-4-5
feature: 002-todo-web-app
branch: 001-ai-k12-efficiency
user: system
command: /sp.plan phase-2-ui-ux-auth
labels: ["planning", "ui-ux", "authentication", "database", "phase-2"]
links:
  spec: specs/002-todo-web-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-todo-web-app/plan-phase2-uiux.md
  - specs/002-todo-web-app/research-phase2.md
  - specs/002-todo-web-app/data-model-phase2.md
  - specs/002-todo-web-app/quickstart-phase2.md
  - specs/002-todo-web-app/contracts/api-spec.yaml
  - specs/002-todo-web-app/PLANNING_SUMMARY.md
tests:
  - None (planning phase - no tests executed)
---

## Prompt

User provided authoritative Phase 2 specification for Todo SaaS application:

**Core Requirements:**
- Clean, spacious, evaluation-ready UI (Linear/Asana style)
- One primary purpose per page
- 4 required pages: Auth, Dashboard, Create/Edit Task, Profile/Settings
- User signs up ONLY ONCE - data stored in Neon PostgreSQL
- User signs in with SAME credentials (no re-signup)
- Auth state must persist across refresh
- All tasks stored in Neon DB and scoped to logged-in user
- Production-grade SaaS polish with subtle animations (120-180ms)
- Mobile-first responsive design with FAB

**Critical Rules:**
- Do NOT mix dashboard + create task
- Do NOT show auth after login
- Do NOT use navbar-only navigation
- Do NOT use in-memory / fake storage

**User Request:** "Option A" - Create detailed architectural plan following Specify methodology

## Response snapshot

**Planning Workflow Executed:**

**Phase 0: Research & Discovery** ✅
- Researched database initialization patterns (Alembic vs SQLModel.metadata.create_all)
- Decision: Use SQLModel.metadata.create_all() for Phase 2 simplicity
- Evaluated auth state persistence strategies (localStorage vs cookies vs hybrid)
- Decision: localStorage + token validation on mount
- Studied UI/UX patterns for clean, spacious design (Linear/Asana analysis)
- Decision: 4-page structure with clear separation of concerns
- Analyzed task management flow (modal vs full page vs inline)
- Decision: Dedicated full pages for create/edit (better mobile experience)

**Phase 1: Design & Contracts** ✅
- Created comprehensive data model with User and Task entities
- Specified database schema with proper indexes and constraints
- Documented 7 common data access patterns
- Generated OpenAPI 3.0.3 specification for all API endpoints
- Created quickstart guide with setup instructions and troubleshooting

**Critical Issues Identified:**
1. Backend tasks API uses mock storage (mock_tasks_db) instead of database
2. User model exists but not integrated with database operations
3. No database initialization script for table creation
4. Frontend has too many pages causing congestion
5. Dashboard mixes multiple concerns (violates "one purpose per page")
6. No dedicated Create/Edit Task page
7. Auth state may not persist properly across refresh

**Architecture Decisions:**
1. Database Initialization: SQLModel.metadata.create_all() in init_db.py
2. Task Create/Edit UI: Dedicated full pages (/tasks/new, /tasks/[id])
3. Auth Persistence: localStorage + token validation on mount
4. Page Structure: Simplify to 4 core pages, remove congestion

**Artifacts Generated:**
1. plan-phase2-uiux.md - Comprehensive implementation plan
2. research-phase2.md - Research findings and decisions
3. data-model-phase2.md - Data model specification
4. quickstart-phase2.md - Setup and verification guide
5. contracts/api-spec.yaml - OpenAPI specification
6. PLANNING_SUMMARY.md - Planning summary report

**Implementation Roadmap:**
- Phase 0: Research ✅ Complete
- Phase 1: Design & Contracts ✅ Complete
- Phase 2: Core Implementation (Next) - 8-12 tasks estimated
- Phase 3: Integration & Testing (After Phase 2)

## Outcome

- ✅ Impact: Comprehensive architectural plan created for Phase 2 redesign with clear implementation roadmap
- 🧪 Tests: No tests executed (planning phase)
- 📁 Files: 6 planning artifacts created (plan, research, data model, quickstart, API contracts, summary)
- 🔁 Next prompts: Run `/sp.tasks` to generate implementation tasks from plan
- 🧠 Reflection: Successfully identified critical issues (mock storage, UI congestion) and provided clear solutions with architectural decisions and rationale

## Evaluation notes (flywheel)

- Failure modes observed: None - planning workflow completed successfully
- Graders run and results (PASS/FAIL): N/A (planning phase)
- Prompt variant (if applicable): Standard /sp.plan workflow
- Next experiment (smallest change to try): Execute /sp.tasks to generate actionable implementation tasks
