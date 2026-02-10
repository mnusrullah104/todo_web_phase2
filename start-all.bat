@echo off
REM Master startup script - Starts both backend and frontend

echo ========================================
echo Phase III AI Chatbot - Full Stack Startup
echo ========================================
echo.

REM Check if backend .env exists
if not exist backend\.env (
    echo ERROR: backend\.env file not found!
    echo Please copy backend\.env.example to backend\.env and add your COHERE_API_KEY
    echo.
    pause
    exit /b 1
)

echo Starting Backend...
start "Backend Server" cmd /k "cd backend && python start.py"

echo Waiting 5 seconds for backend to start...
timeout /t 5 /nobreak >nul

echo.
echo Starting Frontend...
start "Frontend Server" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo Both servers are starting!
echo ========================================
echo.
echo Backend: http://localhost:8000 (or 8001 if 8000 is busy)
echo Frontend: http://localhost:3000
echo.
echo To test:
echo 1. Open http://localhost:3000 in your browser
echo 2. Open browser console (F12) and run:
echo    localStorage.setItem('userId', '123e4567-e89b-12d3-a456-426614174000')
echo 3. Refresh the page
echo 4. Click the chat icon and try: "Add a task to buy groceries"
echo.
echo Press any key to exit (servers will keep running in separate windows)
pause >nul
