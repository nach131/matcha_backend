"""Report service functions."""

from collections.abc import Mapping

from app.models.report import Report
from app.repositories.reports import find_report_by_id, insert_report
from app.services.validation import validate_payload, validated_int, validated_str


def get_report(report_id: int) -> Report | None:
    return find_report_by_id(report_id)


def create_report(data: Mapping[str, object]) -> Report:
    values = validate_payload(data, {
        "reporter_id": int,
        "reported_id": int,
        "reason": str,
    })
    return insert_report(
        reporter_id=validated_int(values, "reporter_id"),
        reported_id=validated_int(values, "reported_id"),
        reason=validated_str(values, "reason"),
    )
