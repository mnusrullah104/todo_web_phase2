"""
Database initialization script to create all tables in PostgreSQL.
Run this script to set up the database schema.
"""
from sqlmodel import SQLModel
from src.database.session import engine
from src.models.user import User
from src.models.task import Task

def init_db():
    """Create all database tables."""
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("[SUCCESS] Database tables created successfully!")
    print("[SUCCESS] Users table created")
    print("[SUCCESS] Tasks table created")

if __name__ == "__main__":
    init_db()
