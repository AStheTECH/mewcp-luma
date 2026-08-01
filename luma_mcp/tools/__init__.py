"""MewCP Luma tool registration."""

from fastmcp import FastMCP

from .events_tools import register_events_tools
from .calendars_tools import register_calendars_tools


def register_tools(mcp: FastMCP) -> None:
    register_events_tools(mcp)
    register_calendars_tools(mcp)
