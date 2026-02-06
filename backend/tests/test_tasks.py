"""
Task Endpoint Tests - Phase II Todo Application

Tests for task CRUD operations (User Stories 2-7).
Covers T029-T067 from tasks.md.
"""

import uuid
from datetime import datetime, timezone

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.task import Task
from tests.conftest import auth_header


class TestListTasks:
    """Test suite for GET /api/tasks (User Story 2)."""

    # === T029: GET /api/tasks returns only user's tasks ===

    @pytest.mark.asyncio
    async def test_list_returns_only_user_tasks(
        self,
        client: AsyncClient,
        user_a_token: str,
        task_for_user_a: Task,
        task_for_user_b: Task,
    ):
        """T029: GET /api/tasks returns only authenticated user's tasks."""
        response = await client.get(
            "/api/tasks",
            headers=auth_header(user_a_token),
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["tasks"]) == 1
        assert data["tasks"][0]["title"] == "User A Task"

    # === T030: GET /api/tasks returns empty array when no tasks ===

    @pytest.mark.asyncio
    async def test_list_returns_empty_array(
        self, client: AsyncClient, user_a_token: str
    ):
        """T030: GET /api/tasks returns empty array when user has no tasks."""
        response = await client.get(
            "/api/tasks",
            headers=auth_header(user_a_token),
        )

        assert response.status_code == 200
        data = response.json()
        assert data["tasks"] == []

    # === T031: User A cannot see user B's tasks ===

    @pytest.mark.asyncio
    async def test_user_isolation(
        self,
        client: AsyncClient,
        user_a_token: str,
        user_b_token: str,
        task_for_user_b: Task,
    ):
        """T031: User A cannot see user B's tasks."""
        # User A requests tasks
        response = await client.get(
            "/api/tasks",
            headers=auth_header(user_a_token),
        )

        assert response.status_code == 200
        data = response.json()
        # User A should see no tasks (only user B has tasks)
        assert data["tasks"] == []

    # === T032: Task list response format ===

    @pytest.mark.asyncio
    async def test_response_format(
        self, client: AsyncClient, user_a_token: str, task_for_user_a: Task
    ):
        """T032: Task list response has correct format with all fields."""
        response = await client.get(
            "/api/tasks",
            headers=auth_header(user_a_token),
        )

        assert response.status_code == 200
        data = response.json()
        assert "tasks" in data
        assert len(data["tasks"]) == 1

        task = data["tasks"][0]
        # Verify all required fields exist (camelCase)
        assert "id" in task
        assert "title" in task
        assert "description" in task
        assert "completed" in task
        assert "userId" in task
        assert "createdAt" in task
        assert "updatedAt" in task

    @pytest.mark.asyncio
    async def test_multiple_tasks_ordered(
        self,
        client: AsyncClient,
        user_a_token: str,
        multiple_tasks_for_user_a: list[Task],
    ):
        """Tasks are returned in order (most recent first)."""
        response = await client.get(
            "/api/tasks",
            headers=auth_header(user_a_token),
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["tasks"]) == 3


