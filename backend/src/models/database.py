"""
SQLAlchemy ORM models for Living Textbook RAG Backend.
Defines all database entities and their relationships.
"""

from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean, ForeignKey, JSON, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

Base = declarative_base()


def generate_id() -> str:
    """Generate a UUID string."""
    return str(uuid.uuid4())


class Chapter(Base):
    """
    Represents a chapter in the textbook.
    Each chapter is indexed 1-16 across 4 modules with 4 chapters per module.
    """

    __tablename__ = "chapters"

    id: str = Column(String(36), primary_key=True, default=generate_id)
    index: int = Column(Integer, unique=True, nullable=False, index=True)
    title: str = Column(String(255), nullable=False)
    module: int = Column(Integer, nullable=False)
    part: int = Column(Integer, nullable=False)
    learning_objectives: list = Column(JSON, nullable=False, default=list)
    keywords: list = Column(JSON, nullable=False, default=list)
    prerequisites: list = Column(JSON, nullable=False, default=list)
    created_at: datetime = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    chunks = relationship("ChunkVector", back_populates="chapter", cascade="all, delete-orphan")
    ingestion_logs = relationship("IngestionLog", back_populates="chapter", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_chapter_module_part", "module", "part"),
    )


class ChunkVector(Base):
    """
    Represents a semantic chunk of text with its embedding.
    Each chapter is chunked into 200-500 token pieces with overlap.
    """

    __tablename__ = "chunk_vectors"

    id: str = Column(String(36), primary_key=True, default=generate_id)
    chapter_id: str = Column(String(36), ForeignKey("chapters.id"), nullable=False, index=True)
    chunk_index: int = Column(Integer, nullable=False)
    content: str = Column(Text, nullable=False)
    embedding: list = Column(JSON, nullable=False)
    token_count: int = Column(Integer, nullable=False)
    created_at: datetime = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    chapter = relationship("Chapter", back_populates="chunks")

    __table_args__ = (
        Index("idx_chunk_chapter_index", "chapter_id", "chunk_index"),
    )


class ChatSession(Base):
    """
    Represents a user's chat session.
    Sessions persist across multiple messages to maintain conversation history.
    Sessions timeout after configurable duration (default 24 hours).
    """

    __tablename__ = "chat_sessions"

    id: str = Column(String(36), primary_key=True, default=generate_id)
    user_id: str = Column(String(255), nullable=True, index=True)
    chapter_context: int = Column(Integer, nullable=True)
    is_active: bool = Column(Boolean, nullable=False, default=True)
    message_count: int = Column(Integer, nullable=False, default=0)
    created_at: datetime = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), index=True)
    updated_at: datetime = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), index=True)
    last_activity_at: datetime = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    # Relationships
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_session_user_active", "user_id", "is_active"),
    )


class ChatMessage(Base):
    """
    Represents a single message in a chat session.
    Stores both user queries and AI responses with source references.
    """

    __tablename__ = "chat_messages"

    id: str = Column(String(36), primary_key=True, default=generate_id)
    session_id: str = Column(String(36), ForeignKey("chat_sessions.id"), nullable=False, index=True)
    role: str = Column(String(10), nullable=False)  # "user" or "assistant"
    content: str = Column(Text, nullable=False)
    highlighted_context: str = Column(Text, nullable=True)
    source_chunks: list = Column(JSON, nullable=True, default=list)
    confidence: float = Column(Float, nullable=True)
    created_at: datetime = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), index=True)

    # Relationships
    session = relationship("ChatSession", back_populates="messages")

    __table_args__ = (
        Index("idx_message_session_role", "session_id", "role"),
    )


class IngestionLog(Base):
    """
    Audit log for content ingestion operations.
    Tracks when chapters are ingested, updated, or failed.
    """

    __tablename__ = "ingestion_logs"

    id: str = Column(String(36), primary_key=True, default=generate_id)
    chapter_id: str = Column(String(36), ForeignKey("chapters.id"), nullable=False, index=True)
    status: str = Column(String(20), nullable=False)  # "success", "partial", "failed"
    chunks_created: int = Column(Integer, nullable=False, default=0)
    error_message: str = Column(Text, nullable=True)
    duration_seconds: float = Column(Float, nullable=True)
    created_at: datetime = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), index=True)

    # Relationships
    chapter = relationship("Chapter", back_populates="ingestion_logs")

    __table_args__ = (
        Index("idx_ingestion_chapter_status", "chapter_id", "status"),
    )
