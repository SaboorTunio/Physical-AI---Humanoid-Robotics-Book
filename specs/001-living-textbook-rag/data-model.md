# Data Model: Living Textbook RAG System

**Date**: 2025-12-18
**Feature**: Living Textbook with RAG Teaching Assistant
**Branch**: `001-living-textbook-rag`

## Overview

This document defines all persistent entities, their relationships, validation rules, and storage backends for the Living Textbook RAG system.

**Storage Backends**:
- **Qdrant Cloud**: Vector embeddings (ChunkVector)
- **Neon Postgres**: Relational data (Chapter, ChatSession, ChatMessage, IngestionLog)

---

## Entities

### 1. Chapter

**Purpose**: Represents a single textbook chapter within the 16-chapter curriculum.

**Storage**: PostgreSQL (Neon)

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique identifier for chapter |
| `title` | VARCHAR(255) | NOT NULL, UNIQUE | Chapter title (e.g., "Servo Motors and Control") |
| `module_id` | INT | NOT NULL, 1–4 | Module number (Foundations, Body, Brain, Humanoid) |
| `part_id` | INT | NOT NULL, 1–4 | Part within module (1–4) |
| `chapter_index` | INT | NOT NULL, 1–16 | Global chapter number (1–16) |
| `content_markdown` | TEXT | NOT NULL | Full chapter content (MDX/Markdown) |
| `metadata_json` | JSONB | NOT NULL | YAML frontmatter: title, objectives, keywords, prerequisites |
| `token_count` | INT | NOT NULL | Total tokens in chapter content (for budget tracking) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT now() | When chapter was created |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT now() | Last update timestamp |

**Indexes**:
- `(module_id, part_id, chapter_index)`: For navigating chapter hierarchy
- `(chapter_index)`: For quick lookup by global order

**Validation Rules**:
- `module_id` ∈ {1, 2, 3, 4}
- `part_id` ∈ {1, 2, 3, 4}
- `chapter_index` ∈ {1, 2, ..., 16}
- `title` is non-empty and unique
- `content_markdown` is non-empty
- `metadata_json` MUST contain: `learning_objectives`, `prerequisites`, `keywords` (array)

**Example**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Servo Motors and Control",
  "module_id": 2,
  "part_id": 2,
  "chapter_index": 6,
  "content_markdown": "## Servo Motors and Control\n\nA servo motor is...",
  "metadata_json": {
    "learning_objectives": [
      "Understand servo motor mechanics",
      "Implement PID controllers"
    ],
    "prerequisites": ["Chapter 5: Sensors"],
    "keywords": ["servo", "PID", "control", "motor"]
  },
  "token_count": 3500,
  "created_at": "2025-12-18T10:00:00Z",
  "updated_at": "2025-12-18T10:00:00Z"
}
```

---

### 2. ChunkVector

**Purpose**: Represents a semantic chunk of chapter content with its embedding vector, stored in Qdrant.

**Storage**: Qdrant Cloud

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | Qdrant id | Unique identifier |
| `chapter_id` | UUID | NOT NULL | Foreign key to Chapter |
| `chunk_index` | INT | NOT NULL | Index within chapter (0, 1, 2, ...) |
| `content_text` | TEXT | NOT NULL, 200–500 tokens | Chunk content (semantic unit) |
| `embedding_vector` | VECTOR(1536) | NOT NULL | OpenAI text-embedding-3-small output |
| `token_count` | INT | NOT NULL, 200–500 | Token count for chunk |
| `created_at` | TIMESTAMP | NOT NULL | When chunk was created |

**Qdrant Configuration**:
- Vector size: 1536 (OpenAI text-embedding-3-small)
- Similarity metric: COSINE
- Indexed payload: `chapter_id`, `chunk_index`, `token_count`

**Validation Rules**:
- `token_count` must be 200–500 (constitutional requirement for context preservation)
- `content_text` must be non-empty
- `chapter_id` must reference an existing Chapter
- `chunk_index` must be >= 0

**Example**:
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440111",
  "chapter_id": "550e8400-e29b-41d4-a716-446655440000",
  "chunk_index": 0,
  "content_text": "A servo motor is an electromechanical device that converts electrical signals into precise angular or linear motion. Unlike DC motors, servo motors use feedback control to maintain a specific position or velocity. The key components are: (1) the motor, (2) a position sensor, and (3) a control circuit. Servo motors are widely used in robotics for joint actuation.",
  "embedding_vector": [0.023, -0.015, 0.042, ..., 0.001],
  "token_count": 250,
  "created_at": "2025-12-18T10:01:00Z"
}
```

---

### 3. ChatSession

**Purpose**: Represents a user session for tracking conversations across multiple messages.

