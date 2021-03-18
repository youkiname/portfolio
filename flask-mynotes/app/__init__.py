from flask import Flask, redirect, flash
from app.views import bp
from config import config
from core.models import init_db
from flask_login import LoginManager
from app.services.auth import load_user_from_session


def create_app() -> Flask:
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config)

    app.register_blueprint(bp)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return load_user_from_session(user_id)

    @login_manager.unauthorized_handler
    def unauthorized():
        flash("You must be logged in!")
        return redirect('/authorization')

    init_db()
    return app
