# Hugging Face Spaces Deployment Guide
## Backend FastAPI Deployment

This guide provides step-by-step instructions for deploying the Todo Web Application backend to Hugging Face Spaces.

---

## 📋 Prerequisites

1. **Hugging Face Account**: Sign up at https://huggingface.co/join
2. **Git**: Installed on your machine
3. **Database**: Neon PostgreSQL database (or any PostgreSQL instance)
4. **Secrets**: Generated secure keys for production

---

## 🚀 Deployment Steps

### Step 1: Create a New Hugging Face Space

1. Go to https://huggingface.co/new-space
2. Fill in the details:
   - **Owner**: Your username
   - **Space name**: `todo-backend` (or your preferred name)
   - **License**: MIT
   - **Select the Space SDK**: **Docker**
   - **Space hardware**: CPU basic (free tier)
   - **Visibility**: Public (or Private if you have Pro)
3. Click **Create Space**

### Step 2: Clone Your Hugging Face Space Repository

```bash
# Clone the empty Space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/todo-backend
cd todo-backend
```

### Step 3: Copy Backend Files

Copy all files from the `backend` directory to your Space repository:

```bash
# From your project root
cp -r backend/* path/to/todo-backend/

# Or on Windows
xcopy /E /I backend path\to\todo-backend
```

Your Space repository should now contain:
```
todo-backend/
├── Dockerfile
├── requirements.txt
├── init_db.py
├── src/
│   ├── main.py
│   ├── config/
│   ├── api/
│   ├── models/
│   ├── schemas/
│   ├── auth/
│   └── database/
└── tests/
```

### Step 4: Create README.md for Your Space

Create a `README.md` file in the Space root:

```markdown
---
title: Todo Backend API
emoji: 📝
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# Todo Web Application Backend

FastAPI backend for the Todo Web Application with JWT authentication.

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/{user_id}/tasks` - Get all tasks
- `POST /api/{user_id}/tasks` - Create task
- `PUT /api/{user_id}/tasks/{task_id}` - Update task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete task

## Environment Variables

Configure these in Space Settings → Repository secrets:
- DATABASE_URL
- SECRET_KEY
- ALGORITHM
- ACCESS_TOKEN_EXPIRE_MINUTES
- BETTER_AUTH_SECRET
- BETTER_AUTH_URL
- BACKEND_URL
- FRONTEND_URL
```

### Step 5: Configure Environment Variables (Secrets)

1. Go to your Space → **Settings** → **Repository secrets**
2. Add each secret by clicking **Add a new secret**:

#### Required Secrets:

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db?sslmode=require` |
| `SECRET_KEY` | JWT signing key (32+ chars) | Generate with: `openssl rand -hex 32` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry time | `30` |
| `BETTER_AUTH_SECRET` | Auth service secret (32+ chars) | Generate with: `openssl rand -hex 32` |
| `BETTER_AUTH_URL` | Your Space URL | `https://YOUR_USERNAME-todo-backend.hf.space` |
| `BACKEND_URL` | Your Space URL | `https://YOUR_USERNAME-todo-backend.hf.space` |
| `FRONTEND_URL` | Vercel frontend URL | `https://your-app.vercel.app` |

