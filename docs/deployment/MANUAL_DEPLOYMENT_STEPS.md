# Manual Deployment Steps for Hugging Face Space

Since automated deployment is having issues with git history, here's how to manually deploy the fixes:

## Option 1: Direct File Upload (Easiest)

1. **Go to your Hugging Face Space**: https://huggingface.co/spaces/mnusrulah104/todo-backend

2. **Click "Files" tab**

3. **Upload/Replace these files** from `D:\mna\phaseII\hf-space-ready\`:

   **Core fixes:**
   - `src/main.py` - Contains database initialization on startup
   - `src/api/auth.py` - Contains error handling for auth endpoints
   - `src/database/session.py` - Contains database connection error handling

   **Documentation:**
   - `README.md` - Updated documentation
   - `QUICK_FIX_GUIDE.md` - Troubleshooting guide
   - `DEPLOYMENT_CHECKLIST.md` - Deployment checklist
   - `verify_deployment.py` - Verification script
   - `FIX_SUMMARY.md` - Technical summary

4. **Commit message**: "Fix: Add database initialization and error handling for auth endpoints"

5. **Wait 2-3 minutes** for the Space to rebuild

## Option 2: Clone and Push (Recommended)

```bash
# 1. Clone your Hugging Face Space to a new directory
cd D:\
git clone https://huggingface.co/spaces/mnusrulah104/todo-backend hf-backend-deploy

# 2. Copy fixed files from hf-space-ready
cd D:\mna\phaseII
xcopy /E /Y hf-space-ready\src D:\hf-backend-deploy\src\
copy /Y hf-space-ready\*.md D:\hf-backend-deploy\
copy /Y hf-space-ready\*.py D:\hf-backend-deploy\

# 3. Commit and push
cd D:\hf-backend-deploy
git add -A
git commit -m "Fix: Add database initialization and comprehensive error handling"
git push

# 4. Clean up
cd D:\
rmdir /S /Q hf-backend-deploy
```

## Option 3: Use the Batch Script

Run the provided batch script:
```bash
cd D:\mna\phaseII
deploy_to_hf.bat
```

## After Deployment

### 1. Verify Environment Variables

Go to Space Settings → Repository secrets and ensure these are set:

```
DATABASE_URL=postgresql://neondb_owner:npg_oyDBNHgQjO97@ep-floral-resonance-ahy4y2dw-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require
SECRET_KEY=embrace-bicycle-adjust
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
BETTER_AUTH_SECRET=bOB2jFYGwhrr9tWgslJQb0MPBdS7Ryux
BETTER_AUTH_URL=https://mnusrulah104-todo-app.hf.space
BACKEND_URL=https://mnusrulah104-todo-app.hf.space
FRONTEND_URL=https://your-vercel-url.vercel.app,http://localhost:3000
```

### 2. Check Logs

1. Go to your Space page
2. Click "Logs" tab
3. Look for:
   - ✅ "Connecting to database..."
   - ✅ "Database engine created successfully"
   - ✅ "Creating database tables..."
   - ✅ "Database tables created successfully!"

### 3. Test Authentication

```bash
# Test health endpoint
curl https://mnusrulah104-todo-app.hf.space/health

# Test registration
curl -X POST https://mnusrulah104-todo-app.hf.space/api/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"test@example.com\", \"password\": \"testpass123\"}"

# Test login
curl -X POST https://mnusrulah104-todo-app.hf.space/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"test@example.com\", \"password\": \"testpass123\"}"
```

### 4. Update Frontend

Update `frontend/.env.local`:
```
NEXT_PUBLIC_API_BASE_URL=https://mnusrulah104-todo-app.hf.space
```

## What Was Fixed

1. **Automatic Database Initialization** - Tables are now created on startup
2. **Comprehensive Error Logging** - All errors are logged with full details
3. **Error Handling** - Auth endpoints now catch and return meaningful errors
4. **Database Connection Handling** - Connection errors are properly logged
5. **Enhanced CORS** - Better support for HTTPS and multiple origins

## Troubleshooting

If you still get 500 errors after deployment:

1. **Check Hugging Face Logs** for specific error messages
2. **Verify DATABASE_URL** is correct and accessible
3. **Check database permissions** - ensure user can CREATE TABLE
4. **Test database connection** independently using psql

## Need Help?

- Check `QUICK_FIX_GUIDE.md` for detailed troubleshooting
- Review `DEPLOYMENT_CHECKLIST.md` for complete deployment guide
- Run `verify_deployment.py` to test all endpoints
