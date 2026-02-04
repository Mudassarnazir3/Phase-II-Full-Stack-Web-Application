"""
Security Tests - Phase II Todo Application

Tests for cross-user isolation and security hardening (Phase 10).
Covers T069-T071 from tasks.md.
"""

import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.task import Task
from tests.conftest import auth_header, create_test_token


class TestCrossUserIsolation:
    """Test suite for cross-user data isolation (T069)."""

    # === T069: Cross-user isolation across all endpoints ===

    @pytest.mark.asyncio
    async def test_list_isolation(
        self,
        client: AsyncClient,
        user_a_token: str,
        user_b_token: str,
        task_for_user_a: Task,
        task_for_user_b: Task,
    ):
        """User A cannot list user B's tasks and vice versa."""
        # User A's list
        response_a = await client.get(
            "/api/tasks",
            headers=auth_header(user_a_token),
        )
        assert response_a.status_code == 200
        tasks_a = response_a.json()["tasks"]
        task_ids_a = [t["id"] for t in tasks_a]

        # User B's list
        response_b = await client.get(
            "/api/tasks",
            headers=auth_header(user_b_token),
        )
        assert response_b.status_code == 200
        tasks_b = response_b.json()["tasks"]
        task_ids_b = [t["id"] for t in tasks_b]

        # Verify isolation - no overlap
        assert str(task_for_user_a.id) in task_ids_a
        assert str(task_for_user_b.id) not in task_ids_a
        assert str(task_for_user_b.id) in task_ids_b
        assert str(task_for_user_a.id) not in task_ids_b

    @pytest.mark.asyncio
    async def test_get_isolation(
        self,
        client: AsyncClient,
        user_a_token: str,
        task_for_user_b: Task,
    ):
        """User A cannot GET user B's task by ID."""
        response = await client.get(
            f"/api/tasks/{task_for_user_b.id}",
            headers=auth_header(user_a_token),
        )
        # Returns 404, not 403 (to not leak existence)
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_isolation(
        self,
        client: AsyncClient,
        user_a_token: str,
        task_for_user_b: Task,
        db_session: AsyncSession,
    ):
        """User A cannot UPDATE user B's task."""
        original_title = task_for_user_b.title

        response = await client.put(
            f"/api/tasks/{task_for_user_b.id}",
            headers=auth_header(user_a_token),
            json={"title": "Hijacked Title"},
        )
        assert response.status_code == 404

        # Verify task unchanged in database
        await db_session.refresh(task_for_user_b)
        assert task_for_user_b.title == original_title

    @pytest.mark.asyncio
    async def test_toggle_isolation(
        self,
        client: AsyncClient,
        user_a_token: str,
        task_for_user_b: Task,
        db_session: AsyncSession,
    ):
        """User A cannot TOGGLE user B's task."""
        original_completed = task_for_user_b.completed

        response = await client.patch(
            f"/api/tasks/{task_for_user_b.id}/toggle",
            headers=auth_header(user_a_token),
        )
        assert response.status_code == 404

        # Verify task unchanged
        await db_session.refresh(task_for_user_b)
        assert task_for_user_b.completed == original_completed

    @pytest.mark.asyncio
    async def test_delete_isolation(
        self,
        client: AsyncClient,
        user_a_token: str,
        task_for_user_b: Task,
        db_session: AsyncSession,
    ):
        """User A cannot DELETE user B's task."""
        task_id = task_for_user_b.id

        response = await client.delete(
            f"/api/tasks/{task_id}",
            headers=auth_header(user_a_token),
        )
        assert response.status_code == 404

        # Verify task still exists
        result = await db_session.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()
        assert task is not None

    @pytest.mark.asyncio
    async def test_many_users_isolation(
        self, client: AsyncClient, db_session: AsyncSession
    ):
        """Multiple users with multiple tasks maintain strict isolation."""
        # Create 3 users with 2 tasks each
        users = []
        for i in range(3):
            user_id = str(uuid.uuid4())
            token = create_test_token(user_id)
            users.append({"id": user_id, "token": token, "tasks": []})

            # Create tasks for this user
            for j in range(2):
                task = Task(
                    title=f"User {i} Task {j}",
                    user_id=user_id,
                )
                db_session.add(task)
                users[i]["tasks"].append(task)

        await db_session.commit()

        # Verify each user only sees their own tasks
        for user in users:
            response = await client.get(
                "/api/tasks",
                headers=auth_header(user["token"]),
            )
            assert response.status_code == 200
            tasks = response.json()["tasks"]
            assert len(tasks) == 2

            for task in tasks:
                assert task["userId"] == user["id"]


