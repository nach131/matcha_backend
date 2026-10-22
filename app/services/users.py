import re, math

from collections.abc import Mapping

from werkzeug.security import generate_password_hash

from app.models.user import UserCreate
from app.repositories.users import find_user_by_name, insert_user


def get_user(user_name: str):
    return find_user_by_name(user_name)


def create_user(data: Mapping[str, object]) -> dict[str, int | str]:
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
            values[field] = value.strip()

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
