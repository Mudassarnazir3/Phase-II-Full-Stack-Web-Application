# Component Props Contract: Frontend UI - Todo Web Application

**Date**: 2026-01-13
**Feature**: Frontend UI - Todo Web Application
**Branch**: `001-frontend-ui`

## Overview

This document defines TypeScript prop interfaces for all major UI components. These contracts ensure type safety and consistent component APIs across the application.

---

## Base UI Components

### Button

```typescript
interface ButtonProps {
  children: React.ReactNode
  onClick?: () => void
  type?: 'button' | 'submit' | 'reset'
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  loading?: boolean
  className?: string
}
```

**Usage**:
```tsx
<Button variant="primary" onClick={handleSubmit} loading={isSubmitting}>
  Save Task
</Button>
```

---

### Input

```typescript
interface InputProps {
  id: string
  name: string
  type?: 'text' | 'email' | 'password'
  value: string
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void
  placeholder?: string
  label?: string
  error?: string
  required?: boolean
  disabled?: boolean
  maxLength?: number
  className?: string
}
```

**Usage**:
```tsx
<Input
  id="email"
  name="email"
  type="email"
  label="Email Address"
  value={email}
  onChange={(e) => setEmail(e.target.value)}
  error={errors.email}
  required
/>
```

---

### Textarea

```typescript
interface TextareaProps {
  id: string
  name: string
  value: string
  onChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void
  placeholder?: string
  label?: string
  error?: string
  required?: boolean
  disabled?: boolean
  rows?: number
  maxLength?: number
  className?: string
}
```

---

### Modal

```typescript
interface ModalProps {
  isOpen: boolean
  onClose: () => void
  title: string
  children: React.ReactNode
  size?: 'sm' | 'md' | 'lg'
  showCloseButton?: boolean
}
```

**Usage**:
```tsx
<Modal isOpen={isOpen} onClose={handleClose} title="Create Task">
  <TaskForm mode="create" onSubmit={handleCreate} onCancel={handleClose} />
</Modal>
```

---

### LoadingSpinner

```typescript
interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg'
  className?: string
}
```

---

## Authentication Components

### SignUpForm

```typescript
interface SignUpFormProps {
  onSubmit: (email: string, password: string) => Promise<void>
  loading?: boolean
  error?: string
}
```

**Behavior**:
- Validates email format and password strength
- Displays inline validation errors
- Shows loading spinner in submit button during API call
- Displays API error message above form

**Usage**:
```tsx
<SignUpForm
  onSubmit={async (email, password) => {
    await signUp(email, password)
  }}
  loading={isLoading}
  error={errorMessage}
/>
```

---

### SignInForm

```typescript
interface SignInFormProps {
  onSubmit: (email: string, password: string) => Promise<void>
  loading?: boolean
  error?: string
}
```

**Behavior**:
- Validates email format
- Displays inline validation errors
- Shows loading spinner in submit button during API call
- Displays "Invalid credentials" error message above form

---

### AuthGuard

```typescript
interface AuthGuardProps {
  children: React.ReactNode
  fallback?: React.ReactNode
}
```

**Behavior**:
- Checks authentication status from AuthContext
- Shows fallback (or loading spinner) while checking auth
- Redirects to /signin if not authenticated
- Renders children if authenticated

**Usage**:
```tsx
<AuthGuard fallback={<LoadingSpinner />}>
  <Dashboard />
</AuthGuard>
```

---

## Task Components

### TaskCard

```typescript
interface TaskCardProps {
  task: Task
  onToggle: (taskId: string) => void
  onEdit: (task: Task) => void
  onDelete: (taskId: string) => void
  isLoading?: boolean
}
```

**Behavior**:
- Displays task title, description, completion status
- Shows strikethrough and muted color for completed tasks
- Checkbox triggers onToggle
- Edit button triggers onEdit
- Delete button triggers onDelete
- Shows subtle loading indicator when isLoading is true

**Visual States**:
- Default: White background, black text
- Completed: Gray background, gray text with strikethrough
- Loading: Opacity reduced, loading indicator on checkbox

**Usage**:
```tsx
<TaskCard
  task={task}
  onToggle={handleToggle}
  onEdit={handleEdit}
  onDelete={handleDelete}
  isLoading={isToggling}
/>
```

---

### TaskList

```typescript
interface TaskListProps {
  tasks: Task[]
  onToggle: (taskId: string) => void
  onEdit: (task: Task) => void
  onDelete: (taskId: string) => void
  loading?: boolean
}
```

