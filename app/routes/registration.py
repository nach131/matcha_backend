from flask import Blueprint, Flask

# TODO: Delete this line after testing
from app.routes.general import general_bp
from app.routes.blocks import blocks_bp
from app.routes.likes import likes_bp
from app.routes.messages import messages_bp
from app.routes.notifications import notifications_bp
from app.routes.photos import photos_bp
from app.routes.profile_visits import profile_visits_bp
from app.routes.reports import reports_bp
from app.routes.tags import tags_bp
from app.routes.user_tags import user_tags_bp
from app.routes.users import users_bp

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")

# TODO: Delete this line after testing
api_bp.register_blueprint(general_bp)

api_bp.register_blueprint(users_bp)
api_bp.register_blueprint(messages_bp)
api_bp.register_blueprint(reports_bp)
api_bp.register_blueprint(blocks_bp)
api_bp.register_blueprint(likes_bp)
api_bp.register_blueprint(notifications_bp)
api_bp.register_blueprint(photos_bp)
api_bp.register_blueprint(tags_bp)
api_bp.register_blueprint(profile_visits_bp)
api_bp.register_blueprint(user_tags_bp)


def register_blueprints(app: Flask) -> None:
    """
    Register all blueprints with the Flask application.
    
    Args:
        app: The Flask application instance.
    """

    app.register_blueprint(api_bp)