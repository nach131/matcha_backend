from dataclasses import dataclass
from datetime import datetime

@dataclass
class Block:
    """
    Represent a block relationship between users.

    Attributes:
        id: Database identifier.
        blocker_id: ID of the user who blocked another user.
        blocked_id: ID of the user who was blocked.
        created_at: Timestamp of when the block was created.
    """

    id: int
    blocker_id: int
    blocked_id: int
    created_at: datetime
