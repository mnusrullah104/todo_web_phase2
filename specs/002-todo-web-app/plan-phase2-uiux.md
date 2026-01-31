# Implementation Plan: Todo SaaS - Phase 2 UI/UX + Auth Redesign

**Branch**: `001-ai-k12-efficiency` | **Date**: 2026-01-29 | **Spec**: Phase 2 Authoritative UI/UX Specification
**Input**: Authoritative Phase 2 UI/UX + Auth requirements (overrides previous UI specs)

## Summary

Redesign and implement a production-grade Todo SaaS application with clean, spacious UI (Linear/Asana style), proper Neon PostgreSQL persistence, and correct authentication flow. This plan addresses critical issues in the current implementation:
- Replace mock storage with actual database operations
- Implement proper User model and database schema
- Create 4 distinct, non-congested pages with clear separation of concerns
- Ensure auth state persistence across refresh
- Deliver evaluation-ready SaaS polish

## Technical Context

**Language/Version**: Python 3.13+ (Backend), TypeScript 5.x (Frontend)
**Primary Dependencies**: FastAPI, Next.js 14+ App Router, SQLModel, Neon PostgreSQL, JWT (python-jose)
**Storage**: Neon Serverless PostgreSQL (already configured in .env)
**Testing**: pytest (Backend), manual testing (Frontend)
**Target Platform**: Web (Browser) - Desktop and Mobile responsive
**Project Type**: Web application (frontend + backend)
**Performance Goals**: API response time < 500ms, smooth animations (120-180ms)
**Constraints**:
- Clean, non-congested UI (one primary purpose per page)
- Auth state must persist across refresh
- User signs up once, logs in with same credentials
- All tasks stored in Neon DB, scoped to logged-in user
**Scale/Scope**: Multi-user SaaS with individual task lists

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Spec-first development: Authoritative Phase 2 spec provided
- ✅ Zero manual coding rule: Will use Claude Code for all implementation
- ✅ Phase isolation: Focusing only on Phase II requirements (web app, auth, CRUD, UI/UX)
- ✅ Deterministic architecture: Following clear UI/UX requirements
- ✅ AI-native design: Preparing for Phase III AI integration
- ✅ Cloud-native readiness: Using Neon PostgreSQL, environment-based config

## Current State Analysis

### Existing Implementation Issues

**Backend Issues:**
1. **CRITICAL**: Tasks API uses mock storage (`mock_tasks_db`) instead of database (backend/src/api/tasks.py:14-16)
2. User model exists but not integrated with database operations
3. Auth endpoints work but user data not properly persisted/retrieved
4. No database initialization script for tables

**Frontend Issues:**
1. Too many pages (analytics, evaluations) - creates congestion
2. Dashboard mixes multiple concerns (stats + actions + recent activity)
3. No dedicated Create/Edit Task page (uses /tasks/new)
4. Auth state may not persist properly across refresh
5. Landing page shows auth links even when authenticated

**Database Issues:**
1. User table not created in database
2. Task table not created in database
3. No migration or initialization process
4. SQLModel models defined but not synced to database

## Project Structure

### Documentation (this feature)

```text
specs/002-todo-web-app/
├── plan-phase2-uiux.md  # This file (Phase 2 redesign plan)
├── spec.md              # Original Phase II spec
├── research.md          # Phase 0 research output
├── data-model.md        # Phase 1 data model (needs update)
├── quickstart.md        # Phase 1 quickstart
└── contracts/           # API contracts
```

### Source Code (repository root)

