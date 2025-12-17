# Quickstart Guide: Living Textbook Development

**Feature**: Living Textbook with RAG Teaching Assistant
**Branch**: `001-living-textbook-rag`
**Date**: 2025-12-18

This guide walks you through setting up the entire monorepo locally and running the system end-to-end.

## Prerequisites

- **OS**: macOS, Linux, or Windows (WSL2)
- **Node.js**: 18+ (for frontend)
- **Python**: 3.12+ (for backend)
- **Git**: For cloning and branch management
- **Accounts** (free tier sufficient):
  - Qdrant Cloud (vector database): https://cloud.qdrant.io/
  - Neon Postgres (database): https://neon.tech/
  - OpenAI (API): https://platform.openai.com/

## Step 1: Clone Repository & Checkout Branch

```bash
# Clone the monorepo
git clone https://github.com/GIAIC-Hackathone/Physical-AI---Humanoid-Robotics-Book.git
cd Physical-AI---Humanoid-Robotics-Book

# Checkout feature branch
git checkout 001-living-textbook-rag

# Verify you're on the correct branch
git branch --show-current
# Output: 001-living-textbook-rag
```

## Step 2: Setup Backend (FastAPI)

### 2a. Create Python Virtual Environment

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Verify activation (prompt should show (venv))
```

### 2b. Install Dependencies

```bash
# Install Python dependencies from requirements.txt
pip install -r requirements.txt

# Verify installation
pip list | grep -E "fastapi|qdrant|openai|sqlalchemy"
```

### 2c. Configure Environment Variables

```bash
# Copy example .env
cp .env.example .env

# Edit .env with your credentials
nano .env
```

**Fill in these variables** (get from your cloud account dashboards):

```bash
# OpenAI API Key (from https://platform.openai.com/api-keys)
OPENAI_API_KEY=sk-...

# Qdrant Cloud credentials (from https://cloud.qdrant.io/)
QDRANT_URL=https://your-instance.qdrant.io
QDRANT_API_KEY=your-qdrant-api-key

# Neon Postgres connection string (from https://neon.tech/)
DATABASE_URL=postgresql://user:password@ep-name.neon.tech/dbname

# Admin token for /api/ingest endpoint (generate any secure string)
ADMIN_TOKEN=your-secure-admin-token-here

# Optional: Backend port
PORT=8000

# Optional: Environment
ENVIRONMENT=development
```

### 2d. Initialize Database

```bash
# Create PostgreSQL tables and migrate schema
python -m alembic upgrade head

# Verify connection
python -c "import psycopg2; print('PostgreSQL connected!')"
```

### 2e. Start Backend Server

```bash
# Run FastAPI development server with auto-reload
uvicorn src.main:app --reload --port 8000

# Expected output:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     Application startup complete
```

**Backend is now running at**: `http://localhost:8000`

**Test it**:
```bash
# In another terminal, test the health endpoint
curl http://localhost:8000/api/health

# Expected response:
# {"status": "healthy", "qdrant_status": "ok", "postgres_status": "ok"}
```

---

## Step 3: Setup Frontend (Docusaurus)

### 3a. Initialize Docusaurus Project

```bash
# Navigate to frontend directory (new terminal)
cd frontend

# If Docusaurus doesn't exist yet, create it:
npx create-docusaurus@latest . classic --typescript

# If Docusaurus already exists:
npm install
```

### 3b. Create 16 Chapter Content

```bash
# Create directory structure for 16 chapters (4 Modules × 4 Parts)
mkdir -p docs/01-module-foundations
mkdir -p docs/02-module-body
mkdir -p docs/03-module-brain
mkdir -p docs/04-module-humanoid

# Example: Create first chapter
cat > docs/01-module-foundations/01-python-intro.mdx << 'EOF'
---
title: Python Fundamentals for Robotics
module: 1
part: 1
chapter: 1
learning_objectives:
  - Understand Python basics for robotics development
  - Learn how to set up a Python environment
prerequisites:
  - None (intro chapter)
keywords:
  - Python
  - programming
  - robotics
---

# Python Fundamentals for Robotics

Welcome to the first chapter of the Physical AI textbook. In this chapter, we'll cover...

## Key Concepts

### Variables and Data Types

In Python, variables are dynamically typed...
EOF
```

