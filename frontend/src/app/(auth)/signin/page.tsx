'use client';

/**
 * Sign In Page
 *
 * Allows existing users to authenticate.
 * Redirects to dashboard after successful signin.
 * Redirects to dashboard if already authenticated.
 */

import React, { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { SignInForm } from '@/components/auth/SignInForm';
import { useAuth } from '@/hooks/useAuth';

export default function SignInPage() {
  const { authState, signIn } = useAuth();
  const router = useRouter();

  // Redirect to dashboard if already authenticated
  useEffect(() => {
    if (!authState.loading && authState.isAuthenticated) {
      router.push('/dashboard');
    }
  }, [authState.loading, authState.isAuthenticated, router]);

  // Show loading while checking auth
  if (authState.loading) {
    return null; // Or show a skeleton
  }

  // Don't render if authenticated (will redirect)
  if (authState.isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 px-4 py-12">
      <SignInForm
        onSubmit={async (email, password) => {
          await signIn({ email, password });
        }}
        loading={authState.loading}
      />
    </div>
  );
}
