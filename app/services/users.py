"""User service functions."""

import re, math

from collections.abc import Mapping
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from app.models.user import User, UserCreate
from app.repositories.users import (
    find_user_by_id,
    find_user_by_name,
    record_user_login,
    search_users_by_name,
    insert_user,
)
from app.services.sessions import (
    create_session,
    revoke_session,
)


def get_user(user_name: str):
    """Retrieve a user from the database by their username."""

    return find_user_by_name(user_name)

def search_users(user_name: str):
    """Search for users by their username."""

    return search_users_by_name(user_name)


def authenticate_user(data: Mapping[str, object]) -> User | None:
    """Authenticate a user and record the successful login time."""

    required_fields = {"username", "password"}
    missing_fields = required_fields - set(data)
    unexpected_fields = set(data) - required_fields
    errors: list[str] = []

    if missing_fields:
        errors.append(
            f"Missing required fields: {', '.join(sorted(missing_fields))}."
        )
    if unexpected_fields:
        errors.append(
            f"Unexpected fields: {', '.join(sorted(unexpected_fields))}."
        )

    username = data.get("username")
    password = data.get("password")
    if not isinstance(username, str) or not username.strip():
        errors.append("'username' must be a non-empty string.")
    if not isinstance(password, str) or not password.strip():
        errors.append("'password' must be a non-empty string.")

    if errors:
        raise ValueError(" ".join(errors))

    assert isinstance(username, str)
    assert isinstance(password, str)
    user = find_user_by_name(username.strip())
    if user is None or not check_password_hash(user.password_hash, password):
        return None

    last_login = record_user_login(user.id)
    if last_login is None:
        return None

    user.last_login = last_login
    return user


def login_user(
    data: Mapping[str, object],
) -> tuple[User, str, datetime] | None:
    user = authenticate_user(data)
    if user is None:
        return None

    token, expires_at = create_session(user.id)
    return user, token, expires_at


def get_user_by_id(user_id: int) -> User | None:
    """Retrieve a user by their database identifier."""

    return find_user_by_id(user_id)


def logout_user(token: str | None) -> None:
    revoke_session(token)


def create_user(data: Mapping[str, object]) -> dict[str, int | str]:
    """
    Create a new user in the database after validating the input data.

    Args:
        data: A mapping containing user data.

    Returns:
        A dictionary containing the new user's ID and username.
    """

    required_fields = {
        "username",
        "email",
        "password",
        "gender",
        "sexual_preferences",
        "biography",
        "latitude",
        "longitude",
    }
    unexpected_fields = set(data) - required_fields
    missing_fields = required_fields - set(data)
    errors: list[str] = []

    if missing_fields:
        errors.append(
            f"Missing required fields: {', '.join(sorted(missing_fields))}."
        )
    if unexpected_fields:
        errors.append(
            f"Unexpected fields: {', '.join(sorted(unexpected_fields))}."
        )

    string_fields = (
        "username",
        "email",
        "password",
        "gender",
        "sexual_preferences",
        "biography",
    )
    values: dict[str, object] = {}
    for field in string_fields:
        value = data.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"'{field}' must be a non-empty string.")
        else:
            values[field] = value if field == "password" else value.strip()

    email = values.get("email")
    if isinstance(email, str) and not re.fullmatch(
        r"[^@\s]+@[^@\s]+\.[^@\s]+", email
    ):
        errors.append("'email' must be a valid email address.")

    numeric_fields = ("latitude", "longitude")
    for field in numeric_fields:
        value = data.get(field)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            errors.append(f"'{field}' must be a number.")
        else:
            try:
                numeric_value = float(value)
            except OverflowError:
                errors.append(f"'{field}' must be a finite number.")
            else:
                if not math.isfinite(numeric_value):
                    errors.append(f"'{field}' must be a finite number.")
                else:
                    values[field] = numeric_value

    latitude = values.get("latitude")
    if isinstance(latitude, float) and not -90 <= latitude <= 90:
        errors.append("'latitude' must be between -90 and 90.")

    longitude = values.get("longitude")
    if isinstance(longitude, float) and not -180 <= longitude <= 180:
        errors.append("'longitude' must be between -180 and 180.")

    if errors:
        raise ValueError(" ".join(errors))

    username = values["username"]
    email = values["email"]
    password = values["password"]
    gender = values["gender"]
    sexual_preferences = values["sexual_preferences"]
    biography = values["biography"]
    latitude = values["latitude"]
    longitude = values["longitude"]

    assert isinstance(username, str)
    assert isinstance(email, str)
    assert isinstance(password, str)
    assert isinstance(gender, str)
    assert isinstance(sexual_preferences, str)
    assert isinstance(biography, str)
    assert isinstance(latitude, float)
    assert isinstance(longitude, float)

    user = UserCreate(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
        gender=gender,
        sexual_preferences=sexual_preferences,
        biography=biography,
        latitude=latitude,
        longitude=longitude,
    )
    user_id = insert_user(user)

    return {
        "id": user_id,
        "username": user.username,
    }
