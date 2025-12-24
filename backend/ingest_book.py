"""
Book ingestion script for Living Textbook RAG Backend.
Recursively reads .mdx files from frontend/docs and upserts chunks to Qdrant.
"""

import os
import re
from pathlib import Path
from typing import List, Tuple, Dict, Any
import asyncio
import logging

from src.config import settings
from src.services.qdrant_service import qdrant_service
from src.services.openai_service import openai_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def clean_markdown_content(content: str) -> str:
    """
    Clean markdown content by removing Docusaurus-specific syntax and metadata.

    Args:
        content: Raw markdown content

    Returns:
        Cleaned content string
    """
    # Remove frontmatter (metadata between ---)
    content = re.sub(r'---\n.*?\n---', '', content, flags=re.DOTALL)

    # Remove Docusaurus-specific syntax like import statements and component usage
    content = re.sub(r'import.*?from.*?\n', '', content)
    content = re.sub(r'<.*?>', '', content)  # Remove JSX-like components

    # Remove extra whitespace and normalize line breaks
    content = re.sub(r'\n\s*\n', '\n\n', content)
    content = content.strip()

    return content


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Split text into overlapping chunks.

    Args:
        text: Input text to chunk
        chunk_size: Maximum size of each chunk
        overlap: Number of characters to overlap between chunks

    Returns:
        List of text chunks
    """
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # If we're at the end, include the rest
        if end >= len(text):
            end = len(text)
        else:
            # Try to break at sentence boundary
            while end > start + chunk_size - overlap and end < len(text) and text[end] not in '.!?':
                end += 1

            # If no sentence boundary found, break at word boundary
            if end == start + chunk_size:
                while end > start + chunk_size - overlap and end < len(text) and text[end] != ' ':
                    end += 1

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        # Move start position forward, considering overlap
        start = end - overlap if end < len(text) else len(text)

        # Ensure we make progress to avoid infinite loop
        if start == end:
            start += chunk_size

    return [chunk for chunk in chunks if len(chunk.strip()) > 50]  # Filter out very short chunks


async def read_mdx_files(docs_path: str) -> List[Tuple[str, str, Dict[str, Any]]]:
    """
    Recursively read all .mdx files from the docs directory.

    Args:
        docs_path: Path to the docs directory

    Returns:
        List of tuples (file_path, content, metadata)
    """
    mdx_files = []
    docs_dir = Path(docs_path)

    for mdx_file in docs_dir.rglob("*.mdx"):
        try:
            with open(mdx_file, 'r', encoding='utf-8') as f:
                content = f.read()
                clean_content = clean_markdown_content(content)

                # Extract chapter/module info from path
                relative_path = mdx_file.relative_to(docs_dir)
                path_parts = str(relative_path).split('/')

                metadata = {
                    "file_path": str(relative_path),
                    "filename": mdx_file.name,
                    "module": path_parts[0] if len(path_parts) > 1 else "unknown",
                    "chapter": path_parts[1] if len(path_parts) > 1 else mdx_file.name,
                    "source": f"{relative_path}"
                }

                mdx_files.append((str(relative_path), clean_content, metadata))
                logger.info(f"Read {mdx_file.name} ({len(clean_content)} chars)")

        except Exception as e:
            logger.error(f"Error reading {mdx_file}: {e}")

    logger.info(f"Found {len(mdx_files)} .mdx files")
    return mdx_files


async def create_embeddings_and_upsert(docs_path: str):
    """
    Read .mdx files, chunk them, create embeddings, and upsert to Qdrant.

    Args:
        docs_path: Path to the docs directory
    """
    logger.info("Starting book ingestion process...")

    # Initialize services
    qdrant_service.init_client()
    openai_service.init_client()

    # Read all .mdx files
    mdx_files = await read_mdx_files(docs_path)

    all_vectors = []
    vector_id = 0

    for file_path, content, metadata in mdx_files:
        logger.info(f"Processing {file_path}...")

        # Chunk the content
        chunks = chunk_text(content)
        logger.info(f"Created {len(chunks)} chunks for {file_path}")

        # Process each chunk
        for i, chunk in enumerate(chunks):
            try:
                # Create embedding for the chunk
                embedding = await openai_service.generate_embedding(chunk)

                # Create vector record
                vector_record = (
                    f"{file_path}_chunk_{i}",
                    embedding,
                    {**metadata, "chunk_id": i, "content": chunk}
                )

                all_vectors.append(vector_record)

                if len(all_vectors) % 10 == 0:  # Progress update every 10 vectors
                    logger.info(f"Processed {len(all_vectors)} chunks so far...")

            except Exception as e:
                logger.error(f"Error processing chunk {i} of {file_path}: {e}")

    logger.info(f"Created {len(all_vectors)} total vector records")

    # Upsert all vectors to Qdrant
    if all_vectors:
        logger.info("Upserting vectors to Qdrant...")
        success = await qdrant_service.upsert_vectors(all_vectors)

        if success:
            logger.info(f"Successfully upserted {len(all_vectors)} vectors to Qdrant")
        else:
            logger.error("Failed to upsert vectors to Qdrant")

    logger.info("Book ingestion process completed!")


async def main():
    """Main entry point for the ingestion script."""
    docs_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "docs")

    if not os.path.exists(docs_path):
        logger.error(f"Docs path does not exist: {docs_path}")
        return

    logger.info(f"Ingesting documents from: {docs_path}")

    try:
        await create_embeddings_and_upsert(docs_path)
    except Exception as e:
        logger.error(f"Error during ingestion: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())