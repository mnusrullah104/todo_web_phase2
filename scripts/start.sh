#!/bin/bash
# Quick Start Script for Evaluation Todo App

echo "🚀 Starting Evaluation Todo App..."
echo ""

# Check if backend is running
if curl -s http://localhost:8001/docs > /dev/null 2>&1; then
    echo "✅ Backend is already running on port 8001"
else
    echo "⚠️  Backend is not running. Starting it now..."
    cd backend
    uvicorn src.main:app --reload --port 8001 &
    BACKEND_PID=$!
    echo "✅ Backend started (PID: $BACKEND_PID)"
    cd ..
    sleep 3
fi

echo ""
echo "📋 Next Steps:"
echo "1. Open a new terminal"
echo "2. Run: cd frontend && npm run dev"
echo "3. Open browser: http://localhost:3000"
echo ""
echo "📚 Available Pages:"
echo "   - Dashboard:    http://localhost:3000/dashboard"
echo "   - Tasks:        http://localhost:3000/tasks"
echo "   - Evaluations:  http://localhost:3000/evaluations"
echo "   - Analytics:    http://localhost:3000/analytics"
echo "   - Settings:     http://localhost:3000/settings"
echo ""
echo "🔧 Backend API Docs: http://localhost:8001/docs"
echo ""
echo "✨ Your premium multi-page SaaS app is ready!"
