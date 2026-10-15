from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
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
