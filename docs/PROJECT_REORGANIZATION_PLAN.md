# 🏗️ Project Structure Reorganization Plan

## Current Issues
1. ❌ Duplicate `src/` folders (root and backend)
2. ❌ Duplicate `tests/` folders (root and backend)
3. ❌ Too many markdown files at root
4. ❌ Old deployment artifacts (`hf-space-ready/`)
5. ❌ Duplicate `init_db.py` files
6. ❌ Messy root directory

## Target Structure (Industry Best Practices)

```
phase3_chatboat/
├── backend/                    # FastAPI Backend
│   ├── src/
│   │   ├── api/               # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── tasks.py
│   │   │   └── chat.py
│   │   ├── models/            # Database models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── task.py
│   │   │   ├── conversation.py
│   │   │   └── message.py
│   │   ├── schemas/           # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   └── task.py
│   │   ├── auth/              # Authentication
│   │   │   ├── __init__.py
│   │   │   └── jwt.py
│   │   ├── config/            # Configuration
│   │   │   ├── __init__.py
│   │   │   └── settings.py
│   │   ├── database/          # Database setup
│   │   │   ├── __init__.py
│   │   │   └── session.py
│   │   ├── middleware/        # Middleware (NEW)
│   │   │   ├── __init__.py
│   │   │   └── error_handler.py
│   │   ├── mcp/               # MCP tools (Phase 3)
│   │   │   ├── __init__.py
│   │   │   ├── tool_executor.py
│   │   │   └── tools/
│   │   ├── agent/             # AI Agent (Phase 3)
│   │   │   ├── __init__.py
│   │   │   ├── cohere_client.py
│   │   │   └── todo_agent.py
│   │   └── main.py            # FastAPI app entry
│   ├── tests/                 # Backend tests
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   └── test_tasks.py
│   ├── scripts/               # Utility scripts
│   │   └── init_db.py
│   ├── .env.example
│   ├── requirements.txt
│   ├── pyproject.toml
│   └── README.md
│
├── frontend/                   # Next.js Frontend
│   ├── src/
│   │   ├── app/               # Next.js 14+ App Router
│   │   │   ├── (auth)/        # Auth routes group
│   │   │   │   ├── login/
│   │   │   │   └── signup/
│   │   │   ├── dashboard/
│   │   │   ├── tasks/
│   │   │   ├── calendar/
│   │   │   ├── analytics/
│   │   │   ├── settings/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   └── globals.css
│   │   ├── components/        # React components
│   │   │   ├── ui/            # Reusable UI components
│   │   │   ├── tasks/         # Task-specific components
│   │   │   ├── ChatWidget.tsx # Phase 3 chatbot
│   │   │   └── ClientLayout.tsx
│   │   ├── contexts/          # React contexts
│   │   │   ├── ThemeContext.tsx
│   │   │   └── ToastContext.tsx (NEW)
│   │   ├── hooks/             # Custom hooks
│   │   │   └── useTaskMetadata.ts
│   │   ├── lib/               # Utilities
│   │   │   ├── api.ts         # API client (ENHANCED)
│   │   │   ├── auth.ts
│   │   │   └── types.ts
│   │   └── styles/            # Global styles
│   ├── public/                # Static assets
│   ├── .env.local.example
│   ├── next.config.js
│   ├── package.json
│   ├── tsconfig.json
│   └── README.md
│
├── docs/                       # Documentation (ORGANIZED)
│   ├── README.md              # Main documentation
│   ├── QUICKSTART.md
│   ├── STARTUP_GUIDE.md
│   ├── TESTING_GUIDE.md
│   ├── deployment/
│   │   ├── VERCEL_DEPLOYMENT_GUIDE.md
│   │   └── MANUAL_DEPLOYMENT_STEPS.md
│   ├── phase3/
│   │   ├── README_PHASE3.md
│   │   └── IMPLEMENTATION_SUMMARY.md
│   └── summaries/
│       ├── COMPLETE_FIX_SUMMARY.md
│       ├── FINAL_SUMMARY.md
│       ├── MVP_TESTING_RESULTS.md
│       └── ERROR_HANDLING_COMPLETE.md
│
├── scripts/                    # Project-level scripts
│   ├── start-all.bat
│   ├── deploy_clean.sh
│   └── deploy_to_hf.bat
│
├── .github/                    # GitHub workflows (optional)
│   └── workflows/
│
├── .gitignore
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── README.md                   # Main project README
└── LICENSE

## Files to Remove/Archive
- ❌ `/src/` (old backend code - duplicate)
- ❌ `/tests/` (old tests - duplicate)
- ❌ `/hf-space-ready/` (deployment artifact)
- ❌ `/init_db.py` (duplicate - keep in backend/scripts/)
- ❌ `/requirements.txt` (duplicate - keep in backend/)
- ❌ `/package-lock.json` at root (not needed)
- ❌ `/nul` (Windows artifact)
- ❌ `/test-chatbot.html` (move to docs/examples/)

## Actions to Take
1. ✅ Create `docs/` folder structure
2. ✅ Move all markdown files to appropriate docs/ subfolders
3. ✅ Remove duplicate folders
4. ✅ Organize scripts
5. ✅ Clean root directory
6. ✅ Update README.md with new structure
7. ✅ Create comprehensive .gitignore