class TestCreateTask:
    """Test suite for POST /api/tasks (User Story 3)."""

    # === T036: POST /api/tasks with valid title creates task ===

    @pytest.mark.asyncio
    async def test_create_with_valid_title(
        self, client: AsyncClient, user_a_token: str
    ):
        """T036: POST /api/tasks with valid title creates task."""
        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"title": "New Task"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["task"]["title"] == "New Task"

    @pytest.mark.asyncio
    async def test_create_with_title_and_description(
        self, client: AsyncClient, user_a_token: str
    ):
        """Create task with both title and description."""
        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"title": "Task Title", "description": "Task Description"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["task"]["title"] == "Task Title"
        assert data["task"]["description"] == "Task Description"

    # === T037: POST /api/tasks without title returns 400 ===

    @pytest.mark.asyncio
    async def test_create_without_title_returns_400(
        self, client: AsyncClient, user_a_token: str
    ):
        """T037: POST /api/tasks without title returns 400."""
        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"description": "No title provided"},
        )

        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert "title" in data["error"].lower() or "required" in data["error"].lower()

    @pytest.mark.asyncio
    async def test_create_with_empty_body_returns_400(
        self, client: AsyncClient, user_a_token: str
    ):
        """Create with empty body returns 400."""
        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={},
        )

        assert response.status_code == 400

    # === T038: POST /api/tasks with title >200 chars returns 400 ===

    @pytest.mark.asyncio
    async def test_create_title_too_long_returns_400(
        self, client: AsyncClient, user_a_token: str
    ):
        """T038: POST /api/tasks with title >200 chars returns 400."""
        long_title = "a" * 201

        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"title": long_title},
        )

        assert response.status_code == 400
        data = response.json()
        assert "200" in data["error"] or "title" in data["error"].lower()

    # === T039: POST /api/tasks with description >1000 chars returns 400 ===

    @pytest.mark.asyncio
    async def test_create_description_too_long_returns_400(
        self, client: AsyncClient, user_a_token: str
    ):
        """T039: POST /api/tasks with description >1000 chars returns 400."""
        long_description = "a" * 1001

        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"title": "Valid Title", "description": long_description},
        )

        assert response.status_code == 400
        data = response.json()
        assert "1000" in data["error"] or "description" in data["error"].lower()

    # === T040: POST /api/tasks ignores forged user_id in body ===

    @pytest.mark.asyncio
    async def test_create_ignores_forged_user_id(
        self, client: AsyncClient, user_a_id: str, user_a_token: str, user_b_id: str
    ):
        """T040: POST /api/tasks ignores forged user_id in body."""
        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"title": "Test Task", "user_id": user_b_id},
        )

        assert response.status_code == 201
        data = response.json()
        # Task should be owned by user_a (from JWT), not user_b (from body)
        assert data["task"]["userId"] == user_a_id

    @pytest.mark.asyncio
    async def test_create_ignores_forged_userId_camelcase(
        self, client: AsyncClient, user_a_id: str, user_a_token: str, user_b_id: str
    ):
        """Forged userId (camelCase) in body is also ignored."""
        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"title": "Test Task", "userId": user_b_id},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["task"]["userId"] == user_a_id

    # === T041: Created task has completed=false, server timestamps ===

    @pytest.mark.asyncio
    async def test_create_defaults_completed_false(
        self, client: AsyncClient, user_a_token: str
    ):
        """T041: Created task has completed=false by default."""
        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"title": "New Task"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["task"]["completed"] is False

    @pytest.mark.asyncio
    async def test_create_has_server_timestamps(
        self, client: AsyncClient, user_a_token: str
    ):
        """Created task has server-generated timestamps."""
        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"title": "New Task"},
        )

        assert response.status_code == 201
        data = response.json()

        # Parse timestamps - should be valid ISO 8601 with Z suffix
        created_at_str = data["task"]["createdAt"]
        updated_at_str = data["task"]["updatedAt"]

        # Should end with Z (UTC indicator)
        assert created_at_str.endswith("Z")
        assert updated_at_str.endswith("Z")

        # Should be parseable as ISO 8601
        created_at = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
        updated_at = datetime.fromisoformat(updated_at_str.replace("Z", "+00:00"))

        # Timestamps should be recent (within last minute)
        now = datetime.now(timezone.utc)
        assert (now - created_at).total_seconds() < 60
        assert (now - updated_at).total_seconds() < 60

    @pytest.mark.asyncio
    async def test_create_ignores_forged_completed_true(
        self, client: AsyncClient, user_a_token: str
    ):
        """Forged completed=true in body is ignored."""
        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"title": "New Task", "completed": True},
        )

        assert response.status_code == 201
        data = response.json()
        # completed should default to false regardless of input
        assert data["task"]["completed"] is False


