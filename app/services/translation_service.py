"""Google Cloud Translation service for VoteDost."""
import logging
from typing import Optional
from google.cloud import translate_v2 as translate
from app.config import config

logger = logging.getLogger(__name__)

# Initialize client gracefully
translate_client = None
if config.PROJECT_ID:
    try:
        translate_client = translate.Client()
        logger.info("Translation client initialized")
    except Exception as e:
        logger.error(f"Failed to initialize Translation API: {e}")

def detect_language(text: str) -> Optional[str]:
    """Detects the language of a given text.
    
    Args:
        text: The text to analyze.
        
    Returns:
        The detected language code (e.g., 'en', 'hi') or None if failed.
    """
    if translate_client is None:
        return None
        
    try:
        result = translate_client.detect_language(text)
        return result["language"]
    except Exception as e:
        logger.error(f"Language detection error: {e}")
        return None

def get_translation_status() -> str:
    """Returns the status of Translation API connection for health checks."""
    return "connected" if translate_client is not None else "unavailable"
