# Research: Phase 2 UI/UX + Auth Implementation

**Feature**: Todo SaaS - Phase 2 Redesign
**Date**: 2026-01-29
**Status**: Complete

## Research Questions

### 1. Database Initialization Pattern with SQLModel + Neon PostgreSQL

**Question**: What's the best approach to initialize database tables using SQLModel with Neon PostgreSQL?

**Research Findings**:

**Option A: Alembic Migrations**
- Pros: Full migration history, rollback capability, production-grade
- Cons: Additional complexity, overkill for Phase II scope
- Use case: When schema changes frequently

**Option B: SQLModel.metadata.create_all()**
- Pros: Simple, direct, works with existing models
- Cons: No migration history, no rollback
- Use case: Initial setup, prototyping, Phase II scope

**Option C: Manual SQL Scripts**
- Pros: Full control
- Cons: Duplicates model definitions, error-prone
- Use case: Complex schemas with custom constraints

**Decision**: Use SQLModel.metadata.create_all() in init_db.py

**Rationale**:
- Phase II scope doesn't require migration history
- Models already defined in SQLModel format
- Simpler to implement and maintain
- Can migrate to Alembic in Phase IV if needed
- Neon PostgreSQL supports standard PostgreSQL DDL

**Implementation Pattern**:
```python
from sqlmodel import SQLModel, create_engine
from src.models.user import User
from src.models.task import Task
from src.config.settings import get_settings

settings = get_settings()
engine = create_engine(settings.database_url)

# Create all tables
SQLModel.metadata.create_all(engine)
```

**Alternatives Considered**:
- Alembic: Rejected due to added complexity for Phase II
- Raw SQL: Rejected due to duplication of model definitions

---

### 2. Auth State Persistence in Next.js 14 App Router

**Question**: How should JWT tokens be stored and validated to ensure auth state persists across browser refresh?

**Research Findings**:

**Option A: localStorage Only**
- Pros: Simple, already implemented
- Cons: No automatic expiration check, vulnerable to XSS
- Use case: Simple apps, development

**Option B: httpOnly Cookies**
- Pros: More secure (not accessible via JS), automatic expiration
- Cons: Requires backend cookie handling, CORS complexity
- Use case: Production apps with strict security

**Option C: localStorage + Token Validation on Mount**
- Pros: Balance of simplicity and security, checks expiration
- Cons: Still vulnerable to XSS (but mitigated by validation)
- Use case: Phase II scope with JWT pattern

**Decision**: localStorage + Token Validation on Mount

**Rationale**:
- Already implemented in current codebase (lib/auth.ts)
- Works well with JWT pattern
- Add validation check to decode token and verify expiration
- Simpler than cookie-based approach for Phase II
- Can enhance security in later phases

**Implementation Pattern**:
```typescript
// lib/auth.ts
export const authUtils = {
  isAuthenticated: (): boolean => {
    const token = localStorage.getItem('token');
    if (!token) return false;

    // Decode and check expiration
    try {
      const payload = decodeJWT(token);
      const now = Date.now() / 1000;
      return payload.exp > now;
    } catch {
      return false;
    }
  }
}
```

**Alternatives Considered**:
- httpOnly Cookies: Rejected due to added backend complexity
- sessionStorage: Rejected because it doesn't persist across tabs

---

### 3. UI/UX Patterns for Clean, Spacious SaaS Design

**Question**: What design patterns create a clean, non-congested UI similar to Linear/Asana?

**Research Findings**:

**Key Principles**:
1. **One Purpose Per Page**: Each page should have a single primary action
2. **Generous Spacing**: Use padding/margins liberally (16-24px minimum)
3. **Clear Hierarchy**: Typography scale (text-sm, text-base, text-lg, text-xl, text-2xl)
4. **Subtle Motion**: Animations 120-180ms for smooth transitions
5. **Minimal Navigation**: Show only essential navigation items

**Linear/Asana Patterns**:
- **Dashboard**: Stats cards + quick actions, NO forms
- **List View**: Clean rows with hover states, minimal decoration
- **Create/Edit**: Dedicated page or modal, focused form
- **Sidebar**: Desktop left sidebar, mobile hamburger menu
- **FAB**: Floating Action Button for primary action on mobile

