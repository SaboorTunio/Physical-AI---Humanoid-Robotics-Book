"""
Living Textbook RAG Backend - FastAPI Application
"""
import os
from typing import Dict, Any, List
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

from src.config import settings
from src.services.qdrant_service import qdrant_service
from src.services.openai_service import openai_service

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Living Textbook RAG API",
    description="Backend API for Physical AI & Humanoid Robotics Living Textbook with RAG Teaching Assistant",
    version="1.0.0",
)

# Configure CORS
cors_origins = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
qdrant_service.init_client()
openai_service.init_client()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/api/health")
async def health_check():
    """
    Health check endpoint for deployment monitoring.

    Returns:
        dict: Health status information
    """
    qdrant_health = await qdrant_service.health_check()
    openai_health = await openai_service.health_check()

    return {
        "status": "healthy",
        "qdrant_status": qdrant_health.get("status"),
        "openai_status": openai_health.get("status"),
        "version": "1.0.0",
    }


@app.post("/api/chat")
async def chat_endpoint(request: dict):
    """
    Chat endpoint that receives a user query, searches Qdrant for context,
    and sends the prompt to OpenAI to get an answer.

    Args:
        request: Dictionary containing query and optional parameters
            - query: User's question/query
            - chapter_context: Optional chapter index for context
            - highlighted_context: Optional highlighted text from textbook
            - max_context_chunks: Maximum number of context chunks to retrieve from Qdrant (default: 5)

    Returns:
        dict: Response containing the answer and source information
    """
    query = request.get("query", "")
    chapter_context = request.get("chapter_context")
    highlighted_context = request.get("highlighted_context")
    max_context_chunks = request.get("max_context_chunks", 5)

    if not query or not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        # Generate embedding for the user query
        query_embedding = await openai_service.generate_embedding(query)

        # Search Qdrant for relevant context
        search_results = await qdrant_service.search_similar(
            query_vector=query_embedding,
            limit=max_context_chunks,
            score_threshold=0.3  # Minimum similarity threshold
        )

        if not search_results:
            logger.warning("No relevant context found for query")
            return {
                "query": query,
                "answer": "I couldn't find relevant information in the textbook to answer your question.",
                "sources": [f"Chapter {chapter_context}"] if chapter_context else [],
                "context_chunks": 0
            }

        # Build context from search results
        context_parts = []
        sources = []
        for result in search_results:
            payload = result.get("payload", {})
            content = payload.get("content", "")
            source_info = payload.get("source", "Unknown source")

            if content:
                context_parts.append(content)
                sources.append(source_info)

        # Combine all context parts
        context = "\n\n".join(context_parts)

        # Include highlighted context if provided
        if highlighted_context:
            context = f"Highlighted text for context: {highlighted_context}\n\n{context}"

        # Create system prompt for the AI
        system_prompt = f"""
        You are an AI Teaching Assistant for the Physical AI & Humanoid Robotics Living Textbook.
        Your role is to help students understand the content from the textbook.

        Use the following context from the textbook to answer the user's question:
        {context}

        If the context doesn't contain relevant information to answer the question,
        politely say that you couldn't find relevant information in the textbook.

        Provide clear, concise, and accurate answers based on the textbook content.
        When possible, cite the specific sources where the information comes from.
        """

        # Generate response using OpenAI
        answer = await openai_service.generate_response(
            system_prompt=system_prompt,
            user_query=query,
            context=None,  # Context is already in system prompt
            temperature=0.7,
            max_tokens=1000
        )

        return {
            "query": query,
            "answer": answer,
            "sources": list(set(sources)),  # Remove duplicates
            "context_chunks": len(search_results),
            "relevance_scores": [result.get("score", 0) for result in search_results]
        }

    except Exception as e:
        logger.error(f"Error processing chat query: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.get("/")
async def root():
    """
    Root endpoint for API information.

    Returns:
        dict: API information and available endpoints
    """
    return {
        "message": "Welcome to Living Textbook RAG API",
        "docs": "/docs",
        "endpoints": {
            "GET /": "This message",
            "GET /api/health": "Health check",
            "POST /api/chat": "Chat endpoint (requires query parameter)"
        },
        "version": "1.0.0",
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    environment = os.getenv("ENVIRONMENT", "development")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=(environment == "development"),
    )