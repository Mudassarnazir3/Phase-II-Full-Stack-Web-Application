# Tasks: Backend API - Todo Web Application

**Input**: Design documents from `/specs/002-backend-api/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Included - spec requires comprehensive testing for security and validation boundaries.

**Organization**: Tasks grouped by user story priority for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US7)
- All paths are relative to repository root

## Path Conventions

- **Backend**: `backend/app/`, `backend/tests/`
- Structure per plan.md:
  ```
  backend/
  ├── app/
  │   ├── main.py, config.py, dependencies.py
  │   ├── models/, routers/, schemas/, db/
  └── tests/
  ```

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Create backend project structure and install dependencies

- [x] T001 Create backend directory structure per plan.md in backend/
- [x] T002 Create backend/requirements.txt with FastAPI, SQLModel, PyJWT, asyncpg, uvicorn, pydantic-settings
- [x] T003 [P] Create backend/requirements-dev.txt with pytest, pytest-asyncio, httpx, pytest-cov
- [x] T004 [P] Create backend/.env.example with DATABASE_URL, BETTER_AUTH_SECRET, BETTER_AUTH_URL
- [x] T005 [P] Create all __init__.py files in backend/app/ subdirectories

**Checkpoint**: Project structure ready, dependencies installable

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure required before ANY user story implementation

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Configuration & Application Entry

- [ ] T006 Implement Settings class with env validation in backend/app/config.py
- [ ] T007 Implement FastAPI application with CORS middleware in backend/app/main.py
- [ ] T008 [P] Implement health check endpoint GET /api/health in backend/app/main.py

### Database Infrastructure

- [ ] T009 Implement Task SQLModel with UUID, title, description, completed, user_id, timestamps in backend/app/models/task.py
- [ ] T010 Implement async database engine and session management in backend/app/db/session.py
- [ ] T011 Implement get_db dependency for session injection in backend/app/dependencies.py
- [ ] T012 Implement database initialization with table creation and index in backend/app/db/init.py

### Request/Response Schemas

- [ ] T013 [P] Implement TaskCreate schema (title required, description optional) in backend/app/schemas/task.py
- [ ] T014 [P] Implement TaskUpdate schema (all fields optional) in backend/app/schemas/task.py
- [ ] T015 [P] Implement TaskResponse schema with camelCase aliases in backend/app/schemas/task.py
- [ ] T016 [P] Implement TaskListResponse and ErrorResponse schemas in backend/app/schemas/task.py

### Error Handling Infrastructure

- [ ] T017 Implement global exception handlers for ValidationError, HTTPException, generic in backend/app/main.py
- [ ] T018 Implement JSON decode error handler returning 400 "Invalid request body" in backend/app/main.py
- [ ] T019 [P] Add security headers middleware (X-Content-Type-Options, X-Frame-Options) in backend/app/main.py

**Checkpoint**: Foundation ready - database connects, schemas defined, error handling consistent

---

## Phase 3: User Story 1 - JWT Authentication Validation (Priority: P1)

**Goal**: Validate JWT tokens from Authorization header and extract user identity

**Independent Test**: Send requests with valid, invalid, expired, and missing JWT tokens - verify correct acceptance/rejection

### Tests for User Story 1

- [ ] T020 [P] [US1] Test valid JWT token acceptance in backend/tests/test_auth.py
- [ ] T021 [P] [US1] Test missing Authorization header returns 401 in backend/tests/test_auth.py
- [ ] T022 [P] [US1] Test invalid/malformed token returns 401 in backend/tests/test_auth.py
- [ ] T023 [P] [US1] Test expired token returns 401 "Token expired" in backend/tests/test_auth.py
- [ ] T024 [P] [US1] Test wrong signature returns 401 in backend/tests/test_auth.py
- [ ] T025 [P] [US1] Test wrong scheme (Basic instead of Bearer) returns 401 in backend/tests/test_auth.py

### Implementation for User Story 1

- [ ] T026 [US1] Implement JWT verification function using PyJWT and BETTER_AUTH_SECRET in backend/app/dependencies.py
- [ ] T027 [US1] Implement get_current_user dependency extracting user_id from sub/user_id claim in backend/app/dependencies.py
- [ ] T028 [US1] Implement auth error responses with consistent format {"error", "code"} in backend/app/dependencies.py

**Checkpoint**: Authentication middleware complete - all auth tests pass

---

## Phase 4: User Story 2 - Task Retrieval for Authenticated User (Priority: P1)

**Goal**: List all tasks for authenticated user with strict user isolation

**Independent Test**: Create tasks for multiple users, verify each user only sees their own tasks

### Tests for User Story 2

- [ ] T029 [P] [US2] Test GET /api/tasks returns only user's tasks in backend/tests/test_tasks.py
- [ ] T030 [P] [US2] Test GET /api/tasks returns empty array when no tasks in backend/tests/test_tasks.py
- [ ] T031 [P] [US2] Test user A cannot see user B's tasks in backend/tests/test_tasks.py
- [ ] T032 [P] [US2] Test task list response format (id, title, description, completed, userId, createdAt, updatedAt) in backend/tests/test_tasks.py

### Implementation for User Story 2

- [ ] T033 [US2] Create tasks router file in backend/app/routers/tasks.py
- [ ] T034 [US2] Implement GET /api/tasks endpoint with user_id filter in backend/app/routers/tasks.py
- [ ] T035 [US2] Register tasks router in FastAPI app with /api prefix in backend/app/main.py

**Checkpoint**: Task listing works with user isolation - P1 stories complete

---

## Phase 5: User Story 3 - Task Creation (Priority: P2)

**Goal**: Create new tasks with validation, ownership from JWT, server-generated fields

**Independent Test**: Submit valid and invalid task data, verify creation or validation errors

### Tests for User Story 3

- [ ] T036 [P] [US3] Test POST /api/tasks with valid title creates task in backend/tests/test_tasks.py
- [ ] T037 [P] [US3] Test POST /api/tasks without title returns 400 in backend/tests/test_tasks.py
- [ ] T038 [P] [US3] Test POST /api/tasks with title >200 chars returns 400 in backend/tests/test_tasks.py
- [ ] T039 [P] [US3] Test POST /api/tasks with description >1000 chars returns 400 in backend/tests/test_tasks.py
- [ ] T040 [P] [US3] Test POST /api/tasks ignores forged user_id in body in backend/tests/test_tasks.py
- [ ] T041 [P] [US3] Test created task has completed=false, server timestamps in backend/tests/test_tasks.py

### Implementation for User Story 3

- [ ] T042 [US3] Implement POST /api/tasks endpoint with validation in backend/app/routers/tasks.py
- [ ] T043 [US3] Add title/description length validation with custom error messages in backend/app/schemas/task.py
- [ ] T044 [US3] Ensure user_id set from JWT, completed defaults false, timestamps generated in backend/app/routers/tasks.py

**Checkpoint**: Task creation works with full validation

---

## Phase 6: User Story 4 - Task Completion Toggle (Priority: P2)

**Goal**: Toggle task completion status for owned tasks only

**Independent Test**: Toggle owned and non-owned tasks, verify toggle or 404 error

### Tests for User Story 4

- [ ] T045 [P] [US4] Test PATCH /api/tasks/:id/toggle flips completed from false to true in backend/tests/test_tasks.py
- [ ] T046 [P] [US4] Test PATCH /api/tasks/:id/toggle flips completed from true to false in backend/tests/test_tasks.py
- [ ] T047 [P] [US4] Test toggle on non-owned task returns 404 in backend/tests/test_tasks.py
- [ ] T048 [P] [US4] Test toggle on non-existent task returns 404 in backend/tests/test_tasks.py
- [ ] T049 [P] [US4] Test toggle updates updatedAt timestamp in backend/tests/test_tasks.py

### Implementation for User Story 4

- [ ] T050 [US4] Implement PATCH /api/tasks/:id/toggle endpoint with ownership check in backend/app/routers/tasks.py
- [ ] T051 [US4] Ensure toggle updates updatedAt and returns full task in backend/app/routers/tasks.py

**Checkpoint**: Task toggle works with ownership enforcement - P2 stories complete

---

## Phase 7: User Story 5 - Task Update (Priority: P3)

**Goal**: Update task title and/or description for owned tasks

**Independent Test**: Update owned and non-owned tasks with valid and invalid data

### Tests for User Story 5

- [ ] T052 [P] [US5] Test PUT /api/tasks/:id updates title in backend/tests/test_tasks.py
- [ ] T053 [P] [US5] Test PUT /api/tasks/:id updates description in backend/tests/test_tasks.py
- [ ] T054 [P] [US5] Test PUT /api/tasks/:id with empty title returns 400 in backend/tests/test_tasks.py
- [ ] T055 [P] [US5] Test PUT /api/tasks/:id on non-owned task returns 404 in backend/tests/test_tasks.py
- [ ] T056 [P] [US5] Test PUT /api/tasks/:id ignores user_id in body in backend/tests/test_tasks.py
- [ ] T057 [P] [US5] Test partial update only changes specified fields in backend/tests/test_tasks.py

### Implementation for User Story 5

- [ ] T058 [US5] Implement PUT /api/tasks/:id endpoint with ownership check in backend/app/routers/tasks.py
- [ ] T059 [US5] Implement partial update logic (only update provided fields) in backend/app/routers/tasks.py

**Checkpoint**: Task update works with partial updates and ownership

---

## Phase 8: User Story 6 - Task Deletion (Priority: P3)

**Goal**: Permanently delete owned tasks

**Independent Test**: Delete owned and non-owned tasks, verify removal or 404 error

### Tests for User Story 6

- [ ] T060 [P] [US6] Test DELETE /api/tasks/:id removes task from database in backend/tests/test_tasks.py
- [ ] T061 [P] [US6] Test DELETE /api/tasks/:id on non-owned task returns 404 in backend/tests/test_tasks.py
- [ ] T062 [P] [US6] Test DELETE /api/tasks/:id on non-existent task returns 404 in backend/tests/test_tasks.py
- [ ] T063 [P] [US6] Test DELETE returns success message not deleted task in backend/tests/test_tasks.py

### Implementation for User Story 6

- [ ] T064 [US6] Implement DELETE /api/tasks/:id endpoint with ownership check in backend/app/routers/tasks.py

**Checkpoint**: Task deletion works with ownership enforcement

---

## Phase 9: User Story 7 - Read Single Task (Priority: P3)

**Goal**: Retrieve single task by ID for owned tasks

**Independent Test**: Request owned and non-owned tasks by ID, verify response or 404

### Tests for User Story 7

- [ ] T065 [P] [US7] Test GET /api/tasks/:id returns owned task in backend/tests/test_tasks.py
- [ ] T066 [P] [US7] Test GET /api/tasks/:id on non-owned task returns 404 in backend/tests/test_tasks.py
- [ ] T067 [P] [US7] Test GET /api/tasks/:id on non-existent task returns 404 in backend/tests/test_tasks.py

### Implementation for User Story 7

- [ ] T068 [US7] Implement GET /api/tasks/:id endpoint with ownership check in backend/app/routers/tasks.py

**Checkpoint**: All P3 stories complete - full CRUD operational

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Security hardening, integration verification, test coverage

### Security Tests

- [ ] T069 [P] Test cross-user isolation across all endpoints in backend/tests/test_security.py
- [ ] T070 [P] Test forged user_id in request body is ignored for all write operations in backend/tests/test_security.py
- [ ] T071 [P] Test no stack traces exposed in any error response in backend/tests/test_security.py

### Validation Boundary Tests

- [ ] T072 [P] Test title at exactly 200 chars passes in backend/tests/test_validation.py
- [ ] T073 [P] Test title at 201 chars fails in backend/tests/test_validation.py
- [ ] T074 [P] Test description at exactly 1000 chars passes in backend/tests/test_validation.py
- [ ] T075 [P] Test description at 1001 chars fails in backend/tests/test_validation.py
- [ ] T076 [P] Test whitespace-only title fails in backend/tests/test_validation.py

### Integration Verification

- [ ] T077 Verify response formats match frontend api-client.md contract
- [ ] T078 Verify CORS configuration allows frontend origin
- [ ] T079 Verify all timestamps are ISO 8601 UTC format

### Documentation

- [ ] T080 [P] Create backend/README.md with setup and run instructions
- [ ] T081 Run test coverage report and verify >90% coverage

**Checkpoint**: All tests pass, security verified, documentation complete

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup)
     │
     ▼
Phase 2 (Foundational) ◄── BLOCKS ALL USER STORIES
     │
     ├──────────────────────────────────────┐
     ▼                                      │
Phase 3 (US1: Auth) ─┐                      │
     │               │                      │
     ▼               │                      │
Phase 4 (US2: List) ─┴─► P1 Complete        │
     │                                      │
     ├──► Phase 5 (US3: Create) ─┐          │
     │                           │          │
     ├──► Phase 6 (US4: Toggle) ─┴─► P2 Complete
     │
     ├──► Phase 7 (US5: Update) ─┐
     │                           │
     ├──► Phase 8 (US6: Delete) ─┼─► P3 Complete
     │                           │
     └──► Phase 9 (US7: Read) ───┘
                    │
                    ▼
           Phase 10 (Polish)
```

