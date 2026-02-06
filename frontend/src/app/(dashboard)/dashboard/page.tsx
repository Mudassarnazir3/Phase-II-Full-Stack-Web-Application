'use client';

/**
 * Dashboard Page (Placeholder)
 *
 * Main dashboard for authenticated users.
 * Will be implemented in Phase 4 (US2: View Tasks).
 */

import React from 'react';
import { AuthGuard } from '@/components/auth/AuthGuard';
import { useAuth } from '@/hooks/useAuth';
import { Button } from '@/components/ui/Button';

export default function DashboardPage() {
  const { authState, signOut } = useAuth();

  return (
    <AuthGuard>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        {/* Header */}
        <header className="bg-white dark:bg-gray-800 shadow">
          <div className="container-custom py-4 flex items-center justify-between">
            <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
              Todo App
            </h1>
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-600 dark:text-gray-400">
                {authState.user?.email}
              </span>
              <Button
                variant="ghost"
                onClick={() => signOut()}
                loading={authState.loading}
              >
                Sign Out
              </Button>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="container-custom py-8">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 text-center">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">
              Welcome to your Dashboard!
            </h2>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              Task management features will be implemented in Phase 4.
            </p>
            <div className="inline-block px-4 py-2 bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-300 rounded-lg">
           🎯 Phase 3 Complete: Authentication Working!
            </div>
          </div>
        </main>
      </div>
    </AuthGuard>
  );
}
