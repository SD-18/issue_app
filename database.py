from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager
from config import Config
import logging

# Configure logging for database operations
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Replace with your database connection URL
DATABASE_URL = Config.DATABASE_URL

# Validate DATABASE_URL
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Check your configuration.")

try:
    # Create database engine with additional options
    engine = create_engine(
    DATABASE_URL,  # Example: "mysql+pymysql://username:password@host:port/database"
    pool_pre_ping=True,  # Ensures connections are valid and usable
    future=True  # Enables SQLAlchemy 2.0-style usage
    )

    logging.info("Database engine created successfully.")
except Exception as e:
    logging.error(f"Failed to create database engine: {e}")
    raise RuntimeError("Database connection failed.")

# Base class for ORM models
Base = declarative_base()

# Session factory with fine-tuned options
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

# Context manager for session handling
@contextmanager
def get_db_session():
    """
    Provides a transactional scope around a series of database operations.
    Automatically handles commit, rollback, and session cleanup.
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logging.error(f"Error during database transaction: {e}")
        raise
    finally:
        session.close()
        logging.info("Database session closed.")

# Context manager for session handling
@contextmanager
def get_db_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()