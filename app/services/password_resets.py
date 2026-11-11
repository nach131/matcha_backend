"""Password reset code creation and validation."""

import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from werkzeug.security import generate_password_hash

from app.repositories.password_resets import (
    consume_password_reset_code,
    find_user_id_by_email,
    is_password_reset_code_valid,
    store_password_reset_code,
)
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)
PASSWORD_RESET_CODE_TTL = timedelta(minutes=15)


def _hash_code(code: str) -> str:
    return hashlib.sha256(code.encode("utf-8")).hexdigest()


def request_password_reset(email: str) -> None:
    user_id = find_user_id_by_email(email)
    if user_id is None:
        return

    code = secrets.token_urlsafe(24)
    expires_at = datetime.now(timezone.utc) + PASSWORD_RESET_CODE_TTL
    store_password_reset_code(user_id, _hash_code(code), expires_at)
    logger.warning(
        "Password reset code for user id %s: %s",
        user_id,
        code,
    )


def verify_password_reset_code(email: str, code: str) -> bool:
    return is_password_reset_code_valid(email, _hash_code(code))


def reset_password(
    email: str,
    code: str,
    new_password: str,
) -> bool:
    password_hash = generate_password_hash(new_password)
    return consume_password_reset_code(
        email,
        _hash_code(code),
        password_hash,
    )
