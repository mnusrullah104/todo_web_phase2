# 🎯 COPY & PASTE THESE COMMANDS

All files are prepared in `hf-space-ready/` directory.

---

## 📋 STEP 1: Get Your HF Token

Go to: https://huggingface.co/settings/tokens
- Click "New token"
- Name: `deploy-todo-backend`
- Type: **Write**
- Copy the token

---

## 🚀 STEP 2: Run These Commands

**Open Command Prompt (Win+R, type `cmd`, Enter)**

```cmd
cd D:\mna\hackathon_2

pip install huggingface-hub

huggingface-cli login
```

*Paste your token when prompted*

```cmd
git clone https://huggingface.co/spaces/mnusrulah104/todo-backend

xcopy /E /I /Y hf-space-ready\* todo-backend\

cd todo-backend

git add .

git commit -m "Deploy Todo Backend API"

git push
```

---

## ⚙️ STEP 3: Configure Secrets

Go to: https://huggingface.co/spaces/mnusrulah104/todo-backend/settings

**Generate secrets:**
```cmd
openssl rand -hex 32
openssl rand -hex 32
```

**Add 8 secrets:**
1. `DATABASE_URL` - Your Neon URL
2. `SECRET_KEY` - First openssl output
3. `ALGORITHM` - `HS256`
4. `ACCESS_TOKEN_EXPIRE_MINUTES` - `30`
5. `BETTER_AUTH_SECRET` - Second openssl output
6. `BETTER_AUTH_URL` - `https://mnusrulah104-todo-backend.hf.space`
7. `BACKEND_URL` - `https://mnusrulah104-todo-backend.hf.space`
8. `FRONTEND_URL` - `http://todo-web-phase2.vercel.app`

---

## ✅ STEP 4: Wait & Test

Wait 3-5 minutes for build, then:

```cmd
curl https://mnusrulah104-todo-backend.hf.space/health
```

Expected: `{"status": "healthy", "version": "1.0.0"}`

---

## 🔧 STEP 5: Fix Vercel

1. Go to: https://vercel.com/dashboard
2. Click: `todo-web-phase2` → Settings → General
3. Root Directory → Edit → `frontend` → Save
4. Deployments → Latest → ... → Redeploy

---

**DONE!** Your app will be live at:
- Frontend: http://todo-web-phase2.vercel.app
- Backend: https://mnusrulah104-todo-backend.hf.space