```text
hackathon_2/
├── backend/
│   ├── src/
│   │   ├── main.py                    # FastAPI app entry point
│   │   ├── models/
│   │   │   ├── user.py                # User SQLModel (EXISTS, needs DB sync)
│   │   │   └── task.py                # Task SQLModel (EXISTS, needs DB sync)
│   │   ├── api/
│   │   │   ├── auth.py                # Auth endpoints (EXISTS, working)
│   │   │   └── tasks.py               # Task CRUD (EXISTS, uses MOCK storage - FIX)
│   │   ├── auth/
│   │   │   └── jwt.py                 # JWT utilities (EXISTS, working)
│   │   ├── database/
│   │   │   └── session.py             # DB session (EXISTS, working)
│   │   └── config/
│   │       └── settings.py            # Settings (EXISTS, working)
│   ├── init_db.py                     # DB initialization (EXISTS, needs enhancement)
│   └── requirements.txt               # Dependencies (EXISTS)
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx               # Landing page (REDESIGN - hide auth when logged in)
│   │   │   ├── login/page.tsx         # Login page (EXISTS, keep)
│   │   │   ├── signup/page.tsx        # Signup page (EXISTS, keep)
│   │   │   ├── dashboard/page.tsx     # Dashboard (REDESIGN - simplify)
│   │   │   ├── tasks/
│   │   │   │   ├── page.tsx           # Task list view (REDESIGN)
│   │   │   │   └── [id]/page.tsx      # Create/Edit task (NEW - dedicated page)
│   │   │   └── settings/page.tsx      # Profile/Settings (REDESIGN)
│   │   ├── components/
│   │   │   ├── auth/
│   │   │   │   ├── LoginForm.tsx      # (EXISTS, keep)
│   │   │   │   └── SignupForm.tsx     # (EXISTS, keep)
│   │   │   ├── tasks/
│   │   │   │   ├── TaskList.tsx       # (EXISTS, simplify)
│   │   │   │   ├── TaskItem.tsx       # (EXISTS, enhance)
│   │   │   │   └── TaskForm.tsx       # (EXISTS, move to dedicated page)
│   │   │   └── ui/
│   │   │       ├── Navbar.tsx         # (EXISTS, simplify)
│   │   │       └── Sidebar.tsx        # (NEW - for desktop layout)
│   │   └── lib/
│   │       ├── auth.ts                # (EXISTS, enhance persistence)
│   │       ├── api.ts                 # (EXISTS, working)
│   │       └── types.ts               # (EXISTS, working)
│   └── package.json
│
├── .env                               # Backend config (EXISTS, has Neon URL)
└── docker-compose.yml                 # (EXISTS)
```

**Structure Decision**: Maintaining existing web application structure with backend/frontend separation. Focus on fixing backend database integration and redesigning frontend for clean, spacious UI.

## Implementation Phases

### Phase 0: Research & Discovery

**Research Tasks:**

1. **Database Initialization Pattern**
   - Research SQLModel table creation with Neon PostgreSQL
   - Investigate Alembic vs direct SQLModel.metadata.create_all()
   - Determine best practice for initial schema setup

2. **Auth State Persistence**
   - Research Next.js 14 App Router auth patterns
   - Investigate localStorage vs cookies for JWT storage
   - Study token refresh strategies

3. **UI/UX Patterns**
   - Research Linear/Asana UI patterns (spacing, hierarchy, motion)
   - Study SaaS dashboard best practices
   - Investigate mobile-first responsive patterns

4. **Task Management Flow**
   - Research dedicated create/edit page patterns
   - Study modal vs full-page task forms
   - Investigate FAB (Floating Action Button) patterns for mobile

**Output**: research.md with decisions on database initialization, auth persistence, UI patterns, and task management flow.

### Phase 1: Data Model & Architecture

**Data Model Updates:**

1. **User Model** (backend/src/models/user.py)
   - Already defined with email, hashed_password, timestamps
   - Needs: Database table creation
   - Needs: Unique constraint on email

2. **Task Model** (backend/src/models/task.py)
   - Already defined with user_id, title, description, completed, timestamps
   - Needs: Database table creation
   - Needs: Foreign key relationship to User
   - Needs: Index on user_id for performance

3. **Database Initialization**
   - Create init_db.py script to create all tables
   - Use SQLModel.metadata.create_all(engine)
   - Run once during deployment setup

**API Contract Updates:**

All existing endpoints remain the same:
- POST /api/auth/register
- POST /api/auth/login
- POST /api/auth/logout
- GET /api/{user_id}/tasks
- POST /api/{user_id}/tasks
- GET /api/{user_id}/tasks/{id}
- PUT /api/{user_id}/tasks/{id}
- DELETE /api/{user_id}/tasks/{id}
- PATCH /api/{user_id}/tasks/{id}/complete

