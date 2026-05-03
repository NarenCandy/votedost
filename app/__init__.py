"""VoteDost Flask Application Factory."""
import os
import time
import uuid
import logging
from flask import Flask, g, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.config import config
from app.services.logging_service import setup_cloud_services

logger = logging.getLogger(__name__)

# Global limiter instance
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="memory://",
    default_limits=[]
)

def create_app() -> Flask:
    """Creates and configures the Flask application."""
    app = Flask(__name__, 
                template_folder='../templates', 
                static_folder='../static')
    
    # 1. Initialize Cloud Services
    setup_cloud_services()
    
    # 2. Rate Limiting
    is_testing = os.getenv('VOTEDOST_TESTING') == 'true' or app.testing
    if is_testing:
        app.config['RATELIMIT_ENABLED'] = False
        app.testing = True
        
        # Initialize a mock model for tests if not already set
        from unittest.mock import MagicMock
        from app.services import ai_service
        if ai_service.model is None:
            ai_service.model = MagicMock()
        
    limiter.init_app(app)
    # Only set default limits for non-testing mode
    if not is_testing:
        limiter._default_limits = ["200 per day", "50 per hour"]
    
    # 3. Register Blueprints
    from app.routes.chat import chat_bp
    app.register_blueprint(chat_bp)
    
    # Apply specific limit to chat route
    # Note: We do this after registration or inside the blueprint
    
    # 4. Middleware & Security Headers
    @app.before_request
    def start_timer():
        g.start_time = time.time()
        g.request_id = str(uuid.uuid4())

    @app.after_request
    def after_request_logic(response):
        # Security Headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src https://fonts.gstatic.com; "
            "connect-src 'self'; "
            "img-src 'self' data:;"
        )
        
        # Performance Logging
        if request.path != '/health':
            start_time = g.get('start_time', time.time())
            request_id = g.get('request_id', 'unknown')
            duration = (time.time() - start_time) * 1000
            logger.info(
                f"Request Processed | ID: {request_id} | Path: {request.path} | "
                f"Status: {response.status_code} | Duration: {duration:.2f}ms"
            )
        return response

    return app

from app.config import config
from app.services.ai_service import get_ai_response, model
from app.services.firestore_service import save_chat_to_firestore
from app.services.bigquery_service import log_to_bigquery
from app.services.translation_service import detect_language

# Re-export for backward compatibility with tests
SUPPORTED_LANGUAGES = config.SUPPORTED_LANGUAGES

# For simple imports
app = create_app()
