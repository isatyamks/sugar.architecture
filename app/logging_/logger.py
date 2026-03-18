"""
Structured logging configuration.

Uses Python stdlib logging with:
- JSON formatter for production (machine-parseable)
- Human-readable formatter for development (colored, indented)

Called once during app startup via create_app().
"""

import logging
import sys


def configure_logging(level: str = "INFO", debug: bool = False) -> None:
    """
    Configure root logger with appropriate handler and formatter.

    Args:
        level: Logging level string (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        debug: If True, use human-readable colored format.
               If False, use structured JSON format for production.
    """
    ...


class JSONFormatter(logging.Formatter):
    """
    Formats log records as single-line JSON objects.

    Output fields: timestamp, level, logger, message, extra
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record as JSON."""
        ...
