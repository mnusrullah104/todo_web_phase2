# Deployment Checklist: Todo SaaS - Phase 2

**Feature**: Todo SaaS - Phase 2 UI/UX + Auth
**Date**: 2026-01-30
**Status**: Ready for Deployment

## Pre-Deployment Checklist

### 1. Code Verification
- [x] All tests passing
- [x] Database integration working
- [x] Auth flow tested end-to-end
- [x] API endpoints secured with JWT
- [x] User data isolation verified
- [x] Mobile responsiveness tested
- [x] No console errors in browser

### 2. Environment Variables Prepared
- [ ] Backend production SECRET_KEY generated (use `openssl rand -hex 32`)
- [ ] Neon PostgreSQL connection string ready
- [ ] Frontend API URL configured for production

### 3. Security Review
- [x] JWT secret key is strong and unique
- [x] Database credentials not in code
- [x] CORS configured for production domain
- [x] SQL injection protection (using SQLModel parameterized queries)
- [x] XSS protection (React escapes by default)
- [x] Password hashing with bcrypt

---

## Frontend Deployment (Vercel)

### Step 1: Prepare Repository
```bash
# Ensure code is committed
git add .
git commit -m "Prepare for deployment"
git push origin 001-ai-k12-efficiency
```

### Step 2: Deploy to Vercel

#### Option A: Vercel CLI
```bash
cd frontend
npm install -g vercel
vercel login
vercel --prod
```

#### Option B: Vercel Dashboard
1. Go to https://vercel.com/new
2. Import Git repository
3. Select `frontend` as root directory
4. Configure build settings:
   - **Framework Preset**: Next.js
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
   - **Install Command**: `npm install`

### Step 3: Configure Environment Variables

In Vercel Dashboard → Settings → Environment Variables:

```env
NEXT_PUBLIC_API_BASE_URL=https://your-backend-url.com
```

**Important**: Replace with your actual backend URL after backend deployment.

### Step 4: Verify Deployment
- [ ] Visit Vercel deployment URL
- [ ] Landing page loads correctly
- [ ] Can navigate to signup page
- [ ] No console errors
- [ ] Mobile view works correctly

---

## Backend Deployment

### Option 1: Railway (Recommended)

#### Step 1: Install Railway CLI
```bash
npm install -g @railway/cli
railway login
```

#### Step 2: Initialize Project
```bash
cd backend
railway init
```

#### Step 3: Configure Environment Variables
```bash
railway variables set DATABASE_URL="postgresql://neondb_owner:..."
railway variables set SECRET_KEY="your-production-secret-key"
railway variables set ALGORITHM="HS256"
railway variables set ACCESS_TOKEN_EXPIRE_MINUTES="30"
```

#### Step 4: Deploy
```bash
railway up
```

#### Step 5: Get Deployment URL
```bash
railway domain
```

### Option 2: Render

#### Step 1: Create New Web Service
1. Go to https://render.com/
2. Click "New +" → "Web Service"
3. Connect your Git repository
4. Configure:
   - **Name**: todo-api
   - **Root Directory**: `backend`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`

#### Step 2: Add Environment Variables
```env
DATABASE_URL=postgresql://neondb_owner:...
SECRET_KEY=your-production-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### Step 3: Deploy
- Click "Create Web Service"
- Wait for deployment to complete

### Option 3: Fly.io

#### Step 1: Install Fly CLI
```bash
curl -L https://fly.io/install.sh | sh
fly auth login
```

#### Step 2: Create fly.toml
```toml
app = "todo-api"

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8080"

[[services]]
  http_checks = []
  internal_port = 8080
  processes = ["app"]
  protocol = "tcp"

  [[services.ports]]
    force_https = true
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443
```

#### Step 3: Deploy
```bash
cd backend
fly launch
fly secrets set DATABASE_URL="postgresql://..."
fly secrets set SECRET_KEY="your-secret-key"
fly deploy
```

---

## Database Setup (Neon PostgreSQL)

### Verify Database Configuration
1. Go to https://console.neon.tech/
2. Select your project
3. Verify database is active
4. Copy connection string

### Initialize Database Tables
```bash
# From backend directory
python init_db.py
```

