"""Photo service functions."""

from collections.abc import Mapping

from app.models.photo import Photo
from app.repositories.photos import find_photo_by_id, insert_photo
from app.services.validation import (
    validate_payload,
    validated_bool,
    validated_int,
    validated_str,
)


def get_photo(photo_id: int) -> Photo | None:
    return find_photo_by_id(photo_id)


def create_photo(data: Mapping[str, object]) -> Photo:
    values = validate_payload(data, {
        "user_id": int,
        "path": str,
        "is_profile": bool,
    })
    return insert_photo(
        user_id=validated_int(values, "user_id"),
        path=validated_str(values, "path"),
        is_profile=validated_bool(values, "is_profile"),
    )
