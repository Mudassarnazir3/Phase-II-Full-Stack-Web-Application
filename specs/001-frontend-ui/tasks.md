# Tasks: Frontend UI - Todo Web Application

**Input**: Design documents from `/specs/001-frontend-ui/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL - not included in this task list as they were not explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `frontend/src/` for application code
- Paths shown below follow the structure defined in plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Initialize Next.js 16+ project with TypeScript in frontend/ directory
- [x] T002 Install core dependencies (React 18+, Next.js, TypeScript, Tailwind CSS, Better Auth, Sonner)
- [x] T003 [P] Configure Tailwind CSS in frontend/tailwind.config.js with mobile-first breakpoints
- [x] T004 [P] Configure TypeScript in frontend/tsconfig.json with strict mode enabled
- [x] T005 [P] Configure Next.js in frontend/next.config.js per plan.md
- [x] T006 [P] Create frontend/src/styles/globals.css with Tailwind imports
- [x] T007 [P] Set up .env.example with NEXT_PUBLIC_API_URL and NEXT_PUBLIC_BETTER_AUTH_URL
- [x] T008 [P] Configure ESLint and Prettier for code quality

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T009 Create TypeScript type definitions in frontend/src/types/auth.ts (User, AuthState, SignUpFormData, SignInFormData per data-model.md)
- [x] T010 [P] Create TypeScript type definitions in frontend/src/types/task.ts (Task, TaskState, TaskFormData per data-model.md)
- [x] T011 [P] Create TypeScript type definitions in frontend/src/types/api.ts (ErrorResponse, ApiResponse per data-model.md)
- [x] T012 Implement API client wrapper in frontend/src/lib/api/client.ts with JWT injection and 401 handling per contracts/api-client.md
- [x] T013 [P] Implement JWT token utilities in frontend/src/lib/auth/token.ts (setAuthToken, getAuthToken, clearAuthToken per data-model.md)
- [x] T014 [P] Implement validation functions in frontend/src/lib/utils/validation.ts (validateEmail, validatePassword, validateTaskTitle per data-model.md)
- [x] T015 [P] Implement debounce utility in frontend/src/lib/utils/debounce.ts per research.md
- [x] T016 Create AuthContext provider in frontend/src/lib/auth/AuthProvider.tsx with signIn, signOut, and auth state management per contracts/auth-flow.md
- [x] T017 Create useAuth custom hook in frontend/src/hooks/useAuth.ts that consumes AuthContext per contracts/component-props.md
- [x] T018 Create root layout in frontend/src/app/layout.tsx with AuthProvider and Sonner Toaster
- [x] T019 Create base Button component in frontend/src/components/ui/Button.tsx with variants (primary, secondary, danger, ghost) per contracts/component-props.md
- [x] T020 [P] Create base Input component in frontend/src/components/ui/Input.tsx with label and error display per contracts/component-props.md
- [x] T021 [P] Create base Textarea component in frontend/src/components/ui/Textarea.tsx per contracts/component-props.md
- [x] T022 [P] Create Modal component in frontend/src/components/ui/Modal.tsx with focus trap per contracts/component-props.md
- [x] T023 [P] Create LoadingSpinner component in frontend/src/components/ui/LoadingSpinner.tsx per contracts/component-props.md

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Authentication Flow (Priority: P1) 🎯 MVP

**Goal**: Enable users to sign up, sign in, and sign out with JWT-based authentication

**Independent Test**: Complete signup with valid email/password, then sign in with those credentials and verify redirect to dashboard. Sign out and verify redirect to signin.

### Implementation for User Story 1

- [x] T024 [P] [US1] Implement Better Auth configuration (SKIPPED - using FastAPI backend directly)
- [x] T025 [P] [US1] Create auth API handlers (SKIPPED - using FastAPI backend directly)
- [x] T026 [P] [US1] Implement auth API functions in frontend/src/lib/api/auth.ts (signUp, signIn, signOut) per contracts/api-client.md
- [x] T027 [US1] Create SignUpForm component in frontend/src/components/auth/SignUpForm.tsx with email/password validation per contracts/component-props.md
- [x] T028 [US1] Create SignInForm component in frontend/src/components/auth/SignInForm.tsx with error handling per contracts/component-props.md
- [x] T029 [US1] Create AuthGuard component in frontend/src/components/auth/AuthGuard.tsx for route protection per contracts/component-props.md
- [x] T030 [US1] Create signup page in frontend/src/app/(auth)/signup/page.tsx using SignUpForm
- [x] T031 [US1] Create signin page in frontend/src/app/(auth)/signin/page.tsx using SignInForm
- [x] T032 [US1] Create landing page in frontend/src/app/page.tsx with redirect logic based on auth status
- [x] T033 [US1] Implement sign out functionality in dashboard (implemented in placeholder)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Users can sign up, sign in, and sign out.

---

## Phase 4: User Story 2 - View Task List (Priority: P1) 🎯 MVP

**Goal**: Display authenticated user's task list with loading, empty, and error states

**Independent Test**: Sign in and view dashboard with pre-populated tasks (requires backend). Verify loading skeleton appears, tasks display with correct styling, empty state shows when no tasks, errors display with retry option.

### Implementation for User Story 2

- [ ] T034 [P] [US2] Implement task API functions in frontend/src/lib/api/tasks.ts (getTasks per contracts/api-client.md)
- [ ] T035 [US2] Create useTasks custom hook in frontend/src/hooks/useTasks.ts with fetchTasks function per contracts/component-props.md
- [ ] T036 [P] [US2] Create TaskCard component in frontend/src/components/tasks/TaskCard.tsx displaying title, description, completed status per contracts/component-props.md
- [ ] T037 [US2] Create TaskList component in frontend/src/components/tasks/TaskList.tsx rendering array of TaskCard components per contracts/component-props.md
- [ ] T038 [P] [US2] Create TaskListSkeleton component in frontend/src/components/tasks/TaskSkeleton.tsx with pulse animation per contracts/component-props.md
- [ ] T039 [P] [US2] Create TaskEmpty component in frontend/src/components/tasks/TaskEmpty.tsx with "Create your first task" call-to-action per contracts/component-props.md
- [ ] T040 [US2] Create Header component in frontend/src/components/layout/Header.tsx with user email and logout button per contracts/component-props.md
- [ ] T041 [US2] Create dashboard layout in frontend/src/app/(dashboard)/layout.tsx with AuthGuard and Header
- [ ] T042 [US2] Create dashboard page in frontend/src/app/(dashboard)/dashboard/page.tsx displaying TaskList with loading/empty/error states
- [ ] T043 [US2] Implement 300ms loading delay pattern in dashboard page per research.md decision

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Users can authenticate and view their task list.

---

## Phase 5: User Story 3 - Create New Task (Priority: P2)

**Goal**: Enable users to create new tasks with title and optional description

**Independent Test**: Click "Create Task" button, fill in title and description in modal, submit, and verify new task appears in list with success toast.

### Implementation for User Story 3

- [ ] T044 [P] [US3] Add createTask function to frontend/src/lib/api/tasks.ts per contracts/api-client.md
- [ ] T045 [US3] Add createTask function to useTasks hook in frontend/src/hooks/useTasks.ts
- [ ] T046 [US3] Create TaskForm component in frontend/src/components/tasks/TaskForm.tsx with mode prop ('create' or 'edit') per contracts/component-props.md
- [ ] T047 [US3] Add title and description validation to TaskForm (1-200 chars for title, 0-1000 for description)
- [ ] T048 [US3] Add "Create Task" button to dashboard page
- [ ] T049 [US3] Add Modal with TaskForm in create mode to dashboard page
- [ ] T050 [US3] Implement form submission with API call and optimistic UI update
- [ ] T051 [US3] Add success toast notification after task creation
- [ ] T052 [US3] Implement form error handling with inline error display

**Checkpoint**: All user stories (US1, US2, US3) should now work independently. Users can create tasks.

---

## Phase 6: User Story 4 - Toggle Task Completion (Priority: P2)

**Goal**: Enable users to mark tasks as complete/incomplete via checkbox with optimistic UI

**Independent Test**: Click checkbox on incomplete task, verify immediate UI update (strikethrough, gray color), verify API call in background, test error reversion by simulating API failure.

### Implementation for User Story 4

- [ ] T053 [P] [US4] Add toggleTask function to frontend/src/lib/api/tasks.ts (PATCH /api/tasks/:id/toggle) per contracts/api-client.md
- [ ] T054 [US4] Add toggleTask function to useTasks hook with optimistic UI update and error reversion per contracts/api-client.md
- [ ] T055 [US4] Add checkbox to TaskCard component with onChange handler
- [ ] T056 [US4] Implement completed task styling in TaskCard (strikethrough text, muted color) per spec.md FR-011
- [ ] T057 [US4] Add debouncing to toggle function (500ms) to prevent rapid multiple API calls per research.md
- [ ] T058 [US4] Implement loading indicator on checkbox during API call
- [ ] T059 [US4] Implement error toast and UI reversion on toggle failure per contracts/api-client.md

**Checkpoint**: All implemented user stories (US1-US4) should work independently. Users can toggle task completion with optimistic UI.

---

## Phase 7: User Story 5 - Edit Existing Task (Priority: P3)

**Goal**: Enable users to edit task title and description

**Independent Test**: Click edit button on a task, modify title in modal form, save, and verify task updates in list with success toast.

### Implementation for User Story 5

- [ ] T060 [P] [US5] Add updateTask function to frontend/src/lib/api/tasks.ts (PUT /api/tasks/:id) per contracts/api-client.md
- [ ] T061 [US5] Add updateTask function to useTasks hook in frontend/src/hooks/useTasks.ts
- [ ] T062 [US5] Add edit button to TaskCard component
- [ ] T063 [US5] Add state management for edit modal in dashboard page
- [ ] T064 [US5] Render TaskForm in edit mode with initialValues pre-populated
- [ ] T065 [US5] Implement save functionality with API call and list update
- [ ] T066 [US5] Add cancel functionality to close modal without saving
- [ ] T067 [US5] Add success toast notification after task update
- [ ] T068 [US5] Implement error handling for update failures

**Checkpoint**: All implemented user stories (US1-US5) should work independently. Users can edit existing tasks.

---

## Phase 8: User Story 6 - Delete Task (Priority: P3)

**Goal**: Enable users to delete tasks with confirmation modal

**Independent Test**: Click delete button on a task, confirm deletion in modal, verify task removed from list with success toast. Cancel deletion and verify task remains.

### Implementation for User Story 6

- [ ] T069 [P] [US6] Add deleteTask function to frontend/src/lib/api/tasks.ts (DELETE /api/tasks/:id) per contracts/api-client.md
- [ ] T070 [US6] Add deleteTask function to useTasks hook in frontend/src/hooks/useTasks.ts
- [ ] T071 [US6] Create DeleteConfirmationModal component in frontend/src/components/tasks/DeleteConfirmationModal.tsx per contracts/component-props.md
- [ ] T072 [US6] Add delete button to TaskCard component
- [ ] T073 [US6] Add state management for delete confirmation modal in dashboard page
- [ ] T074 [US6] Implement delete confirmation with task title display in modal
- [ ] T075 [US6] Implement delete functionality with optimistic UI update (remove from list immediately)
- [ ] T076 [US6] Add success toast notification after task deletion
- [ ] T077 [US6] Implement error handling to re-add task to list on deletion failure
- [ ] T078 [US6] Handle empty state display when last task is deleted

**Checkpoint**: All user stories (US1-US6) should now be independently functional. Complete CRUD operations available.

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T079 [P] Implement responsive mobile layout (320px-768px) with touch-friendly targets (44x44px) per spec.md FR-045, FR-048
- [ ] T080 [P] Implement responsive tablet layout (769px-1024px) per spec.md FR-046
- [ ] T081 [P] Implement responsive desktop layout (1025px+) per spec.md FR-047
- [ ] T082 [P] Add keyboard navigation support to all interactive elements per spec.md FR-053
- [ ] T083 [P] Add visible focus indicators to all focusable elements per spec.md FR-054
- [ ] T084 [P] Verify WCAG AA color contrast (4.5:1) across all components per spec.md FR-052
- [ ] T085 [P] Add ARIA labels and screen reader announcements for form errors per spec.md FR-044
- [ ] T086 Test application on mobile devices (iPhone SE 375px, iPad 768px) per manual testing scenarios
- [ ] T087 [P] Profile performance and optimize re-renders with React.memo if needed per plan.md Risk 3
- [ ] T088 [P] Add error boundary components for graceful error handling
- [ ] T089 Verify all success criteria from spec.md (SC-001 through SC-010)
- [ ] T090 Run accessibility audit with axe-core or similar tool

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P1 → P2 → P2 → P3 → P3)
- **Polish (Phase 9)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Depends on US1 (needs Header with logout from US1 for completion) - Can start US2 tasks in parallel with US1 but Header integration needs US1 complete
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Uses TaskForm and Modal from US2 but independently testable
- **User Story 4 (P2)**: Depends on US2 (needs TaskCard to add checkbox) - Extends TaskCard from US2
- **User Story 5 (P3)**: Depends on US2 and US3 (needs TaskCard and TaskForm) - Extends components from previous stories
- **User Story 6 (P3)**: Depends on US2 (needs TaskCard to add delete button) - Extends TaskCard from US2

### Within Each User Story

- API functions before hooks
- Hooks before components that use them
- Base components before composite components
- Components before pages that use them
- Core implementation before error handling

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- User Stories 1 and parts of US2 can start in parallel (different files)
- Once US2 complete, US3, US4, US5, US6 can partially overlap (different components)
- All Polish tasks marked [P] can run in parallel

---

## Parallel Example: Foundational Phase

```bash
# Launch all type definition tasks together:
Task T009: "Create auth types in frontend/src/types/auth.ts"
Task T010: "Create task types in frontend/src/types/task.ts"
Task T011: "Create API types in frontend/src/types/api.ts"

