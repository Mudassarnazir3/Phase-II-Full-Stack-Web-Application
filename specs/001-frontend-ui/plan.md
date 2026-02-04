# Implementation Plan: Frontend UI - Todo Web Application

**Branch**: `001-frontend-ui` | **Date**: 2026-01-13 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-frontend-ui/spec.md`

## Summary

Build a production-grade, responsive frontend UI for the Phase II Todo application using Next.js 16+ App Router, TypeScript, and Tailwind CSS. The frontend will implement secure JWT-based authentication via Better Auth, provide comprehensive task management interfaces (view, create, edit, delete, toggle completion), and deliver a clean, professional user experience across mobile, tablet, and desktop devices. Implementation follows a frontend-first approach with staged delivery: application shell → authentication UI → core task features → states and polish → integration readiness validation.

## Technical Context

**Language/Version**: TypeScript 5.x with Next.js 16+
**Primary Dependencies**: Next.js (App Router), React 18+, Tailwind CSS 3.x, Better Auth (JWT), Axios/Fetch for API client
**Storage**: Browser localStorage for JWT token persistence
**Testing**: Jest + React Testing Library for component tests, Playwright for E2E tests
**Target Platform**: Modern web browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
**Project Type**: Web application (frontend only - this plan)
**Performance Goals**:
- Page load < 2 seconds
- Task operations complete within 1 second (95th percentile)
- First Contentful Paint < 1.5 seconds
- Loading indicators appear after 300ms delay

**Constraints**:
- Mobile-first responsive design (320px minimum width)
- WCAG AA accessibility compliance
- No backend implementation in this plan (frontend integration readiness only)
- JWT token security (stored in localStorage, transmitted via Authorization header)

**Scale/Scope**:
- 6 user-facing pages (signup, signin, dashboard, and states)
- 10+ reusable UI components
- 55 functional requirements to implement
- Target: single user managing up to 1000 tasks

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase II Scope Compliance

✅ **PASS** - Multi-user Todo Web Application frontend
✅ **PASS** - Responsive web UI (mobile + desktop)
✅ **PASS** - JWT-based authentication (Better Auth integration)
❌ **BLOCKED** - No chatbots, AI assistants, or MCP tools
❌ **BLOCKED** - No Phase III/IV features
❌ **BLOCKED** - No admin or superuser roles

### Technology Stack Compliance

✅ **PASS** - Next.js 16+ with App Router (as mandated)
✅ **PASS** - TypeScript (as mandated)
✅ **PASS** - Tailwind CSS (as mandated)
✅ **PASS** - Better Auth with JWT enabled (as mandated)
✅ **PASS** - Responsive design (mobile + desktop)

### API Architecture Compliance (Frontend Side)

✅ **PASS** - Frontend expects REST API endpoints under `/api/*`
✅ **PASS** - JWT passed via Authorization header (Bearer token)
✅ **PASS** - No GraphQL or RPC dependencies
✅ **PASS** - Only task CRUD and completion toggle operations

### UI Security & Responsiveness Compliance

✅ **PASS** - Authentication required before task access
✅ **PASS** - No cross-user data display (JWT scoped to user)
✅ **PASS** - Responsive design (320px - desktop)
✅ **PASS** - Backend is final authority (frontend validates but doesn't enforce)

### Agent Conduct Compliance

✅ **PASS** - Architecture Planner (this agent) designing system architecture
✅ **PASS** - No scope expansion beyond spec
✅ **PASS** - Frontend Engineer will implement, not reinterpret
✅ **PASS** - Integration Tester will validate, not modify

**Constitution Check Result**: ✅ **ALL GATES PASSED** - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/001-frontend-ui/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification (completed)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   ├── api-client.md    # Frontend API client contract
│   ├── auth-flow.md     # Authentication flow contract
│   └── component-props.md # Component interface contracts
├── checklists/
│   └── requirements.md  # Quality validation checklist (completed)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── layout.tsx          # Root layout with auth provider
│   │   ├── page.tsx            # Landing/redirect page
│   │   ├── (auth)/             # Auth route group
│   │   │   ├── signup/
│   │   │   │   └── page.tsx    # Sign up page
│   │   │   └── signin/
│   │   │       └── page.tsx    # Sign in page
│   │   └── (dashboard)/        # Protected route group
│   │       ├── layout.tsx      # Dashboard layout with header
│   │       └── dashboard/
│   │           └── page.tsx    # Main dashboard page
│   ├── components/             # Reusable UI components
│   │   ├── ui/                 # Base UI components
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Modal.tsx
│   │   │   ├── Toast.tsx
│   │   │   └── LoadingSpinner.tsx
│   │   ├── auth/               # Authentication components
│   │   │   ├── SignUpForm.tsx
│   │   │   ├── SignInForm.tsx
│   │   │   └── AuthGuard.tsx
│   │   ├── tasks/              # Task-related components
│   │   │   ├── TaskCard.tsx
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskForm.tsx
│   │   │   ├── TaskEmpty.tsx
│   │   │   └── TaskSkeleton.tsx
│   │   └── layout/             # Layout components
│   │       └── Header.tsx
│   ├── lib/                    # Utility libraries
│   │   ├── api/                # API client
│   │   │   ├── client.ts       # Axios/Fetch wrapper with JWT
│   │   │   ├── auth.ts         # Auth API calls
│   │   │   └── tasks.ts        # Task API calls
│   │   ├── auth/               # Auth utilities
│   │   │   ├── better-auth.ts  # Better Auth configuration
│   │   │   └── token.ts        # JWT token management
│   │   └── utils/              # General utilities
│   │       ├── validation.ts   # Form validation
│   │       └── debounce.ts     # Debounce utility
│   ├── hooks/                  # Custom React hooks
│   │   ├── useAuth.ts          # Authentication hook
│   │   ├── useTasks.ts         # Task management hook
│   │   └── useToast.ts         # Toast notifications hook
│   ├── types/                  # TypeScript type definitions
│   │   ├── auth.ts             # Auth-related types
│   │   └── task.ts             # Task-related types
│   └── styles/                 # Global styles
│       └── globals.css         # Tailwind imports + custom styles
├── public/                     # Static assets
│   └── favicon.ico
├── tests/                      # Test files
│   ├── components/             # Component tests
│   └── e2e/                    # End-to-end tests
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── next.config.js
└── .env.local                  # Environment variables (gitignored)
```

**Structure Decision**: Selected Web application structure (Option 2 from template) with frontend-only scope. The frontend directory contains all UI implementation using Next.js App Router with clear separation of concerns: pages (`app/`), reusable components (`components/`), business logic (`lib/`), custom hooks (`hooks/`), and type definitions (`types/`). Route groups organize auth pages separately from protected dashboard pages. This structure supports incremental development, component reusability, and clear testing boundaries.

## Complexity Tracking

> **No violations identified** - All constitution requirements met without compromise.

---

## Phase 0: Research & Technology Decisions

**Responsible Agent**: Architecture Planner Agent (this agent)
**Prerequisites**: Specification approved, Constitution Check passed
**Duration**: Research phase (no code)

### Objectives

1. Resolve all technology-specific implementation questions
2. Establish Best Auth integration pattern for Next.js 16+ App Router
3. Define API client architecture (REST client with JWT)
4. Determine state management approach (if needed)
5. Identify optimal UI component patterns for Tailwind CSS

### Research Tasks

#### R001: Better Auth + Next.js App Router Integration

**Question**: How should Better Auth be configured with Next.js 16+ App Router to issue and validate JWT tokens?

**Research Areas**:
- Better Auth documentation for Next.js App Router
- JWT token storage best practices (localStorage vs httpOnly cookies)
- Route protection patterns in App Router (middleware vs layout-based)
- Token refresh strategies

**Decision Required**: Better Auth configuration approach, JWT storage location, route protection pattern

#### R002: API Client Architecture

**Question**: What's the best pattern for a REST API client with JWT authentication in Next.js App Router?

**Research Areas**:
- Axios vs native Fetch API for Next.js App Router
- JWT token injection patterns (interceptors vs wrapper functions)
- Error handling and retry logic
- Request/response type safety with TypeScript

**Decision Required**: HTTP client library choice, JWT injection pattern, error handling approach

#### R003: State Management Strategy

**Question**: Do we need a state management library (Zustand, Jotai, Redux) or is React Context + hooks sufficient?

**Research Areas**:
- Task list state management requirements (local state vs global)
- Optimistic UI update patterns
- Authentication state sharing across components
- Performance implications for up to 1000 tasks

**Decision Required**: State management approach (Context API, lightweight library, or none)

#### R004: Form Handling & Validation

**Question**: Should we use React Hook Form, Formik, or native React state for forms?

**Research Areas**:
- Form library comparison for TypeScript + Tailwind
- Validation patterns (client-side schema validation)
- Error message display conventions
- Accessibility considerations for form errors

**Decision Required**: Form handling library and validation strategy

#### R005: Toast Notification Pattern

**Question**: What's the recommended toast notification library for Next.js App Router?

**Research Areas**:
- Sonner, react-hot-toast, or custom implementation
- Accessibility (ARIA live regions)
- Positioning and animation patterns
- Integration with Tailwind CSS

**Decision Required**: Toast library choice or custom implementation approach

#### R006: Loading State Patterns

**Question**: What patterns should we use for loading indicators (skeleton screens vs spinners)?

**Research Areas**:
- Skeleton screen best practices for task lists
- Loading delay patterns (300ms threshold from spec)
- Suspense boundaries in App Router
- Progressive loading vs full-page spinners

**Decision Required**: Loading UI patterns for different scenarios

#### R007: Responsive Design Breakpoints

**Question**: What Tailwind CSS breakpoint strategy should we use for mobile/tablet/desktop?

**Research Areas**:
- Standard Tailwind breakpoints vs custom
- Mobile-first approach implementation
- Touch target sizing for mobile (44x44px minimum)
- Typography scaling across breakpoints

**Decision Required**: Breakpoint values and responsive design conventions

### Research Output

**Deliverable**: `research.md` containing:
- Decisions made for each research question
- Rationale for technology choices
- Code examples or patterns to follow
- Links to documentation and best practices
- Trade-offs considered and rejected alternatives

**Completion Criteria**:
- All 7 research questions answered
- Technology choices documented with rationale
- No remaining "NEEDS CLARIFICATION" items for Phase 1

---

## Phase 1: Design & Contracts

**Responsible Agent**: Architecture Planner Agent (this agent)
**Prerequisites**: Phase 0 research complete
**Duration**: Design artifacts generation (no code)

### Objectives

1. Define frontend data model (types and interfaces)
2. Create API client contracts (expected request/response formats)
3. Define component interface contracts (props and behavior)
4. Document authentication flow from frontend perspective
5. Create quickstart guide for developers

### Design Tasks

#### D001: Generate data-model.md

**Content**:

##### TypeScript Interfaces

```typescript
// User (frontend perspective)
interface User {
  id: string
  email: string
  // Note: password never stored on frontend
}

// Task
interface Task {
  id: string
  title: string
  description?: string
  completed: boolean
  userId: string  // Owner reference
  createdAt: string  // ISO 8601
  updatedAt: string  // ISO 8601
}

// Authentication State
interface AuthState {
  isAuthenticated: boolean
  user: User | null
  token: string | null  // JWT
  loading: boolean
  error: string | null
}

// Task State
interface TaskState {
  tasks: Task[]
  loading: boolean
  error: string | null
}
```

##### Validation Rules

- **Email**: Standard RFC 5322 regex pattern
- **Password**: Minimum 8 characters, at least one uppercase, one lowercase, one number
- **Task Title**: Required, 1-200 characters, trimmed
- **Task Description**: Optional, 0-1000 characters

##### State Transitions

- **Authentication**: unauthenticated → loading → authenticated/error
- **Task List**: loading → loaded/error
- **Task Operations**: idle → pending → success/error (with optimistic UI)

**Completion Criteria**: data-model.md created with complete type definitions and validation rules

#### D002: Generate contracts/api-client.md

**Content**:

##### Base API Client Configuration

```typescript
// Base URL: /api (relative to frontend)
// Authentication: Bearer token in Authorization header
// Content-Type: application/json
// Timeout: 30 seconds
```

##### Expected Endpoints (Frontend Perspective)

**Authentication**:
- `POST /api/auth/signup` - Create account
  - Request: `{ email: string, password: string }`
  - Response: `{ message: string }` (success) or error
  - Status: 201 Created / 400 Bad Request / 409 Conflict

- `POST /api/auth/signin` - Authenticate user
  - Request: `{ email: string, password: string }`
  - Response: `{ token: string, user: User }`
  - Status: 200 OK / 401 Unauthorized

- `POST /api/auth/signout` - Sign out (optional, primarily client-side)
  - Request: None (JWT in header)
  - Response: `{ message: string }`
  - Status: 200 OK

**Tasks**:
- `GET /api/tasks` - Get all tasks for authenticated user
  - Response: `{ tasks: Task[] }`
  - Status: 200 OK / 401 Unauthorized

- `POST /api/tasks` - Create new task
  - Request: `{ title: string, description?: string }`
  - Response: `{ task: Task }`
  - Status: 201 Created / 400 Bad Request / 401 Unauthorized

- `PUT /api/tasks/:id` - Update task
  - Request: `{ title?: string, description?: string, completed?: boolean }`
  - Response: `{ task: Task }`
  - Status: 200 OK / 400 Bad Request / 401 Unauthorized / 404 Not Found

- `PATCH /api/tasks/:id/toggle` - Toggle completion status
  - Request: None (toggle current state)
  - Response: `{ task: Task }`
  - Status: 200 OK / 401 Unauthorized / 404 Not Found

- `DELETE /api/tasks/:id` - Delete task
  - Response: `{ message: string }`
  - Status: 200 OK / 401 Unauthorized / 404 Not Found

##### Error Response Format

```typescript
interface ErrorResponse {
  error: string          // Error message
  code?: string          // Error code (e.g., "INVALID_EMAIL")
  details?: any          // Additional error details
}
```

##### HTTP Status Code Handling

- **401 Unauthorized**: Redirect to sign-in, clear local token
- **403 Forbidden**: Show "Access denied" message
- **404 Not Found**: Show "Task not found" error
- **500 Internal Server Error**: Show generic error with retry option
- **Network Error**: Show "Connection failed" with retry option

**Completion Criteria**: API client contract documented with all expected endpoints and error handling

#### D003: Generate contracts/auth-flow.md

**Content**:

##### Sign Up Flow

1. User navigates to `/signup`
2. User fills email and password fields
3. Frontend validates email format and password strength
4. On submit: `POST /api/auth/signup`
5. Success: Redirect to `/signin` with success message
6. Error: Display error message in form

##### Sign In Flow

1. User navigates to `/signin`
2. User fills email and password fields
3. On submit: `POST /api/auth/signin`
4. Success:
   - Store JWT token in localStorage
   - Store user info in auth state
   - Redirect to `/dashboard`
5. Error: Display "Invalid credentials" message

##### JWT Token Management

- **Storage**: `localStorage.setItem('auth_token', token)`
- **Retrieval**: `localStorage.getItem('auth_token')`
- **Injection**: `Authorization: Bearer ${token}` header on all authenticated requests
- **Expiration**: Handle 401 responses by clearing token and redirecting to signin

##### Route Protection

- **Protected Routes**: `/dashboard/*`
- **Public Routes**: `/signup`, `/signin`
- **Implementation**: Middleware or layout-based auth check
- **Unauthenticated Access**: Redirect to `/signin`

##### Sign Out Flow

1. User clicks "Logout" button
2. Clear JWT token from localStorage
3. Clear user state
4. Redirect to `/signin`
5. Optional: Call `POST /api/auth/signout` (if backend invalidation needed)

**Completion Criteria**: Complete authentication flow documented from frontend perspective

#### D004: Generate contracts/component-props.md

**Content**: Define prop interfaces for all major components

**Example**:

```typescript
// TaskCard Component
interface TaskCardProps {
  task: Task
  onToggle: (taskId: string) => void
  onEdit: (task: Task) => void
  onDelete: (taskId: string) => void
  isLoading?: boolean
}

// TaskForm Component
interface TaskFormProps {
  mode: 'create' | 'edit'
  initialValues?: Partial<Task>
  onSubmit: (data: { title: string; description?: string }) => Promise<void>
  onCancel: () => void
  isSubmitting?: boolean
}

// AuthGuard Component
interface AuthGuardProps {
  children: React.ReactNode
  fallback?: React.ReactNode
}
```

**Completion Criteria**: Component contracts defined for all 10+ major components

#### D005: Generate quickstart.md

**Content**:

##### Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Git for version control

##### Setup Steps

1. Clone repository and checkout branch `001-frontend-ui`
2. Navigate to `frontend/` directory
3. Install dependencies: `npm install`
4. Copy `.env.example` to `.env.local`
5. Configure environment variables:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
   ```
6. Run development server: `npm run dev`
7. Open browser to `http://localhost:3000`

##### Development Workflow

1. Create feature branch from `001-frontend-ui`
2. Implement component or feature
3. Test locally with development server
4. Run linter: `npm run lint`
5. Run tests: `npm test`
6. Commit changes with descriptive message
7. Push to feature branch

##### Project Commands

- `npm run dev` - Start development server (port 3000)
- `npm run build` - Build production bundle
- `npm start` - Start production server
- `npm test` - Run Jest tests
- `npm run test:e2e` - Run Playwright E2E tests
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript compiler check

##### Key Files to Know

- `src/app/layout.tsx` - Root layout with providers
- `src/lib/api/client.ts` - API client with JWT
- `src/hooks/useAuth.ts` - Authentication hook
- `src/hooks/useTasks.ts` - Task management hook
- `tailwind.config.js` - Tailwind CSS configuration

**Completion Criteria**: Quickstart guide enables new developer to run frontend in under 10 minutes

#### D006: Update Agent Context

**Action**: Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude`

**Purpose**: Add Next.js, TypeScript, Tailwind, Better Auth technology context to agent knowledge base

**Completion Criteria**: Agent context file updated with new technologies from this plan

### Phase 1 Completion Checkpoint

**Validation**:
- [ ] data-model.md created with complete TypeScript interfaces
- [ ] contracts/api-client.md documents all expected endpoints
- [ ] contracts/auth-flow.md documents JWT authentication flow
- [ ] contracts/component-props.md defines component interfaces
- [ ] quickstart.md provides clear setup instructions
- [ ] Agent context updated successfully

**Gate**: ✅ All artifacts generated → Proceed to Phase 2 (handled by `/sp.tasks` command)

---

## Phase 2: Implementation Planning (via /sp.tasks)

**Note**: This phase is executed by the `/sp.tasks` command, NOT by `/sp.plan`.

**Purpose**: Convert design artifacts into granular, executable tasks with agent assignments.

**Expected Output**: `tasks.md` with:
- Detailed task breakdown per user story
- Agent assignments (Frontend Engineer, Integration Tester)
- Dependency chains
- Parallel execution opportunities
- Quality checkpoints

**Phases Expected in tasks.md**:
1. **Phase 1**: Setup & Dependencies (project init, npm packages)
2. **Phase 2**: Application Shell & Layout (root layout, routing structure)
3. **Phase 3**: Authentication UI (signup, signin, auth guards)
4. **Phase 4**: Core Task UI - View (dashboard, task list, task cards)
5. **Phase 5**: Core Task UI - Create (task form, modal, validation)
6. **Phase 6**: Core Task UI - Toggle (checkbox, optimistic UI, error recovery)
7. **Phase 7**: Core Task UI - Edit (edit form, pre-population)
8. **Phase 8**: Core Task UI - Delete (confirmation modal, deletion flow)
9. **Phase 9**: States & Error Handling (empty, loading, error states)
10. **Phase 10**: UX Polish & Responsiveness (mobile optimization, accessibility)
11. **Phase 11**: Integration Readiness (API client validation, JWT flow testing)

---

## Quality Checkpoints

### Checkpoint 1: Visual Consistency

**Trigger**: After implementing first 3 UI components
**Validation**:
- [ ] Consistent spacing (Tailwind spacing scale followed)
- [ ] Consistent color palette (defined in tailwind.config.js)
- [ ] Consistent typography (font sizes, weights, line heights)
- [ ] Consistent border radius and shadows

**Gate**: Must pass before proceeding to next component batch

### Checkpoint 2: Professional Look & Feel

**Trigger**: After implementing all authentication pages
**Validation**:
- [ ] No placeholder text or lorem ipsum
- [ ] Professional button styles and hover states
- [ ] Clean form layouts with proper labels
- [ ] Appropriate white space and visual breathing room
- [ ] No cluttered or cramped interfaces

**Gate**: Must pass before implementing task management UI

### Checkpoint 3: Accessibility

**Trigger**: After implementing all interactive components
**Validation**:
- [ ] Keyboard navigation works for all interactive elements
- [ ] Focus indicators visible on all focusable elements
- [ ] Sufficient color contrast (WCAG AA: 4.5:1 for text)
- [ ] Form inputs have associated labels
- [ ] Error messages announced to screen readers
- [ ] Modal traps focus appropriately

**Gate**: Must pass before responsive optimization

### Checkpoint 4: Responsiveness

**Trigger**: After implementing all pages and components
**Validation**:
- [ ] Mobile layout (320px-768px) displays correctly
- [ ] Tablet layout (769px-1024px) displays correctly
- [ ] Desktop layout (1025px+) displays correctly
- [ ] Touch targets minimum 44x44px on mobile
- [ ] No horizontal scroll at any breakpoint
- [ ] Typography scales appropriately
- [ ] Images/icons scale appropriately

**Gate**: Must pass before error handling implementation

### Checkpoint 5: Error Handling UX

**Trigger**: After implementing all error states
**Validation**:
- [ ] Network errors show clear "Connection failed" message with retry
- [ ] 401 errors redirect to sign-in with session expired message
- [ ] 403 errors show "Access denied" message
- [ ] Form validation errors display inline with clear messaging
- [ ] API errors show user-friendly messages (not technical details)
- [ ] Toast notifications appear for success/error operations
- [ ] Loading states prevent double submissions

**Gate**: Must pass before integration readiness testing

### Checkpoint 6: Integration Readiness

**Trigger**: After completing all frontend implementation
**Validation**:
- [ ] API client correctly adds JWT to Authorization header
- [ ] JWT token stored and retrieved from localStorage correctly
- [ ] Unauthenticated requests redirect to sign-in
- [ ] Loading states appear after 300ms delay
- [ ] Optimistic UI updates work correctly
- [ ] Error recovery (revert on API failure) works correctly
- [ ] All expected API endpoints called with correct payloads
- [ ] Response data correctly parsed and displayed

**Gate**: ✅ All checkpoints passed → Frontend ready for backend integration

---

## Integration Readiness Validation

**Responsible Agent**: Integration Tester Agent
**Prerequisites**: All Phase 2 tasks complete, all checkpoints passed

### Integration Tests

**IT001**: JWT Token Flow
- [ ] Sign up stores no token (correct)
- [ ] Sign in receives token from API
- [ ] Token stored in localStorage
- [ ] Token included in subsequent API calls
- [ ] Token cleared on sign out

**IT002**: API Request Formation
- [ ] GET /api/tasks called on dashboard load with JWT
- [ ] POST /api/tasks called with correct payload on task creation
- [ ] PUT /api/tasks/:id called with correct payload on task edit
- [ ] PATCH /api/tasks/:id/toggle called on checkbox click
- [ ] DELETE /api/tasks/:id called on delete confirmation

**IT003**: Response Handling
- [ ] Successful responses update UI correctly
- [ ] Error responses display user-friendly messages
- [ ] 401 responses trigger sign-in redirect
- [ ] Network errors show connectivity message
- [ ] Loading states display during API calls

**IT004**: Optimistic UI
- [ ] Task toggle updates UI immediately
- [ ] Task toggle reverts on API error
- [ ] Error toast shown on revert

**IT005**: State Management
- [ ] Authentication state persists across page refreshes
- [ ] Task list refreshes on dashboard navigation
- [ ] Created tasks appear in list immediately
- [ ] Updated tasks reflect changes in list
- [ ] Deleted tasks removed from list

### Manual Testing Scenarios

1. **Complete User Journey** (E2E test scenario):
   - Sign up with new account
   - Sign in with credentials
   - Create 3 tasks
   - Toggle 1 task to complete
   - Edit 1 task
   - Delete 1 task
   - Sign out
   - Sign in again
   - Verify tasks persisted (requires backend)

2. **Error Scenario Testing**:
   - Attempt sign in with invalid credentials
   - Attempt task creation with empty title
   - Simulate network disconnection during task creation
   - Simulate API slow response (>2 seconds)
   - Simulate session expiration (401 response)

3. **Responsiveness Testing**:
   - Test on iPhone SE (375px)
   - Test on iPad (768px)
   - Test on desktop (1920px)
   - Test landscape and portrait orientations

**Completion Criteria**:
- All integration tests pass
- Manual testing scenarios complete successfully
- No blocking issues identified
- Frontend is ready to connect to live backend API

---

## Risk Analysis

### Risk 1: Better Auth Integration Complexity

**Likelihood**: Medium
**Impact**: High
**Mitigation**:
- Complete thorough research in Phase 0
- Create isolated auth prototype before full implementation
- Allocate buffer time for auth debugging
- Document auth flow clearly in contracts

### Risk 2: API Contract Mismatch

**Likelihood**: Medium
**Impact**: Medium
**Mitigation**:
- Define clear API contracts in Phase 1
- Use TypeScript for request/response type safety
- Create mock API during frontend development
- Validate contracts with backend team before integration

### Risk 3: Performance with 1000 Tasks

**Likelihood**: Low
**Impact**: Medium
**Mitigation**:
- Implement pagination or virtual scrolling if needed
- Profile performance during development
- Add performance budget monitoring
- Optimize re-renders with React.memo if necessary

### Risk 4: Accessibility Compliance

**Likelihood**: Low
**Impact**: Medium
**Mitigation**:
- Use semantic HTML elements
- Test with keyboard navigation throughout development
- Use axe-core or similar tool for automated checks
- Include accessibility in all checkpoints

### Risk 5: Mobile UX Quality

**Likelihood**: Low
**Impact**: Medium
**Mitigation**:
- Test on real devices early and often
- Use mobile-first development approach
- Ensure touch targets meet 44x44px minimum
- Get user feedback on mobile experience

---

## Success Criteria

**Phase 0 Success**:
- ✅ All research questions answered
- ✅ Technology choices documented with rationale
- ✅ No remaining "NEEDS CLARIFICATION" items

**Phase 1 Success**:
- ✅ All design artifacts generated and complete
- ✅ Contracts define clear API expectations
- ✅ Quickstart guide enables rapid onboarding
- ✅ Agent context updated

**Phase 2 Success** (via /sp.tasks):
- ✅ Frontend implements all 55 functional requirements
- ✅ All 6 user stories fully functional
- ✅ All quality checkpoints passed
- ✅ Integration readiness validation complete
- ✅ Professional-grade UI delivered
- ✅ Ready for backend connection

---

## Next Steps

1. **Execute Phase 0**: Run research tasks (this command continues below)
2. **Execute Phase 1**: Generate design artifacts (this command continues below)
3. **Execute Phase 2**: Run `/sp.tasks` to generate implementation tasks
4. **Execute Implementation**: Frontend Engineer Agent implements per tasks.md
5. **Execute Validation**: Integration Tester Agent validates readiness
6. **Backend Integration**: Connect frontend to live FastAPI backend (separate plan)

**Command Status**: This `/sp.plan` command will now proceed to Phase 0 and Phase 1 generation.
