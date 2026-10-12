"""Database engine and session management.

Why this approach:

- SQLAlchemy's engine maintains a connection pool (QueuePool by default)
  rather than opening a new TCP connection to MySQL on every request.
- Pool size, overflow, timeout, and recycle settings are configurable
  through environment variables.
- pool_pre_ping=True checks that a pooled connection is alive before
  handing it to a request.
- Sessions are created per request through the get_db dependency
  and always closed in a finally block to prevent connection leaks.
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings


settings = get_settings()

engine = create_engine(
    settings.database_url,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    pool_timeout=settings.db_pool_timeout,
    pool_recycle=settings.db_pool_recycle,
    pool_pre_ping=True,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)


class Base(DeclarativeBase):
    """Base class for all ORM models."""


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a DB session and guarantees cleanup."""
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()