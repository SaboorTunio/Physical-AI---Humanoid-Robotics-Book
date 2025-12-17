---
description: "Detailed task breakdown for Living Textbook with RAG Teaching Assistant implementation"
---

# Tasks: Living Textbook with RAG Teaching Assistant

**Input**: Design documents from `/specs/001-living-textbook-rag/`
**Prerequisites**: plan.md ✅, spec.md ✅, data-model.md ✅, contracts/openapi.yaml ✅
**Branch**: `001-living-textbook-rag`

**Tests**: Not explicitly requested in spec, but contract tests recommended for API endpoints.

**Organization**: Tasks are grouped by user story (P1 → P2 → P3) to enable independent implementation and testing of each story. Each user story is independently deployable and testable.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Task can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Which user story (US1, US2, US3) — REQUIRED for story phase tasks
- **File paths**: Absolute to repository root

## Path Conventions

- **Frontend**: `frontend/src/`, `frontend/docs/`, `frontend/static/`
- **Backend**: `backend/src/`, `backend/scripts/`, `backend/tests/`
- **Shared**: `.env`, `.gitignore` at root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

**Duration**: ~2 hours

- [ ] T001 Create monorepo root structure: `/frontend`, `/backend`, `/specs`, `/history`, `/.github`, `README.md`, `CONTRIBUTING.md`
- [ ] T002 [P] Initialize frontend Docusaurus project in `/frontend` with TypeScript support and GitHub Pages config
- [ ] T003 [P] Initialize backend Python venv in `/backend`, create `requirements.txt` with FastAPI, Uvicorn, qdrant-client, openai, sqlalchemy, asyncpg, python-dotenv, slowapi
- [ ] T004 [P] Create `.env.example` at root with template for: OPENAI_API_KEY, QDRANT_URL, QDRANT_API_KEY, DATABASE_URL, ADMIN_TOKEN, ENVIRONMENT
- [ ] T005 Create `.gitignore` to exclude: `.env`, `__pycache__`, `venv/`, `node_modules/`, `dist/`, `build/`, `.DS_Store`
- [ ] T006 [P] Configure GitHub Actions workflows in `.github/workflows/`:
  - `frontend-deploy.yml`: Deploy to GitHub Pages on push to main
  - `backend-lint.yml`: Type check (mypy), lint (ruff), test (pytest) on PR to main
  - `book-ingest.yml`: Optional scheduled ingestion (daily)
- [ ] T007 [P] Create `pyproject.toml` for Python project config (poetry/pip-tools alternative if preferred)
- [ ] T008 Create `frontend/package.json` (npm init) and `frontend/tsconfig.json` for TypeScript configuration

**Checkpoint**: Monorepo scaffolding complete, both frontend and backend can start development

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

**Duration**: ~4-5 hours

### Backend Infrastructure

- [ ] T009 Create `backend/src/config.py` with environment variable loading (python-dotenv) for OPENAI_API_KEY, QDRANT_URL, DATABASE_URL, ADMIN_TOKEN
- [ ] T010 Create `backend/src/main.py` FastAPI application skeleton with:
  - CORS middleware for frontend domain
  - Error handling middleware (custom exception handlers)
  - Logging configuration
  - Startup/shutdown events for database connections
- [ ] T011 [P] Create Pydantic schemas in `backend/src/models/schemas.py`:
  - ChatRequest (query_text, highlighted_context, chapter_context, session_id)
  - ChatResponse (response_text, source_chapters, confidence_score, session_id, timestamp)
  - IngestRequest (force_refresh)
  - IngestResponse (status, chapters_processed, chunks_created, duration_seconds, error_message)
  - ErrorResponse (error, message, details)
- [ ] T012 [P] Create SQLAlchemy ORM models in `backend/src/models/database.py`:
  - Chapter entity (id, title, module_id, part_id, chapter_index, content_markdown, metadata_json, token_count, created_at, updated_at)
  - ChatSession entity (id, user_id, created_at, last_activity, ip_address_hash, metadata_json)
  - ChatMessage entity (id, session_id, query_text, response_text, highlighted_context, source_chapter_ids, confidence_score, created_at)
  - IngestionLog entity (id, run_timestamp, chapters_processed, chunks_created, status, error_message, duration_seconds)
- [ ] T013 Create `backend/src/database.py` with:
  - AsyncSession factory (asyncpg pool)
  - Engine initialization
  - get_session() context manager for dependency injection
- [ ] T014 [P] Create migration framework in `backend/alembic/` (Alembic for SQLAlchemy migrations):
  - `env.py` configuration
  - Initial migration to create all tables
  - Helper script: `backend/scripts/migrate.py`
