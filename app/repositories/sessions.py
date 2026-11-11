"""Database operations for server-side user sessions."""

from datetime import datetime

from app.database.connection import get_connection


def insert_session(
    user_id: int,
    token_hash: str,
    expires_at: datetime,
    idle_timeout_seconds: int,
) -> None:
    cleanup_query = """
        DELETE FROM sessions
        WHERE expires_at <= CURRENT_TIMESTAMP
           OR last_activity <= CURRENT_TIMESTAMP
              - (%s * INTERVAL '1 second')
    """
    insert_query = """
        INSERT INTO sessions (user_id, token_hash, expires_at)
        VALUES (%s, %s, %s)
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(cleanup_query, (idle_timeout_seconds,))
            cursor.execute(insert_query, (user_id, token_hash, expires_at))


def touch_active_session(
    token_hash: str,
    idle_timeout_seconds: int,
) -> int | None:
    query = """
        UPDATE sessions
        SET last_activity = CURRENT_TIMESTAMP
        WHERE token_hash = %s
          AND expires_at > CURRENT_TIMESTAMP
          AND last_activity > CURRENT_TIMESTAMP
              - (%s * INTERVAL '1 second')
        RETURNING user_id
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (token_hash, idle_timeout_seconds))
            row = cursor.fetchone()

    return None if row is None else row["user_id"]


def delete_session(token_hash: str) -> None:
    query = "DELETE FROM sessions WHERE token_hash = %s"
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (token_hash,))
