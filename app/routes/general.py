# TODO: Delete this file after testing
from app.utils.logger import Logger

logger = Logger.create_logger(__name__)

def register_routes(app):
    @app.route("/")
    def index():
        return {
            "message": "hello"
        }

    @app.route("/health")
    def health():
        return {
            "success": True,
            "message": "Llegaste aqui Mother F**ck"
        }