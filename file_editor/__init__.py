"""
file_editor.__init__

Application factory for the file editor web app.
"""

from flask import Flask

from .routes import editor_bp


def create_app() -> Flask:
    """Create and configure the Flask application.

    Returns:
        Flask: Configured Flask application.
    """
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.secret_key = "change-me"
    app.register_blueprint(editor_bp)
    return app
