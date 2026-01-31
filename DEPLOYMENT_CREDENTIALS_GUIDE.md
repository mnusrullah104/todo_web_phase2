# Deployment Credentials Guide
## Todo Web Application - Phase 2

**Repository**: https://github.com/mnusrullah104/todo_web_phase2.git
**Status**: ✅ Code successfully pushed to GitHub

---

## 📋 Table of Contents
1. [Vercel Deployment (Frontend)](#vercel-deployment-frontend)
2. [Hugging Face Deployment (Backend)](#hugging-face-deployment-backend)
3. [Database Setup (Neon PostgreSQL)](#database-setup)
4. [Environment Variables Reference](#environment-variables-reference)
5. [Deployment Checklist](#deployment-checklist)

---

## 🚀 Vercel Deployment (Frontend)

### Prerequisites
- GitHub account (already connected to your repository)
- Vercel account (free tier available)

### Required Credentials

#### 1. **Vercel Account**
- **Where to get**: https://vercel.com/signup
- **Sign up with**: GitHub account (recommended for seamless integration)
- **Cost**: Free tier available (sufficient for this project)

#### 2. **Environment Variables for Vercel**

You'll need to configure these in Vercel Dashboard → Project Settings → Environment Variables:

```bash
# Backend API URL (will be your Hugging Face Space URL)
NEXT_PUBLIC_API_BASE_URL=https://your-username-backend-space.hf.space

# Better Auth URL (same as backend URL)
NEXT_PUBLIC_BETTER_AUTH_URL=https://your-username-backend-space.hf.space
```

### Deployment Steps

#### Step 1: Connect to Vercel
1. Go to https://vercel.com/new
2. Click "Import Git Repository"
3. Select your GitHub repository: `mnusrullah104/todo_web_phase2`
4. Authorize Vercel to access your GitHub account

#### Step 2: Configure Project
```
Framework Preset: Next.js
Root Directory: frontend
Build Command: npm run build
Output Directory: .next
Install Command: npm install
```

#### Step 3: Add Environment Variables
In Vercel Dashboard:
1. Go to Project Settings → Environment Variables
2. Add the following variables:
   - `NEXT_PUBLIC_API_BASE_URL` → Your backend URL
   - `NEXT_PUBLIC_BETTER_AUTH_URL` → Your backend URL

#### Step 4: Deploy
1. Click "Deploy"
2. Wait for build to complete (2-5 minutes)
3. Your frontend will be live at: `https://your-project.vercel.app`

### Post-Deployment
- **Custom Domain**: Settings → Domains (optional)
- **Automatic Deployments**: Enabled by default on git push
- **Preview Deployments**: Automatic for pull requests

---

## 🤗 Hugging Face Deployment (Backend)

### Prerequisites
- Hugging Face account
- Docker knowledge (optional, HF handles this)

### Required Credentials

#### 1. **Hugging Face Account**
- **Where to get**: https://huggingface.co/join
- **Sign up with**: Email or GitHub
- **Cost**: Free tier available

#### 2. **Hugging Face Access Token**
- **Where to get**: https://huggingface.co/settings/tokens
- **Steps**:
  1. Go to Settings → Access Tokens
  2. Click "New token"
  3. Name: `todo-backend-deploy`
  4. Type: Write access
  5. Copy and save the token securely

#### 3. **Environment Variables for Hugging Face Space**

You'll need to configure these as "Secrets" in your Space:

```bash
# Database Connection
DATABASE_URL=postgresql://neondb_owner:npg_oyDBNHgQjO97@ep-floral-resonance-ahy4y2dw-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require

# JWT Authentication
SECRET_KEY=your-super-secret-key-here-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Better Auth
BETTER_AUTH_SECRET=lt8uk47XM6J1Ynnu8x6vLkjakGkSOugf
BETTER_AUTH_URL=https://your-space-name.hf.space

# Backend URL (for CORS)
BACKEND_URL=https://your-space-name.hf.space
```

### Deployment Steps

#### Step 1: Create Hugging Face Space
1. Go to https://huggingface.co/new-space
2. Configure:
   - **Space name**: `todo-backend` (or your preferred name)
   - **License**: MIT
   - **Space SDK**: Docker
   - **Visibility**: Public (or Private if you have Pro)

#### Step 2: Push Backend Code
```bash
# Clone your HF Space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/todo-backend
cd todo-backend

# Copy backend files from your project
cp -r D:/mna/hackathon_2/backend/* .

# Create a Dockerfile in the root (if not exists)
# The Dockerfile is already in backend/Dockerfile

# Commit and push
git add .
git commit -m "Initial backend deployment"
git push
```

#### Step 3: Configure Space Secrets
1. Go to your Space → Settings → Repository secrets
2. Add each environment variable as a secret:
   - Click "Add a new secret"
   - Name: `DATABASE_URL`
   - Value: Your Neon PostgreSQL connection string
   - Repeat for all variables listed above

#### Step 4: Configure Space Settings
1. **Port**: Set to `8000` (FastAPI default)
2. **Hardware**: CPU Basic (free tier)
3. **Sleep time**: Disable if you have Pro (optional)

#### Alternative: Deploy via Docker Hub
If Hugging Face Spaces doesn't work well for your backend, consider:
- **Railway**: https://railway.app (recommended for FastAPI)
- **Render**: https://render.com (free tier available)
- **Fly.io**: https://fly.io (free tier available)

---

## 🗄️ Database Setup (Neon PostgreSQL)

### Current Database
Your `.env.example` shows you're already using Neon PostgreSQL:

```
DATABASE_URL=postgresql://neondb_owner:npg_oyDBNHgQjO97@ep-floral-resonance-ahy4y2dw-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

### ⚠️ SECURITY WARNING
**The database credentials in `.env.example` are exposed!** You should:

1. **Rotate the database password immediately**:
   - Go to https://console.neon.tech
   - Navigate to your project
   - Go to Settings → Reset password
   - Update the `DATABASE_URL` in your deployment environments

2. **Never commit real credentials to Git**:
   - The `.env.example` should contain placeholder values only
   - Real credentials should only be in `.env` (which is gitignored)

### If You Need a New Database

#### Option 1: Neon PostgreSQL (Recommended)
- **Where**: https://neon.tech
- **Sign up**: Free tier available (0.5 GB storage)
- **Steps**:
  1. Create account
  2. Create new project
  3. Copy connection string
  4. Add to environment variables

#### Option 2: Supabase PostgreSQL
- **Where**: https://supabase.com
- **Sign up**: Free tier available (500 MB storage)
- **Includes**: Built-in authentication (optional)

#### Option 3: Railway PostgreSQL
- **Where**: https://railway.app
- **Sign up**: $5 free credit
- **Includes**: Automatic backups

---

## 🔐 Environment Variables Reference

### Frontend (Vercel)
| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_BASE_URL` | Backend API URL | `https://your-backend.hf.space` |
| `NEXT_PUBLIC_BETTER_AUTH_URL` | Auth service URL | `https://your-backend.hf.space` |

### Backend (Hugging Face / Railway / Render)
| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host/db` | ✅ Yes |
| `SECRET_KEY` | JWT signing key | Random 32+ char string | ✅ Yes |
| `ALGORITHM` | JWT algorithm | `HS256` | ✅ Yes |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry time | `30` | ✅ Yes |
| `BETTER_AUTH_SECRET` | Auth service secret | Random 32+ char string | ✅ Yes |
| `BETTER_AUTH_URL` | Backend URL | `https://your-backend.hf.space` | ✅ Yes |
| `BACKEND_URL` | Backend URL (CORS) | `https://your-backend.hf.space` | ✅ Yes |

### How to Generate Secure Secrets
```bash
# On Linux/Mac/Git Bash
openssl rand -hex 32

# On Windows PowerShell
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))

# Online (use with caution)
# https://www.random.org/strings/
```

---

## ✅ Deployment Checklist

### Pre-Deployment
- [x] Code pushed to GitHub
- [ ] Database credentials rotated (if exposed)
- [ ] New secure `SECRET_KEY` generated
- [ ] New secure `BETTER_AUTH_SECRET` generated
- [ ] Database is accessible from deployment platform

### Vercel (Frontend)
- [ ] Vercel account created
- [ ] Repository imported to Vercel
- [ ] Root directory set to `frontend`
- [ ] Environment variables configured
- [ ] First deployment successful
- [ ] Frontend accessible via Vercel URL

### Hugging Face / Alternative (Backend)
- [ ] Hugging Face account created (or alternative platform)
- [ ] Space created (or project created)
- [ ] Backend code pushed
- [ ] All environment variables/secrets configured
- [ ] Port set to 8000
- [ ] Backend API accessible
- [ ] Health check endpoint working (`/` or `/health`)

### Integration Testing
- [ ] Frontend can reach backend API
- [ ] CORS configured correctly
- [ ] User registration works
- [ ] User login works
- [ ] JWT tokens are issued correctly
- [ ] Task CRUD operations work
- [ ] Authentication persists across page reloads

### Post-Deployment
- [ ] Custom domain configured (optional)
- [ ] SSL/HTTPS enabled (automatic on Vercel/HF)
- [ ] Monitoring set up (optional)
- [ ] Error tracking configured (optional - Sentry)
- [ ] Database backups enabled

---

## 🔧 Troubleshooting

### Common Issues

#### 1. CORS Errors
**Problem**: Frontend can't reach backend
**Solution**: Add frontend URL to CORS allowed origins in `backend/src/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-project.vercel.app",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 2. Database Connection Failed
**Problem**: Backend can't connect to database
**Solution**:
- Check `DATABASE_URL` is correct
- Ensure database allows connections from deployment platform IP
- For Neon: Enable "Allow connections from anywhere" in settings

#### 3. Environment Variables Not Loading
**Problem**: App behaves as if env vars are missing
**Solution**:
- Vercel: Redeploy after adding env vars
- Hugging Face: Restart Space after adding secrets
- Check variable names match exactly (case-sensitive)

#### 4. Build Failures
**Problem**: Deployment build fails
**Solution**:
- Check build logs for specific errors
- Ensure all dependencies are in `package.json` / `requirements.txt`
- Verify Node.js / Python versions are compatible

---

## 📞 Support Resources

### Vercel
- **Documentation**: https://vercel.com/docs
- **Support**: https://vercel.com/support
- **Community**: https://github.com/vercel/vercel/discussions

### Hugging Face
- **Documentation**: https://huggingface.co/docs/hub/spaces
- **Support**: https://discuss.huggingface.co
- **Discord**: https://hf.co/join/discord

### Neon PostgreSQL
- **Documentation**: https://neon.tech/docs
- **Support**: https://neon.tech/docs/introduction/support
- **Discord**: https://discord.gg/neon

---

## 🎯 Quick Start Commands

### Local Development
```bash
# Start backend
cd backend
python -m uvicorn src.main:app --reload --port 8000

# Start frontend
cd frontend
npm run dev
```

### Check Deployment Status
```bash
# Vercel CLI (optional)
npm i -g vercel
vercel --prod

# Check backend health
curl https://your-backend-url.hf.space/
```

---

## 📝 Next Steps After Deployment

1. **Test all features** in production environment
2. **Set up monitoring** (optional but recommended)
3. **Configure custom domain** (optional)
4. **Enable analytics** (Vercel Analytics is free)
5. **Set up CI/CD** (already automatic with Vercel + GitHub)
6. **Add error tracking** (Sentry, LogRocket, etc.)
7. **Implement rate limiting** (for production security)
8. **Set up database backups** (Neon has automatic backups)

---

## 🔒 Security Recommendations

1. **Rotate all secrets** before production deployment
2. **Use different secrets** for development and production
3. **Enable 2FA** on all service accounts (GitHub, Vercel, HF)
4. **Restrict database access** to deployment platform IPs only
5. **Use environment-specific** `.env` files
6. **Never commit** `.env` files to Git
7. **Regularly update** dependencies for security patches
8. **Implement rate limiting** on API endpoints
9. **Use HTTPS only** (automatic on Vercel/HF)
10. **Monitor logs** for suspicious activity

---

**Generated**: 2026-01-31
**Repository**: https://github.com/mnusrullah104/todo_web_phase2.git
**Status**: Ready for deployment ✅
