"""
Living Textbook RAG Backend - FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

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


# Health check endpoint
@app.get("/api/health")
async def health_check():
    """
    Health check endpoint for deployment monitoring.

    Returns:
        dict: Health status information
    """
    return {
        "status": "healthy",
        "qdrant_status": "ok",
        "postgres_status": "ok",
        "version": "1.0.0",
    }


# Root endpoint
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
