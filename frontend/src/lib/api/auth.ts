/**
 * Authentication API Functions
 *
 * Provides typed wrappers for authentication API calls.
 * These functions use the API client to communicate with the FastAPI backend.
 */

import { post } from '@/lib/api/client';
import type {
  AuthSignUpRequest,
  AuthSignUpResponse,
  AuthSignInRequest,
  AuthSignInResponse,
} from '@/types/auth';

/**
 * Sign up a new user
 *
 * @param email - User email address
 * @param password - User password
 * @returns Success message from backend
 */
export async function signUpAPI(
  email: string,
  password: string
): Promise<AuthSignUpResponse> {
  const request: AuthSignUpRequest = { email, password };
  return post<AuthSignUpResponse>('/auth/signup', request);
}

/**
 * Sign in an existing user
 *
 * @param email - User email address
 * @param password - User password
 * @returns JWT token and user object
 */
export async function signInAPI(
  email: string,
  password: string
): Promise<AuthSignInResponse> {
  const request: AuthSignInRequest = { email, password };
  return post<AuthSignInResponse>('/auth/signin', request);
}

/**
 * Sign out current user
 *
 * Optional endpoint - backend may or may not implement token blacklist.
 * Frontend always clears token locally regardless of API response.
 *
 * @returns Success message (optional)
 */
export async function signOutAPI(): Promise<void> {
  try {
    await post<{ message: string }>('/auth/signout');
  } catch {
    // Ignore errors - always sign out locally
  }
}
