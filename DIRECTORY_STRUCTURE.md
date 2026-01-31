# 📁 Project Directory Structure

## Root Directory Layout

```
todo_web_phase2/
├── backend/                    # FastAPI backend application
├── frontend/                   # Next.js frontend application
├── docs/                       # All documentation
│   ├── deployment/            # Deployment guides and instructions
│   ├── reports/               # Project reports and summaries
│   └── research-paper/        # Research paper materials
├── scripts/                    # Utility scripts
├── skills/                     # Claude Code skill files
├── specs/                      # Feature specifications
├── history/                    # Prompt history records
├── .claude/                    # Claude Code configuration
├── .specify/                   # Specify framework files
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── CLAUDE.md                  # Claude Code instructions
├── docker-compose.yml         # Docker Compose configuration
├── package-lock.json          # Root package lock
└── README.md                  # Main project README
```

---

## 📂 Directory Details

### `/backend`
FastAPI backend with PostgreSQL database integration.

**Key Files:**
- `Dockerfile` - Docker configuration (port 7860 for Hugging Face)
- `requirements.txt` - Python dependencies
- `src/main.py` - FastAPI application entry point
- `src/config/settings.py` - Environment configuration
- `src/api/` - API route handlers
- `src/models/` - Database models
- `src/schemas/` - Pydantic schemas
- `tests/` - Backend tests

### `/frontend`
Next.js 16 frontend with App Router and Tailwind CSS.

**Key Files:**
- `package.json` - Node.js dependencies
- `next.config.js` - Next.js configuration
- `src/app/` - App Router pages
- `src/components/` - React components
- `src/lib/` - Utility functions and API client
- `tailwind.config.js` - Tailwind CSS configuration

### `/docs`
All project documentation organized by category.

#### `/docs/deployment`
Deployment guides and instructions:
- `DEPLOYMENT_CREDENTIALS_GUIDE.md` - Credentials reference
- `DEPLOYMENT_EXECUTION_GUIDE.md` - Step-by-step deployment workflow
- `DEPLOYMENT_STATUS_REPORT.md` - Deployment preparation status
- `EXECUTIVE_SUMMARY.md` - Executive summary and action plan
- `FINAL_DEPLOYMENT_SUMMARY.md` - Complete deployment summary
- `README_HF_DEPLOYMENT.md` - Hugging Face Spaces guide
- `README_VERCEL_DEPLOYMENT.md` - Vercel deployment guide

#### `/docs/reports`
Project reports and implementation summaries:
- `BACKEND_ERROR_FIX.md` - Backend error fixes
- `BACKEND_FIX.md` - Backend improvements
- `COMPLETE_REPORT.md` - Complete project report
- `FINAL_SUMMARY.md` - Final implementation summary
- `FINAL_UI_UX_REPORT.md` - UI/UX improvements report
- `IMPLEMENTATION_SUMMARY.md` - Implementation overview
- `LANDING_PAGE_ENHANCEMENTS.md` - Landing page updates
- `NAVBAR_ENHANCEMENTS.md` - Navigation improvements
- `PREMIUM_REDESIGN.md` - Premium features redesign
- `PROJECT_REPORT.md` - Comprehensive project report
- `RESPONSIVE_DESIGN.md` - Responsive design implementation
- `SAAS_IMPLEMENTATION_COMPLETE.md` - SaaS features completion
- `SAAS_REDESIGN_PLAN.md` - SaaS redesign planning
- `UI_UX_IMPROVEMENTS.md` - UI/UX enhancement details

#### `/docs/research-paper`
Research paper materials and references.

### `/scripts`
Utility scripts for development and deployment:
- `start.bat` - Windows startup script
- `start.sh` - Unix/Linux startup script

### `/skills`
Claude Code skill files for specialized development workflows:
- `ai_mcp_integrator.skill` - AI and MCP integration specialist
- `cloud_native_devops.skill` - Cloud-native DevOps specialist
- `frontend_architect.skill` - Frontend architecture specialist
- `python_specialist.skill` - Python/FastAPI specialist
- `qa_specialist.skill` - Quality assurance specialist

### `/specs`
Feature specifications and planning documents:
- `001-ai-k12-efficiency/` - AI K-12 efficiency research
- `002-todo-web-app/` - Todo web application specifications

### `/history`
Prompt history records for development tracking:
- `prompts/` - Organized by feature and stage

### `/.claude`
Claude Code configuration and templates.

### `/.specify`
Specify framework configuration:
- `memory/constitution.md` - Project principles
- `templates/` - Document templates
- `scripts/` - Specify scripts

---

## 🚀 Quick Start

### Local Development

**Backend:**
```bash
cd backend
python -m uvicorn src.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Docker Compose:**
```bash
docker-compose up
```

### Deployment

See deployment guides in `/docs/deployment/`:
1. Start with `DEPLOYMENT_EXECUTION_GUIDE.md`
2. Follow `README_HF_DEPLOYMENT.md` for backend
3. Follow `README_VERCEL_DEPLOYMENT.md` for frontend

---

## 📝 Key Files

### Configuration Files
- `.env.example` - Environment variables template (never commit real .env)
- `docker-compose.yml` - Multi-container Docker setup
- `CLAUDE.md` - Claude Code development instructions

### Documentation Entry Points
- `README.md` - Main project overview (this file)
- `docs/deployment/EXECUTIVE_SUMMARY.md` - Deployment quick start
- `docs/reports/PROJECT_REPORT.md` - Comprehensive project report

---

## 🔒 Security Notes

- Never commit `.env` files with real credentials
- Use `.env.example` as a template only
- All secrets should be configured via environment variables
- See `docs/deployment/DEPLOYMENT_CREDENTIALS_GUIDE.md` for details

---

## 📊 Project Status

- ✅ Backend: Production ready
- ✅ Frontend: Production ready
- ✅ Documentation: Complete (2,500+ lines)
- ⏳ Deployment: Awaiting user action

See `docs/deployment/DEPLOYMENT_STATUS_REPORT.md` for detailed status.

---

## 🆘 Support

- **Deployment Issues**: See `/docs/deployment/` guides
- **Development Issues**: See `/docs/reports/` for implementation details
- **Feature Specs**: See `/specs/` for detailed specifications

---

**Repository**: https://github.com/mnusrullah104/todo_web_phase2.git
