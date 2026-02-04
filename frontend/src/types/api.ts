/**
 * API-related TypeScript types
 *
 * This file defines all interfaces and types related to API communication,
 * including error responses and generic API response types.
 */

/** Standard error response from API */
export interface ErrorResponse {
  error: string;      // Human-readable error message
  code?: string;      // Optional error code (e.g., "INVALID_EMAIL", "UNAUTHORIZED")
  details?: any;      // Optional additional error details
}

/** Generic API response wrapper */
export interface ApiResponse<T> {
  data?: T;
  error?: ErrorResponse;
}

/**
 * Common API error codes
 */
export enum ApiErrorCode {
  INVALID_EMAIL = 'INVALID_EMAIL',
  WEAK_PASSWORD = 'WEAK_PASSWORD',
  EMAIL_EXISTS = 'EMAIL_EXISTS',
  INVALID_CREDENTIALS = 'INVALID_CREDENTIALS',
  UNAUTHORIZED = 'UNAUTHORIZED',
  FORBIDDEN = 'FORBIDDEN',
  NOT_FOUND = 'NOT_FOUND',
  NETWORK_ERROR = 'NETWORK_ERROR',
}

/** Toast notification types */
export type ToastType = 'success' | 'error' | 'info' | 'warning';

/** Toast message structure */
export interface ToastMessage {
  id: string;
  type: ToastType;
  message: string;
  duration?: number;    // Auto-dismiss duration in ms (default: 5000)
}
