#!/bin/bash
# Hugging Face Space Deployment Script
# Run this script to deploy your backend to HF Spaces

echo "🚀 Deploying Backend to Hugging Face Spaces"
echo "============================================"
echo ""

# Configuration
HF_USERNAME="mnusrulah104"
SPACE_NAME="todo-backend"
SPACE_URL="https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME"

echo "📋 Configuration:"
echo "   Username: $HF_USERNAME"
echo "   Space: $SPACE_NAME"
echo "   URL: $SPACE_URL"
echo ""

# Check if HF CLI is installed
if ! command -v huggingface-cli &> /dev/null; then
    echo "❌ Hugging Face CLI not found!"
    echo "📦 Installing huggingface-cli..."
    pip install huggingface-hub
fi

# Login to Hugging Face
echo "🔐 Please login to Hugging Face..."
echo "   You'll need your HF access token"
echo "   Get it from: https://huggingface.co/settings/tokens"
echo ""
huggingface-cli login

# Clone the Space
echo ""
echo "📥 Cloning your Space..."
if [ -d "todo-backend" ]; then
    echo "⚠️  Directory 'todo-backend' already exists. Removing..."
    rm -rf todo-backend
fi

git clone https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME
cd todo-backend

# Copy backend files
echo ""
echo "📂 Copying backend files..."
cp -r ../backend/* .

# Create README.md for HF Space
echo ""
echo "📝 Creating README.md..."
cat > README.md << 'EOF'
---
title: Todo Backend API
emoji: 📝
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# Todo Web Application Backend

FastAPI backend with JWT authentication.

## 🚀 Live Endpoints

- Health: https://mnusrulah104-todo-backend.hf.space/health
- API Docs: https://mnusrulah104-todo-backend.hf.space/docs

## 🔧 Features

- User authentication (JWT)
- Task CRUD operations
- PostgreSQL database
- CORS configured

## 📊 Tech Stack

- FastAPI
- PostgreSQL (Neon)
- SQLModel
- Python 3.13
EOF

# Commit and push
echo ""
echo "📤 Pushing to Hugging Face..."
git add .
git commit -m "Deploy Todo Backend API"
git push

echo ""
echo "✅ Deployment initiated!"
echo ""
echo "📋 Next steps:"
echo "   1. Go to: $SPACE_URL/settings"
echo "   2. Configure environment secrets (8 variables)"
echo "   3. Wait for build to complete (3-5 minutes)"
echo "   4. Test: curl https://$HF_USERNAME-$SPACE_NAME.hf.space/health"
echo ""
echo "🎉 Done!"
