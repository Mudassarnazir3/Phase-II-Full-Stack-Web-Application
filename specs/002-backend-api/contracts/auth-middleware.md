# Authentication Middleware Contract: Backend API

**Feature Branch**: `002-backend-api`
**Created**: 2026-01-16
**Spec Reference**: [spec.md](../spec.md)

## Overview

This document specifies the JWT authentication middleware behavior for the backend API. The middleware is the security gatekeeper for all protected endpoints.

---

## Middleware Responsibilities

1. Extract JWT from `Authorization` header
2. Validate Bearer scheme
3. Verify JWT signature using `BETTER_AUTH_SECRET`
4. Check token expiration
5. Extract user identity from claims
6. Make user_id available to route handlers
7. Return appropriate error for any failure

---

## Token Extraction

### Expected Header Format

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Extraction Rules

| Scenario | Behavior |
|----------|----------|
| Header missing | Return 401 "Authentication required" |
| Header present but empty | Return 401 "Authentication required" |
| Scheme is not "Bearer" | Return 401 "Invalid authorization scheme" |
| Token portion missing | Return 401 "Invalid token" |
| Token has extra spaces | Trim and process |

---

## Token Verification

### Verification Steps

1. **Parse JWT structure**: Verify three-part format (header.payload.signature)
2. **Verify signature**: Using HS256 algorithm with `BETTER_AUTH_SECRET`
3. **Check expiration**: Verify `exp` claim is in the future
4. **Extract user ID**: Get `sub` or `user_id` from claims

### Verification Failures

| Failure Type | Error Message | Code |
|--------------|---------------|------|
| Malformed token | "Invalid token" | UNAUTHORIZED |
| Invalid signature | "Invalid token" | UNAUTHORIZED |
| Expired token | "Token expired" | TOKEN_EXPIRED |
| Missing user claim | "Invalid token" | UNAUTHORIZED |

**Security Note**: Do not reveal specific failure reasons beyond the table above. "Invalid token" is intentionally generic.

---

## JWT Claims Expected

### Standard Claims

| Claim | Type | Required | Description |
|-------|------|----------|-------------|
| `sub` | string | Yes* | Subject (user identifier) |
| `exp` | number | Yes | Expiration time (Unix timestamp) |
| `iat` | number | No | Issued at time |

*Either `sub` or `user_id` must be present

### Better Auth Custom Claims

| Claim | Type | Required | Description |
|-------|------|----------|-------------|
| `user_id` | string | Yes* | User identifier (alternative to sub) |
| `email` | string | No | User email (not used by backend) |

### User ID Resolution Order

1. Check for `sub` claim
2. If not present, check for `user_id` claim
3. If neither present, return 401 "Invalid token"

---

## Dependency Injection Pattern

### FastAPI Dependency

```python
# Pseudocode - not actual implementation
async def get_current_user(authorization: str = Header(...)) -> str:
    """
    Dependency that:
    1. Extracts token from Authorization header
    2. Verifies token
    3. Returns user_id string

    Raises HTTPException(401) on any failure
    """
```

### Usage in Route Handlers

```python
# Routes declare dependency to require authentication
@router.get("/tasks")
async def list_tasks(user_id: str = Depends(get_current_user)):
    # user_id is guaranteed valid here
    return get_tasks_for_user(user_id)
```

---

## Error Response Format

All authentication errors return:

```json
{
  "error": "<message>",
  "code": "<code>"
}
```

With HTTP status 401 Unauthorized.

---

## Security Guarantees

### What Middleware MUST Do

- [x] Reject requests without valid JWT
- [x] Verify signature matches BETTER_AUTH_SECRET
- [x] Reject expired tokens
- [x] Extract user_id for downstream use
- [x] Return consistent error format

### What Middleware MUST NOT Do

- [ ] Trust any user_id from request body
- [ ] Reveal specific failure reasons (beyond allowed messages)
- [ ] Cache tokens (stateless design)
- [ ] Accept tokens from query parameters
- [ ] Accept tokens from cookies (Bearer only)

---

## Environment Configuration

### Required Environment Variable

| Variable | Description | Example |
|----------|-------------|---------|
| `BETTER_AUTH_SECRET` | Shared secret for JWT verification | `your-256-bit-secret` |

### Startup Behavior

- If `BETTER_AUTH_SECRET` is not set, application MUST fail to start
- Error message: "Missing required environment variable: BETTER_AUTH_SECRET"

---

## Testing Scenarios

### Must Pass

| Test | Expected |
|------|----------|
| Valid token, valid user | 200 + user_id in context |
| Valid token, request to protected endpoint | Success |
| Token with future exp | Success |

### Must Fail with 401

| Test | Expected Message |
|------|------------------|
| No Authorization header | "Authentication required" |
| Empty Authorization header | "Authentication required" |
| Basic scheme instead of Bearer | "Invalid authorization scheme" |
| Malformed token (not 3 parts) | "Invalid token" |
| Wrong signature | "Invalid token" |
| Expired token | "Token expired" |
| Missing sub and user_id claims | "Invalid token" |

---

## Flow Diagram

```
Request arrives
       │
       ▼
┌──────────────────────────────┐
│ Has Authorization header?     │
└──────────────┬───────────────┘
               │
      No ──────┼────── Yes
               │        │
               ▼        ▼
         401 Error   ┌──────────────────┐
                     │ Is Bearer scheme? │
                     └─────────┬────────┘
                               │
                      No ──────┼────── Yes
                               │        │
                               ▼        ▼
                         401 Error   ┌────────────────────┐
                                     │ Verify JWT signature│
                                     └─────────┬──────────┘
                                               │
                                      Fail ────┼──── Pass
                                               │      │
                                               ▼      ▼
                                         401 Error  ┌────────────────┐
                                                    │ Check exp claim │
                                                    └─────────┬──────┘
                                                              │
                                                    Expired ──┼── Valid
                                                              │    │
                                                              ▼    ▼
                                                        401 Error  ┌──────────────────┐
                                                                   │ Extract user_id   │
                                                                   └─────────┬────────┘
                                                                             │
                                                                    Missing ─┼─ Found
                                                                             │    │
                                                                             ▼    ▼
                                                                       401 Error  SUCCESS
                                                                                   │
                                                                                   ▼
                                                                         Route handler
                                                                         receives user_id
```
