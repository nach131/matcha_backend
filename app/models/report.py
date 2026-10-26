from dataclasses import dataclass
from datetime import datetime

@dataclass
class Report:
    """
    Represent a report submitted by a user.

    Attributes:
        id: Database identifier.
        reporter_id: ID of the user who submitted the report.
        reported_id: ID of the user who was reported.
        reason: Reason for the report.
        created_at: Timestamp of when the report was created.
    """

    id: int
    reporter_id: int
    reported_id: int
    reason: str
    created_at: datetime
