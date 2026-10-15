from flask import Flask
from app.routes.general import register_routes
from app.routes.users import users_bp

def create_app():
    # Create the Flask application
    app = Flask(__name__)

    # TODO: Delete this line after testing
    # Register general routes
    register_routes(app)

    # Register the users blueprint
    app.register_blueprint(users_bp)

    return app
