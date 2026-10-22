from datetime import datetime
from dataclasses import dataclass


@dataclass
class UserCreate:
    username: str
    email: str
    password_hash: str
    gender: str
    sexual_preferences: str
    biography: str
    latitude: float
    longitude: float


@dataclass
class  User:
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
class UserSearch:
    id: int
    username: str
    gender: str
    sexual_preferences: str
    latitude: float
    longitude: float