**Decision**: Implement 4-page structure with clear separation

**Page Structure**:
1. **Auth** (login/signup): Minimal, no sidebar, centered form
2. **Dashboard**: Stats overview + navigation, NO task creation
3. **Tasks**: List view + dedicated create/edit pages
4. **Settings**: User profile + logout, simple layout

**Spacing Guidelines**:
- Card padding: p-6 (24px)
- Section margins: mb-8 (32px)
- Grid gaps: gap-6 (24px)
- Button padding: px-6 py-3 (24px x 12px)

**Animation Guidelines**:
- Hover transitions: transition-all duration-150 (150ms)
- Card hover: hover:-translate-y-1 (subtle lift)
- Button hover: hover:shadow-lg (shadow expansion)

**Alternatives Considered**:
- Single-page app: Rejected due to congestion concerns
- Modal-only forms: Rejected in favor of dedicated pages for clarity

---

### 4. Task Management Flow: Modal vs Full Page

**Question**: Should task creation/editing use a modal overlay or dedicated full page?

**Research Findings**:

**Option A: Modal Overlay**
- Pros: Keeps context, faster interaction
- Cons: Can feel cramped, mobile complexity, congestion
- Use case: Quick edits, simple forms

**Option B: Dedicated Full Page**
- Pros: Focused experience, mobile-friendly, clear navigation
- Cons: Loses list context, requires navigation
- Use case: Complex forms, mobile-first design

**Option C: Inline Editing**
- Pros: Fastest interaction, no navigation
- Cons: Clutters list view, limited space
- Use case: Simple field updates only

**Decision**: Dedicated Full Page (/tasks/new, /tasks/[id])

**Rationale**:
- Meets "one purpose per page" requirement from spec
- Provides focused, non-congested experience
- Better for mobile (no modal complexity)
- Clearer navigation flow
- Easier to implement with Next.js App Router

**Implementation Pattern**:
- List view: /tasks (TaskList component)
- Create: /tasks/new (TaskForm component)
- Edit: /tasks/[id] (TaskForm component with pre-filled data)
- Navigation: "New Task" button → /tasks/new
- Mobile: FAB → /tasks/new

**Alternatives Considered**:
- Modal: Rejected due to mobile complexity and congestion
- Inline: Rejected due to limited space and clutter

---

## Technology Stack Validation

### Backend Stack
- **FastAPI**: ✅ Already implemented, working well
- **SQLModel**: ✅ Models defined, needs database sync
- **python-jose**: ✅ JWT handling working
- **Neon PostgreSQL**: ✅ Connection configured in .env

### Frontend Stack
- **Next.js 14 App Router**: ✅ Already implemented
- **TypeScript**: ✅ Type safety in place
- **Tailwind CSS**: ✅ Styling framework configured
- **Axios**: ✅ API client working

### Integration Points
- **JWT Flow**: Frontend stores token → Backend validates → User identified
- **API Communication**: Axios with Authorization header injection
- **Database**: SQLModel ORM → Neon PostgreSQL

---

## Best Practices Summary

### Database Operations
1. Use SQLModel queries instead of raw SQL
2. Always filter by user_id for multi-user isolation
3. Use session.exec() for queries, session.add() for inserts
4. Commit after mutations, refresh to get updated data

### Authentication
1. Store JWT in localStorage (Phase II scope)
2. Validate token expiration on mount
3. Redirect unauthenticated users from protected routes
4. Backend independently verifies token (never trust frontend)

### UI/UX
1. One primary purpose per page
2. Generous spacing (16-24px minimum)
3. Subtle animations (120-180ms)
4. Mobile-first responsive design
5. Clear visual hierarchy

### API Design
1. RESTful endpoints with proper HTTP methods
2. Consistent error responses (JSON format)
3. Proper status codes (200, 201, 401, 404, 500)
4. User ownership validation on every operation

---

## Implementation Priorities

**Phase 0 (Research)**: ✅ Complete
**Phase 1 (Design)**: Next - Create data-model.md, contracts/, quickstart.md
**Phase 2 (Implementation)**: After Phase 1 - Fix backend, redesign frontend
**Phase 3 (Testing)**: After Phase 2 - Verify all success criteria

---

**Research Status**: Complete
**Next Step**: Generate data-model.md and API contracts
