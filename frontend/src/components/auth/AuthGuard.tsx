'use client';

/**
 * AuthGuard Component
 *
 * Protects routes by checking authentication status.
 * Redirects to signin if user is not authenticated.
 * Shows loading state during auth check.
 */

import React, { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';

export interface AuthGuardProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

export function AuthGuard({ children, fallback }: AuthGuardProps) {
  const { authState } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // If not loading and not authenticated, redirect to signin
    if (!authState.loading && !authState.isAuthenticated) {
      router.push('/signin');
    }
  }, [authState.loading, authState.isAuthenticated, router]);

  // Show loading state
  if (authState.loading) {
    return (
      fallback || (
        <div className="flex items-center justify-center min-h-screen">
          <LoadingSpinner size="lg" />
        </div>
      )
    );
  }

  // Show nothing while redirecting (not authenticated)
  if (!authState.isAuthenticated) {
    return null;
  }

  // Render protected content
  return <>{children}</>;
}
