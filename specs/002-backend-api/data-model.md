# Data Model: Backend API - Todo Web Application

**Feature Branch**: `002-backend-api`
**Created**: 2026-01-16
**Spec Reference**: [spec.md](./spec.md)

## Overview

This document defines the database schema and data models for the backend API. All models use SQLModel for ORM mapping to Neon PostgreSQL.

---

## Entity: Task

Represents a single todo item owned by a user.

### Schema Definition

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, NOT NULL | Unique task identifier (generated server-side) |
| `title` | VARCHAR(200) | NOT NULL | Task title (1-200 chars after trim) |
| `description` | VARCHAR(1000) | NULLABLE | Optional task description (0-1000 chars) |
| `completed` | BOOLEAN | NOT NULL, DEFAULT FALSE | Task completion status |
| `user_id` | VARCHAR(255) | NOT NULL, INDEXED | Owner reference from JWT claims |
| `created_at` | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Creation timestamp (UTC) |
| `updated_at` | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last modification timestamp (UTC) |

### Indexes

| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| `pk_tasks` | `id` | PRIMARY KEY | Unique task lookup |
| `idx_tasks_user_id` | `user_id` | B-TREE | User-scoped queries (FR-025) |

### Constraints

1. **Title Required**: `title` cannot be NULL or empty string
2. **Title Length**: `title` must be 200 characters or less
3. **Description Length**: `description` must be 1000 characters or less (when provided)
4. **User Ownership Immutable**: `user_id` cannot be modified after creation (FR-027)
5. **Completed Default**: New tasks default to `completed = false` (FR-018)

---

## Entity Relationships

```
┌─────────────────────────────────────────────────┐
│                    Task                          │
├─────────────────────────────────────────────────┤
│ id: UUID [PK]                                    │
│ title: VARCHAR(200) [NOT NULL]                   │
│ description: VARCHAR(1000) [NULLABLE]            │
│ completed: BOOLEAN [DEFAULT FALSE]               │
│ user_id: VARCHAR(255) [NOT NULL, INDEXED]        │
│ created_at: TIMESTAMPTZ [NOT NULL]               │
│ updated_at: TIMESTAMPTZ [NOT NULL]               │
└─────────────────────────────────────────────────┘
        │
        │ user_id references JWT claim (no FK)
        ▼
┌─────────────────────────────────────────────────┐
│              User Identity (JWT)                 │
├─────────────────────────────────────────────────┤
│ Extracted from JWT 'sub' or 'user_id' claim      │
│ NOT stored in database                           │
│ Used for query filtering only                    │
└─────────────────────────────────────────────────┘
```

**Note**: There is no `users` table in the backend. User identity comes exclusively from JWT claims. This is intentional - Better Auth manages user accounts on the frontend.

---

## Data Validation Rules

### On Task Creation

| Field | Validation | Error Message |
|-------|------------|---------------|
| `title` | Required, non-empty after trim | "Title is required" |
| `title` | Max 200 characters | "Title must be 200 characters or less" |
| `description` | Max 1000 characters (if provided) | "Description must be 1000 characters or less" |
| `user_id` | Ignored from request body | N/A (silently overwritten with JWT user_id) |
| `completed` | Ignored from request body | N/A (defaults to false) |
| `id` | Ignored from request body | N/A (generated server-side) |
| `created_at` | Ignored from request body | N/A (generated server-side) |
| `updated_at` | Ignored from request body | N/A (generated server-side) |

### On Task Update

| Field | Validation | Error Message |
|-------|------------|---------------|
| `title` | Non-empty after trim (if provided) | "Title cannot be empty" |
| `title` | Max 200 characters (if provided) | "Title must be 200 characters or less" |
| `description` | Max 1000 characters (if provided) | "Description must be 1000 characters or less" |
| `user_id` | Immutable - ignored | N/A (silently ignored) |
| `id` | Immutable - ignored | N/A (silently ignored) |
| `created_at` | Immutable - ignored | N/A (silently ignored) |

---

## State Transitions

### Task Completion States

```
┌──────────────┐      Toggle      ┌──────────────┐
│  incomplete  │ ◄──────────────► │   complete   │
│ completed=F  │                  │ completed=T  │
└──────────────┘                  └──────────────┘
```

**Transition Rules**:
- Toggle flips `completed` boolean
- Toggle updates `updated_at` timestamp
- No other fields affected by toggle

### Task Lifecycle

```
[Created]                    [Updated]                   [Deleted]
    │                            │                           │
    ▼                            ▼                           ▼
┌─────────┐    Update      ┌─────────┐    Delete      ╔═════════╗
│ Active  │ ──────────────►│ Active  │ ──────────────►║ Removed ║
│  Task   │                │  Task   │                ║ (gone)  ║
└─────────┘                └─────────┘                ╚═════════╝
    │                            │
    │          Toggle            │
    └────────────────────────────┘
         (stays Active)
```

---

## Query Patterns

### Required Filters

**ALL task queries MUST include `user_id` filter** (FR-014, Constitution V):

```sql
-- List tasks
SELECT * FROM tasks WHERE user_id = :jwt_user_id;

-- Get single task
SELECT * FROM tasks WHERE id = :task_id AND user_id = :jwt_user_id;

-- Update task
UPDATE tasks SET ... WHERE id = :task_id AND user_id = :jwt_user_id;

-- Delete task
DELETE FROM tasks WHERE id = :task_id AND user_id = :jwt_user_id;
```

### Index Usage Verification

The `idx_tasks_user_id` index should be used for:
- Listing all user tasks
- Verifying task ownership before operations

Query plans should show index scan, not sequential scan.

---

## API Response Serialization

### Task Object (JSON)

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "userId": "user-abc-123",
  "createdAt": "2026-01-16T10:30:00Z",
  "updatedAt": "2026-01-16T10:30:00Z"
}
```

### Field Mapping (Database → API)

| Database Column | API Field | Notes |
|-----------------|-----------|-------|
| `id` | `id` | UUID as string |
| `title` | `title` | String |
| `description` | `description` | String or null |
| `completed` | `completed` | Boolean |
| `user_id` | `userId` | camelCase for frontend |
| `created_at` | `createdAt` | ISO 8601 UTC string |
| `updated_at` | `updatedAt` | ISO 8601 UTC string |

---

## Migration Notes

### Initial Schema (DDL)

```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(200) NOT NULL,
    description VARCHAR(1000),
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
```

### Notes
- Use PostgreSQL's `gen_random_uuid()` for default UUID generation
- `TIMESTAMPTZ` stores timezone-aware timestamps
- Index on `user_id` is REQUIRED per constitution
