"""Database queries for photos."""

from app.database.connection import get_connection
from app.models.photo import Photo
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)


def find_photo_by_id(photo_id: int) -> Photo | None:
    query = """
        SELECT id, user_id, path, is_profile, created_at
        FROM photos
        WHERE id = %s
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (photo_id,))
            row = cursor.fetchone()

    return Photo(**row) if row is not None else None


def insert_photo(user_id: int, path: str, is_profile: bool) -> Photo:
    query = """
        INSERT INTO photos (user_id, path, is_profile)
        VALUES (%s, %s, %s)
        RETURNING id, user_id, path, is_profile, created_at
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (user_id, path, is_profile))
            row = cursor.fetchone()

    if row is None:
        raise RuntimeError("Inserting a photo returned no row.")
    logger.info("Inserted photo %s", row["id"])
    return Photo(**row)
