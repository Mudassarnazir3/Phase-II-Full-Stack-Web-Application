# Feature Specification: Backend API - Todo Web Application

**Feature Branch**: `002-backend-api`
**Created**: 2026-01-16
**Status**: Draft
**Input**: User description: "Complete backend specification for Phase II Todo Full-Stack Web Application - FastAPI, SQLModel, JWT authentication, Neon PostgreSQL"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - JWT Authentication Validation (Priority: P1)

The backend receives API requests from authenticated frontend users. Each request carries a JWT token in the Authorization header. The backend must validate this token, extract user identity, and enforce that users can only access their own data.

**Why this priority**: Authentication is the security foundation. Without JWT validation, no other API functionality can be trusted. This is the gatekeeper for all protected resources.

**Independent Test**: Can be fully tested by sending requests with valid, invalid, expired, and missing JWT tokens and verifying correct acceptance/rejection behavior. Delivers secure API access control.

**Acceptance Scenarios**:

1. **Given** a request with a valid JWT token in Authorization header, **When** the backend processes the request, **Then** user identity is extracted from token and request proceeds
2. **Given** a request with no Authorization header, **When** the backend processes a protected endpoint, **Then** 401 Unauthorized is returned with error message "Authentication required"
3. **Given** a request with an expired JWT token, **When** the backend validates the token, **Then** 401 Unauthorized is returned with error message "Token expired"
4. **Given** a request with a malformed JWT token, **When** the backend validates the token, **Then** 401 Unauthorized is returned with error message "Invalid token"
5. **Given** a request with a JWT signed with wrong secret, **When** the backend validates the token, **Then** 401 Unauthorized is returned with error message "Invalid token"

---

### User Story 2 - Task Retrieval for Authenticated User (Priority: P1)

An authenticated user requests their task list. The backend retrieves only tasks belonging to that user, ensuring complete data isolation from other users.

**Why this priority**: Reading tasks is the primary operation users perform. Without task retrieval, the todo application has no core value. This is the foundation of the user experience.

**Independent Test**: Can be fully tested by creating tasks for multiple users, then requesting tasks with each user's token and verifying strict user isolation. Delivers secure, personalized task list.

**Acceptance Scenarios**:

1. **Given** an authenticated user with existing tasks, **When** they request task list, **Then** only their tasks are returned in response
2. **Given** an authenticated user with no tasks, **When** they request task list, **Then** empty array is returned (not null, not error)
3. **Given** multiple users exist with tasks, **When** user A requests tasks, **Then** user A receives zero tasks belonging to user B
4. **Given** database contains 1000 tasks across users, **When** user requests their 10 tasks, **Then** only those 10 tasks are returned efficiently
5. **Given** an authenticated request, **When** task list is returned, **Then** each task includes id, title, description, completed, userId, createdAt, updatedAt

---

### User Story 3 - Task Creation (Priority: P2)

An authenticated user creates a new task. The backend validates input, assigns ownership to the authenticated user (ignoring any user ID in request body), and persists the task with server-generated timestamps.

**Why this priority**: Creating tasks is how users populate their todo list. After viewing tasks, creation is the next essential operation.

**Independent Test**: Can be fully tested by submitting valid and invalid task data and verifying correct creation or validation error behavior. Delivers task creation capability.

**Acceptance Scenarios**:

1. **Given** valid task data with title, **When** user creates task, **Then** task is persisted with user_id from JWT (not from request body)
2. **Given** task data with title and description, **When** user creates task, **Then** both fields are stored correctly
3. **Given** task data without title, **When** user creates task, **Then** 400 Bad Request with error "Title is required"
4. **Given** task data with title exceeding 200 characters, **When** user creates task, **Then** 400 Bad Request with error "Title must be 200 characters or less"
5. **Given** task data with description exceeding 1000 characters, **When** user creates task, **Then** 400 Bad Request with error "Description must be 1000 characters or less"
6. **Given** task data includes a forged user_id field, **When** user creates task, **Then** forged user_id is ignored and JWT user_id is used
7. **Given** successful task creation, **When** response is returned, **Then** completed defaults to false, createdAt and updatedAt are server-generated

---

### User Story 4 - Task Completion Toggle (Priority: P2)

An authenticated user toggles a task's completion status. The backend verifies task ownership, toggles the boolean value, and returns the updated task.

**Why this priority**: Marking tasks complete is the fundamental todo interaction. It's how users track progress on their tasks.

**Independent Test**: Can be fully tested by toggling owned and non-owned tasks and verifying correct toggle or authorization error. Delivers task completion tracking.

