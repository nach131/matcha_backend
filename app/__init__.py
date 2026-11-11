"""Flask main application factory and initialization."""

import os

from flask import Flask

from app.utils.logger import Logger
from app.routes.registration import register_blueprints
from app.utils.error_handler import register_error_handlers

def create_app():
    logger = Logger.create_logger()

    app = Flask(__name__)
    secure_cookie = os.environ.get(
        "SESSION_COOKIE_SECURE", "true"
    ).strip().lower()
    if secure_cookie not in {"true", "false"}:
        raise ValueError("SESSION_COOKIE_SECURE must be 'true' or 'false'.")
    app.config["SESSION_COOKIE_SECURE"] = secure_cookie == "true"
    logger.info("Flask application created.")

    register_blueprints(app)
    register_error_handlers(app)

    return app
