"""
VoteDost: Indian Election Assistant - Entry Point
------------------------------------------------
This file acts as the main entry point for the application. It maintains 
backward compatibility with existing tests and deployment configurations 
by re-exporting the Flask app and necessary constants.

Author: Antigravity AI
Version: 1.1.0 (Modular)
"""

import os
from app import app
from app.config import config

# Re-export for backward compatibility with tests
SUPPORTED_LANGUAGES = config.SUPPORTED_LANGUAGES

if __name__ == "__main__":
    # Use environment-defined PORT or default to 8080 (Cloud Run standard)
    port = int(os.environ.get("PORT", 8080))
    # We set debug=False for production readiness
    app.run(debug=False, host="0.0.0.0", port=port)
