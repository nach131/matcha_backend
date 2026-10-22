from flask import Flask

from app.utils.logger import Logger
from app.utils.error_handler import register_error_handlers

from app.routes.users import users_bp
from app.routes.general import register_routes

logger = Logger.create_logger()

def create_app():
    app = Flask(__name__)
    logger.info("Flask application created.")

    # TODO: Delete this line after testing
    register_routes(app)

    app.register_blueprint(users_bp)
    register_error_handlers(app)

    return app
