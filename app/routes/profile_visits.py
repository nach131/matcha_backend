"""Flask routes for profile visits."""

from dataclasses import asdict

from flask import Blueprint, request

from app.services.profile_visits import (
    create_profile_visit,
    get_profile_visit,
)
from app.utils.logger import Logger

profile_visits_bp = Blueprint(
    "profile_visits",
    __name__,
    url_prefix="/profile-visits",
)
logger = Logger.get_logger(__name__)


@profile_visits_bp.get("/<int:profile_visit_id>")
def get_profile_visit_route(profile_visit_id: int):
    profile_visit = get_profile_visit(profile_visit_id)
    if profile_visit is None:
        return {
            "success": False,
            "message": f"Profile visit {profile_visit_id} not found.",
            "data": None,
        }, 404

    return {
        "success": True,
        "message": "Profile visit retrieved successfully.",
        "data": asdict(profile_visit),
    }, 200


@profile_visits_bp.post("/create")
def create_profile_visit_route():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return {"success": False, "message": "Request body must be a JSON object."}, 400

    try:
        profile_visit = create_profile_visit(data)
    except ValueError as exc:
        return {"success": False, "message": str(exc), "data": None}, 400

    logger.info("Profile visit created: %s", profile_visit.id)
    return {
        "success": True,
        "message": "Profile visit created successfully.",
        "data": asdict(profile_visit),
    }, 201
