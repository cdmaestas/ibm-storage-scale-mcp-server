"""IBM Storage Scale Remote Clusters MCP Server.

Remote cluster management tools for multi-cluster configurations and operations.
"""

from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v3.remote_clusters import (
    list_remote_clusters_api,
    get_remote_cluster_api,
    add_remote_cluster_api,
    update_remote_cluster_api,
    delete_remote_cluster_api,
    list_remote_filesystems_api,
    get_remote_filesystem_api,
)

# Create the remote clusters MCP server
mcp = FastMCP(
    "remote_clusters",
    instructions="Remote cluster and filesystem management operations",
)


@mcp.tool()
async def list_remote_clusters(
    ctx: Context,
    domain: Optional[str] = None,
) -> Any:
    """List all remote clusters.

    Retrieves a list of all remote clusters configured in the system.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing list of remote clusters
    """
    await ctx.info("Tool called: list_remote_clusters")
    await ctx.debug("Retrieving list of remote clusters")

    try:
        result = await list_remote_clusters_api(domain=domain)
        await ctx.info("Successfully retrieved remote clusters list")
        return result
    except Exception as e:
        await ctx.error(f"Failed to list remote clusters: {str(e)}")
        raise


@mcp.tool()
async def get_remote_cluster(
    ctx: Context,
    cluster: str,
    domain: Optional[str] = None,
) -> Any:
    """Get details of a specific remote cluster.

    Retrieves detailed information about a specific remote cluster.

    Args:
        cluster: Remote cluster name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing remote cluster details
    """
    await ctx.info(f"Tool called: get_remote_cluster for: {cluster}")
    await ctx.debug(f"Retrieving details for remote cluster: {cluster}")

    try:
        result = await get_remote_cluster_api(cluster=cluster, domain=domain)
        await ctx.info(f"Successfully retrieved remote cluster: {cluster}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to get remote cluster {cluster}: {str(e)}")
        raise


@mcp.tool()
async def add_remote_cluster(
    ctx: Context,
    cluster_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Add a new remote cluster.

    Adds a new remote cluster configuration.

    Args:
        cluster_data: Remote cluster configuration data
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing operation status
    """
    cluster_name = cluster_data.get("name", "unknown")
    await ctx.info(f"Tool called: add_remote_cluster for: {cluster_name}")
    await ctx.debug(f"Adding remote cluster: {cluster_name}")

    try:
        result = await add_remote_cluster_api(cluster_data=cluster_data, domain=domain)
        await ctx.info(f"Successfully added remote cluster: {cluster_name}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to add remote cluster {cluster_name}: {str(e)}")
        raise


@mcp.tool()
async def update_remote_cluster(
    ctx: Context,
    cluster: str,
    cluster_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Update remote cluster configuration.

    Updates the configuration of a specific remote cluster.

    Args:
        cluster: Remote cluster name
        cluster_data: Updated cluster configuration data
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing update status
    """
    await ctx.info(f"Tool called: update_remote_cluster for: {cluster}")
    await ctx.debug(f"Updating remote cluster: {cluster}")

    try:
        result = await update_remote_cluster_api(
            cluster=cluster, cluster_data=cluster_data, domain=domain
        )
        await ctx.info(f"Successfully updated remote cluster: {cluster}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to update remote cluster {cluster}: {str(e)}")
        raise


@mcp.tool()
async def delete_remote_cluster(
    ctx: Context,
    cluster: str,
    domain: Optional[str] = None,
) -> Any:
    """Delete a remote cluster.

    Removes the specified remote cluster configuration.

    Args:
        cluster: Remote cluster name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing deletion status
    """
    await ctx.info(f"Tool called: delete_remote_cluster for: {cluster}")
    await ctx.debug(f"Deleting remote cluster: {cluster}")

    try:
        result = await delete_remote_cluster_api(cluster=cluster, domain=domain)
        await ctx.info(f"Successfully deleted remote cluster: {cluster}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to delete remote cluster {cluster}: {str(e)}")
        raise


@mcp.tool()
async def list_remote_filesystems(
    ctx: Context,
    cluster: str,
    domain: Optional[str] = None,
) -> Any:
    """List filesystems on a remote cluster.

    Retrieves a list of filesystems available on the specified remote cluster.

    Args:
        cluster: Remote cluster name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing list of remote filesystems
    """
    await ctx.info(f"Tool called: list_remote_filesystems for cluster: {cluster}")
    await ctx.debug(f"Listing filesystems on remote cluster: {cluster}")

    try:
        result = await list_remote_filesystems_api(cluster=cluster, domain=domain)
        await ctx.info(
            f"Successfully listed filesystems on remote cluster: {cluster}"
        )
        return result
    except Exception as e:
        await ctx.error(
            f"Failed to list filesystems on remote cluster {cluster}: {str(e)}"
        )
        raise


@mcp.tool()
async def get_remote_filesystem(
    ctx: Context,
    cluster: str,
    filesystem: str,
    domain: Optional[str] = None,
) -> Any:
    """Get details of a filesystem on a remote cluster.

    Retrieves detailed information about a specific filesystem on a remote cluster.

    Args:
        cluster: Remote cluster name
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing remote filesystem details
    """
    await ctx.info(
        f"Tool called: get_remote_filesystem for: {cluster}/{filesystem}"
    )
    await ctx.debug(f"Retrieving filesystem {filesystem} on remote cluster {cluster}")

    try:
        result = await get_remote_filesystem_api(
            cluster=cluster, filesystem=filesystem, domain=domain
        )
        await ctx.info(
            f"Successfully retrieved filesystem {filesystem} on remote cluster {cluster}"
        )
        return result
    except Exception as e:
        await ctx.error(
            f"Failed to get filesystem {filesystem} on remote cluster {cluster}: {str(e)}"
        )
        raise
