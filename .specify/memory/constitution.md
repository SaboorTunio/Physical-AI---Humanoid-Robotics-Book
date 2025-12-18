<!--
Sync Impact Report:
- Version change: [UNVERSIONED] → 1.0.0
- Rationale: Initial constitution for dual-hackathon project (Physical AI Book + RAG Chatbot)
- Modified principles: N/A (new constitution)
- Added sections: All core principles, architecture requirements, quality gates, governance
- Removed sections: None
- Templates requiring updates:
  ✅ plan-template.md: Constitution Check section will reference these principles
  ✅ spec-template.md: Requirements aligned with docs-as-code and schema-first
  ✅ tasks-template.md: Task phases aligned with monorepo and security principles
- Follow-up TODOs: None
-->

# Physical AI Book + RAG Chatbot Constitution

## Core Principles

### I. Monorepo Structure (NON-NEGOTIABLE)

The project MUST maintain exactly two top-level directories:

- `/frontend`: Docusaurus v3 (React, TypeScript) for the Physical AI & Humanoid Robotics book
- `/backend`: FastAPI (Python 3.12+) for the RAG Chatbot

**Rationale**: Clear separation of concerns between content delivery (frontend) and AI capabilities (backend) while maintaining unified version control, shared configuration, and coordinated deployments. This structure enforces the dual-hackathon requirement and prevents architectural drift.

**Rules**:
- No source code outside `/frontend` or `/backend` (root-level scripts for orchestration only)
- Shared configuration files (`.env.example`, `.gitignore`, deployment configs) live at monorepo root
- Each directory MUST have its own `README.md`, dependency management, and testing setup
- Cross-directory imports are FORBIDDEN; communication occurs via API contracts only

### II. Book Structure Mandate

The Physical AI & Humanoid Robotics book MUST be organized as:

- **4 Modules** × **4 Parts** = **16 Chapters** (exact count, non-negotiable)
- Deployable as a static site to GitHub Pages
- Follows "Docs-as-Code" principles: content as markdown, version-controlled, peer-reviewed

**Rationale**: Hackathon 1 requirement for structured, comprehensive coverage of Physical AI topics. Fixed structure ensures completeness and aids navigation.

**Rules**:
- Each chapter: standalone markdown file in `/frontend/docs/`
- Module/Part/Chapter hierarchy enforced in Docusaurus config (`sidebars.js`)
- Every chapter MUST include: learning objectives, content, examples, and summary
- Images/diagrams stored in `/frontend/static/img/` with descriptive filenames

### III. Strict Tech Stack (Backend)

Backend MUST use ONLY the following technologies:

- **API Framework**: FastAPI (Python 3.12+)
- **AI Logic**: OpenAI Agents SDK or ChatKit SDK
- **Vector Database**: Qdrant Cloud (Free Tier)
- **Relational Database**: Neon Serverless Postgres

**Rationale**: Hackathon 2 requirement for modern, scalable, cloud-native AI infrastructure. These tools provide production-grade RAG capabilities within free tier constraints.

**Rules**:
- No alternative frameworks (Flask, Django, etc.) permitted for API
- No alternative vector stores (Pinecone, Weaviate, ChromaDB, etc.) permitted
- No alternative databases (SQLite, MySQL, local Postgres, etc.) permitted
- All API endpoints MUST be defined in OpenAPI spec (`backend/openapi.yaml`) BEFORE implementation

### IV. RAG Pipeline Requirements

The RAG (Retrieval-Augmented Generation) system MUST implement:

1. **Content Ingestion**: Parse and chunk book markdown into Qdrant vector embeddings
2. **Chat Interface**: React widget embedded in Docusaurus layout
3. **Context-Aware Queries**: Users can highlight text in the book to ask specific questions about it

**Rationale**: Core value proposition of Hackathon 2 - making the static book interactive and intelligent.

