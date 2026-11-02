from dataclasses import dataclass
from datetime import datetime

@dataclass
class ProfileVisit:
    """
    Represent a profile visit by a user.

    Attributes:
        id: Database identifier.
        visitor_id: ID of the user who visited the profile.
        visited_id: ID of the user whose profile was visited.
        created_at: Timestamp of when the profile visit was created.
    """

    id: int
    visitor_id: int
    visited_id: int
    created_at: datetime
