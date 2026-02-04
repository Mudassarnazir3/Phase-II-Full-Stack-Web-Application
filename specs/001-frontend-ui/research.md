# Phase 0 Research: Frontend UI Technology Decisions

**Date**: 2026-01-13
**Feature**: Frontend UI - Todo Web Application
**Branch**: `001-frontend-ui`
**Status**: Complete

## Overview

This document captures all technology research and decisions made during Phase 0 planning for the frontend UI implementation. All decisions are based on Next.js 16+ App Router, TypeScript, Tailwind CSS, and Better Auth as mandated by the constitution.

---

## R001: Better Auth + Next.js App Router Integration

### Question
How should Better Auth be configured with Next.js 16+ App Router to issue and validate JWT tokens?

### Research Findings

**Better Auth Overview**:
- Better Auth is a modern authentication library designed for Next.js with first-class App Router support
- Provides built-in JWT token generation and validation
- Supports multiple authentication providers and strategies
- Integrates seamlessly with server components and API routes

**Integration Approaches**:

1. **API Route Handler Pattern** (Recommended):
   - Create Better Auth instance in `/api/auth/[...auth]/route.ts`
   - Handle signup, signin, signout through Better Auth endpoints
   - Better Auth automatically manages JWT issuance and validation
   - Frontend calls these endpoints for authentication operations

2. **Custom Auth Wrapper**:
   - Wrap Better Auth with custom middleware
   - More control but increased complexity

### Decision

**Chosen Approach**: API Route Handler Pattern

**Rationale**:
- Simplest integration with App Router
- Better Auth handles JWT complexity automatically
- Follows Next.js best practices for API routes
- Reduces custom code and maintenance burden

**JWT Storage Strategy**: localStorage

**Rationale**:
- Constitution explicitly requires localStorage for JWT tokens
- Acceptable for this Phase II hackathon-grade application
- Simple implementation and debugging
- Note: httpOnly cookies would be more secure for production but not mandated here

**Route Protection Pattern**: Layout-based Auth Guard

**Rationale**:
- App Router best practice: check auth in layout.tsx for protected routes
- Middleware can be used for redirects but layout provides better UX
- Allows for loading states during auth check
- Easier to debug than middleware-based protection

**Implementation Pattern**:

```typescript
// Better Auth configuration
// app/api/auth/[...auth]/route.ts
import { betterAuth } from 'better-auth'

export const auth = betterAuth({
  jwt: {
    enabled: true,
    expiresIn: '7d',
  },
  providers: {
    emailPassword: true
  }
})

export const { GET, POST } = auth.handler
```

**Token Refresh**: Not implemented in Phase II

**Rationale**:
- Phase II scope is limited to basic authentication
- 7-day token expiration is sufficient for hackathon demo
- Refresh tokens add complexity beyond Phase II requirements

---

## R002: API Client Architecture

### Question
What's the best pattern for a REST API client with JWT authentication in Next.js App Router?

### Research Findings

**Option 1: Native Fetch API**:
- Pros: No dependencies, built into browsers, well-supported in Next.js
- Cons: More boilerplate for interceptors, manual error handling

**Option 2: Axios**:
- Pros: Interceptors, automatic JSON parsing, comprehensive error handling
- Cons: Additional dependency (~13KB), overkill for simple use case

**Option 3: Custom Fetch Wrapper**:
- Pros: Lightweight, tailored to our needs, full control
- Cons: Need to implement error handling and JWT injection manually

### Decision

**Chosen Approach**: Custom Fetch Wrapper

**Rationale**:
- Minimal dependencies (Next.js philosophy)
- Easy to implement JWT injection
- Full control over error handling patterns
- Type-safe with TypeScript
- ~50 lines of code vs 13KB dependency

**JWT Injection Pattern**: Wrapper function with automatic token retrieval

**Implementation Pattern**:

```typescript
// lib/api/client.ts
async function apiClient<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const token = localStorage.getItem('auth_token')
  const baseURL = process.env.NEXT_PUBLIC_API_URL || ''

  const config: RequestInit = {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options?.headers,
    },
  }

  const response = await fetch(`${baseURL}${endpoint}`, config)

  if (!response.ok) {
    if (response.status === 401) {
      localStorage.removeItem('auth_token')
      window.location.href = '/signin'
    }
    throw new Error(await response.text())
  }

  return response.json()
}
```

**Error Handling Approach**: Throw errors with status codes, handle in components

