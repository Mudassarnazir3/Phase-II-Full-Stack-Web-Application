"""
Authentication Schemas - Phase II Todo Application

Pydantic models for auth request/response validation.
"""

import re
from pydantic import BaseModel, EmailStr, Field, field_validator


class AuthSignUpRequest(BaseModel):
    """Request body for user registration."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(
        ..., min_length=8, max_length=128, description="User password"
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one digit")
        return v


class AuthSignUpResponse(BaseModel):
    """Response for successful registration."""

    message: str = Field(..., description="Success message")


class AuthSignInRequest(BaseModel):
    """Request body for user login."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class UserResponse(BaseModel):
    """User object in auth response."""

    id: str = Field(..., description="User UUID")
    email: str = Field(..., description="User email")


class AuthSignInResponse(BaseModel):
    """Response for successful login."""

    token: str = Field(..., description="JWT token")
    user: UserResponse = Field(..., description="User object")


class AuthSignOutResponse(BaseModel):
    """Response for logout."""

    message: str = Field(..., description="Success message")
