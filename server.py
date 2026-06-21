import sys
import os

# luma-mcp/ uses a hyphen so it can't be a Python package name;
# add it to sys.path so its modules are importable by name directly.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "luma-mcp"))

from fastmcp import FastMCP
from fastmcp_credentials import CredentialMiddleware, HeaderCredentialBackend
from cli import parse_args
from tools import register_tools

backend = HeaderCredentialBackend()
mcp = FastMCP(
    "MewCP Luma MCP Server",
    middleware=[CredentialMiddleware(backend, "static")],
)
register_tools(mcp)

# ASGI app for hosted platforms (Cloud Run, Vercel, etc.)
app = mcp.http_app(path="/mcp", transport="streamable-http", stateless_http=True)

if __name__ == "__main__":
    args = parse_args()
    run_kwargs: dict = {}
    if args.transport:
        run_kwargs["transport"] = args.transport
    if args.host:
        run_kwargs["host"] = args.host
    if args.port:
        run_kwargs["port"] = args.port
    mcp.run(**run_kwargs)
