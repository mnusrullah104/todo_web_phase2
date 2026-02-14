# Quick Fix for Vercel 404 Error

## The Problem
Vercel is deploying from the root directory, but your Next.js app is in the `frontend` folder.

## The Solution (Choose One)

### Option A: Fix Existing Deployment (Fastest - 2 minutes)

1. **Go to Vercel Dashboard**
   - Visit: https://vercel.com/dashboard
   - Select your project

2. **Update Root Directory**
   - Settings → General
   - Find "Root Directory"
   - Click Edit → Change to: `frontend`
   - Save

3. **Add Environment Variable**
   - Settings → Environment Variables
   - Add new variable:
     - Name: `NEXT_PUBLIC_API_BASE_URL`
     - Value: `https://mnusrulah104-todo-app.hf.space`
     - Select all environments (Production, Preview, Development)
   - Save

4. **Redeploy**
   - Go to Deployments tab
   - Click (...) on latest deployment
   - Click "Redeploy"
   - Wait 2-3 minutes

✅ **Done!** Your app should now work without 404 errors.

---

### Option B: Deploy via CLI (Alternative)

```bash
# Navigate to frontend
cd D:\mna\phaseII\frontend

# Install Vercel CLI (if needed)
npm install -g vercel

# Login
vercel login

# Deploy
vercel --prod

# Set environment variable after deployment
vercel env add NEXT_PUBLIC_API_BASE_URL production
# Enter: https://mnusrulah104-todo-app.hf.space
```

---

## Verify It Works

After deployment:

1. Visit your Vercel URL
2. You should see the landing page (not 404!)
3. Click "Sign Up" and create an account
4. Should redirect to dashboard
5. Try creating a task

---

## Files Created

- `vercel.json` (root) - Monorepo config
- `frontend/vercel.json` - Frontend config
- `VERCEL_DEPLOYMENT_GUIDE.md` - Full guide
- `VERCEL_QUICK_FIX.md` - This file

---

## Need Help?

See `VERCEL_DEPLOYMENT_GUIDE.md` for detailed troubleshooting.
