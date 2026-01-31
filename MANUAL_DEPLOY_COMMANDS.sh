#!/bin/bash
# MANUAL DEPLOYMENT COMMANDS
# Copy and paste these commands one by one

echo "🚀 Manual Deployment to Hugging Face Spaces"
echo "============================================"
echo ""
echo "Step 1: Login to Hugging Face"
echo "Command: huggingface-cli login"
echo ""
echo "You'll need your token from: https://huggingface.co/settings/tokens"
echo ""
read -p "Press Enter after you've logged in..."

echo ""
echo "Step 2: Clone your Space"
cd D:/mna/hackathon_2
git clone https://huggingface.co/spaces/mnusrulah104/todo-backend

echo ""
echo "Step 3: Copy prepared files"
cp -r hf-space-ready/* todo-backend/

echo ""
echo "Step 4: Commit and push"
cd todo-backend
git add .
git commit -m "Deploy Todo Backend API"
git push

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Next steps:"
echo "1. Configure secrets at: https://huggingface.co/spaces/mnusrulah104/todo-backend/settings"
echo "2. Wait for build (3-5 minutes)"
echo "3. Test: curl https://mnusrulah104-todo-backend.hf.space/health"
