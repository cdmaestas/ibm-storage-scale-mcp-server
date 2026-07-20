"""IBM Storage Scale Remote Clusters MCP Server.

Remote cluster tools for managing owning/accessing cluster relationships.
"""

from typing import Any

from fastmcp import Context, FastMCP

from scale_mcp_server.api.v3.remote_clusters import (
    add_remote_cluster_api,
    authorize_remote_cluster_api,
    deauthorize_remote_cluster_api,
    delete_remote_cluster_api,
    get_remote_cluster_api,
    list_remote_clusters_api,
    refresh_remote_cluster_api,
    update_remote_cluster_api,
)

# Create the remote_clusters MCP server
mcp = FastMCP("remote_clusters", instructions="Remote cluster management operations")


@mcp.tool()
async def list_remote_clusters(
    ctx: Context,
    page_size: int | None = None,
    page_token: str | None = None,
    view: str | None = None,
    domain: str | None = None,
) -> Any:
    """List remote clusters known to the accessing cluster.

    Args:
        page_size: Number of items to return per request
        page_token: Token to navigate to the next page
        view: View for remote cluster contents ('basic' or 'full')
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: list_remote_clusters")
    try:
        return await list_remote_clusters_api(page_size=page_size, page_token=page_token, view=view, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to list remote clusters: {str(e)}")
        raise


@mcp.tool()
async def get_remote_cluster(
    ctx: Context,
    name: str,
    view: str | None = None,
    domain: str | None = None,
) -> Any:
    """Retrieve details about a remote cluster.

    Args:
        name: Remote cluster name
        view: View for remote cluster contents ('basic' or 'full')
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: get_remote_cluster with name={name}")
    try:
        return await get_remote_cluster_api(name=name, view=view, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to get remote cluster {name}: {str(e)}")
        raise


@mcp.tool()
async def add_remote_cluster(
    ctx: Context,
    remote_cluster: dict,
    domain: str | None = None,
) -> Any:
    """Add an owning cluster to the set of remote clusters known to this cluster.

    Args:
        remote_cluster: Remote cluster definition; required parameters are
            'name' and 'contact-nodes'
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: add_remote_cluster")
    try:
        return await add_remote_cluster_api(remote_cluster=remote_cluster, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to add remote cluster: {str(e)}")
        raise


@mcp.tool()
async def update_remote_cluster(
    ctx: Context,
    name: str,
    remote_cluster: dict,
    resource_update: bool | None = None,
    domain: str | None = None,
) -> Any:
    """Update information associated with a remote cluster.

    Args:
        name: Remote cluster name
        remote_cluster: Updated remote cluster definition
        resource_update: Update the resource authorization information
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: update_remote_cluster with name={name}")
    try:
        return await update_remote_cluster_api(
            name=name,
            remote_cluster=remote_cluster,
            resource_update=resource_update,
            domain=domain,
        )
    except Exception as e:
        await ctx.error(f"Failed to update remote cluster {name}: {str(e)}")
        raise


@mcp.tool()
async def delete_remote_cluster(
    ctx: Context,
    name: str,
    force: bool | None = None,
    domain: str | None = None,
) -> Any:
    """Delete an owning cluster definition from the accessing cluster.

    Args:
        name: Remote cluster name
        force: Force deletion of the owning cluster definition
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: delete_remote_cluster with name={name}")
    try:
        return await delete_remote_cluster_api(name=name, force=force, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to delete remote cluster {name}: {str(e)}")
        raise


@mcp.tool()
async def authorize_remote_cluster(
    ctx: Context,
    authorization: dict,
    domain: str | None = None,
) -> Any:
    """Authorize an accessing cluster to access resources on the owning cluster.

    Args:
        authorization: Authorization definition; required parameter is 'name'.
            If filesystem_resources or fileset_resources are provided,
            disposition 'GRANT' is required.
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: authorize_remote_cluster")
    try:
        return await authorize_remote_cluster_api(authorization=authorization, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to authorize remote cluster: {str(e)}")
        raise


@mcp.tool()
async def deauthorize_remote_cluster(
    ctx: Context,
    name: str,
    domain: str | None = None,
) -> Any:
    """Delete the authorization of an accessing cluster on the owning cluster.

    Args:
        name: Remote cluster name
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: deauthorize_remote_cluster with name={name}")
    try:
        return await deauthorize_remote_cluster_api(name=name, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to deauthorize remote cluster {name}: {str(e)}")
        raise


@mcp.tool()
async def refresh_remote_cluster(
    ctx: Context,
    name: str,
    domain: str | None = None,
) -> Any:
    """Refresh the information of an owning cluster on the accessing cluster.

    Args:
        name: Remote cluster name
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: refresh_remote_cluster with name={name}")
    try:
        return await refresh_remote_cluster_api(name=name, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to refresh remote cluster {name}: {str(e)}")
        raise
