"""
Content indexing script for the RAG Chatbot Backend.
Extracts content from MDX files, chunks it, creates embeddings, and stores in Qdrant.
"""
import os
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple
from markdown import markdown
import frontmatter  # For parsing MD/MDX files with metadata

import sys
import os
# Add the backend directory to the path to allow imports
sys.path.append(os.path.join(os.path.dirname(__file__)))

from src.utils.config import get_cohere_config, get_indexing_config
from src.utils.qdrant_client import create_qdrant_client, get_or_create_collection, upsert_vectors
from src.utils.logger import get_logger, log_info, log_error, log_debug
from src.utils.models import BookContent, TextChunk, Embedding, VectorRecord

# Initialize logger
logger = get_logger(__name__)

# Import Cohere
import cohere

def extract_content(docs_path: str = "../docs/") -> List[BookContent]:
    """
    Extract text content from MDX files in the specified docs directory.

    Args:
        docs_path: Path to the docs directory (default: "../docs/" - relative to backend)

    Returns:
        List of BookContent objects with extracted content
    """
    log_info(f"Starting content extraction from {docs_path}")

    book_contents = []
    docs_dir = Path(docs_path)

    if not docs_dir.exists():
        log_error(f"Docs directory does not exist: {docs_path}")
        return book_contents

    # Find all MD and MDX files in the docs directory
    md_files = list(docs_dir.rglob("*.md")) + list(docs_dir.rglob("*.mdx"))

    log_info(f"Found {len(md_files)} files to process")

    for file_path in md_files:
        try:
            # Read the file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse the frontmatter and content
            try:
                post = frontmatter.loads(content)
                text_content = post.content
                metadata = post.metadata
            except Exception:
                # If frontmatter parsing fails, treat the whole content as text
                text_content = content
                metadata = {}

            # Convert MDX/Markdown to plain text if needed
            # Remove JSX components and extract plain text
            plain_text = extract_plain_text(text_content)

            # Create path relative to the docs directory for source_path
            # Convert to absolute paths for comparison
            abs_file_path = file_path.resolve()
            abs_docs_path = Path("../docs/").resolve()

            try:
                # Get the relative path from docs directory
                relative_to_docs = abs_file_path.relative_to(abs_docs_path)
                relative_path = f"docs/{relative_to_docs.as_posix()}"
            except ValueError:
                # If the file is not within docs_path, use a simplified path
                relative_path = file_path.name

            # Create BookContent object
            book_content = BookContent(
                source_path=relative_path,
                content=plain_text,
                title=metadata.get('title', ''),
                metadata=metadata
            )

            book_contents.append(book_content)
            log_debug(f"Extracted content from {relative_path}")

        except Exception as e:
            log_error(f"Error processing file {file_path}: {str(e)}")

    log_info(f"Content extraction completed. Extracted {len(book_contents)} content items")
    return book_contents


def extract_plain_text(mdx_content: str) -> str:
    """
    Extract plain text from MDX content by removing JSX components.

    Args:
        mdx_content: Raw MDX content

    Returns:
        Plain text content
    """
    # Remove JSX components (blocks that start with < and end with >)
    # This is a simplified approach - for more complex JSX, a proper parser would be needed
    jsx_pattern = r'<[^>]*>'
    plain_text = re.sub(jsx_pattern, '', mdx_content)

    # Convert markdown to plain text
    try:
        html = markdown(plain_text)
        # Remove HTML tags to get plain text
        plain_text = re.sub(r'<[^>]+>', '', html)
    except Exception:
        # If markdown conversion fails, return the text without JSX
        pass

    return plain_text


def chunk_text(book_contents: List[BookContent], chunk_size: int = 512, chunk_overlap: int = 50) -> List[TextChunk]:
    """
    Chunk the extracted book content into manageable segments.

    Args:
        book_contents: List of BookContent objects
        chunk_size: Maximum size of each chunk (default: 512)
        chunk_overlap: Number of overlapping characters between chunks (default: 50)

    Returns:
        List of TextChunk objects
    """
    log_info(f"Starting text chunking with chunk_size={chunk_size}, overlap={chunk_overlap}")

    text_chunks = []
    chunk_index = 0

    for book_content in book_contents:
        content = book_content.content
        content_id = book_content.id

        # Simple approach: split by sentences or paragraphs
        # For more sophisticated chunking, we could use libraries like langchain
        sentences = re.split(r'[.!?]+\s+', content)

        current_chunk = ""
        current_chunk_size = 0

        for sentence in sentences:
            sentence_size = len(sentence)

            # If adding this sentence would exceed chunk size
            if current_chunk_size + sentence_size > chunk_size and current_chunk:
                # Save the current chunk
                text_chunk = TextChunk(
                    content_id=content_id,
                    text=current_chunk.strip(),
                    chunk_index=chunk_index,
                    metadata={
                        'source_path': book_content.source_path,
                        'title': book_content.title,
                        'original_chunk_size': len(current_chunk)
                    }
                )
                text_chunks.append(text_chunk)
                chunk_index += 1

                # Start a new chunk with overlap
                # Take the end of the current chunk as overlap
                overlap_start = max(0, len(current_chunk) - chunk_overlap)
                current_chunk = current_chunk[overlap_start:] + " " + sentence
                current_chunk_size = len(current_chunk)
            else:
                # Add sentence to current chunk
                if current_chunk:
                    current_chunk += " " + sentence
                else:
                    current_chunk = sentence
                current_chunk_size += sentence_size + 1  # +1 for space

        # Add the last chunk if it has content
        if current_chunk.strip():
            text_chunk = TextChunk(
                content_id=content_id,
                text=current_chunk.strip(),
                chunk_index=chunk_index,
                metadata={
                    'source_path': book_content.source_path,
                    'title': book_content.title,
                    'original_chunk_size': len(current_chunk)
                }
            )
            text_chunks.append(text_chunk)
            chunk_index += 1

    log_info(f"Text chunking completed. Created {len(text_chunks)} chunks")
    return text_chunks


