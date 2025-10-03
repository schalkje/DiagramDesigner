"""Database session factory and utilities."""
import os
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from ..models import Base

# Get database URL from environment variable
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://diagramdesigner:diagramdesigner@localhost:5432/diagramdesigner",
)

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using them
    pool_size=10,  # Number of connections to maintain
    max_overflow=20,  # Maximum number of connections to create beyond pool_size
    echo=False,  # Set to True to log all SQL statements (useful for debugging)
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Initialize the database by creating all tables.

    This is useful for testing or initial setup.
    For production, use Alembic migrations instead.
    """
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Get database session for dependency injection.

    Yields:
        Session: SQLAlchemy database session

    Example:
        ```python
        def some_function(db: Session = Depends(get_db)):
            # Use db session
            pass
        ```
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context() -> Generator[Session, None, None]:
    """Get database session as context manager.

    Yields:
        Session: SQLAlchemy database session

    Example:
        ```python
        with get_db_context() as db:
            # Use db session
            pass
        ```
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def close_db() -> None:
    """Close all database connections.

    Useful for cleanup in tests or application shutdown.
    """
    engine.dispose()
