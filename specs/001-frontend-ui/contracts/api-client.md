# API Client Contract: Frontend UI - Todo Web Application

**Date**: 2026-01-13
**Feature**: Frontend UI - Todo Web Application
**Branch**: `001-frontend-ui`

## Overview

This document defines the contract between the frontend and backend APIs from the frontend's perspective. It specifies all expected endpoints, request/response formats, status codes, and error handling requirements.

---

## Base Configuration

### API Base URL

```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '/api'
```

**Default**: `/api` (relative to frontend)
**Production**: Configured via environment variable

---

### Request Headers

All authenticated requests must include:

```typescript
{
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${token}`  // JWT token from localStorage
}
```

**Note**: The `Authorization` header is automatically added by the API client for all requests after successful authentication.

---

### Timeout

- **Default Timeout**: 30 seconds
- **Loading Indicator Delay**: 300ms (per spec FR-055)

---

## Authentication Endpoints

### Sign Up

**Endpoint**: `POST /api/auth/signup`

**Purpose**: Create new user account

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Success Response** (201 Created):
```json
{
  "message": "Account created successfully"
}
```

**Error Responses**:

400 Bad Request:
```json
{
  "error": "Invalid email format",
  "code": "INVALID_EMAIL"
}
```

409 Conflict:
```json
{
  "error": "An account with this email already exists",
  "code": "EMAIL_EXISTS"
}
```

**Frontend Behavior**:
- Success: Display success toast, redirect to `/signin`
- Error 400: Display inline validation error
- Error 409: Display "Email already exists. Please sign in."

---

### Sign In

**Endpoint**: `POST /api/auth/signin`

**Purpose**: Authenticate user and receive JWT token

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Success Response** (200 OK):
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "user@example.com"
  }
}
```

**Error Responses**:

401 Unauthorized:
```json
{
  "error": "Invalid credentials",
  "code": "INVALID_CREDENTIALS"
}
```

**Frontend Behavior**:
- Success:
  1. Store token in localStorage: `localStorage.setItem('auth_token', token)`
  2. Store user in AuthContext
  3. Redirect to `/dashboard`
