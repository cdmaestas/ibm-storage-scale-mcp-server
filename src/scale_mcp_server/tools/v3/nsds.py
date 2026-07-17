"""IBM Storage Scale NSD Management MCP Server."""

from typing import Any

from fastmcp import Context, FastMCP

from scale_mcp_server.api.v3.nsds import (
    batch_create_nsds_api,
    batch_delete_nsds_api,
    create_nsd_api,
    delete_nsd_api,
    get_nsd_api,
    list_nsds_api,
    update_nsd_api,
)

# Create the nsds MCP server
mcp = FastMCP("nsds", instructions="NSD management operations")


@mcp.tool()
async def list_nsds(
    ctx: Context,
    not_assigned: bool | None = None,
    filesystem_device: str | None = None,
    view: str | None = None,
    page_size: int | None = None,
    page_token: str | None = None,
    domain: str | None = None,
) -> Any:
    """List all NSDs (Network Shared Disks).

    Args:
        not_assigned: List all disks that do not belong to any file system
        filesystem_device: List all disks of the specified file system device
        view: View for NSD content (local-node, all-nodes, all-nsds, long,
            extended)
        page_size: Number of items to return per request
        page_token: Token to navigate to the next page
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: list_nsds")
    try:
        return await list_nsds_api(
            not_assigned=not_assigned,
            filesystem_device=filesystem_device,
            view=view,
            page_size=page_size,
            page_token=page_token,
            domain=domain,
        )
    except Exception as e:
        await ctx.error(f"Failed to list NSDs: {str(e)}")
        raise


@mcp.tool()
async def get_nsd(
    ctx: Context,
    nsd_name: str,
    view: str | None = None,
    domain: str | None = None,
) -> Any:
    """Get information about a specific NSD.

    Args:
        nsd_name: NSD name
        view: View for NSD content (local-node, all-nodes, all-nsds, long,
            extended)
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: get_nsd with nsd_name={nsd_name}")
    try:
        return await get_nsd_api(nsd_name=nsd_name, view=view, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to get NSD {nsd_name}: {str(e)}")
        raise


@mcp.tool()
async def create_nsd(
    ctx: Context,
    nsd_data: dict,
    no_verify: bool | None = None,
    domain: str | None = None,
) -> Any:
    """Create an NSD in the cluster.

    Args:
        nsd_data: NSD definition
        no_verify: Do not verify that the physical disk is unused
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: create_nsd")
    try:
        return await create_nsd_api(nsd_data=nsd_data, no_verify=no_verify, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to create NSD: {str(e)}")
        raise


@mcp.tool()
async def update_nsd(
    ctx: Context,
    nsd_name: str,
    nsd_data: dict,
    domain: str | None = None,
) -> Any:
    """Update an existing NSD (for example, the assigned NSD servers).

    Args:
        nsd_name: NSD name
        nsd_data: Updated NSD definition
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: update_nsd with nsd_name={nsd_name}")
    try:
        return await update_nsd_api(nsd_name=nsd_name, nsd_data=nsd_data, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to update NSD {nsd_name}: {str(e)}")
        raise


@mcp.tool()
async def delete_nsd(
    ctx: Context,
    nsd_name: str,
    domain: str | None = None,
) -> Any:
    """Delete an existing NSD.

    Args:
        nsd_name: NSD name
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: delete_nsd with nsd_name={nsd_name}")
    try:
        return await delete_nsd_api(nsd_name=nsd_name, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to delete NSD {nsd_name}: {str(e)}")
        raise


@mcp.tool()
async def batch_create_nsds(
    ctx: Context,
    nsds_data: dict,
    domain: str | None = None,
) -> Any:
    """Create one or more NSDs (LRO).

    Args:
        nsds_data: Batch NSD definitions
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: batch_create_nsds")
    try:
        return await batch_create_nsds_api(nsds_data=nsds_data, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to batch create NSDs: {str(e)}")
        raise


@mcp.tool()
async def batch_delete_nsds(
    ctx: Context,
    nsds_data: dict,
    domain: str | None = None,
) -> Any:
    """Delete one or more NSDs (LRO).

    Args:
        nsds_data: Batch NSD deletion parameters
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: batch_delete_nsds")
    try:
        return await batch_delete_nsds_api(nsds_data=nsds_data, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to batch delete NSDs: {str(e)}")
        raise
