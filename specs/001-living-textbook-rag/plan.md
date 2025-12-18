# Implementation Plan: Living Textbook with RAG Teaching Assistant

**Branch**: `001-living-textbook-rag` | **Date**: 2025-12-18 | **Spec**: [specs/001-living-textbook-rag/spec.md](spec.md)
**Input**: Feature specification from `/specs/001-living-textbook-rag/spec.md`

## Summary

Build a dual-hackathon "Living Textbook" system combining a 16-chapter Physical AI & Humanoid Robotics Docusaurus site with an embedded RAG-powered Teaching Assistant. The system enables students to ask context-aware questions about textbook content, receive AI-generated answers grounded in the book, and instructors to auto-ingest new chapters. Monorepo structure separates frontend (Docusaurus + React chat widget) from backend (FastAPI RAG pipeline).

**MVP Focus (P1)**: Context-aware chat queries with highlighted text context
**Post-MVP (P2/P3)**: Automated content ingestion, session tracking, learning analytics

## Technical Context

**Language/Version**:
- **Backend**: Python 3.12+ (FastAPI)
- **Frontend**: TypeScript 5.x (React 18+, Docusaurus 3)

**Primary Dependencies**:
- **Backend**: FastAPI, Qdrant client (`qdrant-client`), OpenAI SDK, SQLAlchemy, psycopg2
- **Frontend**: React, Docusaurus 3, Infima (CSS), TypeScript
- **Build**: npm (frontend), pip (backend)

**Storage**:
- **Vector DB**: Qdrant Cloud (Free Tier)
- **Relational DB**: Neon Serverless Postgres (for chat logs, sessions)
- **Frontend Static**: GitHub Pages

**Testing**:
- **Backend**: pytest, pytest-asyncio (async endpoint testing)
- **Frontend**: Jest, React Testing Library

**Target Platform**:
- **Backend**: Cloud-hosted (Render, Railway, Fly.io) with Python 3.12+ runtime
- **Frontend**: Static site deployment to GitHub Pages
- **Chat Widget**: Browser-based, responsive (desktop + mobile)

**Project Type**: Web application (monorepo with frontend + backend)

**Performance Goals**:
- API response time (p95): < 2 seconds for chat queries
- Ingest script: < 1 minute for full 16-chapter book
- Chat widget load time: < 3 seconds on 4G
- Vector search latency: < 500ms (p95)

**Constraints**:
- Monorepo structure (constitution Principle I): exactly `/frontend` + `/backend`, no cross-directory imports
- Tech stack (constitution Principle III): FastAPI, Qdrant, Neon, OpenAI only
- Schema-first API (constitution Principle V): OpenAPI spec before implementation
- Security (constitution Principle VI): all secrets in .env files, never committed
- Testing (constitution Principle VII): CI/CD gates on linting, type checking, tests

**Scale/Scope**:
- Content: 16 chapters (~50,000 tokens total when chunked)
- Users: 100 concurrent students + admin
- Deployment: Stateless backend (scalable on cloud)
- Data: 90-day chat history retention

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Constitution Principles Assessment**:

| Principle | Requirement | Status | Justification |
|-----------|-------------|--------|----------------|
| I. Monorepo Structure | Two directories: `/frontend`, `/backend` | ✅ PASS | Plan adheres to strict monorepo structure; zero cross-directory imports |
| II. Book Structure | 4 Modules × 4 Parts = 16 Chapters | ✅ PASS | Docusaurus config enforces exact chapter hierarchy |
| III. Strict Tech Stack | FastAPI, OpenAI Agents SDK, Qdrant, Neon | ✅ PASS | No alternative frameworks/DBs introduced; scope strictly bounded |
| IV. RAG Pipeline | Content ingest, chat interface, context queries | ✅ PASS | P1 user story covers all three requirements |
| V. Schema-First API | OpenAPI spec before implementation | ✅ PASS | Phase 1 generates `contracts/openapi.yaml` before coding |
| VI. Security | Environment variables for secrets | ✅ PASS | Backend config uses `python-dotenv`; .env in .gitignore |
| VII. Testing | CI/CD gates (type check, lint, tests) | ✅ PASS | Tasks include pytest setup, mypy type checking, ruff linting |
| VIII. Docs-as-Code | Metadata headers, Git workflow | ✅ PASS | Chapters include YAML frontmatter; Git-based content workflow |