- Error 401: Display "Invalid credentials" message (don't reveal which field is wrong)

---

### Sign Out

**Endpoint**: `POST /api/auth/signout` (Optional)

**Purpose**: Invalidate JWT token on backend (if backend maintains token blacklist)

**Request Headers**:
```
Authorization: Bearer ${token}
```

**Request Body**: None

**Success Response** (200 OK):
```json
{
  "message": "Signed out successfully"
}
```

**Frontend Behavior**:
- Always clear local token regardless of API response
- Always redirect to `/signin` regardless of API response
- API call is optional (can sign out client-side only)

**Implementation**:
```typescript
async function signOut() {
  try {
    await apiClient('/auth/signout', { method: 'POST' })
  } catch {
    // Ignore errors - sign out locally regardless
  } finally {
    localStorage.removeItem('auth_token')
    window.location.href = '/signin'
  }
}
```

---

## Task Endpoints

### Get All Tasks

**Endpoint**: `GET /api/tasks`

**Purpose**: Retrieve all tasks for authenticated user

**Request Headers**:
```
Authorization: Bearer ${token}
```

**Success Response** (200 OK):
```json
{
  "tasks": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "userId": "user-id-123",
      "createdAt": "2026-01-13T10:00:00Z",
      "updatedAt": "2026-01-13T10:00:00Z"
    },
    {
      "id": "223e4567-e89b-12d3-a456-426614174001",
      "title": "Finish project",
      "description": null,
      "completed": true,
      "userId": "user-id-123",
      "createdAt": "2026-01-12T15:30:00Z",
      "updatedAt": "2026-01-13T09:00:00Z"
    }
  ]
}
```

**Error Responses**:

401 Unauthorized:
```json
{
  "error": "Authentication required",
  "code": "UNAUTHORIZED"
}
```

**Frontend Behavior**:
- Success: Display tasks in task list
- Error 401: Clear token, redirect to `/signin`
- Loading: Show skeleton screens (with 300ms delay)

---

### Create Task

**Endpoint**: `POST /api/tasks`

**Purpose**: Create new task for authenticated user

**Request Headers**:
```
Authorization: Bearer ${token}
```

**Request Body**:
```json
{
  "title": "New task title",
  "description": "Optional description"
}
```

**Success Response** (201 Created):
```json
{
  "task": {
    "id": "323e4567-e89b-12d3-a456-426614174002",
    "title": "New task title",
    "description": "Optional description",
    "completed": false,
    "userId": "user-id-123",
    "createdAt": "2026-01-13T11:00:00Z",
    "updatedAt": "2026-01-13T11:00:00Z"
  }
}
```

**Error Responses**:

400 Bad Request:
```json
{
  "error": "Title is required",
  "code": "VALIDATION_ERROR"
}
```

401 Unauthorized:
```json
{
  "error": "Authentication required",
  "code": "UNAUTHORIZED"
}
```

**Frontend Behavior**:
- Success:
  1. Add task to local state immediately
  2. Display success toast
  3. Clear form and close modal
- Error 400: Display validation error in form
- Error 401: Clear token, redirect to `/signin`

---

### Update Task

**Endpoint**: `PUT /api/tasks/:id`

**Purpose**: Update task title, description, or completion status

**Request Headers**:
```
Authorization: Bearer ${token}
```

**Request Body** (all fields optional):
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "completed": true
}
```

**Success Response** (200 OK):
```json
{
  "task": {
    "id": "323e4567-e89b-12d3-a456-426614174002",
    "title": "Updated title",
    "description": "Updated description",
    "completed": true,
    "userId": "user-id-123",
    "createdAt": "2026-01-13T11:00:00Z",
    "updatedAt": "2026-01-13T12:00:00Z"
  }
}
```

**Error Responses**:

400 Bad Request:
```json
{
  "error": "Title cannot be empty",
  "code": "VALIDATION_ERROR"
}
```

401 Unauthorized:
```json
{
  "error": "Authentication required",
  "code": "UNAUTHORIZED"
}
```

404 Not Found:
```json
{
  "error": "Task not found",
  "code": "NOT_FOUND"
}
```

**Frontend Behavior**:
- Success: Update task in local state, display success toast
- Error 400: Display validation error in form
- Error 401: Clear token, redirect to `/signin`
- Error 404: Display "Task not found" error, remove from local state

---

### Toggle Task Completion

**Endpoint**: `PATCH /api/tasks/:id/toggle`

**Purpose**: Toggle task completion status (optimized endpoint for checkbox interaction)

**Request Headers**:
```
Authorization: Bearer ${token}
```

**Request Body**: None (backend toggles current state)

**Success Response** (200 OK):
```json
{
  "task": {
    "id": "323e4567-e89b-12d3-a456-426614174002",
    "title": "Task title",
    "description": "Description",
    "completed": true,  // Toggled from false to true
    "userId": "user-id-123",
    "createdAt": "2026-01-13T11:00:00Z",
    "updatedAt": "2026-01-13T13:00:00Z"
  }
}
```

**Error Responses**:

401 Unauthorized:
```json
{
  "error": "Authentication required",
  "code": "UNAUTHORIZED"
}
```

404 Not Found:
```json
{
  "error": "Task not found",
  "code": "NOT_FOUND"
}
```

**Frontend Behavior** (Optimistic UI):
1. **Immediately** toggle task in local state (don't wait for API)
2. Show subtle loading indicator on checkbox
3. Make API call in background
4. On success: Keep optimistic state, hide loading indicator
5. On error:
   - Revert toggle in local state
   - Display error toast: "Failed to update task"
   - Hide loading indicator

**Debouncing**: Rapid clicks should be debounced (500ms) to prevent multiple API calls

---

### Delete Task

**Endpoint**: `DELETE /api/tasks/:id`

**Purpose**: Permanently delete task

**Request Headers**:
```
Authorization: Bearer ${token}
```

**Request Body**: None

**Success Response** (200 OK):
```json
{
  "message": "Task deleted successfully"
}
```

**Error Responses**:

401 Unauthorized:
```json
{
  "error": "Authentication required",
  "code": "UNAUTHORIZED"
}
```

404 Not Found:
```json
{
  "error": "Task not found",
  "code": "NOT_FOUND"
}
```

**Frontend Behavior**:
- User confirms deletion in modal
- On confirmation:
  1. Remove task from local state immediately
  2. Make API call in background
  3. On success: Display success toast
  4. On error: Re-add task to local state, display error toast

---

## Error Handling

### HTTP Status Code Mapping

| Status Code | Meaning | Frontend Action |
|-------------|---------|-----------------|
| **200 OK** | Success | Process response data |
| **201 Created** | Resource created | Process response data, show success feedback |
| **400 Bad Request** | Validation error | Display error message to user |
| **401 Unauthorized** | Authentication failed or token expired | Clear token, redirect to `/signin` |
| **403 Forbidden** | User lacks permission | Display "Access denied" message |
| **404 Not Found** | Resource doesn't exist | Display "Not found" error, remove from local state if applicable |
| **500 Internal Server Error** | Server error | Display "Something went wrong. Please try again." with retry option |
| **Network Error** | Request failed (no response) | Display "Connection failed. Please check your internet." with retry option |

---

### Error Response Format

All error responses follow this structure:

```typescript
interface ErrorResponse {
  error: string      // Human-readable error message
  code?: string      // Optional error code for programmatic handling
  details?: any      // Optional additional error context
}
```

---

### Automatic Error Handling

The API client wrapper automatically handles:

1. **401 Unauthorized**: Clears token and redirects to `/signin`
2. **Network Errors**: Catches and transforms to user-friendly message
3. **Timeout**: Shows timeout message after 30 seconds

**Implementation**:
```typescript
async function apiClient<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const token = localStorage.getItem('auth_token')

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options?.headers,
      },
      signal: AbortSignal.timeout(30000), // 30 second timeout
    })

    // Handle 401: Clear token and redirect
    if (response.status === 401) {
      localStorage.removeItem('auth_token')
      window.location.href = '/signin'
      throw new Error('Session expired. Please sign in again.')
    }

    // Handle other errors
    if (!response.ok) {
      const error: ErrorResponse = await response.json()
      throw new Error(error.error || 'Request failed')
    }

    return await response.json()
  } catch (error) {
    // Network error or timeout
    if (error instanceof TypeError) {
      throw new Error('Connection failed. Please check your internet connection.')
    }
    throw error
  }
}
```

---

## Request Examples

### Authentication Flow Example

```typescript
// Sign up
const signUp = async (email: string, password: string) => {
  try {
    const response = await apiClient<AuthSignUpResponse>('/auth/signup', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    })
    toast.success(response.message)
    router.push('/signin')
  } catch (error) {
    toast.error(error.message)
  }
}

