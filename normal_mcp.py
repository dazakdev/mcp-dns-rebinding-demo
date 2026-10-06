"""A plain local MCP server (the victim). Fake data."""

import os

from fastmcp import FastMCP

PORT = int(os.environ.get("PORT", "4040"))
mcp = FastMCP("acme-api")


@mcp.tool
def get_config() -> dict:
    """Read the app configuration."""
    return {
        "app": "acme-api",
        "env": "production",
        "stripe_secret": "sk_test_DEMO",
        "database_url": "postgres://acme:hunter2@localhost/acme",
    }


@mcp.tool
def list_users() -> list:
    """List application users."""
    return [
        {"id": 1, "email": "founder@acme.io", "role": "owner"},
        {"id": 2, "email": "dana@acme.io", "role": "admin"},
    ]


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=PORT)
