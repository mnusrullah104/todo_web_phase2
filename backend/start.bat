@echo off
REM Backend startup script for Windows with port fallback

echo Starting Phase III AI Chatbot Backend...
echo.

REM Check if .env exists
if not exist .env (
    echo ERROR: .env file not found!
    echo Please copy .env.example to .env and add your COHERE_API_KEY
    pause
    exit /b 1
)

REM Start backend with Python script
python start.py

pause
