"""IBM Storage Scale Filesystem Management MCP Server.

File system tools, including mount state, rebalance/restripe, and directory
operations.
"""

from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v3.filesystems import (
    list_filesystems_api,
    get_filesystem_api,
    create_filesystem_api,
    update_filesystem_api,
    delete_filesystem_api,
    get_mount_status_api,
    mount_filesystem_api,
    unmount_filesystem_api,
    mount_all_filesystems_api,
    unmount_all_filesystems_api,
    rebalance_filesystem_api,
    restripe_filesystem_api,
    list_directory_api,
    stat_directory_api,
    create_directory_api,
    delete_directory_api,
)

# Create the filesystems MCP server
mcp = FastMCP("filesystems", instructions="Filesystem management operations")


@mcp.tool()
async def list_filesystems(
    ctx: Context,
    page_size: Optional[int] = None,
    page_token: Optional[str] = None,
    domain: Optional[str] = None,
) -> Any:
    """List all filesystems registered in the cluster.

    Args:
        page_size: Number of items to return per request
        page_token: Token to navigate to the next page
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: list_filesystems")
    try:
        return await list_filesystems_api(
            page_size=page_size, page_token=page_token, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to list filesystems: {str(e)}")
        raise


@mcp.tool()
async def get_filesystem(
    ctx: Context,
    filesystem: str,
    domain: Optional[str] = None,
) -> Any:
    """Get detailed information about a specific filesystem.

    Args:
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: get_filesystem with filesystem={filesystem}")
    try:
        return await get_filesystem_api(filesystem=filesystem, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to get filesystem {filesystem}: {str(e)}")
        raise


@mcp.tool()
async def create_filesystem(
    ctx: Context,
    filesystem_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Create a new filesystem.

    Args:
        filesystem_data: Filesystem configuration data
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: create_filesystem")
    try:
        return await create_filesystem_api(
            filesystem_data=filesystem_data, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to create filesystem: {str(e)}")
        raise


@mcp.tool()
async def update_filesystem(
    ctx: Context,
    filesystem: str,
    filesystem_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Update the attributes of a filesystem.

    Args:
        filesystem: Filesystem name
        filesystem_data: Updated filesystem attributes
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: update_filesystem with filesystem={filesystem}")
    try:
        return await update_filesystem_api(
            filesystem=filesystem, filesystem_data=filesystem_data, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to update filesystem {filesystem}: {str(e)}")
        raise


@mcp.tool()
async def delete_filesystem(
    ctx: Context,
    name: str,
    permanently_damaged: Optional[bool] = None,
    domain: Optional[str] = None,
) -> Any:
    """Delete a filesystem.

    Args:
        name: Filesystem name
        permanently_damaged: Proceed even if disks are permanently damaged
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: delete_filesystem with name={name}")
    try:
        return await delete_filesystem_api(
            name=name, permanently_damaged=permanently_damaged, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to delete filesystem {name}: {str(e)}")
        raise


@mcp.tool()
async def get_mount_status(
    ctx: Context,
    filesystem: str,
    cluster_name: Optional[str] = None,
    domain: Optional[str] = None,
) -> Any:
    """List the mount state of a filesystem.

    Args:
        filesystem: Filesystem name
        cluster_name: Cluster name
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: get_mount_status with filesystem={filesystem}")
    try:
        return await get_mount_status_api(
            filesystem=filesystem, cluster_name=cluster_name, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to get mount status for {filesystem}: {str(e)}")
        raise


@mcp.tool()
async def mount_filesystem(
    ctx: Context,
    name: str,
    mount_data: Optional[dict] = None,
    domain: Optional[str] = None,
) -> Any:
    """Mount a filesystem on one or more nodes.

    Args:
        name: Filesystem name
        mount_data: Mount parameters, e.g. {"mount_options": ...,
            "mount_point": ..., "target_nodes": [...]}
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: mount_filesystem with name={name}")
    try:
        return await mount_filesystem_api(
            name=name, mount_data=mount_data, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to mount filesystem {name}: {str(e)}")
        raise


@mcp.tool()
async def unmount_filesystem(
    ctx: Context,
    name: str,
    unmount_data: Optional[dict] = None,
    domain: Optional[str] = None,
) -> Any:
    """Unmount a filesystem from one or more nodes.

    Args:
        name: Filesystem name
        unmount_data: Unmount parameters, e.g. {"force": ...,
            "target_nodes": [...]}
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: unmount_filesystem with name={name}")
    try:
        return await unmount_filesystem_api(
            name=name, unmount_data=unmount_data, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to unmount filesystem {name}: {str(e)}")
        raise


@mcp.tool()
async def mount_all_filesystems(
    ctx: Context,
    mount_data: Optional[dict] = None,
    domain: Optional[str] = None,
) -> Any:
    """Mount all existing filesystems.

    Args:
        mount_data: Mount parameters, e.g. {"mount_options": ...,
            "target_nodes": [...]}
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: mount_all_filesystems")
    try:
        return await mount_all_filesystems_api(mount_data=mount_data, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to mount all filesystems: {str(e)}")
        raise


@mcp.tool()
async def unmount_all_filesystems(
    ctx: Context,
    unmount_data: Optional[dict] = None,
    domain: Optional[str] = None,
) -> Any:
    """Unmount all filesystems on one or more nodes.

    Args:
        unmount_data: Unmount parameters, e.g. {"force": ...,
            "target_nodes": [...]}
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: unmount_all_filesystems")
    try:
        return await unmount_all_filesystems_api(
            unmount_data=unmount_data, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to unmount all filesystems: {str(e)}")
        raise


@mcp.tool()
async def rebalance_filesystem(
    ctx: Context,
    filesystem: str,
    rebalance_strategy: Optional[str] = None,
    metadata_only: Optional[bool] = None,
    target_nodes: Optional[str] = None,
    pit_continue_on_error: Optional[bool] = None,
    qos_class: Optional[str] = None,
    domain: Optional[str] = None,
) -> Any:
    """Rebalance the filesystem by distributing file blocks evenly across disks.

    Args:
        filesystem: Filesystem name
        rebalance_strategy: Rebalance strategy ('strict', 'no_rebalance',
            'default')
        metadata_only: Limit the operation to metadata blocks
        target_nodes: Target nodes (node numbers, ranges, names, IPs, classes)
        pit_continue_on_error: Continue repairing remaining files on PIT errors
        qos_class: Quality of service class for IO operations
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: rebalance_filesystem with filesystem={filesystem}")
    try:
        return await rebalance_filesystem_api(
            filesystem=filesystem,
            rebalance_strategy=rebalance_strategy,
            metadata_only=metadata_only,
            target_nodes=target_nodes,
            pit_continue_on_error=pit_continue_on_error,
            qos_class=qos_class,
            domain=domain,
        )
    except Exception as e:
        await ctx.error(f"Failed to rebalance filesystem {filesystem}: {str(e)}")
        raise


@mcp.tool()
async def restripe_filesystem(
    ctx: Context,
    filesystem: str,
    restripe_operation: Optional[str] = None,
    metadata_only: Optional[bool] = None,
    target_nodes: Optional[str] = None,
    pit_continue_on_error: Optional[bool] = None,
    qos_class: Optional[str] = None,
    domain: Optional[str] = None,
) -> Any:
    """Restripe the filesystem, restoring replication of all files.

    Args:
        filesystem: Filesystem name
        restripe_operation: Restripe operation strategy
        metadata_only: Limit the operation to metadata blocks
        target_nodes: Target nodes (node numbers, ranges, names, IPs, classes)
        pit_continue_on_error: Continue repairing remaining files on PIT errors
        qos_class: Quality of service class for IO operations
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: restripe_filesystem with filesystem={filesystem}")
    try:
        return await restripe_filesystem_api(
            filesystem=filesystem,
            restripe_operation=restripe_operation,
            metadata_only=metadata_only,
            target_nodes=target_nodes,
            pit_continue_on_error=pit_continue_on_error,
            qos_class=qos_class,
            domain=domain,
        )
    except Exception as e:
        await ctx.error(f"Failed to restripe filesystem {filesystem}: {str(e)}")
        raise


@mcp.tool()
async def list_directory(
    ctx: Context,
    filesystem: str,
    dirpath: str,
    page_size: Optional[int] = None,
    page_token: Optional[str] = None,
    domain: Optional[str] = None,
) -> Any:
    """Get information about the contents of a filesystem directory.

    Args:
        filesystem: Filesystem name
        dirpath: Path of the filesystem directory
        page_size: Number of items to return per request
        page_token: Token to navigate to the next page
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(
        f"Tool called: list_directory with filesystem={filesystem}, dirpath={dirpath}"
    )
    try:
        return await list_directory_api(
            filesystem=filesystem,
            dirpath=dirpath,
            page_size=page_size,
            page_token=page_token,
            domain=domain,
        )
    except Exception as e:
        await ctx.error(f"Failed to list directory {dirpath}: {str(e)}")
        raise


@mcp.tool()
async def stat_directory(
    ctx: Context,
    filesystem: str,
    dirpath: str,
    domain: Optional[str] = None,
) -> Any:
    """Get detailed information (stat) of a filesystem directory.

    Args:
        filesystem: Filesystem name
        dirpath: Path of the filesystem directory
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(
        f"Tool called: stat_directory with filesystem={filesystem}, dirpath={dirpath}"
    )
    try:
        return await stat_directory_api(
            filesystem=filesystem, dirpath=dirpath, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to stat directory {dirpath}: {str(e)}")
        raise


@mcp.tool()
async def create_directory(
    ctx: Context,
    filesystem: str,
    dirpath: str,
    directory_data: Optional[dict] = None,
    domain: Optional[str] = None,
) -> Any:
    """Create a filesystem directory.

    Args:
        filesystem: Filesystem name
        dirpath: Path of the filesystem directory to create
        directory_data: Directory creation parameters
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(
        f"Tool called: create_directory with filesystem={filesystem}, dirpath={dirpath}"
    )
    try:
        return await create_directory_api(
            filesystem=filesystem,
            dirpath=dirpath,
            directory_data=directory_data,
            domain=domain,
        )
    except Exception as e:
        await ctx.error(f"Failed to create directory {dirpath}: {str(e)}")
        raise


@mcp.tool()
async def delete_directory(
    ctx: Context,
    filesystem: str,
    dirpath: str,
    force: Optional[bool] = None,
    domain: Optional[str] = None,
) -> Any:
    """Delete a directory from a mounted filesystem.

    Args:
        filesystem: Filesystem name
        dirpath: Path of the filesystem directory to delete
        force: Forcefully delete the directory even if it is not empty
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(
        f"Tool called: delete_directory with filesystem={filesystem}, dirpath={dirpath}"
    )
    try:
        return await delete_directory_api(
            filesystem=filesystem, dirpath=dirpath, force=force, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to delete directory {dirpath}: {str(e)}")
        raise
