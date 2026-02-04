# API Endpoints Contract: Backend API - Todo Web Application

**Feature Branch**: `002-backend-api`
**Created**: 2026-01-16
**Spec Reference**: [spec.md](../spec.md)

## Overview

This document defines the REST API endpoints the backend must implement. All endpoints are under the `/api` prefix per FR-001.

---

## Authentication

All endpoints except health check require JWT authentication.

### Request Header

```
Authorization: Bearer <jwt_token>
```

### Authentication Failures

| Scenario | Status | Response |
|----------|--------|----------|
| Missing header | 401 | `{"error": "Authentication required", "code": "UNAUTHORIZED"}` |
| Invalid token | 401 | `{"error": "Invalid token", "code": "UNAUTHORIZED"}` |
| Expired token | 401 | `{"error": "Token expired", "code": "TOKEN_EXPIRED"}` |
| Wrong scheme | 401 | `{"error": "Invalid authorization scheme", "code": "UNAUTHORIZED"}` |

---

## Task Endpoints

### GET /api/tasks

**Purpose**: List all tasks for authenticated user

**Authentication**: Required

**Request**: No body

**Success Response** (200 OK):
```json
{
  "tasks": [
    {
      "id": "uuid",
      "title": "string",
      "description": "string|null",
      "completed": false,
      "userId": "string",
      "createdAt": "ISO8601",
      "updatedAt": "ISO8601"
    }
  ]
}
```

**Behavior**:
- Returns only tasks where `user_id` matches JWT user
- Returns empty array `[]` if no tasks (not null, not error)
- Orders by `created_at` descending (newest first)

---

### POST /api/tasks

**Purpose**: Create new task for authenticated user

**Authentication**: Required

**Request Body**:
```json
{
  "title": "string (required, 1-200 chars)",
  "description": "string (optional, 0-1000 chars)"
}
```

**Success Response** (201 Created):
```json
{
  "task": {
    "id": "uuid (generated)",
    "title": "string",
    "description": "string|null",
    "completed": false,
    "userId": "string (from JWT)",
    "createdAt": "ISO8601 (generated)",
    "updatedAt": "ISO8601 (generated)"
  }
}
```

**Error Responses**:

| Condition | Status | Response |
|-----------|--------|----------|
| Missing title | 400 | `{"error": "Title is required", "code": "VALIDATION_ERROR"}` |
| Title > 200 chars | 400 | `{"error": "Title must be 200 characters or less", "code": "VALIDATION_ERROR"}` |
| Description > 1000 chars | 400 | `{"error": "Description must be 1000 characters or less", "code": "VALIDATION_ERROR"}` |
| Malformed JSON | 400 | `{"error": "Invalid request body", "code": "INVALID_REQUEST"}` |

**Behavior**:
- Ignores any `user_id`, `id`, `completed`, `createdAt`, `updatedAt` in request body
- Sets `user_id` from JWT claims
- Sets `completed` to `false`
- Generates UUID for `id`
- Sets `createdAt` and `updatedAt` to current UTC time

---

### GET /api/tasks/:id

**Purpose**: Get single task by ID

**Authentication**: Required

**Request**: No body

**Success Response** (200 OK):
```json
{
  "task": {
    "id": "uuid",
    "title": "string",
    "description": "string|null",
    "completed": false,
    "userId": "string",
    "createdAt": "ISO8601",
    "updatedAt": "ISO8601"
  }
}
```

**Error Responses**:

| Condition | Status | Response |
|-----------|--------|----------|
| Task not found | 404 | `{"error": "Task not found", "code": "NOT_FOUND"}` |
| Task belongs to other user | 404 | `{"error": "Task not found", "code": "NOT_FOUND"}` |
| Invalid UUID format | 404 | `{"error": "Task not found", "code": "NOT_FOUND"}` |

**Behavior**:
- Query includes `user_id` filter (ownership check)
- Returns 404 for both "not found" and "not owned" (prevents enumeration)

