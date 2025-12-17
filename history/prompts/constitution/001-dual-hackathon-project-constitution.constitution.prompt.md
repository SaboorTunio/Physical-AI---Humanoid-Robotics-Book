---
id: 001
title: Dual-Hackathon Project Constitution
stage: constitution
date: 2025-12-18
surface: agent
model: claude-sonnet-4-5
feature: none
branch: main
user: developer
command: /sp.constitution
labels: ["constitution", "hackathon", "monorepo", "physical-ai", "rag-chatbot"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

Create a Unified Constitution for a Dual-Hackathon Project: "Physical AI Book + RAG Chatbot".

1. SYSTEM ARCHITECTURE (MONOREPO):
   - The project must have two main directories:
     - /frontend: Docusaurus v3 (React, TypeScript) for the book.
     - /backend: FastAPI (Python 3.12+) for the RAG Chatbot.

2. HACKATHON 1 REQUIREMENTS (THE BOOK):
   - Structure: Exactly 4 Modules x 4 Parts (16 Chapters total).
   - Topic: Physical AI & Humanoid Robotics.
   - Output: Static site deployable to GitHub Pages.

3. HACKATHON 2 REQUIREMENTS (THE BRAIN):
   - Tech Stack (STRICT):
     - API: FastAPI.
     - AI Logic: OpenAI Agents SDK / ChatKit SDK.
     - Vector DB: Qdrant Cloud (Free Tier).
     - Database: Neon Serverless Postgres.
   - Core Features:
     - RAG Pipeline: Ingest book content into Qdrant.
     - Chat Interface: React widget embedded in the Docusaurus layout.
     - Context Feature: Users can highlight text in the book to ask specific questions about it.

4. QUALITY & COMPLIANCE:
   - "Docs-as-Code" for the book content.
   - "Schema-First" for the API (OpenAPI spec).
   - Security: Never commit API keys; use .env files.

## Response snapshot

Created comprehensive constitution v1.0.0 for dual-hackathon project with 8 core principles:

1. **Monorepo Structure**: Strict `/frontend` (Docusaurus) + `/backend` (FastAPI) separation
2. **Book Structure Mandate**: 4 Modules × 4 Parts = 16 Chapters, docs-as-code workflow
3. **Strict Tech Stack**: FastAPI, OpenAI Agents SDK, Qdrant Cloud, Neon Postgres (non-negotiable)
4. **RAG Pipeline Requirements**: Content ingestion, chat widget, context-aware queries
5. **Schema-First API Design**: OpenAPI spec before implementation, Pydantic validation
6. **Security & Secrets Management**: .env files, no committed credentials
7. **Testing & Quality Gates**: CI/CD checks for TypeScript, linting, tests, 70% backend coverage
8. **Docs-as-Code**: Git workflow for book chapters with peer review

Additional sections cover:
- Architecture Requirements (deployment, data flow, integration points)
- Quality & Compliance (documentation standards, performance targets, accessibility)
- Development Workflow (branch strategy, commit conventions, code review checklist)
- Governance (amendment process, versioning policy, compliance review)

Constitution includes Sync Impact Report identifying template alignment needs.

## Outcome

- ✅ Impact: Constitution v1.0.0 ratified with 8 principles covering monorepo structure, tech stack constraints, RAG pipeline, security, testing, and docs-as-code workflows
- 🧪 Tests: Template validation checks required for plan-template.md, spec-template.md, tasks-template.md
- 📁 Files: Created .specify/memory/constitution.md with complete principles and governance
- 🔁 Next prompts: Review and validate template alignment with new constitution principles; create initial project structure following monorepo mandate
- 🧠 Reflection: Constitution successfully captures dual-hackathon requirements with clear, testable principles. All placeholders resolved. Version 1.0.0 establishes baseline for project governance.

## Evaluation notes (flywheel)

- Failure modes observed: None - constitution template fully populated with no remaining placeholders
- Graders run and results (PASS/FAIL): Manual validation PASS - all principles declarative, testable, and aligned with user requirements
- Prompt variant (if applicable): N/A - initial constitution creation
- Next experiment (smallest change to try): Validate constitution principles against existing templates; consider adding CI/CD pipeline specifications as separate ADR if implementation details needed
