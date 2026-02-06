# Authentication Flow Contract: Frontend UI - Todo Web Application

**Date**: 2026-01-13
**Feature**: Frontend UI - Todo Web Application
**Branch**: `001-frontend-ui`

## Overview

This document defines the complete authentication flow from the frontend perspective, including user journeys, JWT token management, route protection, and error handling.

---

## Sign Up Flow

### User Journey

```
1. User lands on landing page (/)
2. User clicks "Sign Up" or navigates to /signup
3. User enters email and password
4. Frontend validates email format and password strength
5. User submits form
6. Frontend calls POST /api/auth/signup
7. Backend creates account and returns success message
8. Frontend redirects to /signin with success toast
```

### Implementation Flow

```typescript
// Step 1: User navigates to /signup
router.push('/signup')

// Step 2: User fills form
<SignUpForm
  onSubmit={async (email, password) => {
    // Step 3: Frontend validation
    if (!validateEmail(email)) {
      setError('Invalid email format')
      return
    }
    if (!validatePassword(password).isValid) {
      setError('Password does not meet requirements')
      return
    }

    // Step 4: API call
    try {
      const response = await apiClient<AuthSignUpResponse>('/auth/signup', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      })

      // Step 5: Success
      toast.success(response.message)
      router.push('/signin')
    } catch (error) {
      // Step 6: Error handling
      setError(error.message)
    }
  }}
/>
```

### Success Criteria

- ✅ Account created in backend database
- ✅ Success toast displayed: "Account created successfully"
- ✅ User redirected to `/signin` page
- ✅ Form cleared after successful submission

### Error Scenarios

| Error | Frontend Display | User Action |
|-------|------------------|-------------|
| Invalid email format | "Invalid email format" (inline) | Fix email format |
| Weak password | "Password must be at least 8 characters..." | Fix password |
| Email already exists (409) | "An account with this email already exists. Please sign in." | Navigate to sign in |
| Network error | "Connection failed. Please try again." | Retry submission |

---

## Sign In Flow

### User Journey

```
1. User navigates to /signin (or redirected after signup)
2. User enters email and password
3. User submits form
4. Frontend calls POST /api/auth/signin
5. Backend validates credentials and returns JWT token + user object
6. Frontend stores JWT in localStorage
7. Frontend stores user in AuthContext
8. Frontend redirects to /dashboard
```

### Implementation Flow

```typescript
// Step 1: User navigates to /signin
router.push('/signin')

// Step 2: User fills form and submits
<SignInForm
  onSubmit={async (email, password) => {
    setLoading(true)

    try {
      // Step 3: API call
      const response = await apiClient<AuthSignInResponse>('/auth/signin', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      })

      // Step 4: Store token in localStorage
      localStorage.setItem('auth_token', response.token)

      // Step 5: Store user in context
      setUser(response.user)
      setIsAuthenticated(true)

      // Step 6: Redirect to dashboard
      router.push('/dashboard')
    } catch (error) {
      // Step 7: Error handling
      setError('Invalid credentials')
    } finally {
      setLoading(false)
    }
  }}
/>
```

### Success Criteria

- ✅ JWT token stored in localStorage
- ✅ User object stored in AuthContext
- ✅ `isAuthenticated` set to true
- ✅ User redirected to `/dashboard`
- ✅ Dashboard loads and displays user's tasks

### Error Scenarios

| Error | Frontend Display | User Action |
|-------|------------------|-------------|
| Invalid credentials (401) | "Invalid credentials" | Re-enter credentials |
| Account not found (401) | "Invalid credentials" | Check email or sign up |
| Network error | "Connection failed. Please try again." | Retry submission |
| Server error (500) | "Something went wrong. Please try again later." | Retry later |

**Security Note**: Never reveal whether the email or password is incorrect - always show "Invalid credentials" for 401 errors.

---

## JWT Token Management

### Token Storage

**Location**: `localStorage` (as mandated by constitution)

**Key**: `'auth_token'`

**Storage Implementation**:
```typescript
// Store token after successful signin
localStorage.setItem('auth_token', token)

// Retrieve token for API requests
const token = localStorage.getItem('auth_token')

// Clear token on signout
localStorage.removeItem('auth_token')
```

**Security Considerations**:
- localStorage is vulnerable to XSS attacks
- Phase II acceptable for hackathon-grade application
- Production apps should use httpOnly cookies (not in scope)

---

### Token Injection

**All authenticated API requests** must include the token in the Authorization header:

```typescript
const token = localStorage.getItem('auth_token')

const headers = {
  'Content-Type': 'application/json',
  ...(token && { Authorization: `Bearer ${token}` }),
}
```

**Automatic Injection**: The API client wrapper handles this automatically:

```typescript
async function apiClient<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const token = localStorage.getItem('auth_token')

  const config: RequestInit = {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options?.headers,
    },
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, config)
  // ... error handling
}
```

