"""Shared database operations for resource endpoints."""

from collections.abc import Mapping

from psycopg import sql

from app.database.connection import get_connection
from app.resources import ResourceSpec
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)


def find_resource(
    spec: ResourceSpec,
    key_values: Mapping[str, int],
) -> dict[str, object] | None:
    conditions = sql.SQL(" AND ").join(
        sql.SQL("{} = %s").format(sql.Identifier(key))
        for key in key_values
    )
    query = sql.SQL("SELECT * FROM {} WHERE {}").format(
        sql.Identifier(spec.table),
        conditions,
    )

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, tuple(key_values.values()))
            return cursor.fetchone()


def find_resources_by_user(
    spec: ResourceSpec,
    user_id: int,
) -> list[dict[str, object]]:
    if spec.user_link is not None:
        link_table, resource_field, user_field = spec.user_link
        query = sql.SQL(
            "SELECT DISTINCT resource.* "
            "FROM {} AS resource "
            "JOIN {} AS user_link "
            "ON resource.{} = user_link.{} "
            "WHERE user_link.{} = %s"
        ).format(
            sql.Identifier(spec.table),
            sql.Identifier(link_table),
            sql.Identifier(spec.primary_key[0]),
            sql.Identifier(resource_field),
            sql.Identifier(user_field),
        )
    else:
        conditions = sql.SQL(" OR ").join(
            sql.SQL("{} = %s").format(sql.Identifier(field))
            for field in spec.user_filter_fields
        )
        query = sql.SQL("SELECT * FROM {} WHERE ({})").format(
            sql.Identifier(spec.table),
            conditions,
        )

    with get_connection() as conn:
        with conn.cursor() as cursor:
            params = (
                (user_id,)
                if spec.user_link is not None
                else (user_id,) * len(spec.user_filter_fields)
            )
            cursor.execute(query, params)
            return cursor.fetchall()


def insert_resource(
    spec: ResourceSpec,
    values: Mapping[str, object],
) -> dict[str, object]:
    insert_values = {**values, **spec.defaults}
    columns = tuple(insert_values)
    column_sql = sql.SQL(", ").join(
        sql.Identifier(column) for column in columns
    )
    placeholders = sql.SQL(", ").join(
        sql.Placeholder() for _ in columns
    )
    query = sql.SQL("INSERT INTO {} ({}) VALUES ({}) RETURNING *").format(
        sql.Identifier(spec.table),
        column_sql,
        placeholders,
    )

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, tuple(insert_values.values()))
            row = cursor.fetchone()
            if row is None:
                raise RuntimeError(f"Insert into {spec.table} returned no row.")
            logger.info("Inserted resource into %s", spec.table)
            return row
