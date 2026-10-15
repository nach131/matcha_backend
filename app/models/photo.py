from dataclasses import dataclass
from datetime import datetime

@dataclass
class Photo:
    id: int
    user_id: int
    path: str
    is_profile: bool
    created_at: datetime