# Launch all utility tasks together (after types):
Task T013: "JWT token utilities in frontend/src/lib/auth/token.ts"
Task T014: "Validation functions in frontend/src/lib/utils/validation.ts"
Task T015: "Debounce utility in frontend/src/lib/utils/debounce.ts"

# Launch all base UI component tasks together (after Button):
Task T020: "Input component in frontend/src/components/ui/Input.tsx"
Task T021: "Textarea component in frontend/src/components/ui/Textarea.tsx"
Task T022: "Modal component in frontend/src/components/ui/Modal.tsx"
Task T023: "LoadingSpinner component in frontend/src/components/ui/LoadingSpinner.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 + User Story 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Authentication)
4. Complete Phase 4: User Story 2 (View Tasks)
5. **STOP and VALIDATE**: Test authentication + view tasks flow end-to-end
6. Deploy/demo if ready - **This is a functional MVP!**

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (Auth) → Test independently → Basic app ready
3. Add User Story 2 (View) → Test independently → Deploy/Demo (MVP!)
4. Add User Story 3 (Create) → Test independently → Deploy/Demo
5. Add User Story 4 (Toggle) → Test independently → Deploy/Demo
6. Add User Story 5 (Edit) → Test independently → Deploy/Demo
7. Add User Story 6 (Delete) → Test independently → Deploy/Demo
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Auth)
   - Developer B: Start User Story 2 (View) base components
