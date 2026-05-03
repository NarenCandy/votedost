"""Input validation functions for VoteDost."""
from typing import Optional, Dict, Any
from app.config import config
from app.utils.exceptions import ValidationError

def validate_chat_input(data: Optional[Dict[str, Any]]) -> str:
    """Validates the incoming chat request data.
    
    Args:
        data: The JSON payload from the request.
        
    Returns:
        The sanitized user message.
        
    Raises:
        ValidationError: If the input is invalid.
    """
    if not data:
        raise ValidationError("Empty request body")
        
    user_message = data.get("message")
    if user_message is None:
        raise ValidationError("Message is required")
        
    # Convert to string and strip whitespace, also handle null bytes
    user_message = str(user_message).replace('\x00', '').strip()
    
    if not user_message:
        raise ValidationError("Message cannot be empty")
        
    if len(user_message) > config.MAX_MESSAGE_LENGTH:
        raise ValidationError(f"Message exceeds limit of {config.MAX_MESSAGE_LENGTH} characters")
        
    return user_message

def validate_language(language: Optional[str]) -> str:
    """Validates and falls back for language selection.
    
    Args:
        language: The language string provided by user.
        
    Returns:
        A supported language string.
    """
    if not language or language not in config.SUPPORTED_LANGUAGES:
        return "English"
    return language
