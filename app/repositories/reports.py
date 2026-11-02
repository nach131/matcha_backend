"""Database queries for reports."""

from app.database.connection import get_connection
from app.models.report import Report
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)


def find_report_by_id(report_id: int) -> Report | None:
    query = """
        SELECT id, reporter_id, reported_id, reason, created_at
        FROM reports
        WHERE id = %s
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (report_id,))
            row = cursor.fetchone()

    return Report(**row) if row is not None else None


def insert_report(reporter_id: int, reported_id: int, reason: str) -> Report:
    query = """
        INSERT INTO reports (reporter_id, reported_id, reason)
        VALUES (%s, %s, %s)
        RETURNING id, reporter_id, reported_id, reason, created_at
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (reporter_id, reported_id, reason))
            row = cursor.fetchone()

    if row is None:
        raise RuntimeError("Inserting a report returned no row.")
    logger.info("Inserted report %s", row["id"])
    return Report(**row)