**Rationale**:
- Simple try-catch patterns in components
- Consistent error handling across application
- Automatic 401 handling for expired tokens

---

## R003: State Management Strategy

### Question
Do we need a state management library (Zustand, Jotai, Redux) or is React Context + hooks sufficient?

### Research Findings

**Complexity Analysis**:
- **Auth State**: Shared across app (user, token, isAuthenticated)
- **Task State**: Mostly local to dashboard, but needs optimistic updates
- **UI State**: Toast notifications, modals - can be local

**State Management Options**:

1. **React Context + Hooks**:
   - Pros: No dependencies, built-in, sufficient for simple state
   - Cons: Can cause unnecessary re-renders if not careful

2. **Zustand** (lightweight):
   - Pros: Minimal (~1KB), simple API, good TypeScript support
   - Cons: Additional dependency, overkill for this scope

3. **Jotai** (atomic):
   - Pros: Atomic state management, performant
   - Cons: Learning curve, unnecessary complexity

4. **Redux Toolkit**:
   - Pros: Industry standard, dev tools
   - Cons: Heavy (~45KB), massive overkill for this app

### Decision

**Chosen Approach**: React Context + Custom Hooks

**Rationale**:
- No additional dependencies needed
- Application state is simple (auth + task list)
- Performance is acceptable for up to 1000 tasks
- Custom hooks provide clean API (useAuth, useTasks)
- Optimistic UI can be handled with useState in hooks

**State Organization**:

```typescript
// AuthContext: Global authentication state
// useTasks hook: Local state with optimistic updates
// useToast hook: Local UI state
```

**Optimistic UI Pattern**: Local state updates before API call, revert on error

**Implementation Pattern**:

```typescript
const useTasks = () => {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(false)

  const toggleTask = async (id: string) => {
    // Optimistic update
    setTasks(prev => prev.map(t =>
      t.id === id ? { ...t, completed: !t.completed } : t
    ))

    try {
      await api.patch(`/tasks/${id}/toggle`)
    } catch (error) {
      // Revert on error
      setTasks(prev => prev.map(t =>
        t.id === id ? { ...t, completed: !t.completed } : t
      ))
      toast.error('Failed to update task')
    }
  }

  return { tasks, toggleTask, loading }
}
```

---

## R004: Form Handling & Validation

### Question
Should we use React Hook Form, Formik, or native React state for forms?

### Research Findings

**Form Complexity**:
- Sign up: Email + Password (2 fields)
- Sign in: Email + Password (2 fields)
- Task create: Title + Description (2 fields)
- Task edit: Title + Description (2 fields)

All forms are simple with minimal validation requirements.

**Option Comparison**:

1. **React Hook Form**:
   - Pros: Performant, good DX, TypeScript support
   - Cons: ~40KB, overkill for 2-field forms

2. **Formik**:
   - Pros: Mature, widely used
   - Cons: ~45KB, verbose API, heavier than needed

3. **Native React State**:
   - Pros: No dependencies, simple, full control
   - Cons: More boilerplate, manual validation

### Decision

**Chosen Approach**: Native React State with Custom Validation

**Rationale**:
- Forms are very simple (2 fields each)
- Validation logic is straightforward (email regex, password strength, title length)
- No need for complex form libraries
- Reduces bundle size significantly (~40-45KB saved)
- Easy to understand and maintain

**Validation Strategy**: Client-side validation with clear error messages

**Implementation Pattern**:

```typescript
const SignInForm = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [errors, setErrors] = useState<{email?: string; password?: string}>({})

  const validate = () => {
    const newErrors: any = {}
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      newErrors.email = 'Invalid email format'
    }
    if (password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters'
    }
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!validate()) return
    // Submit form
  }

  return (/* form JSX */)
}
```

**Validation Rules**:
- Email: RFC 5322 regex pattern
- Password: Min 8 chars, 1 uppercase, 1 lowercase, 1 number
- Task Title: 1-200 characters, trimmed, required
- Task Description: 0-1000 characters, optional

---

## R005: Toast Notification Pattern

### Question
What's the recommended toast notification library for Next.js App Router?

### Research Findings

**Options**:

1. **Sonner**:
   - Pros: Modern, beautiful default styling, accessible, ~5KB
   - Cons: Relatively new library

2. **react-hot-toast**:
   - Pros: Mature, widely used, simple API, ~3KB
   - Cons: Basic styling requires customization