**Critical Fix**: Replace mock storage with actual database queries in backend/src/api/tasks.py

**Frontend Architecture:**

**Page Structure (4 Required Pages):**

1. **Auth Page** (login/signup)
   - Minimal layout, no sidebar
   - Clean forms with validation
   - Redirect to dashboard on success

2. **Dashboard Page**
   - Purpose: Overview and navigation
   - Desktop: Left sidebar + stats cards
   - Mobile: Collapsible menu + stats
   - NO task creation form here
   - Links to: Tasks, Create Task, Settings

3. **Tasks Page** (List + Create/Edit)
   - List view: /tasks
   - Create: /tasks/new
   - Edit: /tasks/[id]
   - Focused, non-congested forms
   - Clear primary CTA

4. **Settings/Profile Page**
   - User info display
   - Logout button
   - Theme toggle (light/dark ready)

**Output**:
- data-model.md (updated with database initialization plan)
- contracts/ (API contracts documented)
- quickstart.md (setup instructions)

### Phase 2: Core Implementation

**Backend Implementation Tasks:**

1. **Database Initialization**
   - Enhance init_db.py to create User and Task tables
   - Add script to run: `python backend/init_db.py`
   - Verify tables created in Neon dashboard

2. **Fix Tasks API** (backend/src/api/tasks.py)
   - Remove mock_tasks_db dictionary
   - Replace all mock operations with SQLModel queries
   - GET /tasks: `session.exec(select(Task).where(Task.user_id == user_id)).all()`
   - POST /tasks: Create Task instance, session.add(), session.commit()
   - PUT /tasks/{id}: Query task, verify ownership, update, commit
   - DELETE /tasks/{id}: Query task, verify ownership, delete, commit
   - PATCH /tasks/{id}/complete: Query task, update completed field, commit

3. **Verify Auth Integration**
   - Ensure User records are created in database during signup
   - Ensure login queries database for user verification
   - Test JWT token contains correct user_id

**Frontend Implementation Tasks:**

1. **Auth State Persistence**
   - Enhance lib/auth.ts to check token validity on mount
   - Add token expiration check
   - Implement auto-redirect logic

2. **Landing Page Redesign** (app/page.tsx)
   - Add auth check: if authenticated, redirect to /dashboard
   - Hide login/signup CTAs when logged in
   - Show "Go to Dashboard" button for authenticated users

3. **Dashboard Redesign** (app/dashboard/page.tsx)
   - Simplify: Remove task creation form
   - Keep: Stats cards (total, active, completed, productivity score)
   - Add: Clear navigation to Tasks, Create Task, Settings
   - Desktop: Left sidebar with navigation
   - Mobile: Top menu with hamburger

4. **Tasks List Page** (app/tasks/page.tsx)
   - Clean list view with task items
   - Each item: title, status, actions (edit, delete, toggle)
   - FAB for "Create Task" on mobile
   - Desktop: "New Task" button in header

5. **Create/Edit Task Page** (app/tasks/new/page.tsx and app/tasks/[id]/page.tsx)
   - Dedicated full page or modal
   - Focused form: title (required), description (optional)
   - Clear primary CTA: "Create Task" or "Save Changes"
   - Cancel button returns to task list

6. **Settings Page** (app/settings/page.tsx)
   - Display user email
   - Logout button
   - Theme toggle (prepare for dark mode)
   - Clean, spacious layout

7. **UI Polish**
   - Implement subtle animations (120-180ms transitions)
   - Ensure mobile responsiveness
   - Add loading states
   - Add error handling with user-friendly messages

### Phase 3: Integration & Testing

**Testing Tasks:**

1. **Database Integration Testing**
   - Verify User table exists in Neon
   - Verify Task table exists in Neon
   - Test signup creates user record
   - Test login retrieves user from database
   - Test task CRUD operations persist to database

2. **Auth Flow Testing**
   - Test signup → auto-login → dashboard redirect
   - Test login → dashboard redirect
   - Test logout → login redirect
   - Test auth state persists across browser refresh
   - Test protected routes redirect unauthenticated users

