from dataclasses import dataclass
from datetime import datetime

@dataclass
class Block:
    id: int
    blocker_id: int
    blocked_id: int
    created_at: datetime
