"""
Task Schemas - Phase II Todo Application

Pydantic models for request validation and response serialization.
Implements camelCase aliases for frontend compatibility (FR-038).
"""

import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator


class TaskCreate(BaseModel):
    """
    Schema for creating a new task.

    Validates title is required and within length limits.
    Description is optional.
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Task title (1-200 characters)",
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Optional task description (0-1000 characters)",
    )

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Validate title is not empty after trimming whitespace."""
        stripped = v.strip()
        if not stripped:
            raise ValueError("Title is required")
        if len(stripped) > 200:
            raise ValueError("Title must be 200 characters or less")
        return stripped

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        """Validate description length if provided."""
        if v is None:
            return None
        stripped = v.strip()
        if len(stripped) > 1000:
            raise ValueError("Description must be 1000 characters or less")
        return stripped if stripped else None


class TaskUpdate(BaseModel):
    """
    Schema for updating an existing task.

    All fields optional - supports partial updates.
    """

    title: Optional[str] = Field(
        default=None,
        max_length=200,
        description="New task title",
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="New task description",
    )
    completed: Optional[bool] = Field(
        default=None,
        description="Task completion status",
    )

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        """Validate title is not empty if provided."""
        if v is None:
            return None
        stripped = v.strip()
        if not stripped:
            raise ValueError("Title cannot be empty")
        if len(stripped) > 200:
            raise ValueError("Title must be 200 characters or less")
        return stripped

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        """Validate description length if provided."""
        if v is None:
            return None
        stripped = v.strip()
        if len(stripped) > 1000:
            raise ValueError("Description must be 1000 characters or less")
        return stripped if stripped else None


class TaskResponse(BaseModel):
    """
    Schema for task response.

    Uses camelCase aliases for frontend compatibility.
    Timestamps serialized as ISO 8601 strings with Z suffix.
    """

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: uuid.UUID
    title: str
    description: Optional[str]
    completed: bool
    user_id: str = Field(alias="userId", serialization_alias="userId")
    created_at: datetime = Field(alias="createdAt", serialization_alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt", serialization_alias="updatedAt")

    @field_serializer("created_at", "updated_at")
    def serialize_datetime(self, v: datetime) -> str:
        """Serialize datetime to ISO 8601 with Z suffix for UTC."""
        iso = v.isoformat()
        if iso.endswith("+00:00"):
            return iso.replace("+00:00", "Z")
        return iso + "Z"


class TaskListResponse(BaseModel):
    """Response wrapper for task list (FR-036)."""

    tasks: List[TaskResponse]


class SingleTaskResponse(BaseModel):
    """Response wrapper for single task (FR-037)."""

    task: TaskResponse


class MessageResponse(BaseModel):
    """Response for operations that return a message (e.g., delete)."""

    message: str


class ErrorResponse(BaseModel):
    """
    Standard error response format (FR-029).

    Provides human-readable message and machine-parseable code.
    """

    error: str = Field(description="Human-readable error message")
    code: str = Field(description="Machine-readable error code")
