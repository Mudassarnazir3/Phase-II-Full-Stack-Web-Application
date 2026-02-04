# Quickstart: Backend API - Todo Web Application

**Feature Branch**: `002-backend-api`
**Created**: 2026-01-16

## Prerequisites

- Python 3.11+
- Neon PostgreSQL database (provisioned)
- Better Auth secret (shared with frontend)

---

## Environment Setup

### Required Environment Variables

Create a `.env` file in the backend directory:

```env
DATABASE_URL=postgresql+asyncpg://user:password@host.neon.tech/database?sslmode=require
BETTER_AUTH_SECRET=your-shared-secret-with-frontend
BETTER_AUTH_URL=http://localhost:3000
```

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | Neon PostgreSQL connection string with `asyncpg` driver |
| `BETTER_AUTH_SECRET` | Shared secret for JWT verification (same as frontend) |
| `BETTER_AUTH_URL` | Frontend URL for CORS configuration |

**Critical**: The backend will refuse to start if these variables are missing.

---

## Installation

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Key Dependencies

| Package | Purpose |
|---------|---------|
| `fastapi` | Web framework |
| `uvicorn` | ASGI server |
| `sqlmodel` | ORM (SQLAlchemy + Pydantic) |
| `asyncpg` | Async PostgreSQL driver |
| `pyjwt` | JWT verification |
| `python-dotenv` | Environment variable loading |

---

## Database Setup

### Run Migrations

```bash
# Create tables (run once)
python -m app.db.init
```

This creates the `tasks` table with:
- UUID primary key
- user_id index for query performance
- Timestamp columns with UTC defaults

---

## Running the Server

### Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Server runs at: `http://localhost:8000`

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## Verify Installation

### Health Check

```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2026-01-16T10:30:00Z"
}
```

### API Documentation

FastAPI auto-generates interactive docs:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Testing API Endpoints

### Authenticated Request Example

```bash
# Replace <JWT_TOKEN> with a valid token from Better Auth
curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json"
```

### Create Task Example

```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"title": "My first task", "description": "Optional description"}'
```

---

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── config.py            # Environment configuration
│   ├── dependencies.py      # FastAPI dependencies (auth, db)
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py          # Task SQLModel
│   ├── routers/
│   │   ├── __init__.py
│   │   └── tasks.py         # Task API routes
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── task.py          # Request/Response Pydantic models
│   └── db/
│       ├── __init__.py
│       └── session.py       # Database session management
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── test_auth.py         # Authentication tests
│   └── test_tasks.py        # Task endpoint tests
├── requirements.txt
├── .env.example
└── README.md
```

---

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_tasks.py

# Run with verbose output
pytest -v
```

---

## Troubleshooting

### "Missing required environment variable"

Ensure `.env` file exists and contains all required variables.

### "Connection refused" to database

1. Check DATABASE_URL is correct
2. Verify Neon database is accessible
3. Ensure SSL mode is enabled (`?sslmode=require`)

### "Invalid token" errors

1. Verify BETTER_AUTH_SECRET matches frontend configuration
2. Check token is not expired
3. Ensure Authorization header uses Bearer scheme

### CORS errors from frontend

1. Check BETTER_AUTH_URL points to correct frontend origin
2. Verify CORS middleware is configured in main.py

---

## Next Steps

1. Run `/sp.tasks` to generate implementation tasks
2. Implement in order: config → models → dependencies → routers
3. Test each component before moving to next
4. Run integration tests after all components complete
