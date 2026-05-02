import os
import logging
from flask import Flask, render_template, request, jsonify
import vertexai
from vertexai.generative_models import GenerativeModel, Content, Part

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Vertex AI
project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
location = "us-central1" # Default location

try:
    if project_id:
        vertexai.init(project=project_id, location=location)
        logger.info(f"Initialized Vertex AI with project ID: {project_id}")
    else:
        logger.warning("GOOGLE_CLOUD_PROJECT environment variable not set. Vertex AI may not work correctly.")
        vertexai.init(location=location)

    system_instruction = (
        "You are VoteDost, a friendly and knowledgeable Indian election assistant. "
        "Help users understand the Indian election process, ECI, voting steps, voter ID, timelines, EVMs, "
        "candidate eligibility, and related topics. Be conversational, simple, and easy to understand. "
        "Detect the language the user is typing in and respond in that same language. "
        "Default to English if unsure. Support Hindi, Tamil, Telugu, Kannada, Bengali, Marathi, and English at minimum. "
        "Use simple words to feel friendly."
    )

    model = GenerativeModel(
        "gemini-2.5-flash",
        system_instruction=[system_instruction]
    )
except Exception as e:
    logger.error(f"Failed to initialize Vertex AI Model: {e}")
    model = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    if not model:
        return jsonify({"error": "AI Model not initialized properly. Check server configuration."}), 500

    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Message is required"}), 400
    
    user_message = data["message"]
    history = data.get("history", []) # List of dicts: {"role": "user"|"assistant", "content": "..."}

    try:
        formatted_history = []
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            formatted_history.append(Content(role=role, parts=[Part.from_text(msg["content"])]))
            
        chat_session = model.start_chat(history=formatted_history)
        response = chat_session.send_message(user_message)
        
        return jsonify({
            "response": response.text
        })

    except Exception as e:
        logger.error(f"Error during chat generation: {e}")
        return jsonify({"error": "An error occurred while generating the response. Please try again."}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
