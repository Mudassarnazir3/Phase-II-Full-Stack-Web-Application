# Frontend UI Quickstart Guide

**Feature**: Frontend UI - Todo Web Application
**Branch**: `001-frontend-ui`
**Last Updated**: 2026-01-13

## Overview

This guide helps developers quickly set up and start working on the Phase II Todo application frontend. Follow these steps to get the development environment running in under 10 minutes.

---

## Prerequisites

Before starting, ensure you have:

- **Node.js**: Version 18.0.0 or higher
- **npm**: Version 9.0.0 or higher (comes with Node.js)
- **Git**: For version control
- **Code Editor**: VS Code recommended (with TypeScript and Tailwind extensions)
- **Modern Browser**: Chrome, Firefox, Safari, or Edge (latest version)

### Verify Prerequisites

```bash
node --version  # Should be v18.0.0 or higher
npm --version   # Should be v9.0.0 or higher
git --version   # Any recent version
```

---

## Quick Setup (5 Steps)

### Step 1: Clone and Navigate

```bash
# Clone the repository (if not already cloned)
git clone <repository-url>
cd "Phase II-Full-Stack Web Application"

# Checkout the frontend branch
git checkout 001-frontend-ui

# Navigate to frontend directory
cd frontend
```

### Step 2: Install Dependencies

```bash
npm install
```

**Expected output**: Installation of Next.js, React, Tailwind CSS, Better Auth, Sonner, and dev dependencies.

**Time**: ~2-3 minutes depending on internet speed

### Step 3: Configure Environment

```bash
# Copy environment template
cp .env.example .env.local
```

Edit `.env.local`:

```env
# API Backend URL (update when backend is ready)
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth URL (same as frontend)
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

### Step 4: Start Development Server

```bash
npm run dev
```

**Expected output**:
```
▲ Next.js 16.x
- Local:        http://localhost:3000
- Network:      http://192.168.x.x:3000

✓ Ready in 1.5s
```

### Step 5: Open Browser

Navigate to: `http://localhost:3000`

You should see the landing page with sign-in/sign-up options.

---

## Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router (pages)
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Landing page
│   │   ├── (auth)/             # Auth pages group
│   │   │   ├── signup/page.tsx
│   │   │   └── signin/page.tsx
│   │   └── (dashboard)/        # Protected pages group
│   │       └── dashboard/page.tsx
│   ├── components/             # Reusable components
│   │   ├── ui/                 # Base UI components
│   │   ├── auth/               # Auth components
│   │   ├── tasks/              # Task components
│   │   └── layout/             # Layout components
│   ├── lib/                    # Utilities & libraries
│   │   ├── api/                # API client
│   │   ├── auth/               # Auth utilities
│   │   └── utils/              # General utilities
│   ├── hooks/                  # Custom React hooks
│   ├── types/                  # TypeScript types
│   └── styles/                 # Global styles
├── public/                     # Static assets
├── tests/                      # Test files
├── package.json                # Dependencies
├── tsconfig.json               # TypeScript config
├── tailwind.config.js          # Tailwind config
├── next.config.js              # Next.js config
└── .env.local                  # Environment variables (gitignored)
```

---

## Available Commands

### Development

```bash
# Start development server (port 3000)
npm run dev

# Start with different port
npm run dev -- -p 3001
```

### Building

```bash
# Create production build
npm run build

# Start production server
npm start
```

### Code Quality

```bash
# Run ESLint
npm run lint

# Fix ESLint errors automatically
npm run lint:fix

# Run TypeScript compiler check
npm run type-check
```

### Testing

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage

# Run E2E tests
npm run test:e2e
```

---

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout 001-frontend-ui
git pull origin 001-frontend-ui
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Implement component or feature
- Follow TypeScript strict mode
- Use Tailwind CSS for styling
- Write tests for new functionality

### 3. Test Locally

```bash
# Run linter
npm run lint

# Run type check
npm run type-check

# Run tests
npm test

# Test in browser
npm run dev
```

### 4. Commit Changes

```bash
git add .
git commit -m "feat: your descriptive commit message"
```

