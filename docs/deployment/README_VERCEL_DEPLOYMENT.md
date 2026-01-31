# Vercel Frontend Deployment Guide
## Next.js Todo Application

This guide provides step-by-step instructions for deploying the Todo Web Application frontend to Vercel.

---

## 📋 Prerequisites

1. **Vercel Account**: Sign up at https://vercel.com/signup (free tier available)
2. **GitHub Account**: Connected to your repository
3. **Backend Deployed**: Hugging Face Space URL ready
4. **Database**: Backend connected to PostgreSQL database

---

## 🚀 Deployment Steps

### Step 1: Connect GitHub to Vercel

1. Go to https://vercel.com/new
2. Click **"Import Git Repository"**
3. If not connected, click **"Connect GitHub Account"**
4. Authorize Vercel to access your GitHub repositories
5. Select your repository: `mnusrullah104/todo_web_phase2`

### Step 2: Configure Project Settings

On the import screen, configure:

#### Framework Preset
- **Framework**: Next.js (auto-detected)

#### Root Directory
- **Root Directory**: `frontend`
- Click **"Edit"** next to Root Directory
- Enter: `frontend`
- This tells Vercel to build from the frontend folder

#### Build Settings
- **Build Command**: `npm run build` (default, leave as is)
- **Output Directory**: `.next` (default, leave as is)
- **Install Command**: `npm install` (default, leave as is)

### Step 3: Configure Environment Variables

Click **"Environment Variables"** section and add:

| Name | Value | Environment |
|------|-------|-------------|
| `NEXT_PUBLIC_API_BASE_URL` | `https://YOUR_USERNAME-todo-backend.hf.space` | Production, Preview, Development |
| `NEXT_PUBLIC_BETTER_AUTH_URL` | `https://YOUR_USERNAME-todo-backend.hf.space` | Production, Preview, Development |

**Important**:
- Replace `YOUR_USERNAME` with your actual Hugging Face username
- Use your actual Space name if different from `todo-backend`
- Both variables should point to your Hugging Face backend URL
- Select all three environments (Production, Preview, Development)

**Example**:
```
NEXT_PUBLIC_API_BASE_URL=https://johndoe-todo-backend.hf.space
NEXT_PUBLIC_BETTER_AUTH_URL=https://johndoe-todo-backend.hf.space
```

### Step 4: Deploy

1. Click **"Deploy"**
2. Vercel will:
   - Clone your repository
   - Install dependencies
   - Build the Next.js application
   - Deploy to their CDN
3. Wait 2-5 minutes for the build to complete

### Step 5: Get Your Deployment URL

Once deployed, you'll see:
- **Production URL**: `https://your-project-name.vercel.app`
- This is your live application URL

### Step 6: Update Backend CORS

Now that you have your Vercel URL, update your Hugging Face Space:

1. Go to your Hugging Face Space: `https://huggingface.co/spaces/YOUR_USERNAME/todo-backend`
2. Click **Settings** → **Repository secrets**
3. Find `FRONTEND_URL` secret
4. Update it to: `https://your-project-name.vercel.app`
5. Your Space will automatically restart

**If you have multiple frontend URLs** (staging, production):
```
FRONTEND_URL=https://your-app.vercel.app,https://your-app-staging.vercel.app
```

### Step 7: Verify Deployment

1. Visit your Vercel URL: `https://your-project-name.vercel.app`
2. You should see the landing page
3. Try to sign up for a new account
4. Try to log in
5. Create a task
6. Verify all features work

---

## 🔧 Troubleshooting

### Build Fails

**Check Build Logs**:
1. Go to your Vercel project dashboard
2. Click on the failed deployment
3. View the build logs

**Common Issues**:
- Missing dependencies: Check `frontend/package.json`
- TypeScript errors: Fix type issues in your code
- Environment variables: Ensure they're set correctly

### CORS Errors in Browser Console

**Symptoms**:
```
Access to fetch at 'https://...' from origin 'https://...' has been blocked by CORS policy
```