---

### Token Expiration Handling

**Scenario**: User's JWT token expires while using the application

**Detection**: Backend returns 401 Unauthorized

**Automatic Handling**:
```typescript
if (response.status === 401) {
  // Clear expired token
  localStorage.removeItem('auth_token')

  // Redirect to signin
  window.location.href = '/signin?reason=session_expired'

  // Throw error for component to catch
  throw new Error('Session expired. Please sign in again.')
}
```

**User Experience**:
1. User performing action (e.g., creating task)
2. Token is expired (backend returns 401)
3. Frontend automatically clears token and redirects
4. User sees message: "Session expired. Please sign in again."
5. User signs in and returns to application

---

## Route Protection

### Protected Routes

All routes under `/dashboard/*` require authentication.

**Implementation**: Layout-based auth guard

```typescript
// app/(dashboard)/layout.tsx
export default async function DashboardLayout({ children }) {
  const token = localStorage.getItem('auth_token')

  if (!token) {
    redirect('/signin')
  }

  return (
    <div>
      <Header />
      {children}
    </div>
  )
}
```

---

### Public Routes

The following routes are accessible without authentication:
- `/` (landing page - redirects to signin or dashboard based on auth status)
- `/signup`
- `/signin`

---

### Redirect Logic

**Unauthenticated User Accessing Protected Route**:
```
User tries to access /dashboard
  → No token in localStorage
  → Redirect to /signin
```

**Authenticated User Accessing Auth Routes**:
```
User tries to access /signin
  → Token exists in localStorage
  → Redirect to /dashboard
```

**Implementation**:
```typescript
// app/(auth)/signin/page.tsx
export default function SignInPage() {
  useEffect(() => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      router.push('/dashboard')
    }
  }, [])

  return <SignInForm />
}
```

---

## Sign Out Flow

### User Journey

```
1. User clicks "Logout" button in header
2. Frontend clears JWT token from localStorage
3. Frontend clears user from AuthContext
4. Frontend redirects to /signin
5. (Optional) Frontend calls POST /api/auth/signout
```

### Implementation Flow

```typescript
const signOut = async () => {
  try {
    // Optional: Call backend signout (if backend maintains token blacklist)
    await apiClient('/auth/signout', { method: 'POST' })
  } catch {
    // Ignore errors - always sign out locally
  } finally {
    // Clear local state
    localStorage.removeItem('auth_token')
    setUser(null)
    setIsAuthenticated(false)

    // Redirect to signin
    router.push('/signin')

    // Show toast
    toast.info('You have been signed out')
  }
}
```

### Success Criteria

- ✅ JWT token removed from localStorage
- ✅ User removed from AuthContext
- ✅ `isAuthenticated` set to false
- ✅ User redirected to `/signin`
- ✅ Attempting to access `/dashboard` now redirects to `/signin`

---

## Authentication State Management

### AuthContext

```typescript
interface AuthContextValue {
  user: User | null
  isAuthenticated: boolean
  loading: boolean
  error: string | null
  signIn: (email: string, password: string) => Promise<void>
  signOut: () => Promise<void>
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Initialize auth state from localStorage
  useEffect(() => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      // Optionally validate token with backend
      setIsAuthenticated(true)
    }
    setLoading(false)
  }, [])

  const signIn = async (email: string, password: string) => {
    setLoading(true)
    setError(null)

    try {
      const response = await apiClient<AuthSignInResponse>('/auth/signin', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      })

      localStorage.setItem('auth_token', response.token)
      setUser(response.user)
      setIsAuthenticated(true)
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  const signOut = async () => {
    try {
      await apiClient('/auth/signout', { method: 'POST' })
    } catch {
      // Ignore errors
    } finally {
      localStorage.removeItem('auth_token')
      setUser(null)
      setIsAuthenticated(false)
    }
  }

  return (
    <AuthContext.Provider value={{ user, isAuthenticated, loading, error, signIn, signOut }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
```

---

## AuthGuard Component

Reusable component for protecting routes:

```typescript
interface AuthGuardProps {
  children: React.ReactNode
  fallback?: React.ReactNode
}

export function AuthGuard({ children, fallback }: AuthGuardProps) {
  const { isAuthenticated, loading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push('/signin')
    }
  }, [isAuthenticated, loading, router])

  if (loading) {
    return fallback || <LoadingSpinner />
  }

  if (!isAuthenticated) {
    return null // Will redirect
  }

  return <>{children}</>
}
```

**Usage**:
```typescript
// Protect entire page
export default function DashboardPage() {
  return (
    <AuthGuard>
      <Dashboard />
    </AuthGuard>
  )
}
```

---

## Session Persistence

### Page Refresh Behavior

**Scenario**: User refreshes page while authenticated

