"""MCP tools for IBM Storage Scale XCP operations."""

from typing import Any
from mcp.server import Server
from mcp.types import Tool, TextContent

from scale_mcp_server.api.v3.xcp import (
    list_xcp_operations_api,
    get_xcp_operation_api,
    create_xcp_copy_api,
    create_xcp_sync_api,
    cancel_xcp_operation_api,
    get_xcp_operation_status_api,
    get_xcp_operation_logs_api,
)


def register_xcp_tools(server: Server) -> None:
    """Register XCP tools with the MCP server.

    Args:
        server: MCP server instance
    """

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available XCP tools."""
        return [
            Tool(
                name="list_xcp_operations",
                description="List all XCP parallel copy/sync operations",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "domain": {
                            "type": "string",
                            "description": "Domain to be authorized against",
                        },
                    },
                },
            ),
            Tool(
                name="get_xcp_operation",
                description="Get details of a specific XCP operation",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "operation_id": {
                            "type": "string",
                            "description": "XCP operation identifier",
                        },
                        "domain": {
                            "type": "string",
                            "description": "Domain to be authorized against",
                        },
                    },
                    "required": ["operation_id"],
                },
            ),
            Tool(
                name="create_xcp_copy",
                description="Create a new XCP parallel file copy operation",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "copy_data": {
                            "type": "object",
                            "description": "XCP copy configuration including source and target paths",
                        },
                        "domain": {
                            "type": "string",
                            "description": "Domain to be authorized against",
                        },
                    },
                    "required": ["copy_data"],
                },
            ),
            Tool(
                name="create_xcp_sync",
                description="Create a new XCP parallel file synchronization operation",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "sync_data": {
                            "type": "object",
                            "description": "XCP sync configuration including source and target paths",
                        },
                        "domain": {
                            "type": "string",
                            "description": "Domain to be authorized against",
                        },
                    },
                    "required": ["sync_data"],
                },
            ),
            Tool(
                name="cancel_xcp_operation",
                description="Cancel a running XCP operation",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "operation_id": {
                            "type": "string",
                            "description": "XCP operation identifier",
                        },
                        "domain": {
                            "type": "string",
                            "description": "Domain to be authorized against",
                        },
                    },
                    "required": ["operation_id"],
                },
            ),
            Tool(
                name="get_xcp_operation_status",
                description="Get status and progress of an XCP operation",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "operation_id": {
                            "type": "string",
                            "description": "XCP operation identifier",
                        },
                        "domain": {
                            "type": "string",
                            "description": "Domain to be authorized against",
                        },
                    },
                    "required": ["operation_id"],
                },
            ),
            Tool(
                name="get_xcp_operation_logs",
                description="Get logs for an XCP operation",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "operation_id": {
                            "type": "string",
                            "description": "XCP operation identifier",
                        },
                        "domain": {
                            "type": "string",
                            "description": "Domain to be authorized against",
                        },
                    },
                    "required": ["operation_id"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: Any) -> list[TextContent]:
        """Handle tool calls for XCP operations."""
        try:
            if name == "list_xcp_operations":
                result = await list_xcp_operations_api(domain=arguments.get("domain"))
                return [TextContent(type="text", text=str(result))]

            elif name == "get_xcp_operation":
                result = await get_xcp_operation_api(
                    operation_id=arguments["operation_id"],
                    domain=arguments.get("domain"),
                )
                return [TextContent(type="text", text=str(result))]

            elif name == "create_xcp_copy":
                result = await create_xcp_copy_api(
                    copy_data=arguments["copy_data"],
                    domain=arguments.get("domain"),
                )
                return [TextContent(type="text", text=str(result))]

            elif name == "create_xcp_sync":
                result = await create_xcp_sync_api(
                    sync_data=arguments["sync_data"],
                    domain=arguments.get("domain"),
                )
                return [TextContent(type="text", text=str(result))]

            elif name == "cancel_xcp_operation":
                result = await cancel_xcp_operation_api(
                    operation_id=arguments["operation_id"],
                    domain=arguments.get("domain"),
                )
                return [TextContent(type="text", text=str(result))]

            elif name == "get_xcp_operation_status":
                result = await get_xcp_operation_status_api(
                    operation_id=arguments["operation_id"],
                    domain=arguments.get("domain"),
                )
                return [TextContent(type="text", text=str(result))]

            elif name == "get_xcp_operation_logs":
                result = await get_xcp_operation_logs_api(
                    operation_id=arguments["operation_id"],
                    domain=arguments.get("domain"),
                )
                return [TextContent(type="text", text=str(result))]

            else:
                raise ValueError(f"Unknown tool: {name}")

        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
