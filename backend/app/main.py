"""
FastAPI Application - Phase II Todo Application

Main entry point with CORS, error handling, and router registration.
"""

import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from json import JSONDecodeError

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import get_settings
from app.db.init import init_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events - startup and shutdown."""
    # Startup
    logger.info("Starting backend application...")
    try:
        await init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        # Don't raise - allow app to start, db might be initialized separately
    yield
    # Shutdown
    logger.info("Shutting down backend application...")


# Create FastAPI application
app = FastAPI(
    title="Todo API - Phase II",
    description="Backend API for Phase II Todo Full-Stack Web Application",
    version="1.0.0",
    lifespan=lifespan,
)

# Get settings for CORS configuration
try:
    settings = get_settings()
    frontend_url = settings.better_auth_url
except Exception:
    # Allow app to load even without .env for testing
    frontend_url = "http://localhost:3000"

# Configure CORS middleware (FR-001, api-endpoints.md)
cors_origins = [frontend_url, "http://localhost:3000"]
# Filter out duplicates and empty strings
cors_origins = list(set(o for o in cors_origins if o))

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


# Security headers middleware (T019)
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add security headers to all responses."""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response


# === Exception Handlers (FR-029 to FR-034) ===


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle Pydantic validation errors (FR-030).

    Converts validation errors to user-friendly messages.
    """
    errors = exc.errors()

    # Extract first error message for user-friendly response
    if errors:
        first_error = errors[0]
        loc = first_error.get("loc", [])
        msg = first_error.get("msg", "Validation error")

        # Format field path
        field = ".".join(str(l) for l in loc if l != "body")

        if "title" in field.lower():
            if "required" in msg.lower() or "missing" in msg.lower():
                error_msg = "Title is required"
            elif "empty" in msg.lower():
                error_msg = "Title cannot be empty"
            else:
                error_msg = "Title must be 200 characters or less"
        elif "description" in field.lower():
            error_msg = "Description must be 1000 characters or less"
        else:
            error_msg = msg
    else:
        error_msg = "Validation error"

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": error_msg, "code": "VALIDATION_ERROR"},
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Handle HTTP exceptions - pass through with consistent format.
    """
    detail = exc.detail

    # If detail is already our format, use it
    if isinstance(detail, dict) and "error" in detail:
        return JSONResponse(
            status_code=exc.status_code,
            content=detail,
        )

    # Otherwise, format it
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": str(detail), "code": "ERROR"},
    )


@app.exception_handler(JSONDecodeError)
async def json_decode_exception_handler(request: Request, exc: JSONDecodeError):
    """
    Handle malformed JSON in request body (T018, FR-030).
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "Invalid request body", "code": "INVALID_REQUEST"},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """
    Handle unexpected exceptions (FR-033, FR-034).

    Logs full error server-side, returns generic message to client.
    Never exposes stack traces or internal details.
    """
    logger.exception(f"Unexpected error: {exc}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal server error", "code": "INTERNAL_ERROR"},
    )


# === Health Check Endpoint (T008) ===


@app.get("/api/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring.

    Returns 200 if application is running.
    Does not verify database connection (fast response).
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }


# === Router Registration ===

# Import and register routers after app creation to avoid circular imports
from app.routers.tasks import router as tasks_router  # noqa: E402

app.include_router(tasks_router, prefix="/api", tags=["Tasks"])