**Important**:
- Generate new secure keys for `SECRET_KEY` and `BETTER_AUTH_SECRET`
- Use your actual Space URL (you'll get this after first deployment)
- Add your Vercel frontend URL to `FRONTEND_URL` (you can update this later)

#### Generate Secure Keys:

```bash
# On Linux/Mac/Git Bash
openssl rand -hex 32

# On Windows PowerShell
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))
```

### Step 6: Commit and Push to Hugging Face

```bash
# Add all files
git add .

# Commit
git commit -m "Initial backend deployment for Todo Web App"

# Push to Hugging Face
git push
```

### Step 7: Wait for Build

1. Go to your Space page: `https://huggingface.co/spaces/YOUR_USERNAME/todo-backend`
2. Watch the build logs in the **Logs** tab
3. Build typically takes 2-5 minutes
4. Once complete, you'll see "Running" status

### Step 8: Verify Deployment

Test your deployed backend:

```bash
# Health check
curl https://YOUR_USERNAME-todo-backend.hf.space/health

# Welcome message
curl https://YOUR_USERNAME-todo-backend.hf.space/

# Expected response:
# {"message": "Welcome to the Todo Web Application API"}
```

### Step 9: Update BETTER_AUTH_URL and BACKEND_URL

After first deployment, update these secrets with your actual Space URL:

1. Go to Settings → Repository secrets
2. Update `BETTER_AUTH_URL` to: `https://YOUR_USERNAME-todo-backend.hf.space`
3. Update `BACKEND_URL` to: `https://YOUR_USERNAME-todo-backend.hf.space`
4. Space will automatically restart

---

## 🔧 Troubleshooting

### Build Fails

**Check Dockerfile**:
- Ensure `Dockerfile` is in the root of your Space repository
- Verify it exposes port 7860 (required by HF Spaces)
- Check that all dependencies are in `requirements.txt`

**Check Logs**:
- Go to your Space → Logs tab
- Look for error messages during build

### Space Shows "Building" Forever

- Refresh the page
- Check if there are any errors in the logs
- Verify your Dockerfile syntax

### Database Connection Errors

**Verify DATABASE_URL**:
- Check that the connection string is correct
- Ensure your database allows connections from Hugging Face IPs
- For Neon: Enable "Allow connections from anywhere" in settings

**Test Connection**:
```bash
# From your local machine
psql "your-database-url-here"
```

### CORS Errors

**Update FRONTEND_URL**:
1. Go to Settings → Repository secrets
2. Update `FRONTEND_URL` with your Vercel URL
3. Space will restart automatically

**Multiple Frontend URLs**:
If you have multiple frontend URLs (staging, production), use comma-separated values:
```
FRONTEND_URL=https://app.vercel.app,https://staging.vercel.app
```

### Port Issues

Hugging Face Spaces **requires** port 7860. The Dockerfile is already configured correctly:
```dockerfile
EXPOSE 7860
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

### Space Sleeps After Inactivity

Free tier Spaces sleep after 48 hours of inactivity. To prevent this:
- Upgrade to a paid tier, or
- Set up a cron job to ping your Space every 24 hours

---

## 🔄 Updating Your Deployment

To update your backend after making changes:

```bash
# Make your changes locally
# Test them

# Commit and push
git add .
git commit -m "Description of changes"
git push

# Space will automatically rebuild
```

---

## 📊 Monitoring

### View Logs

1. Go to your Space page
2. Click on **Logs** tab
3. View real-time logs

### Check Status

```bash
# Health endpoint
curl https://YOUR_USERNAME-todo-backend.hf.space/health

# Should return:
# {"status": "healthy", "version": "1.0.0"}
```

---

## 🔒 Security Best Practices

1. **Never commit secrets** to the repository
2. **Use strong keys**: Minimum 32 characters for SECRET_KEY and BETTER_AUTH_SECRET
3. **Rotate secrets regularly**: Update keys every 90 days
4. **Restrict CORS**: Only allow your frontend URL in FRONTEND_URL
5. **Use HTTPS only**: Hugging Face provides this automatically
6. **Monitor logs**: Check for suspicious activity
7. **Database security**: Use strong passwords and restrict IP access

---

## 📝 API Documentation

Once deployed, access interactive API docs at:
- Swagger UI: `https://YOUR_USERNAME-todo-backend.hf.space/docs`
- ReDoc: `https://YOUR_USERNAME-todo-backend.hf.space/redoc`

---

## 🆘 Support

- **Hugging Face Docs**: https://huggingface.co/docs/hub/spaces
- **Hugging Face Discord**: https://hf.co/join/discord
- **FastAPI Docs**: https://fastapi.tiangolo.com

---

## ✅ Deployment Checklist

- [ ] Hugging Face account created
- [ ] Space created with Docker SDK
- [ ] Backend files copied to Space repository
- [ ] README.md created
- [ ] All 8 environment secrets configured
- [ ] Secure keys generated for SECRET_KEY and BETTER_AUTH_SECRET
- [ ] Database URL configured
- [ ] Code committed and pushed
- [ ] Build completed successfully
- [ ] Health check endpoint responding
- [ ] API documentation accessible
- [ ] CORS configured with frontend URL

---

**Your Backend URL**: `https://YOUR_USERNAME-todo-backend.hf.space`

Save this URL - you'll need it for Vercel frontend deployment!
