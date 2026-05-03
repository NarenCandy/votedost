"""Google Cloud BigQuery service for VoteDost."""
import logging
from datetime import datetime
from google.cloud import bigquery
from app.config import config

logger = logging.getLogger(__name__)

# Initialize client gracefully
bigquery_client = None
if config.PROJECT_ID:
    try:
        bigquery_client = bigquery.Client(project=config.PROJECT_ID)
        logger.info("BigQuery client initialized")
    except Exception as e:
        logger.error(f"Failed to initialize BigQuery: {e}")

def log_to_bigquery(row_data: dict) -> bool:
    """Inserts a row into BigQuery for analytics.
    
    Args:
        row_data: Dictionary containing keys session_id, user_message, 
                 language, response_length, duration_ms.
    
    Returns:
        True if successful, False otherwise.
    """
    if bigquery_client is None:
        return False
        
    try:
        dataset_id = config.BIGQUERY_DATASET
        table_id = config.BIGQUERY_TABLE
        table_ref = bigquery_client.dataset(dataset_id).table(table_id)
        
        # Add timestamp if not present
        if "timestamp" not in row_data:
            row_data["timestamp"] = datetime.utcnow().isoformat()
            
        errors = bigquery_client.insert_rows_json(table_ref, [row_data])
        if errors:
            logger.error(f"BigQuery insertion errors: {errors}")
            return False
        return True
    except Exception as e:
        logger.error(f"BigQuery log error: {e}")
        return False

def get_bigquery_status() -> str:
    """Returns the status of BigQuery connection for health checks."""
    return "connected" if bigquery_client is not None else "unavailable"
