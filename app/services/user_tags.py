"""User-tag association service functions."""

from collections.abc import Mapping

from app.models.user_tag import UserTag
from app.repositories.user_tags import find_user_tag, insert_user_tag
from app.services.validation import validate_payload, validated_int


def get_user_tag(user_id: int, tag_id: int) -> UserTag | None:
    return find_user_tag(user_id, tag_id)


def create_user_tag(data: Mapping[str, object]) -> UserTag:
    values = validate_payload(data, {
        "user_id": int,
        "tag_id": int,
    })
    return insert_user_tag(
        user_id=validated_int(values, "user_id"),
        tag_id=validated_int(values, "tag_id"),
    )
