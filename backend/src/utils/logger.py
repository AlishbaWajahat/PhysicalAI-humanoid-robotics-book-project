"""
Logger utility for the RAG Chatbot Backend.
Provides structured logging for debugging and monitoring.
"""
import logging
import sys
from typing import Optional


def setup_logger(name: str = "rag_chatbot", level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with the specified name and level.

    Args:
        name: Name of the logger
        level: Logging level (default: INFO)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Avoid adding multiple handlers to the same logger
    if logger.handlers:
        return logger

    logger.setLevel(level)

    # Create console handler with formatting
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    # Create file handler with formatting
    file_handler = logging.FileHandler("rag_chatbot.log")
    file_handler.setLevel(level)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def get_logger(name: str = "rag_chatbot") -> logging.Logger:
    """
    Get a logger instance with the specified name.

    Args:
        name: Name of the logger (default: "rag_chatbot")

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


# Default logger instance
logger = setup_logger()


def log_info(message: str, extra: Optional[dict] = None) -> None:
    """
    Log an info message.

    Args:
        message: The message to log
        extra: Additional context information
    """
    if extra:
        logger.info(f"{message} | Context: {extra}")
    else:
        logger.info(message)


def log_error(message: str, extra: Optional[dict] = None, exc_info: bool = False) -> None:
    """
    Log an error message.

    Args:
        message: The message to log
        extra: Additional context information
        exc_info: Whether to include exception information
    """
    if extra:
        logger.error(f"{message} | Context: {extra}", exc_info=exc_info)
    else:
        logger.error(message, exc_info=exc_info)


def log_warning(message: str, extra: Optional[dict] = None) -> None:
    """
    Log a warning message.

    Args:
        message: The message to log
        extra: Additional context information
    """
    if extra:
        logger.warning(f"{message} | Context: {extra}")
    else:
        logger.warning(message)


def log_debug(message: str, extra: Optional[dict] = None) -> None:
    """
    Log a debug message.

    Args:
        message: The message to log
        extra: Additional context information
    """
    if extra:
        logger.debug(f"{message} | Context: {extra}")
    else:
        logger.debug(message)


def log_success(message: str, extra: Optional[dict] = None) -> None:
    """
    Log a success message.

    Args:
        message: The message to log
        extra: Additional context information
    """
    if extra:
        logger.info(f"SUCCESS: {message} | Context: {extra}")
    else:
        logger.info(f"SUCCESS: {message}")