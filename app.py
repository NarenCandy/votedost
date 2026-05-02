"""
VoteDost: Indian Election Assistant
-----------------------------------
A Flask-based web application providing real-time assistance and information about 
Indian elections using Google's Gemini Pro AI model. This application includes
integrations with Google Cloud Logging and Monitoring for enterprise-grade 
observability and performance tracking.

Author: Antigravity AI
Version: 1.0.0
"""

import os
import logging
import time
import uuid
import functools
from typing import Dict, List, Tuple, Any, Optional, Union
from flask import Flask, render_template, request, jsonify, g
import vertexai
from vertexai.generative_models import GenerativeModel, Content, Part
from google.cloud import logging as cloud_logging
from google.cloud import monitoring_v3

# --- Constants ---
SUPPORTED_LANGUAGES = ["English", "Hindi", "Tamil", "Telugu", "Kannada", "Bengali", "Marathi"]
DEFAULT_LOCATION = "us-central1"
MAX_MESSAGE_LENGTH = 2000

# --- App Initialization ---
app = Flask(__name__)

# --- Google Cloud Services Setup ---
project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

def setup_cloud_services():
    """Initializes Google Cloud Logging and Monitoring if project ID is available."""
    if project_id:
        try:
            # Setup Cloud Logging
            client = cloud_logging.Client(project=project_id)
            client.setup_logging()
            logging.info(f"Cloud Logging initialized for project: {project_id}")
            
            # Monitoring client can be used for custom metrics if needed
            # monitoring_client = monitoring_v3.MetricServiceClient()
        except Exception as e:
            print(f"Failed to initialize Cloud services: {e}")

setup_cloud_services()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# --- Vertex AI Initialization ---
try:
    if project_id:
        vertexai.init(project=project_id, location=DEFAULT_LOCATION)
        logger.info(f"Initialized Vertex AI with project: {project_id}")
    else:
        logger.warning("GOOGLE_CLOUD_PROJECT not set. Vertex AI might fail in non-ADC environments.")
        vertexai.init(location=DEFAULT_LOCATION)

    system_instruction = (
        "You are VoteDost, a friendly and knowledgeable Indian election assistant. "
        "Help users understand the Indian election process, ECI, voting steps, voter ID, timelines, EVMs, "
        "candidate eligibility, and related topics. Be conversational, simple, and easy to understand. "
        "Detect the language the user is typing in and respond in that same language. "
        "Default to English if unsure. Support Hindi, Tamil, Telugu, Kannada, Bengali, Marathi, and English at minimum. "
        "Use simple words to feel friendly."
    )

    # Note: Using gemini-2.0-flash as it is high-performing and efficient
    model = GenerativeModel(
        "gemini-2.5-flash",
        system_instruction=[system_instruction]
    )
except Exception as e:
    logger.error(f"Failed to initialize Vertex AI Model: {e}")
    model = None

# --- Middleware / Request Tracking ---
@app.before_request
def start_timer():
    """Generates a request ID and starts a timer for performance tracking."""
    g.start_time = time.time()
    g.request_id = str(uuid.uuid4())

@app.after_request
def log_request(response):
    """Logs the request details and performance metrics to Cloud Logging."""
    if request.path == '/health':
        return response
        
    duration = (time.time() - g.start_time) * 1000
    logger.info(
        f"Request Processed | ID: {g.request_id} | Path: {request.path} | "
        f"Method: {request.method} | Status: {response.status_code} | Duration: {duration:.2f}ms"
    )
    return response

# --- Helper Functions & Caching ---
def dict_to_tuple(d: Dict) -> Tuple:
    """Converts a dictionary to a sorted tuple of items to make it hashable."""
    return tuple(sorted(d.items()))

@functools.lru_cache(maxsize=128)
def get_ai_response(message: str, language: str, history_tuple: Tuple[Tuple[Tuple, ...], ...]) -> str:
    """
    Calls Vertex AI to get a response. Cached based on message, language, and history.
    The history_tuple must be hashable (tuple of tuples of tuples).
    """
    if not model:
        raise RuntimeError("AI Model not initialized")

    # Reconstruct history for Vertex AI
    formatted_history = []
    for msg_tuple in history_tuple:
        msg_dict = dict(msg_tuple)
        role = "user" if msg_dict["role"] == "user" else "model"
        formatted_history.append(Content(role=role, parts=[Part.from_text(msg_dict["content"])]))

    chat_session = model.start_chat(history=formatted_history)
    
    # Prepend language instruction
    enhanced_message = f"[{language} language requested] {message}"
    response = chat_session.send_message(enhanced_message)
    
    return response.text

# --- Routes ---
@app.route("/")
def index() -> str:
    """Renders the main application page."""
    return render_template("index.html")

@app.route("/health")
def health() -> Tuple[Any, int]:
    """Health check endpoint for deployment monitoring."""
    return jsonify({
        "status": "ok",
        "model_loaded": model is not None,
        "project_id": project_id or "not_set",
        "version": "1.0.0",
        "timestamp": time.time()
    }), 200

@app.route("/chat", methods=["POST"])
def chat() -> Tuple[Any, int]:
    """
    Main chat endpoint. Validates input, checks cache, and returns AI response.
    """
    if not model:
        return jsonify({"error": "AI Model not initialized properly. Check server configuration."}), 500

    # 1. Basic Content-Type Validation
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    if not data:
        return jsonify({"error": "Empty request body"}), 400

    # 2. Input Validation
    user_message = data.get("message")
    if user_message is None:
        return jsonify({"error": "Message is required"}), 400
    
    # Convert to string and strip whitespace
    user_message = str(user_message).strip()
    
    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400
    
    if len(user_message) > MAX_MESSAGE_LENGTH:
        return jsonify({"error": f"Message exceeds limit of {MAX_MESSAGE_LENGTH} characters"}), 400

    # 3. Language & History Validation
    language = data.get("language", "English")
    if language not in SUPPORTED_LANGUAGES:
        logger.warning(f"Unsupported language '{language}' requested. Defaulting to English.")
        language = "English"

    history = data.get("history", [])
    if not isinstance(history, list):
        return jsonify({"error": "History must be a list"}), 400
    
    # Validate history structure and convert for caching
    try:
        hashable_history = []
        for msg in history:
            if not isinstance(msg, dict) or "role" not in msg or "content" not in msg:
                return jsonify({"error": "Malformed history item"}), 400
            hashable_history.append(dict_to_tuple(msg))
        history_tuple = tuple(hashable_history)
    except Exception as e:
        logger.error(f"History processing error: {e}")
        return jsonify({"error": "Invalid history format"}), 400

    # 4. Generate Response (Cached)
    try:
        start_ai_time = time.time()
        response_text = get_ai_response(user_message, language, history_tuple)
        ai_duration = (time.time() - start_ai_time) * 1000
        
        logger.info(f"AI Generation successful | Duration: {ai_duration:.2f}ms | Lang: {language}")
        
        return jsonify({
            "response": response_text
        }), 200

    except Exception as e:
        logger.error(f"Error during chat generation: {e}")
        return jsonify({"error": "An error occurred while generating the response. Please try again."}), 500

# --- Error Handlers ---
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

# --- Entry Point ---
if __name__ == "__main__":
    # Use environment-defined PORT or default to 8080 (Cloud Run standard)
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=False, host="0.0.0.0", port=port)
