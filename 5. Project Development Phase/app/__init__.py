import os
from datetime import timedelta
from flask import Flask
from app.utils import init_db

def create_app():
    """Flask Application Factory."""
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    
    # Configuration
    # Safe development secret key fallback
    app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "hdi-predictor-secret-key-college-major-project-2026")
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)
    
    # Initialize Database
    with app.app_context():
        init_db()
        
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)
    
    return app
