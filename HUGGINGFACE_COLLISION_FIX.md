# 🔴 URGENT: Fix Hugging Face Configuration Collision

## The Problem
Hugging Face is showing: **"Collision on variables and secrets names"**

This means you have the SAME variable name in BOTH:
- **Variables** section (public)
- **Secrets** section (private)

Hugging Face doesn't allow this - you must choose ONE location.

---

## ✅ SOLUTION: Use ONLY Secrets (Recommended)

### Step 1: Go to Space Settings
Visit: https://huggingface.co/spaces/mnusrulah104/todoapp_chatbot/settings

### Step 2: Remove ALL Variables from "Variables" Section

1. Scroll down to **"Variables"** section
2. You'll see variables like: DATABASE_URL, JWT_SECRET, COHERE_API_KEY, etc.
3. **DELETE EACH ONE** by clicking the trash icon
4. Leave the "Variables" section EMPTY

### Step 3: Keep ONLY "Repository Secrets"

Scroll to **"Repository secrets"** section and verify you have these 4 secrets:

**1. DATABASE_URL**
```
postgresql://neondb_owner:npg_hrqynGo9ZWJ5@ep-polished-water-ai6shq6e-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require
```
⚠️ Make sure this is ONE LINE with NO breaks!

**2. JWT_SECRET**
```
8ZM]fwws%d<q8LCXlpl7djbkA)Oss&AH
```

**3. COHERE_API_KEY**
```
qXoZZDbJMKTd832LJY8XULmT14mHABaMCGMIjILh
```

**4. FRONTEND_URL** (optional)
```
https://taskflow-phase3-ai-chatbot.vercel.app
```

### Step 4: Save and Wait for Rebuild

1. After deleting all Variables, the Space will automatically rebuild
2. Wait 1-2 minutes
3. Check the logs for: "Database tables created successfully!"

---

## 🎯 Why This Happens

Hugging Face Spaces has TWO places to store environment variables:

**Variables (Public):**
- Visible in the Space's public settings
- Anyone can see these values
- ❌ NOT secure for passwords/secrets

**Secrets (Private):**
- Encrypted and hidden
- Only you can see these values
- ✅ Secure for passwords/API keys

You accidentally added the same variable names to BOTH sections, causing a collision.

---

## 📋 Quick Checklist

- [ ] Go to Space Settings
- [ ] Delete ALL items from "Variables" section
- [ ] Verify "Repository secrets" has 4 secrets
- [ ] Verify DATABASE_URL is one line (no breaks)
- [ ] Wait for Space to rebuild
- [ ] Check logs for success message
- [ ] Test: https://mnusrulah104-todoapp-chatbot.hf.space/health

---

## 🔍 After Fixing

Once the backend is running:
1. Test health endpoint: https://mnusrulah104-todoapp-chatbot.hf.space/health
2. Should return: `{"status": "healthy", "version": "1.0.0"}`
3. Your frontend will automatically work: https://taskflow-phase3-ai-chatbot.vercel.app

---

## 📸 Visual Guide

**BEFORE (Wrong - Has Collision):**
```
Variables:
  - DATABASE_URL = postgresql://...
  - JWT_SECRET = ...

Secrets:
  - DATABASE_URL = postgresql://...  ← COLLISION!
  - JWT_SECRET = ...                 ← COLLISION!
```

**AFTER (Correct - No Collision):**
```
Variables:
  (empty)

Secrets:
  - DATABASE_URL = postgresql://...
  - JWT_SECRET = ...
  - COHERE_API_KEY = ...
  - FRONTEND_URL = ...
```

---

**Go fix this now and your backend will start working immediately!**
