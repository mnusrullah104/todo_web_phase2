from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import router as api_router
from .config.settings import get_settings

settings = get_settings()

app = FastAPI(
    title="Todo Web Application API",
    description="A production-ready multi-user Todo Web Application with authentication and task management",
    version="1.0.0",
)

# Configure CORS - dynamically build allowed origins
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
]

# Add production frontend URLs from environment
if settings.frontend_url:
    # Support comma-separated list of URLs
    frontend_urls = [url.strip() for url in settings.frontend_url.split(",")]
    allowed_origins.extend(frontend_urls)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo Web Application API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}