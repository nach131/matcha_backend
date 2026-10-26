from dataclasses import dataclass
from datetime import datetime

@dataclass
class Like:
    """
    Represent a like.

    Attributes:
        id: Database identifier.
        from_user_id: ID of the user who liked another user.
        to_user_id: ID of the user who was liked.
        created_at: Timestamp of when the like was created.
    """

    id: int
    from_user_id: int
    to_user_id: int
    created_at: datetime