**Solution**:
1. Verify `FRONTEND_URL` is set correctly in Hugging Face Space secrets
2. Ensure it matches your Vercel URL exactly (including https://)
3. Wait for Space to restart after updating the secret

### API Calls Fail (Network Error)

**Check Backend URL**:
1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Verify `NEXT_PUBLIC_API_BASE_URL` is correct
3. Test the backend URL in browser: `https://YOUR_USERNAME-todo-backend.hf.space/health`
4. Should return: `{"status": "healthy", "version": "1.0.0"}`

**If Backend URL Changed**:
1. Update environment variables in Vercel
2. Redeploy: Go to Deployments → Click "..." → Redeploy

### Authentication Not Working

**Check Both URLs Match**:
- `NEXT_PUBLIC_API_BASE_URL` and `NEXT_PUBLIC_BETTER_AUTH_URL` should be identical
- Both should point to your Hugging Face Space

**Clear Browser Cache**:
- Open DevTools (F12)
- Right-click refresh button → "Empty Cache and Hard Reload"

### Environment Variables Not Loading

**Redeploy After Adding Variables**:
1. Go to Vercel Dashboard → Your Project → Deployments
2. Click on the latest deployment
3. Click "..." menu → "Redeploy"
4. Environment variables only take effect after redeployment

---

## 🔄 Automatic Deployments

Vercel automatically deploys when you push to GitHub:

- **Push to `main` branch** → Production deployment
- **Push to other branches** → Preview deployment
- **Pull requests** → Preview deployment with unique URL

### Disable Auto-Deploy (Optional)

If you want manual control:
1. Go to Project Settings → Git
2. Toggle off "Production Branch"
3. Deploy manually from Vercel dashboard

---

## 🎨 Custom Domain (Optional)

### Add Custom Domain

1. Go to Project Settings → Domains
2. Click "Add"
3. Enter your domain (e.g., `todo.yourdomain.com`)
4. Follow DNS configuration instructions
5. Vercel provides free SSL certificate

### Update Backend CORS

After adding custom domain:
1. Update `FRONTEND_URL` in Hugging Face Space
2. Add your custom domain: `https://todo.yourdomain.com`
3. Can have multiple: `https://your-app.vercel.app,https://todo.yourdomain.com`

---

## 📊 Monitoring & Analytics

### Vercel Analytics (Free)

1. Go to Project Settings → Analytics
2. Enable Vercel Analytics
3. View real-time visitor data
4. Track Web Vitals (performance metrics)

### Error Tracking

Consider integrating:
- **Sentry**: Error tracking and monitoring
- **LogRocket**: Session replay and debugging
- **Datadog**: Full-stack monitoring

---

## 🔒 Security Best Practices

1. **Environment Variables**:
   - Never commit `.env.local` to Git
   - Use Vercel's environment variable system
   - Prefix public variables with `NEXT_PUBLIC_`

2. **HTTPS Only**:
   - Vercel provides automatic HTTPS
   - Never use HTTP in production

3. **Content Security Policy**:
   - Configure in `next.config.js` if needed
   - Restrict resource loading

4. **Rate Limiting**:
   - Consider adding rate limiting to backend
   - Protect against abuse

---

## 🚀 Performance Optimization

### Already Configured

Your Next.js app includes:
- ✅ React Strict Mode
- ✅ Turbopack (Next.js 16)
- ✅ CSS Optimization
- ✅ Automatic code splitting
- ✅ Image optimization

### Additional Optimizations

1. **Enable Vercel Speed Insights**:
   ```bash
   npm install @vercel/speed-insights
   ```

2. **Add Vercel Analytics**:
   ```bash
   npm install @vercel/analytics
   ```

3. **Configure Caching**:
   - Vercel automatically caches static assets
   - Configure in `next.config.js` if needed

---

## 🔄 Updating Your Deployment

### Automatic Updates

Simply push to GitHub:
```bash
git add .
git commit -m "Update frontend"
git push origin main
```

Vercel will automatically:
1. Detect the push
2. Build the new version
3. Deploy to production
4. Keep previous version as rollback

### Manual Deployment

From Vercel Dashboard:
1. Go to Deployments
2. Click "..." on any deployment
3. Click "Redeploy"

### Rollback

If something goes wrong:
1. Go to Deployments
2. Find a previous working deployment
3. Click "..." → "Promote to Production"

---

## 📱 Preview Deployments

Every pull request gets a unique preview URL:

1. Create a branch: `git checkout -b feature/new-feature`
2. Make changes and push
3. Create pull request on GitHub
4. Vercel automatically creates preview deployment
5. Test on preview URL before merging

---

## 🐛 Debugging

### View Logs

1. Go to Vercel Dashboard → Your Project
2. Click on a deployment
3. View "Build Logs" and "Function Logs"

### Local Development

Test locally before deploying:
```bash
cd frontend
npm install
npm run dev
```

Access at: `http://localhost:3000`

### Environment Variables in Local Dev

Create `frontend/.env.local`:
```bash
NEXT_PUBLIC_API_BASE_URL=https://YOUR_USERNAME-todo-backend.hf.space
NEXT_PUBLIC_BETTER_AUTH_URL=https://YOUR_USERNAME-todo-backend.hf.space
```

**Never commit `.env.local` to Git!**

---

## ✅ Deployment Checklist

- [ ] Vercel account created and GitHub connected
- [ ] Repository imported to Vercel
- [ ] Root directory set to `frontend`
- [ ] Environment variables configured:
  - [ ] `NEXT_PUBLIC_API_BASE_URL`
  - [ ] `NEXT_PUBLIC_BETTER_AUTH_URL`
- [ ] First deployment successful
- [ ] Frontend accessible via Vercel URL
- [ ] Backend CORS updated with Vercel URL
- [ ] Sign up functionality tested
- [ ] Login functionality tested
- [ ] Task creation tested
- [ ] Task CRUD operations tested
- [ ] Authentication persistence verified

---

## 🆘 Support Resources

- **Vercel Documentation**: https://vercel.com/docs
- **Next.js Documentation**: https://nextjs.org/docs
- **Vercel Support**: https://vercel.com/support
- **Vercel Community**: https://github.com/vercel/vercel/discussions

---

## 📝 Important URLs to Save

After deployment, save these URLs:

1. **Production URL**: `https://your-project-name.vercel.app`
2. **Backend URL**: `https://YOUR_USERNAME-todo-backend.hf.space`
3. **Vercel Dashboard**: `https://vercel.com/your-username/your-project`
4. **GitHub Repository**: `https://github.com/mnusrullah104/todo_web_phase2`

---

**Your Frontend URL**: `https://your-project-name.vercel.app`

Share this URL with users to access your Todo application!
