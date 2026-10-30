"""Tag service functions."""

from collections.abc import Mapping

from app.models.tag import Tag
from app.repositories.tags import find_tag_by_id, insert_tag
from app.services.validation import validate_payload, validated_str


def get_tag(tag_id: int) -> Tag | None:
    return find_tag_by_id(tag_id)


def create_tag(data: Mapping[str, object]) -> Tag:
    values = validate_payload(data, {"name": str})
    return insert_tag(name=validated_str(values, "name"))
