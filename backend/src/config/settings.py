try:
    from pydantic_settings import BaseSettings
    SETTINGS_MODULE = "pydantic_settings"
except ImportError:
    from pydantic import BaseSettings
    SETTINGS_MODULE = "pydantic"

from functools import lru_cache
import os

class Settings(BaseSettings):
    # Database configuration
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")

    # JWT configuration
    secret_key: str = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # Better Auth configuration
    better_auth_secret: str = os.getenv("BETTER_AUTH_SECRET", "")
    better_auth_url: str = os.getenv("BETTER_AUTH_URL", "http://localhost:8000")

    # Backend URL for CORS
    backend_url: str = os.getenv("BACKEND_URL", "http://localhost:8000")

    # Frontend URL for CORS (can be comma-separated list)
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:3000")

    # Cohere API configuration (Phase III - AI Chatbot)
    cohere_api_key: str = os.getenv("COHERE_API_KEY", "")

    if SETTINGS_MODULE == "pydantic":
        class Config:
            env_file = ".env"
            case_sensitive = False
    else:
        model_config = {
            "env_file": ".env",
            "case_sensitive": False
        }

@lru_cache()
def get_settings():
    return Settings()