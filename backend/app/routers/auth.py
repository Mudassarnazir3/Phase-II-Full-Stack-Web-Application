"""
Authentication Router - Phase II Todo Application

Handles user registration, login, and logout endpoints.
"""

from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import jwt
import bcrypt

from app.config import get_settings
from app.dependencies import get_db
from app.models.user import User
from app.schemas.auth import (
    AuthSignUpRequest,
    AuthSignUpResponse,
    AuthSignInRequest,
    AuthSignInResponse,
    AuthSignOutResponse,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def create_token(user_id: str) -> str:
    """Create a JWT token for the user."""
    settings = get_settings()
    payload = {
        "sub": user_id,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(days=7),
    }
    return jwt.encode(payload, settings.better_auth_secret, algorithm="HS256")


@router.post(
    "/signup",
    response_model=AuthSignUpResponse,
    status_code=status.HTTP_201_CREATED,
)
async def signup(
    request: AuthSignUpRequest,
    db: AsyncSession = Depends(get_db),
) -> AuthSignUpResponse:
    """
    Register a new user.

    Creates a new user account with hashed password.
    Returns success message on completion.
    """
    # Check if email already exists
    stmt = select(User).where(User.email == request.email)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": "Email already registered", "code": "EMAIL_EXISTS"},
        )

    # Create new user with hashed password
    user = User(
        email=request.email,
        password_hash=hash_password(request.password),
    )

    db.add(user)
    await db.commit()

    return AuthSignUpResponse(message="Account created successfully")


@router.post(
    "/signin",
    response_model=AuthSignInResponse,
)
async def signin(
    request: AuthSignInRequest,
    db: AsyncSession = Depends(get_db),
) -> AuthSignInResponse:
    """
    Authenticate a user.

    Validates credentials and returns JWT token with user object.
    """
    # Find user by email
    stmt = select(User).where(User.email == request.email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    # Check user exists and password matches
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid email or password", "code": "INVALID_CREDENTIALS"},
        )

    # Generate JWT token
    token = create_token(str(user.id))

    return AuthSignInResponse(
        token=token,
        user=UserResponse(id=str(user.id), email=user.email),
    )


@router.post(
    "/signout",
    response_model=AuthSignOutResponse,
)
async def signout() -> AuthSignOutResponse:
    """
    Sign out a user.

    This endpoint is stateless - the frontend handles token removal.
    Backend can implement token blacklisting in future if needed.
    """
    return AuthSignOutResponse(message="Signed out successfully")
