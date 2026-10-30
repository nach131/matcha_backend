"""Flask routes for messages."""

from dataclasses import asdict

from flask import Blueprint, request

from app.services.messages import create_message, get_message
from app.utils.logger import Logger

messages_bp = Blueprint("messages", __name__, url_prefix="/messages")
logger = Logger.get_logger(__name__)


@messages_bp.get("/<int:message_id>")
def get_message_route(message_id: int):
    message = get_message(message_id)
    if message is None:
        return {
            "success": False,
            "message": f"Message {message_id} not found.",
            "data": None,
        }, 404

    return {
        "success": True,
        "message": "Message retrieved successfully.",
        "data": asdict(message),
    }, 200


@messages_bp.post("/create")
def create_message_route():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return {"success": False, "message": "Request body must be a JSON object."}, 400

    try:
        message = create_message(data)
    except ValueError as exc:
        return {"success": False, "message": str(exc), "data": None}, 400

    logger.info("Message created: %s", message.id)
    return {
        "success": True,
        "message": "Message created successfully.",
        "data": asdict(message),
    }, 201
