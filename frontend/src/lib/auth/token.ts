/**
 * JWT Token Management Utilities
 *
 * Handles localStorage operations for JWT token persistence.
 * These utilities are used by the API client and auth context.
 */

const TOKEN_KEY = 'auth_token';

/**
 * Store JWT token in localStorage
 * @param token - JWT token string
 */
export function setAuthToken(token: string): void {
  if (typeof window !== 'undefined') {
    localStorage.setItem(TOKEN_KEY, token);
  }
}

/**
 * Retrieve JWT token from localStorage
 * @returns JWT token string or null if not found
 */
export function getAuthToken(): string | null {
  if (typeof window !== 'undefined') {
    return localStorage.getItem(TOKEN_KEY);
  }
  return null;
}

/**
 * Remove JWT token from localStorage
 */
export function clearAuthToken(): void {
  if (typeof window !== 'undefined') {
    localStorage.removeItem(TOKEN_KEY);
  }
}

/**
 * Check if a valid token exists
 * @returns true if token exists, false otherwise
 */
export function hasAuthToken(): boolean {
  return getAuthToken() !== null;
}