### User Story Dependencies

| Story | Depends On | Can Parallel With |
|-------|------------|-------------------|
| US1 (Auth) | Phase 2 | None (must complete first) |
| US2 (List) | US1 | None (needs auth) |
| US3 (Create) | US1, US2 | US4 |
| US4 (Toggle) | US1, US2 | US3 |
| US5 (Update) | US1, US2 | US6, US7 |
| US6 (Delete) | US1, US2 | US5, US7 |
| US7 (Read) | US1, US2 | US5, US6 |

### Parallel Opportunities

**Within Phase 2 (Foundational)**:
- T013-T016 (schemas) can run in parallel
- T008, T019 can run in parallel

**Test Parallelism per Story**:
- All [P] test tasks within a story can run together
- Tests should be written FIRST, verified to FAIL, then implementation

**Cross-Story Parallelism after P1**:
- US3 and US4 can be developed in parallel
- US5, US6, US7 can all be developed in parallel

---

## Parallel Example: Phase 5 (US3)

```bash
# First: Launch all tests (should fail)
Task: T036 - Test POST /api/tasks with valid title
Task: T037 - Test POST /api/tasks without title returns 400
Task: T038 - Test POST /api/tasks with title >200 chars returns 400
Task: T039 - Test POST /api/tasks with description >1000 chars returns 400
Task: T040 - Test POST /api/tasks ignores forged user_id
Task: T041 - Test created task has defaults

# Then: Sequential implementation
Task: T042 - Implement POST /api/tasks endpoint
Task: T043 - Add validation with custom messages
Task: T044 - Ensure JWT user_id, defaults, timestamps
```

