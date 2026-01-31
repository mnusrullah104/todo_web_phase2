# Quickstart Guide: Todo SaaS - Phase 2

**Feature**: Todo SaaS - Phase 2 UI/UX + Auth
**Date**: 2026-01-29
**Audience**: Developers setting up the application

## Prerequisites

- Python 3.13+ installed
- Node.js 18+ and npm installed
- Neon PostgreSQL account and database created
- Git installed

## Environment Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd hackathon_2
git checkout 001-ai-k12-efficiency
```

### 2. Backend Setup

#### Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### Configure Environment Variables

Create `.env` file in `backend/` directory:

```env
# Backend Configuration
DATABASE_URL=postgresql://neondb_owner:npg_oyDBNHgQjO97@ep-floral-resonance-ahy4y2dw-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
SECRET_KEY=your-super-secret-key-change-this-in-production-12345
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Important**: Replace `DATABASE_URL` with your Neon PostgreSQL connection string.

#### Initialize Database

```bash
# From backend/ directory
python init_db.py
```

Expected output:
```
Database tables created successfully!
```

Verify tables in Neon dashboard:
- `users` table should exist
- `tasks` table should exist

#### Run Backend Server

```bash
# From backend/ directory
uvicorn src.main:app --reload --port 8001
```

Backend will be available at: `http://localhost:8001`

API documentation: `http://localhost:8001/docs`

### 3. Frontend Setup

#### Install Dependencies

```bash
cd frontend
npm install
```

#### Configure Environment Variables

Create `.env.local` file in `frontend/` directory:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8001
```

#### Run Frontend Development Server

```bash
# From frontend/ directory
npm run dev
```

Frontend will be available at: `http://localhost:3000`

## Verification Steps

### 1. Verify Backend

Open browser to `http://localhost:8001/docs`

You should see FastAPI Swagger documentation with endpoints:
- POST /api/auth/register
- POST /api/auth/login
- POST /api/auth/logout
- GET /api/{user_id}/tasks
- POST /api/{user_id}/tasks
- etc.

### 2. Verify Frontend

Open browser to `http://localhost:3000`

You should see:
- Landing page with "Transform Your Productivity" hero
- "Start Free Today" and "Sign In" buttons
- Clean, spacious design

### 3. Test Authentication Flow

1. Click "Start Free Today" → Navigate to signup page
2. Enter email and password → Click "Sign up"
3. Should redirect to dashboard automatically
4. Verify you see dashboard with stats cards

### 4. Test Task Creation

1. From dashboard, click "New Task" button
2. Should navigate to `/tasks/new`
3. Enter task title and description
4. Click "Create Task"
5. Should redirect to task list with new task visible

### 5. Verify Database Persistence

1. Create a task in the UI
2. Refresh the browser (F5)
3. Task should still be visible (persisted in database)
4. Check Neon dashboard → Query `tasks` table → Verify record exists

## Common Issues

### Issue 1: Database Connection Error

**Symptom**: Backend fails to start with connection error

**Solution**:
1. Verify DATABASE_URL in `.env` is correct
2. Check Neon dashboard → Database is active
3. Verify network connectivity to Neon

### Issue 2: CORS Error in Frontend

**Symptom**: API requests fail with CORS error in browser console

**Solution**:
1. Verify backend CORS middleware includes `http://localhost:3000`
2. Check `backend/src/main.py` → `allow_origins` list
3. Restart backend server

### Issue 3: JWT Token Not Persisting

**Symptom**: User logged out after browser refresh

**Solution**:
1. Check browser localStorage → Should contain `token` key
2. Verify token is not expired (check JWT payload)
3. Check `frontend/src/lib/auth.ts` → `isAuthenticated()` function

### Issue 4: Tasks Not Showing

**Symptom**: Tasks created but not visible in UI

**Solution**:
1. Check browser console for API errors
2. Verify backend is using database (not mock storage)
3. Check `backend/src/api/tasks.py` → Should use `session.exec()` queries
4. Verify user_id in API request matches authenticated user

## Development Workflow

### Making Changes

1. **Backend Changes**:
   - Edit files in `backend/src/`
   - Backend auto-reloads (uvicorn --reload)
   - Test changes at `http://localhost:8001/docs`

2. **Frontend Changes**:
   - Edit files in `frontend/src/`
   - Frontend auto-reloads (Next.js dev server)
   - Test changes at `http://localhost:3000`

### Database Schema Changes

1. Update SQLModel models in `backend/src/models/`
2. Drop existing tables in Neon dashboard (development only)
3. Run `python init_db.py` to recreate tables
4. Note: This will delete all data (use migrations in production)

### Testing API Endpoints

Use FastAPI Swagger UI at `http://localhost:8001/docs`:

1. **Register User**:
   - POST /api/auth/register
   - Body: `{"email": "test@example.com", "password": "password123"}`
   - Copy `access_token` from response

2. **Authorize**:
   - Click "Authorize" button in Swagger UI
   - Enter: `Bearer <access_token>`
   - Click "Authorize"

3. **Create Task**:
   - POST /api/{user_id}/tasks
   - Use user_id from JWT token
   - Body: `{"title": "Test task", "description": "Test description"}`

4. **Get Tasks**:
   - GET /api/{user_id}/tasks
   - Should return array with created task

## Architecture Overview

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│                 │         │                 │         │                 │
│  Next.js        │  HTTP   │  FastAPI        │  SQL    │  Neon           │
│  Frontend       │ ──────> │  Backend        │ ──────> │  PostgreSQL     │
│  (Port 3000)    │         │  (Port 8001)    │         │  (Cloud)        │
│                 │         │                 │         │                 │
└─────────────────┘         └─────────────────┘         └─────────────────┘
       │                            │                            │
       │                            │                            │
   localStorage                  JWT Auth                   users, tasks
   (JWT token)                  Middleware                    tables
```

### Request Flow

1. User signs up → Frontend sends POST to `/api/auth/register`
2. Backend creates User record in database → Returns JWT token
3. Frontend stores token in localStorage
4. User creates task → Frontend sends POST to `/api/{user_id}/tasks` with JWT
5. Backend validates JWT → Extracts user_id → Creates Task in database
6. Frontend receives task data → Displays in UI

## Next Steps

After setup is complete:

1. **Implement Phase 2 Changes**:
   - Fix backend tasks API to use database
   - Redesign frontend pages (4-page structure)
   - Enhance auth state persistence
   - Add UI polish (animations, spacing)

2. **Run Tests**:
   - Backend: `cd backend && pytest`
   - Frontend: Manual testing (no automated tests in Phase 2)

3. **Deploy** (Future):
   - Frontend: Vercel
   - Backend: Railway/Render/Fly.io
   - Database: Already on Neon (production-ready)

## Support

For issues or questions:
- Check API documentation: `http://localhost:8001/docs`
- Review error logs in terminal
- Verify environment variables are set correctly
- Check Neon dashboard for database status

---

**Quickstart Status**: Complete
**Last Updated**: 2026-01-29
