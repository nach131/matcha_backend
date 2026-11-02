from dataclasses import dataclass
from datetime import datetime

@dataclass
class Photo:
    """
    Represent a photo uploaded by a user.

    Attributes:
        id: Database identifier.
        user_id: ID of the user who uploaded the photo.
        path: Path to the photo file.
        is_profile: Boolean indicating if the photo is the user's profile photo.
        created_at: Timestamp of when the photo was created.
    """

    id: int
    user_id: int
    path: str
    is_profile: bool
    created_at: datetime