**Commit Message Convention**:
- `feat:` New feature
- `fix:` Bug fix
- `refactor:` Code refactoring
- `style:` Formatting, styling
- `test:` Adding tests
- `docs:` Documentation updates

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create Pull Request on GitHub targeting `001-frontend-ui` branch.

---

## Key Files to Know

### Configuration Files

- **`package.json`**: Dependencies and scripts
- **`tsconfig.json`**: TypeScript configuration (strict mode enabled)
- **`tailwind.config.js`**: Tailwind CSS customization
- **`next.config.js`**: Next.js configuration
- **`.env.local`**: Environment variables (never commit this)

### Core Application Files

- **`src/app/layout.tsx`**: Root layout with AuthProvider and Toaster
- **`src/lib/api/client.ts`**: API client wrapper with JWT injection
- **`src/hooks/useAuth.ts`**: Authentication hook
- **`src/hooks/useTasks.ts`**: Task management hook
- **`src/types/auth.ts`**: Auth-related TypeScript types
- **`src/types/task.ts`**: Task-related TypeScript types

---

## Common Tasks

### Add a New Page

```bash
# Create new page
touch src/app/my-page/page.tsx
```

```tsx
// src/app/my-page/page.tsx
export default function MyPage() {
  return (
    <div>
      <h1>My Page</h1>
    </div>
  )
}
```

Access at: `http://localhost:3000/my-page`

### Add a New Component

```bash
# Create new component
touch src/components/ui/MyComponent.tsx
```

```tsx
// src/components/ui/MyComponent.tsx
interface MyComponentProps {
  title: string
}

export function MyComponent({ title }: MyComponentProps) {
  return <div>{title}</div>
}
```

### Add API Call

```typescript
// src/lib/api/my-api.ts
import { apiClient } from './client'

export async function getMyData() {
  return apiClient<MyDataResponse>('/my-endpoint')
}
```

### Add Custom Hook

```typescript
// src/hooks/useMyHook.ts
import { useState, useEffect } from 'react'

export function useMyHook() {
  const [data, setData] = useState(null)

  useEffect(() => {
    // Hook logic
  }, [])

  return { data }
}
```

---

## Troubleshooting

### Port 3000 Already in Use

```bash
# Kill process on port 3000 (Windows)
npx kill-port 3000

# Or use different port
npm run dev -- -p 3001
```

### Module Not Found Errors

```bash
# Clear node_modules and reinstall
rm -rf node_modules
npm install

# Or clear Next.js cache
rm -rf .next
npm run dev
```

### TypeScript Errors

```bash
# Run type check to see all errors
npm run type-check

# Restart TypeScript server in VS Code
# Command Palette (Ctrl+Shift+P) → "TypeScript: Restart TS Server"
```

### Tailwind CSS Not Working

```bash
# Ensure Tailwind is imported in globals.css
# src/styles/globals.css should have:
@tailwind base;
@tailwind components;
@tailwind utilities;

# Restart dev server
npm run dev
```

### Environment Variables Not Loading

```bash
# Ensure variables start with NEXT_PUBLIC_
NEXT_PUBLIC_API_URL=http://localhost:8000

# Restart dev server (required after .env changes)
npm run dev
```

---

## VS Code Setup (Recommended)

### Extensions

Install these VS Code extensions:

1. **ES7+ React/Redux/React-Native snippets** - Snippet support
2. **Tailwind CSS IntelliSense** - Tailwind autocomplete
3. **TypeScript Error Translator** - Better TS error messages
4. **ESLint** - Linting support
5. **Prettier** - Code formatting

### Settings

Create `.vscode/settings.json`:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "typescript.preferences.importModuleSpecifier": "relative",
  "tailwindCSS.experimental.classRegex": [
    ["clsx\\(([^)]*)\\)", "(?:'|\"|`)([^']*)(?:'|\"|`)"],
    ["className.*?=.*?\\{([^}]*)\\}", "(?:'|\"|`)([^']*)(?:'|\"|`)"]
  ]
}
```

---

## Testing Strategy

### Component Tests

```tsx
// tests/components/Button.test.tsx
import { render, screen } from '@testing-library/react'
import { Button } from '@/components/ui/Button'