**Rules**:
- Ingestion pipeline: automated script in `/backend/scripts/ingest_book.py`
- Embeddings: OpenAI `text-embedding-3-small` (cost-effective, sufficient quality)
- Chunking strategy: semantic splitting (aim for 200-500 tokens per chunk, preserve context)
- Context feature: frontend sends highlighted text + surrounding paragraphs to backend
- Chat widget: non-blocking, accessible (keyboard navigation, screen reader support)

### V. Schema-First API Design

ALL backend endpoints MUST be defined in OpenAPI spec (`backend/openapi.yaml`) BEFORE implementation.

**Rationale**: Contract-driven development prevents frontend/backend misalignment, enables parallel development, and serves as living documentation.

**Rules**:
- Endpoint signature (path, method, parameters, request/response schemas) in OpenAPI spec
- Use Pydantic models for request/response validation in FastAPI
- No undocumented endpoints - spec is the source of truth
- Breaking changes require versioning (`/api/v1/`, `/api/v2/`)
- Generate TypeScript types from OpenAPI spec for frontend (use `openapi-typescript`)

### VI. Security & Secrets Management

API keys, database credentials, and secrets MUST NEVER be committed to version control.

**Rationale**: Security best practice to prevent credential leakage, especially in public repositories.

**Rules**:
- All secrets in `.env` files (never committed; add to `.gitignore`)
- Provide `.env.example` files with dummy values and comments
- Use environment variables in code: `os.getenv('API_KEY')` (Python), `process.env.API_KEY` (TypeScript)
- Deployment environments (Vercel, Render, etc.) inject secrets via platform-specific mechanisms
- Rotate API keys immediately if accidentally exposed

### VII. Testing & Quality Gates

Code changes MUST pass automated checks before merging:

**Frontend**:
- TypeScript compilation (`tsc --noEmit`)
- Linting (`eslint`)
- Build validation (`docusaurus build`)

**Backend**:
- Type checking (`mypy backend/`)
- Linting (`ruff check backend/`)
- Unit tests for core logic (`pytest backend/tests/`)
- API contract validation (response schemas match OpenAPI spec)

**Rationale**: Prevents broken deployments, maintains code quality, and catches errors early.

**Rules**:
- CI/CD pipeline MUST run all checks on every pull request
- Failing checks block merging (no override without documented justification)
- Minimum test coverage: 70% for backend business logic (RAG pipeline, query handling)
- Frontend tests: optional but encouraged for complex React components

### VIII. Docs-as-Code for Book Content

Book chapters are source-controlled markdown files following Git workflow:

**Rationale**: Version control for content enables collaborative editing, change tracking, and rollback capabilities.

**Rules**:
- Branch naming: `content/module-X-part-Y` for chapter additions
- Peer review required: at least one approval before merging chapter content
- Commit messages: `docs(module-X): add chapter on [topic]`
- No direct commits to `main` - all changes via pull requests
- Use GitHub Issues for content planning and tracking

## Architecture Requirements

### Deployment Targets

- **Frontend**: GitHub Pages (static site, auto-deploy from `main` branch via GitHub Actions)
- **Backend**: Cloud platform with Python 3.12+ support (Render, Railway, Fly.io, or Vercel Serverless Functions)

**Constraints**:
- Frontend build output MUST be in `/frontend/build/` (Docusaurus default)
- Backend MUST expose health check endpoint at `/api/health`
- CORS: backend MUST allow requests from frontend domain (configure in FastAPI middleware)

### Data Flow

1. **Book Content → Qdrant**: Ingestion script runs on content updates (manual or CI-triggered)
2. **User Query → Backend API**: Chat widget sends query + optional context to `/api/v1/chat`
3. **Backend → Qdrant**: Retrieve relevant chunks via vector similarity search
4. **Backend → OpenAI**: Construct prompt with retrieved context + user query
5. **Backend → Frontend**: Stream response back to chat widget
6. **User Activity → Neon Postgres**: Log queries, feedback, and usage metrics

