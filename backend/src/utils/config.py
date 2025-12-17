"""
Configuration utility for loading environment variables securely.
"""
import os
from typing import Optional
from dotenv import load_dotenv


def validate_config(config: dict) -> list:
    """
    Validate the configuration values.

    Args:
        config: Configuration dictionary to validate

    Returns:
        list: List of validation errors, empty if all validations pass
    """
    errors = []

    # Check required keys exist
    required_keys = ['qdrant_api_key', 'qdrant_url', 'cohere_api_key', 'gemini_api_key']
    for key in required_keys:
        if not config.get(key):
            errors.append(f"Missing required configuration key: {key}")

    # Validate URL format
    import re
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if config.get('qdrant_url') and not url_pattern.match(config['qdrant_url']):
        errors.append(f"Invalid URL format for qdrant_url: {config['qdrant_url']}")

    # Validate numeric values
    try:
        chunk_size = config['chunk_size']
        if not (100 <= chunk_size <= 2048):
            errors.append(f"chunk_size ({chunk_size}) must be between 100 and 2048")
    except (ValueError, TypeError):
        errors.append("chunk_size must be a valid integer")

    try:
        chunk_overlap = config['chunk_overlap']
        if not (0 <= chunk_overlap <= 500):
            errors.append(f"chunk_overlap ({chunk_overlap}) must be between 0 and 500")
    except (ValueError, TypeError):
        errors.append("chunk_overlap must be a valid integer")

    try:
        top_k = config['top_k_retrieval']
        if not (1 <= top_k <= 20):
            errors.append(f"top_k_retrieval ({top_k}) must be between 1 and 20")
    except (ValueError, TypeError):
        errors.append("top_k_retrieval must be a valid integer")

    # Check API key formats (basic validation)
    if config.get('cohere_api_key') and len(config['cohere_api_key']) < 10:
        errors.append("cohere_api_key appears to be too short (likely invalid)")

    if config.get('gemini_api_key') and len(config['gemini_api_key']) < 10:
        errors.append("gemini_api_key appears to be too short (likely invalid)")

    if config.get('qdrant_api_key') and len(config['qdrant_api_key']) < 10:
        errors.append("qdrant_api_key appears to be too short (likely invalid)")

    return errors


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

    # Validate configuration
    validation_errors = validate_config(config)
    if validation_errors:
        error_msg = "\n".join(validation_errors)
        raise ValueError(f"Configuration validation failed:\n{error_msg}")

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