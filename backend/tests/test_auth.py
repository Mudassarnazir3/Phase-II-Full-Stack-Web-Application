"""
Authentication Tests - Phase II Todo Application

Tests for JWT authentication middleware (User Story 1).
Covers T020-T025 from tasks.md.
"""

import pytest
from httpx import AsyncClient

from tests.conftest import (
    auth_header,
    create_test_token,
    create_expired_token,
    create_token_wrong_secret,
)


class TestJWTAuthentication:
    """Test suite for JWT authentication validation (US1)."""

    # === T020: Valid JWT token acceptance ===

    @pytest.mark.asyncio
    async def test_valid_token_accepted(
        self, client: AsyncClient, user_a_token: str
    ):
        """T020: Valid JWT token is accepted and request proceeds."""
        response = await client.get(
            "/api/tasks",
            headers=auth_header(user_a_token),
        )

        # Should not return 401 - authentication succeeded
        assert response.status_code == 200
        data = response.json()
        assert "tasks" in data

    @pytest.mark.asyncio
    async def test_valid_token_extracts_user_id(
        self, client: AsyncClient, user_a_id: str, user_a_token: str
    ):
        """Valid token extracts correct user_id from claims."""
        # Create a task to verify user_id extraction
        response = await client.post(
            "/api/tasks",
            headers=auth_header(user_a_token),
            json={"title": "Test Task"},
        )

        assert response.status_code == 201
        data = response.json()
        # Task should be owned by user_a
        assert data["task"]["userId"] == user_a_id

    # === T021: Missing Authorization header returns 401 ===

    @pytest.mark.asyncio
    async def test_missing_auth_header_returns_401(self, client: AsyncClient):
        """T021: Request without Authorization header returns 401."""
        response = await client.get("/api/tasks")

        assert response.status_code == 401
        data = response.json()
        assert "error" in data
        assert data["code"] == "UNAUTHORIZED"

    @pytest.mark.asyncio
    async def test_missing_auth_header_error_message(self, client: AsyncClient):
        """Missing Authorization header returns appropriate error message."""
        response = await client.get("/api/tasks")

        assert response.status_code == 401
        data = response.json()
        assert data["error"] == "Authentication required"

    # === T022: Invalid/malformed token returns 401 ===

    @pytest.mark.asyncio
    async def test_malformed_token_returns_401(self, client: AsyncClient):
        """T022: Malformed token returns 401."""
        response = await client.get(
            "/api/tasks",
            headers={"Authorization": "Bearer not-a-valid-jwt-token"},
        )

        assert response.status_code == 401
        data = response.json()
        assert "error" in data
        assert data["code"] == "UNAUTHORIZED"

    @pytest.mark.asyncio
    async def test_empty_token_returns_401(self, client: AsyncClient):
        """Empty token value returns 401."""
        response = await client.get(
            "/api/tasks",
            headers={"Authorization": "Bearer "},
        )

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_garbage_token_returns_401(self, client: AsyncClient):
        """Garbage/random string token returns 401."""
        response = await client.get(
            "/api/tasks",
            headers={"Authorization": "Bearer abc123xyz"},
        )

        assert response.status_code == 401
        data = response.json()
        assert data["error"] == "Invalid token"

    @pytest.mark.asyncio
    async def test_token_with_invalid_segments_returns_401(self, client: AsyncClient):
        """Token with wrong number of segments returns 401."""
        response = await client.get(
            "/api/tasks",
            headers={"Authorization": "Bearer header.payload"},
        )

        assert response.status_code == 401

    # === T023: Expired token returns 401 "Token expired" ===

    @pytest.mark.asyncio
    async def test_expired_token_returns_401(
        self, client: AsyncClient, expired_token: str
    ):
        """T023: Expired token returns 401."""
        response = await client.get(
            "/api/tasks",
            headers=auth_header(expired_token),
        )

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_expired_token_returns_token_expired_code(
        self, client: AsyncClient, expired_token: str
    ):
        """Expired token returns TOKEN_EXPIRED code."""
        response = await client.get(
            "/api/tasks",
            headers=auth_header(expired_token),
        )

        assert response.status_code == 401
        data = response.json()
        assert data["code"] == "TOKEN_EXPIRED"
        assert data["error"] == "Token expired"

    # === T024: Wrong signature returns 401 ===

    @pytest.mark.asyncio
    async def test_wrong_signature_returns_401(
        self, client: AsyncClient, wrong_secret_token: str
    ):
        """T024: Token signed with wrong secret returns 401."""
        response = await client.get(
            "/api/tasks",
            headers=auth_header(wrong_secret_token),
        )

        assert response.status_code == 401
        data = response.json()
        assert data["error"] == "Invalid token"
        assert data["code"] == "UNAUTHORIZED"

    # === T025: Wrong scheme (Basic instead of Bearer) returns 401 ===

    @pytest.mark.asyncio
    async def test_basic_scheme_returns_401(
        self, client: AsyncClient, user_a_token: str
    ):
        """T025: Basic auth scheme instead of Bearer returns 401."""
        response = await client.get(
            "/api/tasks",
            headers={"Authorization": f"Basic {user_a_token}"},
        )

        assert response.status_code == 401
        data = response.json()
        assert data["error"] == "Invalid authorization scheme"
        assert data["code"] == "UNAUTHORIZED"

    @pytest.mark.asyncio
    async def test_other_scheme_returns_401(self, client: AsyncClient):
        """Other auth schemes (Digest, etc.) return 401."""
        response = await client.get(
            "/api/tasks",
            headers={"Authorization": "Digest username=test"},
        )

        assert response.status_code == 401
        data = response.json()
        assert data["code"] == "UNAUTHORIZED"

    @pytest.mark.asyncio
    async def test_bearer_lowercase_accepted(
        self, client: AsyncClient, user_a_token: str
    ):
        """Bearer scheme is case-insensitive (bearer vs Bearer)."""
        response = await client.get(
            "/api/tasks",
            headers={"Authorization": f"bearer {user_a_token}"},
        )

        # Should be accepted (case-insensitive check)
        assert response.status_code == 200

    # === Additional edge cases ===

    @pytest.mark.asyncio
    async def test_token_without_exp_claim_returns_401(self, client: AsyncClient, user_a_id: str):
        """Token without exp claim returns 401."""
        from tests.conftest import create_test_token
        token = create_test_token(user_a_id, include_exp=False)

        response = await client.get(
            "/api/tasks",
            headers=auth_header(token),
        )

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_token_without_user_id_returns_401(self, client: AsyncClient):
        """Token without sub/user_id claim returns 401."""
        import jwt
        from tests.conftest import TEST_SECRET
        from datetime import datetime, timedelta, timezone

        # Create token without sub claim
        payload = {
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
            "iat": datetime.now(timezone.utc),
        }
        token = jwt.encode(payload, TEST_SECRET, algorithm="HS256")

        response = await client.get(
            "/api/tasks",
            headers=auth_header(token),
        )

        assert response.status_code == 401
        data = response.json()
        assert data["error"] == "Invalid token"


