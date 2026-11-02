"""Flask routes for blocks."""

from dataclasses import asdict

from flask import Blueprint, request

from app.services.blocks import create_block, get_block
from app.utils.logger import Logger

blocks_bp = Blueprint("blocks", __name__, url_prefix="/blocks")
logger = Logger.get_logger(__name__)


@blocks_bp.get("/<int:block_id>")
def get_block_route(block_id: int):
    block = get_block(block_id)
    if block is None:
        return {
            "success": False,
            "message": f"Block {block_id} not found.",
            "data": None,
        }, 404

    return {
        "success": True,
        "message": "Block retrieved successfully.",
        "data": asdict(block),
    }, 200


@blocks_bp.post("/create")
def create_block_route():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return {"success": False, "message": "Request body must be a JSON object."}, 400

    try:
        block = create_block(data)
    except ValueError as exc:
        return {"success": False, "message": str(exc), "data": None}, 400

    logger.info("Block created: %s", block.id)
    return {
        "success": True,
        "message": "Block created successfully.",
        "data": asdict(block),
    }, 201
