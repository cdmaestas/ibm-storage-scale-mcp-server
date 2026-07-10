"""MCP tools for IBM Storage Scale Authorization operations."""

from typing import Any
from mcp.server import Server
from mcp.types import Tool, TextContent

from scale_mcp_server.api.v3.authorization import (
    login_api,
    logout_api,
    refresh_token_api,
    get_session_info_api,
)


def register_authorization_tools(server: Server) -> None:
    """Register authorization tools with the MCP server.

    Args:
        server: MCP server instance
    """

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available authorization tools."""
        return [
            Tool(
                name="login",
                description="Authenticate and create a session with IBM Storage Scale",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "username": {
                            "type": "string",
                            "description": "Username for authentication",
                        },
                        "password": {
                            "type": "string",
                            "description": "Password for authentication",
                        },
                        "domain": {
                            "type": "string",
                            "description": "Domain to be authorized against (default 'StorageScaleDomain')",
                        },
                    },
                    "required": ["username", "password"],
                },
            ),
            Tool(
                name="logout",
                description="Logout and invalidate the current session",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "domain": {
                            "type": "string",
                            "description": "Domain to be authorized against (default 'StorageScaleDomain')",
                        },
                    },
                },
            ),
            Tool(
                name="refresh_token",
                description="Refresh authentication token using a valid refresh token",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "refresh_token": {
                            "type": "string",
                            "description": "Valid refresh token",
                        },
                        "domain": {
                            "type": "string",
                            "description": "Domain to be authorized against (default 'StorageScaleDomain')",
                        },
                    },
                    "required": ["refresh_token"],
                },
            ),
            Tool(
                name="get_session_info",
                description="Get information about the current authenticated session",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "domain": {
                            "type": "string",
                            "description": "Domain to be authorized against (default 'StorageScaleDomain')",
                        },
                    },
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: Any) -> list[TextContent]:
        """Handle tool calls for authorization operations."""
        try:
            if name == "login":
                result = await login_api(
                    username=arguments["username"],
                    password=arguments["password"],
                    domain=arguments.get("domain"),
                )
                return [TextContent(type="text", text=str(result))]

            elif name == "logout":
                result = await logout_api(domain=arguments.get("domain"))
                return [TextContent(type="text", text=str(result))]

            elif name == "refresh_token":
                result = await refresh_token_api(
                    refresh_token=arguments["refresh_token"],
                    domain=arguments.get("domain"),
                )
                return [TextContent(type="text", text=str(result))]

            elif name == "get_session_info":
                result = await get_session_info_api(domain=arguments.get("domain"))
                return [TextContent(type="text", text=str(result))]

            else:
                raise ValueError(f"Unknown tool: {name}")

        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
