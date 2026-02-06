'use client';

/**
 * Authentication Context Provider
 *
 * Manages authentication state across the application including:
 * - User authentication status
 * - Current user data
 * - Sign in/sign up/sign out operations
 * - JWT token persistence
 */

import React, { createContext, useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { toast } from 'sonner';
import { apiClient } from '@/lib/api/client';
import { setAuthToken, getAuthToken, clearAuthToken } from '@/lib/auth/token';
import type {
  User,
  AuthState,
  AuthContextValue,
  SignInFormData,
  SignUpFormData,
  AuthSignInResponse,
  AuthSignUpResponse,
} from '@/types/auth';

// Create Auth Context
export const AuthContext = createContext<AuthContextValue | undefined>(undefined);

/**
 * AuthProvider component
 *
 * Wraps the application to provide authentication state and functions
 * to all child components via Context API.
 */
export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [authState, setAuthState] = useState<AuthState>({
    isAuthenticated: false,
    user: null,
    token: null,
    loading: true,
    error: null,
  });

  const router = useRouter();

  // Initialize auth state from localStorage on mount
  useEffect(() => {
    const token = getAuthToken();

    if (token) {
      // Token exists - user is authenticated
      // Note: We don't have user data yet, but token validates on API calls
      setAuthState((prev) => ({
        ...prev,
        isAuthenticated: true,
        token,
        loading: false,
      }));
    } else {
      // No token - user is not authenticated
      setAuthState((prev) => ({
        ...prev,
        loading: false,
      }));
    }
  }, []);

  /**
   * Sign up new user
   */
  const signUp = useCallback(async (data: SignUpFormData): Promise<void> => {
    setAuthState((prev) => ({ ...prev, loading: true, error: null }));

    try {
      const response = await apiClient<AuthSignUpResponse>('/auth/signup', {
        method: 'POST',
        body: JSON.stringify({
          email: data.email,
          password: data.password,
        }),
      });

      // Success - show toast and redirect to signin
      toast.success(response.message || 'Account created successfully');
      router.push('/signin');

      setAuthState((prev) => ({
        ...prev,
        loading: false,
        error: null,
      }));
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Sign up failed';

      setAuthState((prev) => ({
        ...prev,
        loading: false,
        error: errorMessage,
      }));

      toast.error(errorMessage);
      throw error;
    }
  }, [router]);

  /**
   * Sign in existing user
   */
  const signIn = useCallback(async (data: SignInFormData): Promise<void> => {
    setAuthState((prev) => ({ ...prev, loading: true, error: null }));

    try {
      const response = await apiClient<AuthSignInResponse>('/auth/signin', {
        method: 'POST',
        body: JSON.stringify({
          email: data.email,
          password: data.password,
        }),
      });

      // Store token in localStorage
      setAuthToken(response.token);

      // Update auth state
      setAuthState({
        isAuthenticated: true,
        user: response.user,
        token: response.token,
        loading: false,
        error: null,
      });

      // Success - show toast and redirect to dashboard
      toast.success('Signed in successfully');
      router.push('/dashboard');
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Sign in failed';

      setAuthState((prev) => ({
        ...prev,
        loading: false,
        error: errorMessage,
      }));

      toast.error(errorMessage);
      throw error;
    }
  }, [router]);

  /**
   * Sign out current user
   */
  const signOut = useCallback(async (): Promise<void> => {
    try {
      // Optional: Call backend signout endpoint (if backend maintains token blacklist)
      // Ignore errors - always sign out locally
      await apiClient('/auth/signout', { method: 'POST' }).catch(() => {});
    } finally {
      // Clear token from localStorage
      clearAuthToken();

      // Reset auth state
      setAuthState({
        isAuthenticated: false,
        user: null,
        token: null,
        loading: false,
        error: null,
      });

      // Show toast and redirect to signin
      toast.info('You have been signed out');
      router.push('/signin');
    }
  }, [router]);

  const contextValue: AuthContextValue = {
    authState,
    signIn,
    signUp,
    signOut,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
}