**Acceptance Scenarios**:

1. **Given** user owns incomplete task, **When** toggle is requested, **Then** task completed becomes true and updatedAt is refreshed
2. **Given** user owns complete task, **When** toggle is requested, **Then** task completed becomes false and updatedAt is refreshed
3. **Given** task belongs to different user, **When** toggle is requested, **Then** 404 Not Found is returned (not 403, to prevent user enumeration)
4. **Given** task ID does not exist, **When** toggle is requested, **Then** 404 Not Found is returned
5. **Given** successful toggle, **When** response is returned, **Then** full updated task object is included

---

### User Story 5 - Task Update (Priority: P3)

An authenticated user updates a task's title or description. The backend validates ownership, validates input, and persists changes.

**Why this priority**: Editing allows users to refine tasks. Less critical than creation and completion but important for task management.

**Independent Test**: Can be fully tested by updating owned and non-owned tasks with valid and invalid data. Delivers task editing capability.

**Acceptance Scenarios**:

1. **Given** user owns task, **When** title is updated with valid value, **Then** title is changed and updatedAt is refreshed
2. **Given** user owns task, **When** description is updated, **Then** description is changed and updatedAt is refreshed
3. **Given** user owns task, **When** title is set to empty string, **Then** 400 Bad Request with error "Title cannot be empty"
4. **Given** task belongs to different user, **When** update is requested, **Then** 404 Not Found is returned
5. **Given** update request includes user_id field, **When** processed, **Then** user_id field is ignored (immutable)
6. **Given** partial update (only title OR only description), **When** processed, **Then** only specified fields are changed

---

### User Story 6 - Task Deletion (Priority: P3)

An authenticated user deletes a task. The backend verifies ownership and permanently removes the task from the database.

**Why this priority**: Deletion is useful for cleanup but less frequently used. Users can manage their list effectively without it.

**Independent Test**: Can be fully tested by deleting owned and non-owned tasks and verifying correct removal or authorization error. Delivers task removal capability.

**Acceptance Scenarios**:

1. **Given** user owns task, **When** delete is requested, **Then** task is permanently removed from database
2. **Given** task belongs to different user, **When** delete is requested, **Then** 404 Not Found is returned
3. **Given** task ID does not exist, **When** delete is requested, **Then** 404 Not Found is returned
4. **Given** successful deletion, **When** response is returned, **Then** success message is returned (not the deleted task)
5. **Given** task is deleted, **When** subsequent operations reference that task ID, **Then** 404 Not Found is returned

---

### User Story 7 - Read Single Task (Priority: P3)

An authenticated user retrieves a single task by ID. The backend verifies ownership and returns the complete task details.

**Why this priority**: Single task retrieval supports detailed views and is needed for editing workflows.

**Independent Test**: Can be fully tested by requesting owned and non-owned tasks by ID. Delivers single task access.

**Acceptance Scenarios**:

1. **Given** user owns task, **When** task is requested by ID, **Then** complete task object is returned
2. **Given** task belongs to different user, **When** task is requested by ID, **Then** 404 Not Found is returned
3. **Given** task ID does not exist, **When** task is requested by ID, **Then** 404 Not Found is returned

---

### Edge Cases

- What happens when JWT secret changes while tokens are valid? Existing tokens become invalid; users receive 401 and must re-authenticate.
- What happens when database connection fails? Backend returns 500 Internal Server Error with generic message (no internal details exposed).
- What happens when request body is malformed JSON? Backend returns 400 Bad Request with error "Invalid request body".
- What happens when task title contains only whitespace? Backend trims whitespace and validates; if empty after trim, returns 400 "Title is required".
- What happens when concurrent requests modify same task? Last write wins; updatedAt reflects most recent modification.
- What happens when user_id in JWT doesn't exist in database? Request proceeds (no user table dependency); tasks are created with that user_id.
- What happens when Authorization header uses wrong scheme (e.g., "Basic" instead of "Bearer")? Backend returns 401 "Invalid authorization scheme".

## Requirements *(mandatory)*

### Functional Requirements

#### Application Architecture

- **FR-001**: Backend MUST expose all endpoints under `/api/*` prefix
- **FR-002**: Backend MUST be stateless - no server-side session storage
- **FR-003**: Backend MUST use dependency injection for database sessions and authentication
- **FR-004**: Backend MUST organize routes into logical router modules (auth, tasks)
- **FR-005**: Backend MUST load configuration from environment variables at startup
- **FR-006**: Backend MUST fail to start if required environment variables are missing (DATABASE_URL, BETTER_AUTH_SECRET)

#### Authentication & Authorization

