from flask import Flask
from app.views import bp
from config import config
from core.models import init_db


def create_app() -> Flask:
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config)

    app.register_blueprint(bp)

    init_db()
    return app
