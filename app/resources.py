"""Database resource definitions shared by generic resource services."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ResourceSpec:
    table: str
    primary_key: tuple[str, ...]
    fields: dict[str, type]
    defaults: dict[str, object]


RESOURCE_SPECS = {
    "messages": ResourceSpec(
        table="messages",
        primary_key=("id",),
        fields={
            "sender_id": int,
            "receiver_id": int,
            "content": str,
        },
        defaults={"read": False},
    ),
    "reports": ResourceSpec(
        table="reports",
        primary_key=("id",),
        fields={
            "reporter_id": int,
            "reported_id": int,
            "reason": str,
        },
        defaults={},
    ),
    "blocks": ResourceSpec(
        table="blocks",
        primary_key=("id",),
        fields={
            "blocker_id": int,
            "blocked_id": int,
        },
        defaults={},
    ),
    "likes": ResourceSpec(
        table="likes",
        primary_key=("id",),
        fields={
            "from_user_id": int,
            "to_user_id": int,
        },
        defaults={},
    ),
    "notifications": ResourceSpec(
        table="notifications",
        primary_key=("id",),
        fields={
            "user_id": int,
            "type": int,
            "related_user_id": int,
        },
        defaults={"read": False},
    ),
    "photos": ResourceSpec(
        table="photos",
        primary_key=("id",),
        fields={
            "user_id": int,
            "path": str,
            "is_profile": bool,
        },
        defaults={},
    ),
    "tags": ResourceSpec(
        table="tags",
        primary_key=("id",),
        fields={"name": str},
        defaults={},
    ),
    "profile_visits": ResourceSpec(
        table="profile_visits",
        primary_key=("id",),
        fields={
            "visitor_id": int,
            "visited_id": int,
        },
        defaults={},
    ),
    "user_tags": ResourceSpec(
        table="user_tags",
        primary_key=("user_id", "tag_id"),
        fields={
            "user_id": int,
            "tag_id": int,
        },
        defaults={},
    ),
}
