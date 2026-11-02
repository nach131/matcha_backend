"""Flask routes for likes."""

from dataclasses import asdict

from flask import Blueprint, request

from app.services.likes import create_like, get_like
from app.utils.logger import Logger

likes_bp = Blueprint("likes", __name__, url_prefix="/likes")
logger = Logger.get_logger(__name__)


@likes_bp.get("/<int:like_id>")
def get_like_route(like_id: int):
    like = get_like(like_id)
    if like is None:
        return {
            "success": False,
            "message": f"Like {like_id} not found.",
            "data": None,
        }, 404

    return {
        "success": True,
        "message": "Like retrieved successfully.",
        "data": asdict(like),
    }, 200


@likes_bp.post("/create")
def create_like_route():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return {"success": False, "message": "Request body must be a JSON object."}, 400

    try:
        like = create_like(data)
    except ValueError as exc:
        return {"success": False, "message": str(exc), "data": None}, 400

    logger.info("Like created: %s", like.id)
    return {
        "success": True,
        "message": "Like created successfully.",
        "data": asdict(like),
    }, 201
