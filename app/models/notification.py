from dataclasses import dataclass
from datetime import datetime

@dataclass
class Notification:
    """
    Represent a notification for a user.

    Attributes:
        id: Database identifier.
        user_id: ID of the user who received the notification.
        type: Type of the notification.
        related_user_id: ID of the user related to the notification.
        read: Boolean indicating if the notification has been read.
        created_at: Timestamp of when the notification was created.
    """

    id: int
    user_id: int
    type: int
    related_user_id: int
    read: bool
    created_at: datetime
