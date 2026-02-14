@echo off
echo ========================================
echo Deploying Backend Fixes to Hugging Face
echo ========================================
echo.

cd hf-space-ready

echo Step 1: Checking Hugging Face remote...
git remote -v | findstr huggingface
if %errorlevel% neq 0 (
    echo Adding Hugging Face remote...
    git remote add huggingface https://huggingface.co/spaces/mnusrulah104/todo-backend
)

echo.
echo Step 2: Staging all changes...
git add -A

echo.
echo Step 3: Committing changes...
git commit -m "Fix: Add database initialization and comprehensive error handling

- Automatic database table creation on startup
- Comprehensive error handling and logging in auth endpoints
- Enhanced CORS configuration with HTTPS support
- Add deployment verification tools

This fixes the 500 error on authentication endpoints."

echo.
echo Step 4: Pushing to Hugging Face Space...
git push huggingface main

echo.
echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Wait 2-3 minutes for Space to rebuild
echo 2. Check logs at: https://huggingface.co/spaces/mnusrulah104/todo-backend
echo 3. Run: python verify_deployment.py
echo.
pause