**Storage**: PostgreSQL (Neon)

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Session identifier (generated on first chat) |
| `user_id` | UUID | NULLABLE | Optional user ID (for authenticated users) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT now() | When session started |
| `last_activity` | TIMESTAMP | NOT NULL, DEFAULT now() | Last message timestamp |
| `ip_address_hash` | VARCHAR(64) | NOT NULL | SHA256 hash of IP (privacy) |
| `metadata_json` | JSONB | NOT NULL, DEFAULT '{}' | Session metadata (e.g., browser, device type) |

**Indexes**:
- `(id)`: PRIMARY KEY
- `(created_at)`: For cleanup (90-day retention)
- `(ip_address_hash)`: For rate limiting

**Validation Rules**:
- `id` must be a valid UUID
- `created_at` is immutable (set once at creation)
- `last_activity` is automatically updated on each message

**Example**:
```json
{
  "id": "770e8400-e29b-41d4-a716-446655440222",
  "user_id": null,
  "created_at": "2025-12-18T09:30:00Z",
  "last_activity": "2025-12-18T10:15:00Z",
  "ip_address_hash": "a1b2c3d4e5f6...",
  "metadata_json": {
    "browser": "Chrome",
    "device": "mobile",
    "country": "US"
  }
}
```

---

### 4. ChatMessage

**Purpose**: Represents a single question-response exchange in a chat session.

**Storage**: PostgreSQL (Neon)

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique message identifier |
| `session_id` | UUID | NOT NULL, FK | Foreign key to ChatSession |
| `query_text` | TEXT | NOT NULL, non-empty | Student's question |
| `response_text` | TEXT | NOT NULL | AI-generated answer |
| `highlighted_context` | TEXT | NULLABLE | Text the student highlighted (if any) |
| `source_chapter_ids` | UUID[] | NOT NULL | Which chapters were used in response |
| `confidence_score` | FLOAT | NOT NULL, 0.0–1.0 | Confidence that response is accurate (0–1) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT now() | When message was created |

**Indexes**:
- `(session_id, created_at)`: For retrieving session history
- `(created_at)`: For cleanup (90-day retention)

**Validation Rules**:
- `query_text` must be non-empty and <2000 characters
- `response_text` must be non-empty
- `confidence_score` must be between 0.0 and 1.0 (inclusive)
- `source_chapter_ids` must not be empty (at least one chapter should be cited)
- `session_id` must reference an existing ChatSession

**Example**:
```json
{
  "id": "880e8400-e29b-41d4-a716-446655440333",
  "session_id": "770e8400-e29b-41d4-a716-446655440222",
  "query_text": "How do I implement a PID controller in Python for servo motors?",
  "response_text": "To implement a PID controller in Python, you'll need three main components:\n\n1. **Error Calculation**: error = setpoint - current_position\n2. **PID Terms**:\n   - Proportional: Kp * error\n   - Integral: Ki * sum(error)\n   - Derivative: Kd * (error_rate)\n3. **Control Output**: u(t) = Kp*e(t) + Ki*∫e(t)dt + Kd*de(t)/dt\n\nHere's a basic implementation:\n```python\nclass PIDController:\n    def __init__(self, Kp, Ki, Kd):\n        self.Kp = Kp\n        ...\n```",
  "highlighted_context": "Servo motors use feedback control to maintain a specific position or velocity. The key components are: (1) the motor, (2) a position sensor, and (3) a control circuit.",
  "source_chapter_ids": [
    "550e8400-e29b-41d4-a716-446655440000",
    "550e8400-e29b-41d4-a716-446655440001"
  ],
  "confidence_score": 0.92,
  "created_at": "2025-12-18T10:15:00Z"
}
```

---

### 5. IngestionLog

**Purpose**: Audit trail for content update runs (tracking when and how the Qdrant index was updated).

**Storage**: PostgreSQL (Neon)

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique log entry identifier |
| `run_timestamp` | TIMESTAMP | NOT NULL, DEFAULT now() | When the ingest script ran |
| `chapters_processed` | INT | NOT NULL, >= 0 | Number of chapters processed |
| `chunks_created` | INT | NOT NULL, >= 0 | Total chunks created/updated |
| `status` | ENUM | NOT NULL, IN ('success', 'partial', 'failed') | Ingestion result |
| `error_message` | TEXT | NULLABLE | Error details (if failed or partial) |
| `duration_seconds` | FLOAT | NOT NULL, > 0 | How long the ingest took |

**Indexes**:
- `(run_timestamp)`: For audit trails and debugging
- `(status)`: For failure detection

**Validation Rules**:
- `chapters_processed` >= 0
- `chunks_created` >= 0
- `status` must be one of: 'success', 'partial', 'failed'
- `duration_seconds` must be > 0
- If `status` == 'success', `error_message` should be NULL

**Example**:
```json
{
  "id": "990e8400-e29b-41d4-a716-446655440444",
  "run_timestamp": "2025-12-18T11:00:00Z",
  "chapters_processed": 16,
  "chunks_created": 450,
  "status": "success",
  "error_message": null,
  "duration_seconds": 45.3
}
```