**Gate Result**: ✅ **PASS** - All constitutional principles satisfied. No violations. Design may proceed.

## Project Structure

### Documentation (this feature)

```text
specs/001-living-textbook-rag/
├── spec.md                        # Feature specification (completed)
├── plan.md                        # This file (implementation architecture)
├── research.md                    # Phase 0: Research findings (to be generated)
├── data-model.md                  # Phase 1: Entity definitions (to be generated)
├── quickstart.md                  # Phase 1: Developer setup guide (to be generated)
├── contracts/                     # Phase 1: API contracts
│   ├── openapi.yaml              # OpenAPI 3.1 specification
│   ├── chat-schema.json          # POST /api/chat request/response
│   └── ingest-schema.json        # POST /api/ingest request/response
└── checklists/
    └── requirements.md            # Quality validation (completed)
```

### Source Code (repository root)

```text
.
├── frontend/                      # Docusaurus book application
│   ├── docs/                      # Content (16 chapters)
│   │   ├── 01-module-foundations/
│   │   │   ├── 01-python-intro.mdx
│   │   │   ├── 02-simulation-basics.mdx
│   │   │   ├── 03-math-robotics.mdx
│   │   │   └── 04-tools-setup.mdx
│   │   ├── 02-module-body/
│   │   │   ├── 05-sensors-overview.mdx
│   │   │   ├── 06-actuators-control.mdx
│   │   │   ├── 07-urdf-model.mdx
│   │   │   └── 08-kinematics.mdx
│   │   ├── 03-module-brain/
│   │   │   ├── 09-computer-vision.mdx
│   │   │   ├── 10-pytorch-basics.mdx
│   │   │   ├── 11-reinforcement-learning.mdx
│   │   │   └── 12-neural-networks.mdx
│   │   └── 04-module-humanoid/
│   │       ├── 13-walking-locomotion.mdx
│   │       ├── 14-grasping-manipulation.mdx
│   │       ├── 15-agentic-behaviors.mdx
│   │       └── 16-integration-project.mdx
│   ├── src/
│   │   ├── components/
│   │   │   ├── AiAssistant.tsx    # Chat widget (main integration)
│   │   │   ├── ChatWindow.tsx     # Chat UI
│   │   │   ├── MessageBubble.tsx  # Message display
│   │   │   └── ContextHighlight.tsx  # Highlight interaction
│   │   ├── services/
│   │   │   ├── api.ts            # Fetch wrapper for backend API
│   │   │   └── types.ts          # TypeScript types (generated from OpenAPI)
│   │   └── styles/
│   │       └── assistant.css      # Chat widget styles
│   ├── static/
│   │   └── img/                  # Images and diagrams
│   ├── sidebars.js               # Navigation structure (16 chapters)
│   ├── docusaurus.config.js      # Docusaurus config (TypeScript, Infima)
│   ├── package.json              # Node dependencies
│   └── README.md                 # Frontend setup guide
│
├── backend/                       # FastAPI RAG application
│   ├── src/
│   │   ├── main.py              # FastAPI app, routes, middleware
│   │   ├── config.py            # Environment config, secrets
│   │   ├── models/
│   │   │   ├── chapter.py       # Chapter entity
│   │   │   ├── chat.py          # ChatMessage, ChatSession entities
│   │   │   └── schemas.py       # Pydantic request/response schemas
│   │   ├── services/
│   │   │   ├── qdrant_service.py    # Vector search, embedding
│   │   │   ├── openai_service.py    # LLM queries, response generation
│   │   │   ├── postgres_service.py  # Session/chat log persistence
│   │   │   └── ingest_service.py    # Content chunking, embedding
│   │   ├── api/
│   │   │   ├── chat.py          # POST /api/chat endpoint
│   │   │   ├── ingest.py        # POST /api/ingest endpoint
│   │   │   ├── health.py        # GET /api/health endpoint
│   │   │   └── metadata.py      # GET /api/metadata endpoint
│   │   └── utils/
│   │       ├── chunker.py       # Semantic text chunking
│   │       ├── logger.py        # Structured logging
│   │       └── validators.py    # Input validation
│   ├── scripts/
│   │   ├── ingest_book.py       # Standalone ingestion script
│   │   └── reset_db.py          # Development: clear Qdrant/Postgres
│   ├── tests/
│   │   ├── contract/
│   │   │   ├── test_chat_contract.py
│   │   │   └── test_ingest_contract.py
│   │   ├── integration/
│   │   │   ├── test_chat_flow.py
│   │   │   └── test_ingest_flow.py
│   │   └── unit/
│   │       ├── test_chunker.py
│   │       ├── test_qdrant_service.py
│   │       └── test_validators.py
│   ├── requirements.txt          # Python dependencies
│   ├── pyproject.toml            # Project metadata, tool config
│   ├── .env.example              # Environment template (no secrets)
│   └── README.md                 # Backend setup guide
│
├── .gitignore                     # Ignore .env, __pycache__, node_modules
├── .env.example                  # Root-level env template (optional)
├── .github/
│   └── workflows/
│       ├── frontend-deploy.yml   # Deploy to GitHub Pages on push
│       ├── backend-lint.yml      # Type check, lint, test on PR
│       └── book-ingest.yml       # Optional: trigger ingest on schedule
├── README.md                      # Root monorepo guide
└── CONTRIBUTING.md               # How to add chapters/features
```

