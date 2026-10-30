# TODO: Delete this file after testing
from flask import Blueprint
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)
general_bp = Blueprint("general", __name__)

@general_bp.route("/")
def index():
    return {
        "message": "hello"
    }

@general_bp.route("/health")
def health():
    return {
        "success": True,
        "message": "Llegaste aqui Mother F**ck"
    }