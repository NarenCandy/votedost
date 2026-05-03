from dataclasses import dataclass, field
from typing import List
import os

@dataclass
class AppConfig:
    """Application configuration with validation.
    
    This class handles all environment variables and constants used across the 
    application, providing a centralized place for configuration.
    """
    PROJECT_ID: str = field(default_factory=lambda: os.getenv('GOOGLE_CLOUD_PROJECT', ''))
    LOCATION: str = field(default_factory=lambda: os.getenv('LOCATION', 'us-central1'))
    MAX_MESSAGE_LENGTH: int = 2000
    CACHE_SIZE: int = 128
    MODEL_NAME: str = "gemini-2.5-flash"
    SUPPORTED_LANGUAGES: List[str] = field(default_factory=lambda: [
        "English", "Hindi", "Tamil", "Telugu", "Kannada", "Bengali", "Marathi"
    ])
    BIGQUERY_DATASET: str = "votedost_analytics"
    BIGQUERY_TABLE: str = "query_logs"
    FIRESTORE_COLLECTION: str = "chat_sessions"
    
    def __post_init__(self):
        """Validate configuration on initialization.
        
        Raises:
            ValueError: If configuration values are invalid.
        """
        if self.MAX_MESSAGE_LENGTH <= 0:
            raise ValueError("MAX_MESSAGE_LENGTH must be positive")
        if self.CACHE_SIZE <= 0:
            raise ValueError("CACHE_SIZE must be positive")
    
    @property
    def is_production(self) -> bool:
        """Check if running in production (GCP environment).
        
        Returns:
            True if PROJECT_ID is set, indicating a GCP environment.
        """
        return bool(self.PROJECT_ID)

config = AppConfig()
