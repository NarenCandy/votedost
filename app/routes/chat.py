"""Routes for VoteDost application."""
import time
import os
import logging
import uuid
from typing import Tuple, Any
from flask import Blueprint, render_template, request, jsonify, g
from app.config import config
from app.utils.validators import validate_chat_input, validate_language
from app.utils.cache import dict_to_tuple
from app.utils.exceptions import AIServiceError, ValidationError
from app.services.logging_service import get_logging_status
from app import limiter

logger = logging.getLogger(__name__)
chat_bp = Blueprint('chat', __name__)

from app.services import ai_service
from app.services import firestore_service
from app.services import bigquery_service
from app.services import translation_service

# Re-export for test patching
model = ai_service.model
get_ai_response = ai_service.get_ai_response
save_chat_to_firestore = firestore_service.save_chat_to_firestore
log_to_bigquery = bigquery_service.log_to_bigquery
detect_language = translation_service.detect_language

@chat_bp.route("/")
def index() -> str:
    """Renders the main application page."""
    return render_template("index.html")

@chat_bp.route("/health")
def health() -> Tuple[Any, int]:
    """Comprehensive health check for all services."""
    services_status = {
        "vertex_ai": ai_service.get_ai_status(),
        "cloud_logging": get_logging_status(),
        "firestore": firestore_service.get_firestore_status(),
        "bigquery": bigquery_service.get_bigquery_status(),
        "translation": translation_service.get_translation_status(),
    }
    return jsonify({
        "status": "ok",
        "model_loaded": ai_service.model is not None,
        "project_id": config.PROJECT_ID or "not_set",
        "version": "1.0.0",
        "timestamp": time.time(),
        "services": services_status
    }), 200

@chat_bp.route("/chat", methods=["POST"])
def chat() -> Tuple[Any, int]:
    """Main chat endpoint. Validates input, detects language, and returns AI response."""
    # Bug fix: Rate limit exemption for tests
    if request.environ.get('flask_limiter.exempt') is None and os.getenv('VOTEDOST_TESTING') == 'true':
         pass # Handled by app.config['RATELIMIT_ENABLED'] = False in factory
    
    # Bug fix: Check model status at request time
    # We use a helper to ensure we catch the latest patched version
    from app.routes.chat import model as current_model
    if not current_model:
        return jsonify({"error": "AI Model not initialized"}), 500

    start_time = time.time()
    
    try:
        # 1. Validation
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
            
        data = request.get_json()
        user_message = validate_chat_input(data)
        
        # 2. Language Detection & Manual Selection
        selected_language = validate_language(data.get("language"))
        try:
            detected_lang_code = detect_language(user_message)
        except Exception as e:
            logger.warning(f"Language detection failed: {e}")
            detected_lang_code = None
        
        # Use detected language if it fails manual validation or just for logging
        logger.info(f"Language detection: Manual={selected_language}, Detected={detected_lang_code}")
        
        # 3. History Processing
        history = data.get("history", [])
        if not isinstance(history, list):
            return jsonify({"error": "History must be a list"}), 400
            
        hashable_history = []
        for msg in history:
            if not isinstance(msg, dict) or "role" not in msg or "content" not in msg:
                return jsonify({"error": "Malformed history item"}), 400
            hashable_history.append(dict_to_tuple(msg))
        history_tuple = tuple(hashable_history)
        
        # 4. Generate Response
        response_text = get_ai_response(user_message, selected_language, history_tuple)
        
        # 5. Post-Response Analytics (Async/Graceful)
        duration_ms = (time.time() - start_time) * 1000
        session_id = data.get("session_id", str(uuid.uuid4()))
        
        try:
            # Save to Firestore
            save_chat_to_firestore(
                session_id=session_id,
                user_message=user_message,
                bot_response=response_text,
                language=selected_language,
                duration_ms=duration_ms
            )
        except Exception as e:
            logger.error(f"Post-response Firestore error: {e}")
            
        try:
            # Log to BigQuery
            log_to_bigquery({
                "session_id": session_id,
                "user_message": user_message,
                "language": selected_language,
                "response_length": len(response_text),
                "duration_ms": duration_ms
            })
        except Exception as e:
            logger.error(f"Post-response BigQuery error: {e}")
        
        return jsonify({
            "response": response_text
        }), 200

    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except AIServiceError as e:
        logger.error(f"AI Service Error: {e}")
        return jsonify({"error": "The AI assistant is temporarily unavailable."}), 500
    except Exception as e:
        logger.exception(f"Unexpected error in chat: {e}")
        return jsonify({"error": "An internal error occurred."}), 500
