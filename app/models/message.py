from dataclasses import dataclass
from datetime import datetime

@dataclass
class Message:
    """
    Represent a message between users.

    Attributes:
        id: Database identifier.
        sender_id: ID of the user who sent the message.
        receiver_id: ID of the user who received the message.
        created_at: Timestamp of when the message was created.
    """

    id: int
    sender_id: int
    receiver_id: int
    content: str
    read: bool
    created_at: datetime
