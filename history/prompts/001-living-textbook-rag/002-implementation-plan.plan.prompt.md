---
id: 002
title: Implementation Plan for Living Textbook
stage: plan
date: 2025-12-18
surface: agent
model: claude-haiku-4-5-20251001
feature: living-textbook-rag
branch: 001-living-textbook-rag
user: developer
command: /sp.plan
labels: ["plan", "architecture", "monorepo", "rag", "fastapi", "docusaurus"]
links:
  spec: specs/001-living-textbook-rag/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-living-textbook-rag/plan.md
 - specs/001-living-textbook-rag/data-model.md
 - specs/001-living-textbook-rag/contracts/openapi.yaml
 - specs/001-living-textbook-rag/quickstart.md
tests:
 - none
---

## Prompt

Create a Comprehensive Development Plan for the "Physical AI Book & RAG Chatbot" Monorepo.

Based on the Specification, outline the architecture for these two distinct systems:

1. MONOREPO ARCHITECTURE (STRICT):
   - Define the root structure with two main directories:
     - `/frontend`: The Docusaurus v3 application.
     - `/backend`: The FastAPI Python application.
   - List the root-level configuration files needed (e.g., `requirements.txt` for Python, `package.json` for Node).

2. FRONTEND IMPLEMENTATION (THE BOOK):
   - **Setup:** Steps to initialize Docusaurus with TypeScript and Infima styling.
   - **Content Structure:** detailed file tree for the 16 Chapters (Modules 1-4) using numbered folders (e.g., `docs/01-module-foundations/01-intro.mdx`).
   - **AI Integration:** Plan for a custom React component (`<AiAssistant />`) that floats on the page and sends user queries to the backend.

3. BACKEND IMPLEMENTATION (THE BRAIN):
   - **Tech Stack:** FastAPI, OpenAI Agents SDK, Qdrant Client, Neon Postgres driver.
   - **Ingestion Pipeline:** Design a specific Python script (`scripts/ingest_book.py`) that reads all Markdown files from the frontend and indexes them into Qdrant.
   - **API Endpoints:** Define the schema for `POST /api/chat` (accepts user message + page context) and `POST /api/reset-db`.

4. DEPLOYMENT & WORKFLOW:
   - **Frontend:** Steps to configure the GitHub Actions workflow for deploying the book to GitHub Pages.
   - **Local Dev:** Instructions on how to run both servers simultaneously (e.g., `npm start` + `uvicorn main:app`).

## Response snapshot

Created comprehensive 3-phase implementation plan:

**Phase 0: Research & Design**
- 7 architectural decisions documented (Docusaurus + TypeScript, semantic chunking, OpenAI SDK choice, async database drivers, React Context state, rate limiting, error handling)
- All technical unknowns resolved
- Best practices for each technology component established

**Phase 1: Design & Contracts** (this plan document)
- Complete monorepo structure (frontend/ + backend/ with 40+ total files)
- 5 key data entities with full schemas (Chapter, ChunkVector, ChatSession, ChatMessage, IngestionLog)
- 4 core API endpoints with full OpenAPI 3.1 specification
- Frontend architecture (React hooks + context, floating chat widget)
- Backend architecture (async FastAPI, RAG pipeline, ingestion flow)

**Phase 2: Development Workflow**
- Local setup instructions (Python venv, npm, environment variables)
- CI/CD pipeline structure (GitHub Actions for frontend + backend)
- Testing strategy (pytest, Jest, mypy, ruff linting)
- Deployment targets (GitHub Pages for frontend, cloud platform for backend)

**Phase 3: Risk Analysis**
- 5 identified risks with mitigation strategies
- Success criteria mapped to design components
- Architecture diagram showing data flow

**Supporting Artifacts** (generated in Phase 1):
1. **plan.md** (5,000+ words): Full implementation architecture
2. **data-model.md**: 5 entity schemas with validation, relationships, state transitions
3. **contracts/openapi.yaml**: Complete REST API specification (4 endpoints, 6 schema definitions)
4. **quickstart.md**: Step-by-step developer setup (from cloning to end-to-end test)

**Constitution Compliance**:
✅ All 8 constitutional principles pass gate review
✅ Monorepo structure enforced (I)
✅ 16-chapter book mandate (II)
✅ Strict tech stack (III)
✅ RAG pipeline requirements (IV)
✅ Schema-first API design (V)
✅ Security via environment variables (VI)
✅ Testing & quality gates (VII)
✅ Docs-as-code workflow (VIII)

## Outcome

- ✅ Impact: Complete implementation plan ready for coding phase. All architecture decisions documented with rationale. No ambiguities remain (0 NEEDS CLARIFICATION markers).
- 🧪 Tests: Schema-first API enables contract testing. Data model supports unit/integration testing. Quickstart includes test commands.
- 📁 Files: plan.md (5K words), data-model.md (3K words), openapi.yaml (full REST spec), quickstart.md (setup guide)
- 🔁 Next prompts: Run `/sp.tasks` to generate detailed implementation tasks organized by user story (P1, P2, P3)
- 🧠 Reflection: Plan provides clear bridge from specification to implementation. Phase 0 (research) resolved all technical unknowns. Phase 1 (design) specifies exact data models, API contracts, and component architecture. Quickstart makes setup friction-free.

## Evaluation notes (flywheel)

- Failure modes observed: None—plan complete with full technical depth
- Graders run and results (PASS/FAIL): Manual validation PASS—all requirements mapped to design components, no gaps, constitution check passed
- Prompt variant (if applicable): N/A—single comprehensive plan
- Next experiment (smallest change to try): Generate tasks via `/sp.tasks` command; then begin Phase 3 implementation (Red-Green-Refactor TDD cycle)
