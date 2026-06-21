import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="MewCP Luma MCP Server")
    parser.add_argument("-t", "--transport", default=None, help="Transport: stdio or streamable-http")
    parser.add_argument("--host", default=None, help="Bind address")
    parser.add_argument("--port", type=int, default=None, help="Listen port")
    return parser.parse_args()
