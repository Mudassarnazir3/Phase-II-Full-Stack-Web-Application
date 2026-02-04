# Implementation Plan: Backend API - Todo Web Application

**Branch**: `002-backend-api` | **Date**: 2026-01-16 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-backend-api/spec.md`

## Summary

Implement a stateless FastAPI backend that provides JWT-authenticated REST API endpoints for task management. The backend validates Better Auth JWT tokens, enforces user-based data isolation at the query level, and connects to Neon PostgreSQL via SQLModel ORM. All operations are scoped to the authenticated user with no cross-user data access.

---

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI, SQLModel, PyJWT, asyncpg, uvicorn
**Storage**: Neon Serverless PostgreSQL (via asyncpg driver)
**Testing**: pytest, pytest-asyncio, httpx
**Target Platform**: Linux server / Docker container
**Project Type**: Web application (backend only)
**Performance Goals**: <500ms response time, 100 concurrent requests
**Constraints**: Stateless, JWT-only auth, no session cookies
**Scale/Scope**: Multi-user todo application, single tasks table

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| **I. Spec Authority** | ✅ PASS | Plan derived from spec.md, no invented features |
| **II. Scope Boundary** | ✅ PASS | Todo API only, no admin roles, no Phase III features |
| **III. Technology Stack** | ✅ PASS | FastAPI + SQLModel + Neon PostgreSQL as mandated |
| **IV. API Architecture** | ✅ PASS | RESTful under /api/*, no GraphQL/RPC |
| **V. Database Integrity** | ✅ PASS | tasks.user_id indexed, ownership enforced |
| **VI. UI Security** | ✅ N/A | Backend only - no UI in this spec |
| **VII. Agent Conduct** | ✅ PASS | Plan only, no code written |
| **VIII. Change Control** | ✅ PASS | Spec created before plan |

**Gate Result**: PASSED - Proceed to implementation phases

---

## Project Structure

### Documentation (this feature)

```text
specs/002-backend-api/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Technical decisions
├── data-model.md        # Database schema
├── quickstart.md        # Setup guide
├── contracts/
│   ├── api-endpoints.md # REST API contract
│   └── auth-middleware.md # JWT verification contract
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # [Created by /sp.tasks]
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry
│   ├── config.py            # Environment configuration
│   ├── dependencies.py      # DI: auth, database session
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py          # Task SQLModel
│   ├── routers/
│   │   ├── __init__.py
│   │   └── tasks.py         # Task CRUD endpoints
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── task.py          # Pydantic request/response
│   └── db/
│       ├── __init__.py
│       ├── session.py       # Async engine + session
│       └── init.py          # Table creation
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Fixtures
│   ├── test_auth.py         # Auth middleware tests
│   └── test_tasks.py        # Task endpoint tests
├── requirements.txt
├── .env.example
└── README.md
```

**Structure Decision**: Web application structure (backend only). Frontend exists separately in `/frontend/`.

---

## Complexity Tracking

> No violations requiring justification. Plan uses minimal viable architecture.

| Aspect | Decision | Why Minimal |
|--------|----------|-------------|
| Project count | 1 (backend) | Single responsibility |
| Database tables | 1 (tasks) | No user table needed (JWT auth) |
| Dependencies | 5 core packages | FastAPI ecosystem essentials only |
| Patterns | None | Direct route → db, no repository layer |

---

## Implementation Phases

### Phase 1: Backend Foundation

**Purpose**: Establish project structure, configuration, and application entry point

**Responsible Agent**: Backend API Implementer

**Input Specs**:
- `specs/002-backend-api/spec.md` (FR-001 to FR-006)
- `specs/002-backend-api/quickstart.md`

**Ordered Tasks**:

1. **Create backend directory structure**
   - Create `backend/app/` with subdirectories
   - Create `backend/tests/` directory
   - Create empty `__init__.py` files

2. **Create requirements.txt**
   - FastAPI, uvicorn, SQLModel, asyncpg
   - PyJWT, python-dotenv, pydantic-settings
   - pytest, pytest-asyncio, httpx (dev)

3. **Implement config.py**
   - Load environment variables using pydantic-settings
   - Define Settings class with DATABASE_URL, BETTER_AUTH_SECRET, BETTER_AUTH_URL
   - Fail fast if required variables missing (FR-006)

4. **Implement main.py entry point**
   - Create FastAPI application
   - Configure CORS middleware
   - Include router placeholders
   - Add startup/shutdown events for database

5. **Create .env.example**
   - Document all required environment variables

**Dependencies**: None (first phase)

**Output Artifacts**:
- `backend/` directory structure
- `backend/requirements.txt`
- `backend/app/config.py`
- `backend/app/main.py`
- `backend/.env.example`

**Acceptance Criteria**:
- [ ] `pip install -r requirements.txt` succeeds
- [ ] Application starts without .env (fails with clear error)
- [ ] Application starts with valid .env (logs ready message)
- [ ] Health endpoint returns 200 (placeholder OK)

---

### Phase 2: Authentication & Security Layer

**Purpose**: Implement JWT verification and user identity extraction

**Responsible Agent**: Backend API Implementer

**Input Specs**:
- `specs/002-backend-api/spec.md` (FR-007 to FR-013)
- `specs/002-backend-api/contracts/auth-middleware.md`

**Ordered Tasks**:

1. **Implement JWT verification function**
   - Extract token from Authorization header
   - Verify Bearer scheme
   - Decode and verify using BETTER_AUTH_SECRET (HS256)
   - Check expiration claim
   - Return 401 on any failure with appropriate message

2. **Implement get_current_user dependency**
   - FastAPI Depends function
   - Calls JWT verification
   - Extracts user_id from `sub` or `user_id` claim
   - Returns user_id string for route handlers

3. **Create auth error responses**
   - Consistent error format: `{"error": "...", "code": "..."}`
   - Map failure types to messages per contract
   - HTTPException with 401 status

4. **Write auth middleware tests**
   - Test valid token acceptance
   - Test missing header rejection
   - Test invalid scheme rejection
   - Test expired token rejection
   - Test wrong signature rejection

**Dependencies**: Phase 1 complete

**Output Artifacts**:
- `backend/app/dependencies.py` (get_current_user)
- `backend/tests/test_auth.py`

**Acceptance Criteria**:
- [ ] Valid JWT returns user_id to route handler
- [ ] Missing Authorization header returns 401 "Authentication required"
- [ ] Invalid token returns 401 "Invalid token"
- [ ] Expired token returns 401 "Token expired"
- [ ] All auth tests pass

---

### Phase 3: Database Layer

**Purpose**: Implement SQLModel schema and database connection

**Responsible Agent**: Database Engineer

**Input Specs**:
- `specs/002-backend-api/spec.md` (FR-023 to FR-028)
- `specs/002-backend-api/data-model.md`

**Ordered Tasks**:

1. **Implement Task SQLModel**
   - UUID primary key (uuid.uuid4)
   - title: str (max 200)
   - description: Optional[str] (max 1000)
   - completed: bool (default False)
   - user_id: str (indexed)
   - created_at: datetime (UTC)
   - updated_at: datetime (UTC)

2. **Implement database session management**
   - Async SQLAlchemy engine with asyncpg
   - Neon-compatible connection string parsing
   - SSL mode enabled
   - Connection pooling (max 10)

3. **Implement get_db dependency**
   - Async context manager for session
   - Proper session cleanup on request end

4. **Create database initialization script**
   - Create tables from SQLModel metadata
   - Create user_id index
   - Idempotent (safe to run multiple times)

5. **Write database connection tests**
   - Test connection to database
   - Test table creation
   - Test basic CRUD operations on Task

**Dependencies**: Phase 1 complete

**Output Artifacts**:
- `backend/app/models/task.py`
- `backend/app/db/session.py`
- `backend/app/db/init.py`
- `backend/app/dependencies.py` (get_db added)

**Acceptance Criteria**:
- [ ] Database connection succeeds with valid DATABASE_URL
- [ ] Tasks table created with all columns
- [ ] user_id index created
- [ ] Task CRUD operations work at model level
- [ ] Connection errors return 500 (not stack trace)

---

### Phase 4: API Layer (Task Operations)

**Purpose**: Implement REST API endpoints for task CRUD

**Responsible Agent**: Backend API Implementer

**Input Specs**:
- `specs/002-backend-api/spec.md` (FR-014 to FR-022, FR-035 to FR-039)
- `specs/002-backend-api/contracts/api-endpoints.md`

**Ordered Tasks**:

1. **Create Pydantic request/response schemas**
   - TaskCreate (title required, description optional)
   - TaskUpdate (all fields optional)
   - TaskResponse (full task with camelCase fields)
   - TaskListResponse (tasks array wrapper)
   - ErrorResponse (error + code)

2. **Implement GET /api/tasks (list)**
   - Require auth dependency
   - Query tasks WHERE user_id = jwt_user_id
   - Return {"tasks": [...]}
   - Return empty array if no tasks

3. **Implement POST /api/tasks (create)**
   - Require auth dependency
   - Validate title required, lengths
   - Set user_id from JWT (ignore body user_id)
   - Set completed=false, generate timestamps
   - Return 201 with {"task": {...}}

4. **Implement GET /api/tasks/{id} (read single)**
   - Require auth dependency
   - Query WHERE id AND user_id
   - Return 404 if not found OR not owned
   - Return {"task": {...}}

5. **Implement PUT /api/tasks/{id} (update)**
   - Require auth dependency
   - Query WHERE id AND user_id
   - Return 404 if not found OR not owned
   - Validate title not empty if provided
   - Update only provided fields
   - Update updatedAt
   - Return {"task": {...}}

6. **Implement PATCH /api/tasks/{id}/toggle**
   - Require auth dependency
   - Query WHERE id AND user_id
   - Return 404 if not found OR not owned
   - Flip completed boolean
   - Update updatedAt
   - Return {"task": {...}}

7. **Implement DELETE /api/tasks/{id}**
   - Require auth dependency
   - Query WHERE id AND user_id
   - Return 404 if not found OR not owned
   - Delete from database
   - Return {"message": "Task deleted successfully"}

8. **Register router in main.py**
   - Include tasks router with /api prefix
   - Ensure CORS applies to all routes

**Dependencies**: Phase 2 and Phase 3 complete

**Output Artifacts**:
- `backend/app/schemas/task.py`
- `backend/app/routers/tasks.py`
- Updated `backend/app/main.py`

**Acceptance Criteria**:
- [ ] All 6 task endpoints functional
- [ ] All endpoints require valid JWT
- [ ] All queries filter by user_id
- [ ] Response format matches contract
- [ ] Status codes correct (200, 201, 400, 401, 404)

---

### Phase 5: Error Handling & Hardening

**Purpose**: Implement consistent error handling and security hardening

**Responsible Agent**: Backend API Implementer

**Input Specs**:
- `specs/002-backend-api/spec.md` (FR-029 to FR-034)

**Ordered Tasks**:

1. **Implement global exception handlers**
   - RequestValidationError → 400 with formatted message
   - HTTPException → pass through
   - Generic Exception → 500 "Internal server error"

2. **Ensure no stack traces in responses**
   - Log full errors server-side
   - Return generic message to client

3. **Implement request body validation error formatting**
   - Convert Pydantic errors to user-friendly messages
   - Use error code VALIDATION_ERROR

4. **Implement malformed JSON handling**
   - Catch JSONDecodeError
   - Return 400 "Invalid request body"

5. **Add security headers middleware**
   - X-Content-Type-Options: nosniff
   - X-Frame-Options: DENY
   - (HTTPS handled by deployment)

**Dependencies**: Phase 4 complete

**Output Artifacts**:
- Updated `backend/app/main.py` (exception handlers)

**Acceptance Criteria**:
- [ ] Validation errors return 400 with specific message
- [ ] Malformed JSON returns 400 "Invalid request body"
- [ ] Unexpected errors return 500 generic message
- [ ] No stack traces in any error response
- [ ] Security headers present in responses

---

### Phase 6: Frontend Integration Readiness

**Purpose**: Verify backend meets frontend contract requirements

**Responsible Agent**: Integration Tester

**Input Specs**:
- `specs/001-frontend-ui/contracts/api-client.md`
- `specs/002-backend-api/contracts/api-endpoints.md`

**Ordered Tasks**:

1. **Verify response format compatibility**
   - Task object fields match frontend expectations
   - Timestamps in ISO 8601 format
   - camelCase field names (userId, createdAt, updatedAt)
   - Wrapper objects (tasks, task, message)

2. **Verify error response compatibility**
   - Error format: {"error": "...", "code": "..."}
   - Error codes match frontend expectations
   - Status codes trigger correct frontend behavior

3. **Verify CORS configuration**
   - Frontend origin allowed
   - Credentials allowed
   - Required methods allowed
   - Authorization header allowed

4. **Verify authentication flow**
   - Bearer token accepted from Authorization header
   - 401 triggers frontend redirect to signin
   - Token expiry handled correctly

**Dependencies**: Phase 5 complete

**Output Artifacts**:
- Integration test results document
- Contract compliance checklist

**Acceptance Criteria**:
- [ ] All response fields match frontend TypeScript types
- [ ] All error codes match frontend error handling
- [ ] CORS preflight requests succeed
- [ ] Frontend can authenticate and fetch tasks

---

### Phase 7: Validation & Integration Testing

**Purpose**: Comprehensive testing of all requirements and security guarantees

**Responsible Agent**: Integration Tester

**Input Specs**:
- `specs/002-backend-api/spec.md` (all acceptance scenarios)
- `specs/002-backend-api/checklists/requirements.md`

**Ordered Tasks**:

1. **Write task endpoint integration tests**
   - Test all 7 user stories acceptance scenarios
   - Test with real database
   - Test with real JWT tokens

2. **Write security boundary tests**
   - User A cannot access User B's tasks
   - Forged user_id in body is ignored
   - Invalid tokens rejected
   - Missing tokens rejected

3. **Write validation boundary tests**
   - Title at exactly 200 chars (pass)
   - Title at 201 chars (fail)
   - Description at exactly 1000 chars (pass)
   - Description at 1001 chars (fail)
   - Empty title (fail)
   - Whitespace-only title (fail)

4. **Write performance baseline tests**
   - Response time under 500ms
   - No degradation at 100 concurrent requests

5. **Generate test coverage report**
   - Target: >90% line coverage
   - All critical paths covered

6. **Complete spec compliance checklist**
   - Verify all 39 FRs implemented
   - Verify all 11 SCs measurable

**Dependencies**: Phase 6 complete

**Output Artifacts**:
- `backend/tests/test_tasks.py` (comprehensive)
- `backend/tests/test_security.py`
- Test coverage report
- Compliance checklist

**Acceptance Criteria**:
- [ ] All acceptance scenarios pass
- [ ] Zero cross-user data leakage
- [ ] All validation boundaries correct
- [ ] Performance targets met
- [ ] >90% test coverage
- [ ] All spec requirements verified

---

## Quality & Security Checkpoints

### Checkpoint 1: After Phase 2 (Auth Layer)

| Check | Pass Criteria |
|-------|---------------|
| Auth bypass prevention | No route accessible without valid JWT |
| Token verification | Invalid/expired tokens rejected 100% |
| User identity | user_id extracted from JWT claims only |

### Checkpoint 2: After Phase 4 (API Layer)

| Check | Pass Criteria |
|-------|---------------|
| Cross-user isolation | All queries include user_id filter |
| Ownership verification | Non-owned tasks return 404 |
| user_id immutability | Request body user_id ignored |

### Checkpoint 3: After Phase 5 (Error Handling)

| Check | Pass Criteria |
|-------|---------------|
| Error leakage prevention | No stack traces in responses |
| Validation messages | Specific, actionable error messages |
| Generic 500 | Internal errors don't expose details |

### Checkpoint 4: After Phase 7 (Final)

| Check | Pass Criteria |
|-------|---------------|
| Spec compliance | All 39 FRs implemented |
| Success criteria | All 11 SCs verifiable |
| Frontend contract | Response formats match exactly |
| Constitution | All 8 principles satisfied |

**GATE**: Failure at any checkpoint blocks progression to next phase.

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Neon connection issues | Test with real Neon early in Phase 3 |
| JWT format mismatch | Verify Better Auth token structure before Phase 2 |
| Field name mismatch | Use explicit serialization aliases |
| Missing index | Verify index creation in Phase 3 acceptance |

---

## Next Steps

1. Run `/sp.tasks` to generate ordered implementation tasks
2. Assign tasks to appropriate agents
3. Execute phases in order with checkpoint verification
4. Do not proceed past failed checkpoints
