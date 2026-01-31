# Todo Web Application - Phase II

A production-ready multi-user Todo Web Application with persistent cloud database storage, secure authentication using Better Auth, REST API backend, and responsive web frontend.

## Features

- Secure user authentication and registration
- Personalized task management
- Full CRUD operations for tasks
- JWT-based authorization
- Responsive web interface
- Multi-user data isolation

## Tech Stack

- **Frontend**: Next.js 14+, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.13+
- **Database**: PostgreSQL (Neon Serverless)
- **ORM**: SQLModel
- **Authentication**: Better Auth

## Setup

### Prerequisites

- Node.js 18+
- Python 3.13+
- PostgreSQL (or Docker for local development)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd todo-web-app
```

2. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd frontend
npm install
```

4. Copy environment variables:
```bash
cp .env.example .env
```

5. Update the `.env` file with your configuration

### Running Locally

#### With Docker (recommended):

```bash
docker-compose up
```

#### Without Docker:

1. Start the database (PostgreSQL)

2. Run the backend:
```bash
cd backend
uvicorn src.main:app --reload --port 8001

```

3. Run the frontend:
```bash
cd frontend
npm run dev
```

## API Endpoints

- `GET /api/{user_id}/tasks` - Get user's tasks
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion

## Environment Variables

See `.env.example` for all required environment variables.

## Development

### Backend

The backend is built with FastAPI and follows a modular structure:
- `src/models/` - Database models
- `src/schemas/` - Pydantic schemas
- `src/api/` - API routes
- `src/auth/` - Authentication logic
- `src/database/` - Database session management
- `src/config/` - Configuration settings

### Frontend

The frontend uses Next.js App Router:
- `src/app/` - Page components
- `src/components/` - Reusable components
- `src/lib/` - Utility functions and API client
- `src/styles/` - Global styles

## Testing

### Backend Tests
Run backend tests with pytest:
```bash
cd backend
pip install pytest
pytest tests/
```

### Frontend Tests
Run frontend tests:
```bash
cd frontend
npm test
```

## Deployment

### Frontend
Deploy the frontend to Vercel:
```bash
cd frontend
npm run build
vercel deploy
```

Or with Docker:
```bash
docker build -t todo-frontend .
docker run -p 3000:3000 todo-frontend
```

### Backend
Deploy the backend to platforms like Render, Railway, or AWS:

With Docker:
```bash
cd backend
docker build -t todo-backend .
docker run -p 8001:8001 todo-backend
```

Using the provided docker-compose:
```bash
docker-compose up --build
```

## Security

- JWT-based authentication and authorization
- User data isolation
- Input validation and sanitization
- Environment-based configuration for secrets

## Architecture

The application follows a clean architecture with separation of concerns between frontend and backend. The backend provides a REST API that the frontend consumes, with JWT tokens ensuring secure communication.