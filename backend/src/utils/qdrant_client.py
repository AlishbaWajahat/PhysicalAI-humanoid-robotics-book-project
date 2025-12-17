"""
Qdrant client configuration for the RAG Chatbot Backend.
Provides a configured Qdrant client instance for vector storage and retrieval.
"""
import os
from typing import Optional, Dict, Any, List
from qdrant_client import QdrantClient
from qdrant_client.http import models
from .config import get_qdrant_config
from .logger import get_logger, log_info, log_error

logger = get_logger(__name__)


def create_qdrant_client() -> QdrantClient:
    """
    Create and return a configured Qdrant client instance.
    """
    config = get_qdrant_config()

    try:
        client = QdrantClient(
            url=config['url'],
            api_key=config['api_key'],
            timeout=30
        )
        # Verify connection
        client.get_collections()
        log_info("Qdrant client created and connection verified successfully")
        return client
    except Exception as e:
        log_error(f"Failed to create Qdrant client or verify connection: {str(e)}")
        raise


def get_or_create_collection(client: QdrantClient, collection_name: Optional[str] = None) -> str:
    """
    Ensure the collection exists; create it if missing.
    """
    if collection_name is None:
        collection_name = get_qdrant_config()['collection_name']

    try:
        client.get_collection(collection_name)
        log_info(f"Collection '{collection_name}' exists")
    except Exception:
        log_info(f"Collection '{collection_name}' not found. Creating new collection.")
        try:
            client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=1024,
                    distance=models.Distance.COSINE
                )
            )
            log_info(f"Collection '{collection_name}' created successfully")
        except Exception as e:
            log_error(f"Failed to create collection '{collection_name}': {str(e)}")
            raise

    return collection_name


def upsert_vectors(client: QdrantClient, collection_name: str, points: List[models.PointStruct]) -> bool:
    """
    Upsert vectors into the collection.
    """
    try:
        client.upsert(collection_name=collection_name, points=points)
        log_info(f"Upserted {len(points)} vectors into '{collection_name}'")
        return True
    except Exception as e:
        log_error(f"Failed to upsert vectors: {str(e)}")
        return False


def search_vectors(
    client: QdrantClient,
    collection_name: str,
    query_vector: List[float],
    top_k: int = 5,
    metadata_filter: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """
    Search vectors in a collection and return formatted results.
    """
    try:
        qdrant_filter = None
        if metadata_filter:
            filter_conditions = [
                models.FieldCondition(key=k, match=models.MatchValue(value=v))
                for k, v in metadata_filter.items()
            ]
            if filter_conditions:
                qdrant_filter = models.Filter(must=filter_conditions)

        # Use query_points for newer qdrant-client versions
        try:
            results = client.query_points(
                collection_name=collection_name,
                query=query_vector,
                limit=top_k,
                query_filter=qdrant_filter,
                with_payload=True
            )
            formatted_results = [
                {'id': r.id, 'payload': r.payload, 'score': r.score}
                for r in results.points
            ]
        except AttributeError:
            # Fallback to older search method
            results = client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                limit=top_k,
                filter=qdrant_filter,
                with_payload=True
            )
            formatted_results = [
                {'id': r.id, 'payload': r.payload, 'score': r.score}
                for r in results
            ]
        log_info(f"Search found {len(formatted_results)} results in '{collection_name}'")
        return formatted_results

    except Exception as e:
        log_error(f"Failed to search vectors: {str(e)}")
        return []


def scroll_all_points(client: QdrantClient, collection_name: str, batch_size: int = 100, max_points: int = 1000) -> List[Dict[str, Any]]:
    """
    Scroll points in a collection (useful for metadata retrieval).
    Limited to max_points to prevent timeouts.
    """
    all_points = []
    offset = 0

    while len(all_points) < max_points:
        try:
            points, _ = client.scroll(
                collection_name=collection_name,
                limit=min(batch_size, max_points - len(all_points)),
                offset=offset,
                with_payload=True
            )
            if not points:
                break
            all_points.extend(points)
            offset += batch_size
        except Exception as e:
            log_error(f"Error scrolling points: {str(e)}")
            break

    log_info(f"Scrolled {len(all_points)} points from '{collection_name}' (max: {max_points})")
    return all_points


def delete_collection(client: QdrantClient, collection_name: str) -> bool:
    """
    Delete a collection.
    """
    try:
        client.delete_collection(collection_name)
        log_info(f"Deleted collection '{collection_name}'")
        return True
    except Exception as e:
        log_error(f"Failed to delete collection '{collection_name}': {str(e)}")
        return False


def count_vectors(client: QdrantClient, collection_name: str) -> int:
    """
    Count vectors in a collection.
    """
    try:
        count_result = client.count(collection_name=collection_name)
        return count_result.count
    except Exception as e:
        log_error(f"Failed to count vectors: {str(e)}")
        return 0

