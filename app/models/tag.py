from dataclasses import dataclass

@dataclass
class Tag:
    """
    Represent a tag.

    Attributes:
        id: Database identifier.
        name: Name of the tag.
    """

    id: int
    name: str