---

## Relationships

```
Chapter (1) ──── (many) ChunkVector
  |                    |
  └─────────────────────┘
           |
   (referenced in)
           |
      ChatMessage
           |
        (part of)
           |
      ChatSession
```

**Relationships**:
- One Chapter has many ChunkVectors (1:N)
- One ChatSession has many ChatMessages (1:N)
- ChatMessage references multiple Chapters via `source_chapter_ids` (M:N)

**Cascade Rules**:
- Deleting a Chapter cascades delete to ChunkVectors
- Deleting a ChatSession cascades delete to ChatMessages
- Deleting a ChatMessage does NOT cascade (it's just a log)

---

## Data Retention Policies

| Entity | Retention | Reason |
|--------|-----------|--------|
| Chapter | Indefinite | Textbook content is authoritative |
| ChunkVector | Indefinite | Vectors stay until chapter updated |
| ChatSession | 90 days | Privacy: comply with data retention standards |
| ChatMessage | 90 days | Same as ChatSession (delete with session) |
| IngestionLog | 30 days | Audit trail, then archive to cold storage |

---

## Migration Strategy

### Initial Setup (Phase 2 - Red/Green Testing)

1. **Create PostgreSQL schema** (using SQLAlchemy migrations):
   ```sql
   CREATE TABLE chapters (...)
   CREATE TABLE chat_sessions (...)
   CREATE TABLE chat_messages (...)
   CREATE TABLE ingestion_logs (...)
   ```

2. **Initialize Qdrant collection**:
   ```python
   client.recreate_collection(
       collection_name="book_chunks",
       vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
   )
   ```

3. **Initial book ingestion**: Run `scripts/ingest_book.py` to populate first 16 chapters

### Updates (During development)

- **Add new chapter**: Run ingest script (automatic upsert)
- **Modify chapter**: Run ingest script (replaces old vectors)
- **Schema changes**: Use SQLAlchemy migrations (Alembic)

---

## Example Queries

### Query 1: Find all chapters in a specific module

```sql
SELECT title, part_id, chapter_index
FROM chapters
WHERE module_id = 2
ORDER BY part_id, chapter_index;
```

### Query 2: Retrieve chat history for a session

```sql
SELECT query_text, response_text, confidence_score, created_at
FROM chat_messages
WHERE session_id = '770e8400-e29b-41d4-a716-446655440222'
ORDER BY created_at DESC
LIMIT 10;
```

### Query 3: Find most recent successful ingestion

```sql
SELECT run_timestamp, chapters_processed, chunks_created, duration_seconds
FROM ingestion_logs
WHERE status = 'success'
ORDER BY run_timestamp DESC
LIMIT 1;
```

### Query 4: Cleanup old sessions (90 days)

```sql
DELETE FROM chat_sessions
WHERE last_activity < NOW() - INTERVAL '90 days';
```

### Query 5: Vector search (via Qdrant Python client)

```python
results = qdrant_client.search(
    collection_name="book_chunks",
    query_vector=query_embedding,
    limit=5,
    with_payload=True,
    query_filter={
        "key": "chapter_id",
        "match": {"value": "550e8400-e29b-41d4-a716-446655440000"}
    }
)
```

---

## State Diagrams

### ChatSession Lifecycle

```
[Created] ──→ [Active] ──→ [Idle] ──→ [Deleted (after 90 days)]
   |              |
   └──────────────┘
   (last_activity updated)
```

### ChatMessage State

```
[Query Received]
     ↓
[Embedded]
     ↓
[Vector Search]
     ↓
[Prompt Constructed]
     ↓
[LLM Response Generated]
     ↓
[Validated (book-only check)]
     ↓
[Logged to DB] ──→ [Sent to Frontend]
```

### IngestionLog State

```
[Script Started]
     ↓
[Reading Chapters]
     ↓
[Chunking Content]
     ↓
[Generating Embeddings]
     ↓
[Upserting to Qdrant]
     ↓
[Logging Result] ──→ {'success' | 'partial' | 'failed'}
```

---

## Type Definitions (for API)

### Pydantic Schemas (FastAPI)

```python
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

class ChapterMetadata(BaseModel):
    learning_objectives: List[str]
    prerequisites: List[str]
    keywords: List[str]

class ChapterOut(BaseModel):
    id: uuid.UUID
    title: str
    module_id: int
    part_id: int
    chapter_index: int
    metadata: ChapterMetadata

class ChatMessageOut(BaseModel):
    query_text: str
    response_text: str
    source_chapters: List[str]  # chapter titles
    confidence_score: float
    created_at: datetime

class ChatSessionOut(BaseModel):
    id: uuid.UUID
    created_at: datetime
    message_count: int
```