**Expected Behavior**:
1. Page reloads
2. AuthProvider checks localStorage for token
3. If token exists: Set `isAuthenticated = true`
4. User remains on current page (no redirect)

**Implementation**:
```typescript
// AuthProvider initialization
useEffect(() => {
  const token = localStorage.getItem('auth_token')

  if (token) {
    // Token exists - user is authenticated
    setIsAuthenticated(true)
    // Optionally: Call /api/auth/verify to validate token
  }

  setLoading(false)
}, [])
```

---

## Error State Recovery

### Scenario: Sign In Error

```
User enters wrong password
  → Backend returns 401
  → Frontend displays "Invalid credentials"
  → User corrects password
  → User resubmits
  → Success
```

**Implementation**:
```typescript
const [error, setError] = useState<string | null>(null)

const handleSubmit = async () => {
  setError(null) // Clear previous error

  try {
    await signIn(email, password)
  } catch (err) {
    setError(err.message) // Display new error
  }
}
```

---

## Security Best Practices

### 1. Don't Reveal User Existence

❌ Bad: "Email not found"
✅ Good: "Invalid credentials"

### 2. Clear Token on 401

Always clear token and redirect on 401 responses:
```typescript
if (response.status === 401) {
  localStorage.removeItem('auth_token')
  window.location.href = '/signin'
}
```

### 3. Validate on Both Client and Server

- Client-side validation: UX improvement (instant feedback)
- Server-side validation: Security enforcement (final authority)

### 4. Use HTTPS in Production

- JWT tokens transmitted in headers are visible to network sniffers
- HTTPS encrypts all communication
- Required for production deployment

---

## Testing Scenarios

### Manual Testing Checklist

**Sign Up**:
- [ ] Valid email and password creates account
- [ ] Invalid email shows validation error
- [ ] Weak password shows validation error
- [ ] Duplicate email shows "Email already exists" error
- [ ] Success redirects to signin with toast

**Sign In**:
- [ ] Valid credentials authenticate user
- [ ] Invalid credentials show "Invalid credentials"
- [ ] Success stores token in localStorage
- [ ] Success redirects to dashboard
- [ ] Page refresh maintains authentication

**Sign Out**:
- [ ] Sign out clears token from localStorage
- [ ] Sign out redirects to signin
- [ ] Accessing dashboard after signout redirects to signin

**Token Expiration**:
- [ ] Expired token triggers 401 response
- [ ] 401 clears token and redirects to signin
- [ ] User sees "Session expired" message

**Route Protection**:
- [ ] Unauthenticated user accessing /dashboard redirects to /signin
- [ ] Authenticated user accessing /signin redirects to /dashboard

---

## Flow Diagrams

### Sign Up Flow

```
┌─────────────┐
│ User Input  │
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│ Client Validation│
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ POST /auth/signup│
└──────┬───────────┘
       │
       ├─Success──►┌────────────┐
       │           │ Show Toast │
       │           └─────┬──────┘
       │                 ▼
       │           ┌──────────────┐
       │           │ Redirect /signin│
       │           └──────────────┘
       │
       └─Error────►┌──────────────┐
                   │ Show Error   │
                   └──────────────┘
```

### Sign In Flow

```
┌─────────────┐
│ User Input  │
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│ POST /auth/signin│
└──────┬───────────┘
       │
       ├─Success──►┌─────────────────┐
       │           │ Store Token     │
       │           └────────┬────────┘
       │                    ▼
       │           ┌─────────────────┐
       │           │ Update Context  │
       │           └────────┬────────┘
       │                    ▼
       │           ┌─────────────────┐
       │           │ Redirect /dashboard│
       │           └─────────────────┘
       │
       └─Error────►┌──────────────────┐
                   │ Show "Invalid    │
                   │  credentials"    │
                   └──────────────────┘
```

### Token Expiration Flow

```
┌──────────────────┐
│ User Action      │
│ (e.g., toggle)   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ API Call with    │
│ expired token    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Backend: 401     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Clear Token      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Redirect /signin │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Show "Session    │
│  expired"        │
└──────────────────┘
```

---

## Summary

**Authentication Methods**: Email/Password (Better Auth)
**Token Type**: JWT (JSON Web Token)
**Token Storage**: localStorage (key: 'auth_token')
**Token Transmission**: Authorization header (Bearer token)
**Protected Routes**: /dashboard/*
**Public Routes**: /, /signup, /signin

**Key Flows**:
1. Sign Up → Create account → Redirect to Sign In
2. Sign In → Store token → Redirect to Dashboard
3. Sign Out → Clear token → Redirect to Sign In
4. Token Expiration → Auto-clear → Redirect to Sign In

**Security Measures**:
- Client-side validation (UX)
- Server-side validation (security)
- Automatic 401 handling
- Generic error messages (no user enumeration)
- HTTPS required in production

**Next Step**: Define component prop interfaces