class TestToggleTask:
    """Test suite for PATCH /api/tasks/:id/toggle (User Story 4)."""

    # === T045: Toggle flips completed from false to true ===

    @pytest.mark.asyncio
    async def test_toggle_false_to_true(
        self, client: AsyncClient, user_a_token: str, task_for_user_a: Task
    ):
        """T045: PATCH /api/tasks/:id/toggle flips completed from false to true."""
        assert task_for_user_a.completed is False

        response = await client.patch(
            f"/api/tasks/{task_for_user_a.id}/toggle",
            headers=auth_header(user_a_token),
        )

        assert response.status_code == 200
        data = response.json()
        assert data["task"]["completed"] is True

    # === T046: Toggle flips completed from true to false ===

    @pytest.mark.asyncio
    async def test_toggle_true_to_false(
        self, client: AsyncClient, user_a_token: str, completed_task_for_user_a: Task
    ):
        """T046: PATCH /api/tasks/:id/toggle flips completed from true to false."""
        assert completed_task_for_user_a.completed is True

        response = await client.patch(
            f"/api/tasks/{completed_task_for_user_a.id}/toggle",
            headers=auth_header(user_a_token),
        )

        assert response.status_code == 200
        data = response.json()
        assert data["task"]["completed"] is False

    # === T047: Toggle on non-owned task returns 404 ===

    @pytest.mark.asyncio
    async def test_toggle_non_owned_returns_404(
        self, client: AsyncClient, user_a_token: str, task_for_user_b: Task
    ):
        """T047: Toggle on non-owned task returns 404."""
        response = await client.patch(
            f"/api/tasks/{task_for_user_b.id}/toggle",
            headers=auth_header(user_a_token),
        )

        assert response.status_code == 404
        data = response.json()
        assert data["code"] == "NOT_FOUND"

    # === T048: Toggle on non-existent task returns 404 ===

    @pytest.mark.asyncio
    async def test_toggle_nonexistent_returns_404(
        self, client: AsyncClient, user_a_token: str
    ):
        """T048: Toggle on non-existent task returns 404."""
        fake_id = str(uuid.uuid4())

        response = await client.patch(
            f"/api/tasks/{fake_id}/toggle",
            headers=auth_header(user_a_token),
        )

        assert response.status_code == 404

    # === T049: Toggle updates updatedAt timestamp ===

    @pytest.mark.asyncio
    async def test_toggle_updates_timestamp(
        self, client: AsyncClient, user_a_token: str, task_for_user_a: Task
    ):
        """T049: Toggle updates updatedAt timestamp."""
        # Get original timestamp via API to ensure consistent timezone handling
        get_response = await client.get(
            f"/api/tasks/{task_for_user_a.id}",
            headers=auth_header(user_a_token),
        )
        original_updated_at = get_response.json()["task"]["updatedAt"]

        response = await client.patch(
            f"/api/tasks/{task_for_user_a.id}/toggle",
            headers=auth_header(user_a_token),
        )

        assert response.status_code == 200
        data = response.json()
        new_updated_at = data["task"]["updatedAt"]

        # Compare as strings (both ISO 8601 with Z suffix)
        assert new_updated_at >= original_updated_at


