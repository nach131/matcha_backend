"""Factory for resource-specific GET and create blueprints."""

from flask import Blueprint, request

from app.services.resources import (
    create_resource,
    get_resource,
    get_resources_by_user,
)
from app.utils.auth import require_session
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)


def create_resource_blueprint(
    resource_name: str,
    url_prefix: str,
    primary_key_fields: tuple[str, ...],
) -> Blueprint:
    blueprint = Blueprint(
        resource_name,
        __name__,
        url_prefix=url_prefix,
    )
    key_path = "/".join(
        f"<int:{field}>" for field in primary_key_fields
    )

    @blueprint.get(f"/{key_path}")
    @require_session
    def get_resource_route(**route_values: int):
        record = get_resource(
            resource_name,
            tuple(route_values[field] for field in primary_key_fields),
        )
        if record is None:
            return {
                "success": False,
                "message": f"{resource_name.rstrip('s')} not found.",
                "data": None,
            }, 404

        return {
            "success": True,
            "message": f"{resource_name.rstrip('s')} retrieved successfully.",
            "data": record,
        }, 200

    @blueprint.get("/by-user/<int:user_id>")
    @require_session
    def get_user_resources_route(user_id: int):
        try:
            records = get_resources_by_user(resource_name, user_id)
        except ValueError as exc:
            return {
                "success": False,
                "message": str(exc),
                "data": None,
            }, 400

        return {
            "success": True,
            "message": f"{resource_name} retrieved successfully.",
            "data": records,
        }, 200

    @blueprint.post("/create")
    @require_session
    def create_resource_route():
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return {
                "success": False,
                "message": "Request body must be a JSON object.",
            }, 400

        try:
            record = create_resource(resource_name, data)
        except ValueError as exc:
            return {
                "success": False,
                "message": str(exc),
                "data": None,
            }, 400

        logger.info("Created %s resource", resource_name)
        return {
            "success": True,
            "message": f"{resource_name.rstrip('s')} created successfully.",
            "data": record,
        }, 201

    return blueprint
