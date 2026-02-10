"""Cohere client configuration for Phase III AI Chatbot Integration.

Provides configured Cohere ClientV2 instance for the TodoChatAgent.
"""
import cohere
from ..config.settings import get_settings
import logging

logger = logging.getLogger(__name__)


def get_cohere_client() -> cohere.ClientV2:
    """Get configured Cohere client.

    Returns:
        Configured Cohere ClientV2 instance

    Raises:
        ValueError: If COHERE_API_KEY is not configured
    """
    settings = get_settings()

    if not settings.cohere_api_key:
        logger.error("COHERE_API_KEY not configured")
        raise ValueError(
            "COHERE_API_KEY is required for AI chatbot functionality. "
            "Please set it in your .env file."
        )

    logger.info("Initializing Cohere client")
    return cohere.ClientV2(api_key=settings.cohere_api_key)