**Behavior**:
- Renders list of TaskCard components
- Shows TaskListSkeleton when loading
- Shows TaskEmpty when tasks array is empty
- Displays task count summary at top

**Usage**:
```tsx
<TaskList
  tasks={tasks}
  onToggle={handleToggle}
  onEdit={handleEdit}
  onDelete={handleDelete}
  loading={isLoadingTasks}
/>
```

---

### TaskForm

```typescript
interface TaskFormProps {
  mode: 'create' | 'edit'
  initialValues?: Partial<Task>
  onSubmit: (data: { title: string; description?: string }) => Promise<void>
  onCancel: () => void
  isSubmitting?: boolean
}
```

**Behavior**:
- Mode 'create': Empty form
- Mode 'edit': Pre-populated with initialValues
- Validates title (required, 1-200 chars)
- Validates description (optional, 0-1000 chars)
- Shows character count for both fields
- Disables submit button when isSubmitting
- Cancel button calls onCancel (doesn't submit)

**Usage**:
```tsx
// Create mode
<TaskForm
  mode="create"
  onSubmit={async (data) => {
    await createTask(data)
  }}
  onCancel={handleClose}
  isSubmitting={isCreating}
/>

// Edit mode
<TaskForm
  mode="edit"
  initialValues={{ title: task.title, description: task.description }}
  onSubmit={async (data) => {
    await updateTask(task.id, data)
  }}
  onCancel={handleClose}
  isSubmitting={isUpdating}
/>
```

---

### TaskEmpty

```typescript
interface TaskEmptyProps {
  onCreateTask: () => void
}
```

**Behavior**:
- Displays empty state message
- Shows illustration or icon
- Prominent "Create your first task" call-to-action button
- Button triggers onCreateTask

**Usage**:
```tsx
<TaskEmpty onCreateTask={() => setModalOpen(true)} />
```

---

### TaskListSkeleton

```typescript
interface TaskListSkeletonProps {
  count?: number
}
```

**Behavior**:
- Renders skeleton placeholders for task cards
- Default count: 5
- Pulse animation for loading effect
- Matches TaskCard dimensions

**Usage**:
```tsx
{isLoading ? <TaskListSkeleton count={3} /> : <TaskList tasks={tasks} />}
```

---

### DeleteConfirmationModal

```typescript
interface DeleteConfirmationModalProps {
  isOpen: boolean
  onClose: () => void
  onConfirm: () => void
  taskTitle: string
  isDeleting?: boolean
}
```

**Behavior**:
- Displays task title in confirmation message
- Shows "Cancel" and "Delete" buttons
- "Delete" button is danger variant (red)
- Disables buttons when isDeleting
- Shows loading spinner in Delete button when isDeleting

**Usage**:
```tsx
<DeleteConfirmationModal
  isOpen={isModalOpen}
  onClose={() => setModalOpen(false)}
  onConfirm={async () => {
    await deleteTask(taskId)
    setModalOpen(false)
  }}
  taskTitle={task.title}
  isDeleting={isDeleting}
/>
```

---

## Layout Components

### Header

```typescript
interface HeaderProps {
  user: User | null
  onSignOut: () => void
}
```

**Behavior**:
- Displays app logo/title on left
- Shows user email on right
- "Logout" button triggers onSignOut
- Responsive: Collapses to menu on mobile

**Usage**:
```tsx
<Header user={currentUser} onSignOut={handleSignOut} />
```

---

### DashboardLayout

```typescript
interface DashboardLayoutProps {
  children: React.ReactNode
}
```

**Behavior**:
- Wraps children with Header
- Provides consistent padding/spacing
- Responsive container

**Usage**:
```tsx
<DashboardLayout>
  <TaskList tasks={tasks} />
</DashboardLayout>
```

---

## Toast Components

### Toast (from Sonner)

Sonner library provides these functions:

```typescript
import { toast } from 'sonner'

// Success toast
toast.success(message: string, options?: ToastOptions)

// Error toast
toast.error(message: string, options?: ToastOptions)

// Info toast
toast.info(message: string, options?: ToastOptions)

interface ToastOptions {
  duration?: number  // Auto-dismiss duration in ms (default: 5000)
  position?: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right'
}
```

**Usage**:
```tsx
toast.success('Task created successfully')
toast.error('Failed to delete task')
```

---

## Custom Hooks

### useAuth

```typescript
interface UseAuthReturn {
  user: User | null
  isAuthenticated: boolean
  loading: boolean
  error: string | null
  signIn: (email: string, password: string) => Promise<void>
  signOut: () => Promise<void>
}

function useAuth(): UseAuthReturn
```

**Usage**:
```tsx
const { user, isAuthenticated, signIn, signOut } = useAuth()
```

---

### useTasks

```typescript
interface UseTasksReturn {
  tasks: Task[]
  loading: boolean
  error: string | null
  fetchTasks: () => Promise<void>
  createTask: (data: TaskFormData) => Promise<void>
  updateTask: (id: string, data: Partial<Task>) => Promise<void>
  toggleTask: (id: string) => Promise<void>
  deleteTask: (id: string) => Promise<void>
}

function useTasks(): UseTasksReturn
```

**Usage**:
```tsx
const { tasks, loading, createTask, toggleTask, deleteTask } = useTasks()
```

---

### useToast

```typescript
interface UseToastReturn {
  success: (message: string) => void
  error: (message: string) => void
  info: (message: string) => void
}

function useToast(): UseToastReturn
```

**Note**: This is a wrapper around Sonner's toast functions for convenience.

**Usage**:
```tsx
const toast = useToast()
toast.success('Task created successfully')
```

---

## Component Composition Examples

### Complete Task Creation Flow

```tsx
function DashboardPage() {
  const [isModalOpen, setModalOpen] = useState(false)
  const { tasks, loading, createTask } = useTasks()
  const toast = useToast()

  return (
    <AuthGuard>
      <DashboardLayout>
        <Button
          variant="primary"
          onClick={() => setModalOpen(true)}
        >
          Create Task
        </Button>

        {loading ? (
          <TaskListSkeleton count={5} />
        ) : tasks.length === 0 ? (
          <TaskEmpty onCreateTask={() => setModalOpen(true)} />
        ) : (
          <TaskList
            tasks={tasks}
            onToggle={toggleTask}
            onEdit={handleEdit}
            onDelete={handleDelete}
          />
        )}

        <Modal
          isOpen={isModalOpen}
          onClose={() => setModalOpen(false)}
          title="Create Task"
        >
          <TaskForm
            mode="create"
            onSubmit={async (data) => {
              await createTask(data)
              toast.success('Task created successfully')
              setModalOpen(false)
            }}
            onCancel={() => setModalOpen(false)}
          />
        </Modal>
      </DashboardLayout>
    </AuthGuard>
  )
}
```

---

## Responsive Behavior

All components must support responsive design:

### Mobile (320px-768px)
- Stack elements vertically
- Full-width buttons
- Touch-friendly targets (44x44px minimum)
- Simplified header (hamburger menu)

### Tablet (769px-1024px)
- Moderate padding/spacing
- 2-column grid for task cards
- Expanded header

### Desktop (1025px+)
- Generous padding/spacing
- 3-column grid for task cards
- Full header with all elements visible

---

## Accessibility Requirements

All components must:
- Use semantic HTML elements
- Include ARIA labels where needed
- Support keyboard navigation
- Show visible focus indicators
- Maintain WCAG AA color contrast (4.5:1)
- Announce state changes to screen readers

### Examples

```tsx
// Proper button accessibility
<button
  type="button"
  onClick={handleClick}
  aria-label="Delete task"
  aria-busy={isDeleting}
>
  Delete
</button>

// Proper input accessibility
<input
  id="email"
  type="email"
  aria-required="true"
  aria-invalid={!!error}
  aria-describedby={error ? 'email-error' : undefined}
/>
{error && <span id="email-error" role="alert">{error}</span>}
```

---

## Summary

**Base Components**: 5 (Button, Input, Textarea, Modal, LoadingSpinner)
**Auth Components**: 3 (SignUpForm, SignInForm, AuthGuard)
**Task Components**: 6 (TaskCard, TaskList, TaskForm, TaskEmpty, TaskListSkeleton, DeleteConfirmationModal)
**Layout Components**: 2 (Header, DashboardLayout)
**Custom Hooks**: 3 (useAuth, useTasks, useToast)

**Key Design Principles**:
1. Type-safe props with TypeScript interfaces
2. Consistent callback naming (on* prefix)
3. Optional loading and error states
4. Responsive and accessible by default
5. Composable components with single responsibility

**Next Step**: Create quickstart.md developer guide
