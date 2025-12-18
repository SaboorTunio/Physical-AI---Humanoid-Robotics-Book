"""
Database connection management for Living Textbook RAG Backend.
Provides AsyncSession factory and engine initialization with connection pooling.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool, QueuePool
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import logging

from src.config import settings
from src.models.database import Base

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """
    Manages database connection lifecycle.
    Provides async session factory with connection pooling.
    """

    def __init__(self):
        """Initialize database connection with configuration from settings."""
        self.engine = None
        self.SessionLocal = None
        self._initialized = False

    def init_engine(self):
        """
        Initialize SQLAlchemy async engine with connection pooling.
        Uses asyncpg for async PostgreSQL driver.
        """
        if self._initialized:
            logger.warning("Engine already initialized")
            return

        # Convert postgresql:// to postgresql+asyncpg:// for async driver
        db_url = settings.database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

        # Configure connection pool based on environment
        if settings.environment == "production":
            poolclass = QueuePool
            pool_size = settings.database_pool_size
            max_overflow = settings.database_max_overflow
        else:
            # Use NullPool in development to avoid connection issues
            poolclass = NullPool
            pool_size = 1
            max_overflow = 0

        self.engine = create_async_engine(
            db_url,
            echo=settings.debug,
            poolclass=poolclass,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_pre_ping=settings.database_pool_pre_ping,
            pool_recycle=3600,  # Recycle connections after 1 hour
        )

        self.SessionLocal = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )

        self._initialized = True
        logger.info(f"Database engine initialized: {settings.environment} mode")

    async def close_engine(self):
        """Close all database connections."""
        if self.engine:
            await self.engine.dispose()
            logger.info("Database engine closed")

    async def create_all_tables(self):
        """
        Create all database tables defined in ORM models.
        Used for initial setup and testing.
        """
        if not self._initialized or not self.engine:
            raise RuntimeError("Engine not initialized. Call init_engine() first.")

        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("All database tables created")

    async def drop_all_tables(self):
        """
        Drop all database tables.
        Used for testing and development cleanup.
        WARNING: This is destructive and should only be used in development.
        """
        if not self._initialized or not self.engine:
            raise RuntimeError("Engine not initialized. Call init_engine() first.")

        if settings.environment == "production":
            raise RuntimeError("Cannot drop tables in production environment")

        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            logger.warning("All database tables dropped")

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Context manager for database sessions.
        Automatically handles commit/rollback.

        Yields:
            AsyncSession instance

        Raises:
            RuntimeError: If SessionLocal not initialized
        """
        if not self.SessionLocal:
            raise RuntimeError("SessionLocal not initialized. Call init_engine() first.")

        session = self.SessionLocal()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def get_db_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        FastAPI dependency for database sessions.
        Used as a dependency in route handlers.

        Yields:
            AsyncSession instance
        """
        if not self.SessionLocal:
            raise RuntimeError("SessionLocal not initialized. Call init_engine() first.")

        session = self.SessionLocal()
        try:
            yield session
        finally:
            await session.close()


# Global database connection instance
db = DatabaseConnection()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency function for database sessions.
    Yields an async session for use in route handlers.

    Yields:
        AsyncSession instance
    """
    async for session in db.get_db_session():
        yield session
