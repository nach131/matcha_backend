"""Database queries for suggested user profiles."""

from app.database.connection import get_connection


def find_suggested_profiles(user_id: int) -> list[dict[str, object]]:
    query = """
        WITH requester AS (
            SELECT id, latitude, longitude
            FROM users
            WHERE id = %s
        ),
        shared_tags AS (
            SELECT other_tags.user_id AS candidate_id,
                   COUNT(*)::INTEGER AS shared_tag_count
            FROM user_tags AS own_tags
            JOIN user_tags AS other_tags
              ON other_tags.tag_id = own_tags.tag_id
            JOIN requester AS me
              ON own_tags.user_id = me.id
            WHERE other_tags.user_id <> me.id
            GROUP BY other_tags.user_id
        )
        SELECT
            candidate.id,
            candidate.username,
            candidate.gender,
            candidate.sexual_preferences,
            candidate.biography,
            candidate.latitude,
            candidate.longitude,
            candidate.fame_rating,
            COALESCE(shared_tags.shared_tag_count, 0) AS shared_tag_count,
            6371 * 2 * ASIN(SQRT(LEAST(
                1.0,
                POWER(SIN(RADIANS(candidate.latitude - me.latitude) / 2), 2)
                + COS(RADIANS(me.latitude))
                * COS(RADIANS(candidate.latitude))
                * POWER(SIN(RADIANS(candidate.longitude - me.longitude) / 2), 2)
            ))) AS distance_km
        FROM users AS candidate
        CROSS JOIN requester AS me
        LEFT JOIN shared_tags
          ON shared_tags.candidate_id = candidate.id
        WHERE candidate.id <> me.id
        ORDER BY
            shared_tag_count DESC,
            distance_km ASC,
            candidate.fame_rating DESC,
            candidate.id ASC
        LIMIT 10
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (user_id,))
            return cursor.fetchall()
