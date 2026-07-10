"""MCP tools for IBM Storage Scale AFMCOS operations."""

from typing import Any
from mcp.server import Server
from mcp.types import Tool, TextContent

from scale_mcp_server.api.v3.afmcos import (
    list_afmcos_filesets_api,
    get_afmcos_fileset_api,
    create_afmcos_fileset_api,
    update_afmcos_fileset_api,
    delete_afmcos_fileset_api,
    prefetch_afmcos_fileset_api,
    evict_afmcos_fileset_api,
    get_afmcos_fileset_status_api,
)


def register_afmcos_tools(server: Server) -> None:
    """Register AFMCOS tools with the MCP server.

    Args:
        server: MCP server instance
    """

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available AFMCOS tools."""
        return [
            Tool(
                name="list_afmcos_filesets",
                description="List all AFMCOS filesets in a filesystem",
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
                name="get_afmcos_fileset",
                description="Get AFMCOS configuration for a specific fileset",
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
                name="create_afmcos_fileset",
                description="Create an AFMCOS fileset for cloud object storage",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "filesystem": {
                            "type": "string",
                            "description": "Filesystem name",
                        },
                        "afmcos_data": {
                            "type": "object",
                            "description": "AFMCOS fileset configuration data",
                        },
                        "domain": {
                            "type": "string",
                            "description": "Domain to be authorized against",
                        },
                    },
                    "required": ["filesystem", "afmcos_data"],
                },
            ),
            Tool(
                name="update_afmcos_fileset",
                description="Update AFMCOS configuration for a fileset",
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
                        "afmcos_data": {
                            "type": "object",
                            "description": "Updated AFMCOS configuration data",
                        },
                        "domain": {
                            "type": "string",
                            "description": "Domain to be authorized against",
                        },
                    },
                    "required": ["filesystem", "fileset", "afmcos_data"],
                },
            ),
            Tool(
                name="delete_afmcos_fileset",
                description="Delete AFMCOS configuration from a fileset",
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
                name="prefetch_afmcos_fileset",
                description="Prefetch data from cloud object storage for an AFMCOS fileset",
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
                name="evict_afmcos_fileset",
                description="Evict cached data from an AFMCOS fileset",
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
                        "evict_data": {
                            "type": "object",
                            "description": "Optional eviction configuration",
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
                name="get_afmcos_fileset_status",
                description="Get status of an AFMCOS fileset",
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
        """Handle tool calls for AFMCOS operations."""
        try:
            if name == "list_afmcos_filesets":
                result = await list_afmcos_filesets_api(
                    filesystem=arguments["filesystem"],
                    domain=arguments.get("domain"),
                )
                return [TextContent(type="text", text=str(result))]

            elif name == "get_afmcos_fileset":
                result = await get_afmcos_fileset_api(
                    filesystem=arguments["filesystem"],
                    fileset=arguments["fileset"],
                    domain=arguments.get("domain"),
                )
                return [TextContent(type="text", text=str(result))]

            elif name == "create_afmcos_fileset":
                result = await create_afmcos_fileset_api(
                    filesystem=arguments["filesystem"],
                    afmcos_data=arguments["afmcos_data"],
                    domain=arguments.get("domain"),
                )
                return [TextContent(type="text", text=str(result))]

            elif name == "update_afmcos_fileset":
                result = await update_afmcos_fileset_api(
                    filesystem=arguments["filesystem"],
                    fileset=arguments["fileset"],
                    afmcos_data=arguments["afmcos_data"],
                    domain=arguments.get("domain"),
                )
                return [TextContent(type="text", text=str(result))]

            elif name == "delete_afmcos_fileset":
                result = await delete_afmcos_fileset_api(
                    filesystem=arguments["filesystem"],
                    fileset=arguments["fileset"],
                    domain=arguments.get("domain"),
                )
                return [TextContent(type="text", text=str(result))]

            elif name == "prefetch_afmcos_fileset":
                result = await prefetch_afmcos_fileset_api(
                    filesystem=arguments["filesystem"],
                    fileset=arguments["fileset"],
                    prefetch_data=arguments.get("prefetch_data"),
                    domain=arguments.get("domain"),
                )
                return [TextContent(type="text", text=str(result))]

            elif name == "evict_afmcos_fileset":
                result = await evict_afmcos_fileset_api(
                    filesystem=arguments["filesystem"],
                    fileset=arguments["fileset"],
                    evict_data=arguments.get("evict_data"),
                    domain=arguments.get("domain"),
                )
                return [TextContent(type="text", text=str(result))]

            elif name == "get_afmcos_fileset_status":
                result = await get_afmcos_fileset_status_api(
                    filesystem=arguments["filesystem"],
                    fileset=arguments["fileset"],
                    domain=arguments.get("domain"),
                )
                return [TextContent(type="text", text=str(result))]

            else:
                raise ValueError(f"Unknown tool: {name}")

        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
