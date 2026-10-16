import os
import sys
import logging
import logging.handlers

DEFAULT_LOG_LEVEL = logging.WARNING
DEFAULT_LOG_FILE = "/var/log/matcha_backend.log"

class Logger:
    _logger: logging.Logger | None = None

    @classmethod
    def create_logger(cls, log_file: str = DEFAULT_LOG_FILE) -> logging.Logger:
        if cls._logger is not None:
            return cls._logger

        logger = logging.getLogger("matcha_backend")
        logger.setLevel(DEFAULT_LOG_LEVEL)

        if not logger.handlers:
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
            )

            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(DEFAULT_LOG_LEVEL)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

            try:
                file_handler = logging.handlers.RotatingFileHandler(
                    log_file,
                    maxBytes=10 * 1024 * 1024,
                    backupCount=5,
                )
            except OSError as exc:
                logger.error("Could not open log file %s: %s", log_file, exc)
            else:
                file_handler.setLevel(DEFAULT_LOG_LEVEL)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)

        cls._logger = logger
        return cls._logger

    @classmethod
    def get_logger(cls) -> logging.Logger:
        if cls._logger is None:
            raise RuntimeError(
                "Logger has not been initialized; call Logger.create_logger() first."
            )
        return cls._logger
