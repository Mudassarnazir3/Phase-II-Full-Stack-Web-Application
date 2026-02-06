# Backend API - Phase II Todo Application

FastAPI backend for the Todo web application with JWT authentication and PostgreSQL storage.

## Requirements

- Python 3.11+
- Neon PostgreSQL database

## Setup

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your values:
   # - DATABASE_URL: Neon PostgreSQL connection string
   # - BETTER_AUTH_SECRET: Shared secret with frontend
   # - BETTER_AUTH_URL: Frontend URL for CORS
   ```

## Running

**Development server**:
```bash
uvicorn app.main:app --reload --port 8000
```

**Production**:
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

API docs available at `http://localhost:8000/docs`.

## API Endpoints

### Authentication

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/auth/signup` | No | Register new user |
| POST | `/api/auth/signin` | No | Authenticate, returns JWT |
| POST | `/api/auth/signout` | No | Sign out (stateless) |

### Tasks

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/tasks` | Yes | List user's tasks |
| POST | `/api/tasks` | Yes | Create new task |
| GET | `/api/tasks/{id}` | Yes | Get task by ID |
| PUT | `/api/tasks/{id}` | Yes | Update task |
| PATCH | `/api/tasks/{id}/toggle` | Yes | Toggle completion |
| DELETE | `/api/tasks/{id}` | Yes | Delete task |

### Health

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/health` | No | Health check |

All task endpoints require `Authorization: Bearer <token>` header.

## Testing

Tests use in-memory SQLite - no database required.

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=app --cov-report=term-missing

# Run specific test file
python -m pytest tests/test_security.py -v
```

## Project Structure

```
backend/
  app/
    main.py           # FastAPI app, middleware, error handlers
    config.py          # Environment configuration
    dependencies.py    # DI for auth and database
    db/
      init.py          # Database initialization
      session.py       # Async session management
    models/
      task.py          # SQLModel Task entity
      user.py          # SQLModel User entity
    routers/
      tasks.py         # Task CRUD endpoints
      auth.py          # Authentication endpoints
    schemas/
      task.py          # Task request/response schemas
      auth.py          # Auth request/response schemas
  tests/
    conftest.py        # Test fixtures
    test_auth.py       # JWT authentication tests
    test_tasks.py      # Task CRUD tests
    test_security.py   # User isolation & CORS tests
    test_validation.py # Input validation tests
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `BETTER_AUTH_SECRET` | Yes | JWT signing secret (shared with frontend) |
| `BETTER_AUTH_URL` | No | Frontend URL for CORS (default: http://localhost:3000) |
