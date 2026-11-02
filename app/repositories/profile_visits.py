"""Database queries for profile visits."""

from app.database.connection import get_connection
from app.models.profile_visit import ProfileVisit
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)


def find_profile_visit_by_id(profile_visit_id: int) -> ProfileVisit | None:
    query = """
        SELECT id, visitor_id, visited_id, created_at
        FROM profile_visits
        WHERE id = %s
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (profile_visit_id,))
            row = cursor.fetchone()

    return ProfileVisit(**row) if row is not None else None


def insert_profile_visit(visitor_id: int, visited_id: int) -> ProfileVisit:
    query = """
        INSERT INTO profile_visits (visitor_id, visited_id)
        VALUES (%s, %s)
        RETURNING id, visitor_id, visited_id, created_at
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (visitor_id, visited_id))
            row = cursor.fetchone()

    if row is None:
        raise RuntimeError("Inserting a profile visit returned no row.")
    logger.info("Inserted profile visit %s", row["id"])
    return ProfileVisit(**row)
