/**
 * Task-related TypeScript types
 *
 * This file defines all interfaces and types related to todo tasks,
 * including task data, task state, and form data structures.
 */

/** Represents a single todo item belonging to a user */
export interface Task {
  id: string;              // Unique task identifier (UUID from backend)
  title: string;           // Task title (required)
  description?: string;    // Task description (optional)
  completed: boolean;      // Completion status
  userId: string;          // Owner reference (user who created this task)
  createdAt: string;       // ISO 8601 timestamp
  updatedAt: string;       // ISO 8601 timestamp
}

/** Represents the state of the task list and task operations */
export interface TaskState {
  tasks: Task[];             // Array of tasks for current user
  loading: boolean;          // Task operation in progress
  error: string | null;      // Error message from last task operation
}

/** Data structure for task creation/editing forms */
export interface TaskFormData {
  title: string;
  description?: string;
}

/** API response for task list */
export interface TaskListResponse {
  tasks: Task[];      // Array of tasks for authenticated user
}

/** API request for task creation */
export interface TaskCreateRequest {
  title: string;
  description?: string;
}

/** API response for task creation */
export interface TaskCreateResponse {
  task: Task;         // Newly created task with ID and timestamps
}

/** API request for task update */
export interface TaskUpdateRequest {
  title?: string;
  description?: string;
  completed?: boolean;
}

/** API response for task update */
export interface TaskUpdateResponse {
  task: Task;         // Updated task
}

/** API response for task toggle completion */
export interface TaskToggleResponse {
  task: Task;         // Task with toggled completed status
}

/** API response for task deletion */
export interface TaskDeleteResponse {
  message: string;    // Success message (e.g., "Task deleted successfully")
}

/** Modal state for task operations */
export interface ModalState {
  isOpen: boolean;
  mode: 'create' | 'edit' | 'delete' | null;
  task?: Task;          // Task being edited/deleted (null for create)
}
