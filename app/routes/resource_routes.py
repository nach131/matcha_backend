"""Factory for resource-specific GET and create blueprints."""

from flask import Blueprint, request

from app.services.resources import create_resource, get_resource
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

    @blueprint.post("/create")
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
