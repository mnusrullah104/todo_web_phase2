# Phase III AI Chatbot - Startup Guide

## Quick Start

### 1. Backend Setup

**Step 1: Configure Environment**
```bash
cd backend
cp .env.example .env
# Edit .env and add your COHERE_API_KEY
```

**Step 2: Start Backend (with automatic port fallback)**
```bash
# This will try port 8000, then 8001 if busy
python start.py
```

**Alternative: Manual start**
```bash
# Port 8000
python -m uvicorn src.main:app --reload --port 8000

# Port 8001 (if 8000 is busy)
python -m uvicorn src.main:app --reload --port 8001
```

### 2. Frontend Setup

**Step 1: Install Dependencies**
```bash
cd frontend
npm install
```

**Step 2: Configure API URL**
```bash
# .env.local is already created with default settings
# If backend is on port 8001, edit .env.local:
# NEXT_PUBLIC_API_URL=http://localhost:8001
```

**Step 3: Start Frontend**
```bash
npm run dev
```

### 3. Test the Application

**Step 1: Open Browser**
```
http://localhost:3000
```

**Step 2: Set User ID (temporary auth)**
```javascript
// Open browser console (F12) and run:
localStorage.setItem('userId', '123e4567-e89b-12d3-a456-426614174000')
// Refresh the page
```

**Step 3: Test Chat**
- Click the chat icon (bottom right)
- Try: "Add a task to buy groceries"
- Try: "What's on my list?"
- Verify tasks appear in chat and task list

## Troubleshooting

### Backend Issues

**Problem: Port 8000 already in use**
- Solution: The start.py script automatically tries port 8001
- Or manually specify: `python -m uvicorn src.main:app --reload --port 8001`

**Problem: COHERE_API_KEY not set**
- Error: "COHERE_API_KEY is required"
- Solution: Add your Cohere API key to backend/.env

**Problem: Database connection error**
- Check DATABASE_URL in backend/.env
- Default uses SQLite (test.db) - should work out of the box

### Frontend Issues

**Problem: ERR_CONNECTION_REFUSED**
- Check if backend is running: `curl http://localhost:8000/health`
- Check if API URL matches backend port in frontend/.env.local
- If backend is on 8001, update: `NEXT_PUBLIC_API_URL=http://localhost:8001`

**Problem: CORS errors**
- Backend CORS is configured for localhost:3000 and localhost:3001
- Check browser console for specific CORS error
- Verify backend logs show the request

**Problem: Chat widget not appearing**
- Set userId in localStorage (see Step 2 above)
- Check browser console for errors
- Verify ChatWidget is imported in ClientLayout.tsx

### Chat Issues

**Problem: "AI service configuration error"**
- COHERE_API_KEY is missing or invalid
- Check backend/.env file

**Problem: Chat sends but no response**
- Check backend logs for errors
- Verify Cohere API key is valid
- Check network tab in browser for API response

**Problem: Tasks not appearing in chat**
- Verify backend database has tasks
- Check browser console for errors
- Try: "What's on my list?" to see all tasks

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=sqlite:///./test.db
JWT_SECRET=your-secret-key
COHERE_API_KEY=your-cohere-api-key-here
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Port Configuration

**Backend Ports:**
- Primary: 8000
- Fallback: 8001

**Frontend Port:**
- Default: 3000

**If backend runs on 8001:**
1. Update frontend/.env.local: `NEXT_PUBLIC_API_URL=http://localhost:8001`
2. Restart frontend: `npm run dev`

## Testing Checklist

- [ ] Backend starts successfully
- [ ] Frontend starts successfully
- [ ] Health check works: `curl http://localhost:8000/health`
- [ ] Chat widget appears on page
- [ ] Can send message: "Add a task to buy groceries"
- [ ] Task appears in chat response
- [ ] Task appears in task list UI
- [ ] Can list tasks: "What's on my list?"
- [ ] Conversation persists after page refresh

## Next Steps

After successful startup:
1. Test all MVP features (add tasks, list tasks)
2. Verify conversation persistence
3. Test with multiple users (different user IDs)
4. Check database for saved conversations and messages

## Getting Help

If you encounter issues:
1. Check backend logs for errors
2. Check browser console for frontend errors
3. Verify all environment variables are set
4. Ensure Cohere API key is valid
5. Check that ports are not blocked by firewall
