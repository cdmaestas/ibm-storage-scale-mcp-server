"""IBM Storage Scale Health Monitoring MCP Server (v3 API).

This module provides health monitoring tools using v3 API endpoints.
Unlike v2 which had dedicated /health endpoints, v3 uses:
- /nodes/status for node health
- /filesystems/{name} for filesystem health
- /nodes/{node}/diagnostics/* for diagnostics
"""

from typing import Any

from fastmcp import Context, FastMCP

from scale_mcp_server.api.v3.health import (
    get_cluster_health_summary_api,
    get_filesystem_health_api,
    get_node_diagnostics_api,
    get_node_health_api,
)

# Create the health monitoring MCP server
mcp = FastMCP(
    "health_v3",
    instructions="Health monitoring and diagnostics operations (v3 API)",
)


@mcp.tool()
async def get_filesystem_health(
    ctx: Context,
    filesystem: str,
    domain: str | None = None,
) -> Any:
    """Get health information for a filesystem.

    Retrieves filesystem health indicators including mount status, capacity,
    and operational state using v3 API endpoints.

    Args:
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing filesystem health information
    """
    await ctx.info(f"Tool called: get_filesystem_health for filesystem: {filesystem}")
    await ctx.debug(f"Retrieving health information for filesystem: {filesystem}")

    try:
        result = await get_filesystem_health_api(filesystem=filesystem, domain=domain)
        await ctx.info(f"Successfully retrieved health information for filesystem: {filesystem}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to get health information for filesystem {filesystem}: {str(e)}")
        raise


@mcp.tool()
async def get_node_health(
    ctx: Context,
    node: str | None = None,
    domain: str | None = None,
) -> Any:
    """Get health/status information for nodes.

    Retrieves node health indicators including daemon status, quorum status,
    and operational state using v3 API endpoints.

    Args:
        node: Specific node name, or None for all nodes
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing node health/status information
    """
    node_info = f" for node: {node}" if node else " for all nodes"
    await ctx.info(f"Tool called: get_node_health{node_info}")
    await ctx.debug(f"Retrieving health/status information{node_info}")

    try:
        result = await get_node_health_api(node=node, domain=domain)
        await ctx.info(f"Successfully retrieved health/status information{node_info}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to get health/status information{node_info}: {str(e)}")
        raise


@mcp.tool()
async def get_node_diagnostics(
    ctx: Context,
    node: str,
    domain: str | None = None,
) -> Any:
    """Get diagnostic information for a specific node.

    Retrieves detailed diagnostic information including version information
    for the specified node.

    Args:
        node: Node name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing node diagnostic information
    """
    await ctx.info(f"Tool called: get_node_diagnostics for node: {node}")
    await ctx.debug(f"Retrieving diagnostics for node: {node}")

    try:
        result = await get_node_diagnostics_api(node=node, domain=domain)
        await ctx.info(f"Successfully retrieved diagnostics for node: {node}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to get diagnostics for node {node}: {str(e)}")
        raise


@mcp.tool()
async def get_cluster_health_summary(
    ctx: Context,
    domain: str | None = None,
) -> Any:
    """Get overall cluster health summary.

    Provides a comprehensive health overview by combining information from
    multiple v3 API endpoints including node status and filesystem information.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing cluster health summary with node and filesystem statistics
    """
    await ctx.info("Tool called: get_cluster_health_summary")
    await ctx.debug("Retrieving cluster health summary")

    try:
        result = await get_cluster_health_summary_api(domain=domain)
        await ctx.info("Successfully retrieved cluster health summary")
        return result
    except Exception as e:
        await ctx.error(f"Failed to get cluster health summary: {str(e)}")
        raise