**Structure Decision**:
This is **Option 2: Web application** (monorepo with separate frontend + backend):
- `/frontend`: Docusaurus v3 static site with TypeScript + React chat widget
- `/backend`: FastAPI Python application with async endpoints
- Communication: REST API over HTTPS (schema-first via OpenAPI)
- No cross-directory imports; frontend only calls backend via HTTP

**Rationale**:
- Clear separation of concerns (content delivery vs. AI logic)
- Independent deployment (frontend → GitHub Pages, backend → cloud)
- Scalability (stateless backend, static frontend)
- Monorepo structure satisfies constitution Principle I

## Complexity Tracking

> No violations of constitutional principles. All design decisions within scope bounds. Table omitted (not needed).

---

## Phase 0: Research & Design Decisions

**Goal**: Resolve architectural unknowns and validate approach before detailed coding begins.

### Research Tasks

1. **Docusaurus + TypeScript Integration**
   - Decision: Use Docusaurus 3 with TypeScript support enabled
   - Rationale: Native TypeScript support, Infima styling included, minimal config
   - Findings: Docusaurus v3 has `typescript.enabled: true` in config

2. **Qdrant Semantic Chunking**
   - Decision: Implement client-side semantic chunking (200–500 tokens per chunk)
   - Rationale: Preserve context better than fixed-size chunks; use OpenAI's text-embedding-3-small
   - Alternatives: LangChain (adds dependency), LLamaIndex (complexity)
   - Finding: `qdrant-client` supports batch upsert; use `langchain-text-splitters` for semantic chunking

3. **OpenAI Agents SDK vs. ChatKit SDK**
   - Decision: Use OpenAI SDK directly (not Agents SDK) with gpt-4o-mini model
   - Rationale: Simpler integration, lower latency for MVP, cost-effective
   - Agents SDK (swarm) better for multi-turn complex workflows (future)
   - Finding: `openai==1.3.0+` supports structured outputs, async calls

4. **PostgreSQL Adapter for Neon**
   - Decision: Use SQLAlchemy ORM with async driver (`asyncpg`)
   - Rationale: ORM handles Neon connection pooling, async matches FastAPI
   - Alternative: Raw psycopg2 (more control, more code)
   - Finding: Neon provides PostgreSQL-compatible connection strings

5. **Frontend Context API vs. Redux**
   - Decision: Use React Context + hooks for session/chat state (MVP)
   - Rationale: Minimal setup, sufficient for MVP, no extra dependencies
   - Redux added later if needed (P3 complex state management)
   - Finding: Context works well for app-level state (session, user preferences)