describe('Button', () => {
  it('renders button text', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn()
    render(<Button onClick={handleClick}>Click me</Button>)
    screen.getByText('Click me').click()
    expect(handleClick).toHaveBeenCalledTimes(1)
  })
})
```

### E2E Tests

```typescript
// tests/e2e/auth.spec.ts
import { test, expect } from '@playwright/test'

test('user can sign up and sign in', async ({ page }) => {
  // Navigate to signup
  await page.goto('http://localhost:3000/signup')

  // Fill form
  await page.fill('input[name="email"]', 'test@example.com')
  await page.fill('input[name="password"]', 'TestPass123')

  // Submit
  await page.click('button[type="submit"]')

  // Should redirect to signin
  await expect(page).toHaveURL('http://localhost:3000/signin')
})
```

---

## Performance Tips

### Optimize Re-renders

```tsx
import { memo } from 'react'

// Memoize expensive components
export const TaskCard = memo(function TaskCard({ task }: TaskCardProps) {
  // Component implementation
})
```

### Use Loading States

```tsx
// Show skeleton instead of blank screen
{loading ? <TaskListSkeleton /> : <TaskList tasks={tasks} />}
```

### Debounce User Input

```tsx
import { debounce } from '@/lib/utils/debounce'

const debouncedSearch = useMemo(
  () => debounce((query: string) => {
    // Search logic
  }, 500),
  []
)
```

---

## Debugging

### React DevTools

1. Install React DevTools browser extension
2. Open browser DevTools
3. Navigate to "Components" tab
4. Inspect component props and state

### Network Requests

1. Open browser DevTools
2. Navigate to "Network" tab
3. Filter by "Fetch/XHR"
4. Inspect API requests and responses

### Console Logging

```tsx
// Conditional logging (won't show in production)
if (process.env.NODE_ENV === 'development') {
  console.log('Debug:', data)
}
```

---

## Production Build

### Create Optimized Build

```bash
# Build for production
npm run build

# Test production build locally
npm start
```

### Environment Variables

Create `.env.production`:

```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_BETTER_AUTH_URL=https://yourdomain.com
```

### Deploy

```bash
# Build and deploy to Vercel (recommended)
vercel

# Or build and deploy to your hosting provider
npm run build
# Upload .next folder to server
```

---

## Getting Help

### Documentation

- **Next.js Docs**: https://nextjs.org/docs
- **React Docs**: https://react.dev
- **Tailwind Docs**: https://tailwindcss.com/docs
- **TypeScript Docs**: https://www.typescriptlang.org/docs

### Project Documentation

- **Spec**: `specs/001-frontend-ui/spec.md`
- **Plan**: `specs/001-frontend-ui/plan.md`
- **Research**: `specs/001-frontend-ui/research.md`
- **Data Model**: `specs/001-frontend-ui/data-model.md`
- **API Contract**: `specs/001-frontend-ui/contracts/api-client.md`
- **Component Props**: `specs/001-frontend-ui/contracts/component-props.md`

### Ask for Help

- Check project documentation first
- Search for similar issues on GitHub
- Ask team members
- Create GitHub issue with reproduction steps

---

## Summary

**Setup Time**: ~5-10 minutes
**Development Server**: `npm run dev` (port 3000)
**Key Technologies**: Next.js 16+, React 18+, TypeScript, Tailwind CSS
**API Client**: Custom fetch wrapper with JWT injection
**State Management**: React Context + hooks
**Testing**: Jest + React Testing Library + Playwright

**Quick Start Checklist**:
- [ ] Node.js 18+ installed
- [ ] Repository cloned
- [ ] Branch checked out (`001-frontend-ui`)
- [ ] Dependencies installed (`npm install`)
- [ ] Environment configured (`.env.local`)
- [ ] Dev server running (`npm run dev`)
- [ ] Browser opened (`http://localhost:3000`)

**You're ready to start development!** 🚀
