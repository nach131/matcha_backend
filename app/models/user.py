from datetime import datetime
from dataclasses import dataclass


@dataclass
class User:
    """
    Represent a user.

    Attributes:
        id: Database identifier.
        username: Username of the user.
        email: Email address of the user.
        password_hash: Hashed password of the user.
        gender: Gender of the user.
        sexual_preferences: Sexual preferences of the user.
        biography: Biography of the user.
        latitude: Latitude of the user's location.
        longitude: Longitude of the user's location.
        fame_rating: Fame rating of the user.
        email_verified: Whether the user's email is verified.
        last_login: Timestamp of the user's last login.
        created_at: Timestamp of when the user was created.
    """

    id: int
    username: str
    email: str
    password_hash: str
    gender: str
    sexual_preferences: str
    biography: str
    latitude: float
    longitude: float
    fame_rating: float
    email_verified: bool
    last_login: datetime | None
    created_at: datetime


@dataclass
class UserCreate:
    """
    Represent a user creation request.

    Attributes:
        username: Username of the user.
        email: Email address of the user.
        password_hash: Hashed password of the user.
        gender: Gender of the user.
        sexual_preferences: Sexual preferences of the user.
        biography: Biography of the user.
        latitude: Latitude of the user's location.
        longitude: Longitude of the user's location.
    """

    username: str
    email: str
    password_hash: str
    gender: str
    sexual_preferences: str
    biography: str
    latitude: float
    longitude: float


@dataclass
class UserSearch:
    """
    Represent a user search query.

    Attributes:
        id: Database identifier.
        username: Username of the user.
        gender: Gender of the user.
        sexual_preferences: Sexual preferences of the user.
        latitude: Latitude of the user's location.
        longitude: Longitude of the user's location.
    """

    id: int
    username: str
    gender: str
    sexual_preferences: str
    latitude: float
    longitude: float