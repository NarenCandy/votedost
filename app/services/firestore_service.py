"""Google Cloud Firestore service for VoteDost."""
import logging
from typing import Optional
from google.cloud import firestore
from app.config import config
from app.utils.exceptions import DatabaseError

logger = logging.getLogger(__name__)

# Initialize client gracefully
firestore_client = None
if config.PROJECT_ID:
    try:
        firestore_client = firestore.Client(project=config.PROJECT_ID)
        logger.info("Firestore client initialized")
    except Exception as e:
        logger.error(f"Failed to initialize Firestore: {e}")

def save_chat_to_firestore(
    session_id: str,
    user_message: str,
    bot_response: str,
    language: str,
    duration_ms: float
) -> bool:
    """Saves a chat interaction to Google Cloud Firestore.
    
    Args:
        session_id: Unique identifier for the chat session.
        user_message: The message sent by the user.
        bot_response: The AI-generated response.
        language: The language used in this interaction.
        duration_ms: Time taken to generate response in milliseconds.
    
    Returns:
        True if save was successful, False otherwise.
    """
    if firestore_client is None:
        return False
        
    try:
        # 1. Save individual chat session
        doc_ref = firestore_client.collection(config.FIRESTORE_COLLECTION).document()
        doc_ref.set({
            "session_id": session_id,
            "user_message": user_message,
            "bot_response": bot_response,
            "language": language,
            "duration_ms": duration_ms,
            "timestamp": firestore.SERVER_TIMESTAMP
        })
        
        # 2. Update aggregate analytics
        analytics_ref = firestore_client.collection("analytics").document("summary")
        analytics_ref.set({
            "total_queries": firestore.Increment(1),
            f"lang_{language.lower()}": firestore.Increment(1)
        }, merge=True)
        
        return True
    except Exception as e:
        logger.error(f"Firestore save error: {e}")
        return False

def get_firestore_status() -> str:
    """Returns the status of Firestore connection for health checks."""
    return "connected" if firestore_client is not None else "unavailable"
