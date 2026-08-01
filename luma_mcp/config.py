"""Configuration for MewCP Luma MCP Server."""

import logging
import os

SERVER_VERSION = "v1.0.0"
BREAKING_CHANGES: list[dict] = []

LUMA_API_BASE = "https://public-api.luma.com"

CONNECT_TIMEOUT = 5    # TCP connection — fixed across all servers
READ_TIMEOUT = 30      # no documented SLA for Luma's public API; 30s covers standard
                        # CRUD-style event/calendar/guest reads and writes


def configure_logging() -> None:
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    try:
        from pythonjsonlogger import jsonlogger
        handler = logging.StreamHandler()
        handler.setFormatter(
            jsonlogger.JsonFormatter(fmt="%(asctime)s %(name)s %(levelname)s %(message)s")
        )
    except ImportError:
        handler = logging.StreamHandler()
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(log_level)
