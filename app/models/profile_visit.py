from dataclasses import dataclass
from datetime import datetime

@dataclass
class ProfileVisit:
    id: int
    visitor_id: int
    visited_id: int
    created_at: datetime