---

## Implementation Strategy

### MVP First (P1 Stories Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T019)
3. Complete Phase 3: US1 Auth (T020-T028)
4. Complete Phase 4: US2 List (T029-T035)
5. **STOP and VALIDATE**: Backend can authenticate and list tasks
6. **MVP READY**: Minimal but functional authenticated task list

### Incremental Delivery

| Increment | Stories | Capability |
|-----------|---------|------------|
| MVP | US1 + US2 | Auth + List tasks |
| +P2 | US3 + US4 | Create + Toggle |
| +P3 | US5 + US6 + US7 | Update + Delete + Read single |
| Final | Polish | Security hardened, tested |

### Task Counts

| Phase | Tasks | Cumulative |
|-------|-------|------------|
| Setup | 5 | 5 |
| Foundational | 14 | 19 |
| US1 (P1) | 9 | 28 |
| US2 (P1) | 7 | 35 |
| US3 (P2) | 9 | 44 |
| US4 (P2) | 7 | 51 |
| US5 (P3) | 8 | 59 |
| US6 (P3) | 5 | 64 |
| US7 (P3) | 4 | 68 |
| Polish | 13 | 81 |

**Total: 81 tasks**

---

## Notes

- All tasks follow checklist format: `- [ ] [ID] [P?] [Story?] Description with file path`
- Tests included per spec security requirements
- [P] tasks can run in parallel within their story
- Each user story is independently testable after completion
- Commit after each logical task group
- Verify tests FAIL before implementing
- Security tests in Phase 10 verify cross-cutting concerns
