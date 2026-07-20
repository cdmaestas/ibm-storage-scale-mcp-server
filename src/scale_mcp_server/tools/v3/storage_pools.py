"""IBM Storage Scale Storage Pool Management MCP Server."""

from typing import Any

from fastmcp import Context, FastMCP

from scale_mcp_server.api.v3.storage_pools import (
    get_storage_pool_api,
    list_storage_pools_api,
    update_storage_pool_api,
)

# Create the storage_pools MCP server
mcp = FastMCP("storage_pools", instructions="Storage pool management operations")


@mcp.tool()
async def list_storage_pools(
    ctx: Context,
    filesystem: str,
    page_size: int | None = None,
    page_token: str | None = None,
    domain: str | None = None,
) -> Any:
    """List storage pools for a filesystem.

    Args:
        filesystem: Filesystem name
        page_size: Number of items to return per request
        page_token: Token to navigate to the next page
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: list_storage_pools with filesystem={filesystem}")
    try:
        return await list_storage_pools_api(
            filesystem=filesystem,
            page_size=page_size,
            page_token=page_token,
            domain=domain,
        )
    except Exception as e:
        await ctx.error(f"Failed to list storage pools for {filesystem}: {str(e)}")
        raise


@mcp.tool()
async def get_storage_pool(
    ctx: Context,
    filesystem: str,
    pool_name: str,
    domain: str | None = None,
) -> Any:
    """Get information about a specific storage pool.

    Args:
        filesystem: Filesystem name
        pool_name: Storage pool name
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: get_storage_pool with filesystem={filesystem}, pool_name={pool_name}")
    try:
        return await get_storage_pool_api(filesystem=filesystem, pool_name=pool_name, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to get storage pool {pool_name}: {str(e)}")
        raise


@mcp.tool()
async def update_storage_pool(
    ctx: Context,
    filesystem: str,
    pool_name: str,
    pool_data: dict,
    domain: str | None = None,
) -> Any:
    """Update an existing storage pool of a filesystem.

    Args:
        filesystem: Filesystem name
        pool_name: Storage pool name
        pool_data: Updated storage pool definition
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: update_storage_pool with filesystem={filesystem}, pool_name={pool_name}")
    try:
        return await update_storage_pool_api(
            filesystem=filesystem,
            pool_name=pool_name,
            pool_data=pool_data,
            domain=domain,
        )
    except Exception as e:
        await ctx.error(f"Failed to update storage pool {pool_name}: {str(e)}")
        raise
