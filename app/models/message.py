from dataclasses import dataclass
from datetime import datetime

@dataclass
class Message:
    id: int
    sender_id: int
    receiver_id: int
    content: str
    read: bool
    created_at: datetime
