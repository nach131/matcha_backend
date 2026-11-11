"""Database resource definitions shared by generic resource services."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ResourceSpec:
    table: str
    primary_key: tuple[str, ...]
    fields: dict[str, type]
    defaults: dict[str, object]
    user_filter_fields: tuple[str, ...] = ()
    user_link: tuple[str, str, str] | None = None


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
        user_filter_fields=("sender_id", "receiver_id"),
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
        user_filter_fields=("reporter_id", "reported_id"),
    ),
    "blocks": ResourceSpec(
        table="blocks",
        primary_key=("id",),
        fields={
            "blocker_id": int,
            "blocked_id": int,
        },
        defaults={},
        user_filter_fields=("blocker_id", "blocked_id"),
    ),
    "likes": ResourceSpec(
        table="likes",
        primary_key=("id",),
        fields={
            "from_user_id": int,
            "to_user_id": int,
        },
        defaults={},
        user_filter_fields=("from_user_id", "to_user_id"),
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
        user_filter_fields=("user_id", "related_user_id"),
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
        user_filter_fields=("user_id",),
    ),
    "tags": ResourceSpec(
        table="tags",
        primary_key=("id",),
        fields={"name": str},
        defaults={},
        user_link=("user_tags", "tag_id", "user_id"),
    ),
    "profile_visits": ResourceSpec(
        table="profile_visits",
        primary_key=("id",),
        fields={
            "visitor_id": int,
            "visited_id": int,
        },
        defaults={},
        user_filter_fields=("visitor_id", "visited_id"),
    ),
    "user_tags": ResourceSpec(
        table="user_tags",
        primary_key=("user_id", "tag_id"),
        fields={
            "user_id": int,
            "tag_id": int,
        },
        defaults={},
        user_filter_fields=("user_id",),
    ),
}
