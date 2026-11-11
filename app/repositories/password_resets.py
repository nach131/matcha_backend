"""Database operations for one-time password reset codes."""

from datetime import datetime

from app.database.connection import get_connection


def find_user_id_by_email(email: str) -> int | None:
    query = """
        SELECT id
        FROM users
        WHERE email = %s
        ORDER BY id
        LIMIT 1
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (email,))
            row = cursor.fetchone()

    return None if row is None else row["id"]


def store_password_reset_code(
    user_id: int,
    token_hash: str,
    expires_at: datetime,
) -> None:
    query = """
        INSERT INTO password_reset_tokens (user_id, token_hash, expires_at)
        VALUES (%s, %s, %s)
        ON CONFLICT (user_id) DO UPDATE
        SET token_hash = EXCLUDED.token_hash,
            created_at = CURRENT_TIMESTAMP,
            expires_at = EXCLUDED.expires_at
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (user_id, token_hash, expires_at))


def is_password_reset_code_valid(email: str, token_hash: str) -> bool:
    query = """
        SELECT 1
        FROM password_reset_tokens AS reset
        JOIN users AS account
          ON account.id = reset.user_id
        WHERE account.email = %s
          AND reset.token_hash = %s
          AND reset.expires_at > CURRENT_TIMESTAMP
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (email, token_hash))
            return cursor.fetchone() is not None


def consume_password_reset_code(
    email: str,
    token_hash: str,
    password_hash: str,
) -> bool:
    query = """
        WITH consumed AS (
            DELETE FROM password_reset_tokens AS reset
            USING users AS account
            WHERE reset.user_id = account.id
              AND account.email = %s
              AND reset.token_hash = %s
              AND reset.expires_at > CURRENT_TIMESTAMP
            RETURNING reset.user_id
        )
        UPDATE users
        SET password_hash = %s
        WHERE id IN (SELECT user_id FROM consumed)
        RETURNING id
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (email, token_hash, password_hash))
            row = cursor.fetchone()
            if row is None:
                return False

            cursor.execute(
                "DELETE FROM sessions WHERE user_id = %s",
                (row["id"],),
            )

    return True
