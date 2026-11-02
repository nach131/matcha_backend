"""Database queries for messages."""

from app.database.connection import get_connection
from app.models.message import Message
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)


def find_message_by_id(message_id: int) -> Message | None:
    query = """
        SELECT id, sender_id, receiver_id, content, read, created_at
        FROM messages
        WHERE id = %s
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (message_id,))
            row = cursor.fetchone()

    return Message(**row) if row is not None else None


def insert_message(sender_id: int, receiver_id: int, content: str) -> Message:
    query = """
        INSERT INTO messages (sender_id, receiver_id, content, read)
        VALUES (%s, %s, %s, FALSE)
        RETURNING id, sender_id, receiver_id, content, read, created_at
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (sender_id, receiver_id, content))
            row = cursor.fetchone()

    if row is None:
        raise RuntimeError("Inserting a message returned no row.")
    logger.info("Inserted message %s", row["id"])
    return Message(**row)
