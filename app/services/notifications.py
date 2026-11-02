"""Notification service functions."""

from collections.abc import Mapping

from app.models.notification import Notification
from app.repositories.notifications import (
    find_notification_by_id,
    insert_notification,
)
from app.services.validation import validate_payload, validated_int


def get_notification(notification_id: int) -> Notification | None:
    return find_notification_by_id(notification_id)


def create_notification(data: Mapping[str, object]) -> Notification:
    values = validate_payload(data, {
        "user_id": int,
        "type": int,
        "related_user_id": int,
    })
    return insert_notification(
        user_id=validated_int(values, "user_id"),
        notification_type=validated_int(values, "type"),
        related_user_id=validated_int(values, "related_user_id"),
    )
