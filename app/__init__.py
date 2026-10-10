from flask import Flask
from app.routes.general import register_routes
from app.routes.users import users_bp

def create_app():
    app = Flask(__name__)
    register_routes(app)
    app.register_blueprint(users_bp)
    return app
