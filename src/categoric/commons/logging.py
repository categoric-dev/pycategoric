"""Unified logging configuration."""

import logging
import os
import sys

from loguru import logger

# Constants for logging configuration
LOG_LEVEL_STR = os.environ.get("LOG_LEVEL", "DEBUG")
LOG_LEVEL = logging.getLevelName(LOG_LEVEL_STR)
JSON_LOGS = os.environ.get("JSON_LOGS", "0") == "1"


class InterceptHandler(logging.Handler):
    """Default handler for cases with (G)Uvicorn and loguru.
    See: https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record):
        # find caller from where originated the logged message
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


def get_eager_logging_config() -> dict:
    """Manual parse of sys.argv for logging flags before Typer starts."""
    level = None
    testing = False
    for i, arg in enumerate(sys.argv):
        if arg == "--log-level" and i + 1 < len(sys.argv):
            level = sys.argv[i + 1]
        elif arg.startswith("--log-level="):
            level = arg.split("=", 1)[1]
        elif arg in ["--testing"]:
            testing = True
    return {"level": level, "is_testing": testing}


def setup_logging(level: str | None = None, is_testing: bool = False):
    """Configure unified logging for the application."""
    # intercept everything at the root logger
    logging.root.handlers = [InterceptHandler()]
    if is_testing or level == "SILENT":
        logging.root.setLevel(100)
    else:
        logging.root.setLevel(LOG_LEVEL)

    # remove every other logger's handlers
    # and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # configure loguru
    # Remove existing handlers to avoid duplicates (important for reload)
    logger.remove()

    # Standard format for text logs if not JSON
    LOGURU_FORMAT = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS!UTC}</green> "
        "| <level>{level: <8}</level> "
        "| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> "
        "- <level>{message}</level>"
    )

    effective_level = level or LOG_LEVEL_STR

    if is_testing or effective_level == "SILENT":
        # Do not add any loguru handlers
        pass
    elif JSON_LOGS:
        logger.configure(
            handlers=[
                {
                    "sink": sys.stdout,
                    "serialize": True,
                    "level": effective_level,
                    "diagnose": False,
                },
            ],
        )
    else:
        logger.configure(
            handlers=[
                {
                    "sink": sys.stdout,
                    "format": LOGURU_FORMAT,
                    "level": effective_level,
                    "diagnose": False,
                },
            ],
        )

    # Specifically ensure uvicorn loggers are intercepted
    for name in ["uvicorn", "uvicorn.access", "uvicorn.error"]:
        u_logger = logging.getLogger(name)
        u_logger.handlers = []
        u_logger.propagate = True

    # Configure Telemetry (OpenObserve integration)
    if os.getenv("OPENOBSERVE_ENDPOINT"):
        try:
            from categoric.commons.openobserve import (
                setup_telemetry,
            )

            setup_telemetry()
        except Exception:
            logger.warning("Failed to setup telemetry")
