# Research: Backend API - Todo Web Application

**Feature Branch**: `002-backend-api`
**Created**: 2026-01-16
**Status**: Complete

## Overview

This document captures research findings and technical decisions for the backend API implementation. All decisions align with the constitution's mandatory technology stack.

---

## 1. FastAPI Project Structure

### Decision
Use a modular FastAPI structure with routers, dependencies, and models separated into distinct modules.

### Rationale
- FastAPI's dependency injection system naturally supports modular architecture
- Constitution requires stateless design and separation of concerns (FR-002, FR-003)
- Enables independent testing of each component

### Alternatives Considered

| Alternative | Why Rejected |
|-------------|--------------|
| Single file application | Violates FR-004 (router organization requirement) |
| Django REST Framework | Constitution mandates FastAPI specifically |
| Flask | Constitution mandates FastAPI specifically |

### Implementation Pattern
```
backend/
├── app/
│   ├── main.py          # Application entry point, middleware
│   ├── config.py        # Environment variable loading
│   ├── dependencies.py  # Dependency injection (db, auth)
│   ├── models/          # SQLModel definitions
│   ├── routers/         # API route handlers
│   └── schemas/         # Pydantic request/response schemas
└── tests/
```

---

## 2. JWT Verification Strategy

### Decision
Use PyJWT library with HS256 algorithm to verify tokens signed by Better Auth using BETTER_AUTH_SECRET.

### Rationale
- Better Auth uses HS256 symmetric signing by default
- PyJWT is the standard Python JWT library
- Symmetric verification requires only the shared secret (BETTER_AUTH_SECRET)

### Alternatives Considered

| Alternative | Why Rejected |
|-------------|--------------|
| RS256 asymmetric | Better Auth default is HS256; would require configuration changes |
| python-jose | PyJWT is more widely used and maintained |
| authlib | Overkill for simple JWT verification |

### Key Implementation Notes
- Extract `sub` or `user_id` claim from JWT payload
- Verify `exp` claim for token expiry
- Return 401 on any verification failure
- Do NOT expose specific failure reasons (security)

---

## 3. SQLModel + Neon PostgreSQL Integration

### Decision
Use SQLModel with asyncpg driver via async SQLAlchemy engine for Neon PostgreSQL connection.

### Rationale
- Constitution mandates SQLModel ORM (Section III)
- Constitution mandates Neon Serverless PostgreSQL (Section III)
- Async driver improves connection pooling efficiency with serverless

### Alternatives Considered

| Alternative | Why Rejected |
|-------------|--------------|
| Synchronous psycopg2 | Less efficient with serverless cold starts |
| SQLAlchemy without SQLModel | Constitution mandates SQLModel |
| Tortoise ORM | Constitution mandates SQLModel |

### Connection String Pattern
```
postgresql+asyncpg://user:password@host/database?sslmode=require
```

### Key Implementation Notes
- Use connection pooling with reasonable limits (max 5-10 for serverless)
- Enable SSL mode for Neon security requirements
- Handle connection errors gracefully (FR-028)

---

## 4. User Identity from JWT

### Decision
Extract user identity from JWT `sub` claim (standard) or `user_id` claim (Better Auth specific). Store in request state via FastAPI dependency.

### Rationale
- Better Auth stores user ID in JWT claims
- FastAPI dependencies make user context available to all route handlers
- Spec requires JWT user_id as sole source of truth (FR-013)

### Alternatives Considered

| Alternative | Why Rejected |
|-------------|--------------|
| Accept user_id from request body | Security violation - clients can forge |
| Query user from database | Unnecessary - JWT already contains identity |
| Session-based auth | Constitution explicitly forbids session cookies |

### Key Implementation Notes
- Dependency returns user_id string
- Protected routes declare dependency to require authentication
- All task queries filter by this user_id (FR-014)

---

## 5. Error Response Format

### Decision
Standardize on `{"error": "message", "code": "ERROR_CODE"}` for all error responses.

### Rationale
- Matches frontend api-client.md contract expectations
- Provides both human-readable message and machine-parseable code
- Consistent across all error types (FR-029)

### Error Code Catalog

| HTTP Status | Code | When Used |
|-------------|------|-----------|
| 400 | VALIDATION_ERROR | Input validation failures |
| 400 | INVALID_REQUEST | Malformed JSON body |
| 401 | UNAUTHORIZED | Missing or invalid JWT |
| 401 | TOKEN_EXPIRED | Expired JWT |
| 404 | NOT_FOUND | Task doesn't exist or not owned |
| 500 | INTERNAL_ERROR | Unexpected server errors |

### Key Implementation Notes
- Never expose database errors or stack traces
- Use FastAPI exception handlers for consistency
- Log detailed errors server-side, return generic to client

---

## 6. UUID Generation Strategy

### Decision
Use Python's `uuid.uuid4()` for task IDs, stored as PostgreSQL UUID type.

### Rationale
- Spec requires UUID for task primary keys (FR-026)
- UUID4 provides cryptographic randomness
- PostgreSQL native UUID type is efficient for indexing

### Alternatives Considered

| Alternative | Why Rejected |
|-------------|--------------|
| Auto-increment integers | Reveals task count, not spec compliant |
| ULIDs | More complex, UUID meets requirements |
| Database-generated UUIDs | Less portable, prefer application control |

---

## 7. Timestamp Handling

### Decision
Use Python `datetime.utcnow()` for timestamps, store as PostgreSQL TIMESTAMP WITH TIME ZONE, serialize as ISO 8601 string.

### Rationale
- Spec requires ISO 8601 UTC timestamps (FR-038)
- PostgreSQL TIMESTAMPTZ handles timezone correctly
- Frontend expects ISO 8601 strings (api-client.md)

### Key Implementation Notes
- Always use UTC (never local time)
- Format: `2026-01-16T10:30:00Z`
- Server generates all timestamps (never trust client)

---

## 8. CORS Configuration

### Decision
Configure CORS middleware to allow frontend origin with credentials support.

### Rationale
- Frontend may run on different origin during development
- Production may have same-origin, but CORS is safe default
- Spec mentions CORS-ready requirement

### Configuration Pattern
```python
CORSMiddleware(
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

---

## 9. Input Validation Strategy

### Decision
Use Pydantic models for request body validation with custom validators for business rules.

### Rationale
- FastAPI native integration with Pydantic
- Automatic 422 responses for schema violations
- Custom validators handle title/description length limits

### Key Validations
- Title: required, 1-200 chars after trim
- Description: optional, 0-1000 chars
- user_id in body: ignored (stripped from input model)

---

## 10. Testing Strategy

### Decision
Use pytest with pytest-asyncio for async test support, httpx for API testing.

### Rationale
- pytest is Python standard for testing
- httpx provides async test client for FastAPI
- AsyncIO support needed for async database operations

### Test Categories
1. **Unit tests**: Individual functions (validation, JWT parsing)
2. **Integration tests**: Full API request/response cycles
3. **Security tests**: Auth bypass attempts, cross-user access

---

## Summary of Technical Stack

| Component | Decision |
|-----------|----------|
| Framework | FastAPI |
| ORM | SQLModel |
| Database | Neon PostgreSQL (asyncpg driver) |
| JWT Library | PyJWT |
| UUID | Python uuid.uuid4() |
| Timestamps | UTC, ISO 8601 |
| Validation | Pydantic |
| Testing | pytest + httpx |

All decisions align with constitution requirements and spec functional requirements.
