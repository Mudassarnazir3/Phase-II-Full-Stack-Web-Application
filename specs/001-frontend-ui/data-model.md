# Data Model: Frontend UI - Todo Web Application

**Date**: 2026-01-13
**Feature**: Frontend UI - Todo Web Application
**Branch**: `001-frontend-ui`

## Overview

This document defines all TypeScript interfaces, types, and data structures used in the frontend application. These models represent the frontend's perspective of the data and may differ from backend database schemas.

---

## Core Data Types

### User

Represents an authenticated user account (frontend perspective).

```typescript
interface User {
  id: string              // Unique user identifier (UUID from backend)
  email: string           // User email address
  // Note: Password never stored or transmitted to frontend
}
```

**Constraints**:
- `id`: Non-empty string, UUID format
- `email`: Valid email format (RFC 5322)

**Usage**: Stored in authentication context after successful signin

---

### Task

Represents a single todo item belonging to a user.

```typescript
interface Task {
  id: string              // Unique task identifier (UUID from backend)
  title: string           // Task title (required)
  description?: string    // Task description (optional)
  completed: boolean      // Completion status
  userId: string          // Owner reference (user who created this task)
  createdAt: string       // ISO 8601 timestamp
  updatedAt: string       // ISO 8601 timestamp
}
```

**Constraints**:
- `id`: Non-empty string, UUID format
- `title`: 1-200 characters, trimmed, required
- `description`: 0-1000 characters, optional
- `completed`: Boolean (true/false)
- `userId`: Non-empty string, UUID format
- `createdAt`: ISO 8601 format (e.g., "2026-01-13T10:30:00Z")
- `updatedAt`: ISO 8601 format

**Usage**: Displayed in task list, forms, and detail views

---

## State Management Types

### AuthState

Represents the current authentication state of the application.

```typescript
interface AuthState {
  isAuthenticated: boolean    // Whether user is currently authenticated
  user: User | null           // Current user (null if not authenticated)
  token: string | null        // JWT token (null if not authenticated)
  loading: boolean            // Auth operation in progress
  error: string | null        // Error message from last auth operation
}
```

**State Transitions**:
1. Initial: `{ isAuthenticated: false, user: null, token: null, loading: false, error: null }`
2. Signing in: `{ isAuthenticated: false, user: null, token: null, loading: true, error: null }`
3. Authenticated: `{ isAuthenticated: true, user: {...}, token: "jwt...", loading: false, error: null }`
4. Auth error: `{ isAuthenticated: false, user: null, token: null, loading: false, error: "Invalid credentials" }`
5. Sign out: Return to initial state

**Usage**: Managed by `AuthContext` and accessed via `useAuth` hook

---

### TaskState

Represents the state of the task list and task operations.

```typescript
interface TaskState {
  tasks: Task[]             // Array of tasks for current user
  loading: boolean          // Task operation in progress
  error: string | null      // Error message from last task operation
}
```

**State Transitions**:
1. Initial: `{ tasks: [], loading: false, error: null }`
2. Loading tasks: `{ tasks: [], loading: true, error: null }`
3. Tasks loaded: `{ tasks: [...], loading: false, error: null }`
4. Task error: `{ tasks: [...], loading: false, error: "Failed to load tasks" }`

**Usage**: Managed by `useTasks` hook in dashboard

---

## Form Data Types

### SignUpFormData

Data structure for user registration form.

```typescript
interface SignUpFormData {
  email: string
  password: string
  confirmPassword?: string    // Optional: Frontend-only field for UX
}
```

**Validation Rules**:
- `email`: Must match RFC 5322 email regex
- `password`: Minimum 8 characters, at least one uppercase, one lowercase, one number
- `confirmPassword`: Must match password (if used)

---

### SignInFormData

Data structure for user authentication form.

```typescript
interface SignInFormData {
  email: string
  password: string
}
```

