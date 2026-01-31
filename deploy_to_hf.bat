@echo off
REM Hugging Face Space Deployment Script for Windows
REM Run this script to deploy your backend to HF Spaces

echo ========================================
echo 🚀 Deploying Backend to Hugging Face Spaces
echo ========================================
echo.

REM Configuration
set HF_USERNAME=mnusrulah104
set SPACE_NAME=todo-backend
set SPACE_URL=https://huggingface.co/spaces/%HF_USERNAME%/%SPACE_NAME%

echo 📋 Configuration:
echo    Username: %HF_USERNAME%
echo    Space: %SPACE_NAME%
echo    URL: %SPACE_URL%
echo.

REM Check if HF CLI is installed
where huggingface-cli >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Hugging Face CLI not found!
    echo 📦 Installing huggingface-cli...
    pip install huggingface-hub
)

REM Login to Hugging Face
echo 🔐 Please login to Hugging Face...
echo    You'll need your HF access token
echo    Get it from: https://huggingface.co/settings/tokens
echo.
huggingface-cli login

REM Clone the Space
echo.
echo 📥 Cloning your Space...
if exist todo-backend (
    echo ⚠️  Directory 'todo-backend' already exists. Removing...
    rmdir /s /q todo-backend
)

git clone https://huggingface.co/spaces/%HF_USERNAME%/%SPACE_NAME%
cd todo-backend

REM Copy backend files
echo.
echo 📂 Copying backend files...
xcopy /E /I ..\backend\* .

REM Create README.md for HF Space
echo.
echo 📝 Creating README.md...
(
echo ---
echo title: Todo Backend API
echo emoji: 📝
echo colorFrom: blue
echo colorTo: green
echo sdk: docker
echo pinned: false
echo ---
echo.
echo # Todo Web Application Backend
echo.
echo FastAPI backend with JWT authentication.
echo.
echo ## 🚀 Live Endpoints
echo.
echo - Health: https://mnusrulah104-todo-backend.hf.space/health
echo - API Docs: https://mnusrulah104-todo-backend.hf.space/docs
echo.
echo ## 🔧 Features
echo.
echo - User authentication ^(JWT^)
echo - Task CRUD operations
echo - PostgreSQL database
echo - CORS configured
echo.
echo ## 📊 Tech Stack
echo.
echo - FastAPI
echo - PostgreSQL ^(Neon^)
echo - SQLModel
echo - Python 3.13
) > README.md

REM Commit and push
echo.
echo 📤 Pushing to Hugging Face...
git add .
git commit -m "Deploy Todo Backend API"
git push

echo.
echo ✅ Deployment initiated!
echo.
echo 📋 Next steps:
echo    1. Go to: %SPACE_URL%/settings
echo    2. Configure environment secrets (8 variables)
echo    3. Wait for build to complete (3-5 minutes)
echo    4. Test: curl https://%HF_USERNAME%-%SPACE_NAME%.hf.space/health
echo.
echo 🎉 Done!
pause
