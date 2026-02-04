/**
 * Authentication-related TypeScript types
 *
 * This file defines all interfaces and types related to user authentication,
 * including user data, auth state, and form data structures.
 */

/** Represents an authenticated user account */
export interface User {
  id: string;              // Unique user identifier (UUID from backend)
  email: string;           // User email address
}

/** Represents the current authentication state of the application */
export interface AuthState {
  isAuthenticated: boolean;    // Whether user is currently authenticated
  user: User | null;           // Current user (null if not authenticated)
  token: string | null;        // JWT token (null if not authenticated)
  loading: boolean;            // Auth operation in progress
  error: string | null;        // Error message from last auth operation
}

/** Data structure for user registration form */
export interface SignUpFormData {
  email: string;
  password: string;
  confirmPassword?: string;    // Optional: Frontend-only field for UX
}

/** Data structure for user authentication form */
export interface SignInFormData {
  email: string;
  password: string;
}

/** API request for user sign up */
export interface AuthSignUpRequest {
  email: string;
  password: string;
}

/** API response for successful sign up */
export interface AuthSignUpResponse {
  message: string;    // Success message (e.g., "Account created successfully")
}

/** API request for user sign in */
export interface AuthSignInRequest {
  email: string;
  password: string;
}

/** API response for successful sign in */
export interface AuthSignInResponse {
  token: string;      // JWT token
  user: User;         // User object
}

/** Auth context value exposed to consumers */
export interface AuthContextValue {
  authState: AuthState;
  signIn: (data: SignInFormData) => Promise<void>;
  signUp: (data: SignUpFormData) => Promise<void>;
  signOut: () => Promise<void>;
}
