"""Block service functions."""

from collections.abc import Mapping

from app.models.block import Block
from app.repositories.blocks import find_block_by_id, insert_block
from app.services.validation import validate_payload, validated_int


def get_block(block_id: int) -> Block | None:
    return find_block_by_id(block_id)


def create_block(data: Mapping[str, object]) -> Block:
    values = validate_payload(data, {
        "blocker_id": int,
        "blocked_id": int,
    })
    return insert_block(
        blocker_id=validated_int(values, "blocker_id"),
        blocked_id=validated_int(values, "blocked_id"),
    )
