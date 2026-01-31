# 🚀 Quick Deploy to Vercel

**Time**: 15 minutes | **Difficulty**: Easy

---

## Prerequisites

- Vercel account (free): https://vercel.com/signup
- GitHub account connected to your repository
- Backend deployed to Hugging Face (get your HF Space URL)

---

## Step 1: Create Vercel Account (2 minutes)

1. Go to https://vercel.com/signup
2. Click **"Continue with GitHub"**
3. Authorize Vercel to access your repositories

---

## Step 2: Import Repository (3 minutes)

1. Go to https://vercel.com/new
2. Click **"Import Git Repository"**
3. Find and select: `mnusrullah104/todo_web_phase2`
4. Click **"Import"**

---

## Step 3: Configure Project (5 minutes)

### Root Directory
1. Click **"Edit"** next to "Root Directory"
2. Enter: `frontend`
3. Click **"Continue"**

### Framework
- Should auto-detect as **"Next.js"**
- Leave all build settings as default

### Environment Variables
Click **"Environment Variables"** and add these 2 variables:

| Name | Value |
|------|-------|
| `NEXT_PUBLIC_API_BASE_URL` | `https://YOUR_USERNAME-todo-backend.hf.space` |
| `NEXT_PUBLIC_BETTER_AUTH_URL` | `https://YOUR_USERNAME-todo-backend.hf.space` |

**⚠️ Important:**
- Replace `YOUR_USERNAME` with your Hugging Face username
- Use your actual Space name if different from `todo-backend`
- Both variables should have the same value (your HF backend URL)
- Select all environments: **Production**, **Preview**, **Development**

**Example:**
```
NEXT_PUBLIC_API_BASE_URL=https://johndoe-todo-backend.hf.space
NEXT_PUBLIC_BETTER_AUTH_URL=https://johndoe-todo-backend.hf.space
```

---

## Step 4: Deploy (2 minutes)

1. Click **"Deploy"**
2. Wait 2-5 minutes for build
3. You'll get a URL like: `https://your-project-name.vercel.app`

**Your frontend is live!** 🎉

---

## Step 5: Update Backend CORS (3 minutes)

Now connect your frontend to backend:

1. Go to your Hugging Face Space: `https://huggingface.co/spaces/YOUR_USERNAME/todo-backend`
2. Click **Settings** → **Repository secrets**
3. Find `FRONTEND_URL` secret
4. Click **"Edit"**
5. Update value to: `https://your-project-name.vercel.app`
6. Click **"Update secret"**
7. Wait ~1 minute for Space to restart

---

## Step 6: Verify (2 minutes)

1. Visit your Vercel URL: `https://your-project-name.vercel.app`
2. You should see the landing page
3. Open browser DevTools (F12) → Console tab
4. Should see no CORS errors

**Test the app:**
- Click **"Sign Up"**
- Create a test account
- Should redirect to dashboard
- Try creating a task

---

## 🔗 Your URLs

**Frontend**: `https://your-project-name.vercel.app`
**Backend**: `https://YOUR_USERNAME-todo-backend.hf.space`
**Vercel Dashboard**: `https://vercel.com/dashboard`

---

## 🐛 Troubleshooting

### Build fails
- Check build logs in Vercel dashboard
- Verify root directory is set to `frontend`
- Ensure `package.json` exists in frontend folder

### CORS errors in browser console
```
Access to fetch at '...' has been blocked by CORS policy
```
**Fix:**
- Verify `FRONTEND_URL` in HF Space matches Vercel URL exactly
- Include `https://` in the URL
- Wait for HF Space to restart (check Logs tab)

### API calls fail (Network Error)
- Verify `NEXT_PUBLIC_API_BASE_URL` is correct
- Test backend: `curl https://YOUR_USERNAME-todo-backend.hf.space/health`
- Check backend is running (HF Space shows "Running")

### Environment variables not working
- Redeploy after adding variables:
  1. Go to Vercel Dashboard → Your Project → Deployments
  2. Click latest deployment → "..." menu → "Redeploy"
- Environment variables only take effect after redeployment

### Can't sign up or login
- Check browser console for errors
- Verify both environment variables are set correctly
- Test backend health endpoint
- Check Network tab in DevTools for failed requests

---

## 🔄 Automatic Deployments

Vercel automatically deploys when you push to GitHub:

- **Push to `main`** → Production deployment
- **Push to other branches** → Preview deployment
- **Pull requests** → Preview deployment with unique URL

To disable auto-deploy:
1. Project Settings → Git
2. Toggle off "Production Branch"

---

## 🎨 Optional: Custom Domain

1. Go to Project Settings → Domains
2. Click **"Add"**
3. Enter your domain (e.g., `todo.yourdomain.com`)
4. Follow DNS configuration instructions
5. Vercel provides free SSL certificate

**After adding custom domain:**
- Update `FRONTEND_URL` in HF Space to include custom domain
- Can have multiple: `https://your-app.vercel.app,https://todo.yourdomain.com`

---

## 📊 Optional: Enable Analytics

1. Go to Project Settings → Analytics
2. Enable **Vercel Analytics** (free)
3. View real-time visitor data and Web Vitals

---

## ✅ Deployment Checklist

- [x] Vercel account created
- [x] Repository imported
- [x] Root directory set to `frontend`
- [x] 2 environment variables configured
- [x] First deployment successful
- [x] Frontend accessible via Vercel URL
- [x] Backend CORS updated with Vercel URL
- [ ] Sign up tested
- [ ] Login tested
- [ ] Task creation tested
- [ ] No CORS errors in console

---

## 📝 Next Steps

1. ✅ Frontend deployed to Vercel
2. ✅ Backend CORS updated
3. ⏳ Test all functionality:
   - Sign up
   - Login
   - Create tasks
   - Edit tasks
   - Delete tasks
   - Refresh page (should stay logged in)

---

## 🆘 Need Help?

- **Detailed guide**: `docs/deployment/README_VERCEL_DEPLOYMENT.md`
- **Vercel Support**: https://vercel.com/support
- **Check logs**: Vercel Dashboard → Deployments → Build logs

---

## 🎉 Success!

Your Todo Web Application is now fully deployed:

- ✅ **Backend**: Hugging Face Spaces
- ✅ **Frontend**: Vercel
- ✅ **Database**: Neon PostgreSQL
- ✅ **CORS**: Configured
- ✅ **HTTPS**: Automatic (both platforms)

**Share your app**: Send your Vercel URL to users!

---

**Deployment complete!** Your full-stack application is live. 🚀
