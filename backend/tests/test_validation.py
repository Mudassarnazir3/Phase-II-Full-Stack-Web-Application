"""
Validation Boundary Tests - Phase II Todo Application

Tests for input validation at exact boundaries (Phase 10).
Covers T072-T076 from tasks.md.
"""

import pytest
from httpx import AsyncClient

from app.models.task import Task
from tests.conftest import auth_header


class TestTitleValidationBoundaries:
    """Test suite for title length validation boundaries."""

    # === T072: Title at exactly 200 chars passes ===

    @pytest.mark.asyncio
    async def test_title_200_chars_passes(
        self, client: AsyncClient, user_a_token: str
    ):
        """T072: Title at exactly 200 characters passes validation."""
        title_200 = "a" * 200

        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"title": title_200},
        )

        assert response.status_code == 201
        data = response.json()
        assert len(data["task"]["title"]) == 200

    @pytest.mark.asyncio
    async def test_title_199_chars_passes(
        self, client: AsyncClient, user_a_token: str
    ):
        """Title at 199 characters passes validation."""
        title_199 = "a" * 199

        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"title": title_199},
        )

        assert response.status_code == 201

    # === T073: Title at 201 chars fails ===

    @pytest.mark.asyncio
    async def test_title_201_chars_fails(
        self, client: AsyncClient, user_a_token: str
    ):
        """T073: Title at 201 characters fails validation."""
        title_201 = "a" * 201

        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"title": title_201},
        )

        assert response.status_code == 400
        data = response.json()
        assert "200" in data["error"] or "title" in data["error"].lower()

    @pytest.mark.asyncio
    async def test_title_500_chars_fails(
        self, client: AsyncClient, user_a_token: str
    ):
        """Title way over limit (500 chars) fails validation."""
        title_500 = "a" * 500

        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"title": title_500},
        )

        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_update_title_200_chars_passes(
        self, client: AsyncClient, user_a_token: str, task_for_user_a: Task
    ):
        """Update with 200 character title passes."""
        title_200 = "b" * 200

        response = await client.put(
            f"/api/tasks/{task_for_user_a.id}",
            headers=auth_header(user_a_token),
            json={"title": title_200},
        )

        assert response.status_code == 200
        assert len(response.json()["task"]["title"]) == 200

    @pytest.mark.asyncio
    async def test_update_title_201_chars_fails(
        self, client: AsyncClient, user_a_token: str, task_for_user_a: Task
    ):
        """Update with 201 character title fails."""
        title_201 = "b" * 201

        response = await client.put(
            f"/api/tasks/{task_for_user_a.id}",
            headers=auth_header(user_a_token),
            json={"title": title_201},
        )

        assert response.status_code == 400


class TestDescriptionValidationBoundaries:
    """Test suite for description length validation boundaries."""

    # === T074: Description at exactly 1000 chars passes ===

    @pytest.mark.asyncio
    async def test_description_1000_chars_passes(
        self, client: AsyncClient, user_a_token: str
    ):
        """T074: Description at exactly 1000 characters passes validation."""
        description_1000 = "a" * 1000

        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"title": "Test Task", "description": description_1000},
        )

        assert response.status_code == 201
        data = response.json()
        assert len(data["task"]["description"]) == 1000

    @pytest.mark.asyncio
    async def test_description_999_chars_passes(
        self, client: AsyncClient, user_a_token: str
    ):
        """Description at 999 characters passes validation."""
        description_999 = "a" * 999

        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"title": "Test Task", "description": description_999},
        )

        assert response.status_code == 201

    # === T075: Description at 1001 chars fails ===

    @pytest.mark.asyncio
    async def test_description_1001_chars_fails(
        self, client: AsyncClient, user_a_token: str
    ):
        """T075: Description at 1001 characters fails validation."""
        description_1001 = "a" * 1001

        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"title": "Test Task", "description": description_1001},
        )

        assert response.status_code == 400
        data = response.json()
        assert "1000" in data["error"] or "description" in data["error"].lower()

    @pytest.mark.asyncio
    async def test_description_5000_chars_fails(
        self, client: AsyncClient, user_a_token: str
    ):
        """Description way over limit (5000 chars) fails validation."""
        description_5000 = "a" * 5000

        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"title": "Test Task", "description": description_5000},
        )

        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_update_description_1000_chars_passes(
        self, client: AsyncClient, user_a_token: str, task_for_user_a: Task
    ):
        """Update with 1000 character description passes."""
        description_1000 = "b" * 1000

        response = await client.put(
            f"/api/tasks/{task_for_user_a.id}",
            headers=auth_header(user_a_token),
            json={"description": description_1000},
        )

        assert response.status_code == 200
        assert len(response.json()["task"]["description"]) == 1000

    @pytest.mark.asyncio
    async def test_update_description_1001_chars_fails(
        self, client: AsyncClient, user_a_token: str, task_for_user_a: Task
    ):
        """Update with 1001 character description fails."""
        description_1001 = "b" * 1001

        response = await client.put(
            f"/api/tasks/{task_for_user_a.id}",
            headers=auth_header(user_a_token),
            json={"description": description_1001},
        )

        assert response.status_code == 400


