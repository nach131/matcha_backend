from flask import Blueprint, request
from app.utils.logger import Logger

from app.services.users import (
    get_user,
    create_user
)

users_bp = Blueprint(
    "users",
    __name__,
    url_prefix="/users"
)
logger = Logger.create_logger(__name__)

@users_bp.route("/<string:user_name>", methods=["GET"])
def get_user_route(user_name):
    user = get_user(user_name)
    if user is None:
        logger.warning(f"User with name {user_name} not found.")
        return {
            "success": False,
            "message": f"User with name {user_name} not found.",
            "data": None
        }, 404
    return {
        "success": True,
        "message": f"User with name {user_name} retrieved successfully.",
        "data": user
    }, 200

@users_bp.route("", methods=["POST"])
def create_user_route():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return {
            "success": False,
            "message": "Request body must be a JSON object.",
        }, 400

    try:
        user = create_user(data)
    except ValueError as exc:
        return {
            "success": False,
            "message": str(exc),
        }, 400

    return {
        "success": True,
        "message": "User created successfully.",
        "data": user,
    }, 201