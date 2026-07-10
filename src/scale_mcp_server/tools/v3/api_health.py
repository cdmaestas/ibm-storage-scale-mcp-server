"""IBM Storage Scale API Health MCP Server.

API health monitoring tools for checking REST API service status.
"""

from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v3.api_health import (
    get_api_health_api,
    get_api_status_api,
)

# Create the API health MCP server
mcp = FastMCP(
    "api_health",
    instructions="API health monitoring and status operations",
)


@mcp.tool()
async def get_api_health(
    ctx: Context,
    domain: Optional[str] = None,
) -> Any:
    """Get API health status.

    Checks the health and availability of the Scale REST API service.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing API health status information
    """
    await ctx.info("Tool called: get_api_health")
    await ctx.debug("Checking API health status")

    try:
        result = await get_api_health_api(domain=domain)
        await ctx.info("Successfully retrieved API health status")
        return result
    except Exception as e:
        await ctx.error(f"Failed to get API health: {str(e)}")
        raise


@mcp.tool()
async def get_api_status(
    ctx: Context,
    domain: Optional[str] = None,
) -> Any:
    """Get detailed API status information.

    Retrieves detailed status information about the Scale REST API service
    including version, uptime, and service state.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing detailed API status information
    """
    await ctx.info("Tool called: get_api_status")
    await ctx.debug("Retrieving detailed API status")

    try:
        result = await get_api_status_api(domain=domain)
        await ctx.info("Successfully retrieved API status")
        return result
    except Exception as e:
        await ctx.error(f"Failed to get API status: {str(e)}")
        raise
