"""IBM Storage Scale Filesystem Health Management MCP Server (v2 API).

DEPRECATION NOTICE:
This module uses the v2 API which is deprecated. Please migrate to the v3 API
health monitoring tools in scale_mcp_server.tools.v3.health module.

The v3 API provides health information through:
- get_filesystem_health() - Replaces get_filesystem_health_states() and get_filesystem_health_events()
- get_cluster_health_summary() - Provides comprehensive cluster health overview
"""

import warnings
from typing import Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v2.filesystems import (
    get_filesystem_health_states_api,
    get_filesystem_health_events_api,
)

# Create the filesystems health MCP server
mcp = FastMCP(
    "filesystems_health_v2",
    instructions="Filesystem health monitoring operations (v2 API)",
)


@mcp.tool()
async def get_filesystem_health_states(
    ctx: Context,
    filesystem: str,
) -> Any:
    """Get Cluster Related health State for a filesystem.

    DEPRECATED: This tool uses the v2 API. Please use get_filesystem_health() from
    the health_v3 module instead, which provides equivalent functionality using v3 API.

    Returns the health state for the specified filesystem.

    Args:
        filesystem: Filesystem name

    Returns:
        Dictionary containing filesystem health state information
    """
    warnings.warn(
        "get_filesystem_health_states is deprecated. Use get_filesystem_health from health_v3 module.",
        DeprecationWarning,
        stacklevel=2,
    )
    await ctx.info(
        f"Tool called: get_filesystem_health_states for filesystem: {filesystem}"
    )
    await ctx.debug(f"Retrieving health states for filesystem: {filesystem}")

    try:
        result = await get_filesystem_health_states_api(filesystem=filesystem)
        await ctx.info(
            f"Successfully retrieved health states for filesystem: {filesystem}"
        )
        return result
    except Exception as e:
        await ctx.error(
            f"Failed to get health states for filesystem {filesystem}: {str(e)}"
        )
        raise


@mcp.tool()
async def get_filesystem_health_events(
    ctx: Context,
    filesystem_name: str,
) -> Any:
    """Get Cluster Related System Health events for a filesystem.

    DEPRECATED: This tool uses the v2 API. Please use get_filesystem_health() from
    the health_v3 module instead, which provides equivalent functionality using v3 API.

    Returns a list of currently active Cluster related System Health events for the specified filesystem.

    Args:
        filesystem_name: Filesystem name

    Returns:
        Dictionary containing filesystem health events information
    """
    warnings.warn(
        "get_filesystem_health_events is deprecated. Use get_filesystem_health from health_v3 module.",
        DeprecationWarning,
        stacklevel=2,
    )
    await ctx.info(
        f"Tool called: get_filesystem_health_events for filesystem: {filesystem_name}"
    )
    await ctx.debug(f"Retrieving health events for filesystem: {filesystem_name}")

    try:
        result = await get_filesystem_health_events_api(filesystem_name=filesystem_name)
        await ctx.info(
            f"Successfully retrieved health events for filesystem: {filesystem_name}"
        )
        return result
    except Exception as e:
        await ctx.error(
            f"Failed to get health events for filesystem {filesystem_name}: {str(e)}"
        )
        raise
