"""Database queries for tags."""

from app.database.connection import get_connection
from app.models.tag import Tag
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)


def find_tag_by_id(tag_id: int) -> Tag | None:
    query = """
        SELECT id, name
        FROM tags
        WHERE id = %s
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (tag_id,))
            row = cursor.fetchone()

    return Tag(**row) if row is not None else None


def insert_tag(name: str) -> Tag:
    query = """
        INSERT INTO tags (name)
        VALUES (%s)
        RETURNING id, name
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (name,))
            row = cursor.fetchone()

    if row is None:
        raise RuntimeError("Inserting a tag returned no row.")
    logger.info("Inserted tag %s", row["id"])
    return Tag(**row)
