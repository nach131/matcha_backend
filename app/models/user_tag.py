from dataclasses import dataclass

@dataclass
class UserTag:
    """
    Represent a tag associated with a user.

    Attributes:
        id: Database identifier.
        user_id: ID of the user who has the tag.
        tag_id: ID of the tag.
    """
        
    user_id: int
    tag_id: int