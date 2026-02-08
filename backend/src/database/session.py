from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from sqlmodel import Session
from ..config.settings import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

try:
    logger.info(f"Connecting to database: {settings.database_url[:30]}...")
    engine = create_engine(
        settings.database_url,
        poolclass=QueuePool,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=False,  # Set to True for SQL query logging
    )
    logger.info("Database engine created successfully")
except Exception as e:
    logger.error(f"Failed to create database engine: {str(e)}")
    raise

def get_session():
    try:
        with Session(engine) as session:
            yield session
    except Exception as e:
        logger.error(f"Database session error: {str(e)}")
        raise