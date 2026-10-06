from flask import Blueprint, request

from app.services.users import (
    get_user,
    create_user
)

users_bp = Blueprint(
    "users",
    __name__,
    url_prefix="/users"
)

@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user_route(user_id):
    # Logic to retrieve user by ID
    return {
        "success": True,
        "message": f"User with ID {user_id} retrieved successfully."
    }