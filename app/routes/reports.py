"""Flask routes for reports."""

from dataclasses import asdict

from flask import Blueprint, request

from app.services.reports import create_report, get_report
from app.utils.logger import Logger

reports_bp = Blueprint("reports", __name__, url_prefix="/reports")
logger = Logger.get_logger(__name__)


@reports_bp.get("/<int:report_id>")
def get_report_route(report_id: int):
    report = get_report(report_id)
    if report is None:
        return {
            "success": False,
            "message": f"Report {report_id} not found.",
            "data": None,
        }, 404

    return {
        "success": True,
        "message": "Report retrieved successfully.",
        "data": asdict(report),
    }, 200


@reports_bp.post("/create")
def create_report_route():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return {"success": False, "message": "Request body must be a JSON object."}, 400

    try:
        report = create_report(data)
    except ValueError as exc:
        return {"success": False, "message": str(exc), "data": None}, 400

    logger.info("Report created: %s", report.id)
    return {
        "success": True,
        "message": "Report created successfully.",
        "data": asdict(report),
    }, 201
