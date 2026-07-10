"""IBM Storage Scale Managers MCP Server.

Manager node management tools for managing manager operations and configuration.
"""

from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v3.managers import (
    list_managers_api,
    get_manager_api,
    add_manager_api,
    remove_manager_api,
    update_manager_api,
)

# Create the managers MCP server
mcp = FastMCP(
    "managers",
    instructions="Manager node management operations",
)


@mcp.tool()
async def list_managers(
    ctx: Context,
    domain: Optional[str] = None,
) -> Any:
    """List all manager nodes.

    Retrieves a list of all manager nodes in the cluster.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing list of manager nodes
    """
    await ctx.info("Tool called: list_managers")
    await ctx.debug("Retrieving list of manager nodes")

    try:
        result = await list_managers_api(domain=domain)
        await ctx.info("Successfully retrieved managers list")
        return result
    except Exception as e:
        await ctx.error(f"Failed to list managers: {str(e)}")
        raise


@mcp.tool()
async def get_manager(
    ctx: Context,
    manager: str,
    domain: Optional[str] = None,
) -> Any:
    """Get details of a specific manager node.

    Retrieves detailed information about a specific manager node.

    Args:
        manager: Manager node name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing manager node details
    """
    await ctx.info(f"Tool called: get_manager for: {manager}")
    await ctx.debug(f"Retrieving details for manager: {manager}")

    try:
        result = await get_manager_api(manager=manager, domain=domain)
        await ctx.info(f"Successfully retrieved manager: {manager}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to get manager {manager}: {str(e)}")
        raise


@mcp.tool()
async def add_manager(
    ctx: Context,
    manager_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Add a new manager node.

    Adds a new manager node to the cluster.

    Args:
        manager_data: Manager node configuration data
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing operation status
    """
    manager_name = manager_data.get("name", "unknown")
    await ctx.info(f"Tool called: add_manager for: {manager_name}")
    await ctx.debug(f"Adding manager node: {manager_name}")

    try:
        result = await add_manager_api(manager_data=manager_data, domain=domain)
        await ctx.info(f"Successfully added manager: {manager_name}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to add manager {manager_name}: {str(e)}")
        raise


@mcp.tool()
async def remove_manager(
    ctx: Context,
    manager: str,
    domain: Optional[str] = None,
) -> Any:
    """Remove a manager node.

    Removes the specified manager node from the cluster.

    Args:
        manager: Manager node name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing operation status
    """
    await ctx.info(f"Tool called: remove_manager for: {manager}")
    await ctx.debug(f"Removing manager node: {manager}")

    try:
        result = await remove_manager_api(manager=manager, domain=domain)
        await ctx.info(f"Successfully removed manager: {manager}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to remove manager {manager}: {str(e)}")
        raise


@mcp.tool()
async def update_manager(
    ctx: Context,
    manager: str,
    manager_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Update manager node configuration.

    Updates the configuration of a specific manager node.

    Args:
        manager: Manager node name
        manager_data: Updated manager configuration data
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing update status
    """
    await ctx.info(f"Tool called: update_manager for: {manager}")
    await ctx.debug(f"Updating manager node: {manager}")

    try:
        result = await update_manager_api(
            manager=manager, manager_data=manager_data, domain=domain
        )
        await ctx.info(f"Successfully updated manager: {manager}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to update manager {manager}: {str(e)}")
        raise