- **FR-007**: Backend MUST extract JWT from Authorization header using Bearer scheme
- **FR-008**: Backend MUST verify JWT signature using BETTER_AUTH_SECRET environment variable
- **FR-009**: Backend MUST reject expired JWT tokens with 401 status
- **FR-010**: Backend MUST extract user_id from JWT claims for request context
- **FR-011**: Backend MUST return 401 for all protected endpoints when JWT is missing or invalid
- **FR-012**: Backend MUST NOT reveal whether a user_id exists when authorization fails (use 404, not 403)
- **FR-013**: Backend MUST treat JWT user_id as the sole source of truth for user identity

#### Task Operations

- **FR-014**: Backend MUST include user_id filter in ALL task queries (no cross-user access)
- **FR-015**: Backend MUST ignore any user_id provided in request body - use JWT user_id only
- **FR-016**: Backend MUST validate task title is non-empty and 200 characters or less
- **FR-017**: Backend MUST validate task description is 1000 characters or less (when provided)
- **FR-018**: Backend MUST set completed to false for newly created tasks
- **FR-019**: Backend MUST generate createdAt timestamp on task creation (server time, UTC)
- **FR-020**: Backend MUST update updatedAt timestamp on any task modification (server time, UTC)
- **FR-021**: Backend MUST return full task object after create, update, and toggle operations
- **FR-022**: Backend MUST return 404 for operations on non-existent or non-owned tasks

#### Database Interaction

- **FR-023**: Backend MUST connect to Neon PostgreSQL using DATABASE_URL environment variable
- **FR-024**: Backend MUST use SQLModel ORM for all database operations
- **FR-025**: Backend MUST include user_id index on tasks table for query performance
- **FR-026**: Backend MUST use UUID for task primary keys
- **FR-027**: Backend MUST NOT allow modification of task user_id after creation
- **FR-028**: Backend MUST handle database connection errors gracefully with 500 response

#### Error Handling

- **FR-029**: Backend MUST return consistent error response format: `{"error": "message", "code": "ERROR_CODE"}`
- **FR-030**: Backend MUST return 400 for validation errors with specific error messages
- **FR-031**: Backend MUST return 401 for authentication failures
- **FR-032**: Backend MUST return 404 for not found OR authorization failures on specific resources
- **FR-033**: Backend MUST return 500 for unexpected errors with generic message (no stack traces)
- **FR-034**: Backend MUST NOT expose internal implementation details in error messages

#### API Response Format

- **FR-035**: Backend MUST return JSON responses with Content-Type: application/json
- **FR-036**: Backend MUST return task list wrapped in `{"tasks": [...]}` format
- **FR-037**: Backend MUST return single task wrapped in `{"task": {...}}` format
- **FR-038**: Backend MUST return timestamps in ISO 8601 format (UTC)
- **FR-039**: Backend MUST return appropriate HTTP status codes (200, 201, 400, 401, 404, 500)

### Key Entities

- **Task**: Represents a user's todo item with unique identifier (UUID), title (required, 1-200 chars), description (optional, 0-1000 chars), completion status (boolean), owner reference (user_id from JWT), and server-managed timestamps (createdAt, updatedAt in UTC)
- **User Identity**: Extracted from JWT claims; represents the authenticated user making the request; used to scope all data operations

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All API endpoints respond within 500ms under normal load
- **SC-002**: 100% of task queries include user_id filter - zero cross-user data exposure
- **SC-003**: Invalid JWT tokens result in 401 response 100% of the time
- **SC-004**: All validation errors return specific, actionable error messages
- **SC-005**: Backend handles 100 concurrent requests without degradation
- **SC-006**: Database queries use indexed user_id column for all task operations
- **SC-007**: No internal implementation details (stack traces, SQL errors) exposed in error responses
- **SC-008**: All timestamps are consistently formatted in ISO 8601 UTC
- **SC-009**: Task creation ignores client-provided user_id 100% of the time
- **SC-010**: Backend starts successfully with valid environment configuration
- **SC-011**: Backend fails fast with clear error message when required environment variables are missing

### Assumptions

- Better Auth is configured on the frontend and issues valid JWT tokens signed with BETTER_AUTH_SECRET
- JWT tokens contain a user_id (or sub) claim that identifies the user
- Neon PostgreSQL database is provisioned and accessible via DATABASE_URL
- Frontend sends requests with Content-Type: application/json
- Frontend stores and sends JWT token in Authorization header as Bearer token
- Network latency between backend and database is reasonable (<100ms)
- Application runs in a production environment with HTTPS (JWT transmitted securely)
