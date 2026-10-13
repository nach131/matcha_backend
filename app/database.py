import os

from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row

DATABASE_URL = os.environ["DATABASE_URL"]

pool = ConnectionPool(
    conninfo=DATABASE_URL,
    min_size=1,
    max_size=10,
    kwargs={"row_factory": dict_row},
)

def get_connection():
    return pool.connection()
