"""IBM Storage Scale API Health MCP Server.

API health tools for the administration daemon (scaleadmd) on cluster nodes.
"""

from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v3.api_health import (
    get_api_health_api,
    get_node_api_health_api,
)

# Create the api_health MCP server
mcp = FastMCP("api_health", instructions="Native REST API health operations")


@mcp.tool()
async def get_api_health(
    ctx: Context,
    page_size: Optional[int] = None,
    page_token: Optional[str] = None,
    domain: Optional[str] = None,
) -> Any:
    """List the health status of the native REST API services on nodes.

    Args:
        page_size: Number of items to return per request
        page_token: Token to navigate to the next page
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: get_api_health")
    try:
        return await get_api_health_api(
            page_size=page_size, page_token=page_token, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to get API health: {str(e)}")
        raise


@mcp.tool()
async def get_node_api_health(
    ctx: Context,
    node_name: str,
    domain: Optional[str] = None,
) -> Any:
    """Get the health status of the native REST API service on a node.

    Args:
        node_name: Node name
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: get_node_api_health with node_name={node_name}")
    try:
        return await get_node_api_health_api(node_name=node_name, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to get API health for node {node_name}: {str(e)}")
        raise