class TestAuthenticationOnAllEndpoints:
    """Verify authentication is required on all protected endpoints."""

    @pytest.mark.asyncio
    async def test_get_tasks_requires_auth(self, client: AsyncClient):
        """GET /api/tasks requires authentication."""
        response = await client.get("/api/tasks")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_post_tasks_requires_auth(self, client: AsyncClient):
        """POST /api/tasks requires authentication."""
        response = await client.post("/api/tasks", json={"title": "Test"})
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_get_task_by_id_requires_auth(self, client: AsyncClient):
        """GET /api/tasks/:id requires authentication."""
        response = await client.get("/api/tasks/00000000-0000-0000-0000-000000000001")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_put_task_requires_auth(self, client: AsyncClient):
        """PUT /api/tasks/:id requires authentication."""
        response = await client.put(
            "/api/tasks/00000000-0000-0000-0000-000000000001",
            json={"title": "Updated"},
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_patch_toggle_requires_auth(self, client: AsyncClient):
        """PATCH /api/tasks/:id/toggle requires authentication."""
        response = await client.patch(
            "/api/tasks/00000000-0000-0000-0000-000000000001/toggle"
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_delete_task_requires_auth(self, client: AsyncClient):
        """DELETE /api/tasks/:id requires authentication."""
        response = await client.delete(
            "/api/tasks/00000000-0000-0000-0000-000000000001"
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_health_check_does_not_require_auth(self, client: AsyncClient):
        """GET /api/health does NOT require authentication."""
        response = await client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