3. **react-toastify**:
   - Pros: Very mature, feature-rich
   - Cons: Heavier (~20KB), more complex than needed

4. **Custom Implementation**:
   - Pros: Full control, no dependencies
   - Cons: Need to implement accessibility, positioning, animations

### Decision

**Chosen Approach**: Sonner

**Rationale**:
- Perfect size/feature balance (~5KB)
- Beautiful defaults that match modern UI expectations
- Built-in accessibility (ARIA live regions)
- Works seamlessly with Tailwind CSS
- Active development and Next.js focused
- Simple API: `toast.success()`, `toast.error()`

**Implementation Pattern**:

```typescript
// app/layout.tsx
import { Toaster } from 'sonner'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Toaster position="top-right" />
      </body>
    </html>
  )
}

// In components
import { toast } from 'sonner'

toast.success('Task created successfully')
toast.error('Failed to update task')
```

**Positioning**: Top-right (industry standard, non-intrusive)

**Accessibility**: Sonner handles ARIA live regions automatically

---

## R006: Loading State Patterns

### Question
What patterns should we use for loading indicators (skeleton screens vs spinners)?

### Research Findings

**Loading Scenarios**:
1. Initial page load (dashboard with tasks)
2. Authentication (signin/signup)
3. Task operations (create, edit, delete)
4. Task toggle (quick operation)

**Pattern Options**:

1. **Skeleton Screens**:
   - Pros: Better perceived performance, shows page structure
   - Cons: More complex to implement, need skeleton for each component

2. **Spinners**:
   - Pros: Simple, universal, easy to implement
   - Cons: Doesn't show structure, can feel slower

3. **Hybrid Approach**:
   - Skeleton for initial loads (task list)
   - Spinners for operations (form submissions)
   - Inline indicators for quick actions (toggle checkbox)

### Decision

**Chosen Approach**: Hybrid Pattern

**Rationale**:
- Skeleton screens for task list provide better UX (shows structure)
- Spinners for modals/forms are simple and sufficient
- Inline loading for task toggle (subtle indicator on checkbox)
- Matches modern web app UX expectations

**300ms Delay Implementation**: Use `setTimeout` to avoid flashing

**Implementation Pattern**:

```typescript
const TaskList = () => {
  const [tasks, setTasks] = useState<Task[]>([])
  const [showLoading, setShowLoading] = useState(false)

  useEffect(() => {
    const timer = setTimeout(() => setShowLoading(true), 300)

    fetchTasks().then(data => {
      clearTimeout(timer)
      setTasks(data)
      setShowLoading(false)
    })

    return () => clearTimeout(timer)
  }, [])

  if (showLoading) return <TaskListSkeleton />
  return <TaskList tasks={tasks} />
}
```

**Skeleton Component**: Card-like shapes with pulse animation (Tailwind)

**Spinner Component**: Circular spinner with Tailwind animation

**Suspense Boundaries**: Use React Suspense for async components in App Router

---

## R007: Responsive Design Breakpoints

### Question
What Tailwind CSS breakpoint strategy should we use for mobile/tablet/desktop?

### Research Findings

**Tailwind Default Breakpoints**:
- sm: 640px
- md: 768px
- lg: 1024px
- xl: 1280px
- 2xl: 1536px

**Spec Requirements**:
- Mobile: 320px-768px
- Tablet: 769px-1024px
- Desktop: 1025px+

### Decision

**Chosen Approach**: Standard Tailwind Breakpoints (mobile-first)

**Rationale**:
- Tailwind defaults align perfectly with spec requirements
- Mobile-first approach (default styles = mobile)
- No custom configuration needed
- `md:` prefix for tablet (768px+)
- `lg:` prefix for desktop (1024px+)

**Breakpoint Strategy**:

```css
/* Mobile: Default (no prefix) */
.container { padding: 1rem; }

/* Tablet: md: prefix (768px+) */
@media (min-width: 768px) {
  .container { padding: 1.5rem; }
}

/* Desktop: lg: prefix (1024px+) */
@media (min-width: 1024px) {
  .container { padding: 2rem; }
}
```

**Touch Target Sizing**: Minimum 44x44px on mobile (Tailwind utilities)

**Implementation Pattern**:

```tsx
<button className="
  h-11 px-4           // Mobile: 44px height, padding
  md:h-10 md:px-6     // Tablet: 40px height, more padding
  lg:h-12 lg:px-8     // Desktop: 48px height, generous padding
">
  Button Text
</button>
```

