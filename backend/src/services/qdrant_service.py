"""
Qdrant vector database service for Living Textbook RAG Backend.
Provides vector search and semantic similarity operations.
"""

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from typing import List, Optional, Dict, Any
import logging

from src.config import settings

logger = logging.getLogger(__name__)


class QdrantService:
    """
    Service for interacting with Qdrant vector database.
    Handles vector storage, search, and collection management.
    """

    def __init__(self):
        """Initialize Qdrant client with settings."""
        self.client = None
        self._initialized = False
        self.collection_name = settings.qdrant_collection_name
        self.vector_size = settings.qdrant_vector_size

    def init_client(self):
        """
        Initialize Qdrant client.
        Connects to Qdrant instance at configured URL.
        """
        if self._initialized:
            logger.warning("Qdrant client already initialized")
            return

        try:
            self.client = QdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key,
                timeout=30.0,
            )
            self._initialized = True
            logger.info(f"Qdrant client initialized: {settings.qdrant_url}")
        except Exception as e:
            logger.error(f"Failed to initialize Qdrant client: {e}")
            raise

    async def health_check(self) -> Dict[str, Any]:
        """
        Check Qdrant service health.

        Returns:
            Dictionary with status and latency information
        """
        if not self.client:
            raise RuntimeError("Qdrant client not initialized. Call init_client() first.")

        try:
            info = self.client.get_collections()
            return {
                "status": "ok",
                "collections": len(info.collections),
            }
        except Exception as e:
            logger.error(f"Qdrant health check failed: {e}")
            return {
                "status": "error",
                "error": str(e),
            }

    async def create_collection(self) -> bool:
        """
        Create or recreate the collection for textbook chunks.
        Configures vector size and distance metric.

        Returns:
            True if collection created successfully, False if already exists
        """
        if not self.client:
            raise RuntimeError("Qdrant client not initialized. Call init_client() first.")

        try:
            # Check if collection exists
            collections = self.client.get_collections()
            for collection in collections.collections:
                if collection.name == self.collection_name:
                    logger.info(f"Collection '{self.collection_name}' already exists")
                    return False

            # Create collection
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE,
                ),
            )
            logger.info(f"Collection '{self.collection_name}' created successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to create collection: {e}")
            raise

    async def delete_collection(self):
        """
        Delete the collection.
        Used for cleanup and testing.
        WARNING: This removes all data in the collection.
        """
        if not self.client:
            raise RuntimeError("Qdrant client not initialized. Call init_client() first.")

        try:
            self.client.delete_collection(collection_name=self.collection_name)
            logger.info(f"Collection '{self.collection_name}' deleted")
        except Exception as e:
            logger.error(f"Failed to delete collection: {e}")
            raise

    async def upsert_vectors(
        self,
        vectors: List[tuple[str, List[float], Dict[str, Any]]],
    ) -> bool:
        """
        Upsert vectors into the collection.
        Each vector includes ID, embedding, and metadata.

        Args:
            vectors: List of tuples (id, embedding, payload)

        Returns:
            True if successful
        """
        if not self.client:
            raise RuntimeError("Qdrant client not initialized. Call init_client() first.")

        if not vectors:
            logger.warning("No vectors to upsert")
            return True

        try:
            points = [
                PointStruct(
                    id=int(idx),
                    vector=embedding,
                    payload=payload,
                )
                for idx, (point_id, embedding, payload) in enumerate(vectors)
            ]

            self.client.upsert(
                collection_name=self.collection_name,
                points=points,
            )
            logger.info(f"Upserted {len(points)} vectors into '{self.collection_name}'")
            return True

        except Exception as e:
            logger.error(f"Failed to upsert vectors: {e}")
            raise

    async def search_similar(
        self,
        query_vector: List[float],
        limit: int = 5,
        score_threshold: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for vectors similar to the query vector.

        Args:
            query_vector: The embedding vector to search with
            limit: Maximum number of results to return
            score_threshold: Minimum similarity score (0.0-1.0)

        Returns:
            List of similar vectors with metadata and scores
        """
        if not self.client:
            raise RuntimeError("Qdrant client not initialized. Call init_client() first.")

        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                score_threshold=score_threshold,
            )

            search_results = []
            for result in results:
                search_results.append({
                    "id": result.id,
                    "score": result.score,
                    "payload": result.payload,
                })

            logger.debug(f"Found {len(search_results)} similar vectors")
            return search_results

        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise

    async def get_collection_info(self) -> Dict[str, Any]:
        """
        Get information about the collection.

        Returns:
            Dictionary with collection statistics
        """
        if not self.client:
            raise RuntimeError("Qdrant client not initialized. Call init_client() first.")

        try:
            collection_info = self.client.get_collection(
                collection_name=self.collection_name
            )

            return {
                "name": collection_info.config.collection_name,
                "vectors_count": collection_info.vectors_count,
                "points_count": collection_info.points_count,
                "status": collection_info.status,
            }

        except Exception as e:
            logger.error(f"Failed to get collection info: {e}")
            raise

    async def delete_vector(self, vector_id: str) -> bool:
        """
        Delete a specific vector by ID.

        Args:
            vector_id: The ID of the vector to delete

        Returns:
            True if deletion successful
        """
        if not self.client:
            raise RuntimeError("Qdrant client not initialized. Call init_client() first.")

        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=[int(vector_id)],
            )
            logger.info(f"Deleted vector {vector_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to delete vector: {e}")
            raise


# Global Qdrant service instance
qdrant_service = QdrantService()


async def get_qdrant_service() -> QdrantService:
    """
    Get the global Qdrant service instance.
    Can be used as a FastAPI dependency.

    Returns:
        QdrantService instance
    """
    if not qdrant_service._initialized:
        qdrant_service.init_client()
    return qdrant_service
