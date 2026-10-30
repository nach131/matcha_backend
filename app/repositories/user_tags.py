"""Database queries for user-tag associations."""

from app.database.connection import get_connection
from app.models.user_tag import UserTag
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)


def find_user_tag(user_id: int, tag_id: int) -> UserTag | None:
    query = """
        SELECT user_id, tag_id
        FROM user_tags
        WHERE user_id = %s AND tag_id = %s
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (user_id, tag_id))
            row = cursor.fetchone()

    return UserTag(**row) if row is not None else None


def insert_user_tag(user_id: int, tag_id: int) -> UserTag:
    query = """
        INSERT INTO user_tags (user_id, tag_id)
        VALUES (%s, %s)
        RETURNING user_id, tag_id
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (user_id, tag_id))
            row = cursor.fetchone()

    if row is None:
        raise RuntimeError("Inserting a user tag returned no row.")
    logger.info("Inserted user tag (%s, %s)", user_id, tag_id)
    return UserTag(**row)
