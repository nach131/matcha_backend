from dataclasses import dataclass
from datetime import datetime

@dataclass
class Report:
    id: int
    reporter_id: int
    reported_id: int
    reason: str
    created_at: datetime