class TestUpdateTask:
    """Test suite for PUT /api/tasks/:id (User Story 5)."""

    # === T052: PUT /api/tasks/:id updates title ===

    @pytest.mark.asyncio
    async def test_update_title(
        self, client: AsyncClient, user_a_token: str, task_for_user_a: Task
    ):
        """T052: PUT /api/tasks/:id updates title."""
        response = await client.put(
            f"/api/tasks/{task_for_user_a.id}",
            headers=auth_header(user_a_token),
            json={"title": "Updated Title"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["task"]["title"] == "Updated Title"

    # === T053: PUT /api/tasks/:id updates description ===

    @pytest.mark.asyncio
    async def test_update_description(
        self, client: AsyncClient, user_a_token: str, task_for_user_a: Task
    ):
        """T053: PUT /api/tasks/:id updates description."""
        response = await client.put(
            f"/api/tasks/{task_for_user_a.id}",
            headers=auth_header(user_a_token),
            json={"description": "Updated Description"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["task"]["description"] == "Updated Description"

    # === T054: PUT /api/tasks/:id with empty title returns 400 ===

    @pytest.mark.asyncio
    async def test_update_empty_title_returns_400(
        self, client: AsyncClient, user_a_token: str, task_for_user_a: Task
    ):
        """T054: PUT /api/tasks/:id with empty title returns 400."""
        response = await client.put(
            f"/api/tasks/{task_for_user_a.id}",
            headers=auth_header(user_a_token),
            json={"title": ""},
        )

        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_update_whitespace_title_returns_400(
        self, client: AsyncClient, user_a_token: str, task_for_user_a: Task
    ):
        """Update with whitespace-only title returns 400."""
        response = await client.put(
            f"/api/tasks/{task_for_user_a.id}",
            headers=auth_header(user_a_token),
            json={"title": "   "},
        )

        assert response.status_code == 400

    # === T055: PUT /api/tasks/:id on non-owned task returns 404 ===

    @pytest.mark.asyncio
    async def test_update_non_owned_returns_404(
        self, client: AsyncClient, user_a_token: str, task_for_user_b: Task
    ):
        """T055: PUT /api/tasks/:id on non-owned task returns 404."""
        response = await client.put(
            f"/api/tasks/{task_for_user_b.id}",
            headers=auth_header(user_a_token),
            json={"title": "Hijacked Title"},
        )

        assert response.status_code == 404

    # === T056: PUT /api/tasks/:id ignores user_id in body ===

    @pytest.mark.asyncio
    async def test_update_ignores_user_id(
        self,
        client: AsyncClient,
        user_a_id: str,
        user_a_token: str,
        user_b_id: str,
        task_for_user_a: Task,
    ):
        """T056: PUT /api/tasks/:id ignores user_id in body."""
        response = await client.put(
            f"/api/tasks/{task_for_user_a.id}",
            headers=auth_header(user_a_token),
            json={"title": "Updated Title", "user_id": user_b_id},
        )

        assert response.status_code == 200
        data = response.json()
        # user_id should remain unchanged
        assert data["task"]["userId"] == user_a_id

    # === T057: Partial update only changes specified fields ===

    @pytest.mark.asyncio
    async def test_partial_update_preserves_other_fields(
        self, client: AsyncClient, user_a_token: str, task_for_user_a: Task
    ):
        """T057: Partial update only changes specified fields."""
        original_title = task_for_user_a.title
        original_description = task_for_user_a.description

        # Update only completed status
        response = await client.put(
            f"/api/tasks/{task_for_user_a.id}",
            headers=auth_header(user_a_token),
            json={"completed": True},
        )

        assert response.status_code == 200
        data = response.json()
        # Title and description should be preserved
        assert data["task"]["title"] == original_title
        assert data["task"]["description"] == original_description
        assert data["task"]["completed"] is True

    @pytest.mark.asyncio
    async def test_update_updates_timestamp(
        self, client: AsyncClient, user_a_token: str, task_for_user_a: Task
    ):
        """Update changes updatedAt timestamp."""
        # Get original timestamp via API to ensure consistent timezone handling
        get_response = await client.get(
            f"/api/tasks/{task_for_user_a.id}",
            headers=auth_header(user_a_token),
        )
        original_updated_at = get_response.json()["task"]["updatedAt"]

        response = await client.put(
            f"/api/tasks/{task_for_user_a.id}",
            headers=auth_header(user_a_token),
            json={"title": "Updated Title"},
        )

        assert response.status_code == 200
        data = response.json()
        new_updated_at = data["task"]["updatedAt"]

        # Compare as strings (both ISO 8601 with Z suffix)
        assert new_updated_at >= original_updated_at


class TestDeleteTask:
    """Test suite for DELETE /api/tasks/:id (User Story 6)."""

    # === T060: DELETE /api/tasks/:id removes task from database ===

    @pytest.mark.asyncio
    async def test_delete_removes_task(
        self,
        client: AsyncClient,
        user_a_token: str,
        task_for_user_a: Task,
        db_session: AsyncSession,
    ):
        """T060: DELETE /api/tasks/:id removes task from database."""
        task_id = task_for_user_a.id

        response = await client.delete(
            f"/api/tasks/{task_id}",
            headers=auth_header(user_a_token),
        )

        assert response.status_code == 200

        # Verify task is removed from database
        result = await db_session.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()
        assert task is None

    # === T061: DELETE /api/tasks/:id on non-owned task returns 404 ===

    @pytest.mark.asyncio
    async def test_delete_non_owned_returns_404(
        self, client: AsyncClient, user_a_token: str, task_for_user_b: Task
    ):
        """T061: DELETE /api/tasks/:id on non-owned task returns 404."""
        response = await client.delete(
            f"/api/tasks/{task_for_user_b.id}",
            headers=auth_header(user_a_token),
        )

        assert response.status_code == 404

    # === T062: DELETE /api/tasks/:id on non-existent task returns 404 ===

    @pytest.mark.asyncio
    async def test_delete_nonexistent_returns_404(
        self, client: AsyncClient, user_a_token: str
    ):
        """T062: DELETE /api/tasks/:id on non-existent task returns 404."""
        fake_id = str(uuid.uuid4())

        response = await client.delete(
            f"/api/tasks/{fake_id}",
            headers=auth_header(user_a_token),
        )

        assert response.status_code == 404

    # === T063: DELETE returns success message not deleted task ===

    @pytest.mark.asyncio
    async def test_delete_returns_message(
        self, client: AsyncClient, user_a_token: str, task_for_user_a: Task
    ):
        """T063: DELETE returns success message, not the deleted task."""
        response = await client.delete(
            f"/api/tasks/{task_for_user_a.id}",
            headers=auth_header(user_a_token),
        )

        assert response.status_code == 200
        data = response.json()
        # Should have message, not task
        assert "message" in data
        assert "task" not in data
        assert "deleted" in data["message"].lower() or "success" in data["message"].lower()


class TestGetSingleTask:
    """Test suite for GET /api/tasks/:id (User Story 7)."""

    # === T065: GET /api/tasks/:id returns owned task ===

    @pytest.mark.asyncio
    async def test_get_returns_owned_task(
        self, client: AsyncClient, user_a_token: str, task_for_user_a: Task
    ):
        """T065: GET /api/tasks/:id returns owned task."""
        response = await client.get(
            f"/api/tasks/{task_for_user_a.id}",
            headers=auth_header(user_a_token),
        )

        assert response.status_code == 200
        data = response.json()
        assert data["task"]["id"] == str(task_for_user_a.id)
        assert data["task"]["title"] == task_for_user_a.title

    @pytest.mark.asyncio
    async def test_get_response_format(
        self, client: AsyncClient, user_a_token: str, task_for_user_a: Task
    ):
        """GET single task response has correct format."""
        response = await client.get(
            f"/api/tasks/{task_for_user_a.id}",
            headers=auth_header(user_a_token),
        )

        assert response.status_code == 200
        data = response.json()

        # Should have "task" wrapper
        assert "task" in data
        task = data["task"]

        # Verify all required fields (camelCase)
        assert "id" in task
        assert "title" in task
        assert "description" in task
        assert "completed" in task
        assert "userId" in task
        assert "createdAt" in task
        assert "updatedAt" in task

    # === T066: GET /api/tasks/:id on non-owned task returns 404 ===

    @pytest.mark.asyncio
    async def test_get_non_owned_returns_404(
        self, client: AsyncClient, user_a_token: str, task_for_user_b: Task
    ):
        """T066: GET /api/tasks/:id on non-owned task returns 404."""
        response = await client.get(
            f"/api/tasks/{task_for_user_b.id}",
            headers=auth_header(user_a_token),
        )

        assert response.status_code == 404
        data = response.json()
        assert data["code"] == "NOT_FOUND"

    # === T067: GET /api/tasks/:id on non-existent task returns 404 ===

    @pytest.mark.asyncio
    async def test_get_nonexistent_returns_404(
        self, client: AsyncClient, user_a_token: str
    ):
        """T067: GET /api/tasks/:id on non-existent task returns 404."""
        fake_id = str(uuid.uuid4())

        response = await client.get(
            f"/api/tasks/{fake_id}",
            headers=auth_header(user_a_token),
        )

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_invalid_uuid_returns_error(
        self, client: AsyncClient, user_a_token: str
    ):
        """GET with invalid UUID format returns error (400 or 422)."""
        response = await client.get(
            "/api/tasks/not-a-valid-uuid",
            headers=auth_header(user_a_token),
        )

        # API returns 400 or 422 for invalid path parameters
        assert response.status_code in [400, 422]
