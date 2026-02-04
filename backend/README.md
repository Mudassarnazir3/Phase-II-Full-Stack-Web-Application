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
   pip install -r requirements-dev.txt  # For testing
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
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check (no auth required) |
| GET | `/api/tasks` | List user's tasks |
| POST | `/api/tasks` | Create new task |
| GET | `/api/tasks/{id}` | Get task by ID |
| PUT | `/api/tasks/{id}` | Update task |
| PATCH | `/api/tasks/{id}/toggle` | Toggle completion |
| DELETE | `/api/tasks/{id}` | Delete task |

All endpoints except `/api/health` require JWT authentication via `Authorization: Bearer <token>` header.

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=term-missing

# Run specific test file
pytest tests/test_auth.py -v
```

## Project Structure

```
backend/
├── app/
│   ├── main.py           # FastAPI app, middleware, error handlers
│   ├── config.py         # Environment configuration
│   ├── dependencies.py   # DI for auth and database
│   ├── db/
│   │   ├── init.py       # Database initialization
│   │   └── session.py    # Async session management
│   ├── models/
│   │   └── task.py       # SQLModel Task entity
│   ├── routers/
│   │   └── tasks.py      # Task CRUD endpoints
│   └── schemas/
│       └── task.py       # Pydantic request/response schemas
└── tests/
    ├── conftest.py       # Test fixtures
    ├── test_auth.py      # JWT authentication tests
    ├── test_tasks.py     # Task CRUD tests
    ├── test_security.py  # User isolation tests
    └── test_validation.py # Input validation tests
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `BETTER_AUTH_SECRET` | Yes | JWT signing secret (shared with frontend) |
| `BETTER_AUTH_URL` | No | Frontend URL for CORS (default: http://localhost:3000) |
