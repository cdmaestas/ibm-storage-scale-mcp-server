"""IBM Storage Scale Filesystem Disks MCP Server.

Filesystem disk management tools for managing disks within filesystems.
"""

from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v3.filesystem_disks import (
    list_filesystem_disks_api,
    get_filesystem_disk_api,
    add_disks_to_filesystem_api,
    remove_disk_from_filesystem_api,
    update_filesystem_disk_api,
)

# Create the filesystem disks MCP server
mcp = FastMCP(
    "filesystem_disks",
    instructions="Filesystem disk management operations",
)


@mcp.tool()
async def list_filesystem_disks(
    ctx: Context,
    filesystem: str,
    domain: Optional[str] = None,
) -> Any:
    """List all disks in a filesystem.

    Retrieves a list of all disks associated with the specified filesystem.

    Args:
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing list of filesystem disks
    """
    await ctx.info(f"Tool called: list_filesystem_disks for: {filesystem}")
    await ctx.debug(f"Listing disks for filesystem: {filesystem}")

    try:
        result = await list_filesystem_disks_api(filesystem=filesystem, domain=domain)
        await ctx.info(f"Successfully listed disks for filesystem: {filesystem}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to list disks for filesystem {filesystem}: {str(e)}")
        raise


@mcp.tool()
async def get_filesystem_disk(
    ctx: Context,
    filesystem: str,
    disk: str,
    domain: Optional[str] = None,
) -> Any:
    """Get details of a specific disk in a filesystem.

    Retrieves detailed information about a specific disk in the filesystem.

    Args:
        filesystem: Filesystem name
        disk: Disk name or NSD name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing disk details
    """
    await ctx.info(f"Tool called: get_filesystem_disk for: {filesystem}/{disk}")
    await ctx.debug(f"Retrieving disk details: {disk} in {filesystem}")

    try:
        result = await get_filesystem_disk_api(
            filesystem=filesystem, disk=disk, domain=domain
        )
        await ctx.info(f"Successfully retrieved disk: {disk} in {filesystem}")
        return result
    except Exception as e:
        await ctx.error(
            f"Failed to get disk {disk} in filesystem {filesystem}: {str(e)}"
        )
        raise


@mcp.tool()
async def add_disks_to_filesystem(
    ctx: Context,
    filesystem: str,
    disks_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Add disks to a filesystem.

    Adds one or more disks to the specified filesystem.

    Args:
        filesystem: Filesystem name
        disks_data: Data specifying disks to add
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing operation status
    """
    await ctx.info(f"Tool called: add_disks_to_filesystem for: {filesystem}")
    await ctx.debug(f"Adding disks to filesystem: {filesystem}")

    try:
        result = await add_disks_to_filesystem_api(
            filesystem=filesystem, disks_data=disks_data, domain=domain
        )
        await ctx.info(f"Successfully added disks to filesystem: {filesystem}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to add disks to filesystem {filesystem}: {str(e)}")
        raise


@mcp.tool()
async def remove_disk_from_filesystem(
    ctx: Context,
    filesystem: str,
    disk: str,
    domain: Optional[str] = None,
) -> Any:
    """Remove a disk from a filesystem.

    Removes the specified disk from the filesystem.

    Args:
        filesystem: Filesystem name
        disk: Disk name or NSD name to remove
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing operation status
    """
    await ctx.info(f"Tool called: remove_disk_from_filesystem for: {filesystem}/{disk}")
    await ctx.debug(f"Removing disk: {disk} from {filesystem}")

    try:
        result = await remove_disk_from_filesystem_api(
            filesystem=filesystem, disk=disk, domain=domain
        )
        await ctx.info(f"Successfully removed disk: {disk} from {filesystem}")
        return result
    except Exception as e:
        await ctx.error(
            f"Failed to remove disk {disk} from filesystem {filesystem}: {str(e)}"
        )
        raise


@mcp.tool()
async def update_filesystem_disk(
    ctx: Context,
    filesystem: str,
    disk: str,
    disk_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Update disk configuration in a filesystem.

    Updates the configuration of a specific disk in the filesystem.

    Args:
        filesystem: Filesystem name
        disk: Disk name or NSD name
        disk_data: Updated disk configuration data
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing update status
    """
    await ctx.info(f"Tool called: update_filesystem_disk for: {filesystem}/{disk}")
    await ctx.debug(f"Updating disk: {disk} in {filesystem}")

    try:
        result = await update_filesystem_disk_api(
            filesystem=filesystem, disk=disk, disk_data=disk_data, domain=domain
        )
        await ctx.info(f"Successfully updated disk: {disk} in {filesystem}")
        return result
    except Exception as e:
        await ctx.error(
            f"Failed to update disk {disk} in filesystem {filesystem}: {str(e)}"
        )
        raise
