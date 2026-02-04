"""
Test Configuration - Phase II Todo Application

Shared fixtures for pytest testing with FastAPI TestClient.
"""

import os
import uuid
from datetime import datetime, timedelta, timezone
from typing import AsyncGenerator, Generator

import jwt
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel

# Set test environment variables before importing app
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["BETTER_AUTH_SECRET"] = "test-secret-key-for-jwt-testing"
os.environ["BETTER_AUTH_URL"] = "http://localhost:3000"

from app.main import app
from app.dependencies import get_db
from app.models.task import Task


# Test database engine - in-memory SQLite for isolation
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    """Override database dependency for testing."""
    async with TestSessionLocal() as session:
        yield session


# Override the dependency
app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    """Create tables before each test and drop after."""
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a database session for direct database operations in tests."""
    async with TestSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Provide an async HTTP client for testing."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# === JWT Token Fixtures ===

TEST_SECRET = "test-secret-key-for-jwt-testing"


def create_test_token(
    user_id: str,
    expires_delta: timedelta = timedelta(hours=1),
    secret: str = TEST_SECRET,
    algorithm: str = "HS256",
    include_exp: bool = True,
) -> str:
    """Generate a JWT token for testing."""
    payload = {
        "sub": user_id,
        "iat": datetime.now(timezone.utc),
    }
    if include_exp:
        payload["exp"] = datetime.now(timezone.utc) + expires_delta
    return jwt.encode(payload, secret, algorithm=algorithm)


def create_expired_token(user_id: str) -> str:
    """Generate an expired JWT token."""
    return create_test_token(user_id, expires_delta=timedelta(hours=-1))


def create_token_wrong_secret(user_id: str) -> str:
    """Generate a token signed with wrong secret."""
    return create_test_token(user_id, secret="wrong-secret-key")


@pytest.fixture
def user_a_id() -> str:
    """Unique ID for test user A."""
    return str(uuid.uuid4())


@pytest.fixture
def user_b_id() -> str:
    """Unique ID for test user B."""
    return str(uuid.uuid4())


@pytest.fixture
def user_a_token(user_a_id: str) -> str:
    """Valid JWT token for user A."""
    return create_test_token(user_a_id)


@pytest.fixture
def user_b_token(user_b_id: str) -> str:
    """Valid JWT token for user B."""
    return create_test_token(user_b_id)


@pytest.fixture
def expired_token(user_a_id: str) -> str:
    """Expired JWT token."""
    return create_expired_token(user_a_id)


@pytest.fixture
def wrong_secret_token(user_a_id: str) -> str:
    """Token signed with wrong secret."""
    return create_token_wrong_secret(user_a_id)


def auth_header(token: str) -> dict:
    """Create Authorization header with Bearer token."""
    return {"Authorization": f"Bearer {token}"}


# === Task Fixtures ===


@pytest_asyncio.fixture
async def task_for_user_a(db_session: AsyncSession, user_a_id: str) -> Task:
    """Create a task owned by user A."""
    task = Task(
        title="User A Task",
        description="Task owned by user A",
        completed=False,
        user_id=user_a_id,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)
    return task


@pytest_asyncio.fixture
async def task_for_user_b(db_session: AsyncSession, user_b_id: str) -> Task:
    """Create a task owned by user B."""
    task = Task(
        title="User B Task",
        description="Task owned by user B",
        completed=False,
        user_id=user_b_id,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)
    return task


@pytest_asyncio.fixture
async def completed_task_for_user_a(db_session: AsyncSession, user_a_id: str) -> Task:
    """Create a completed task owned by user A."""
    task = Task(
        title="Completed Task",
        description="Already completed",
        completed=True,
        user_id=user_a_id,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)
    return task


@pytest_asyncio.fixture
async def multiple_tasks_for_user_a(db_session: AsyncSession, user_a_id: str) -> list[Task]:
    """Create multiple tasks owned by user A."""
    tasks = []
    for i in range(3):
        task = Task(
            title=f"Task {i + 1}",
            description=f"Description {i + 1}",
            completed=i % 2 == 0,
            user_id=user_a_id,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        db_session.add(task)
        tasks.append(task)
    await db_session.commit()
    for task in tasks:
        await db_session.refresh(task)
    return tasks