### Integration Points

- **Frontend ↔ Backend**: REST API over HTTPS (defined in OpenAPI spec)
- **Backend ↔ Qdrant**: Qdrant Python client (`qdrant-client`)
- **Backend ↔ Neon Postgres**: SQLAlchemy ORM or raw `psycopg2`
- **Backend ↔ OpenAI**: OpenAI Agents SDK or ChatKit SDK

## Quality & Compliance

### Documentation Standards

Each directory MUST include:

- `README.md`: Setup instructions, architecture overview, deployment guide
- `CONTRIBUTING.md`: How to add chapters (frontend) or extend API (backend)
- `/frontend/docs/`: Book content in markdown
- `/backend/docs/`: API documentation (auto-generated from OpenAPI spec)

### Performance Targets

- **Frontend**: Lighthouse score ≥ 90 (Performance, Accessibility, Best Practices)
- **Backend**: API response time < 2 seconds (p95) for chat queries
- **Vector Search**: Qdrant query latency < 500ms (p95)

### Accessibility

- Frontend MUST meet WCAG 2.1 AA standards
- Chat widget: keyboard navigable, screen reader compatible
- Semantic HTML throughout the book content

## Development Workflow

### Branch Strategy

- `main`: Production-ready code (protected, requires PR + CI checks)
- `develop`: Integration branch for features (optional, for multi-developer teams)
- Feature branches: `feature/[description]` (e.g., `feature/chat-widget`, `feature/module-1`)
- Content branches: `content/module-X-part-Y` (for book chapters)

### Commit Conventions

Follow Conventional Commits specification:

- `feat:` New feature (e.g., `feat(backend): add context-aware query endpoint`)
- `fix:` Bug fix (e.g., `fix(frontend): resolve chat widget z-index issue`)
- `docs:` Documentation/content changes (e.g., `docs(module-2): add chapter on actuators`)
- `chore:` Maintenance (e.g., `chore(deps): update FastAPI to 0.115.0`)

### Code Review Checklist

Before approving any PR, verify:

- [ ] All CI checks pass (linting, type checking, tests, build)
- [ ] Code follows project structure (no cross-directory imports)
- [ ] New API endpoints documented in OpenAPI spec
- [ ] No secrets committed (verify `.env` not added)
- [ ] README updated if setup process changed
- [ ] For backend: Pydantic models used for validation
- [ ] For frontend: TypeScript types correctly used (no `any`)

## Governance

### Constitution Authority

This constitution supersedes all other practices and conventions. When in doubt, refer to this document.

### Amendment Process

1. Propose change via GitHub Issue with label `constitution-amendment`
2. Discuss rationale, impact on existing code, and migration plan
3. Approval required: project maintainer(s) consensus
4. Update constitution version per semantic versioning (see below)
5. Propagate changes to dependent templates and documentation
6. Announce amendment to all contributors

### Versioning Policy

Constitution version follows semantic versioning:

- **MAJOR** (X.0.0): Backward-incompatible changes (e.g., removing a principle, changing tech stack)
- **MINOR** (0.X.0): New principles added or existing ones materially expanded
- **PATCH** (0.0.X): Clarifications, wording improvements, typo fixes

### Compliance Review

- All pull requests MUST verify compliance with constitution principles
- Monthly review: check for drift, identify areas needing clarification
- Violations require explicit justification in the Complexity Tracking section of `plan.md`

### Complexity Justification

If a feature violates constitutional principles (e.g., requires additional tech stack components), document in `specs/[feature]/plan.md`:

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [Principle violated] | [Specific requirement] | [Why mandated approach insufficient] |

Example:
| Add Redis cache | Sub-second query response impossible with Qdrant alone | Qdrant query latency tests show 1.5s p95; user experience requirement is <500ms |

**Version**: 1.0.0 | **Ratified**: 2025-12-18 | **Last Amended**: 2025-12-18
