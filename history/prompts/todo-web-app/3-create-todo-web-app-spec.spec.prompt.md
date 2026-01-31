---
id: 3
title: Create Todo Web App Spec
stage: spec
date: 2026-01-24
surface: agent
model: claude-sonnet-4-5-20250929
feature: todo-web-app
branch: 002-todo-web-app
user: User
command: /sp.specify
labels: [spec, web-app, todo, authentication, crud]
links:
  spec: specs/002-todo-web-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/002-todo-web-app/spec.md
 - specs/002-todo-web-app/checklists/requirements.md
tests:
 - none
---

## Prompt

```
/sp.specify

Project: Hackathon II — Phase II Todo Web Application

────────────────────────────────────
TARGET OUTCOME
────────────────────────────────────

Build a production-ready multi-user Todo Web Application that replaces the Phase I CLI app with:

- Persistent cloud database storage
- Secure authentication using Better Auth
- REST API backend
- Responsive web frontend
- JWT-based authorization between frontend and backend

This phase establishes the foundation for AI chatbot and cloud-native deployment in later phases.

────────────────────────────────────
TARGET USERS
────────────────────────────────────

Primary Users:
- Individual authenticated users managing personal todo lists

User Capabilities:
- Create account
- Login/logout securely
- Manage private task list
- Perform CRUD operations
- Access app via browser

────────────────────────────────────
CORE FEATURES (REQUIRED)
────────────────────────────────────

1. Authentication System

User Stories:
- As a user, I can sign up using email and password
- As a user, I can log in securely
- As a user, I can remain logged in via session/JWT
- As a user, I can log out safely

Acceptance Criteria:
- Uses Better Auth official integration
- JWT tokens issued after login
- JWT attached to every backend API request
- Backend validates JWT signature
- Unauthorized requests return HTTP 401
- Each user only accesses their own data

────────────────────────────────────

2. Task CRUD Operations (Basic Level)

User Stories:
- As a user, I can create tasks
- As a user, I can view all my tasks
- As a user, I can update task details
- As a user, I can delete tasks
- As a user, I can mark tasks as complete or incomplete

Acceptance Criteria:

Create Task:
- Title is required
- Description optional
- Task linked to authenticated user
- Default completed = false

View Tasks:
- Only show authenticated user's tasks
- Display title, status, created date
- Paginated or scrollable list

Update Task:
- Allow editing title and description
- Only owner can update

Delete Task:
- Only owner can delete
- Task permanently removed

Toggle Complete:
- Allow marking completed/uncompleted
- Status updates instantly in UI

────────────────────────────────────
API REQUIREMENTS
────────────────────────────────────

All API routes must:

- Be protected by JWT authentication
- Reject unauthenticated requests
- Enforce user ownership on every operation

Required Endpoints:

GET    /api/{user_id}/tasks
POST   /api/{user_id}/tasks
GET    /api/{user_id}/tasks/{id}
PUT    /api/{user_id}/tasks/{id}
DELETE /api/{user_id}/tasks/{id}
PATCH  /api/{user_id}/tasks/{id}/complete

Acceptance Criteria:

- user_id in URL must match authenticated JWT user
- Token extracted from Authorization header
- Responses must be JSON formatted
- Proper HTTP status codes used

────────────────────────────────────
DATABASE REQUIREMENTS
────────────────────────────────────

Database: Neon Serverless PostgreSQL

Required Tables:

Tasks Table:

Fields:
- id (primary key)
- user_id (foreign key)
- title (string, required)
- description (text, optional)
- completed (boolean)
- created_at (timestamp)
- updated_at (timestamp)

Acceptance Criteria:

- Tasks linked to user accounts
- Indexed by user_id
- Automatic timestamps
- SQLModel ORM must be used

────────────────────────────────────
FRONTEND REQUIREMENTS
────────────────────────────────────

Framework:
- Next.js App Router
- TypeScript
- Tailwind CSS

UI Requirements:

Authentication UI:
- Signup page
- Login page
- Logout button
- Auth state persistence

Task UI:
- Add task form
- Task list display
- Edit task modal or inline edit
- Delete task button
- Complete toggle checkbox

UX Acceptance Criteria:

- Mobile responsive
- Loading states visible
- Error messages shown to user
- Protected routes redirect unauthenticated users

────────────────────────────────────
SECURITY REQUIREMENTS
────────────────────────────────────

Mandatory Rules:

- JWT token required on every backend request
- No public task endpoints
- Secrets stored in environment variables
- No credentials hardcoded
- Backend independently verifies token

────────────────────────────────────
PERFORMANCE BASELINE
────────────────────────────────────

- API response time < 500ms for basic CRUD
- Database queries indexed by user_id
- Frontend uses minimal blocking renders

────────────────────────────────────
INTEGRATION REQUIREMENTS
────────────────────────────────────

System Integration:

Frontend:
- Uses Better Auth client
- Attaches JWT token automatically
- Uses centralized API client

Backend:
- JWT verification middleware
- Extracts user identity
- Filters database queries by user

────────────────────────────────────
SUCCESS CRITERIA
────────────────────────────────────

Phase II is successful when:

- Users can sign up and login
- JWT authentication works end-to-end
- Users can perform all task CRUD operations
- Data persists in Neon database
- Multi-user isolation is enforced
- App deployed successfully on Vercel (frontend)
- Backend accessible via public API URL

────────────────────────────────────
OUT OF SCOPE (NOT BUILDING)
────────────────────────────────────

The following are explicitly excluded in Phase II:

- AI chatbot functionality (Phase III)
- Kubernetes deployment (Phase IV)
- Kafka and Dapr integration (Phase V)
- Recurring tasks
- Reminders and notifications
- Search and filtering
- Voice commands
- Multi-language chatbot

────────────────────────────────────
DELIVERY CONSTRAINTS
────────────────────────────────────

Development Rules:

- Must follow /sp.constitution
- No manual coding allowed
- Must use Claude Code generation
- Specs must be updated before feature changes
- Monorepo structure required

Format:

- Markdown specs
- Spec-Kit compatible
- Traceable to tasks and plans

Timeline:

- Must be completed within Phase II deadline window
```

## Response snapshot

Created a comprehensive specification for the Phase II Todo Web Application. The spec includes user stories for authentication and task management, detailed functional requirements covering the entire stack (frontend, backend, database, security), API endpoint specifications, and measurable success criteria. The specification follows the template structure with mandatory sections and defines clear boundaries for what is included and excluded in this phase. This establishes the foundation for the next phase of the Hackathon II project.

## Outcome

- ✅ Impact: Created complete specification for Todo Web Application Phase II
- 🧪 Tests: none
- 📁 Files: 2 files created (spec and checklist)
- 🔁 Next prompts: Proceed with planning the implementation
- 🧠 Reflection: Specification covers full stack requirements with clear scope boundaries

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementation planning