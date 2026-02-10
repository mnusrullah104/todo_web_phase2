# Quick Fix for NEXT_PUBLIC_API_BASE_URL Error

## Problem
Frontend can't find the `NEXT_PUBLIC_API_BASE_URL` environment variable.

## Solution Applied
Created `frontend/.env.local` with:
```
NEXT_PUBLIC_API_BASE_URL=https://mnusrulah104-todo-app.hf.space
```

## Next Steps

### 1. Restart Your Next.js Dev Server

**Stop the current server:**
- Press `Ctrl+C` in the terminal where Next.js is running

**Start it again:**
```bash
cd D:\mna\phaseII\frontend
npm run dev
```

### 2. Verify the Fix

After restarting, you should see:
- ✅ No more "NEXT_PUBLIC_API_BASE_URL is not set" error
- ✅ The app loads without console errors
- ✅ You can access the login/signup pages

### 3. Test Authentication

1. **Open your browser**: http://localhost:3000
2. **Go to Login page**
3. **Try to login** with test credentials
4. **Check browser console** - should see API calls to `https://mnusrulah104-todo-app.hf.space`

## Important Notes

- **Environment variables in Next.js** require a server restart to take effect
- **NEXT_PUBLIC_** prefix makes the variable available in the browser
- **Never commit `.env.local`** to git (it's already in .gitignore)

## If You're Deploying to Vercel

Add this environment variable in Vercel dashboard:
1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add:
   - **Name**: `NEXT_PUBLIC_API_BASE_URL`
   - **Value**: `https://mnusrulah104-todo-app.hf.space`
4. Redeploy

## Troubleshooting

**Still seeing the error after restart?**
- Make sure you're in the correct directory: `D:\mna\phaseII\frontend`
- Verify the file exists: `ls -la .env.local`
- Check file content: `cat .env.local`
- Try clearing Next.js cache: `rm -rf .next` then restart

**API calls failing?**
- Verify backend is running: `curl https://mnusrulah104-todo-app.hf.space/health`
- Check CORS settings in backend
- Look at browser Network tab for specific errors
