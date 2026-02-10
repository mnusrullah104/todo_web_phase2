# Phase III AI Chatbot - Quick Start Guide

## Prerequisites

1. **Python 3.13+** installed
2. **Node.js 18+** and npm installed
3. **PostgreSQL database** (Neon Serverless or local)
4. **Cohere API key** (get from https://cohere.com)

## Setup Instructions

### 1. Backend Setup

```bash
cd backend

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add:
#   DATABASE_URL=postgresql://...
#   COHERE_API_KEY=your_cohere_api_key
#   SECRET_KEY=your_secret_key
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment (optional)
cp .env.example .env.local
# Edit .env.local if needed:
#   NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Database Initialization

The database tables are automatically created on first startup using SQLModel's `create_all()` method. No manual migration needed.

## Running the Application

### Option 1: Use the Startup Script (Windows)

```bash
# From project root
start-all.bat
```

This will start both backend and frontend servers in separate windows.

### Option 2: Manual Startup

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Testing the Chat Interface

### 1. Access the Application

Open your browser and navigate to: http://localhost:3000

### 2. Set a Test User ID

Since JWT authentication is not yet fully integrated, you need to set a user ID manually:

1. Open browser console (F12)
2. Run:
   ```javascript
   localStorage.setItem('userId', '123e4567-e89b-12d3-a456-426614174000')
   ```
3. Refresh the page

### 3. Open the Chat

Click the blue chat icon in the bottom-right corner.

### 4. Try These Commands

**Add tasks:**
- "Add a task to buy groceries"
- "Create a task to call dentist"
- "Add finish report with description needs charts and data"

**List tasks:**
- "What's on my list?"
- "Show my pending tasks"
- "Show completed tasks"

**Complete tasks:**
- "Mark buy groceries as done"
- "Complete the dentist task"

**Update tasks:**
- "Change buy groceries to buy groceries and household items"
- "Update the report task description to include presentation"

**Delete tasks:**
- "Delete the groceries task"
- "Remove the dentist task"

## Verifying the Implementation

### 1. Check Backend Health

```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy","version":"1.0.0"}
```

### 2. Check API Documentation

Open: http://localhost:8000/docs

You should see the FastAPI interactive documentation with all endpoints including `/api/{user_id}/chat`.

### 3. Test Tools Directly

```bash
cd backend
python test_tools.py
```

This will run unit tests for all 5 MCP tools and verify they work correctly.

### 4. Check Database Tables

Connect to your database and verify these tables exist:
- `user`
- `task`
- `conversation` (new in Phase III)
- `message` (new in Phase III)

## Troubleshooting

### Backend won't start

**Error: "COHERE_API_KEY not configured"**
- Solution: Add your Cohere API key to `backend/.env`

**Error: "Database connection failed"**
- Solution: Verify DATABASE_URL in `backend/.env` is correct
- Check that your PostgreSQL database is running

### Frontend won't start

**Error: "Module not found"**
- Solution: Run `npm install` in the frontend directory

**Error: "Port 3000 already in use"**
- Solution: Kill the process using port 3000 or change the port:
  ```bash
  npm run dev -- -p 3001
  ```

### Chat not working

**Chat icon doesn't appear:**
- Check browser console for errors
- Verify userId is set in localStorage
- Verify backend is running on port 8000

**Chat returns errors:**
- Check backend logs for detailed error messages
- Verify COHERE_API_KEY is valid
- Check network tab in browser dev tools

**Tasks not appearing:**
- Verify the task was created by checking the database
- Try refreshing the traditional task list UI
- Check that you're using the same user_id

## Architecture Overview

```
Frontend (Next.js)
    ↓ HTTP POST /api/{user_id}/chat
Backend (FastAPI)
    ↓ Load conversation history
Database (PostgreSQL)
    ↓ Return messages
Backend
    ↓ Send to Cohere agent
Cohere API
    ↓ Interpret intent, call tools
MCP Tools (5 tools)
    ↓ Execute database operations
Database
    ↓ Return results
Backend
    ↓ Save conversation
Database
    ↓ Return response
Frontend
    ↓ Display in chat
```

## Next Steps

1. **Integrate Better Auth JWT:**
   - Replace the placeholder authentication in `backend/src/api/chat.py`
   - Add Authorization header in `frontend/src/components/ChatWidget.tsx`

2. **Deploy to Production:**
   - Set environment variables in production
   - Deploy backend (e.g., Railway, Render, AWS)
   - Deploy frontend (e.g., Vercel, Netlify)
   - Update CORS settings for production URLs

3. **Add More Features:**
   - Task priorities
   - Due dates
   - Task categories/tags
   - Search functionality
   - Bulk operations

## Support

For issues or questions:
1. Check the logs in backend terminal
2. Check browser console for frontend errors
3. Review the implementation summary: `IMPLEMENTATION_SUMMARY.md`
4. Check the specification: `specs/003-ai-chatbot-integration/spec.md`
