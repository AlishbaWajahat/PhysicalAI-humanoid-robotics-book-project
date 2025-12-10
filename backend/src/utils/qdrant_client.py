"""
Qdrant client configuration for the RAG Chatbot Backend.
Provides a configured Qdrant client instance for vector storage and retrieval.
"""
from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import Optional, Dict, Any, List
from .config import get_qdrant_config, get_indexing_config
from .logger import get_logger


logger = get_logger(__name__)


def create_qdrant_client() -> QdrantClient:
    """
    Create and return a configured Qdrant client instance.

    Returns:
        Configured QdrantClient instance
    """
    config = get_qdrant_config()

    client = QdrantClient(
        url=config['url'],
        api_key=config['api_key']
    )

    logger.info("Qdrant client created successfully")
    return client


def get_or_create_collection(
    client: QdrantClient,
    collection_name: Optional[str] = None
) -> str:
    """
    Get the collection name from config or use provided one, ensuring it exists.
    Note: The collection 'humanoid_ai_book' is expected to exist already.

    Args:
        client: Qdrant client instance
        collection_name: Optional collection name to use (defaults to config)

    Returns:
        The collection name that will be used
    """
    if collection_name is None:
        collection_name = get_qdrant_config()['collection_name']

    # Use the specific collection name if not overridden
    if collection_name == get_qdrant_config()['collection_name']:  # which is 'humanoid_ai_book' by default
        collection_name = "humanoid_ai_book"

    # Check if collection exists
    try:
        client.get_collection(collection_name)
        logger.info(f"Collection '{collection_name}' already exists")
    except Exception:
        logger.info(f"Collection '{collection_name}' does not exist. Creating new collection.")
        # Create collection with vector configuration
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=1024,  # Cohere embedding size
                distance=models.Distance.COSINE
            )
        )
        logger.info(f"Created new collection '{collection_name}'")

    return collection_name


def upsert_vectors(
    client: QdrantClient,
    collection_name: str,
    points: List[models.PointStruct]
) -> bool:
    """
    Upsert vectors into the specified collection.

    Args:
        client: Qdrant client instance
        collection_name: Name of the collection
        points: List of PointStruct objects to upsert

    Returns:
        True if successful, False otherwise
    """
    try:
        client.upsert(
            collection_name=collection_name,
            points=points
        )
        logger.info(f"Successfully upserted {len(points)} vectors to collection '{collection_name}'")
        return True
    except Exception as e:
        logger.error(f"Failed to upsert vectors: {str(e)}")
        return False


def search_vectors(
    client: QdrantClient,
    collection_name: str,
    query_vector: List[float],
    top_k: int = 5,
    metadata_filter: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """
    Search for similar vectors in the collection.

    Args:
        client: Qdrant client instance
        collection_name: Name of the collection
        query_vector: Vector to search for similar vectors
        top_k: Number of results to return (default: 5)
        metadata_filter: Optional filter for metadata fields

    Returns:
        List of matching vectors with their payload data
    """
    try:
        # Prepare filter if provided
        qdrant_filter = None
        if metadata_filter:
            filter_conditions = []
            for key, value in metadata_filter.items():
                filter_conditions.append(
                    models.FieldCondition(
                        key=key,
                        match=models.MatchValue(value=value)
                    )
                )

            if filter_conditions:
                qdrant_filter = models.Filter(
                    must=filter_conditions
                )

        # Check which search method is available and use it
        if hasattr(client, 'search'):
            # Newer version of qdrant-client
            results = client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                limit=top_k,
                query_filter=qdrant_filter
            )
        elif hasattr(client, 'search_points'):
            # Older version of qdrant-client
            results = client.search_points(
                collection_name=collection_name,
                vector=query_vector,
                limit=top_k,
                filter=qdrant_filter
            )
        else:
            # If neither method exists, log an error and return empty results
            logger.error("Qdrant client does not have 'search' or 'search_points' methods")
            return []

        # Format results to include payload and score
        formatted_results = []
        for result in results:
            # Handle different result formats depending on the method used
            if hasattr(result, 'id') and hasattr(result, 'payload') and hasattr(result, 'score'):
                # Result from newer API
                formatted_results.append({
                    'id': result.id,
                    'payload': result.payload,
                    'score': result.score,
                    'vector': getattr(result, 'vector', None)
                })
            else:
                # Handle other result formats if needed
                logger.warning(f"Unexpected result format: {result}")
                continue

        logger.info(f"Successfully searched vectors, found {len(formatted_results)} results")
        return formatted_results
    except Exception as e:
        logger.error(f"Failed to search vectors: {str(e)}")
        return []


def delete_collection(
    client: QdrantClient,
    collection_name: str
) -> bool:
    """
    Delete the specified collection.

    Args:
        client: Qdrant client instance
        collection_name: Name of the collection to delete

    Returns:
        True if successful, False otherwise
    """
    try:
        client.delete_collection(collection_name)
        logger.info(f"Successfully deleted collection '{collection_name}'")
        return True
    except Exception as e:
        logger.error(f"Failed to delete collection: {str(e)}")
        return False


def count_vectors(
    client: QdrantClient,
    collection_name: str
) -> int:
    """
    Count the number of vectors in the collection.

    Args:
        client: Qdrant client instance
        collection_name: Name of the collection

    Returns:
        Number of vectors in the collection
    """
    try:
        count_result = client.count(
            collection_name=collection_name
        )
        return count_result.count
    except Exception as e:
        logger.error(f"Failed to count vectors: {str(e)}")
        return 0