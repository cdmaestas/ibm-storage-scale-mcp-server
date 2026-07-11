"""IBM Storage Scale Troubleshooting MCP Server.

Troubleshooting tools for clearing NSD volume IDs and persistent reserve keys.
"""

from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v3.troubleshooting import (
    clear_nsd_id_api,
    get_persistent_reserve_keys_api,
    clear_persistent_reserve_keys_api,
)

# Create the troubleshooting MCP server
mcp = FastMCP("troubleshooting", instructions="Troubleshooting and recovery operations")


@mcp.tool()
async def clear_nsd_id(
    ctx: Context,
    id: str,
    node_name: Optional[str] = None,
    domain: Optional[str] = None,
) -> Any:
    """Delete the NSD volume ID from a device.

    Args:
        id: NSD volume ID to clear
        node_name: Node directly attached to the disk holding the NSD volume ID
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: clear_nsd_id with id={id}")
    try:
        return await clear_nsd_id_api(id=id, node_name=node_name, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to clear NSD volume ID {id}: {str(e)}")
        raise


@mcp.tool()
async def get_persistent_reserve_keys(
    ctx: Context,
    device: str,
    node_name: Optional[str] = None,
    domain: Optional[str] = None,
) -> Any:
    """Get persistent reserve registration key values from a device.

    Args:
        device: Device name
        node_name: Node directly attached to the device to read
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: get_persistent_reserve_keys with device={device}")
    try:
        return await get_persistent_reserve_keys_api(
            device=device, node_name=node_name, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to get persistent reserve keys for {device}: {str(e)}")
        raise


@mcp.tool()
async def clear_persistent_reserve_keys(
    ctx: Context,
    device: str,
    key: Optional[str] = None,
    node_name: Optional[str] = None,
    force: Optional[bool] = None,
    domain: Optional[str] = None,
) -> Any:
    """Delete the persistent reserve registration key from a device.

    Args:
        device: Device name
        key: Persistent reserve key used to clear the keys; defaults to the
            IBM persistent reserve key
        node_name: Node where the device is attached
        force: Override clearing keys not created by IBM Storage Scale
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: clear_persistent_reserve_keys with device={device}")
    try:
        return await clear_persistent_reserve_keys_api(
            device=device, key=key, node_name=node_name, force=force, domain=domain
        )
    except Exception as e:
        await ctx.error(
            f"Failed to clear persistent reserve keys for {device}: {str(e)}"
        )
        raise
