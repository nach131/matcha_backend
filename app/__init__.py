from flask import Flask
from app.utils.logger import Logger
from app.routes.general import register_routes
from app.routes.users import users_bp

# Create the general logger instance
logger = Logger.create_logger()

def create_app():
    # Create the Flask application
    app = Flask(__name__)
    logger.info("Flask application created.")

    # TODO: Delete this line after testing
    # Register general routes
    register_routes(app)

    # Register the users blueprint
    app.register_blueprint(users_bp)

    return app
