"""
Configuration Management - Phase II Todo Application

Loads and validates environment variables at startup.
Application fails fast if required variables are missing (FR-006).
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database connection (FR-023)
    database_url: str

    # JWT verification secret (FR-008)
    better_auth_secret: str

    # Frontend URL for CORS
    better_auth_url: str = "http://localhost:3000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    """
    Get cached application settings.

    Raises ValidationError if required environment variables are missing.
    This implements FR-006: fail to start if required env vars missing.
    """
    return Settings()