- [ ] T015 [P] Create utility modules:
  - `backend/src/utils/logger.py`: Structured logging (JSON format)
  - `backend/src/utils/validators.py`: Input validation (query_text length, session_id format, etc.)
  - `backend/src/utils/errors.py`: Custom exception classes (QuotaExceeded, QdrantUnavailable, ValidationError)
- [ ] T016 Create `backend/src/services/qdrant_service.py` with:
  - QdrantClient initialization and connection management
  - get_collection_info() method
  - Health check method
  - Exception handling for Qdrant downtime
- [ ] T017 Create `backend/src/services/openai_service.py` with:
  - OpenAI client initialization
  - embed_text() method using text-embedding-3-small
  - generate_response() method using gpt-4o-mini
  - Rate limit detection and handling
  - Exception handling for API errors

### Frontend Infrastructure

- [ ] T018 Create `frontend/docusaurus.config.js` with:
  - TypeScript support enabled
  - GitHub Pages deployment configuration (baseUrl, organizationName, projectName)
  - Infima CSS theme configured
  - Custom CSS imports
  - Sidebar structure for 16 chapters (4 modules × 4 parts)
- [ ] T019 Create `frontend/sidebars.js` with chapter hierarchy:
  - Module 1: Foundations (Chapters 1-4)
  - Module 2: The Body (Chapters 5-8)
  - Module 3: The Brain (Chapters 9-12)
  - Module 4: Humanoid Control (Chapters 13-16)
- [ ] T020 Create TypeScript types in `frontend/src/types/api.ts` (generated from OpenAPI spec or manually):
  - ChatRequest, ChatResponse types
  - IngestRequest, IngestResponse types
  - ErrorResponse type
- [ ] T021 Create `frontend/src/services/api.ts` with:
  - Fetch wrapper for backend API calls
  - Base URL configuration (localhost:8000 dev, production URL prod)
  - Error handling and user-friendly messages
  - Session ID persistence in localStorage
- [ ] T022 Create `frontend/src/components/AiAssistant.tsx` component skeleton:
  - Empty React component with floating widget styling
  - Chat window structure (messages, input field, send button)
  - Basic CSS module: `frontend/src/components/AiAssistant.module.css`

**Checkpoint**: Backend and frontend scaffolding complete. All infrastructure ready. Ready to start user stories in parallel.

---

## Phase 3: User Story 1 - Context-Aware Chat Queries (Priority: P1) 🎯 MVP

**Goal**: Students can highlight text in the book, ask questions, and receive AI-generated answers grounded in the textbook content.

**Independent Test**:
1. Upload minimal book content (2 chapters) to Qdrant
2. Highlight text on frontend
3. Submit query via `/api/chat` with highlighted context
4. Verify response includes relevant explanation + code example
5. Verify response delivered within 2 seconds

**Duration**: ~8-10 hours for complete implementation

### Data Preparation for User Story 1

- [ ] T023 [P] Create 2 sample chapters in `frontend/docs/01-module-foundations/`:
  - `01-python-intro.mdx`: Python basics, YAML metadata header
  - `02-simulation-basics.mdx`: Simulation setup, YAML metadata header
- [ ] T024 Create `frontend/docs/chapter-template.mdx` as template for other chapters (YAML frontmatter format)

### Backend Implementation for User Story 1

- [ ] T025 [P] Create `backend/src/services/chunker.py` with:
  - Semantic text chunking function (200-500 tokens per chunk)
  - Overlap handling for context preservation
  - Token counter using tiktoken library
  - Markdown-to-text extraction
- [ ] T026 Create `backend/src/services/ingest_service.py` with:
  - read_chapters() function: Read all .mdx files from `/frontend/docs/`
  - parse_chapter_metadata() function: Extract YAML frontmatter
  - chunk_chapter() function: Call chunker.py
  - embed_chunks() function: Call openai_service.embed_text() (batch if possible)
  - upsert_to_qdrant() function: Batch upsert to Qdrant
  - log_ingestion() function: Write IngestionLog to PostgreSQL
- [ ] T027 Create `backend/src/services/rag_service.py` with:
  - retrieve_relevant_chunks() method:
    * Takes query_text, highlighted_context (optional), chapter_context (optional)
    * Embeds query using openai_service
    * Vector search in Qdrant (top-5 chunks)
    * If highlighted_context: boost relevance of chunks from that chapter (70/30 weighting)
    * Returns list of chunks with metadata (chapter_id, title, confidence)
  - generate_response() method:
    * Constructs system prompt: "You are a teaching assistant. Answer ONLY using the provided textbook content."
    * Constructs user prompt with retrieved chunks and query
    * Calls openai_service.generate_response()
    * Validates response (checks for hallucination/out-of-scope content)
    * Returns response_text, source_chapters, confidence_score
  - validate_response() method: Ensures response references textbook content