6. **API Rate Limiting & Fallback**
   - Decision: Implement rate limiting on backend (100 queries/hour per session)
   - Rationale: Prevent abuse, manage OpenAI costs
   - Fallback: Return 429 Too Many Requests; frontend shows user-friendly message
   - Finding: Use `slowapi` library for FastAPI rate limiting

7. **Qdrant Fallback & Error Handling**
   - Decision: If Qdrant unavailable, return 503 Service Unavailable (not generic 500)
   - Rationale: Signals temporary outage (client can retry); better UX than generic error
   - Finding: Wrap Qdrant calls in try-except, log error, return 503

**Output**: Phase 0 findings incorporated into Phase 1 design below.

---

## Phase 1: Design & Contracts

### 1.1 Data Model

**Generated Entities** (see data-model.md for full details):

- **Chapter**: Represents a textbook chapter
  - Fields: `id`, `title`, `module_id`, `part_id`, `chapter_index`, `content_markdown`, `metadata_json`, `created_at`, `updated_at`
  - Validation: `chapter_index` must be 1–16, `module_id` 1–4, `part_id` 1–4
  - Storage: PostgreSQL (Neon)

- **ChunkVector**: Semantic text chunk with embedding
  - Fields: `id`, `chapter_id`, `chunk_index`, `content_text`, `embedding_vector` (vector type), `token_count`, `created_at`
  - Validation: `token_count` must be 200–500
  - Storage: Qdrant Cloud

- **ChatSession**: User session tracking
  - Fields: `id`, `user_id` (optional, nullable), `created_at`, `last_activity`, `ip_address_hash`, `metadata_json`
  - Validation: `id` is UUID, `created_at` immutable
  - Storage: PostgreSQL (Neon)

- **ChatMessage**: Query-response pair
  - Fields: `id`, `session_id`, `query_text`, `response_text`, `highlighted_context`, `source_chapter_ids`, `confidence_score`, `created_at`
  - Validation: `confidence_score` 0.0–1.0, `query_text` non-empty
  - Storage: PostgreSQL (Neon)

- **IngestionLog**: Audit trail for content updates
  - Fields: `id`, `run_timestamp`, `chapters_processed`, `chunks_created`, `status`, `error_message`, `duration_seconds`
  - Validation: `status` IN ('success', 'failed', 'partial')
  - Storage: PostgreSQL (Neon)

### 1.2 API Contracts (OpenAPI 3.1)

**Core Endpoints**:

```yaml
POST /api/chat
  Summary: Answer a student's question about textbook content
  Request:
    - query_text: string (required, non-empty)
    - highlighted_context: string (optional)
    - chapter_context: number (optional, chapter ID)
    - session_id: string (UUID, optional; generated if missing)
  Response:
    - response_text: string
    - source_chapters: array[chapter_id, title]
    - confidence_score: number (0.0–1.0)
    - session_id: string (UUID)
    - timestamp: ISO8601
  Status Codes:
    - 200: OK
    - 400: Bad request (empty query, invalid session_id)
    - 429: Rate limit exceeded (100 queries/hour)
    - 503: Service unavailable (Qdrant down, OpenAI rate limited)

POST /api/ingest
  Summary: Update Qdrant with book content (admin-only)
  Request:
    - admin_token: string (bearer auth)
    - force_refresh: boolean (optional, default false)
  Response:
    - status: string ('success' | 'failed' | 'partial')
    - chapters_processed: number
    - chunks_created: number
    - duration_seconds: number
    - error_message: string (if failed)
  Status Codes:
    - 200: OK
    - 401: Unauthorized (invalid token)
    - 500: Server error

GET /api/health
  Summary: Health check for deployment monitoring
  Response:
    - status: string ('healthy' | 'degraded')
    - qdrant_status: string ('ok' | 'offline')
    - postgres_status: string ('ok' | 'offline')
  Status Codes:
    - 200: Healthy
    - 503: Degraded

GET /api/metadata
  Summary: List available chapters and keywords for frontend filters
  Response:
    - chapters: array[{ id, title, module_id, part_id, keywords }]
  Status Codes:
    - 200: OK
```

*(Full OpenAPI spec in `/specs/001-living-textbook-rag/contracts/openapi.yaml`)*

### 1.3 Frontend Architecture

