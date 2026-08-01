"""Calendars group: get_calendar."""

import logging

from fastmcp import FastMCP
from mcp.types import ToolAnnotations

from .. import service
from ..config import CONNECT_TIMEOUT, READ_TIMEOUT
from ..logging_utils import ToolLogger
from ..schemas.calendars import CalendarData, CalendarResult
from ._helpers import _handle_request_exc, _upstream_err

logger = logging.getLogger("luma-mcp.tools.calendars")


def register_calendars_tools(mcp: FastMCP) -> None:

    @mcp.tool(
        name="get_calendar",
        description=(
            "Retrieves details for a calendar and returns its metadata, including name, "
            "slug, URL, description, location, coordinates, and social handles."
        ),
        annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=True),
    )
    def get_calendar() -> CalendarResult:
        tlog = ToolLogger(logger, "get_calendar")

        try:
            data, status, retry_after = service.api_request(
                "GET", "/v1/calendars/get",
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            )
            if 200 <= status < 300:
                tlog.success()
                return CalendarResult(success=True, statusCode=status, data=CalendarData(**data))
            return _upstream_err(CalendarResult, tlog, status, data, retry_after)
        except Exception as exc:
            return _handle_request_exc(CalendarResult, tlog, exc)
