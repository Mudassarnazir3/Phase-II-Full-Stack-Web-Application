"""
Task Model - Phase II Todo Application

SQLModel definition for the tasks table per data-model.md specification.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    """
    Task entity representing a user's todo item.

    Attributes:
        id: UUID primary key (generated server-side)
        title: Task title (1-200 chars, required)
        description: Optional description (0-1000 chars)
        completed: Completion status (defaults to False)
        user_id: Owner reference from JWT claims (indexed)
        created_at: Creation timestamp (UTC)
        updated_at: Last modification timestamp (UTC)
    """

    __tablename__ = "tasks"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False,
    )
    title: str = Field(
        max_length=200,
        nullable=False,
        index=False,
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        nullable=True,
    )
    completed: bool = Field(
        default=False,
        nullable=False,
    )
    user_id: str = Field(
        max_length=255,
        nullable=False,
        index=True,  # FR-025: Index on user_id for query performance
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
