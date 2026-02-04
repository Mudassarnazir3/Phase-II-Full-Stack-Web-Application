"""
Database Session Management - Phase II Todo Application

Async SQLAlchemy engine and session configuration for Neon PostgreSQL.
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import get_settings


def get_engine():
    """
    Create async database engine for Neon PostgreSQL.

    Uses asyncpg driver with SSL enabled.
    Connection pooling configured for serverless environment.
    """
    settings = get_settings()

    engine = create_async_engine(
        settings.database_url,
        echo=False,  # Set to True for SQL debugging
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,  # Check connection health before use
    )

    return engine


def get_async_session_maker():
    """Create async session factory."""
    engine = get_engine()

    return sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for injecting database sessions into route handlers.

    Yields an async session and ensures proper cleanup.
    """
    async_session_maker = get_async_session_maker()

    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