**Validation Rules**:
- `email`: Must match RFC 5322 email regex
- `password`: Non-empty (strength not validated on signin)

---

### TaskFormData

Data structure for task creation/editing forms.

```typescript
interface TaskFormData {
  title: string
  description?: string
}
```

**Validation Rules**:
- `title`: Required, 1-200 characters, trimmed
- `description`: Optional, 0-1000 characters

---

## API Request/Response Types

### AuthSignUpRequest

```typescript
interface AuthSignUpRequest {
  email: string
  password: string
}
```

### AuthSignUpResponse

```typescript
interface AuthSignUpResponse {
  message: string    // Success message (e.g., "Account created successfully")
}
```

---

### AuthSignInRequest

```typescript
interface AuthSignInRequest {
  email: string
  password: string
}
```

### AuthSignInResponse

```typescript
interface AuthSignInResponse {
  token: string      // JWT token
  user: User         // User object
}
```

---

### TaskListResponse

```typescript
interface TaskListResponse {
  tasks: Task[]      // Array of tasks for authenticated user
}
```

---

### TaskCreateRequest

```typescript
interface TaskCreateRequest {
  title: string
  description?: string
}
```

### TaskCreateResponse

```typescript
interface TaskCreateResponse {
  task: Task         // Newly created task with ID and timestamps
}
```

---

### TaskUpdateRequest

```typescript
interface TaskUpdateRequest {
  title?: string
  description?: string
  completed?: boolean
}
```

### TaskUpdateResponse

```typescript
interface TaskUpdateResponse {
  task: Task         // Updated task
}
```

---

### TaskToggleResponse

```typescript
interface TaskToggleResponse {
  task: Task         // Task with toggled completed status
}
```

---

### TaskDeleteResponse

```typescript
interface TaskDeleteResponse {
  message: string    // Success message (e.g., "Task deleted successfully")
}
```

---

### ErrorResponse

```typescript
interface ErrorResponse {
  error: string      // Human-readable error message
  code?: string      // Optional error code (e.g., "INVALID_EMAIL", "UNAUTHORIZED")
  details?: any      // Optional additional error details
}
```

**Common Error Codes**:
- `INVALID_EMAIL`: Email format validation failed
- `WEAK_PASSWORD`: Password strength requirements not met
- `EMAIL_EXISTS`: Email already registered
- `INVALID_CREDENTIALS`: Email or password incorrect
- `UNAUTHORIZED`: JWT token missing or invalid
- `FORBIDDEN`: User lacks permission for this operation
- `NOT_FOUND`: Requested resource not found
- `NETWORK_ERROR`: Request failed due to network issue

---

## UI State Types

### ToastType

```typescript
type ToastType = 'success' | 'error' | 'info' | 'warning'
```

### ToastMessage

```typescript
interface ToastMessage {
  id: string
  type: ToastType
  message: string
  duration?: number    // Auto-dismiss duration in ms (default: 5000)
}
```

---

### Modal State

```typescript
interface ModalState {
  isOpen: boolean
  mode: 'create' | 'edit' | 'delete' | null
  task?: Task          // Task being edited/deleted (null for create)
}
```

---

## Validation Functions

### Email Validation

```typescript
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

function validateEmail(email: string): boolean {
  return EMAIL_REGEX.test(email)
}
```

---

### Password Validation

```typescript
const PASSWORD_MIN_LENGTH = 8
const PASSWORD_REGEX = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/

interface PasswordValidationResult {
  isValid: boolean
  errors: string[]
}

function validatePassword(password: string): PasswordValidationResult {
  const errors: string[] = []

  if (password.length < PASSWORD_MIN_LENGTH) {
    errors.push(`Password must be at least ${PASSWORD_MIN_LENGTH} characters`)
  }
  if (!/[a-z]/.test(password)) {
    errors.push('Password must contain at least one lowercase letter')
  }
  if (!/[A-Z]/.test(password)) {
    errors.push('Password must contain at least one uppercase letter')
  }
  if (!/\d/.test(password)) {
    errors.push('Password must contain at least one number')
  }

  return {
    isValid: errors.length === 0,
    errors
  }
}
```

