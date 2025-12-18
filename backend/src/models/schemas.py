"""
Pydantic schemas for request/response validation.
Defines data models for all API endpoints.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ============================================================================
# Chat Endpoint Schemas
# ============================================================================

class ChatRequest(BaseModel):
    """Request schema for POST /api/chat endpoint."""

    query: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="The question about the textbook content"
    )
    session_id: Optional[str] = Field(
        None,
        description="Optional session ID for conversation history"
    )
    highlighted_context: Optional[str] = Field(
        None,
        description="Optional highlighted text from the textbook"
    )
    chapter_context: Optional[int] = Field(
        None,
        description="Optional chapter index for context"
    )


class ChatResponseSource(BaseModel):
    """Source document for chat response."""

    chapter_index: int = Field(..., description="Chapter index")
    chapter_title: str = Field(..., description="Chapter title")
    section: str = Field(..., description="Section within chapter")
    excerpt: str = Field(..., description="Relevant text excerpt")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")


class ChatResponse(BaseModel):
    """Response schema for POST /api/chat endpoint."""

    session_id: str = Field(..., description="Session ID for tracking conversation")
    answer: str = Field(..., description="AI-generated answer")
    sources: List[ChatResponseSource] = Field(..., description="Source references")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Overall confidence score")
    timestamp: datetime = Field(..., description="Response timestamp")
    message_id: str = Field(..., description="Unique message identifier")


# ============================================================================
# Ingest Endpoint Schemas
# ============================================================================

class IngestRequest(BaseModel):
    """Request schema for POST /api/ingest endpoint."""

    force_refresh: bool = Field(
        False,
        description="Force re-ingest all chapters"
    )


class IngestChapterResult(BaseModel):
    """Result for a single chapter ingestion."""

    chapter_index: int = Field(..., description="Chapter index")
    title: str = Field(..., description="Chapter title")
    chunks_created: int = Field(..., description="Number of chunks created")
    status: str = Field(..., description="Status: success or error")
    error_message: Optional[str] = Field(None, description="Error message if failed")


class IngestResponse(BaseModel):
    """Response schema for POST /api/ingest endpoint."""

    status: str = Field(..., description="Overall status: success or partial")
    chapters_processed: int = Field(..., description="Number of chapters processed")
    chunks_created: int = Field(..., description="Total chunks created")
    results: List[IngestChapterResult] = Field(..., description="Per-chapter results")
    timestamp: datetime = Field(..., description="Ingest completion timestamp")


# ============================================================================
# Health Endpoint Schemas
# ============================================================================

class ServiceStatus(BaseModel):
    """Status of a single service."""

    name: str = Field(..., description="Service name")
    status: str = Field(..., description="Status: ok, degraded, or error")
    latency_ms: Optional[float] = Field(None, description="Response latency in ms")
    message: Optional[str] = Field(None, description="Status message")


class HealthResponse(BaseModel):
    """Response schema for GET /api/health endpoint."""

    status: str = Field(..., description="Overall status: healthy or unhealthy")
    services: List[ServiceStatus] = Field(..., description="Status of each service")
    version: str = Field(..., description="API version")
    timestamp: datetime = Field(..., description="Health check timestamp")


# ============================================================================
# Metadata Endpoint Schemas
# ============================================================================

class ChapterMetadata(BaseModel):
    """Metadata for a single chapter."""

    chapter_index: int = Field(..., description="Chapter index (1-16)")
    title: str = Field(..., description="Chapter title")
    module: int = Field(..., description="Module number (1-4)")
    part: int = Field(..., description="Part within module (1-4)")
    learning_objectives: List[str] = Field(..., description="Learning objectives")
    keywords: List[str] = Field(..., description="Related keywords")
    prerequisites: List[int] = Field(default_factory=list, description="Prerequisite chapter indices")
    chunks_count: int = Field(..., description="Number of chunks for this chapter")


class MetadataResponse(BaseModel):
    """Response schema for GET /api/metadata endpoint."""

    chapters: List[ChapterMetadata] = Field(..., description="All chapter metadata")
    total_chapters: int = Field(..., description="Total number of chapters")
    total_chunks: int = Field(..., description="Total number of chunks")
    modules: int = Field(..., description="Number of modules")
    last_updated: datetime = Field(..., description="Last update timestamp")


# ============================================================================
# Error Response Schemas
# ============================================================================

class ErrorDetail(BaseModel):
    """Detailed error information."""

    code: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional details")


class ErrorResponse(BaseModel):
    """Standard error response."""

    error: ErrorDetail = Field(..., description="Error details")
    timestamp: datetime = Field(..., description="Error timestamp")
    request_id: str = Field(..., description="Request ID for tracking")


# ============================================================================
# Internal Database Schemas
# ============================================================================

class ChapterCreate(BaseModel):
    """Schema for creating a chapter."""

    index: int = Field(..., description="Chapter index (1-16)")
    title: str = Field(..., description="Chapter title")
    module: int = Field(..., description="Module number (1-4)")
    part: int = Field(..., description="Part within module (1-4)")
    learning_objectives: List[str] = Field(..., description="Learning objectives")
    keywords: List[str] = Field(..., description="Related keywords")
    prerequisites: List[int] = Field(default_factory=list, description="Prerequisite chapters")


class ChunkVectorCreate(BaseModel):
    """Schema for creating a chunk vector."""

    chapter_index: int = Field(..., description="Chapter index")
    chunk_index: int = Field(..., description="Chunk index within chapter")
    content: str = Field(..., description="Chunk text content")
    embedding: List[float] = Field(..., description="Vector embedding")
    token_count: int = Field(..., description="Number of tokens in chunk")


class ChatSessionCreate(BaseModel):
    """Schema for creating a chat session."""

    user_id: Optional[str] = Field(None, description="Optional user identifier")
    chapter_context: Optional[int] = Field(None, description="Initial chapter context")


class ChatMessageCreate(BaseModel):
    """Schema for creating a chat message."""

    session_id: str = Field(..., description="Session ID")
    role: str = Field(..., description="Message role: user or assistant")
    content: str = Field(..., description="Message content")
    highlighted_context: Optional[str] = Field(None, description="Highlighted text context")
