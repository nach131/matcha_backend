import os

from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row

DATABASE_URL = (
    f"host={os.environ['DB_HOST']} "
    f"port={os.environ.get('DB_PORT', '5432')} "
    f"dbname={os.environ['DB_NAME']} "
    f"user={os.environ['DB_USER']} "
    f"password={os.environ['DB_PASSWORD']}"
)

pool = ConnectionPool(
    conninfo=DATABASE_URL,
    min_size=1,
    max_size=10,
    kwargs={
        "row_factory": dict_row
    }
)

def get_connection():
    return pool.connection()