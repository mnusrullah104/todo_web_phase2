# 🚀 Vercel Deployment Guide - Fix 404 Error

## Problem
Vercel is showing 404 errors because it's trying to deploy from the root directory instead of the `frontend` folder where the Next.js app is located.

## ✅ Solution: Deploy Frontend to Vercel

### Option 1: Update Existing Vercel Project (Recommended)

If you already have a Vercel project deployed:

1. **Go to your Vercel project settings**
   - Visit: https://vercel.com/dashboard
   - Select your project
   - Go to **Settings** → **General**

2. **Update Root Directory**
   - Find the "Root Directory" setting
   - Click **Edit**
   - Set it to: `frontend`
   - Click **Save**

3. **Set Environment Variables**
   - Go to **Settings** → **Environment Variables**
   - Add the following variable:
     ```
     Name: NEXT_PUBLIC_API_BASE_URL
     Value: https://mnusrulah104-todo-app.hf.space
     Environment: Production, Preview, Development
     ```

4. **Redeploy**
   - Go to **Deployments** tab
   - Click the three dots (...) on the latest deployment
   - Click **Redeploy**
   - Wait 2-3 minutes for the build to complete

### Option 2: Deploy Fresh from GitHub

If you want to start fresh:

1. **Push your code to GitHub** (if not already done)
   ```bash
   cd D:\mna\phaseII
   git add vercel.json frontend/vercel.json VERCEL_DEPLOYMENT_GUIDE.md
   git commit -m "Add Vercel configuration for monorepo deployment"
   git push origin main
   ```

2. **Create new Vercel project**
   - Go to: https://vercel.com/new
   - Import your GitHub repository
   - **IMPORTANT:** In the "Configure Project" step:
     - Framework Preset: **Next.js**
     - Root Directory: **frontend** (click Edit and select `frontend`)
     - Build Command: `npm run build` (default is fine)
     - Output Directory: `.next` (default is fine)
     - Install Command: `npm install` (default is fine)

3. **Add Environment Variable**
   - Before clicking "Deploy", expand **Environment Variables**
   - Add:
     ```
     NEXT_PUBLIC_API_BASE_URL = https://mnusrulah104-todo-app.hf.space
     ```

4. **Click Deploy**
   - Wait 2-3 minutes for deployment
   - Your app will be live at: `https://your-project.vercel.app`

### Option 3: Deploy via Vercel CLI

```bash
# Install Vercel CLI (if not installed)
npm install -g vercel

# Navigate to frontend directory
cd D:\mna\phaseII\frontend

# Login to Vercel
vercel login

# Deploy
vercel --prod

# When prompted:
# - Set up and deploy? Yes
# - Which scope? Select your account
# - Link to existing project? No (or Yes if you have one)
# - What's your project's name? todo-frontend (or your preferred name)
# - In which directory is your code located? ./ (current directory)
# - Want to override settings? No
```

## 📋 Verification Steps

After deployment, verify everything works:

### 1. Check Homepage
- Visit your Vercel URL: `https://your-project.vercel.app`
- You should see the landing page with "Transform Your Productivity"
- **No 404 error!**

### 2. Test Authentication
- Click "Sign Up" button
- Create a new account
- Should redirect to `/dashboard` after signup
- Try logging out and logging in again

### 3. Check API Connection
- Open browser DevTools (F12)
- Go to Console tab
- Look for API calls to `https://mnusrulah104-todo-app.hf.space`
- Should see successful responses (200 status codes)

### 4. Test Task Management
- Create a new task
- Edit a task
- Delete a task
- All should work without errors

## 🔧 Environment Variables Checklist

Make sure these are set in Vercel:

| Variable | Value | Required |
|----------|-------|----------|
| `NEXT_PUBLIC_API_BASE_URL` | `https://mnusrulah104-todo-app.hf.space` | ✅ Yes |

**Note:** The `NEXT_PUBLIC_` prefix is required for environment variables that need to be accessible in the browser.

## 🐛 Troubleshooting

### Still Getting 404 Error?

**Check Root Directory:**
1. Go to Vercel project settings
2. Verify "Root Directory" is set to `frontend`
3. If not, update it and redeploy

**Check Build Logs:**
1. Go to your Vercel deployment
2. Click on the deployment
3. Check the build logs for errors
4. Common issues:
   - Missing dependencies: Run `npm install` in frontend folder
   - Build errors: Run `npm run build` locally to test
   - Environment variables: Verify they're set correctly

### API Connection Errors?

**CORS Issues:**
- The backend at Hugging Face should already have CORS configured
- Check backend logs at: https://huggingface.co/spaces/mnusrulah104/todo-backend

**Wrong API URL:**
- Verify `NEXT_PUBLIC_API_BASE_URL` is set correctly in Vercel
- Check browser console for the actual API URL being called

### Build Fails?

**Check Node Version:**
- Vercel uses Node 18.x by default
- Your app should work with Node 18+
- If needed, add to `package.json`:
  ```json
  "engines": {
    "node": ">=18.0.0"
  }
  ```

**Missing Dependencies:**
- Make sure `package-lock.json` is committed
- Try deleting `node_modules` and `.next` locally
- Run `npm install` and `npm run build` to verify

## 📝 Files Created

This guide created the following files:

1. **`vercel.json`** (root) - Monorepo configuration
2. **`frontend/vercel.json`** - Frontend-specific configuration
3. **`VERCEL_DEPLOYMENT_GUIDE.md`** - This guide

## 🎯 Expected Result

After following this guide:

✅ No more 404 errors on Vercel
✅ Homepage loads correctly
✅ Authentication works (signup/login)
✅ Tasks can be created, edited, and deleted
✅ API calls to Hugging Face backend work
✅ Dark mode and all features functional

## 🔗 Useful Links

- **Vercel Dashboard:** https://vercel.com/dashboard
- **Vercel Docs - Monorepos:** https://vercel.com/docs/monorepos
- **Next.js Deployment:** https://nextjs.org/docs/deployment
- **Your Backend:** https://mnusrulah104-todo-app.hf.space

## 💡 Pro Tips

1. **Custom Domain:** After deployment, you can add a custom domain in Vercel settings
2. **Preview Deployments:** Every git push creates a preview deployment automatically
3. **Environment Variables:** Use different values for Production vs Preview environments
4. **Analytics:** Enable Vercel Analytics in project settings for performance insights

---

## 🎉 You're Ready to Deploy!

Choose Option 1 (update existing project) or Option 2 (fresh deployment) and follow the steps above. Your app will be live in minutes!
