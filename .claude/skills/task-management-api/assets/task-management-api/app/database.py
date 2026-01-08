"""Database configuration and session management."""

import os

from dotenv import load_dotenv
from sqlmodel import Session, create_engine

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment variable
# For Neon: postgresql://user:password@ep-xxx.region.neon.tech/dbname?sslmode=require
# Fallback to SQLite for local development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")

# PostgreSQL requires different connection args than SQLite
if DATABASE_URL.startswith("postgresql"):
    engine = create_engine(DATABASE_URL, echo=False)
else:
    # SQLite needs check_same_thread=False for FastAPI
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False}
    )


def get_session():
    """Yield a database session."""
    with Session(engine) as session:
        yield session
