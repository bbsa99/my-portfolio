# CloudForge API Gateway - Database Configuration
"""SQLAlchemy database configuration with async session management."""

from sqlalchemy import create_engine, event
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from ...core.config import Settings


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    
    pass


# Create async engine for PostgreSQL
engine: AsyncEngine = create_async_engine(
    Settings.postgres_dsn,
    echo=Settings.debug,
    future=True,
    pool_size=Settings.postgres_pool_max,
    max_overflow=Settings.postgres_pool_max - Settings.postgres_pool_min,
    pool_timeout=30,
    pool_pre_ping=True,
    pool_recycle=3600,
)


# Create session factory
async_session_factory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


# Getter for the engine
async def get_engine() -> AsyncEngine:
    """Get the async database engine."""
    return engine


# Getter for the session factory
def get_session_factory():
    """Get the session factory."""
    return async_session_factory


# Context manager for getting a database session
async def get_session():
    """Get an async database session."""
    async with async_session_factory() as session:
        yield session


# Utility function to close the engine
async def close_engine():
    """Close the database engine."""
    await engine.dispose()


# Event listeners for connection pool logging
@event.listens_for(engine.sync_engine, "connect")
def connect(dbapi_connection, connection_record):
    """Log database connection establishment."""
    pass


@event.listens_for(engine.sync_engine, "close")
def close(dbapi_connection, connection_record):
    """Log database connection closure."""
    pass
