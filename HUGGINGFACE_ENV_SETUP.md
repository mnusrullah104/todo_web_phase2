# 🔧 Hugging Face Space Environment Variables - COPY & PASTE

## ⚠️ IMPORTANT: Copy these EXACTLY as shown (no line breaks!)

Go to: https://huggingface.co/spaces/mnusrulah104/todoapp_chatbot/settings

Click **"Repository secrets"** and add these 4 variables:

---

## 1. DATABASE_URL

**Name:** `DATABASE_URL`

**Value:** (Copy this entire line - NO line breaks!)
```
postgresql://neondb_owner:npg_hrqynGo9ZWJ5@ep-polished-water-ai6shq6e-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require
```

⚠️ **Critical**: Make sure there are NO line breaks in the URL. It must be one continuous line.

---

## 2. JWT_SECRET

**Name:** `JWT_SECRET`

**Value:**
```
8ZM]fwws%d<q8LCXlpl7djbkA)Oss&AH
```

---

## 3. COHERE_API_KEY

**Name:** `COHERE_API_KEY`

**Value:**
```
qXoZZDbJMKTd832LJY8XULmT14mHABaMCGMIjILh
```

---

## 4. FRONTEND_URL (Optional but recommended)

**Name:** `FRONTEND_URL`

**Value:**
```
https://taskflow-phase3-ai-chatbot.vercel.app
```

This allows your Vercel frontend to communicate with the backend.

---

## ✅ After Adding All Variables

1. Click **"Save"** for each variable
2. The Space will automatically rebuild (takes 1-2 minutes)
3. Check the logs to verify it starts successfully
4. Test the API: https://mnusrulah104-todoapp-chatbot.hf.space/docs

---

## 🔍 How to Verify It's Working

1. **Check Logs**: Go to your Space → "Logs" tab
2. **Look for**: "Database tables created successfully!"
3. **Test API**: Visit https://mnusrulah104-todoapp-chatbot.hf.space/health
4. **Expected Response**: `{"status": "healthy", "version": "1.0.0"}`

---

## 🚨 Common Mistakes to Avoid

❌ **DON'T**: Add line breaks in DATABASE_URL
❌ **DON'T**: Add quotes around the values
❌ **DON'T**: Add spaces before or after the values
❌ **DON'T**: Use the `psql` prefix in DATABASE_URL
❌ **DON'T**: Include `channel_binding=require` parameter

✅ **DO**: Copy and paste exactly as shown above
✅ **DO**: Verify each value after pasting
✅ **DO**: Wait for the Space to rebuild after adding variables

---

## 📝 Quick Checklist

- [ ] Go to Space Settings → Repository secrets
- [ ] Add `DATABASE_URL` (one line, no breaks)
- [ ] Add `JWT_SECRET`
- [ ] Add `COHERE_API_KEY`
- [ ] Add `FRONTEND_URL` (optional)
- [ ] Save all variables
- [ ] Wait for Space to rebuild
- [ ] Check logs for "Database tables created successfully!"
- [ ] Test /health endpoint
- [ ] Test your frontend at https://taskflow-phase3-ai-chatbot.vercel.app

---

## 🎯 Once Everything is Working

Your full-stack application will be live:
- **Frontend**: https://taskflow-phase3-ai-chatbot.vercel.app
- **Backend**: https://mnusrulah104-todoapp-chatbot.hf.space
- **API Docs**: https://mnusrulah104-todoapp-chatbot.hf.space/docs

You can then:
1. Sign up for an account
2. Create tasks
3. Use the AI chatbot to manage tasks with natural language
4. Navigate the app using voice commands
