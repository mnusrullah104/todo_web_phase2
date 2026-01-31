# Quickstart Guide: Todo Web Application - Phase II

**Feature**: 002-todo-web-app
**Date**: 2026-01-24

## Overview
Quickstart guide for setting up and running the multi-user Todo Web Application with authentication and persistent storage.

## Prerequisites

### System Requirements
- Node.js 18+ (for frontend development)
- Python 3.13+ (for backend development)
- PostgreSQL-compatible database (Neon recommended)
- Docker and Docker Compose (for containerization)

### Environment Setup
1. Install Python 3.13+ and pip
2. Install Node.js 18+
3. Set up a Neon PostgreSQL account or local PostgreSQL instance

## Environment Variables

Create a `.env` file in the project root with the following:

```env
# Backend Configuration
BACKEND_URL=http://localhost:8000
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Frontend Configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000

# Better Auth Configuration
BETTER_AUTH_SECRET=your-better-auth-secret
BETTER_AUTH_URL=http://localhost:8000
```

## Project Setup

### 1. Clone and Initialize Repository
```bash
# Create project directory
mkdir hackathon-todo
cd hackathon-todo

# Initialize the repository structure
mkdir backend frontend
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn sqlmodel python-multipart python-jose[cryptography] passlib[bcrypt] psycopg2-binary python-dotenv

# Create basic project structure
mkdir -p src/{models,schemas,api,auth,database,config}
touch src/{main.py,__init__.py}
touch src/models/__init__.py src/models/task.py
touch src/schemas/__init__.py src/schemas/task.py
touch src/api/__init__.py src/api/tasks.py
touch src/auth/__init__.py src/auth/jwt.py
touch src/database/__init__.py src/database/session.py
touch src/config/__init__.py src/config/settings.py
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd ../frontend

# Initialize Next.js project
npm create next-app@latest .
npm install @types/node @types/react @types/react-dom tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Install Better Auth client
npm install @better-auth/react @better-auth/client
```

## Backend Development

### 1. Database Models (src/models/task.py)
```python
from sqlmodel import SQLModel, Field
from typing import Optional
import uuid
from datetime import datetime

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
```

### 2. API Routes (src/api/tasks.py)
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from ..database.session import get_session
from ..models.task import Task, TaskCreate, TaskUpdate
from ..auth.jwt import get_current_user

router = APIRouter(prefix="/api/{user_id}")

@router.get("/tasks", response_model=List[TaskRead])
async def get_tasks(
    user_id: uuid.UUID,
    current_user_id: uuid.UUID = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if current_user_id != user_id:
        raise HTTPException(status_code=403, detail="Access forbidden")

    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    return tasks
```

### 3. Run Backend Server
```bash
# From backend directory
uvicorn src.main:app --reload --port 8000
```

## Frontend Development

### 1. Configure Tailwind CSS (tailwind.config.js)
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
```

### 2. Create Authentication Component (src/components/auth/LoginForm.tsx)
```tsx
"use client";
import { useState } from "react";
import { signIn } from "@better-auth/client";

export default function LoginForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await signIn("credentials", {
        email,
        password,
        redirectTo: "/dashboard",
      });
    } catch (error) {
      console.error("Login failed:", error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        required
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
        required
      />
      <button type="submit">Login</button>
    </form>
  );
}
```

### 3. Run Frontend Development Server
```bash
# From frontend directory
npm run dev
```

## Running the Full Application

### 1. Start Database
```bash
# If using Docker
docker-compose up -d

# Or connect to Neon PostgreSQL
# Update DATABASE_URL in .env with your Neon connection string
```

### 2. Run Backend and Frontend Together
```bash
# Terminal 1: Start backend
cd backend
source venv/bin/activate
uvicorn src.main:app --reload --port 8000

# Terminal 2: Start frontend
cd frontend
npm run dev
```

## API Testing

### Test Authentication
```bash
# Register a new user (Better Auth endpoint)
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# Login to get JWT token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

### Test Task Operations
```bash
# Replace with actual user_id and JWT token from login
USER_ID="actual-user-id"
TOKEN="actual-jwt-token"

# Create a task
curl -X POST http://localhost:8000/api/$USER_ID/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test task", "description": "Test description"}'

# Get user's tasks
curl -X GET http://localhost:8000/api/$USER_ID/tasks \
  -H "Authorization: Bearer $TOKEN"
```

## Deployment

### Frontend to Vercel
1. Connect your repository to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy automatically on git push

### Backend Deployment Options
1. **Railway**: `npx railway login` and follow deployment steps
2. **Render**: Create a web service and connect to repository
3. **Docker**: Use the provided docker-compose.yml

## Troubleshooting

### Common Issues
- **Database Connection**: Ensure PostgreSQL is running and credentials are correct
- **JWT Validation**: Verify signing algorithm matches between auth providers
- **CORS**: Configure CORS middleware in FastAPI for frontend domain
- **Environment Variables**: Check all required variables are set

### Debugging Tips
- Enable detailed logging in development
- Check database connection with simple health check endpoint
- Verify JWT token format and signing method