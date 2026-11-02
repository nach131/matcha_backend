"""PostgreSQL database connection management."""

import os

from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from app.utils.logger import Logger

DATABASE_URL = os.environ["DATABASE_URL"]

logger = Logger.get_logger(__name__)
pool = ConnectionPool(
    conninfo=DATABASE_URL,
    min_size=1,
    max_size=10,
    kwargs={"row_factory": dict_row},
)

def get_connection():
    """Get a database connection from the connection pool."""

    logger.info("Getting connection from pool...")
    conn = pool.connection()
    logger.info("Connection acquired!")
    logger.debug(f"Connection details: {conn}")
    return conn
