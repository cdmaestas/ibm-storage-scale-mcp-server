"""MCP tools for IBM Storage Scale Remote Filesystem operations."""

from typing import Any
from mcp.server import Server
from mcp.types import Tool, TextContent

from scale_mcp_server.api.v3.remote_filesystems import (
    list_remote_filesystems_api,
    get_remote_filesystem_api,
    mount_remote_filesystem_api,
    unmount_remote_filesystem_api,
    get_remote_filesystem_status_api,
)


def register_remote_filesystem_tools(server: Server) -> None:
    """Register remote filesystem tools with the MCP server.

    Args:
        server: MCP server instance
    """

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available remote filesystem tools."""
        return [
            Tool(
                name="list_remote_filesystems",
                description="List filesystems on a remote cluster",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "cluster": {
                            "type": "string",
                            "description": "Remote cluster name",
                        },
                        "domain": {
                            "type": "string",
                            "description": "Domain to be authorized against",
                        },
                    },
                    "required": ["cluster"],
                },
            ),
            Tool(
                name="get_remote_filesystem",
                description="Get details of a filesystem on a remote cluster",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "cluster": {
                            "type": "string",
                            "description": "Remote cluster name",
                        },
                        "filesystem": {
                            "type": "string",
                            "description": "Filesystem name",
                        },
                        "domain": {
                            "type": "string",
                            "description": "Domain to be authorized against",
                        },
                    },
                    "required": ["cluster", "filesystem"],
                },
            ),
            Tool(
                name="mount_remote_filesystem",
                description="Mount a remote filesystem locally",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "cluster": {
                            "type": "string",
                            "description": "Remote cluster name",
                        },
                        "filesystem": {
                            "type": "string",
                            "description": "Filesystem name",
                        },
                        "mount_data": {
                            "type": "object",
                            "description": "Optional mount configuration",
                        },
                        "domain": {
                            "type": "string",
                            "description": "Domain to be authorized against",
                        },
                    },
                    "required": ["cluster", "filesystem"],
                },
            ),
            Tool(
                name="unmount_remote_filesystem",
                description="Unmount a remote filesystem",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "cluster": {
                            "type": "string",
                            "description": "Remote cluster name",
                        },
                        "filesystem": {
                            "type": "string",
                            "description": "Filesystem name",
                        },
                        "unmount_data": {
                            "type": "object",
                            "description": "Optional unmount configuration",
                        },
                        "domain": {
                            "type": "string",
                            "description": "Domain to be authorized against",
                        },
                    },
                    "required": ["cluster", "filesystem"],
                },
            ),
            Tool(
                name="get_remote_filesystem_status",
                description="Get status of a remote filesystem",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "cluster": {
                            "type": "string",
                            "description": "Remote cluster name",
                        },
                        "filesystem": {
                            "type": "string",
                            "description": "Filesystem name",
                        },
                        "domain": {
                            "type": "string",
                            "description": "Domain to be authorized against",
                        },
                    },
                    "required": ["cluster", "filesystem"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: Any) -> list[TextContent]:
        """Handle tool calls for remote filesystem operations."""
        try:
            if name == "list_remote_filesystems":
                result = await list_remote_filesystems_api(
                    cluster=arguments["cluster"],
                    domain=arguments.get("domain"),
                )
                return [TextContent(type="text", text=str(result))]

            elif name == "get_remote_filesystem":
                result = await get_remote_filesystem_api(
                    cluster=arguments["cluster"],
                    filesystem=arguments["filesystem"],
                    domain=arguments.get("domain"),
                )
                return [TextContent(type="text", text=str(result))]

            elif name == "mount_remote_filesystem":
                result = await mount_remote_filesystem_api(
                    cluster=arguments["cluster"],
                    filesystem=arguments["filesystem"],
                    mount_data=arguments.get("mount_data"),
                    domain=arguments.get("domain"),
                )
                return [TextContent(type="text", text=str(result))]

            elif name == "unmount_remote_filesystem":
                result = await unmount_remote_filesystem_api(
                    cluster=arguments["cluster"],
                    filesystem=arguments["filesystem"],
                    unmount_data=arguments.get("unmount_data"),
                    domain=arguments.get("domain"),
                )
                return [TextContent(type="text", text=str(result))]

            elif name == "get_remote_filesystem_status":
                result = await get_remote_filesystem_status_api(
                    cluster=arguments["cluster"],
                    filesystem=arguments["filesystem"],
                    domain=arguments.get("domain"),
                )
                return [TextContent(type="text", text=str(result))]

            else:
                raise ValueError(f"Unknown tool: {name}")

        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
