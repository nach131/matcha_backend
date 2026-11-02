"""Flask routes for photos."""

from dataclasses import asdict

from flask import Blueprint, request

from app.services.photos import create_photo, get_photo
from app.utils.logger import Logger

photos_bp = Blueprint("photos", __name__, url_prefix="/photos")
logger = Logger.get_logger(__name__)


@photos_bp.get("/<int:photo_id>")
def get_photo_route(photo_id: int):
    photo = get_photo(photo_id)
    if photo is None:
        return {
            "success": False,
            "message": f"Photo {photo_id} not found.",
            "data": None,
        }, 404

    return {
        "success": True,
        "message": "Photo retrieved successfully.",
        "data": asdict(photo),
    }, 200


@photos_bp.post("/create")
def create_photo_route():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return {"success": False, "message": "Request body must be a JSON object."}, 400

    try:
        photo = create_photo(data)
    except ValueError as exc:
        return {"success": False, "message": str(exc), "data": None}, 400

    logger.info("Photo created: %s", photo.id)
    return {
        "success": True,
        "message": "Photo created successfully.",
        "data": asdict(photo),
    }, 201
