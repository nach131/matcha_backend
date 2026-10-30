"""Database queries for blocks."""

from app.database.connection import get_connection
from app.models.block import Block
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)


def find_block_by_id(block_id: int) -> Block | None:
    query = """
        SELECT id, blocker_id, blocked_id, created_at
        FROM blocks
        WHERE id = %s
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (block_id,))
            row = cursor.fetchone()

    return Block(**row) if row is not None else None


def insert_block(blocker_id: int, blocked_id: int) -> Block:
    query = """
        INSERT INTO blocks (blocker_id, blocked_id)
        VALUES (%s, %s)
        RETURNING id, blocker_id, blocked_id, created_at
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (blocker_id, blocked_id))
            row = cursor.fetchone()

    if row is None:
        raise RuntimeError("Inserting a block returned no row.")
    logger.info("Inserted block %s", row["id"])
    return Block(**row)
