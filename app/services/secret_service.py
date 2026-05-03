"""Google Cloud Secret Manager service for VoteDost."""
import logging
from typing import Optional
from google.cloud import secretmanager
from app.config import config

logger = logging.getLogger(__name__)

def get_secret(secret_id: str, version_id: str = "latest") -> Optional[str]:
    """Fetches a secret value from Google Cloud Secret Manager.
    
    This pattern provides enterprise-grade credential management by avoiding
    environment variables for sensitive data.
    
    Args:
        secret_id: The ID of the secret to fetch.
        version_id: The version of the secret. Defaults to "latest".
        
    Returns:
        The secret payload string if successful, None otherwise.
    """
    if not config.PROJECT_ID:
        return None
        
    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{config.PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        logger.warning(f"Could not fetch secret {secret_id}: {e}")
        return None