### 3c. Configure Docusaurus

Edit `docusaurus.config.js` to enable TypeScript and configure the chat widget placeholder:

```javascript
// docusaurus.config.js
module.exports = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'Living Textbook with AI Teaching Assistant',
  url: 'https://giaic-hackathone.github.io',
  baseUrl: '/Physical-AI---Humanoid-Robotics-Book/',

  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/GIAIC-Hackathone/Physical-AI---Humanoid-Robotics-Book/edit/main/frontend/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],

  themeConfig: {
    navbar: {
      title: 'Living Textbook',
      logo: {
        alt: 'Physical AI Logo',
        src: 'img/logo.svg',
      },
    },
  },
};
```

### 3d. Create AI Assistant Component

Create `src/components/AiAssistant.tsx`:

```typescript
import React, { useState } from 'react';
import styles from './AiAssistant.module.css';

export const AiAssistant: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Array<{ role: 'user' | 'assistant'; content: string }>>([]);
  const [input, setInput] = useState('');

  const handleSend = async () => {
    if (!input.trim()) return;

    // Add user message
    const userMessage = { role: 'user' as const, content: input };
    setMessages(prev => [...prev, userMessage]);

    try {
      // Call backend API
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query_text: input,
          highlighted_context: null,
          chapter_context: null,
          session_id: null,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setMessages(prev => [...prev, { role: 'assistant', content: data.response_text }]);
      }
    } catch (error) {
      console.error('Error calling API:', error);
    }

    setInput('');
  };

  return (
    <div className={styles.assistant}>
      <button className={styles.toggle} onClick={() => setIsOpen(!isOpen)}>
        💬
      </button>
      {isOpen && (
        <div className={styles.chatWindow}>
          <div className={styles.messages}>
            {messages.map((msg, idx) => (
              <div key={idx} className={`${styles.message} ${styles[msg.role]}`}>
                {msg.content}
              </div>
            ))}
          </div>
          <input
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyPress={e => e.key === 'Enter' && handleSend()}
            placeholder="Ask about the textbook..."
          />
          <button onClick={handleSend}>Send</button>
        </div>
      )}
    </div>
  );
};
```

### 3e. Start Frontend Server

```bash
# Run Docusaurus development server
npm start

# Expected output:
# [INFO] Docusaurus server started on http://localhost:3000
```

**Frontend is now running at**: `http://localhost:3000`

---

## Step 4: Test End-to-End

### 4a. Verify Both Servers Are Running

```bash
# Terminal 1 (Backend):
# http://localhost:8000/api/health

# Terminal 2 (Frontend):
# http://localhost:3000

# Terminal 3 (for testing):
curl -X GET http://localhost:8000/api/health
```

### 4b. Ingest Book Content

```bash
# In backend terminal, run the ingestion script:
cd backend

# Run the ingest script
python scripts/ingest_book.py

# Expected output:
# INFO: Processing 16 chapters...
# INFO: Chapter 1: Python Fundamentals
# INFO: Chunked into 28 vectors
# ...
# INFO: Ingestion complete! 450 chunks created in 45.2 seconds
```

### 4c. Test Chat Endpoint

```bash
# Test the chat API manually
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query_text": "How do I use Python for robotics?",
    "session_id": null
  }'

# Expected response:
# {
#   "response_text": "Python is widely used for robotics...",
#   "source_chapters": [{"id": 1, "title": "Python Fundamentals for Robotics"}],
#   "confidence_score": 0.92,
#   "session_id": "550e8400-e29b-41d4-a716-446655440000",
#   "timestamp": "2025-12-18T10:15:00Z"
# }
```