**Typography Scaling**: Use Tailwind responsive text utilities

```tsx
<h1 className="
  text-2xl            // Mobile: 24px
  md:text-3xl         // Tablet: 30px
  lg:text-4xl         // Desktop: 36px
">
  Heading
</h1>
```

**Container Max Width**: Use Tailwind container utility

```tsx
<div className="container mx-auto px-4 md:px-6 lg:px-8">
  {/* Content */}
</div>
```

---

## Technology Stack Summary

### Final Decisions

| Category | Technology | Rationale |
|----------|-----------|-----------|
| **Authentication** | Better Auth (API Route Pattern) | First-class App Router support, automatic JWT handling |
| **JWT Storage** | localStorage | Constitution requirement, simple implementation |
| **Route Protection** | Layout-based Auth Guard | Best practice for App Router, better UX |
| **API Client** | Custom Fetch Wrapper | Lightweight, full control, type-safe |
| **State Management** | React Context + Hooks | Sufficient for app complexity, no extra dependencies |
| **Form Handling** | Native React State | Simple forms, no library needed, reduces bundle size |
| **Validation** | Custom Functions | Straightforward validation rules, full control |
| **Toast Notifications** | Sonner | Modern, accessible, perfect size (~5KB) |
| **Loading States** | Hybrid (Skeleton + Spinner) | Best UX for each scenario |
| **Responsive Design** | Tailwind Default Breakpoints | Aligns with spec, mobile-first approach |

### Rejected Alternatives

| Technology | Reason for Rejection |
|-----------|---------------------|
| Axios | Custom fetch wrapper sufficient, saves ~13KB |
| React Hook Form | Forms too simple, saves ~40KB |
| Formik | Forms too simple, saves ~45KB |
| Zustand/Jotai/Redux | Context API sufficient for app complexity |
| react-toastify | Sonner more modern and lighter |
| httpOnly cookies | localStorage mandated by constitution |
| Middleware auth | Layout-based approach better for App Router UX |

### Bundle Size Impact

**Avoided Dependencies** (savings):
- Axios: ~13KB
- React Hook Form: ~40KB
- React Toastify: ~20KB
- Zustand: ~1KB (minimal but unnecessary)

**Added Dependencies**:
- Sonner: ~5KB (necessary for good UX)

**Net Savings**: ~69KB reduction by making pragmatic technology choices

---

## Implementation Guidelines

### Code Organization

```
lib/
  api/
    client.ts          // Custom fetch wrapper
    auth.ts            // Auth API calls
    tasks.ts           // Task API calls
  auth/
    better-auth.ts     // Better Auth configuration
    token.ts           // JWT token utilities
  utils/
    validation.ts      // Form validation functions
    debounce.ts        // Debounce utility
```

### Best Practices

1. **API Client Usage**: Always use `apiClient()` wrapper, never raw fetch
2. **Error Handling**: Try-catch in components, display toast on error
3. **Loading States**: Use 300ms delay pattern consistently
4. **Optimistic UI**: Update immediately, revert on error, show toast
5. **Validation**: Client-side validation before API calls
6. **Responsive Design**: Mobile-first, test on real devices
7. **Accessibility**: Semantic HTML, keyboard navigation, ARIA labels
8. **TypeScript**: Strict mode, no `any` types, comprehensive interfaces

---

## Risks & Mitigation

### Risk 1: Better Auth Learning Curve

**Mitigation**:
- Thoroughly review Better Auth documentation before implementation
- Create isolated auth prototype to validate approach
- Document auth flow clearly in contracts

### Risk 2: Custom Fetch Client Bugs

**Mitigation**:
- Comprehensive unit tests for client wrapper
- Type-safe with TypeScript
- Test all error scenarios (401, 403, 404, network errors)

### Risk 3: Performance with 1000 Tasks

**Mitigation**:
- Profile with React DevTools during development
- Implement pagination if needed (can be added later)
- Use React.memo for task cards if re-renders become issue

---

## Phase 0 Completion Status

✅ **All research questions answered**
✅ **Technology choices documented with rationale**
✅ **No remaining "NEEDS CLARIFICATION" items**
✅ **Ready to proceed to Phase 1 (Design & Contracts)**

**Next Step**: Generate Phase 1 design artifacts (data-model.md, contracts/, quickstart.md)
