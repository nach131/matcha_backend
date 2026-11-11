"""Profile suggestion orchestration."""

from app.repositories.recommendations import find_suggested_profiles


def get_suggested_profiles(user_id: int) -> list[dict[str, object]]:
    """Return up to ten profiles ordered by shared tags, distance, then fame."""

    return find_suggested_profiles(user_id)
