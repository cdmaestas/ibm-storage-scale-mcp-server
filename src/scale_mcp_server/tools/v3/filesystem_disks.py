"""IBM Storage Scale Filesystem Disks MCP Server.

File system disk tools for adding, deleting, and inspecting disks.
"""

from typing import Any

from fastmcp import Context, FastMCP

from scale_mcp_server.api.v3.filesystem_disks import (
    add_filesystem_disk_api,
    batch_add_filesystem_disks_api,
    batch_delete_filesystem_disks_api,
    delete_filesystem_disk_api,
    get_disks_quorum_api,
    get_filesystem_disk_api,
    list_filesystem_disks_api,
)

# Create the filesystem_disks MCP server
mcp = FastMCP("filesystem_disks", instructions="Filesystem disk management operations")


@mcp.tool()
async def list_filesystem_disks(
    ctx: Context,
    filesystem: str,
    page_size: int | None = None,
    page_token: str | None = None,
    domain: str | None = None,
) -> Any:
    """List all disks in a filesystem.

    Args:
        filesystem: Filesystem name
        page_size: Number of items to return per request
        page_token: Token to navigate to the next page
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: list_filesystem_disks with filesystem={filesystem}")
    try:
        return await list_filesystem_disks_api(
            filesystem=filesystem,
            page_size=page_size,
            page_token=page_token,
            domain=domain,
        )
    except Exception as e:
        await ctx.error(f"Failed to list disks for {filesystem}: {str(e)}")
        raise


@mcp.tool()
async def get_filesystem_disk(
    ctx: Context,
    filesystem: str,
    disk_name: str,
    domain: str | None = None,
) -> Any:
    """Get the current configuration and state of a disk in a filesystem.

    Args:
        filesystem: Filesystem name
        disk_name: Disk name
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: get_filesystem_disk with filesystem={filesystem}, disk_name={disk_name}")
    try:
        return await get_filesystem_disk_api(filesystem=filesystem, disk_name=disk_name, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to get disk {disk_name}: {str(e)}")
        raise


@mcp.tool()
async def add_filesystem_disk(
    ctx: Context,
    filesystem: str,
    disk_data: dict | None = None,
    verify_disks: bool | None = None,
    target_nodes: str | None = None,
    domain: str | None = None,
) -> Any:
    """Add disks to a filesystem.

    Args:
        filesystem: Filesystem name
        disk_data: Disk definition to add
        verify_disks: Verify the disks do not belong to an existing filesystem
        target_nodes: Target nodes (node numbers, ranges, names, IPs, classes)
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: add_filesystem_disk with filesystem={filesystem}")
    try:
        return await add_filesystem_disk_api(
            filesystem=filesystem,
            disk_data=disk_data,
            verify_disks=verify_disks,
            target_nodes=target_nodes,
            domain=domain,
        )
    except Exception as e:
        await ctx.error(f"Failed to add disks to {filesystem}: {str(e)}")
        raise


@mcp.tool()
async def delete_filesystem_disk(
    ctx: Context,
    filesystem: str,
    disk_name: str,
    continue_on_error: bool,
    qos_class: str | None = None,
    rebalance_strategy: str | None = None,
    minimal_copy: bool | None = None,
    preserve_replication: bool | None = None,
    target_nodes: str | None = None,
    permanently_damaged: bool | None = None,
    pit_continue_on_error: bool | None = None,
    domain: str | None = None,
) -> Any:
    """Delete an existing filesystem disk, migrating its data to other disks.

    Args:
        filesystem: Filesystem name
        disk_name: Disk name
        continue_on_error: Continue deleting remaining files on errors
        qos_class: Quality of service class for IO operations
        rebalance_strategy: Rebalance strategy ('strict', 'no_rebalance',
            'default')
        minimal_copy: Minimal copying of data located only on the deleted disk
        preserve_replication: Preserve the replication factor of all files
        target_nodes: Target nodes (node numbers, ranges, names, IPs, classes)
        permanently_damaged: Proceed regardless of permanently damaged disks
        pit_continue_on_error: Continue deleting remaining files on PIT errors
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: delete_filesystem_disk with filesystem={filesystem}, disk_name={disk_name}")
    try:
        return await delete_filesystem_disk_api(
            filesystem=filesystem,
            disk_name=disk_name,
            continue_on_error=continue_on_error,
            qos_class=qos_class,
            rebalance_strategy=rebalance_strategy,
            minimal_copy=minimal_copy,
            preserve_replication=preserve_replication,
            target_nodes=target_nodes,
            permanently_damaged=permanently_damaged,
            pit_continue_on_error=pit_continue_on_error,
            domain=domain,
        )
    except Exception as e:
        await ctx.error(f"Failed to delete disk {disk_name}: {str(e)}")
        raise


@mcp.tool()
async def batch_add_filesystem_disks(
    ctx: Context,
    filesystem: str,
    disks_data: dict,
    domain: str | None = None,
) -> Any:
    """Add a batch of disks to a filesystem.

    Args:
        filesystem: Filesystem name
        disks_data: Batch disk definitions
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: batch_add_filesystem_disks with filesystem={filesystem}")
    try:
        return await batch_add_filesystem_disks_api(filesystem=filesystem, disks_data=disks_data, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to batch add disks to {filesystem}: {str(e)}")
        raise


@mcp.tool()
async def batch_delete_filesystem_disks(
    ctx: Context,
    filesystem: str,
    disk_names: str | None = None,
    qos_class: str | None = None,
    rebalance_strategy: str | None = None,
    minimal_copy: bool | None = None,
    preserve_replication: bool | None = None,
    target_nodes: str | None = None,
    pit_continues_on_error: bool | None = None,
    domain: str | None = None,
) -> Any:
    """Delete a batch of disks from a filesystem.

    Args:
        filesystem: Filesystem name
        disk_names: Names of the disks to delete
        qos_class: Quality of service class for IO operations
        rebalance_strategy: Rebalance strategy (NO_REBALANCE, DEFAULT_STRATEGY,
            STRICT_STRATEGY)
        minimal_copy: Minimal copying of data located only on deleted disks
        preserve_replication: Preserve replication of all files and metadata
        target_nodes: Target nodes (node numbers, ranges, names, IPs, classes)
        pit_continues_on_error: Continue repairing remaining files on PIT errors
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: batch_delete_filesystem_disks with filesystem={filesystem}")
    try:
        return await batch_delete_filesystem_disks_api(
            filesystem=filesystem,
            disk_names=disk_names,
            qos_class=qos_class,
            rebalance_strategy=rebalance_strategy,
            minimal_copy=minimal_copy,
            preserve_replication=preserve_replication,
            target_nodes=target_nodes,
            pit_continues_on_error=pit_continues_on_error,
            domain=domain,
        )
    except Exception as e:
        await ctx.error(f"Failed to batch delete disks from {filesystem}: {str(e)}")
        raise


@mcp.tool()
async def get_disks_quorum(
    ctx: Context,
    filesystem: str,
    domain: str | None = None,
) -> Any:
    """List information about the file system descriptor (disk) quorum.

    Args:
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: get_disks_quorum with filesystem={filesystem}")
    try:
        return await get_disks_quorum_api(filesystem=filesystem, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to get disk quorum for {filesystem}: {str(e)}")
        raise
