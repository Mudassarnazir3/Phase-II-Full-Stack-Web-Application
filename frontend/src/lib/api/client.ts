/**
 * API Client Wrapper
 *
 * Provides a centralized HTTP client with:
 * - JWT token injection
 * - Automatic 401 handling (token expiration)
 * - Error response normalization
 * - 30-second timeout
 */

import { getAuthToken, clearAuthToken } from '@/lib/auth/token';
import type { ErrorResponse } from '@/types/api';

// API base URL from environment
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Request timeout (30 seconds)
const REQUEST_TIMEOUT = 30000;

/**
 * Custom error class for API errors
 */
export class ApiError extends Error {
  constructor(
    message: string,
    public statusCode?: number,
    public code?: string
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

/**
 * Generic API client function
 *
 * Handles:
 * - Automatic JWT token injection
 * - 401 response handling (clears token and redirects to signin)
 * - Error response parsing
 * - Network error handling
 * - Request timeout (30s)
 *
 * @param endpoint - API endpoint (e.g., '/auth/signin', '/tasks')
 * @param options - Standard fetch options (method, body, headers, etc.)
 * @returns Parsed JSON response of type T
 * @throws ApiError on failure
 *
 * @example
 * const response = await apiClient<AuthSignInResponse>('/auth/signin', {
 *   method: 'POST',
 *   body: JSON.stringify({ email, password }),
 * });
 */
export async function apiClient<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const token = getAuthToken();
  const url = `${API_BASE_URL}${endpoint}`;

  // Create abort controller for timeout
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT);

  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options?.headers,
      },
      signal: controller.signal,
    });

    // Clear timeout
    clearTimeout(timeoutId);

    // Handle 401 Unauthorized: Token expired or invalid
    if (response.status === 401) {
      clearAuthToken();

      // Redirect to signin (client-side only)
      if (typeof window !== 'undefined') {
        window.location.href = '/signin';
      }

      throw new ApiError('Session expired. Please sign in again.', 401, 'UNAUTHORIZED');
    }

    // Handle other HTTP errors
    if (!response.ok) {
      let errorMessage = 'Request failed';
      let errorCode: string | undefined;

      try {
        const errorData: ErrorResponse = await response.json();
        errorMessage = errorData.error || errorMessage;
        errorCode = errorData.code;
      } catch {
        // If error response is not JSON, use status text
        errorMessage = response.statusText || errorMessage;
      }

      throw new ApiError(errorMessage, response.status, errorCode);
    }

    // Parse successful response
    return await response.json();
  } catch (error) {
    // Clear timeout in case of error
    clearTimeout(timeoutId);

    // Handle AbortError (timeout)
    if (error instanceof Error && error.name === 'AbortError') {
      throw new ApiError(
        'Request timeout. Please try again.',
        undefined,
        'TIMEOUT'
      );
    }

    // Handle network errors (TypeError from fetch)
    if (error instanceof TypeError) {
      throw new ApiError(
        'Connection failed. Please check your internet connection.',
        undefined,
        'NETWORK_ERROR'
      );
    }

    // Re-throw ApiError or other errors
    throw error;
  }
}

/**
 * Helper for GET requests
 */
export async function get<T>(endpoint: string): Promise<T> {
  return apiClient<T>(endpoint, { method: 'GET' });
}

/**
 * Helper for POST requests
 */
export async function post<T>(endpoint: string, body?: any): Promise<T> {
  return apiClient<T>(endpoint, {
    method: 'POST',
    body: body ? JSON.stringify(body) : undefined,
  });
}

/**
 * Helper for PUT requests
 */
export async function put<T>(endpoint: string, body?: any): Promise<T> {
  return apiClient<T>(endpoint, {
    method: 'PUT',
    body: body ? JSON.stringify(body) : undefined,
  });
}

/**
 * Helper for PATCH requests
 */
export async function patch<T>(endpoint: string, body?: any): Promise<T> {
  return apiClient<T>(endpoint, {
    method: 'PATCH',
    body: body ? JSON.stringify(body) : undefined,
  });
}

/**
 * Helper for DELETE requests
 */
export async function del<T>(endpoint: string): Promise<T> {
  return apiClient<T>(endpoint, { method: 'DELETE' });
}