3. After US1 complete:
   - Developer A: User Story 3 (Create)
   - Developer B: Complete User Story 2 (View)
4. After US2 complete:
   - Developer A: Continue US3
   - Developer B: User Story 4 (Toggle)
   - Developer C: User Story 5 (Edit)
5. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies on incomplete work
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Tests not included as they were not explicitly requested in spec
- All tasks reference exact file paths per plan.md structure
- Frontend-only scope - backend API integration validated but not implemented here

---

## Task Count Summary

- **Phase 1 (Setup)**: 8 tasks
- **Phase 2 (Foundational)**: 15 tasks (BLOCKING)
- **Phase 3 (US1 - Auth)**: 10 tasks
- **Phase 4 (US2 - View)**: 10 tasks
- **Phase 5 (US3 - Create)**: 9 tasks
- **Phase 6 (US4 - Toggle)**: 7 tasks
- **Phase 7 (US5 - Edit)**: 9 tasks
- **Phase 8 (US6 - Delete)**: 10 tasks
- **Phase 9 (Polish)**: 12 tasks

**Total**: 90 tasks

**MVP Scope**: Phases 1-4 (43 tasks) delivers functional authentication + view tasks

**Parallel Opportunities**: 35 tasks marked [P] can run in parallel within their phase constraints
