"""
Database Initialization - Phase II Todo Application

Creates tables and indexes from SQLModel metadata.
Idempotent - safe to run multiple times.
"""

import asyncio

from sqlmodel import SQLModel

from app.db.session import get_engine
from app.models.task import Task  # noqa: F401 - Import to register model
from app.models.user import User  # noqa: F401 - Import to register model


async def init_db():
    """
    Initialize database tables and indexes.

    Creates the tasks table with user_id index per FR-025.
    Safe to run multiple times (CREATE TABLE IF NOT EXISTS).
    """
    engine = get_engine()

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    await engine.dispose()


async def drop_db():
    """
    Drop all database tables.

    WARNING: Destructive operation - use only for testing/reset.
    """
    engine = get_engine()

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()


if __name__ == "__main__":
    # Allow running as script: python -m app.db.init
    asyncio.run(init_db())
    print("Database initialized successfully.")
