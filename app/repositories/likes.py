"""Database queries for likes."""

from app.database.connection import get_connection
from app.models.like import Like
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)


def find_like_by_id(like_id: int) -> Like | None:
    query = """
        SELECT id, from_user_id, to_user_id, created_at
        FROM likes
        WHERE id = %s
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (like_id,))
            row = cursor.fetchone()

    return Like(**row) if row is not None else None


def insert_like(from_user_id: int, to_user_id: int) -> Like:
    query = """
        INSERT INTO likes (from_user_id, to_user_id)
        VALUES (%s, %s)
        RETURNING id, from_user_id, to_user_id, created_at
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (from_user_id, to_user_id))
            row = cursor.fetchone()

    if row is None:
        raise RuntimeError("Inserting a like returned no row.")
    logger.info("Inserted like %s", row["id"])
    return Like(**row)
