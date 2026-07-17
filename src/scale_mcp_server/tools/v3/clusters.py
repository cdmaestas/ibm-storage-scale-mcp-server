"""IBM Storage Scale Cluster Management MCP Server.

Local cluster tools. Remote cluster tools live in remote_clusters.py.
"""

from typing import Any

from fastmcp import Context, FastMCP

from scale_mcp_server.api.v3.clusters import (
    create_cluster_api,
    list_cluster_trust_api,
    list_clusters_api,
    migrate_cluster_api,
)

# Create the clusters MCP server
mcp = FastMCP("clusters", instructions="Cluster management operations")


@mcp.tool()
async def list_clusters(
    ctx: Context,
    view: str | None = None,
    domain: str | None = None,
) -> Any:
    """List information about the local cluster.

    Args:
        view: Level of detail to return (basic, ces, cnfs, node-comments)
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: list_clusters")
    try:
        return await list_clusters_api(view=view, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to list clusters: {str(e)}")
        raise


@mcp.tool()
async def create_cluster(
    ctx: Context,
    cluster_data: dict,
    domain: str | None = None,
) -> Any:
    """Create an IBM Storage Scale cluster.

    Args:
        cluster_data: Cluster definition (see scalectl cluster command)
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: create_cluster")
    try:
        return await create_cluster_api(cluster_data=cluster_data, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to create cluster: {str(e)}")
        raise


@mcp.tool()
async def migrate_cluster(
    ctx: Context,
    precheck: bool | None = None,
    domain: str | None = None,
) -> Any:
    """Migrate a legacy cluster to the native REST API.

    Args:
        precheck: Run a cluster migration precheck only
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: migrate_cluster")
    try:
        return await migrate_cluster_api(precheck=precheck, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to migrate cluster: {str(e)}")
        raise


@mcp.tool()
async def list_cluster_trust(
    ctx: Context,
    end_point: str | None = None,
    domain: str | None = None,
) -> Any:
    """List all CA chains that are currently trusted by the local cluster.

    Args:
        end_point: Filter the results by the specified endpoint subject name
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: list_cluster_trust")
    try:
        return await list_cluster_trust_api(end_point=end_point, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to list cluster trust: {str(e)}")
        raise
