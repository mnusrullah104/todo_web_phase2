try:
    from pydantic_settings import BaseSettings
    SETTINGS_MODULE = "pydantic_settings"
except ImportError:
    from pydantic import BaseSettings
    SETTINGS_MODULE = "pydantic"

from functools import lru_cache

class Settings(BaseSettings):
    database_url: str = "sqlite:///./test.db"  # Use SQLite for easier testing
    secret_key: str = "your-super-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    if SETTINGS_MODULE == "pydantic":
        class Config:
            env_file = ".env"
    else:
        model_config = {"env_file": ".env"}

@lru_cache()
def get_settings():
    return Settings()