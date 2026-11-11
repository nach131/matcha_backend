"""Session token creation, validation, and revocation."""

import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from app.repositories.sessions import (
    delete_session,
    insert_session,
    touch_active_session,
)

SESSION_COOKIE_NAME = "session_token"
SESSION_ABSOLUTE_TIMEOUT = timedelta(days=7)
SESSION_IDLE_TIMEOUT = timedelta(minutes=30)


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def create_session(user_id: int) -> tuple[str, datetime]:
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + SESSION_ABSOLUTE_TIMEOUT
    insert_session(
        user_id,
        _hash_token(token),
        expires_at,
        int(SESSION_IDLE_TIMEOUT.total_seconds()),
    )
    return token, expires_at


def get_session_user_id(token: str | None) -> int | None:
    if not token:
        return None

    return touch_active_session(
        _hash_token(token),
        int(SESSION_IDLE_TIMEOUT.total_seconds()),
    )


def revoke_session(token: str | None) -> None:
    if token:
        delete_session(_hash_token(token))
