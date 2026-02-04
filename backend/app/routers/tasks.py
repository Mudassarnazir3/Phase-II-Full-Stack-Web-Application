"""
Tasks Router - Phase II Todo Application

REST API endpoints for task CRUD operations.
All endpoints require JWT authentication and enforce user isolation.
"""

from datetime import datetime, timezone
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, get_db
from app.models.task import Task
from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskListResponse,
    SingleTaskResponse,
    MessageResponse,
)

router = APIRouter()


def task_to_response(task: Task) -> TaskResponse:
    """Convert Task model to TaskResponse schema."""
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        userId=task.user_id,
        createdAt=task.created_at,
        updatedAt=task.updated_at,
    )


@router.get("/tasks", response_model=TaskListResponse)
async def list_tasks(
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TaskListResponse:
    """
    List all tasks for authenticated user (FR-014, FR-036).

    Returns only tasks belonging to the authenticated user.
    Returns empty array if no tasks exist.
    """
    # Query with user_id filter (FR-014)
    stmt = (
        select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
    )
    result = await db.execute(stmt)
    tasks = result.scalars().all()

    return TaskListResponse(tasks=[task_to_response(t) for t in tasks])


@router.post("/tasks", response_model=SingleTaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SingleTaskResponse:
    """
    Create a new task (FR-015 to FR-021).

    - user_id set from JWT (ignores any user_id in body)
    - completed defaults to false
    - Timestamps generated server-side
    """
    now = datetime.now(timezone.utc)

    # Create task with user_id from JWT (FR-015)
    task = Task(
        title=task_data.title,
        description=task_data.description,
        completed=False,  # FR-018
        user_id=user_id,  # From JWT, not request body
        created_at=now,  # FR-019
        updated_at=now,  # FR-020
    )

    db.add(task)
    await db.commit()
    await db.refresh(task)

    return SingleTaskResponse(task=task_to_response(task))


@router.get("/tasks/{task_id}", response_model=SingleTaskResponse)
async def get_task(
    task_id: UUID,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SingleTaskResponse:
    """
    Get a single task by ID (FR-022, FR-037).

    Returns 404 if task not found or not owned by user.
    """
    # Query with user_id filter (FR-014)
    stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Task not found", "code": "NOT_FOUND"},
        )

    return SingleTaskResponse(task=task_to_response(task))


@router.put("/tasks/{task_id}", response_model=SingleTaskResponse)
async def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SingleTaskResponse:
    """
    Update a task (FR-022, FR-027).

    - Only updates provided fields (partial update)
    - user_id is immutable
    - Updates updatedAt timestamp
    """
    # Query with user_id filter (FR-014)
    stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Task not found", "code": "NOT_FOUND"},
        )

    # Update only provided fields (FR-027: user_id immutable)
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.completed is not None:
        task.completed = task_data.completed

    task.updated_at = datetime.now(timezone.utc)  # FR-020

    await db.commit()
    await db.refresh(task)

    return SingleTaskResponse(task=task_to_response(task))


@router.patch("/tasks/{task_id}/toggle", response_model=SingleTaskResponse)
async def toggle_task(
    task_id: UUID,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> SingleTaskResponse:
    """
    Toggle task completion status (FR-022).

    Flips completed boolean and updates updatedAt.
    """
    # Query with user_id filter (FR-014)
    stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Task not found", "code": "NOT_FOUND"},
        )

    # Toggle completed status
    task.completed = not task.completed
    task.updated_at = datetime.now(timezone.utc)  # FR-020

    await db.commit()
    await db.refresh(task)

    return SingleTaskResponse(task=task_to_response(task))


@router.delete("/tasks/{task_id}", response_model=MessageResponse)
async def delete_task(
    task_id: UUID,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    """
    Delete a task (FR-022).

    Permanently removes task from database.
    Returns success message, not the deleted task.
    """
    # Query with user_id filter (FR-014)
    stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await db.execute(stmt)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Task not found", "code": "NOT_FOUND"},
        )

    await db.delete(task)
    await db.commit()

    return MessageResponse(message="Task deleted successfully")
