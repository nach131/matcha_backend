"""Flask routes for notifications."""

from dataclasses import asdict

from flask import Blueprint, request

from app.services.notifications import create_notification, get_notification
from app.utils.logger import Logger

notifications_bp = Blueprint(
    "notifications",
    __name__,
    url_prefix="/notifications",
)
logger = Logger.get_logger(__name__)


@notifications_bp.get("/<int:notification_id>")
def get_notification_route(notification_id: int):
    notification = get_notification(notification_id)
    if notification is None:
        return {
            "success": False,
            "message": f"Notification {notification_id} not found.",
            "data": None,
        }, 404

    return {
        "success": True,
        "message": "Notification retrieved successfully.",
        "data": asdict(notification),
    }, 200


@notifications_bp.post("/create")
def create_notification_route():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return {"success": False, "message": "Request body must be a JSON object."}, 400

    try:
        notification = create_notification(data)
    except ValueError as exc:
        return {"success": False, "message": str(exc), "data": None}, 400

    logger.info("Notification created: %s", notification.id)
    return {
        "success": True,
        "message": "Notification created successfully.",
        "data": asdict(notification),
    }, 201
