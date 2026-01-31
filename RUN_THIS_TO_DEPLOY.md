# 🚀 Deploy Backend to Hugging Face - YOU Run This

I've prepared deployment scripts for you. **You need to run these yourself** because I cannot access Hugging Face with your credentials.

---

## 📋 What I Prepared

✅ **deploy_to_hf.bat** - Windows deployment script
✅ **deploy_to_hf.sh** - Linux/Mac deployment script

These scripts will:
1. Install HF CLI (if needed)
2. Login with your HF token
3. Clone your Space
4. Copy backend files
5. Create README.md
6. Push to Hugging Face

---

## 🎯 How to Deploy (Choose Your OS)

### Option A: Windows

```cmd
cd D:\mna\hackathon_2
deploy_to_hf.bat
```

### Option B: Linux/Mac

```bash
cd /path/to/hackathon_2
chmod +x deploy_to_hf.sh
./deploy_to_hf.sh
```

---

## 🔑 You'll Need

**Hugging Face Access Token**:
1. Go to: https://huggingface.co/settings/tokens
2. Click "New token"
3. Name: `deploy-todo-backend`
4. Type: Write
5. Copy the token
6. Paste when script asks for login

---

## ⚙️ After Script Runs

### Configure Secrets (IMPORTANT!)

Go to: https://huggingface.co/spaces/mnusrulah104/todo-backend/settings

Add these 8 secrets:

| Secret Name | Value |
|-------------|-------|
| `DATABASE_URL` | Your Neon PostgreSQL URL |
| `SECRET_KEY` | Run: `openssl rand -hex 32` |
| `ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` |
| `BETTER_AUTH_SECRET` | Run: `openssl rand -hex 32` |
| `BETTER_AUTH_URL` | `https://mnusrulah104-todo-backend.hf.space` |
| `BACKEND_URL` | `https://mnusrulah104-todo-backend.hf.space` |
| `FRONTEND_URL` | `http://todo-web-phase2.vercel.app` |

---

## ✅ Verify Deployment

After build completes (3-5 minutes):

```bash
curl https://mnusrulah104-todo-backend.hf.space/health
```

Expected: `{"status": "healthy", "version": "1.0.0"}`

---

## 🐛 If Script Fails

### Manual Deployment

```bash
# 1. Install HF CLI
pip install huggingface-hub

# 2. Login
huggingface-cli login

# 3. Clone Space
git clone https://huggingface.co/spaces/mnusrulah104/todo-backend
cd todo-backend

# 4. Copy files
xcopy /E /I ..\backend\* .

# 5. Add README
copy ..\HF_SPACE_README.md README.md

# 6. Push
git add .
git commit -m "Deploy Backend"
git push
```

---

## 📞 Why Can't I Do This For You?

I'm an AI assistant running locally on your machine. I can:
- ✅ Read local files
- ✅ Create scripts
- ✅ Run local commands

I cannot:
- ❌ Authenticate with external services
- ❌ Access your HF token
- ❌ Push to remote repositories

**You need to run the script with your credentials.**

---

## 🎯 Your Action

**Run this now**:
```cmd
cd D:\mna\hackathon_2
deploy_to_hf.bat
```

Then let me know if you encounter any errors!
