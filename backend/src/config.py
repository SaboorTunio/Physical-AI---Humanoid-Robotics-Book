"""
Configuration management for Living Textbook RAG Backend.
Centralizes environment variable loading and validation using Pydantic.
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Uses pydantic-settings for validation and type coercion.
    """

    # Application Settings
    environment: str = "development"
    port: int = 8000
    debug: bool = False

    # CORS Configuration
    cors_allowed_origins: str = "http://localhost:3000,http://localhost:8000"

    # OpenAI Configuration
    openai_api_key: str = ""
    openai_model: str = "gpt-4-turbo-preview"
    openai_embedding_model: str = "text-embedding-3-small"
    openai_max_tokens: int = 2000

    # Qdrant Configuration
    qdrant_url: str = "https://localhost:6333"
    qdrant_api_key: str = ""
    qdrant_collection_name: str = "living_textbook"
    qdrant_vector_size: int = 1536

    # Neon Postgres Configuration
    database_url: str = "postgresql://user:password@localhost/living_textbook"
    database_pool_size: int = 5
    database_max_overflow: int = 10
    database_pool_pre_ping: bool = True

    # Rate Limiting
    rate_limit_queries_per_hour: int = 100
    rate_limit_ingest_per_day: int = 10

    # Admin Authentication
    admin_token: str = ""

    # Chunking Configuration
    chunk_size: int = 500  # tokens per chunk
    chunk_overlap: int = 100  # tokens overlap between chunks

    # Session Configuration
    session_timeout_hours: int = 24

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


def validate_settings() -> tuple[bool, list[str]]:
    """
    Validate critical settings are properly configured.

    Returns:
        Tuple of (is_valid, list of error messages)
    """
    errors = []

    # Validate required fields for production
    if settings.environment == "production":
        if not settings.openai_api_key:
            errors.append("OPENAI_API_KEY not configured")
        if not settings.qdrant_api_key:
            errors.append("QDRANT_API_KEY not configured")
        if not settings.admin_token:
            errors.append("ADMIN_TOKEN not configured")

    # Validate database URL format
    if not settings.database_url.startswith("postgresql://"):
        errors.append("DATABASE_URL must start with 'postgresql://'")

    # Validate Qdrant URL format
    if not settings.qdrant_url.startswith("https://") and settings.environment == "production":
        errors.append("QDRANT_URL should use HTTPS in production")

    # Validate numeric ranges
    if settings.chunk_size < 100 or settings.chunk_size > 2000:
        errors.append("CHUNK_SIZE must be between 100 and 2000 tokens")

    if settings.chunk_overlap >= settings.chunk_size:
        errors.append("CHUNK_OVERLAP must be less than CHUNK_SIZE")

    return len(errors) == 0, errors


def get_settings() -> Settings:
    """
    Get the global settings instance.
    Can be used for dependency injection in FastAPI.

    Returns:
        Settings instance with all configuration values
    """
    return settings
