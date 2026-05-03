"""Vertex AI service for VoteDost using Gemini models."""
import logging
import functools
from typing import Tuple, List, Dict, Optional
import vertexai
from vertexai.generative_models import GenerativeModel, Content, Part
from app.config import config
from app.utils.exceptions import AIServiceError

logger = logging.getLogger(__name__)

# Initialize Vertex AI
model = None
try:
    if config.PROJECT_ID:
        vertexai.init(project=config.PROJECT_ID, location=config.LOCATION)
        
        system_instruction = (
            "You are VoteDost, a friendly and knowledgeable Indian election assistant. "
            "Help users understand the Indian election process, ECI, voting steps, voter ID, timelines, EVMs, "
            "candidate eligibility, and related topics. Be conversational, simple, and easy to understand. "
            "Detect the language the user is typing in and respond in that same language. "
            "Default to English if unsure. Support Hindi, Tamil, Telugu, Kannada, Bengali, Marathi, and English at minimum. "
            "Use simple words to feel friendly."
        )

        model = GenerativeModel(
            config.MODEL_NAME,
            system_instruction=[system_instruction]
        )
        logger.info(f"Vertex AI initialized with model: {config.MODEL_NAME}")
except Exception as e:
    logger.error(f"Failed to initialize Vertex AI Model: {e}")

@functools.lru_cache(maxsize=128)
def get_ai_response(message: str, language: str, history_tuple: Tuple[Tuple[Tuple, ...], ...]) -> str:
    """Calls Vertex AI to get a response. Cached based on message, language, and history.
    
    Args:
        message: The user's input message.
        language: The requested response language.
        history_tuple: A hashable representation of the chat history.
        
    Returns:
        The generated response text.
        
    Raises:
        AIServiceError: If the model is not loaded or generation fails.
    """
    if not model:
        raise AIServiceError("AI Model not initialized")

    try:
        # Reconstruct history for Vertex AI
        formatted_history = []
        for msg_tuple in history_tuple:
            msg_dict = dict(msg_tuple)
            role = "user" if msg_dict["role"] == "user" else "model"
            # Handle standard role names from frontend (assistant -> model)
            if msg_dict["role"] == "assistant":
                role = "model"
            formatted_history.append(Content(role=role, parts=[Part.from_text(msg_dict["content"])]))

        chat_session = model.start_chat(history=formatted_history)
        
        # Prepend language instruction to guide the model
        enhanced_message = f"[{language} language requested] {message}"
        response = chat_session.send_message(enhanced_message)
        
        return response.text
    except Exception as e:
        logger.error(f"Vertex AI generation error: {e}")
        raise AIServiceError(f"Generation failed: {str(e)}")

def get_ai_status() -> str:
    """Returns the status of Vertex AI connection for health checks."""
    return "connected" if model is not None else "unavailable"
