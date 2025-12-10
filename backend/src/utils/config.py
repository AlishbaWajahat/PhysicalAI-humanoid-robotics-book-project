"""
Configuration utility for loading environment variables securely.
"""
import os
from typing import Optional
from dotenv import load_dotenv


def load_config() -> dict:
    """
    Load configuration from environment variables.

    Returns:
        dict: Configuration dictionary with all required settings
    """
    # Load environment variables from .env file
    load_dotenv()

    config = {
        'qdrant_api_key': os.getenv('QDRANT_API_KEY'),
        'qdrant_url': os.getenv('QDRANT_URL'),
        'cohere_api_key': os.getenv('COHERE_API_KEY'),
        'gemini_api_key': os.getenv('GEMINI_API_KEY'),
        'collection_name': 'humanoid_ai_book',  # Fixed collection name as per requirements
        'chunk_size': int(os.getenv('CHUNK_SIZE', '512')),
        'chunk_overlap': int(os.getenv('CHUNK_OVERLAP', '50')),
        'top_k_retrieval': int(os.getenv('TOP_K_RETRIEVAL', '5'))
    }

    # Validate required configuration
    required_keys = ['qdrant_api_key', 'qdrant_url', 'cohere_api_key', 'gemini_api_key']
    missing_keys = [key for key in required_keys if not config[key]]

    if missing_keys:
        raise ValueError(f"Missing required configuration keys: {', '.join(missing_keys)}")

    return config


def get_config_value(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    Get a specific configuration value by key.

    Args:
        key: The configuration key to retrieve
        default: Default value if key is not found

    Returns:
        The configuration value or default if not found
    """
    load_dotenv()
    return os.getenv(key.upper(), default)


# Initialize configuration
config = load_config()


def get_qdrant_config() -> dict:
    """
    Get Qdrant-specific configuration.

    Returns:
        dict: Qdrant configuration
    """
    return {
        'api_key': config['qdrant_api_key'],
        'url': config['qdrant_url'],
        'collection_name': config['collection_name']
    }


def get_cohere_config() -> dict:
    """
    Get Cohere-specific configuration.

    Returns:
        dict: Cohere configuration
    """
    return {
        'api_key': config['cohere_api_key']
    }


def get_gemini_config() -> dict:
    """
    Get Gemini-specific configuration.

    Returns:
        dict: Gemini configuration
    """
    return {
        'api_key': config['gemini_api_key']
    }


def get_indexing_config() -> dict:
    """
    Get indexing-specific configuration.

    Returns:
        dict: Indexing configuration
    """
    return {
        'chunk_size': config['chunk_size'],
        'chunk_overlap': config['chunk_overlap'],
        'collection_name': config['collection_name']
    }


def get_retrieval_config() -> dict:
    """
    Get retrieval-specific configuration.

    Returns:
        dict: Retrieval configuration
    """
    return {
        'top_k': config['top_k_retrieval'],
        'collection_name': config['collection_name']
    }