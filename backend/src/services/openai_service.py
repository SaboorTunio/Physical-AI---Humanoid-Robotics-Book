"""
OpenAI API service for Living Textbook RAG Backend.
Provides LLM inference and embedding generation capabilities.
"""

from openai import AsyncOpenAI
from typing import List, Optional, Dict, Any
import logging

from src.config import settings

logger = logging.getLogger(__name__)


class OpenAIService:
    """
    Service for interacting with OpenAI API.
    Handles text embeddings and language model completions.
    """

    def __init__(self):
        """Initialize OpenAI client with API key."""
        self.client = None
        self._initialized = False

    def init_client(self):
        """
        Initialize async OpenAI client.
        API key loaded from settings.
        """
        if self._initialized:
            logger.warning("OpenAI client already initialized")
            return

        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY not configured in environment")

        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self._initialized = True
        logger.info("OpenAI client initialized")

    async def health_check(self) -> Dict[str, Any]:
        """
        Check OpenAI API health by attempting a simple request.

        Returns:
            Dictionary with status and model availability
        """
        if not self.client:
            raise RuntimeError("OpenAI client not initialized. Call init_client() first.")

        try:
            # Test embedding model
            response = await self.client.embeddings.create(
                model=settings.openai_embedding_model,
                input="test",
            )
            return {
                "status": "ok",
                "embedding_model": settings.openai_embedding_model,
                "llm_model": settings.openai_model,
            }
        except Exception as e:
            logger.error(f"OpenAI health check failed: {e}")
            return {
                "status": "error",
                "error": str(e),
            }

    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate an embedding vector for the given text.
        Uses text-embedding-3-small model for efficiency.

        Args:
            text: The text to embed

        Returns:
            List of embedding floats (1536-dimensional)

        Raises:
            ValueError: If text is empty
            RuntimeError: If client not initialized
        """
        if not self.client:
            raise RuntimeError("OpenAI client not initialized. Call init_client() first.")

        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        try:
            response = await self.client.embeddings.create(
                model=settings.openai_embedding_model,
                input=text.strip(),
            )
            embedding = response.data[0].embedding
            logger.debug(f"Generated embedding for {len(text)} chars")
            return embedding

        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            raise

    async def generate_embeddings_batch(
        self,
        texts: List[str],
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in a batch.
        More efficient than individual calls.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors (1536-dimensional each)

        Raises:
            ValueError: If texts list is empty or contains empty strings
            RuntimeError: If client not initialized
        """
        if not self.client:
            raise RuntimeError("OpenAI client not initialized. Call init_client() first.")

        if not texts:
            raise ValueError("Texts list cannot be empty")

        # Filter and validate texts
        valid_texts = [t.strip() for t in texts if t and t.strip()]
        if not valid_texts:
            raise ValueError("All texts are empty")

        try:
            response = await self.client.embeddings.create(
                model=settings.openai_embedding_model,
                input=valid_texts,
            )

            # Sort by index to maintain order
            embeddings = sorted(response.data, key=lambda x: x.index)
            result = [e.embedding for e in embeddings]

            logger.debug(f"Generated embeddings for {len(result)} texts")
            return result

        except Exception as e:
            logger.error(f"Failed to generate batch embeddings: {e}")
            raise

    async def generate_response(
        self,
        system_prompt: str,
        user_query: str,
        context: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Generate a response from the language model.
        Includes context from RAG for grounded responses.

        Args:
            system_prompt: System role instruction
            user_query: The user's question
            context: Optional RAG context to include
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens in response

        Returns:
            Generated response text

        Raises:
            RuntimeError: If client not initialized
        """
        if not self.client:
            raise RuntimeError("OpenAI client not initialized. Call init_client() first.")

        if not user_query or not user_query.strip():
            raise ValueError("User query cannot be empty")

        # Build messages
        messages = [
            {"role": "system", "content": system_prompt},
        ]

        # Add context if provided
        if context:
            user_message = f"{context}\n\nUser Question: {user_query}"
        else:
            user_message = user_query

        messages.append({"role": "user", "content": user_message})

        try:
            response = await self.client.chat.completions.create(
                model=settings.openai_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens or settings.openai_max_tokens,
            )

            answer = response.choices[0].message.content
            logger.debug(f"Generated response ({len(answer)} chars)")
            return answer

        except Exception as e:
            logger.error(f"Failed to generate response: {e}")
            raise

    async def extract_keywords(
        self,
        text: str,
        max_keywords: int = 5,
    ) -> List[str]:
        """
        Extract key topics/keywords from text using LLM.

        Args:
            text: The text to extract keywords from
            max_keywords: Maximum number of keywords to extract

        Returns:
            List of keyword strings

        Raises:
            RuntimeError: If client not initialized
        """
        if not self.client:
            raise RuntimeError("OpenAI client not initialized. Call init_client() first.")

        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        system_prompt = f"Extract up to {max_keywords} key topics/keywords from the given text. Return as a comma-separated list."

        try:
            response = await self.client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text.strip()},
                ],
                temperature=0.3,
                max_tokens=200,
            )

            keywords_text = response.choices[0].message.content
            keywords = [k.strip() for k in keywords_text.split(",")]
            logger.debug(f"Extracted {len(keywords)} keywords")
            return keywords

        except Exception as e:
            logger.error(f"Failed to extract keywords: {e}")
            raise


# Global OpenAI service instance
openai_service = OpenAIService()


async def get_openai_service() -> OpenAIService:
    """
    Get the global OpenAI service instance.
    Can be used as a FastAPI dependency.

    Returns:
        OpenAIService instance
    """
    if not openai_service._initialized:
        openai_service.init_client()
    return openai_service