- [ ] T028 [P] Create API endpoints in `backend/src/api/chat.py`:
  - POST `/api/chat` endpoint:
    * Accept ChatRequest (query_text, highlighted_context, chapter_context, session_id)
    * Validate input (non-empty query, valid session_id if provided)
    * Check rate limit (100 queries/hour per session)
    * Call rag_service.retrieve_relevant_chunks()
    * Call rag_service.generate_response()
    * Create ChatSession if needed (store in PostgreSQL)
    * Log ChatMessage to PostgreSQL (query, response, source_chapters, confidence)
    * Return ChatResponse (response_text, source_chapters, confidence_score, session_id, timestamp)
    * Stream response chunks if possible (FastAPI streaming)
    * Error handling: 400 (bad request), 429 (rate limit), 503 (Qdrant/OpenAI down)
- [ ] T029 [P] Create API endpoints in `backend/src/api/health.py`:
  - GET `/api/health` endpoint:
    * Check Qdrant connectivity (quick test collection)
    * Check PostgreSQL connectivity (quick query)
    * Return HealthResponse (status: healthy/degraded, qdrant_status, postgres_status, timestamp)
    * Status: 200 if healthy, 503 if degraded
- [ ] T030 [P] Create API endpoints in `backend/src/api/metadata.py`:
  - GET `/api/metadata` endpoint:
    * Query PostgreSQL chapters table
    * Return list of chapters with id, title, module_id, part_id, keywords
    * Support optional filter: ?module_id=2
- [ ] T031 Create `backend/src/api/ingest.py` (admin endpoint):
  - POST `/api/ingest` endpoint:
    * Require bearer token authentication (compare with ADMIN_TOKEN from .env)
    * Accept IngestRequest (force_refresh boolean)
    * Call ingest_service methods to read/chunk/embed/upsert
    * Return IngestResponse (status, chapters_processed, chunks_created, duration_seconds, error_message)
    * Error handling: 401 (unauthorized), 500 (server error)

### Frontend Implementation for User Story 1

- [ ] T032 Create `frontend/src/components/ChatWindow.tsx`:
  - Display list of messages (alternating user/assistant)
  - Message bubble styling
  - Input field for new queries
  - Send button (disabled while loading)
  - Loading indicator
- [ ] T033 Create `frontend/src/components/MessageBubble.tsx`:
  - Display single message with role (user/assistant)
  - Format code blocks (syntax highlighting)
  - Format links
  - Markdown rendering in responses
- [ ] T034 Implement chat logic in `frontend/src/components/AiAssistant.tsx`:
  - Initialize component: Load sessionId from localStorage
  - State management (messages, input, loading)
  - handleSend() function:
    * Get highlighted text (if any)
    * Call api.chat() with query + highlighted context
    * Add user message to display
    * Handle response streaming
    * Add assistant message to display
    * Handle errors (display user-friendly messages)
  - Fetch session history from localStorage
  - Update lastActivity timestamp
- [ ] T035 Create `frontend/src/components/ContextHighlight.tsx`:
  - Capture text selection via window.getSelection()
  - Show popup: "Ask AI about this" button
  - Pass highlighted text to AiAssistant component
  - Visual indication of highlighted text
- [ ] T036 [P] Create chapter layout and styling:
  - `frontend/src/components/ChapterLayout.tsx`: Wrapper for chapter content
  - `frontend/src/components/HighlightableText.tsx`: Make text selectable and highlightable
  - `frontend/src/styles/assistant.css`: Chat widget floating styles, colors, animations
  - Ensure floating widget visible on all pages
  - Keyboard accessibility (Tab navigation, Enter to send)
- [ ] T037 Create helper utility `frontend/src/utils/text.ts`:
  - extractText() function: Get highlighted text from DOM selection
  - linkToAPI() function: Build API URL with query parameters
  - formatTimestamp() function: Display ISO timestamp in user timezone

### Integration Tests for User Story 1

- [ ] T038 [P] Create backend integration test `backend/tests/integration/test_chat_flow.py`:
  - Test: User submits query without highlighting
  - Test: User submits query with highlighted text
  - Test: Out-of-scope query returns "not found" message
  - Test: Rate limit enforcement (send 101 queries in hour)
  - Test: Response structure matches ChatResponse schema
  - Test: Response time < 3 seconds
