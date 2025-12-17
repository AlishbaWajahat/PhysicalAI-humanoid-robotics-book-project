import sys
import os
# Add the backend directory to the path to allow imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.utils.config import get_retrieval_config, get_cohere_config
from typing import Dict, List, Any, Optional
from agents import function_tool
from src.utils.config import get_retrieval_config, get_cohere_config
from src.utils.qdrant_client import create_qdrant_client, search_vectors, scroll_all_points
from src.utils.logger import get_logger, log_info, log_error
# Initialize logger
logger = get_logger(__name__)
import time



@function_tool
def retrieve_book_content(query: str, top_k: Optional[int] = 5, search_type: str = "semantic") -> List[Dict[str, Any]]:
    """
    Retrieve relevant book content from Qdrant vector database based on the query.
    """
    start_time = time.time()
    log_info(f"Retrieving book content for query: {query[:50]}... (search_type: {search_type})")

    try:
        client = create_qdrant_client()
        retrieval_config = get_retrieval_config()
        cohere_config = get_cohere_config()
        import cohere
        co = cohere.Client(cohere_config['api_key'])

        # Generate embedding
        response = co.embed(
            texts=[query],
            model='embed-english-v3.0',
            input_type="search_query"
        )
        query_embedding = response.embeddings[0]

        # Search vectors in Qdrant
        results = search_vectors(
            client=client,
            collection_name=retrieval_config['collection_name'],
            query_vector=query_embedding,
            top_k=top_k
        )

        retrieved_chunks = [
            {
                'id': r['id'],
                'text': r['payload'].get('text', ''),
                'relevance_score': r['score'],
                'source_path': r['payload'].get('source_path', ''),
                'title': r['payload'].get('title', ''),
                'metadata': r['payload']
            } for r in results
        ]

        elapsed_time = time.time() - start_time
        log_info(f"Retrieved {len(retrieved_chunks)} relevant chunks in {elapsed_time:.2f} seconds")

        if elapsed_time > 5.0:
            logger.warning(f"Performance warning: Retrieval took {elapsed_time:.2f} seconds")

        return retrieved_chunks

    except Exception as e:
        elapsed_time = time.time() - start_time
        log_error(f"Error retrieving book content after {elapsed_time:.2f} seconds: {str(e)}")
        return []


@function_tool
def search_book_content(query: str, top_k: Optional[int] = 5) -> List[Dict[str, Any]]:
    """
    Search for specific content or topics within the book using semantic search.
    """
    start_time = time.time()
    log_info(f"Searching book content for: {query[:50]}...")

    try:
        # Use retrieve_book_content internally for consistency
        results = retrieve_book_content(query=query, top_k=top_k, search_type="semantic")

        elapsed_time = time.time() - start_time
        log_info(f"Search returned {len(results)} results in {elapsed_time:.2f} seconds")

        if elapsed_time > 5.0:
            logger.warning(f"Performance warning: Search took {elapsed_time:.2f} seconds")

        return results

    except Exception as e:
        elapsed_time = time.time() - start_time
        log_error(f"Error searching book content after {elapsed_time:.2f} seconds: {str(e)}")
        return []


def format_search_results(results: List[Dict[str, Any]]) -> str:
    """
    Format search results for display.
    """
    if not results:
        return "No relevant content found for your search query."

    formatted = [f"Found {len(results)} relevant sections:\n"]
    for i, r in enumerate(results, 1):
        text_preview = r.get('text', '')[:200] + ('...' if len(r.get('text', '')) > 200 else '')
        formatted.append(
            f"{i}. {r.get('title', 'Untitled')}\n"
            f"   Source: {r.get('source_path', 'Unknown')}\n"
            f"   Relevance: {r.get('relevance_score', 0):.2f}\n"
            f"   Content Preview: {text_preview}\n"
        )
    return "\n".join(formatted)


@function_tool
def get_book_metadata(query: str = "") -> Dict[str, Any]:
    """
    Retrieve book metadata such as chapters, parts, and document titles.
    """
    start_time = time.time()
    log_info(f"Retrieving book metadata for query: {query}")

    try:
        client = create_qdrant_client()
        retrieval_config = get_retrieval_config()

        # Use scroll_all_points to get ALL documents for metadata aggregation
        results = scroll_all_points(
            client=client,
            collection_name=retrieval_config['collection_name'],
            batch_size=100
        )

        all_parts, all_chapters, all_sections, all_titles, all_source_paths = set(), set(), set(), set(), set()

        for r in results:
            payload = r.payload
            if 'parts' in payload: all_parts.update(payload['parts'])
            if 'chapters' in payload: all_chapters.update(payload['chapters'])
            if 'sections' in payload: all_sections.update(payload['sections'])
            if 'title' in payload and payload['title']: all_titles.add(payload['title'])
            if 'source_path' in payload and payload['source_path']: all_source_paths.add(payload['source_path'])

        metadata_response = {
            'total_documents': len(all_source_paths),
            'parts': list(all_parts),
            'chapters': list(all_chapters),
            'sections': list(all_sections),
            'titles': list(all_titles),
            'source_paths': list(all_source_paths)
        }

        # Filter by query if given
        q_lower = query.lower()
        if 'part' in q_lower: metadata_response = {'parts': list(all_parts)}
        elif 'chapter' in q_lower: metadata_response = {'chapters': list(all_chapters)}
        elif 'section' in q_lower: metadata_response = {'sections': list(all_sections)}
        elif 'title' in q_lower: metadata_response = {'titles': list(all_titles)}
        elif 'document' in q_lower or 'file' in q_lower: metadata_response = {'source_paths': list(all_source_paths)}

        elapsed_time = time.time() - start_time
        log_info(f"Retrieved metadata for {len(all_source_paths)} documents in {elapsed_time:.2f} seconds")
        if elapsed_time > 5.0:
            logger.warning(f"Performance warning: Metadata retrieval took {elapsed_time:.2f} seconds")

        return metadata_response

    except Exception as e:
        elapsed_time = time.time() - start_time
        log_error(f"Error retrieving book metadata after {elapsed_time:.2f} seconds: {str(e)}")
        return {"error": str(e)}


def format_metadata_results(metadata: Dict[str, Any]) -> str:
    """
    Format metadata results for display.
    """
    if not metadata or 'error' in metadata:
        return f"Could not retrieve metadata: {metadata.get('error', 'No metadata available') if metadata else 'No metadata available'}"

    formatted = []
    if 'total_documents' in metadata: formatted.append(f"Total Documents: {metadata['total_documents']}\n")
    if 'parts' in metadata and metadata['parts']:
        formatted.append("Book Parts:")
        formatted += [f"  {i+1}. {p}" for i, p in enumerate(metadata['parts'])]
    if 'chapters' in metadata and metadata['chapters']:
        formatted.append("Chapters:")
        formatted += [f"  {i+1}. {c}" for i, c in enumerate(metadata['chapters'])]
    if 'sections' in metadata and metadata['sections']:
        formatted.append("Sections:")
        formatted += [f"  {i+1}. {s}" for i, s in enumerate(metadata['sections'])]
    if 'titles' in metadata and metadata['titles']:
        formatted.append("Document Titles:")
        formatted += [f"  {i+1}. {t}" for i, t in enumerate(metadata['titles'])]
    if 'source_paths' in metadata and metadata['source_paths']:
        formatted.append("Available Documents:")
        formatted += [f"  {i+1}. {p}" for i, p in enumerate(metadata['source_paths'])]

    return "\n".join(formatted) if formatted else "No metadata available."