3. **UI/UX Testing**
   - Verify 4 pages exist and are distinct
   - Verify no congestion (one purpose per page)
   - Test mobile responsiveness
   - Test animations are smooth (120-180ms)
   - Verify FAB appears on mobile

4. **Multi-User Isolation Testing**
   - Create two users
   - Verify each user only sees their own tasks
   - Verify user A cannot access user B's tasks via API

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |

## Architecture Decisions

### Decision 1: Database Initialization Strategy

**Options Considered:**
1. Alembic migrations (full migration framework)
2. SQLModel.metadata.create_all() (direct table creation)
3. Manual SQL scripts

**Decision**: Use SQLModel.metadata.create_all() in init_db.py

**Rationale**:
- Simpler for Phase II scope
- No migration history needed yet
- Models already defined in SQLModel
- Can add Alembic in Phase IV if needed

### Decision 2: Task Create/Edit UI Pattern

**Options Considered:**
1. Modal overlay
2. Dedicated full page
3. Inline editing in list

**Decision**: Dedicated full page (/tasks/new, /tasks/[id])

**Rationale**:
- Meets "one purpose per page" requirement
- Provides focused, non-congested experience
- Better for mobile (no modal complexity)
- Clearer navigation flow

### Decision 3: Auth State Persistence

**Options Considered:**
1. localStorage only
2. Cookies only
3. localStorage + token validation on mount

**Decision**: localStorage + token validation on mount

**Rationale**:
- Already implemented in current codebase
- Works with JWT pattern
- Add validation check to ensure token not expired
- Simpler than cookie-based sessions for Phase II

### Decision 4: Page Reduction Strategy

**Options Considered:**
1. Keep all pages (analytics, evaluations, etc.)
2. Remove non-essential pages
3. Hide non-essential pages behind feature flags

**Decision**: Keep pages but simplify navigation focus

**Rationale**:
- Pages already exist in codebase
- Focus on 4 core pages for Phase 2
- Other pages can remain for future phases
- Simplify dashboard to emphasize core flow

## Critical Path Items

**Must Complete for Phase 2 Success:**

1. ✅ Database tables created in Neon (User, Task)
2. ✅ Tasks API uses database instead of mock storage
3. ✅ Auth state persists across refresh
4. ✅ 4 core pages exist with clear separation
5. ✅ User signup creates database record
6. ✅ User login authenticates against database
7. ✅ Tasks are scoped to logged-in user
8. ✅ UI is clean, spacious, non-congested
9. ✅ Mobile responsive with FAB
10. ✅ Animations are smooth (120-180ms)

## Risk Analysis

**Risk 1: Database Connection Issues**
- **Mitigation**: Neon URL already configured in .env, test connection before implementation
- **Fallback**: Use connection pooling settings in session.py

**Risk 2: Auth State Not Persisting**
- **Mitigation**: Add token expiration check and validation on mount
- **Fallback**: Implement token refresh mechanism

**Risk 3: UI Congestion**
- **Mitigation**: Follow "one purpose per page" rule strictly
- **Fallback**: User testing to identify congestion points

## Success Criteria

Phase 2 is successful when:

- ✅ User can signup once and data is stored in Neon PostgreSQL
- ✅ User can login with same credentials (no re-signup)
- ✅ Auth state persists across browser refresh
- ✅ Dashboard shows stats but NO task creation form
- ✅ Dedicated Create/Edit Task page exists and works
- ✅ Tasks are stored in Neon DB and scoped to user
- ✅ Multi-user isolation is enforced
- ✅ UI is clean, spacious, evaluation-ready
- ✅ Mobile responsive with FAB
- ✅ All 4 core pages exist and are distinct

## Next Steps

After this plan is approved:

1. Run `/sp.tasks` to generate implementation tasks
2. Execute tasks in order (database → backend → frontend)
3. Test each component as implemented
4. Verify success criteria before marking Phase 2 complete

---

**Plan Status**: Draft - Awaiting Approval
**Estimated Complexity**: Medium (fixing existing implementation + UI redesign)
**Dependencies**: Neon PostgreSQL (already configured), existing codebase
