"""Flask routes for user-tag associations."""

from dataclasses import asdict

from flask import Blueprint, request

from app.services.user_tags import create_user_tag, get_user_tag
from app.utils.logger import Logger

user_tags_bp = Blueprint("user_tags", __name__, url_prefix="/user-tags")
logger = Logger.get_logger(__name__)


@user_tags_bp.get("/<int:user_id>/<int:tag_id>")
def get_user_tag_route(user_id: int, tag_id: int):
    user_tag = get_user_tag(user_id, tag_id)
    if user_tag is None:
        return {
            "success": False,
            "message": f"User-tag association ({user_id}, {tag_id}) not found.",
            "data": None,
        }, 404

    return {
        "success": True,
        "message": "User-tag association retrieved successfully.",
        "data": asdict(user_tag),
    }, 200


@user_tags_bp.post("/create")
def create_user_tag_route():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return {"success": False, "message": "Request body must be a JSON object."}, 400

    try:
        user_tag = create_user_tag(data)
    except ValueError as exc:
        return {"success": False, "message": str(exc), "data": None}, 400

    logger.info(
        "User-tag association created: (%s, %s)",
        user_tag.user_id,
        user_tag.tag_id,
    )
    return {
        "success": True,
        "message": "User-tag association created successfully.",
        "data": asdict(user_tag),
    }, 201