---

### Task Title Validation

```typescript
const TITLE_MIN_LENGTH = 1
const TITLE_MAX_LENGTH = 200

function validateTaskTitle(title: string): string | null {
  const trimmed = title.trim()

  if (trimmed.length < TITLE_MIN_LENGTH) {
    return 'Title is required'
  }
  if (trimmed.length > TITLE_MAX_LENGTH) {
    return `Title must be ${TITLE_MAX_LENGTH} characters or less`
  }

  return null // No error
}
```

---

### Task Description Validation

```typescript
const DESCRIPTION_MAX_LENGTH = 1000

function validateTaskDescription(description?: string): string | null {
  if (!description) return null // Optional field

  if (description.length > DESCRIPTION_MAX_LENGTH) {
    return `Description must be ${DESCRIPTION_MAX_LENGTH} characters or less`
  }

  return null // No error
}
```

---

## Utility Types

### ApiResponse Wrapper

```typescript
type ApiResponse<T> = {
  data?: T
  error?: ErrorResponse
}
```

**Usage**: Wrap API responses for consistent error handling

---

### Loading State Wrapper

```typescript
type LoadingState<T> = {
  data: T | null
  loading: boolean
  error: string | null
}
```

**Usage**: Wrap component state for consistent loading patterns

---

## State Persistence

### LocalStorage Keys

```typescript
const STORAGE_KEYS = {
  AUTH_TOKEN: 'auth_token',
  // Future: Add more keys if needed (e.g., theme preference)
} as const
```

### Token Storage

```typescript
// Store JWT token
function setAuthToken(token: string): void {
  localStorage.setItem(STORAGE_KEYS.AUTH_TOKEN, token)
}

// Retrieve JWT token
function getAuthToken(): string | null {
  return localStorage.getItem(STORAGE_KEYS.AUTH_TOKEN)
}

// Clear JWT token
function clearAuthToken(): void {
  localStorage.removeItem(STORAGE_KEYS.AUTH_TOKEN)
}
```

---

## Type Export Organization

All types should be exported from dedicated type files:

```typescript
// types/auth.ts
export type { User, AuthState, SignUpFormData, SignInFormData }
export type { AuthSignUpRequest, AuthSignUpResponse }
export type { AuthSignInRequest, AuthSignInResponse }

// types/task.ts
export type { Task, TaskState, TaskFormData }
export type { TaskListResponse, TaskCreateRequest, TaskCreateResponse }
export type { TaskUpdateRequest, TaskUpdateResponse }
export type { TaskToggleResponse, TaskDeleteResponse }

// types/api.ts
export type { ErrorResponse, ApiResponse, LoadingState }

// types/ui.ts
export type { ToastType, ToastMessage, ModalState }
```

---

## Data Flow Diagram

```
┌──────────────┐
│ User Actions │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ React Components │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐      ┌─────────────┐
│ Custom Hooks     │◄─────┤ Auth Context│
│ (useAuth,        │      └─────────────┘
│  useTasks)       │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐      ┌─────────────┐
│ API Client       │◄─────┤ localStorage│
│ (fetch wrapper)  │      └─────────────┘
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Backend API      │
│ (FastAPI)        │
└──────────────────┘
```

---

## Summary

**Total Interfaces**: 20+
**Validation Functions**: 3 (email, password, task fields)
**Storage Keys**: 1 (auth_token)

**Key Design Decisions**:
1. Strict TypeScript types for all data structures
2. Separate interfaces for requests, responses, and internal state
3. Validation functions with clear error messages
4. Consistent error response format
5. Type-safe localStorage access

**Next Step**: Generate API client contracts and component prop interfaces
