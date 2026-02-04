/**
 * useAuth Custom Hook
 *
 * Provides access to authentication state and functions from AuthContext.
 * Must be used within a component wrapped by AuthProvider.
 */

import { useContext } from 'react';
import { AuthContext } from '@/lib/auth/AuthProvider';
import type { AuthContextValue } from '@/types/auth';

/**
 * Custom hook to access authentication context
 *
 * @returns AuthContextValue with current auth state and auth functions
 * @throws Error if used outside of AuthProvider
 *
 * @example
 * function MyComponent() {
 *   const { authState, signIn, signOut } = useAuth();
 *
 *   if (authState.loading) return <LoadingSpinner />;
 *   if (!authState.isAuthenticated) return <SignInForm />;
 *
 *   return <div>Welcome, {authState.user?.email}</div>;
 * }
 */
export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);

  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }

  return context;
}
