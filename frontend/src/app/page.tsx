'use client';

/**
 * Landing Page
 *
 * Redirects users based on authentication status:
 * - Authenticated users → /dashboard
 * - Unauthenticated users → /signin
 */

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';

export default function LandingPage() {
  const { authState } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!authState.loading) {
      if (authState.isAuthenticated) {
        router.push('/dashboard');
      } else {
        router.push('/signin');
      }
    }
  }, [authState.loading, authState.isAuthenticated, router]);

  // Show loading spinner while checking auth
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
      <LoadingSpinner size="lg" />
    </div>
  );
}
