"""Like service functions."""

from collections.abc import Mapping

from app.models.like import Like
from app.repositories.likes import find_like_by_id, insert_like
from app.services.validation import validate_payload, validated_int


def get_like(like_id: int) -> Like | None:
    return find_like_by_id(like_id)


def create_like(data: Mapping[str, object]) -> Like:
    values = validate_payload(data, {
        "from_user_id": int,
        "to_user_id": int,
    })
    return insert_like(
        from_user_id=validated_int(values, "from_user_id"),
        to_user_id=validated_int(values, "to_user_id"),
    )
