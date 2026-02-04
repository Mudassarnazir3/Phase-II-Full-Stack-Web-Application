"""
Dependencies - Phase II Todo Application

FastAPI dependency injection for database sessions and authentication.
"""

from typing import AsyncGenerator

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import jwt

from app.config import get_settings
from app.db.session import get_async_session


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for injecting database sessions into route handlers.

    Usage:
        @router.get("/tasks")
        async def list_tasks(db: AsyncSession = Depends(get_db)):
            ...
    """
    async for session in get_async_session():
        yield session


async def get_current_user(
    authorization: str = Header(None, alias="Authorization"),
) -> str:
    """
    Dependency for extracting authenticated user_id from JWT.

    Validates Bearer token from Authorization header using BETTER_AUTH_SECRET.
    Returns user_id from token claims.

    Raises:
        HTTPException 401 for any authentication failure.

    Usage:
        @router.get("/tasks")
        async def list_tasks(user_id: str = Depends(get_current_user)):
            ...
    """
    settings = get_settings()

    # Check for Authorization header (FR-011)
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Authentication required", "code": "UNAUTHORIZED"},
        )

    # Validate Bearer scheme (FR-007)
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid authorization scheme", "code": "UNAUTHORIZED"},
        )

    token = parts[1]

    try:
        # Decode and verify JWT (FR-008, FR-009)
        payload = jwt.decode(
            token,
            settings.better_auth_secret,
            algorithms=["HS256"],
            options={"require": ["exp"]},
        )

        # Extract user_id from claims (FR-010)
        # Better Auth may use 'sub' or 'user_id' claim
        user_id = payload.get("sub") or payload.get("user_id")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": "Invalid token", "code": "UNAUTHORIZED"},
            )

        return str(user_id)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Token expired", "code": "TOKEN_EXPIRED"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid token", "code": "UNAUTHORIZED"},
        )
