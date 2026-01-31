from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from sqlmodel import Session
from ..config.settings import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=300,
)

def get_session():
    with Session(engine) as session:
        yield session