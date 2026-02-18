# Project Structure

This document describes the clean, organized structure of the Phase III Todo AI Chatbot project.

## Root Directory Structure

```
phase3_chatboat/
├── backend/                    # FastAPI backend application
│   ├── app/                   # Main application code
│   ├── tests/                 # Backend tests
│   ├── alembic/              # Database migrations
│   └── pyproject.toml        # Python dependencies
│
├── frontend/                   # Next.js frontend application
│   ├── src/                   # Source code
│   ├── public/                # Static assets
│   └── package.json          # Node dependencies
│
├── specs/                      # Feature specifications
│   ├── phase3-chatbot/       # Chatbot feature specs
│   ├── api/                  # API specifications
│   ├── database/             # Database schemas
│   └── ui/                   # UI/UX specifications
│
├── docs/                       # Project documentation
│   ├── deployment/           # Deployment guides
│   ├── development/          # Development guides
│   └── architecture/         # Architecture docs
│
├── scripts/                    # Utility scripts
│   ├── setup/                # Setup scripts
│   ├── deployment/           # Deployment scripts
│   └── maintenance/          # Maintenance scripts
│
├── skills/                     # Claude Code skills
│   └── [skill-name]/         # Individual skill definitions
│
├── history/                    # Project history
│   ├── prompts/              # Prompt History Records
│   └── adr/                  # Architecture Decision Records
│
├── .specify/                   # SpecKit Plus configuration
│   ├── memory/               # Project memory
│   ├── templates/            # Document templates
│   └── scripts/              # SpecKit scripts
│
├── .env.example               # Environment variables template
├── docker-compose.yml         # Docker composition
├── Dockerfile                 # Docker image definition
├── vercel.json               # Vercel deployment config
├── CLAUDE.md                 # Claude Code instructions
└── README.md                 # Project overview
```

## Directory Purposes

### `/backend`
FastAPI backend with:
- RESTful API endpoints
- Database models (SQLModel)
- JWT authentication
- MCP server integration
- OpenAI Agents SDK integration

### `/frontend`
Next.js 14+ frontend with:
- App Router architecture
- TypeScript + Tailwind CSS
- ChatKit UI components
- API integration layer

### `/specs`
Specification-driven development artifacts:
- Feature specifications
- API contracts
- Database schemas
- UI/UX requirements

### `/docs`
Comprehensive documentation:
- Deployment guides
- Development setup
- Architecture decisions
- API documentation

### `/scripts`
Automation and utility scripts:
- Environment setup
- Database migrations
- Deployment automation
- Testing utilities

### `/skills`
Claude Code custom skills:
- AI/MCP integration specialist
- Cloud/DevOps specialist
- Frontend architect
- Python specialist
- QA specialist

### `/history`
Project development history:
- Prompt History Records (PHRs)
- Architecture Decision Records (ADRs)
- Development timeline

### `/.specify`
SpecKit Plus framework:
- Project constitution
- Document templates
- Workflow scripts
- Memory artifacts

## Configuration Files

| File | Purpose |
|------|---------|
| `.env.example` | Environment variables template |
| `docker-compose.yml` | Multi-container Docker setup |
| `Dockerfile` | Backend container definition |
| `vercel.json` | Frontend deployment config |
| `.gitignore` | Git exclusion rules |
| `.dockerignore` | Docker exclusion rules |
| `CLAUDE.md` | Claude Code behavior rules |
| `README.md` | Project overview and setup |

## Documentation Organization

All documentation files should be organized under `/docs`:

```
docs/
├── deployment/
│   ├── huggingface.md        # HuggingFace deployment
│   ├── vercel.md             # Vercel deployment
│   └── environment.md        # Environment setup
│
├── development/
│   ├── setup.md              # Local development setup
│   ├── database.md           # Database management
│   └── testing.md            # Testing guidelines
│
└── architecture/
    ├── overview.md           # System architecture
    ├── api.md                # API design
    └── security.md           # Security considerations
```

## Best Practices

1. **Separation of Concerns**: Keep backend, frontend, and documentation separate
2. **Clear Naming**: Use descriptive directory and file names
3. **Documentation**: Keep docs organized by category
4. **Configuration**: Use `.env` files, never commit secrets
5. **Version Control**: Follow `.gitignore` rules strictly
6. **Modularity**: Each directory should have a clear, single purpose

## Navigation Tips

- Start with `README.md` for project overview
- Check `/specs` for feature requirements
- Review `/docs` for detailed guides
- Explore `/backend` and `/frontend` for implementation
- Reference `/history` for development decisions

## Maintenance

- Keep documentation up-to-date
- Archive old deployment guides
- Update structure as project evolves
- Document major architectural changes in ADRs
