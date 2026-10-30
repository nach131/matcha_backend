"""Flask routes for tags."""

from dataclasses import asdict

from flask import Blueprint, request

from app.services.tags import create_tag, get_tag
from app.utils.logger import Logger

tags_bp = Blueprint("tags", __name__, url_prefix="/tags")
logger = Logger.get_logger(__name__)


@tags_bp.get("/<int:tag_id>")
def get_tag_route(tag_id: int):
    tag = get_tag(tag_id)
    if tag is None:
        return {
            "success": False,
            "message": f"Tag {tag_id} not found.",
            "data": None,
        }, 404

    return {
        "success": True,
        "message": "Tag retrieved successfully.",
        "data": asdict(tag),
    }, 200


@tags_bp.post("/create")
def create_tag_route():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return {"success": False, "message": "Request body must be a JSON object."}, 400

    try:
        tag = create_tag(data)
    except ValueError as exc:
        return {"success": False, "message": str(exc), "data": None}, 400

    logger.info("Tag created: %s", tag.id)
    return {
        "success": True,
        "message": "Tag created successfully.",
        "data": asdict(tag),
    }, 201
