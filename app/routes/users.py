"""Flask routes for user-related operations."""

from dataclasses import asdict

from flask import Blueprint, current_app, g, make_response, request

from app.utils.logger import Logger
from app.utils.auth import require_session
from app.services.users import (
    get_user,
    search_users,
    create_user,
    get_user_by_id,
    login_user,
    logout_user,
)
from app.services.password_resets import (
    request_password_reset,
    reset_password,
    verify_password_reset_code,
)
from app.services.recommendations import get_suggested_profiles
from app.services.sessions import (
    SESSION_ABSOLUTE_TIMEOUT,
    SESSION_COOKIE_NAME,
)

logger = Logger.get_logger(__name__)
users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("/get/<string:user_name>", methods=["GET"])
def get_user_route(user_name):
    """Get a user by their username."""

    user = get_user(user_name)
    if user is None:
        logger.warning(f"User with name {user_name} not found.")
        return {
            "success": False,
            "message": f"User with name {user_name} not found.",
            "data": None
        }, 404
    user_data = asdict(user)
    user_data.pop("password_hash")
    return {
        "success": True,
        "message": f"User with name {user_name} retrieved successfully.",
        "data": user_data
    }, 200


@users_bp.route("/search/<string:user_name>", methods=["GET"])
def search_users_route(user_name):
    """Get a list of users by their username."""

    users = search_users(user_name)
    if not users:
        logger.warning(f"Users with name {user_name} not found.")
        return {
            "success": False,
            "message": f"Users with name {user_name} not found.",
            "data": None
        }, 404
    return {
        "success": True,
        "message": f"Users with name {user_name} retrieved successfully.",
        "data": users
    }, 200


@users_bp.route("/create", methods=["POST"])
def create_user_route():
    """Create a new user."""

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


@users_bp.route("/login", methods=["POST"])
def login_user_route():
    """Authenticate a user by username and password."""

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return {
            "success": False,
            "message": "Request body must be a JSON object.",
            "data": None,
        }, 400

    try:
        login = login_user(data)
    except ValueError as exc:
        return {
            "success": False,
            "message": str(exc),
            "data": None,
        }, 400

    if login is None:
        return {
            "success": False,
            "message": "Invalid username or password.",
            "data": None,
        }, 401

    user, token, expires_at = login
    user_data = asdict(user)
    user_data.pop("password_hash")
    response = make_response({
        "success": True,
        "message": "User logged in successfully.",
        "data": user_data,
    }, 200)
    response.set_cookie(
        SESSION_COOKIE_NAME,
        token,
        max_age=int(SESSION_ABSOLUTE_TIMEOUT.total_seconds()),
        expires=expires_at,
        httponly=True,
        secure=current_app.config["SESSION_COOKIE_SECURE"],
        samesite="Lax",
        path="/",
    )
    return response


@users_bp.route("/me", methods=["GET"])
@require_session
def current_user_route():
    """Return the authenticated user's profile."""

    user = get_user_by_id(g.user_id)
    if user is None:
        return {
            "success": False,
            "message": "User not found.",
            "data": None,
        }, 404

    user_data = asdict(user)
    user_data.pop("password_hash")
    return {
        "success": True,
        "message": "Current user retrieved successfully.",
        "data": user_data,
    }, 200


@users_bp.route("/logout", methods=["POST"])
def logout_user_route():
    """Revoke the current session and clear its cookie."""

    logout_user(request.cookies.get(SESSION_COOKIE_NAME))
    response = make_response({
        "success": True,
        "message": "User logged out successfully.",
        "data": None,
    }, 200)
    response.delete_cookie(
        SESSION_COOKIE_NAME,
        httponly=True,
        secure=current_app.config["SESSION_COOKIE_SECURE"],
        samesite="Lax",
        path="/",
    )
    return response


@users_bp.route("/password-reset/request", methods=["POST"])
def request_password_reset_route():
    """Create and log a reset code without disclosing whether an account exists."""

    data = request.get_json(silent=True)
    if not isinstance(data, dict) or set(data) != {"email"}:
        return {
            "success": False,
            "message": "Request body must contain only an email.",
            "data": None,
        }, 400

    email = data.get("email")
    if not isinstance(email, str) or not email.strip():
        return {
            "success": False,
            "message": "'email' must be a non-empty string.",
            "data": None,
        }, 400

    request_password_reset(email.strip())
    return {
        "success": True,
        "message": "If the account exists, a reset code was logged.",
        "data": None,
    }, 200


@users_bp.route("/password-reset/confirm", methods=["POST"])
def confirm_password_reset_route():
    """Set a new password with a valid one-time reset code."""

    data = request.get_json(silent=True)
    required_fields = {"email", "code", "new_password"}
    if not isinstance(data, dict) or set(data) != required_fields:
        return {
            "success": False,
            "message": "Request body must contain email, code, and new_password.",
            "data": None,
        }, 400

    email = data["email"]
    code = data["code"]
    new_password = data["new_password"]
    if not isinstance(email, str) or not email.strip():
        return {
            "success": False,
            "message": "'email' must be a non-empty string.",
            "data": None,
        }, 400
    if not isinstance(code, str) or not code.strip():
        return {
            "success": False,
            "message": "'code' must be a non-empty string.",
            "data": None,
        }, 400
    if not isinstance(new_password, str) or not new_password.strip():
        return {
            "success": False,
            "message": "'new_password' must be a non-empty string.",
            "data": None,
        }, 400

    if not reset_password(email.strip(), code.strip(), new_password):
        return {
            "success": False,
            "message": "Invalid or expired reset code.",
            "data": None,
        }, 400

    return {
        "success": True,
        "message": "Password reset successfully.",
        "data": None,
    }, 200


@users_bp.route("/password-reset/verify", methods=["POST"])
def verify_password_reset_code_route():
    """Check a reset code without consuming it or changing the password."""

    data = request.get_json(silent=True)
    if not isinstance(data, dict) or set(data) != {"email", "code"}:
        return {
            "success": False,
            "message": "Request body must contain email and code.",
            "data": None,
        }, 400

    email = data["email"]
    code = data["code"]
    if not isinstance(email, str) or not email.strip():
        return {
            "success": False,
            "message": "'email' must be a non-empty string.",
            "data": None,
        }, 400
    if not isinstance(code, str) or not code.strip():
        return {
            "success": False,
            "message": "'code' must be a non-empty string.",
            "data": None,
        }, 400

    if not verify_password_reset_code(email.strip(), code.strip()):
        return {
            "success": False,
            "message": "Invalid or expired reset code.",
            "data": None,
        }, 400

    return {
        "success": True,
        "message": "Reset code verified successfully.",
        "data": None,
    }, 200


@users_bp.route("/suggested", methods=["GET"])
@require_session
def suggested_profiles_route():
    """List the ten best-matching profiles for the authenticated user."""

    profiles = get_suggested_profiles(g.user_id)
    return {
        "success": True,
        "message": "Suggested profiles retrieved successfully.",
        "data": profiles,
    }, 200
