"""Profile visit service functions."""

from collections.abc import Mapping

from app.models.profile_visit import ProfileVisit
from app.repositories.profile_visits import (
    find_profile_visit_by_id,
    insert_profile_visit,
)
from app.services.validation import validate_payload, validated_int


def get_profile_visit(profile_visit_id: int) -> ProfileVisit | None:
    return find_profile_visit_by_id(profile_visit_id)


def create_profile_visit(data: Mapping[str, object]) -> ProfileVisit:
    values = validate_payload(data, {
        "visitor_id": int,
        "visited_id": int,
    })
    return insert_profile_visit(
        visitor_id=validated_int(values, "visitor_id"),
        visited_id=validated_int(values, "visited_id"),
    )
