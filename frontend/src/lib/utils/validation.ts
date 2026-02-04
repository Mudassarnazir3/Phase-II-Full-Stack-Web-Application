/**
 * Form Validation Utilities
 *
 * Provides validation functions for user input (email, password, task fields).
 * These functions implement the validation rules defined in data-model.md.
 */

// Regular expression for RFC 5322 email validation (simplified)
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

// Password requirements
const PASSWORD_MIN_LENGTH = 8;
const PASSWORD_REGEX = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;

// Task field limits
const TITLE_MIN_LENGTH = 1;
const TITLE_MAX_LENGTH = 200;
const DESCRIPTION_MAX_LENGTH = 1000;

/**
 * Validate email format
 * @param email - Email address to validate
 * @returns true if email is valid, false otherwise
 */
export function validateEmail(email: string): boolean {
  return EMAIL_REGEX.test(email);
}

/**
 * Password validation result with detailed errors
 */
export interface PasswordValidationResult {
  isValid: boolean;
  errors: string[];
}

/**
 * Validate password strength
 * @param password - Password to validate
 * @returns Validation result with isValid flag and error messages
 */
export function validatePassword(password: string): PasswordValidationResult {
  const errors: string[] = [];

  if (password.length < PASSWORD_MIN_LENGTH) {
    errors.push(`Password must be at least ${PASSWORD_MIN_LENGTH} characters`);
  }
  if (!/[a-z]/.test(password)) {
    errors.push('Password must contain at least one lowercase letter');
  }
  if (!/[A-Z]/.test(password)) {
    errors.push('Password must contain at least one uppercase letter');
  }
  if (!/\d/.test(password)) {
    errors.push('Password must contain at least one number');
  }

  return {
    isValid: errors.length === 0,
    errors,
  };
}

/**
 * Validate task title
 * @param title - Task title to validate
 * @returns Error message if invalid, null if valid
 */
export function validateTaskTitle(title: string): string | null {
  const trimmed = title.trim();

  if (trimmed.length < TITLE_MIN_LENGTH) {
    return 'Title is required';
  }
  if (trimmed.length > TITLE_MAX_LENGTH) {
    return `Title must be ${TITLE_MAX_LENGTH} characters or less`;
  }

  return null; // No error
}

/**
 * Validate task description
 * @param description - Task description to validate (optional)
 * @returns Error message if invalid, null if valid
 */
export function validateTaskDescription(description?: string): string | null {
  if (!description) return null; // Optional field

  if (description.length > DESCRIPTION_MAX_LENGTH) {
    return `Description must be ${DESCRIPTION_MAX_LENGTH} characters or less`;
  }

  return null; // No error
}