---

### PUT /api/tasks/:id

**Purpose**: Update task title and/or description

**Authentication**: Required

**Request Body** (all fields optional):
```json
{
  "title": "string (1-200 chars if provided)",
  "description": "string (0-1000 chars if provided)",
  "completed": "boolean (if provided)"
}
```

**Success Response** (200 OK):
```json
{
  "task": {
    "id": "uuid",
    "title": "string",
    "description": "string|null",
    "completed": false,
    "userId": "string",
    "createdAt": "ISO8601",
    "updatedAt": "ISO8601 (updated)"
  }
}
```

**Error Responses**:

| Condition | Status | Response |
|-----------|--------|----------|
| Task not found/not owned | 404 | `{"error": "Task not found", "code": "NOT_FOUND"}` |
| Empty title | 400 | `{"error": "Title cannot be empty", "code": "VALIDATION_ERROR"}` |
| Title > 200 chars | 400 | `{"error": "Title must be 200 characters or less", "code": "VALIDATION_ERROR"}` |
| Description > 1000 chars | 400 | `{"error": "Description must be 1000 characters or less", "code": "VALIDATION_ERROR"}` |

**Behavior**:
- Query includes `user_id` filter (ownership check)
- Only updates provided fields (partial update supported)
- Ignores `user_id`, `id`, `createdAt` in request body
- Updates `updatedAt` to current UTC time

---

### PATCH /api/tasks/:id/toggle

**Purpose**: Toggle task completion status

**Authentication**: Required

**Request Body**: None required

**Success Response** (200 OK):
```json
{
  "task": {
    "id": "uuid",
    "title": "string",
    "description": "string|null",
    "completed": true,
    "userId": "string",
    "createdAt": "ISO8601",
    "updatedAt": "ISO8601 (updated)"
  }
}
```

**Error Responses**:

| Condition | Status | Response |
|-----------|--------|----------|
| Task not found/not owned | 404 | `{"error": "Task not found", "code": "NOT_FOUND"}` |

**Behavior**:
- Query includes `user_id` filter (ownership check)
- Flips `completed` from `true` to `false` or vice versa
- Updates `updatedAt` to current UTC time
- Returns full updated task object

---

### DELETE /api/tasks/:id

**Purpose**: Permanently delete task

**Authentication**: Required

**Request Body**: None

**Success Response** (200 OK):
```json
{
  "message": "Task deleted successfully"
}
```

**Error Responses**:

| Condition | Status | Response |
|-----------|--------|----------|
| Task not found/not owned | 404 | `{"error": "Task not found", "code": "NOT_FOUND"}` |

**Behavior**:
- Query includes `user_id` filter (ownership check)
- Permanently removes task from database
- Returns success message (not the deleted task)

---

## Health Check Endpoint

### GET /api/health

**Purpose**: Health check for monitoring

**Authentication**: NOT required

**Request**: No body

**Success Response** (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "ISO8601"
}
```

**Behavior**:
- Returns 200 if application is running
- Does not verify database connection (fast response)

---

## Response Format Summary

### Success Responses

| Operation | Status | Wrapper |
|-----------|--------|---------|
| List tasks | 200 | `{"tasks": [...]}` |
| Get task | 200 | `{"task": {...}}` |
| Create task | 201 | `{"task": {...}}` |
| Update task | 200 | `{"task": {...}}` |
| Toggle task | 200 | `{"task": {...}}` |
| Delete task | 200 | `{"message": "..."}` |
| Health check | 200 | `{"status": "...", "timestamp": "..."}` |

### Error Response Format

All errors follow this structure:
```json
{
  "error": "Human-readable message",
  "code": "MACHINE_READABLE_CODE"
}
```

---

## CORS Headers

Backend must include CORS headers for frontend compatibility:

```
Access-Control-Allow-Origin: <frontend_url>
Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS
Access-Control-Allow-Headers: Authorization, Content-Type
Access-Control-Allow-Credentials: true
```