### 4d. Test Chat Widget in Browser

1. Open `http://localhost:3000` in your browser
2. Click the 💬 button in the bottom-right corner
3. Type: "How do servo motors work?"
4. Click "Send"
5. Wait 2-3 seconds for response

---

## Step 5: Development Workflow

### Add a New Chapter

1. Create markdown file in `/frontend/docs/0X-module-name/YY-chapter-name.mdx`
2. Add YAML frontmatter with metadata
3. Write content in Markdown
4. Run ingest script to update vectors:
   ```bash
   cd backend && python scripts/ingest_book.py
   ```

### Run Tests

```bash
# Backend unit tests
cd backend
pytest tests/unit/ -v

# Backend integration tests
pytest tests/integration/ -v

# Frontend tests
cd ../frontend
npm test
```

### Type Checking & Linting

```bash
# Backend type checking
cd backend
mypy src/

# Backend linting
ruff check src/

# Frontend type checking
cd ../frontend
npm run type-check

# Frontend linting
npm run lint
```

### Build & Deploy

```bash
# Build frontend static site
cd frontend
npm run build
# Output: ./build/

# Deploy to GitHub Pages (automated via GitHub Actions)
git push origin 001-living-textbook-rag

# Deploy backend (depends on your cloud platform)
# Example for Render: Connect your repo and auto-deploy
```

---

## Troubleshooting

### Backend won't start: "Connection refused" (Qdrant/Postgres)

**Solution**: Verify credentials in `.env`
```bash
# Test Qdrant connection
python -c "from qdrant_client import QdrantClient; QdrantClient(url='...', api_key='...').get_collections()"

# Test Postgres connection
psql $DATABASE_URL -c "SELECT 1;"
```

### Frontend chat widget not working: "CORS error"

**Solution**: Backend CORS middleware not configured. Update `backend/src/main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Ingest script fails: "OpenAI rate limit exceeded"

**Solution**: Add delay between embedding requests
```python
import time
time.sleep(1)  # Between each embedding call
```

### Database migration errors

**Solution**: Reset database and re-migrate
```bash
# Drop all tables (development only!)
python -c "from src.models import Base; Base.metadata.drop_all(engine)"

# Re-run migrations
alembic upgrade head
```

---

## Next Steps

1. **Implement P1 User Story**: Focus on context-aware chat queries (Hackathon 1 MVP)
2. **Write Unit Tests**: Cover RAG pipeline, API endpoints, chunking logic
3. **Run CI/CD Pipeline**: Set up GitHub Actions for automated testing/deployment
4. **Performance Optimization**: Profile latency, optimize vector search
5. **Add P2 User Story**: Auto-ingest content updates

---

## Architecture Summary

```
Frontend (Docusaurus + React)    Backend (FastAPI)         External Services
http://localhost:3000            http://localhost:8000
    ↓                               ↓                             ↓
[Chat Widget] ←→ REST API ←→ [RAG Pipeline] ←→ [Qdrant Cloud]
[16 Chapters]                  [OpenAI LLM]     [Neon Postgres]
                               [Validation]
```

---

## Commands Reference

| Action | Command |
|--------|---------|
| Start backend | `cd backend && uvicorn src.main:app --reload` |
| Start frontend | `cd frontend && npm start` |
| Run tests | `pytest tests/` or `npm test` |
| Type check | `mypy src/` or `npm run type-check` |
| Lint code | `ruff check src/` or `npm run lint` |
| Ingest chapters | `python backend/scripts/ingest_book.py` |
| Reset database | `python backend/scripts/reset_db.py` |
| Build static site | `cd frontend && npm run build` |
| View OpenAPI docs | `http://localhost:8000/docs` |

---

## Support

For issues or questions:
1. Check the main `/README.md` in the monorepo
2. Review `/backend/README.md` and `/frontend/README.md`
3. Open a GitHub Issue with error logs
4. Consult the Spec (`specs/001-living-textbook-rag/spec.md`)
