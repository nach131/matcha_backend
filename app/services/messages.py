"""Message service functions."""

from collections.abc import Mapping

from app.models.message import Message
from app.repositories.messages import find_message_by_id, insert_message
from app.services.validation import (
    validate_payload,
    validated_int,
    validated_str,
)


def get_message(message_id: int) -> Message | None:
    return find_message_by_id(message_id)


def create_message(data: Mapping[str, object]) -> Message:
    values = validate_payload(data, {
        "sender_id": int,
        "receiver_id": int,
        "content": str,
    })
    return insert_message(
        sender_id=validated_int(values, "sender_id"),
        receiver_id=validated_int(values, "receiver_id"),
        content=validated_str(values, "content"),
    )
