"""User repository for handling database operations related to users."""

from app.utils.logger import Logger
from app.database.connection import get_connection
from app.models.user import User, UserCreate, UserSearch

logger = Logger.create_logger(__name__)

def find_user_by_name(user_name: str) -> User | None:
    """
    Find complete user's informations by their username.
    
    Args:
        user_name: The username of the user to find.

    Returns:
        Returns a `User` object if found, otherwise None.
    """

    query = """
        SELECT
            id,
            username,
            email,
            password_hash,
            gender,
            sexual_preferences,
            biography,
            latitude,
            longitude,
            fame_rating,
            email_verified,
            last_login,
            created_at
        FROM users
        WHERE username = %s
    """
    logger.debug(f"Query: {query}")

    with get_connection() as conn:
        with conn.cursor() as cursor:
            logger.info(f"Find user by name: {user_name}")

            cursor.execute(
                query,
                (user_name,)
            )

            row = cursor.fetchone()

    if row is None:
        logger.warning(f"No user found with username: {user_name}")
        return None

    return User(**row)

def search_users_by_name(user_name: str) -> list[UserSearch]:
    """
    Search for users by their username.

    Args:
        user_name: The username to search for.

    Returns:
        A list of `UserSearch` objects that match the search term.
    """

    query = """
        SELECT
            id,
            username,
            gender,
            sexual_preferences,
            latitude,
            longitude
        FROM users
        WHERE username ILIKE %s
    """
    logger.debug(f"Query: {query}")

    with get_connection() as conn:
        with conn.cursor() as cursor:
            logger.info(f"Searching users by name: {user_name}")

            cursor.execute(
                query,
                (f"%{user_name}%",)
            )

            rows = cursor.fetchall()
            usernames = ", ".join(row["username"] for row in rows)
            logger.debug("Found %s users: %s", cursor.rowcount, usernames)

    return [UserSearch(**row) for row in rows]

def insert_user(user: UserCreate) -> int:
    """
    Insert a new user into the database.

    Args:
        user: The user creation request.

    Returns:
        The ID of the newly inserted user.
    """

    query = """
        INSERT INTO users (
            username,
            email,
            password_hash,
            gender,
            sexual_preferences,
            biography,
            latitude,
            longitude
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """
    logger.debug(f"Query: {query}")

    with get_connection() as conn:
        with conn.cursor() as cursor:
            logger.info(f"Inserting user: {user.username}")

            cursor.execute(
                query,
                (
                    user.username,
                    user.email,
                    user.password_hash,
                    user.gender,
                    user.sexual_preferences,
                    user.biography,
                    user.latitude,
                    user.longitude,
                )
            )
            user_id = cursor.fetchone()["id"]
            logger.info(f"User inserted successfully: {user.username} (ID: {user_id})")

    return user_id