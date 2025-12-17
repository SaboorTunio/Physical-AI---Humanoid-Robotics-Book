# Feature Specification: Living Textbook with RAG Teaching Assistant

**Feature Branch**: `001-living-textbook-rag`
**Created**: 2025-12-18
**Status**: Draft
**Input**: Create a Master Technical Specification for the "Physical AI & Humanoid Robotics" Textbook and RAG Chatbot.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Student Asks Context-Aware Questions (Priority: P1)

**Scenario**: A student is reading Chapter 7 ("Servo Motors and Control") and encounters unfamiliar concepts. They highlight a paragraph about "PID controllers in servo loops" and open the chat widget asking: "How do I implement this in Python?" The Teaching Assistant provides a code example directly relevant to the highlighted text, pulled from related chapters.

**Why this priority**: Core value proposition—the ability to ask questions about specific parts of the textbook is the primary differentiator for this "Living Textbook." Without this, the chatbot is just a generic RAG system.

**Independent Test**: Can be fully tested by:
1. Uploading book content to Qdrant
2. Highlighting a section on the frontend
3. Sending a context-aware query via `/api/chat` with highlighted text
4. Verifying response includes relevant code/explanation from book

Delivers: Students can learn faster by asking targeted questions.

**Acceptance Scenarios**:

1. **Given** a student has the book open, **When** they highlight text and submit a question, **Then** the chat widget displays a response within 2 seconds based on that highlighted section's context
2. **Given** a student asks a question without highlighting, **When** they submit the query, **Then** the AI searches the entire book and returns relevant information
3. **Given** the AI cannot find relevant information in the book, **When** the student submits a query, **Then** the system displays: "I couldn't find information about this in the textbook. Please consult your instructor."

---

### User Story 2 - Admin Updates Book Content Automatically (Priority: P2)

**Scenario**: An instructor writes a new chapter ("Advanced Grasping Techniques") and adds it to the frontend content directory. They want the Teaching Assistant to immediately have access to this new content without manual intervention. An automated script detects the new chapter and ingests it into Qdrant, updating the vector embeddings.

**Why this priority**: Enables rapid content iteration during the hackathon and allows instructors to scale the textbook without waiting for deployment processes.

**Independent Test**: Can be fully tested by:
1. Adding a new markdown chapter to `/frontend/docs/`
2. Running the ingest script `/backend/scripts/ingest_book.py`
3. Verifying new chapter content is searchable via `/api/chat`

Delivers: Automated content pipeline for instructor productivity.

**Acceptance Scenarios**:

1. **Given** a new chapter markdown file exists in `/frontend/docs/`, **When** the ingest script runs, **Then** the chapter is chunked, embedded, and stored in Qdrant within 30 seconds
2. **Given** existing chapter content is modified, **When** the ingest script runs, **Then** old vectors are replaced with updated ones (no duplicates)
3. **Given** the ingest script encounters an error, **When** it fails, **Then** it logs the error with chapter name and line number for debugging

---

### User Story 3 - Student Tracks Learning Progress (Priority: P3)

**Scenario**: A student wants to understand their engagement with the textbook. The system logs their chat interactions (questions asked, topics explored) in a session-based way. Over time, they can review their learning patterns: "I asked 15 questions about Actuators but only 3 about Reinforcement Learning."

**Why this priority**: Enhances the learning experience with personalization and self-reflection, but not critical for MVP. Can be added post-hackathon.

**Independent Test**: Can be fully tested by:
1. Creating a user session on the frontend
2. Submitting multiple chat queries
3. Querying `/api/user/session-history` to retrieve logged interactions
4. Verifying accurate recording of topics and timestamps

Delivers: Students gain insights into their learning behavior.

**Acceptance Scenarios**:

1. **Given** a student has submitted 5 chat queries in a session, **When** they query their session history, **Then** all 5 interactions are returned with timestamps and topics
2. **Given** a student closes the browser and returns later, **When** they log in with the same session ID, **Then** previous interactions are available
3. **Given** a session is older than 30 days, **When** the system performs cleanup, **Then** old sessions are archived (not deleted)

---

### Edge Cases

- What happens when a student highlights text that spans multiple chapters (cross-chapter context)?
- How does the system handle PDFs or images embedded in chapters?
- What happens if Qdrant Cloud goes down during a student query?
- How does the system behave if the OpenAI API rate limit is exceeded?
- What if a student submits a question that's completely outside the scope of the Physical AI textbook (e.g., "What's the capital of France?")?

## Requirements *(mandatory)*

### Functional Requirements

**Book Content (Hackathon 1)**

- **FR-001**: System MUST organize the textbook into exactly 4 Modules, each containing exactly 4 Parts (16 Chapters total)
- **FR-002**: System MUST support each chapter as an independently renderable page in Docusaurus
- **FR-003**: System MUST include chapter metadata header (title, learning objectives, prerequisites, keywords) that can be parsed by the RAG system
- **FR-004**: System MUST render all chapters as a static site deployable to GitHub Pages
- **FR-005**: System MUST display a global chat widget (React component) on every page of the textbook