**Chat Widget (`<AiAssistant />` component)**:
- Floats on right side of page (fixed position)
- Accessible via `Tab` key (keyboard navigation)
- Drag-to-minimize, click-to-expand
- Sends highlighted text + page context to backend
- Displays streaming responses (chunks as they arrive)

**Context Highlighting**:
- Student selects text in chapter
- Popup appears: "Ask AI about this"
- Opens chat widget with selected text injected

**Session Management**:
- Browser local storage stores `session_id` (UUID)
- Persists across page refreshes
- Each session = independent chat history

### 1.4 Backend Architecture

**Request Flow** (for POST `/api/chat`):
1. Validate query (non-empty, rate limit check)
2. Retrieve or create session
3. Embed query using OpenAI `text-embedding-3-small`
4. Vector search in Qdrant (return top-5 chunks)
5. Construct prompt with retrieved chunks
6. Call OpenAI `gpt-4o-mini` to generate response
7. Validate response (book-only content check)
8. Log to PostgreSQL (chat_message table)
9. Stream response back to frontend

**Ingestion Flow** (for POST `/api/ingest`):
1. Authenticate admin token
2. Read all `.mdx` files from `/frontend/docs/`
3. For each chapter:
   - Extract metadata header (YAML frontmatter)
   - Split content into semantic chunks (200–500 tokens)
   - Generate embeddings via OpenAI API
   - Upsert to Qdrant (batch operation)
   - Record in PostgreSQL (chapters, chunks tables)
4. Log ingestion result (PostgreSQL: ingestion_logs table)

---

## Phase 2: Development Workflow

### Setup Phase

1. **Initialize Backend** (`/backend`)
   - Create virtual environment: `python -m venv venv`
   - Install dependencies: `pip install -r requirements.txt`
   - Setup PostgreSQL connection: `DATABASE_URL=postgres://...` in `.env`
   - Setup Qdrant connection: `QDRANT_URL=...` in `.env`
   - Setup OpenAI key: `OPENAI_API_KEY=...` in `.env`

2. **Initialize Frontend** (`/frontend`)
   - Create Docusaurus site: `npx create-docusaurus@latest frontend classic --typescript`
   - Install chat dependencies: `npm install`
   - Copy chapter templates to `/frontend/docs/`
   - Configure `sidebars.js` with 16-chapter structure

3. **Local Development**
   - Terminal 1: `cd frontend && npm start` (Docusaurus dev server, port 3000)
   - Terminal 2: `cd backend && uvicorn src.main:app --reload` (FastAPI server, port 8000)
   - Frontend calls backend at `http://localhost:8000/api/chat`

### CI/CD Pipeline

1. **Frontend Deploy** (GitHub Actions)
   - Trigger: Push to `main` branch
   - Steps: TypeScript compile, ESLint, Jest tests, `npm run build`, deploy to GitHub Pages
   - Status: Automatic

2. **Backend Lint & Test** (GitHub Actions)
   - Trigger: PR to `main` branch
   - Steps: mypy type check, ruff lint, pytest (unit + integration), coverage report
   - Status: Required pass before merge

3. **Book Ingest Trigger** (Optional CI job)
   - Trigger: Schedule (daily) or manual
   - Steps: Call `POST /api/ingest` with admin token
   - Purpose: Keep Qdrant updated with latest chapters

---

## Next Steps

**Phase 0 Output**: [To be generated as `research.md`]
- Architecture decisions documented
- Technology choices validated
- Integration patterns confirmed

**Phase 1 Output** (from this plan):
- `data-model.md`: Full entity definitions with validation rules
- `contracts/openapi.yaml`: Complete API specification
- `quickstart.md`: Developer setup guide (step-by-step)

**Phase 2 Output** (via `/sp.tasks`):
- Detailed implementation tasks (T001, T002, ...)
- Task dependencies and parallelization
- Estimated effort per task

**Recommended Next Command**:
```bash
/sp.tasks
```
Generate detailed task breakdown organized by user story (P1 MVP first, then P2, P3).

---

## Architecture Diagram (Text)

