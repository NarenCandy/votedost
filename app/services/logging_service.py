"""Google Cloud Logging and Monitoring service for VoteDost."""
import logging
from google.cloud import logging as cloud_logging
from app.config import config

logger = logging.getLogger(__name__)

cloud_logging_enabled = False

def setup_cloud_services():
    """Initializes Google Cloud Logging if project ID is available."""
    global cloud_logging_enabled
    if config.PROJECT_ID:
        try:
            client = cloud_logging.Client(project=config.PROJECT_ID)
            client.setup_logging()
            cloud_logging_enabled = True
            logging.info(f"Cloud Logging initialized for project: {config.PROJECT_ID}")
        except Exception as e:
            print(f"Failed to initialize Cloud services: {e}")

def get_logging_status() -> str:
    """Returns the status of Cloud Logging for health checks."""
    return "connected" if cloud_logging_enabled else "unavailable"