class TestWhitespaceValidation:
    """Test suite for whitespace handling in validation."""

    # === T076: Whitespace-only title fails ===

    @pytest.mark.asyncio
    async def test_whitespace_only_title_fails(
        self, client: AsyncClient, user_a_token: str
    ):
        """T076: Whitespace-only title fails validation."""
        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"title": "   "},
        )

        assert response.status_code == 400
        data = response.json()
        assert "title" in data["error"].lower() or "required" in data["error"].lower()

    @pytest.mark.asyncio
    async def test_tabs_only_title_fails(
        self, client: AsyncClient, user_a_token: str
    ):
        """Tabs-only title fails validation."""
        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"title": "\t\t\t"},
        )

        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_newlines_only_title_fails(
        self, client: AsyncClient, user_a_token: str
    ):
        """Newlines-only title fails validation."""
        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"title": "\n\n"},
        )

        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_mixed_whitespace_title_fails(
        self, client: AsyncClient, user_a_token: str
    ):
        """Mixed whitespace (spaces, tabs, newlines) title fails."""
        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"title": " \t \n "},
        )

        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_title_with_leading_trailing_whitespace_trimmed(
        self, client: AsyncClient, user_a_token: str
    ):
        """Title with leading/trailing whitespace is trimmed."""
        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"title": "  Valid Title  "},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["task"]["title"] == "Valid Title"

    @pytest.mark.asyncio
    async def test_update_whitespace_title_fails(
        self, client: AsyncClient, user_a_token: str, task_for_user_a: Task
    ):
        """Update with whitespace-only title fails."""
        response = await client.put(
            f"/api/tasks/{task_for_user_a.id}",
            headers=auth_header(user_a_token),
            json={"title": "   "},
        )

        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_empty_string_title_fails(
        self, client: AsyncClient, user_a_token: str
    ):
        """Empty string title fails validation."""
        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"title": ""},
        )

        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_whitespace_description_normalized(
        self, client: AsyncClient, user_a_token: str
    ):
        """Whitespace-only description is normalized to None."""
        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"title": "Valid Title", "description": "   "},
        )

        assert response.status_code == 201
        data = response.json()
        # Whitespace-only description should become None
        assert data["task"]["description"] is None


class TestTitleMinLength:
    """Test suite for minimum title length."""

    @pytest.mark.asyncio
    async def test_single_char_title_passes(
        self, client: AsyncClient, user_a_token: str
    ):
        """Single character title passes validation."""
        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"title": "a"},
        )

        assert response.status_code == 201
        assert response.json()["task"]["title"] == "a"

    @pytest.mark.asyncio
    async def test_unicode_title_passes(
        self, client: AsyncClient, user_a_token: str
    ):
        """Unicode characters in title pass validation."""
        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"title": "Task with emoji: Check the code"},
        )

        assert response.status_code == 201

    @pytest.mark.asyncio
    async def test_unicode_200_chars_boundary(
        self, client: AsyncClient, user_a_token: str
    ):
        """Unicode title at exactly 200 characters passes."""
        # Mix of ASCII and unicode
        title = "Task " + "x" * 195  # 200 chars total

        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"title": title},
        )

        assert response.status_code == 201


class TestOptionalDescriptionValidation:
    """Test suite for optional description field."""

    @pytest.mark.asyncio
    async def test_null_description_accepted(
        self, client: AsyncClient, user_a_token: str
    ):
        """Null description is accepted."""
        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"title": "Task", "description": None},
        )

        assert response.status_code == 201
        assert response.json()["task"]["description"] is None

    @pytest.mark.asyncio
    async def test_missing_description_accepted(
        self, client: AsyncClient, user_a_token: str
    ):
        """Missing description field is accepted."""
        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"title": "Task"},
        )

        assert response.status_code == 201
        assert response.json()["task"]["description"] is None

    @pytest.mark.asyncio
    async def test_empty_string_description_normalized(
        self, client: AsyncClient, user_a_token: str
    ):
        """Empty string description is normalized to None."""
        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"title": "Task", "description": ""},
        )

        assert response.status_code == 201
        # Empty string should be normalized to None
        assert response.json()["task"]["description"] is None


class TestResponseFormatValidation:
    """Test suite for response format validation (T077-T079)."""

    @pytest.mark.asyncio
    async def test_timestamp_iso8601_utc_format(
        self, client: AsyncClient, user_a_token: str
    ):
        """T079: Timestamps are in ISO 8601 UTC format."""
        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"title": "Test Task"},
        )

        assert response.status_code == 201
        data = response.json()

        created_at = data["task"]["createdAt"]
        updated_at = data["task"]["updatedAt"]

        # Should end with Z (UTC)
        assert created_at.endswith("Z")
        assert updated_at.endswith("Z")

        # Should be parseable as ISO 8601
        from datetime import datetime
        datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        datetime.fromisoformat(updated_at.replace("Z", "+00:00"))

    @pytest.mark.asyncio
    async def test_list_response_format(
        self, client: AsyncClient, user_a_token: str, task_for_user_a: Task
    ):
        """T077: List response format matches contract."""
        response = await client.get(
            "/api/tasks",
            headers=auth_header(user_a_token),
        )

        assert response.status_code == 200
        data = response.json()

        # Should have "tasks" array wrapper
        assert "tasks" in data
        assert isinstance(data["tasks"], list)

    @pytest.mark.asyncio
    async def test_single_task_response_format(
        self, client: AsyncClient, user_a_token: str, task_for_user_a: Task
    ):
        """Single task response format matches contract."""
        response = await client.get(
            f"/api/tasks/{task_for_user_a.id}",
            headers=auth_header(user_a_token),
        )

        assert response.status_code == 200
        data = response.json()

        # Should have "task" object wrapper
        assert "task" in data
        assert isinstance(data["task"], dict)

    @pytest.mark.asyncio
    async def test_uuid_format_in_response(
        self, client: AsyncClient, user_a_token: str
    ):
        """Task ID is valid UUID format in response."""
        import uuid

        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"title": "Test Task"},
        )

        assert response.status_code == 201
        task_id = response.json()["task"]["id"]

        # Should be valid UUID
        uuid.UUID(task_id)