// Sign in
const signIn = async (email: string, password: string) => {
  try {
    const response = await apiClient<AuthSignInResponse>('/auth/signin', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    })
    localStorage.setItem('auth_token', response.token)
    setUser(response.user)
    router.push('/dashboard')
  } catch (error) {
    toast.error(error.message)
  }
}
```

---

### Task Operations Example

```typescript
// Get tasks
const getTasks = async (): Promise<Task[]> => {
  const response = await apiClient<TaskListResponse>('/tasks')
  return response.tasks
}

// Create task
const createTask = async (data: TaskFormData): Promise<Task> => {
  const response = await apiClient<TaskCreateResponse>('/tasks', {
    method: 'POST',
    body: JSON.stringify(data),
  })
  return response.task
}

// Toggle task (with optimistic UI)
const toggleTask = async (taskId: string) => {
  // Optimistic update
  setTasks(prev => prev.map(t =>
    t.id === taskId ? { ...t, completed: !t.completed } : t
  ))

  try {
    const response = await apiClient<TaskToggleResponse>(`/tasks/${taskId}/toggle`, {
      method: 'PATCH',
    })
    // Success: optimistic update was correct
  } catch (error) {
    // Error: revert optimistic update
    setTasks(prev => prev.map(t =>
      t.id === taskId ? { ...t, completed: !t.completed } : t
    ))
    toast.error('Failed to update task')
  }
}
```

---

## Performance Considerations

### Loading Indicator Delay

Per spec requirement FR-055, loading indicators should not appear immediately to avoid flashing on fast connections:

```typescript
const [showLoading, setShowLoading] = useState(false)

useEffect(() => {
  const timer = setTimeout(() => setShowLoading(true), 300) // 300ms delay

  fetchData().finally(() => {
    clearTimeout(timer)
    setShowLoading(false)
  })

  return () => clearTimeout(timer)
}, [])
```

---

### Request Debouncing

For rapid user interactions (e.g., task toggle checkbox), debounce requests:

```typescript
const debouncedToggle = debounce(async (taskId: string) => {
  await apiClient(`/tasks/${taskId}/toggle`, { method: 'PATCH' })
}, 500) // 500ms debounce
```

---

## Testing Strategy

### Mock API Responses

During frontend development, mock the API responses:

```typescript
// lib/api/mock.ts
export const mockApiClient = async <T>(endpoint: string): Promise<T> => {
  await new Promise(resolve => setTimeout(resolve, 500)) // Simulate network delay

  if (endpoint === '/tasks') {
    return { tasks: mockTasks } as T
  }
  if (endpoint.includes('/tasks/') && endpoint.includes('/toggle')) {
    return { task: mockToggledTask } as T
  }
  // ... more mock responses
}
```

---

## Summary

**Authentication Endpoints**: 3 (signup, signin, signout)
**Task Endpoints**: 5 (list, create, update, toggle, delete)
**Error Status Codes**: 6 (400, 401, 403, 404, 500, network)

**Key Design Decisions**:
1. Automatic 401 handling with redirect to signin
2. Optimistic UI for task toggle with error reversion
3. 300ms loading indicator delay to prevent flashing
4. 30-second timeout for all requests
5. Consistent error response format
6. JWT in Authorization header (Bearer token)
7. Debouncing for rapid user interactions

**Next Step**: Document authentication flow and component prop contracts