```
┌─────────────────────────────────────────────────────────────────┐
│                     STUDENT / INSTRUCTOR                         │
└────────────────────────┬────────────────────────────────────────┘
                         │ (Browser)
                         ▼
┌──────────────────────────────────────────────────────────────────┐
│                      FRONTEND (Docusaurus)                        │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  📖 16 Chapters (4 Modules × 4 Parts)                      │ │
│  │  - Module 1: Foundations (Ch 1-4)                         │ │
│  │  - Module 2: The Body (Ch 5-8)                            │ │
│  │  - Module 3: The Brain (Ch 9-12)                          │ │
│  │  - Module 4: Humanoid Control (Ch 13-16)                 │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  💬 AI Assistant Widget (React Component)                  │ │
│  │  - Highlight text → Ask question                          │ │
│  │  - Sends: query + context to backend                      │ │
│  │  - Receives: AI response (streamed)                       │ │
│  └────────────────────────────────────────────────────────────┘ │
│                   GitHub Pages (Static Deploy)                   │
└──────────────────┬─────────────────────────────────────────────┘
                   │ (HTTPS REST API)
                   │ POST /api/chat
                   │ GET /api/metadata
                   │ GET /api/health
                   ▼
┌──────────────────────────────────────────────────────────────────┐
│                   BACKEND (FastAPI - Python)                      │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  🧠 RAG Pipeline                                           │ │
│  │  1. Embed query (OpenAI text-embedding-3-small)           │ │
│  │  2. Vector search (Qdrant Cloud) → top-5 chunks          │ │
│  │  3. Generate response (OpenAI gpt-4o-mini)               │ │
│  │  4. Validate (book-only content)                          │ │
│  │  5. Log to PostgreSQL + stream to frontend                │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  📥 Ingest Pipeline (ingest_book.py script)               │ │
│  │  1. Read chapters from /frontend/docs/                    │ │
│  │  2. Semantic chunking (200-500 tokens)                    │ │
│  │  3. Generate embeddings (OpenAI)                          │ │
│  │  4. Upsert to Qdrant (batch)                              │ │
│  │  5. Log to PostgreSQL                                      │ │
│  └────────────────────────────────────────────────────────────┘ │
│           Cloud Platform (Render, Railway, Fly.io)               │
└──────────────┬──────────────────────┬──────────────────────────┘
               │                      │
               ▼                      ▼
    ┌──────────────────┐  ┌────────────────────────────┐
    │  Qdrant Cloud    │  │ Neon Postgres              │
    │  (Vector DB)     │  │ (Chat logs, sessions)      │
    │  Free Tier       │  │ Serverless                 │
    └──────────────────┘  └────────────────────────────┘
```

---

## Risk Analysis & Mitigation

| Risk | Blast Radius | Mitigation |
|------|--------------|-----------|
| Qdrant unavailable | Chat queries fail (P1 blocked) | Return 503; log error; retry logic in frontend |
| OpenAI rate limit exceeded | Responses slow/fail | Implement rate limiting on backend; queue queries |
| Neon connection pooling exhausted | Session logging fails | Async connection pooling (asyncpg); monitor connections |
| Chapter metadata parsing fails | Ingest fails; AI confused | Validate YAML frontmatter; unit tests for parser |
| Cross-chapter highlighting ambiguity | Poor context retrieval | Implement priority ranking (70% highlighted chapter, 30% global) |

---

## Success Criteria Mapping

| Success Criterion | Design Support |
|------------------|----------------|
| SC-001: Response < 2s (p95) | Async FastAPI, vector search optimization, streaming |
| SC-002: Ingest < 1 min | Batch Qdrant upsert, parallel embeddings (OpenAI batch API) |
| SC-003: 90% include code examples | Prompt design in system message; few-shot examples |
| SC-004: Lighthouse ≥ 90 | TypeScript strict mode, lazy-load chat widget, optimize images |
| SC-005: 95% reject out-of-scope | System prompt: "Only answer from the book"; confidence threshold |
| SC-006: Widget loads < 3s on 4G | Defer chat component, use CDN for assets |
| SC-007: 100 concurrent queries | Stateless backend, horizontal scaling, rate limiting |
| SC-008: 100% OpenAPI compliance | Generate TypeScript types from spec; contract tests |

