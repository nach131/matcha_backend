from dataclasses import dataclass
from datetime import datetime

@dataclass
class Notification:
    id: int
    user_id: int
    type: int
    related_user_id: int
    read: bool
    created_at: datetime
