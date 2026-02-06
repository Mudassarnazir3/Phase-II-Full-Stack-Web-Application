"""
User Model - Phase II Todo Application

SQLModel definition for the users table for authentication.
"""

import uuid
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """
    User entity for authentication.

    Attributes:
        id: UUID primary key (generated server-side)
        email: User email address (unique, indexed)
        password_hash: Hashed password (never stored in plain text)
        created_at: Account creation timestamp (UTC)
        updated_at: Last modification timestamp (UTC)
    """

    __tablename__ = "users"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False,
    )
    email: str = Field(
        max_length=255,
        nullable=False,
        unique=True,
        index=True,
    )
    password_hash: str = Field(
        max_length=255,
        nullable=False,
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
