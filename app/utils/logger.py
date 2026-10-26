"""Logging utility for the application."""

import os, sys, logging, logging.handlers

"""
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0
"""

# Default variables for logging configuration
DEFAULT_LOG_LEVEL = logging.WARNING
DEFAULT_LOG_FILE = "/var/log/matcha_backend.log"

class Logger:
    _log_level: int = DEFAULT_LOG_LEVEL
    _logger: logging.Logger | None = None

    @classmethod
    def create_logger(cls, log_file: str = DEFAULT_LOG_FILE) -> logging.Logger:
        """
        Create and configure the logger instance. If a logger already exists, return it. Otherwise, create a new logger with the specified log file and log level.

        Args:
            log_file: The path to the log file if the user wants to specify a custom location.

        Returns:
            The configured logger instance.
        """

        if cls._logger is not None:
            return cls._logger

        if os.getenv("LOG_LEVEL"):
            cls._log_level = logging.getLevelName(os.getenv("LOG_LEVEL"))
        logger = logging.getLogger("matcha_backend")
        logger.setLevel(cls._log_level)

        if not logger.handlers:
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
            )

            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(cls._log_level)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

            try:
                # Size-based log rotation
                file_handler = logging.handlers.RotatingFileHandler(
                    log_file,
                    maxBytes = 10 * 1024 * 1024,
                    backupCount = 5,
                )
                # Time-based log rotation (uncomment if needed)
                # file_handler = logging.handlers.TimedRotatingFileHandler(
                #     log_file,
                #     when = "midnight",
                #     interval = 1,
                #     backupCount = 30,
                #     encoding = "utf-8",
                # )
            except OSError as exc:
                logger.error("Could not open log file %s: %s", log_file, exc)
            else:
                file_handler.setLevel(cls._log_level)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)

        cls._logger = logger
        return cls._logger

    @staticmethod
    def get_logger(name: str = "", log_level: int | None = None) -> logging.Logger:
        """
        Get a logger instance with a specific name and log level.

        Args:
            name: The name of the logger.
            log_level: The log level for the logger.

        Returns:
            The requested logger instance.
        """

        logger_name = "matcha_backend"
        if name:
            logger_name = f"{logger_name}.{name}"
        logger = logging.getLogger(logger_name)
        if log_level is not None:
            logger.setLevel(log_level)
        return logger
