"""Database queries for notifications."""

from app.database.connection import get_connection
from app.models.notification import Notification
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)


def find_notification_by_id(notification_id: int) -> Notification | None:
    query = """
        SELECT id, user_id, type, related_user_id, read, created_at
        FROM notifications
        WHERE id = %s
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (notification_id,))
            row = cursor.fetchone()

    return Notification(**row) if row is not None else None


def insert_notification(
    user_id: int,
    notification_type: int,
    related_user_id: int,
) -> Notification:
    query = """
        INSERT INTO notifications (user_id, type, related_user_id, read)
        VALUES (%s, %s, %s, FALSE)
        RETURNING id, user_id, type, related_user_id, read, created_at
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (user_id, notification_type, related_user_id))
            row = cursor.fetchone()

    if row is None:
        raise RuntimeError("Inserting a notification returned no row.")
    logger.info("Inserted notification %s", row["id"])
    return Notification(**row)
