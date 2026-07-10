"""IBM Storage Scale Node Health Management MCP Server (v2 API).

DEPRECATION NOTICE:
This module uses the v2 API which is deprecated. Please migrate to the v3 API
health monitoring tools in scale_mcp_server.tools.v3.health module.

The v3 API provides health information through:
- get_node_health() - Replaces get_node_health_states() and get_node_health_events()
- get_node_diagnostics() - Provides detailed node diagnostics
- get_cluster_health_summary() - Provides comprehensive cluster health overview
"""

import warnings
from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v2.nodes import (
    get_node_health_states_api,
    get_node_health_events_api,
)

# Create the nodes health MCP server
mcp = FastMCP(
    "nodes_health_v2", instructions="Node health monitoring operations (v2 API)"
)


@mcp.tool()
async def get_node_health_states(
    ctx: Context,
    name: str,
    fields: Optional[str] = None,
    filter: Optional[str] = None,
) -> Any:
    """Get System Health states for a node or nodeclass.

    DEPRECATED: This tool uses the v2 API. Please use get_node_health() from
    the health_v3 module instead, which provides equivalent functionality using v3 API.

    Returns a list of currently active System Health states for the given node or nodeclass.

    Args:
        name: Nodeclass, node name or ':all:'
        fields: Comma separated list of fields to be included in response. ':all:' selects all available fields
        filter: Filter objects by expression, e.g. 'status=HEALTHY,entityType=FILESET'

    Returns:
        Dictionary containing system health states information
    """
    warnings.warn(
        "get_node_health_states is deprecated. Use get_node_health from health_v3 module.",
        DeprecationWarning,
        stacklevel=2,
    )
    await ctx.info(f"Tool called: get_node_health_states for node: {name}")
    await ctx.debug(f"Retrieving health states for node: {name}")

    try:
        result = await get_node_health_states_api(
            name=name, fields=fields, filter=filter
        )
        await ctx.info(f"Successfully retrieved health states for node: {name}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to get health states for node {name}: {str(e)}")
        raise


@mcp.tool()
async def get_node_health_events(
    ctx: Context,
    name: str,
    fields: Optional[str] = None,
    filter: Optional[str] = None,
) -> Any:
    """Get System Health events for a node or nodeclass.

    DEPRECATED: This tool uses the v2 API. Please use get_node_health() from
    the health_v3 module instead, which provides equivalent functionality using v3 API.

    Returns a list of currently active System Health events for the given node or nodeclass.

    Args:
        name: Nodeclass, node name or ':all:'
        fields: Comma separated list of fields to be included in response. ':all:' selects all available fields
        filter: Filter objects by expression, e.g. 'status=HEALTHY,entityType=FILESET'

    Returns:
        Dictionary containing system health events information
    """
    warnings.warn(
        "get_node_health_events is deprecated. Use get_node_health from health_v3 module.",
        DeprecationWarning,
        stacklevel=2,
    )
    await ctx.info(f"Tool called: get_node_health_events for node: {name}")
    await ctx.debug(f"Retrieving health events for node: {name}")

    try:
        result = await get_node_health_events_api(
            name=name, fields=fields, filter=filter
        )
        await ctx.info(f"Successfully retrieved health events for node: {name}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to get health events for node {name}: {str(e)}")
        raise