class TestForgedUserIdIgnored:
    """Test suite for forged user_id rejection (T070)."""

    # === T070: Forged user_id in request body is ignored ===

    @pytest.mark.asyncio
    async def test_create_ignores_forged_user_id(
        self, client: AsyncClient, user_a_id: str, user_a_token: str, user_b_id: str
    ):
        """POST ignores forged user_id - task owned by JWT user."""
        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={
                "title": "Test Task",
                "user_id": user_b_id,  # Forged!
            },
        )

        assert response.status_code == 201
        assert response.json()["task"]["userId"] == user_a_id

    @pytest.mark.asyncio
    async def test_create_ignores_forged_userId_camelcase(
        self, client: AsyncClient, user_a_id: str, user_a_token: str, user_b_id: str
    ):
        """POST ignores forged userId (camelCase) - task owned by JWT user."""
        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={
                "title": "Test Task",
                "userId": user_b_id,  # Forged (camelCase)!
            },
        )

        assert response.status_code == 201
        assert response.json()["task"]["userId"] == user_a_id

    @pytest.mark.asyncio
    async def test_update_ignores_forged_user_id(
        self,
        client: AsyncClient,
        user_a_id: str,
        user_a_token: str,
        user_b_id: str,
        task_for_user_a: Task,
    ):
        """PUT ignores forged user_id - ownership unchanged."""
        response = await client.put(
            f"/api/tasks/{task_for_user_a.id}",
            headers=auth_header(user_a_token),
            json={
                "title": "Updated",
                "user_id": user_b_id,  # Forged!
            },
        )

        assert response.status_code == 200
        assert response.json()["task"]["userId"] == user_a_id

    @pytest.mark.asyncio
    async def test_update_ignores_forged_userId_camelcase(
        self,
        client: AsyncClient,
        user_a_id: str,
        user_a_token: str,
        user_b_id: str,
        task_for_user_a: Task,
    ):
        """PUT ignores forged userId (camelCase) - ownership unchanged."""
        response = await client.put(
            f"/api/tasks/{task_for_user_a.id}",
            headers=auth_header(user_a_token),
            json={
                "title": "Updated",
                "userId": user_b_id,  # Forged (camelCase)!
            },
        )

        assert response.status_code == 200
        assert response.json()["task"]["userId"] == user_a_id

    @pytest.mark.asyncio
    async def test_cannot_transfer_task_ownership(
        self,
        client: AsyncClient,
        user_a_id: str,
        user_a_token: str,
        user_b_id: str,
        task_for_user_a: Task,
        db_session: AsyncSession,
    ):
        """Cannot transfer task to another user via PUT."""
        response = await client.put(
            f"/api/tasks/{task_for_user_a.id}",
            headers=auth_header(user_a_token),
            json={"user_id": user_b_id},
        )

        assert response.status_code == 200

        # Verify in database
        await db_session.refresh(task_for_user_a)
        assert task_for_user_a.user_id == user_a_id


class TestNoStackTracesExposed:
    """Test suite for stack trace suppression (T071)."""

    # === T071: No stack traces exposed in any error response ===

    @pytest.mark.asyncio
    async def test_validation_error_no_stack_trace(
        self, client: AsyncClient, user_a_token: str
    ):
        """Validation errors don't expose stack traces."""
        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={},  # Missing required title
        )

        assert response.status_code == 400
        data = response.json()

        # Should not contain stack trace indicators
        response_text = str(data)
        assert "Traceback" not in response_text
        assert "File \"" not in response_text
        assert "line " not in response_text.lower() or "line" in data.get("error", "").lower()

    @pytest.mark.asyncio
    async def test_auth_error_no_stack_trace(self, client: AsyncClient):
        """Auth errors don't expose stack traces."""
        response = await client.get(
            "/api/tasks",
            headers={"Authorization": "Bearer invalid"},
        )

        assert response.status_code == 401
        data = response.json()

        response_text = str(data)
        assert "Traceback" not in response_text
        assert "File \"" not in response_text

    @pytest.mark.asyncio
    async def test_not_found_error_no_stack_trace(
        self, client: AsyncClient, user_a_token: str
    ):
        """404 errors don't expose stack traces."""
        fake_id = str(uuid.uuid4())
        response = await client.get(
            f"/api/tasks/{fake_id}",
            headers=auth_header(user_a_token),
        )

        assert response.status_code == 404
        data = response.json()

        response_text = str(data)
        assert "Traceback" not in response_text
        assert "File \"" not in response_text

    @pytest.mark.asyncio
    async def test_malformed_json_no_stack_trace(
        self, client: AsyncClient, user_a_token: str
    ):
        """Malformed JSON doesn't expose stack traces."""
        response = await client.post(
            "/api/tasks",
            headers={
                **auth_header(user_a_token),
                "Content-Type": "application/json",
            },
            content="{not valid json",
        )

        # Should return 400, not 500
        assert response.status_code in [400, 422]
        data = response.json()

        response_text = str(data)
        assert "Traceback" not in response_text
        assert "File \"" not in response_text

    @pytest.mark.asyncio
    async def test_error_format_consistent(
        self, client: AsyncClient, user_a_token: str
    ):
        """All errors follow consistent format with error and code."""
        # Auth error
        auth_response = await client.get("/api/tasks")
        assert "error" in auth_response.json()
        assert "code" in auth_response.json()

        # Validation error
        val_response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={},
        )
        assert "error" in val_response.json()
        assert "code" in val_response.json()

        # Not found error
        not_found_response = await client.get(
            f"/api/tasks/{uuid.uuid4()}",
            headers=auth_header(user_a_token),
        )
        assert "error" in not_found_response.json()
        assert "code" in not_found_response.json()


class TestSecurityHeaders:
    """Test security headers are present on responses."""

    @pytest.mark.asyncio
    async def test_x_content_type_options_header(
        self, client: AsyncClient, user_a_token: str
    ):
        """X-Content-Type-Options: nosniff header is present."""
        response = await client.get(
            "/api/tasks",
            headers=auth_header(user_a_token),
        )

        assert response.headers.get("X-Content-Type-Options") == "nosniff"

    @pytest.mark.asyncio
    async def test_x_frame_options_header(
        self, client: AsyncClient, user_a_token: str
    ):
        """X-Frame-Options: DENY header is present."""
        response = await client.get(
            "/api/tasks",
            headers=auth_header(user_a_token),
        )

        assert response.headers.get("X-Frame-Options") == "DENY"

    @pytest.mark.asyncio
    async def test_security_headers_on_error_responses(self, client: AsyncClient):
        """Security headers present even on error responses."""
        response = await client.get("/api/tasks")  # No auth - 401

        assert response.status_code == 401
        assert response.headers.get("X-Content-Type-Options") == "nosniff"
        assert response.headers.get("X-Frame-Options") == "DENY"
