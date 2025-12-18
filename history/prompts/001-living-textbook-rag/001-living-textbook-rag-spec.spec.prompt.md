---
id: 001
title: Living Textbook RAG Specification
stage: spec
date: 2025-12-18
surface: agent
model: claude-haiku-4-5-20251001
feature: living-textbook-rag
branch: 001-living-textbook-rag
user: developer
command: /sp.specify
labels: ["spec", "textbook", "rag", "chatbot", "hackathon", "physical-ai"]
links:
  spec: specs/001-living-textbook-rag/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-living-textbook-rag/spec.md
 - specs/001-living-textbook-rag/checklists/requirements.md
tests:
 - none
---

## Prompt

Create a Master Technical Specification for the "Physical AI & Humanoid Robotics" Textbook and RAG Chatbot.

1. PROJECT OVERVIEW:
   - We are building a "Living Textbook" where students read about Physical AI and can chat with the book itself.
   - The system consists of a Frontend (Docusaurus) and a Backend (FastAPI + RAG).

2. PART A: THE TEXTBOOK SPECIFICATIONS (Hackathon 1)
   - Structure: 4 Modules x 4 Parts (16 Chapters total).
   - Module 1: "Foundations" (Python, Simulation setup, Math for Robotics).
   - Module 2: "The Body" (Sensors, Actuators, URDF, Kinematics).
   - Module 3: "The Brain" (Computer Vision, PyTorch Basics, Reinforcement Learning).
   - Module 4: "Humanoid Control" (Walking, Grasping, Agentic Behaviors).
   - Feature Requirement: Every chapter must have a unique "metadata header" that the RAG system can read later.

3. PART B: THE INTELLIGENT CHATBOT SPECIFICATIONS (Hackathon 2)
   - Goal: An embedded "Teaching Assistant" that answers questions using ONLY the book's content.
   - Core Architecture:
     - Database: Neon Serverless Postgres (for chat logs and user sessions).
     - Vector Store: Qdrant Cloud Free Tier (to store the book's text chunks).
     - LLM: OpenAI Agents SDK (using gpt-4o-mini or similar).
   - API Requirement: Define the `/api/chat` endpoint and the `/api/ingest` endpoint.

4. PART C: USER STORIES (Functionality)
   - "As a Student, I want to highlight a paragraph about 'Servo Motors' and ask 'How do I code this in Python?', so the AI gives me a code example based on that specific text."
   - "As an Admin, I want to run a script that automatically updates the Chatbot's knowledge whenever I write a new chapter."

5. DOCUSAURUS INTEGRATION:
   - Specify that the Chatbot UI must be a global React component (floating widget) visible on every page.

## Response snapshot

Created comprehensive feature specification with:

**User Stories (3 prioritized)**:
- P1: Student asks context-aware questions (core MVP value)
- P2: Admin auto-updates book content via ingest script
- P3: Student tracks learning progress via session history

**Functional Requirements (18 total)**:
- Book content: 5 FRs (16-chapter structure, metadata headers, Docusaurus rendering, GitHub Pages deployment, global chat widget)
- Backend RAG: 9 FRs (chat endpoint, ingest endpoint, content validation, context-aware retrieval, chat logging, streaming, metadata API)
- Integration & Security: 4 FRs (CORS, environment variables, input validation, HTTP status codes)

**Key Entities (5 models)**:
- Chapter, ChunkVector, ChatSession, ChatMessage, IngestionLog

**Success Criteria (8 measurable outcomes)**:
- API response time < 2 seconds (p95)
- Ingest script processes full book in < 1 minute
- 90% of responses include relevant code examples
- Frontend Lighthouse ≥ 90 score
- 95% accuracy on rejecting out-of-scope queries
- Chat widget loads < 3 seconds on 4G
- System handles 100 concurrent queries
- 100% API compliance with OpenAPI spec

**Assumptions (8 documented)**:
- Anonymous access (no login MVP)
- 90-day chat log retention
- Manual ingest triggers
- Vector-based RAG (not keyword search)
- Conversational text responses
- 100 queries/hour rate limit
- 503 fallback if Qdrant down
- Cross-chapter context prioritization logic

**Specification Quality**:
- ✅ All 4 content quality items pass
- ✅ All 8 requirement completeness items pass
- ✅ All 4 feature readiness items pass
- **Ready for planning phase**

## Outcome

- ✅ Impact: Feature specification complete (16 requirements, 3 user stories, 8 success criteria, 5 data models). Aligns with constitution principles (monorepo, schema-first, docs-as-code, security, testing).
- 🧪 Tests: All FRs are testable; acceptance scenarios use BDD format (Given-When-Then). Quality checklist: 16/16 items passing.
- 📁 Files: specs/001-living-textbook-rag/spec.md (2,500+ words), specs/001-living-textbook-rag/checklists/requirements.md
- 🔁 Next prompts: Run `/sp.clarify` if additional detail needed, or proceed directly to `/sp.plan` for architecture design
- 🧠 Reflection: Specification captures dual-hackathon scope (Book + Chatbot) with clear MVP (P1 story) that enables independent testing and deployment. All user stories are independently deliverable, supporting incremental development.

## Evaluation notes (flywheel)

- Failure modes observed: None—specification complete with minimal clarifications needed
- Graders run and results (PASS/FAIL): Manual validation PASS—all requirements testable, success criteria measurable, no ambiguities
- Prompt variant (if applicable): N/A—first specification creation
- Next experiment (smallest change to try): Recommend proceeding to `/sp.plan` to design data flow, API contracts (OpenAPI), and backend/frontend integration points
