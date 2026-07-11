"""IBM Storage Scale XCP MCP Server.

Parallel copy (XCP) tools for copying, synchronizing, and verifying files
within a single IBM Storage Scale cluster.
"""

from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v3.xcp import (
    list_xcp_operations_api,
    get_xcp_operation_api,
    get_xcp_config_api,
    update_xcp_config_api,
    enable_xcp_copy_api,
    sync_xcp_api,
    verify_xcp_api,
)

# Create the xcp MCP server
mcp = FastMCP("xcp", instructions="XCP parallel copy operations")


@mcp.tool()
async def list_xcp_operations(
    ctx: Context,
    domain: Optional[str] = None,
) -> Any:
    """List configuration information of all currently running XCP operations.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: list_xcp_operations")
    try:
        return await list_xcp_operations_api(domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to list XCP operations: {str(e)}")
        raise


@mcp.tool()
async def get_xcp_operation(
    ctx: Context,
    id: str,
    domain: Optional[str] = None,
) -> Any:
    """Retrieve configuration information of a specific XCP operation by ID.

    Args:
        id: XCP operation ID
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: get_xcp_operation with id={id}")
    try:
        return await get_xcp_operation_api(id=id, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to get XCP operation {id}: {str(e)}")
        raise


@mcp.tool()
async def get_xcp_config(
    ctx: Context,
    domain: Optional[str] = None,
) -> Any:
    """Retrieve the current XCP configuration limits for the cluster.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: get_xcp_config")
    try:
        return await get_xcp_config_api(domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to get XCP config: {str(e)}")
        raise


@mcp.tool()
async def update_xcp_config(
    ctx: Context,
    config_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Update the XCP configuration limits for the cluster.

    Args:
        config_data: Configuration updates, e.g.
            {"updates": {"max_files": ..., "max_parallel": ..., "max_threads": ...}}
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: update_xcp_config")
    try:
        return await update_xcp_config_api(config_data=config_data, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to update XCP config: {str(e)}")
        raise


@mcp.tool()
async def start_xcp_copy(
    ctx: Context,
    copy_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Start a parallel copy of files from a source to a target in the cluster.

    Supports copying within a file system, between file systems in the same
    cluster, from live file systems, and from snapshots. Cross-cluster copy
    is not supported.

    Args:
        copy_data: Copy parameters (source, target, nodes, thread_level,
            snapshot options, etc.)
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: start_xcp_copy")
    try:
        return await enable_xcp_copy_api(copy_data=copy_data, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to start XCP copy: {str(e)}")
        raise


@mcp.tool()
async def sync_xcp(
    ctx: Context,
    sync_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Synchronize files from a source directory to a target directory.

    Copies only files that are missing or appear different.

    Args:
        sync_data: Sync parameters (source, target, snapshot options)
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: sync_xcp")
    try:
        return await sync_xcp_api(sync_data=sync_data, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to start XCP sync: {str(e)}")
        raise


@mcp.tool()
async def verify_xcp(
    ctx: Context,
    verify_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Compare metadata between a source and target of a previous XCP copy.

    Args:
        verify_data: Verify parameters (source, target, check_attributes,
            snapshot options)
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: verify_xcp")
    try:
        return await verify_xcp_api(verify_data=verify_data, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to start XCP verify: {str(e)}")
        raise
