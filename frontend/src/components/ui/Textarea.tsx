/**
 * Textarea Component
 *
 * Reusable textarea input with label, error display, and validation support.
 * Includes proper accessibility attributes.
 */

import React from 'react';

export interface TextareaProps {
  id: string;
  name: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
  placeholder?: string;
  label?: string;
  error?: string;
  required?: boolean;
  disabled?: boolean;
  rows?: number;
  maxLength?: number;
  className?: string;
}

export function Textarea({
  id,
  name,
  value,
  onChange,
  placeholder,
  label,
  error,
  required = false,
  disabled = false,
  rows = 4,
  maxLength,
  className = '',
}: TextareaProps) {
  const textareaStyles = `
    w-full px-4 py-2 text-base
    bg-white dark:bg-gray-800
    border rounded-lg
    ${error ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 dark:border-gray-600 focus:ring-blue-500'}
    focus:outline-none focus:ring-2 focus:ring-offset-0
    disabled:opacity-50 disabled:cursor-not-allowed
    transition-colors
    resize-vertical
    ${className}
  `.trim();

  return (
    <div className="w-full">
      {label && (
        <label
          htmlFor={id}
          className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
        >
          {label}
          {required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}
      <textarea
        id={id}
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        disabled={disabled}
        rows={rows}
        maxLength={maxLength}
        aria-invalid={!!error}
        aria-describedby={error ? `${id}-error` : undefined}
        className={textareaStyles}
      />
      {maxLength && (
        <p className="mt-1 text-xs text-gray-500 dark:text-gray-400 text-right">
          {value.length} / {maxLength}
        </p>
      )}
      {error && (
        <p
          id={`${id}-error`}
          className="mt-1 text-sm text-red-600 dark:text-red-400"
          role="alert"
        >
          {error}
        </p>
      )}
    </div>
  );
}