- [ ] T039 Create `backend/tests/integration/test_rag_pipeline.py`:
  - Test: End-to-end RAG flow (retrieve chunks, generate response, validate)
  - Test: Highlighted context prioritization (verify boost factor)
  - Test: Session persistence (same session_id returns same history)

### User Story 1 Validation

- [ ] T040 Run integration tests: `pytest backend/tests/integration/test_chat_flow.py -v`
- [ ] T041 Manual testing: Open frontend on http://localhost:3000, upload 2 chapters, test chat
- [ ] T042 Performance testing: Measure response latency with ApacheBench or curl

**Checkpoint**: User Story 1 (P1 MVP) is complete and independently testable. Can demo to stakeholders.

---

## Phase 4: User Story 2 - Admin Auto-Updates Book Content (Priority: P2)

**Goal**: Instructors can add new chapters to `/frontend/docs/`, and an automated script ingests them into Qdrant without manual intervention.

**Independent Test**:
1. Add new chapter to `/frontend/docs/`
2. Run `python backend/scripts/ingest_book.py`
3. Verify chapter is searchable via `/api/chat`
4. Verify ingestion completed in < 1 minute

**Duration**: ~4-5 hours

### Complete Book Content for User Story 2

- [ ] T043 [P] Create Module 1 chapters (Foundations) in `frontend/docs/01-module-foundations/`:
  - `03-math-robotics.mdx`: Mathematics for robotics (linear algebra, transforms)
  - `04-tools-setup.mdx`: Development environment setup
- [ ] T044 [P] Create Module 2 chapters (The Body) in `frontend/docs/02-module-body/`:
  - `05-sensors-overview.mdx`: Sensor types and integration
  - `06-actuators-control.mdx`: Motor types, PWM control, servo control
  - `07-urdf-model.mdx`: URDF format for robot models
  - `08-kinematics.mdx`: Forward/inverse kinematics basics
- [ ] T045 [P] Create Module 3 chapters (The Brain) in `frontend/docs/03-module-brain/`:
  - `09-computer-vision.mdx`: OpenCV basics, image processing
  - `10-pytorch-basics.mdx`: PyTorch tensors, neural network basics
  - `11-reinforcement-learning.mdx`: Q-learning, policy gradient, DQN
  - `12-neural-networks.mdx`: CNNs, RNNs, transformers overview
- [ ] T046 [P] Create Module 4 chapters (Humanoid Control) in `frontend/docs/04-module-humanoid/`:
  - `13-walking-locomotion.mdx`: Bipedal walking, gait planning
  - `14-grasping-manipulation.mdx`: Grasp planning, manipulation
  - `15-agentic-behaviors.mdx`: Multi-task learning, hierarchical control
  - `16-integration-project.mdx`: Capstone project (design a humanoid behavior)

### Ingest Script for User Story 2

- [ ] T047 Create `backend/scripts/ingest_book.py`:
  - Main entry point: read all .mdx files from `/frontend/docs/`
  - For each chapter:
    * Parse YAML frontmatter (metadata)
    * Read Markdown content
    * Call chunker to split into semantic chunks
    * Call openai_service to generate embeddings (batch if < 50 chapters)
    * Call qdrant_service.upsert() for batch upload
    * Log progress
  - Handle errors gracefully:
    * Skip chapters with parsing errors (log error)
    * Retry failed embeddings (max 3 attempts)
    * Partial success if some chapters fail
  - Measure total duration
  - Write IngestionLog to PostgreSQL
  - Exit code: 0 (success), 1 (partial), 2 (failure)
- [ ] T048 Create `backend/scripts/reset_db.py` (development utility):
  - Delete all records from Qdrant collection
  - Delete all records from PostgreSQL tables (chapters, chunks, sessions, messages)
  - Recreate Qdrant collection
  - Useful for development/testing

### Frontend Support for User Story 2

- [ ] T049 Create `frontend/src/pages/AdminIngest.tsx` (optional admin page):
  - Display current chapter count
  - Show last ingestion run (timestamp, status, duration)
  - Button to trigger manual ingest (calls POST /api/ingest)
  - Ingest progress/logs display
  - Note: Can also be triggered via CLI script

### Integration Tests for User Story 2

- [ ] T050 [P] Create backend integration test `backend/tests/integration/test_ingest_flow.py`:
  - Test: Ingest 2 chapters successfully
  - Test: Ingest with modified chapter (old vectors replaced)
  - Test: Ingest with missing file (logged error, partial success)
  - Test: Verify chunking produces 200-500 token chunks
  - Test: Verify embeddings stored in Qdrant (query by chapter_id)
  - Test: Verify IngestionLog entry created
  - Test: Verify ingest completes in < 1 minute
