'use client';

/**
 * SignUpForm Component
 *
 * Form for user registration with email and password.
 * Includes frontend validation for email format and password strength.
 */

import React, { useState } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { validateEmail, validatePassword } from '@/lib/utils/validation';

export interface SignUpFormProps {
  onSubmit: (email: string, password: string) => Promise<void>;
  loading?: boolean;
}

export function SignUpForm({ onSubmit, loading = false }: SignUpFormProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [errors, setErrors] = useState<{
    email?: string;
    password?: string;
    confirmPassword?: string;
    form?: string;
  }>({});

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Clear previous errors
    setErrors({});

    // Validate email
    if (!validateEmail(email)) {
      setErrors((prev) => ({
        ...prev,
        email: 'Please enter a valid email address',
      }));
      return;
    }

    // Validate password
    const passwordValidation = validatePassword(password);
    if (!passwordValidation.isValid) {
      setErrors((prev) => ({
        ...prev,
        password: passwordValidation.errors[0], // Show first error
      }));
      return;
    }

    // Validate confirm password
    if (password !== confirmPassword) {
      setErrors((prev) => ({
        ...prev,
        confirmPassword: 'Passwords do not match',
      }));
      return;
    }

    // Submit form
    try {
      await onSubmit(email, password);
      // Success handled by parent (redirect to signin)
    } catch (error) {
      setErrors((prev) => ({
        ...prev,
        form: error instanceof Error ? error.message : 'Sign up failed',
      }));
    }
  };

  return (
    <div className="w-full max-w-md mx-auto">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8">
        {/* Header */}
        <div className="text-center mb-6">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
            Create Account
          </h1>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
            Sign up to start managing your tasks
          </p>
        </div>

        {/* Form Error */}
        {errors.form && (
          <div
            className="mb-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg"
            role="alert"
          >
            <p className="text-sm text-red-600 dark:text-red-400">{errors.form}</p>
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            id="email"
            name="email"
            type="email"
            label="Email Address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            error={errors.email}
            required
            disabled={loading}
            placeholder="you@example.com"
          />

          <Input
            id="password"
            name="password"
            type="password"
            label="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            error={errors.password}
            required
            disabled={loading}
            placeholder="••••••••"
          />

          <Input
            id="confirmPassword"
            name="confirmPassword"
            type="password"
            label="Confirm Password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            error={errors.confirmPassword}
            required
            disabled={loading}
            placeholder="••••••••"
          />

          {/* Password Requirements */}
          <div className="text-xs text-gray-600 dark:text-gray-400">
            <p className="font-medium mb-1">Password must contain:</p>
            <ul className="list-disc list-inside space-y-0.5">
              <li>At least 8 characters</li>
              <li>One uppercase letter</li>
              <li>One lowercase letter</li>
              <li>One number</li>
            </ul>
          </div>

          {/* Submit Button */}
          <Button
            type="submit"
            variant="primary"
            className="w-full"
            loading={loading}
            disabled={loading}
          >
            {loading ? 'Creating account...' : 'Sign Up'}
          </Button>
        </form>

        {/* Sign In Link */}
        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Already have an account?{' '}
            <Link
              href="/signin"
              className="font-medium text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300"
            >
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
