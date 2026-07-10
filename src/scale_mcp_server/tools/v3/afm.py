"""MCP tools for IBM Storage Scale AFM operations."""

from typing import Any
from mcp.server import Server
from mcp.types import Tool, TextContent

from scale_mcp_server.api.v3.afm import (
    list_afm_filesets_api,
    get_afm_fileset_api,
    create_afm_fileset_api,
    update_afm_fileset_api,
    delete_afm_fileset_api,
    prefetch_afm_fileset_api,
    resync_afm_fileset_api,
    get_afm_fileset_status_api,
)


def register_afm_tools(server: Server) -> None:
    """Register AFM tools with the MCP server.

    Args:
        server: MCP server instance
    """

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available AFM tools."""
        return [
            Tool(
                name="list_afm_filesets",
                description="List all AFM filesets in a filesystem",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "filesystem": {
                            "type": "string",
                            "description": "Filesystem name",
                        },
                        "domain": {
                            "type": "string",
                            "description": "Domain to be authorized against",
                        },
                    },
                    "required": ["filesystem"],
                },
            ),
            Tool(
                name="get_afm_fileset",
                description="Get AFM configuration for a specific fileset",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "filesystem": {
                            "type": "string",
                            "description": "Filesystem name",
                        },
                        "fileset": {
                            "type": "string",
                            "description": "Fileset name",
                        },
                        "domain": {
                            "type": "string",
                            "description": "Domain to be authorized against",
                        },
                    },
                    "required": ["filesystem", "fileset"],
                },
            ),
            Tool(
                name="create_afm_fileset",
                description="Create an AFM fileset",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "filesystem": {
                            "type": "string",
                            "description": "Filesystem name",
                        },
                        "afm_data": {
                            "type": "object",
                            "description": "AFM fileset configuration data",
                        },
                        "domain": {
                            "type": "string",
                            "description": "Domain to be authorized against",
                        },
                    },
                    "required": ["filesystem", "afm_data"],
                },
            ),
            Tool(
                name="update_afm_fileset",
                description="Update AFM configuration for a fileset",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "filesystem": {
                            "type": "string",
                            "description": "Filesystem name",
                        },
                        "fileset": {
                            "type": "string",
                            "description": "Fileset name",
                        },
                        "afm_data": {
                            "type": "object",
                            "description": "Updated AFM configuration data",
                        },
                        "domain": {
                            "type": "string",
                            "description": "Domain to be authorized against",
                        },
                    },
                    "required": ["filesystem", "fileset", "afm_data"],
                },
            ),
            Tool(
                name="delete_afm_fileset",
                description="Delete AFM configuration from a fileset",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "filesystem": {
                            "type": "string",
                            "description": "Filesystem name",
                        },
                        "fileset": {
                            "type": "string",
                            "description": "Fileset name",
                        },
                        "domain": {
                            "type": "string",
                            "description": "Domain to be authorized against",
                        },
                    },
                    "required": ["filesystem", "fileset"],
                },
            ),
            Tool(
                name="prefetch_afm_fileset",
                description="Prefetch data for an AFM fileset",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "filesystem": {
                            "type": "string",
                            "description": "Filesystem name",
                        },
                        "fileset": {
                            "type": "string",
                            "description": "Fileset name",
                        },
                        "prefetch_data": {
                            "type": "object",
                            "description": "Optional prefetch configuration",
                        },
                        "domain": {
                            "type": "string",
                            "description": "Domain to be authorized against",
                        },
                    },
                    "required": ["filesystem", "fileset"],
                },
            ),
            Tool(
                name="resync_afm_fileset",
                description="Resynchronize an AFM fileset with its source",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "filesystem": {
                            "type": "string",
                            "description": "Filesystem name",
                        },
                        "fileset": {
                            "type": "string",
                            "description": "Fileset name",
                        },
                        "resync_data": {
                            "type": "object",
                            "description": "Optional resync configuration",
                        },
                        "domain": {
                            "type": "string",
                            "description": "Domain to be authorized against",
                        },
                    },
                    "required": ["filesystem", "fileset"],
                },
            ),
            Tool(
                name="get_afm_fileset_status",
                description="Get status of an AFM fileset",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "filesystem": {
                            "type": "string",
                            "description": "Filesystem name",
                        },
                        "fileset": {
                            "type": "string",
                            "description": "Fileset name",
                        },
                        "domain": {
                            "type": "string",
                            "description": "Domain to be authorized against",
                        },
                    },
                    "required": ["filesystem", "fileset"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: Any) -> list[TextContent]:
        """Handle tool calls for AFM operations."""
        try:
            if name == "list_afm_filesets":
                result = await list_afm_filesets_api(
                    filesystem=arguments["filesystem"],
                    domain=arguments.get("domain"),
                )
                return [TextContent(type="text", text=str(result))]

            elif name == "get_afm_fileset":
                result = await get_afm_fileset_api(
                    filesystem=arguments["filesystem"],
                    fileset=arguments["fileset"],
                    domain=arguments.get("domain"),
                )
                return [TextContent(type="text", text=str(result))]

            elif name == "create_afm_fileset":
                result = await create_afm_fileset_api(
                    filesystem=arguments["filesystem"],
                    afm_data=arguments["afm_data"],
                    domain=arguments.get("domain"),
                )
                return [TextContent(type="text", text=str(result))]

            elif name == "update_afm_fileset":
                result = await update_afm_fileset_api(
                    filesystem=arguments["filesystem"],
                    fileset=arguments["fileset"],
                    afm_data=arguments["afm_data"],
                    domain=arguments.get("domain"),
                )
                return [TextContent(type="text", text=str(result))]

            elif name == "delete_afm_fileset":
                result = await delete_afm_fileset_api(
                    filesystem=arguments["filesystem"],
                    fileset=arguments["fileset"],
                    domain=arguments.get("domain"),
                )
                return [TextContent(type="text", text=str(result))]

            elif name == "prefetch_afm_fileset":
                result = await prefetch_afm_fileset_api(
                    filesystem=arguments["filesystem"],
                    fileset=arguments["fileset"],
                    prefetch_data=arguments.get("prefetch_data"),
                    domain=arguments.get("domain"),
                )
                return [TextContent(type="text", text=str(result))]

            elif name == "resync_afm_fileset":
                result = await resync_afm_fileset_api(
                    filesystem=arguments["filesystem"],
                    fileset=arguments["fileset"],
                    resync_data=arguments.get("resync_data"),
                    domain=arguments.get("domain"),
                )
                return [TextContent(type="text", text=str(result))]

            elif name == "get_afm_fileset_status":
                result = await get_afm_fileset_status_api(
                    filesystem=arguments["filesystem"],
                    fileset=arguments["fileset"],
                    domain=arguments.get("domain"),
                )
                return [TextContent(type="text", text=str(result))]

            else:
                raise ValueError(f"Unknown tool: {name}")

        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
