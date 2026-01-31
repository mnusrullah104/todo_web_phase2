# 🎯 STEP-BY-STEP: Run Deployment Script

**Current Directory**: D:\mna\hackathon_2

---

## 📋 Before You Start

### 1. Get Your Hugging Face Token

1. Go to: https://huggingface.co/settings/tokens
2. Click **"New token"**
3. Name: `deploy-todo-backend`
4. Type: **Write** (important!)
5. Click **"Generate"**
6. **Copy the token** - you'll need it in a moment

---

## 🚀 Run the Deployment

### Open Command Prompt

**Press**: `Win + R`
**Type**: `cmd`
**Press**: Enter

### Navigate to Project

```cmd
cd D:\mna\hackathon_2
```

### Run the Script

```cmd
deploy_to_hf.bat
```

---

## 📝 What Will Happen

### Step 1: HF CLI Check
```
🚀 Deploying Backend to Hugging Face Spaces
============================================

📋 Configuration:
   Username: mnusrulah104
   Space: todo-backend
   URL: https://huggingface.co/spaces/mnusrulah104/todo-backend

📦 Installing huggingface-cli... (if needed)
```

### Step 2: Login Prompt
```
🔐 Please login to Hugging Face...
   You'll need your HF access token
   Get it from: https://huggingface.co/settings/tokens

Token:
```

**Paste your token here** (it won't show as you type - this is normal)

### Step 3: Clone Space
```
📥 Cloning your Space...
Cloning into 'todo-backend'...
```

### Step 4: Copy Files
```
📂 Copying backend files...
Copying: Dockerfile
Copying: requirements.txt
Copying: src/main.py
... (all backend files)
```

### Step 5: Create README
```
📝 Creating README.md...
```

### Step 6: Push to HF
```
📤 Pushing to Hugging Face...
[main abc1234] Deploy Todo Backend API
 50 files changed, 1000 insertions(+)
Pushing to https://huggingface.co/spaces/mnusrulah104/todo-backend
```

### Step 7: Success
```
✅ Deployment initiated!

📋 Next steps:
   1. Go to: https://huggingface.co/spaces/mnusrulah104/todo-backend/settings
   2. Configure environment secrets (8 variables)
   3. Wait for build to complete (3-5 minutes)
   4. Test: curl https://mnusrulah104-todo-backend.hf.space/health

🎉 Done!
```

---

## ⚠️ If You See Errors

### "huggingface-cli: command not found"
**Fix**: Script will install it automatically

### "Authentication failed"
**Fix**: Make sure you copied the full token

### "Permission denied"
**Fix**: Make sure token has **Write** access

### "Directory already exists"
**Fix**: Script will remove and re-clone

---

## ✅ After Script Completes

### Configure Secrets (IMPORTANT!)

1. Go to: https://huggingface.co/spaces/mnusrulah104/todo-backend/settings
2. Scroll to **"Repository secrets"**
3. Add these 8 secrets:

**Generate these first:**
```cmd
openssl rand -hex 32
openssl rand -hex 32
```

| Secret Name | Value |
|-------------|-------|
| `DATABASE_URL` | Your Neon PostgreSQL URL |
| `SECRET_KEY` | First openssl output |
| `ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` |
| `BETTER_AUTH_SECRET` | Second openssl output |
| `BETTER_AUTH_URL` | `https://mnusrulah104-todo-backend.hf.space` |
| `BACKEND_URL` | `https://mnusrulah104-todo-backend.hf.space` |
| `FRONTEND_URL` | `http://todo-web-phase2.vercel.app` |

### Wait for Build

1. Go to: https://huggingface.co/spaces/mnusrulah104/todo-backend
2. Click **"Logs"** tab
3. Watch build progress (3-5 minutes)
4. Wait for status: **"Running"**

### Test Backend

```cmd
curl https://mnusrulah104-todo-backend.hf.space/health
```

**Expected**: `{"status": "healthy", "version": "1.0.0"}`

---

## 🎯 Ready to Start?

**Open Command Prompt and run:**

```cmd
cd D:\mna\hackathon_2
deploy_to_hf.bat
```

**Have your HF token ready!**

---

**Let me know when you've run the script and I'll help with the next steps!**