Expected output:
```
Creating database tables...
[SUCCESS] Database tables created successfully!
[SUCCESS] Users table created
[SUCCESS] Tasks table created
```

### Verify Tables Created
In Neon SQL Editor, run:
```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';
```

Should see:
- `user`
- `task`

---

## Post-Deployment Verification

### 1. Backend Health Check
```bash
curl https://your-backend-url.com/health
```

Expected response:
```json
{"status":"healthy","version":"1.0.0"}
```

### 2. API Documentation
Visit: `https://your-backend-url.com/docs`

Verify all endpoints are listed:
- POST /api/auth/register
- POST /api/auth/login
- GET /api/{user_id}/tasks
- etc.

### 3. Frontend-Backend Integration
1. Visit your Vercel URL
2. Click "Start Free Today"
3. Create account with test email
4. Verify redirect to dashboard
5. Create a test task
6. Verify task appears in list
7. Refresh browser
8. Verify task still visible (database persistence)

### 4. Complete User Journey Test
- [ ] Signup with new email
- [ ] Redirected to dashboard
- [ ] Dashboard shows stats (0 tasks)
- [ ] Click "Create Task"
- [ ] Fill form and submit
- [ ] Task appears in list
- [ ] Click edit on task
- [ ] Update task and save
- [ ] Changes reflected in list
- [ ] Toggle task completion
- [ ] Status updates
- [ ] Delete task
- [ ] Task removed from list
- [ ] Logout
- [ ] Login with same credentials
- [ ] Dashboard loads correctly

### 5. Security Verification
- [ ] Try accessing /dashboard without login → Redirected to /login
- [ ] Try API request without token → Receive 401
- [ ] Create task as User A, login as User B → Cannot see User A's tasks
- [ ] Token expires after configured time → Auto-logout

---

## Update Frontend with Backend URL

After backend is deployed, update Vercel environment variable:

1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Update `NEXT_PUBLIC_API_BASE_URL` with your backend URL
3. Redeploy frontend:
   ```bash
   vercel --prod
   ```

---

## Monitoring & Maintenance

### Backend Monitoring
- Railway: Check logs in Railway dashboard
- Render: Check logs in Render dashboard
- Fly.io: `fly logs`

### Database Monitoring
- Neon Dashboard → Monitoring tab
- Check connection count
- Monitor query performance
- Set up alerts for high usage

### Frontend Monitoring
- Vercel Dashboard → Analytics
- Monitor page load times
- Check error rates
- Review deployment logs

---

## Rollback Plan

### Frontend Rollback
```bash
# Vercel Dashboard → Deployments → Select previous deployment → Promote to Production
```

### Backend Rollback
```bash
# Railway
railway rollback

# Render
# Render Dashboard → Manual Deploy → Select previous commit

# Fly.io
fly releases
fly releases rollback <version>
```

---

## Common Issues & Solutions

### Issue 1: CORS Error
**Symptom**: Frontend can't connect to backend

**Solution**: Update backend CORS settings in `src/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-vercel-app.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue 2: Database Connection Timeout
**Symptom**: Backend fails to connect to Neon

**Solution**:
1. Verify DATABASE_URL is correct
2. Check Neon database is active
3. Verify connection pooling settings
4. Check if IP is whitelisted (Neon allows all by default)

### Issue 3: Environment Variables Not Loading
**Symptom**: Backend returns 500 errors

**Solution**:
1. Verify all required env vars are set
2. Restart backend service
3. Check logs for missing variable errors

---

## Production Checklist Summary

- [ ] Backend deployed and healthy
- [ ] Frontend deployed and accessible
- [ ] Database tables created
- [ ] Environment variables configured
- [ ] CORS configured for production domain
- [ ] Complete user journey tested
- [ ] Security verification passed
- [ ] Monitoring set up
- [ ] Rollback plan documented
- [ ] Team notified of deployment

---

## Deployment Complete! 🎉

Your Todo SaaS application is now live and ready for users.

**Frontend URL**: https://your-app.vercel.app
**Backend URL**: https://your-backend-url.com
**API Docs**: https://your-backend-url.com/docs

**Next Steps**:
1. Share URLs with stakeholders
2. Monitor initial user feedback
3. Set up error tracking (Sentry)
4. Plan Phase 3 features (AI integration)
