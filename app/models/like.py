from dataclasses import dataclass
from datetime import datetime

@dataclass
class Like:
    id: int
    from_user_id: int
    to_user_id: int
    created_at: datetime
