"""Flask main application factory and initialization."""

from flask import Flask

from app.utils.logger import Logger
from app.routes.registration import register_blueprints
from app.utils.error_handler import register_error_handlers

def create_app():
    logger = Logger.create_logger()

    app = Flask(__name__)
    logger.info("Flask application created.")

    register_blueprints(app)
    register_error_handlers(app)

    return app
