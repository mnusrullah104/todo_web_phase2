# Research: Todo Web Application - Phase II

**Feature**: 002-todo-web-app
**Date**: 2026-01-24

## Overview
Research for implementing a multi-user Todo Web Application with authentication, REST API, and persistent storage using the specified technology stack.

## Better Auth Integration Research

### Better Auth with FastAPI
Better Auth is primarily designed for Next.js applications and provides authentication services with JWT tokens. For FastAPI integration:

- Better Auth offers a REST API that can be used to verify tokens
- Need to implement custom JWT verification middleware in FastAPI
- Better Auth can be configured to work with external databases but may require custom implementation

### Alternative Approach
Consider using python-jose or similar library for JWT handling and implement authentication flow manually, with Better Auth only for the frontend portion.

## Frontend-Backend JWT Flow

### Current Understanding
1. User authenticates via Better Auth on frontend
2. Better Auth provides JWT token to frontend
3. Frontend attaches JWT to all backend API requests in Authorization header
4. Backend verifies JWT signature and extracts user identity
5. Backend enforces user ownership on all operations

### Potential Challenges
- Ensuring JWT signing algorithms match between Better Auth and FastAPI
- Handling token expiration and refresh
- Secure storage of JWT in browser (consider httpOnly cookies vs localStorage)

## Database Integration Research

### Neon PostgreSQL with SQLModel
- Neon provides serverless PostgreSQL with excellent performance characteristics
- SQLModel combines SQLAlchemy and Pydantic for type-safe database operations
- Need to ensure proper connection pooling for serverless environment
- Alembic for database migrations

### Connection Management
- Use connection pooling with proper disposal
- Handle serverless cold start scenarios
- Optimize for Neon's connection limits

## API Design Research

### REST Endpoint Structure
Based on requirements, the API will follow this pattern:
- GET /api/{user_id}/tasks - Retrieve user's tasks
- POST /api/{user_id}/tasks - Create new task for user
- GET /api/{user_id}/tasks/{id} - Retrieve specific task
- PUT /api/{user_id}/tasks/{id} - Update specific task
- DELETE /api/{user_id}/tasks/{id} - Delete specific task
- PATCH /api/{user_id}/tasks/{id}/complete - Toggle completion status

### Authentication Middleware
- Custom JWT verification middleware in FastAPI
- Extract user_id from JWT payload
- Verify user_id matches the one in the URL
- Return 401 for invalid tokens, 403 for unauthorized access

## Next.js App Router Integration

### Authentication State Management
- Use React Context for global authentication state
- Protect routes using authentication checks
- Redirect unauthenticated users to login page
- Persist authentication state across page navigations

### API Client Implementation
- Create centralized API client that automatically injects JWT tokens
- Handle authentication errors gracefully
- Implement request/response interceptors for consistent error handling

## Security Considerations

### JWT Best Practices
- Use strong signing algorithms (RS256 preferred)
- Implement proper token expiration
- Secure token storage in frontend
- Validate token signatures on every request

### User Data Isolation
- Enforce user_id matching between JWT and URL parameters
- Always filter database queries by user_id
- Prevent direct object references (IDOR) attacks

## Deployment Considerations

### Vercel Frontend Deployment
- Next.js app optimized for Vercel deployment
- Environment variables for API endpoints
- Static asset optimization

### Backend Deployment Options
- Could use Railway, Render, or AWS for FastAPI backend
- Containerization with Docker for consistent deployment
- Environment variable management for secrets

## Research Conclusion

The architecture is feasible with the chosen technologies. The main challenge will be integrating Better Auth's frontend authentication with a separate FastAPI backend. This can be achieved by using Better Auth for token generation and validation on the frontend, while implementing custom JWT verification middleware in FastAPI to ensure secure communication between frontend and backend.