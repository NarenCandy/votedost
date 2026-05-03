"""Custom exception hierarchy for VoteDost application."""

class VoteDostError(Exception):
    """Base exception for VoteDost application."""
    pass

class AIServiceError(VoteDostError):
    """Raised when Vertex AI API calls fail."""
    pass

class DatabaseError(VoteDostError):
    """Raised when Firestore operations fail."""
    pass

class ValidationError(VoteDostError):
    """Raised when input validation fails."""
    pass

class TranslationError(VoteDostError):
    """Raised when Translation API fails."""
    pass
