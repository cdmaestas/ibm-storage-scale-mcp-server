"""IBM Storage Scale Managers MCP Server.

Manager tools for updating the cluster and file system manager nodes.
"""

from typing import Any

from fastmcp import Context, FastMCP

from scale_mcp_server.api.v3.managers import (
    set_cluster_manager_api,
    set_filesystem_manager_api,
)

# Create the managers MCP server
mcp = FastMCP("managers", instructions="Cluster and filesystem manager node operations")


@mcp.tool()
async def set_cluster_manager(
    ctx: Context,
    manager_data: dict,
    domain: str | None = None,
) -> Any:
    """Update the cluster manager node.

    Args:
        manager_data: Request body identifying the new cluster manager node
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: set_cluster_manager")
    try:
        return await set_cluster_manager_api(manager_data=manager_data, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to set cluster manager: {str(e)}")
        raise


@mcp.tool()
async def set_filesystem_manager(
    ctx: Context,
    filesystem: str,
    manager_data: dict,
    domain: str | None = None,
) -> Any:
    """Update the manager node of an existing file system.

    Args:
        filesystem: Filesystem name
        manager_data: Request body identifying the new manager node
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: set_filesystem_manager with filesystem={filesystem}")
    try:
        return await set_filesystem_manager_api(filesystem=filesystem, manager_data=manager_data, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to set manager for {filesystem}: {str(e)}")
        raise