def generate_embeddings(text_chunks: List[TextChunk]) -> List[Embedding]:
    """
    Generate vector embeddings for text chunks using Cohere.

    Args:
        text_chunks: List of TextChunk objects

    Returns:
        List of Embedding objects
    """
    log_info(f"Starting embedding generation for {len(text_chunks)} text chunks")

    # Initialize Cohere client
    cohere_config = get_cohere_config()
    co = cohere.Client(cohere_config['api_key'])

    embeddings = []

    # Process in batches to avoid hitting API limits
    batch_size = 96  # Cohere's API limit is typically 96 texts per request

    for i in range(0, len(text_chunks), batch_size):
        batch = text_chunks[i:i + batch_size]
        batch_texts = [chunk.text for chunk in batch]

        try:
            # Generate embeddings
            response = co.embed(
                texts=batch_texts,
                model='embed-english-v3.0',  # Using Cohere's English embedding model
                input_type="search_document"  # Specify this is for search documents
            )

            # Create Embedding objects
            for j, embedding_vector in enumerate(response.embeddings):
                embedding = Embedding(
                    chunk_id=batch[j].id,
                    vector=embedding_vector,
                    model_name='embed-english-v3.0',
                    model_version='3.0'
                )
                embeddings.append(embedding)

        except Exception as e:
            log_error(f"Error generating embeddings for batch {i//batch_size + 1}: {str(e)}")
            # Continue with the next batch
            continue

    log_info(f"Embedding generation completed. Generated {len(embeddings)} embeddings")
    return embeddings


def store_in_qdrant(embeddings: List[Embedding], text_chunks: List[TextChunk]) -> bool:
    """
    Store embeddings in Qdrant vector database with proper metadata.

    Args:
        embeddings: List of Embedding objects
        text_chunks: Corresponding TextChunk objects for metadata

    Returns:
        True if successful, False otherwise
    """
    log_info(f"Starting storage of {len(embeddings)} embeddings in Qdrant")

    # Create Qdrant client
    client = create_qdrant_client()

    # Get or create collection (using the specified collection name)
    collection_name = get_or_create_collection(client)

    # Create PointStruct objects for upsertion
    points = []

    # Create a mapping from chunk_id to TextChunk for metadata lookup
    chunk_map = {chunk.id: chunk for chunk in text_chunks}

    for embedding in embeddings:
        chunk = chunk_map.get(embedding.chunk_id)
        if not chunk:
            log_error(f"Could not find text chunk for embedding with chunk_id: {embedding.chunk_id}")
            continue

        # Get the original book content for additional metadata
        book_content = None
        # In a real implementation, we'd have a way to get the original book content
        # For now, we'll use what's in the chunk metadata

        # Create payload with metadata
        payload = {
            'text': chunk.text,
            'source_path': chunk.metadata.get('source_path', ''),
            'title': chunk.metadata.get('title', ''),
            'chunk_index': chunk.chunk_index,
            'content_id': chunk.content_id
        }

        # Add any additional metadata from the chunk
        for key, value in chunk.metadata.items():
            if key not in payload:
                payload[key] = value

        # Create PointStruct
        point = {
            "id": embedding.chunk_id,
            "vector": embedding.vector,
            "payload": payload
        }

        points.append(point)

    # Convert to Qdrant PointStruct format
    from qdrant_client.http import models
    point_structs = [
        models.PointStruct(
            id=point["id"],
            vector=point["vector"],
            payload=point["payload"]
        )
        for point in points
    ]

    # Upsert vectors to Qdrant
    success = upsert_vectors(client, collection_name, point_structs)

    if success:
        log_info(f"Successfully stored {len(point_structs)} vectors in Qdrant collection '{collection_name}'")
    else:
        log_error("Failed to store vectors in Qdrant")

    return success


def main_indexing_pipeline(docs_path: str = "docs/") -> bool:
    """
    Main orchestrator function that runs the complete indexing pipeline:
    1. Extract content from MDX files
    2. Chunk the text
    3. Generate embeddings
    4. Store in Qdrant

    Args:
        docs_path: Path to the docs directory (default: "docs/")

    Returns:
        True if successful, False otherwise
    """
    log_info("Starting the complete indexing pipeline")

    try:
        # Get indexing configuration
        config = get_indexing_config()

        # Step 1: Extract content
        book_contents = extract_content(docs_path)
        if not book_contents:
            log_error("No content extracted, stopping pipeline")
            return False

        # Step 2: Chunk text
        text_chunks = chunk_text(
            book_contents,
            chunk_size=config['chunk_size'],
            chunk_overlap=config['chunk_overlap']
        )
        if not text_chunks:
            log_error("No text chunks created, stopping pipeline")
            return False

        # Step 3: Generate embeddings
        embeddings = generate_embeddings(text_chunks)
        if not embeddings:
            log_error("No embeddings generated, stopping pipeline")
            return False

        # Step 4: Store in Qdrant
        success = store_in_qdrant(embeddings, text_chunks)

        if success:
            log_info("Indexing pipeline completed successfully")
        else:
            log_error("Indexing pipeline failed during storage step")

        return success

    except Exception as e:
        log_error(f"Indexing pipeline failed with error: {str(e)}")
        return False


if __name__ == "__main__":
    # Run the main indexing pipeline
    success = main_indexing_pipeline()
    if success:
        print("Content indexing completed successfully!")
    else:
        print("Content indexing failed!")
        exit(1)