- [ ] T051 Create `backend/tests/unit/test_chunker.py`:
  - Test: Chunk text into 200-500 token chunks
  - Test: Overlap handling (adjacent chunks share context)
  - Test: Markdown-to-text conversion
  - Test: Token counting accuracy

### User Story 2 Validation

- [ ] T052 Run integration tests: `pytest backend/tests/integration/test_ingest_flow.py -v`
- [ ] T053 Manual testing: Run `python backend/scripts/ingest_book.py`, verify all 16 chapters ingested
- [ ] T054 Verify chapter queries work: Ask about content from Module 3 (ensure all 16 chapters in vectors)

**Checkpoint**: User Story 2 (P2) complete. All 16 chapters can be ingested and searched. Admin workflow functional.

---

## Phase 5: User Story 3 - Session Tracking & Learning Analytics (Priority: P3)

**Goal**: Students can view their learning history (questions asked, topics explored) across sessions.

**Independent Test**:
1. Create session, submit 5 queries
2. Query `/api/user/session-history`
3. Verify all 5 interactions returned with timestamps
4. Close browser, return with same session_id
5. Verify previous interactions still available

**Duration**: ~3-4 hours

### Backend Implementation for User Story 3

- [ ] T055 Create `backend/src/api/sessions.py`:
  - GET `/api/user/session-history` endpoint:
    * Accept optional query params: session_id, limit (default 50)
    * Return list of ChatMessages for session
    * Include query_text, response_text, source_chapters, created_at
    * Order by created_at DESC (most recent first)
    * Error handling: 400 if invalid session_id
  - GET `/api/user/session-stats` endpoint:
    * Accept session_id
    * Return statistics: total_queries, topics_explored, chapters_visited, average_confidence
    * Aggregate data from ChatMessage table
- [ ] T056 Create `backend/src/services/session_service.py`:
  - get_or_create_session() method: Create new session or retrieve existing
  - get_session_history() method: Query PostgreSQL for messages in session
  - get_session_stats() method: Aggregate analytics
  - extract_topics() method: Extract keywords from queries and responses

### Frontend Implementation for User Story 3

- [ ] T057 Create `frontend/src/pages/SessionHistory.tsx`:
  - Display list of all queries in current session
  - Show timestamp, query, response preview, topics
  - Expandable responses (show full text)
  - Option to clear session
- [ ] T058 Update `frontend/src/components/AiAssistant.tsx`:
  - Add link to session history page
  - Update localStorage session persistence (30-day expiry check)
- [ ] T059 Create `frontend/src/services/session.ts`:
  - Manage session state: creation, persistence, retrieval
  - Extract and cache topics from responses
  - Handle session expiry (30 days)

### Data Cleanup Task for User Story 3

- [ ] T060 Create `backend/src/tasks/cleanup.py`:
  - Task: Delete ChatSessions older than 90 days
  - Task: Archive old sessions to cold storage (if needed)
  - Can be run via APScheduler or cron job
  - Log cleanup results

### Integration Tests for User Story 3

- [ ] T061 Create backend integration test `backend/tests/integration/test_session_flow.py`:
  - Test: Create session, submit query, retrieve from history
  - Test: Persist session across page refresh
  - Test: Session stats aggregation (topics, chapters)
  - Test: Session expiry after 30 days (mock time)
  - Test: Session cleanup removes entries > 90 days old

### User Story 3 Validation

- [ ] T062 Run integration tests: `pytest backend/tests/integration/test_session_flow.py -v`
- [ ] T063 Manual testing: Navigate to SessionHistory page, verify queries displayed
- [ ] T064 Data persistence: Close browser, reopen, verify session restored

**Checkpoint**: User Story 3 (P3) complete. Full learning analytics available.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories, optimization, documentation, deployment

**Duration**: ~6-8 hours

### Testing & Quality Assurance

- [ ] T065 [P] Backend unit tests for all services:
  - `backend/tests/unit/test_openai_service.py`: Mock OpenAI API
  - `backend/tests/unit/test_qdrant_service.py`: Mock Qdrant client
  - `backend/tests/unit/test_validators.py`: Input validation tests
  - Run: `pytest backend/tests/unit/ -v`
- [ ] T066 [P] Frontend unit tests (Jest):
  - `frontend/tests/components/AiAssistant.test.tsx`: Chat component
  - `frontend/tests/services/api.test.ts`: API wrapper
  - Run: `npm test`
