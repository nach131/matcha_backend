"""Error handling functions for database operations."""

import psycopg

from flask import Flask, jsonify
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)

def handle_unique_violation(error: psycopg.errors.UniqueViolation):
    logger.warning("Database uniqueness constraint violated: %s", error)
    return jsonify({
        "success": False,
        "error": "A user with that value already exists.",
    }), 409


def handle_integrity_error(error: psycopg.IntegrityError):
    logger.warning("Database integrity constraint violated: %s", error)
    return jsonify({
        "success": False,
        "error": "The request conflicts with the current data.",
    }), 409


def handle_data_error(error: psycopg.DataError):
    logger.warning("Invalid data sent to the database: %s", error)
    return jsonify({
        "success": False,
        "error": "One or more submitted values are invalid.",
    }), 400


def handle_transient_database_error(error: psycopg.Error):
    logger.exception("Transient database error: %s", error)
    return jsonify({
        "success": False,
        "error": "The database is temporarily unavailable. Please try again.",
    }), 503


def handle_operational_error(error: psycopg.OperationalError):
    logger.exception("Database connection or operation failed: %s", error)
    return jsonify({
        "success": False,
        "error": "The database is temporarily unavailable. Please try again.",
    }), 503


def handle_database_error(error: psycopg.Error):
    logger.exception("Database operation failed: %s", error)
    return jsonify({
        "success": False,
        "error": "A database error occurred.",
    }), 500


def register_error_handlers(app: Flask) -> None:
    """
    Register error handlers for the Flask application.
    """
    
    app.register_error_handler(
        psycopg.errors.UniqueViolation,
        handle_unique_violation,
    )
    app.register_error_handler(
        psycopg.IntegrityError,
        handle_integrity_error,
    )
    app.register_error_handler(
        psycopg.DataError,
        handle_data_error,
    )
    app.register_error_handler(
        psycopg.errors.SerializationFailure,
        handle_transient_database_error,
    )
    app.register_error_handler(
        psycopg.errors.DeadlockDetected,
        handle_transient_database_error,
    )
    app.register_error_handler(
        psycopg.OperationalError,
        handle_operational_error,
    )
    app.register_error_handler(
        psycopg.Error,
        handle_database_error
    )