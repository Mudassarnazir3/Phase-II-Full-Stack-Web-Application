'use client';

/**
 * Sign Up Page
 *
 * Allows new users to create an account.
 * Redirects to signin after successful signup.
 * Redirects to dashboard if already authenticated.
 */

import React, { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { SignUpForm } from '@/components/auth/SignUpForm';
import { useAuth } from '@/hooks/useAuth';

export default function SignUpPage() {
  const { authState, signUp } = useAuth();
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
      <SignUpForm
        onSubmit={async (email, password) => {
          await signUp({ email, password });
        }}
        loading={authState.loading}
      />
    </div>
  );
}
