from flask import Blueprint, Flask

# TODO: Delete this line after testing
from app.routes.general import general_bp
from app.routes.users import users_bp

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")

# TODO: Delete this line after testing
api_bp.register_blueprint(general_bp)
api_bp.register_blueprint(users_bp)


def register_blueprints(app: Flask) -> None:
    """
    Register all blueprints with the Flask application.
    
    Args:
        app: The Flask application instance.
    """

    app.register_blueprint(api_bp)