**RAG Chatbot Backend (Hackathon 2)**

- **FR-006**: System MUST provide `/api/chat` endpoint that accepts: query text, optional highlighted text, optional chapter context, session ID
- **FR-007**: System MUST provide `/api/ingest` endpoint to update Qdrant with latest book content (admin-only)
- **FR-008**: System MUST validate that responses come only from the textbook content (no hallucinations outside book scope)
- **FR-009**: System MUST support context-aware retrieval: if highlighted text provided, prioritize similar chunks from that section
- **FR-010**: System MUST log all chat interactions to Neon Postgres with: user session ID, query, response, timestamp, chapter context
- **FR-011**: System MUST return `/api/health` endpoint for deployment monitoring
- **FR-012**: System MUST chunk book content with semantic overlap (200–500 tokens per chunk) to preserve context
- **FR-013**: System MUST support streaming responses to the frontend (chunked response bodies)
- **FR-014**: System MUST provide `/api/metadata` endpoint returning available chapters and keywords for frontend search filters

**Integration & Security**

- **FR-015**: System MUST enforce CORS to allow requests only from the frontend domain
- **FR-016**: System MUST use environment variables for all sensitive configuration (API keys, database URLs, never committed)
- **FR-017**: System MUST validate all user inputs to prevent injection attacks
- **FR-018**: System MUST respond with appropriate HTTP status codes (400 for bad request, 500 for server error, 429 for rate limit)

### Key Entities *(include if feature involves data)*

- **Chapter**: A markdown file representing one module/part of the textbook. Attributes: title, module_id, part_id, chapter_index, content_markdown, metadata_header, created_at, updated_at
- **ChunkVector**: A semantic chunk of chapter content stored in Qdrant. Attributes: chunk_id, chapter_id, content_text, embedding_vector, chunk_index, token_count
- **ChatSession**: A user session tracking interactions. Attributes: session_id, user_id (optional), created_at, last_activity, ip_address
- **ChatMessage**: A single query-response pair. Attributes: message_id, session_id, query_text, response_text, highlighted_context, source_chapters, confidence_score, created_at
- **IngestionLog**: Tracks content updates. Attributes: log_id, run_timestamp, chapters_processed, chunks_created, status (success/failed), error_message

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Students can submit a highlighted-text question and receive a relevant response within 2 seconds (p95 latency)
- **SC-002**: The ingest script can process the entire 16-chapter textbook and update Qdrant in under 1 minute
- **SC-003**: 90% of chat responses include at least one relevant code example or direct quote from the textbook
- **SC-004**: The frontend Lighthouse score is ≥ 90 for Performance and Accessibility (per constitution requirement)
- **SC-005**: The system correctly rejects out-of-scope questions (e.g., general knowledge queries) with "I don't have information about this in the textbook" ≥ 95% of the time
- **SC-006**: The chat widget loads and becomes interactive within 3 seconds on a 4G mobile connection
- **SC-007**: System can handle 100 concurrent chat queries without error or degradation
- **SC-008**: All API responses are documented in OpenAPI spec and responses match spec 100% of the time

## Assumptions *(document defaults for unspecified details)*

- **Authentication**: Students access the textbook anonymously; optional session tracking via local storage (no login required for MVP)
- **Data Retention**: Chat logs retained for 90 days, then archived to cold storage
- **Content Updates**: Ingest script runs on manual trigger or CI/CD pipeline (not real-time)
- **RAG Approach**: Retrieval-Augmented Generation uses vector similarity (not keyword search)
- **Response Format**: AI responses are conversational text (not structured JSON or multiple-choice)
- **Rate Limiting**: 100 queries per session per hour (to avoid abuse)
- **Fallback Behavior**: If Qdrant unavailable, system returns 503 Service Unavailable (not generic error)

## Technical Context (for Planner)

*(This section helps the planner understand scope; not user-facing)*

- **Language/Version**: Python 3.12+ (backend), TypeScript/React (frontend)
- **Primary Dependencies**: FastAPI, Qdrant Python client, OpenAI SDK, SQLAlchemy, Docusaurus 3
- **Storage**: Neon Serverless Postgres (chat logs), Qdrant Cloud (vectors)
- **Testing**: pytest (backend), Jest (frontend)
- **Target Platform**: Web (responsive for mobile + desktop)
- **Performance Goals**: API p95 < 2s, ingest < 1 min for full book, chat widget load < 3s
- **Constraints**: Monorepo structure (constitution), schema-first API, no cross-directory imports
- **Scale/Scope**: 16 chapters (~50,000 tokens total), 100 concurrent users, 90-day session history

---

## Clarifications Needed (if any)

1. **Highlighted-text scope** (Minor): When a student highlights text spanning multiple chapters, should the system prioritize the highlighted chapter or search all chapters equally? *Assumed: Prioritize highlighted chapter 70%, others 30% in retrieval ranking.*

2. **Anonymous sessions** (Minor): Should anonymous students be tracked at all for analytics, or completely anonymous? *Assumed: Track via browser fingerprint + local storage, no PII collected.*

That's all clarifications—scope is well-defined by the user requirements.