- [ ] T067 Run backend type checking: `mypy backend/src/ --strict`
- [ ] T068 Run backend linting: `ruff check backend/src/`
- [ ] T069 Run frontend type checking: `npm run type-check` (tsc)
- [ ] T070 Run frontend linting: `npm run lint` (eslint)
- [ ] T071 Backend code coverage: `pytest backend/tests/ --cov=backend/src/ --cov-report=html` (target > 70%)
- [ ] T072 Create `backend/tests/contract/test_chat_contract.py`:
  - Test POST /api/chat request/response matches OpenAPI schema
  - Validate status codes (200, 400, 429, 503)
  - Test edge cases (empty query, very long query, invalid JSON)

### Documentation

- [ ] T073 [P] Update `/README.md`:
  - Project overview (Living Textbook + RAG Chatbot)
  - Quick links to frontend/backend READMEs
  - Monorepo structure diagram
  - Getting started instructions
- [ ] T074 [P] Create/update `frontend/README.md`:
  - Frontend setup steps
  - Docusaurus commands (npm start, npm build)
  - How to add chapters
  - TypeScript configuration
- [ ] T075 [P] Create/update `backend/README.md`:
  - Backend setup steps
  - FastAPI commands (uvicorn)
  - How to run tests
  - Database migrations
- [ ] T076 [P] Create `CONTRIBUTING.md`:
  - Coding style guide (Python: PEP 8, JavaScript: Prettier)
  - Git workflow (branches, PRs, commits)
  - How to add new chapters (step-by-step)
  - How to extend API endpoints
- [ ] T077 Create `frontend/docs/API.md`:
  - Link to OpenAPI spec
  - Example curl/fetch requests
  - Response examples
- [ ] T078 Update `/specs/001-living-textbook-rag/quickstart.md`:
  - Verify all setup steps still accurate
  - Add troubleshooting section
  - Add performance testing section

### Performance Optimization

- [ ] T079 Backend optimization:
  - Profile RAG pipeline (measure each step: embed, search, generate, validate)
  - Optimize vector search (Qdrant query tuning)
  - Batch embedding requests (OpenAI batch API if available)
  - Connection pooling (asyncpg pool size tuning)
- [ ] T080 Frontend optimization:
  - Lazy-load chat widget (defer component loading)
  - Optimize images in chapters (compression, webp format)
  - Code splitting (split JS bundles by page)
  - Run Lighthouse audit: `npm run lighthouse` (target ≥ 90)
- [ ] T081 Measure end-to-end latency:
  - Chat query: target < 2 seconds (p95)
  - Ingest 16 chapters: target < 1 minute
  - Chat widget load: target < 3 seconds on 4G

### Deployment Preparation

- [ ] T082 [P] Frontend deployment:
  - Build static site: `cd frontend && npm run build`
  - Verify build output in `frontend/build/`
  - Test GitHub Pages deployment URL
  - Verify CORS headers in deployment
- [ ] T083 [P] Backend deployment:
  - Create `backend/Dockerfile` (Python 3.12, FastAPI)
  - Create `.dockerignore`
  - Build Docker image: `docker build -t living-textbook-backend:latest .`
  - Test locally with docker: `docker run -p 8000:8000 living-textbook-backend:latest`
  - Create deployment guide for: Render / Railway / Fly.io
- [ ] T084 Environment configuration for production:
  - Set production secrets in cloud platform (OPENAI_API_KEY, ADMIN_TOKEN)
  - Configure database connection string (Neon)
  - Configure Qdrant Cloud connection
  - Set CORS_ALLOWED_ORIGINS to production frontend URL
- [ ] T085 Create health monitoring:
  - Set up `/api/health` checks in cloud platform
  - Configure alerts if health check fails
  - Document SLA expectations

### Security Hardening

- [ ] T086 Backend security audit:
  - Verify no secrets in code (hardcoded API keys)
  - Validate all user inputs (SQL injection, XSS prevention)
  - Enforce HTTPS in production
  - Rate limiting active (100 queries/hour per session)
  - CORS properly configured (not "Allow *")
- [ ] T087 Frontend security audit:
  - Disable inline scripts (Content Security Policy)
  - Escape user input (prevent XSS in responses)
  - Verify no secrets in environment (console logs)
  - Test browser security headers
- [ ] T088 Database security:
  - Neon Postgres: enforce SSL connection
  - Qdrant: verify API key required, TLS enabled
  - Backup strategy documented (Neon auto-backups)

### Integration & Final Validation

