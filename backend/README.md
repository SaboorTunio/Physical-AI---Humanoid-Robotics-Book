# Physical AI Living Textbook - Backend

This is the **FastAPI** powered backend for the Living Textbook RAG system. It handles the RAG pipeline, chat endpoints, content ingestion, and session management.

## Tech Stack

- **FastAPI**: Modern Python web framework with automatic API documentation
- **Python 3.12+**: Latest Python with async/await support
- **Qdrant**: Vector database for semantic search
- **OpenAI**: LLM for response generation and embeddings
- **Neon Postgres**: Serverless PostgreSQL for persistence
- **SQLAlchemy**: ORM for database operations
- **Pydantic**: Data validation and serialization

## Project Structure

```
backend/
├── src/
│   ├── main.py              # FastAPI application entrypoint
│   ├── config.py            # Environment configuration
│   ├── models/
│   │   ├── database.py      # SQLAlchemy ORM models
│   │   └── schemas.py       # Pydantic request/response schemas
│   ├── services/
│   │   ├── qdrant_service.py    # Vector DB operations
│   │   ├── openai_service.py    # LLM and embedding calls
│   │   ├── postgres_service.py  # Database operations
│   │   ├── rag_service.py       # RAG pipeline logic
│   │   └── ingest_service.py    # Content ingestion
│   ├── api/
│   │   ├── chat.py          # POST /api/chat endpoint
│   │   ├── ingest.py        # POST /api/ingest endpoint
│   │   ├── health.py        # GET /api/health endpoint
│   │   └── metadata.py      # GET /api/metadata endpoint
│   └── utils/
│       ├── logger.py        # Structured logging
│       ├── validators.py    # Input validation
│       ├── errors.py        # Custom exceptions
│       └── chunker.py       # Text chunking
├── scripts/
│   ├── ingest_book.py       # Standalone ingestion script
│   ├── reset_db.py          # Development utility to reset databases
│   └── migrate.py           # Database migration script
├── tests/
│   ├── unit/                # Unit tests
│   ├── integration/         # Integration tests
│   └── contract/            # Contract tests (API)
├── alembic/                 # Database migrations
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
└── venv/                    # Python virtual environment
```

## Getting Started

### Prerequisites

- Python 3.12+ (download from https://www.python.org/)
- pip or poetry
- Qdrant Cloud account (free tier at https://cloud.qdrant.io/)
- Neon Postgres account (free tier at https://neon.tech/)
- OpenAI API key (from https://platform.openai.com/api-keys)

### Installation

1. **Create Virtual Environment**

```bash
cd backend
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure Environment**

```bash
cp .env.example .env
# Edit .env with your credentials
```

### Running the Server

```bash
# With auto-reload for development
uvicorn src.main:app --reload --port 8000

# Production (without auto-reload)
uvicorn src.main:app --port 8000
```

The API will be available at:
- HTTP: http://localhost:8000
- Docs: http://localhost:8000/docs (Swagger UI)
- ReDoc: http://localhost:8000/redoc

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Specific test file
pytest tests/unit/test_chunker.py -v

# Integration tests only
pytest tests/integration/ -v
```

## API Endpoints

### Chat
- **POST** `/api/chat` - Answer a question about the textbook
  - Query: question text
  - Optional: highlighted_context, chapter_context, session_id
  - Response: answer, source chapters, confidence score

### Ingest
- **POST** `/api/ingest` - Update Qdrant with book content (admin-only)
  - Header: Authorization (Bearer token)
  - Optional: force_refresh (boolean)
  - Response: status, chapters_processed, chunks_created

### Health
- **GET** `/api/health` - Check system health
  - Response: status, qdrant_status, postgres_status

### Metadata
- **GET** `/api/metadata` - Get chapter list and keywords
  - Optional: module_id filter
  - Response: chapters array with metadata

See `specs/001-living-textbook-rag/contracts/openapi.yaml` for full OpenAPI specification.

## Commands

| Command | Purpose |
|---------|---------|
| `uvicorn src.main:app --reload` | Start development server |
| `pytest` | Run all tests |
| `pytest --cov=src` | Run tests with coverage |
| `mypy src/` | Type checking |
| `ruff check src/` | Linting |
| `python scripts/ingest_book.py` | Ingest all chapters |
| `python scripts/reset_db.py` | Reset databases (dev only) |

## Development Workflow

### Creating a New Endpoint

1. Define Pydantic schema in `src/models/schemas.py`
2. Add route to `src/api/[endpoint].py`
3. Write tests in `tests/contract/test_[endpoint].py`
4. Update OpenAPI spec in `specs/001-living-textbook-rag/contracts/openapi.yaml`

### Adding a New Service

1. Create `src/services/[service_name].py`
2. Implement service class with methods
3. Write unit tests in `tests/unit/test_[service_name].py`
4. Import and use in API endpoints

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Ingestion Pipeline

### Manual Ingestion

```bash
python scripts/ingest_book.py
```

This script:
1. Reads all .mdx files from `frontend/docs/`
2. Parses YAML metadata from each chapter
3. Chunks content semantically (200-500 tokens)
4. Generates embeddings via OpenAI
5. Upserts to Qdrant
6. Logs to PostgreSQL

### Automatic Ingestion (CI/CD)

GitHub Actions workflow: `.github/workflows/book-ingest.yml`
- Runs daily or on manual trigger
- Calls `POST /api/ingest` with admin token

## Configuration

### Environment Variables

```bash
# OpenAI
OPENAI_API_KEY=sk-...

# Qdrant
QDRANT_URL=https://your-instance.qdrant.io:6333
QDRANT_API_KEY=...

# Neon Postgres
DATABASE_URL=postgresql://user:password@ep-name.neon.tech/dbname

# Backend
PORT=8000
ENVIRONMENT=development
ADMIN_TOKEN=...

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Rate Limiting
RATE_LIMIT_QUERIES_PER_HOUR=100
```

## Performance Optimization

### Vector Search

- Use Qdrant batch operations for ingestion
- Index optimization in Qdrant console
- Query optimization with proper payloads

### Database

- Connection pooling (asyncpg)
- Query optimization with indexes
- Batch inserts for logging

### API

- Response streaming for large chunks
- Caching headers for metadata
- Request size validation

## Troubleshooting

### Connection Issues

```bash
# Test Qdrant connection
python -c "from qdrant_client import QdrantClient; print(QdrantClient(url='...', api_key='...').get_collections())"

# Test Postgres connection
psql $DATABASE_URL
```

### Type Checking Errors

```bash
mypy src/ --strict
```

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Contributing

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and test: `pytest`
3. Type check: `mypy src/`
4. Lint: `ruff check src/`
5. Commit: `git commit -m "feat: description"`
6. Push: `git push origin feature/your-feature`
7. Open PR

## Testing Strategy

### Unit Tests
- Test individual services in isolation
- Mock external dependencies (Qdrant, OpenAI)
- Located in `tests/unit/`

### Integration Tests
- Test API endpoints end-to-end
- Use real Qdrant/Postgres (or test fixtures)
- Located in `tests/integration/`

### Contract Tests
- Verify API responses match OpenAPI spec
- Test request/response schemas
- Located in `tests/contract/`

## Documentation

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Qdrant Docs](https://qdrant.tech/documentation/)
- [OpenAI Docs](https://platform.openai.com/docs/)

## Support

- GitHub Issues: Report bugs and feature requests
- Discussions: Ask questions and share ideas
- Architecture: See specs/ for detailed design

## License

Copyright © 2025 GIAIC Hackathon. Licensed under MIT.
