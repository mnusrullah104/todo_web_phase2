#!/bin/bash

# Simple deployment script - Clone fresh and deploy
echo "========================================="
echo "Deploying Backend Fixes to Hugging Face"
echo "========================================="
echo ""

# Create temporary directory
TEMP_DIR="/tmp/hf-deploy-$(date +%s)"
mkdir -p "$TEMP_DIR"

echo "Step 1: Cloning Hugging Face Space..."
cd "$TEMP_DIR"
git clone https://huggingface.co/spaces/mnusrulah104/todo-backend .

echo ""
echo "Step 2: Copying fixed files..."
# Copy source files
cp -r "D:/mna/phaseII/hf-space-ready/src/"* ./src/

# Copy documentation
cp "D:/mna/phaseII/hf-space-ready/README.md" ./
cp "D:/mna/phaseII/hf-space-ready/QUICK_FIX_GUIDE.md" ./
cp "D:/mna/phaseII/hf-space-ready/DEPLOYMENT_CHECKLIST.md" ./
cp "D:/mna/phaseII/hf-space-ready/FIX_SUMMARY.md" ./
cp "D:/mna/phaseII/hf-space-ready/verify_deployment.py" ./

echo ""
echo "Step 3: Committing changes..."
git add -A
git commit -m "Fix: Add database initialization and comprehensive error handling

- Automatic database table creation on startup
- Comprehensive error handling and logging in auth endpoints
- Enhanced CORS configuration with HTTPS support
- Add deployment verification tools

This fixes the 500 error on authentication endpoints."

echo ""
echo "Step 4: Pushing to Hugging Face..."
git push

echo ""
echo "========================================="
echo "Deployment Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Wait 2-3 minutes for Space to rebuild"
echo "2. Check logs at: https://huggingface.co/spaces/mnusrulah104/todo-backend"
echo "3. Test: curl https://mnusrulah104-todo-app.hf.space/health"
echo ""

# Cleanup
cd /
rm -rf "$TEMP_DIR"