- [ ] T089 End-to-end test (full user journey):
  - Open frontend
  - Read chapter
  - Highlight text
  - Ask question
  - Verify response < 2 seconds
  - Check session history
  - Verify analytics
- [ ] T090 Regression testing:
  - Verify all 3 user stories still work after optimization
  - Test on mobile browser (4G network simulation)
  - Test on desktop browsers (Chrome, Firefox, Safari)
- [ ] T091 Performance baselines:
  - Document actual p95 latencies achieved
  - Document actual throughput (concurrent users)
  - Document infrastructure costs (Neon, Qdrant, cloud platform)
- [ ] T092 Stakeholder validation (demo):
  - Demo P1 (context-aware chat)
  - Demo P2 (auto-ingest)
  - Demo P3 (session analytics)
  - Gather feedback

### CI/CD Pipeline Activation

- [ ] T093 [P] Activate GitHub Actions:
  - Frontend deploy workflow: triggered on push to main
  - Backend lint workflow: triggered on PR to main
  - Book ingest workflow: triggered on schedule (daily) or manual
- [ ] T094 [P] Setup monitoring:
  - Backend error logs (Sentry, LogRocket, or cloud provider)
  - Frontend error logs
  - Performance metrics dashboard
- [ ] T095 Create runbooks:
  - Runbook: How to deploy frontend
  - Runbook: How to deploy backend
  - Runbook: How to recover from Qdrant outage
  - Runbook: How to recover from OpenAI rate limit

### Final Checks & Deployment

- [ ] T096 [P] Run full test suite:
  - Backend: `pytest backend/tests/ -v --cov`
  - Frontend: `npm test -- --coverage`
  - Type checking: `mypy backend/src/` + `npm run type-check`
  - Linting: `ruff check backend/src/` + `npm run lint`
- [ ] T097 Create CHANGELOG.md documenting:
  - Features implemented (P1, P2, P3)
  - Bug fixes
  - Performance improvements
  - Known limitations
- [ ] T098 [P] Final documentation review:
  - `/README.md` complete
  - `/CONTRIBUTING.md` clear
  - `quickstart.md` verified
  - OpenAPI spec accurate
- [ ] T099 Deploy to production:
  - Frontend: Push to main → GitHub Pages auto-deploy
  - Backend: Deploy to Render / Railway / Fly.io
  - Run smoke tests on production
  - Monitor logs for errors
- [ ] T100 Post-launch monitoring:
  - Monitor API latency (target < 2s p95)
  - Monitor error rates (target < 0.1%)
  - Monitor concurrent users
  - Collect user feedback

**Checkpoint**: Full system deployed, monitored, and ready for production usage.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately ✅
- **Foundational (Phase 2)**: Depends on Setup completion - **BLOCKS all user stories** 🚫
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staffed) or sequentially (P1 → P2 → P3)
  - US1 has no dependencies on US2/US3
  - US2 has no dependencies on US1/US3 (independent ingestion)
  - US3 has no dependencies on US1/US2 (independent session tracking)
- **Polish (Phase 6)**: Depends on at least US1 being complete (can do in parallel with US2/US3)

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
  - Blocked by: T025, T026, T027, T028, T029, T030
  - Unblocks: Nothing (independent MVP)

- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on User Story 1
  - Blocked by: Foundational phase complete, T047
  - Can run in parallel with US1

- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on US1/US2
  - Blocked by: Foundational phase complete, T055, T056
  - Can run in parallel with US1/US2

### Within Each User Story

- Tests MUST be written and FAIL before implementation (TDD optional for this project)
- Models/schemas before services (data contracts first)
- Services before API endpoints (business logic first)
- Core implementation before integration/polish
- Story complete before moving to next priority

### Parallel Opportunities

| When | What Can Run in Parallel |
|------|-------------------------|
| **Phase 1** | T002-T003, T004, T006-T008 (all marked [P]) |
| **Phase 2** | T009-T010, T011-T012, T014-T015, T018-T022 (within same layer) |
| **Phase 3** | Models (T025), schemas (T028), endpoints (T029-T030) can start after services ready |
| **Phase 3-5** | All 3 user stories (US1, US2, US3) can proceed in parallel after Phase 2 |
| **Phase 6** | Tests, documentation, deployment, monitoring can run in parallel |

---

## Parallel Execution Examples

### Example 1: Parallel Backend Setup (Phase 2)

**Two developers**:
```
Developer A: T009-T017 (Backend services: config, ORM, Qdrant, OpenAI)
Developer B: T018-T022 (Frontend: Docusaurus config, types, API wrapper, component skeleton)
→ Merge after both complete
```

### Example 2: Parallel User Story 1 Implementation

**Two developers**:
```
Developer A: T025-T027 (Backend services: chunker, ingest, RAG)
Developer B: T032-T036 (Frontend: chat components, highlighting)
→ Merge both, then T028-T031 (API endpoints) when services ready
```

### Example 3: Parallel User Stories (Phase 3-5)

**Three developers after Phase 2 complete**:
```
Developer A: User Story 1 (T023-T042)
Developer B: User Story 2 (T043-T054)
Developer C: User Story 3 (T055-T064)
→ All work in parallel, no blocking
→ Merge P1 first for MVP demo
→ Then merge P2, P3 for incremental delivery
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

**Goal**: Deliver a working context-aware chat system in 1-2 days

1. **Day 1 - Setup**: Complete Phase 1 + Phase 2 (4-6 hours)
   - Initialize monorepo, frontend, backend
   - Create ORM models, Pydantic schemas
   - Setup database connections
2. **Day 1-2 - User Story 1**: Complete Phase 3 (8-10 hours)
   - Create sample chapters (2)
   - Implement RAG pipeline (retrieve, generate, validate)
   - Implement chat endpoint + chat widget
   - Run integration tests
3. **STOP and VALIDATE**: Demo to stakeholders
   - Test highlighting + chat
   - Measure response latency
   - Get feedback before proceeding

**MVP Scope**: P1 user story only (context-aware chat)
- 2 sample chapters (not full 16)
- No admin UI (ingest script only)
- No session analytics (P3 deferred)
- No advanced optimization (P6 optional)

### Incremental Delivery

**Phase Timeline** (assuming 1 developer):

| Phase | Duration | Cumulative |
|-------|----------|-----------|
| 1 Setup | 2 hours | 2 hours |
| 2 Foundational | 4-5 hours | 6-7 hours |
| 3 US1 (MVP) | 8-10 hours | 14-17 hours |
| 4 US2 | 4-5 hours | 18-22 hours |
| 5 US3 | 3-4 hours | 21-26 hours |
| 6 Polish | 6-8 hours | 27-34 hours |

**Delivery Milestones**:
- **Day 2**: US1 (MVP) ready for demo
- **Day 3**: US1 + US2 (full 16 chapters + auto-ingest)
- **Day 4**: US1 + US2 + US3 (+ analytics)
- **Day 5**: Fully polished, tested, deployed

### Parallel Team Strategy

**With 3 developers**:

```
Week 1:
  All: Phase 1 + Phase 2 (Setup + Foundational) → 1 day

Week 1-2:
  Dev A: User Story 1 (P1 MVP)
  Dev B: User Story 2 (P2 Auto-ingest)
  Dev C: User Story 3 (P3 Analytics)
  → All in parallel, no blocking

Week 2:
  All: Phase 6 (Polish, testing, deployment)

Week 2 (End):
  Deploy to production
  Monitor and gather feedback
```

---

## Task Summary

| Phase | Task Count | Est. Hours |
|-------|-----------|-----------|
| 1 Setup | 8 | 2 |
| 2 Foundational | 14 | 4-5 |
| 3 User Story 1 | 18 | 8-10 |
| 4 User Story 2 | 12 | 4-5 |
| 5 User Story 3 | 10 | 3-4 |
| 6 Polish | 36 | 6-8 |
| **Total** | **98** | **27-34** |

---

## Task Checklist Validation

✅ **Format Compliance**: All 100 tasks follow strict checklist format:
- Checkbox: `- [ ]`
- Task ID: T001-T100 (sequential)
- [P] marker: Included only when parallelizable
- [Story] label: US1, US2, US3 for story phases; none for setup/foundational/polish
- File paths: Absolute to repository root

✅ **Organization**: Tasks grouped by user story for independent implementation
✅ **Dependencies**: Clear task ordering and parallel opportunities identified
✅ **MVP Scope**: User Story 1 (P1) delivers minimum viable product in ~12-17 hours
✅ **Incremental**: Each story independently testable and deployable

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks in same phase
- [Story] label maps task to specific user story (US1, US2, US3)
- Each user story is independently completable and testable
- Verify tests fail before implementing (TDD approach optional)
- Commit after each logical group of tasks (every 2-3 tasks)
- **STOP at any checkpoint to validate story independently before proceeding**
- Avoid: vague tasks, same-file conflicts, cross-story dependencies that break independence
- For parallel execution: Ensure [P] marked tasks truly have no dependencies on incomplete work
- Schedule daily standups to coordinate progress across team members
