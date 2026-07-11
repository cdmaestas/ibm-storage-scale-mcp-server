"""IBM Storage Scale Node Management MCP Server.

Node tools for adding nodes, starting/stopping mmfsd, and node status.
"""

from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v3.nodes import (
    add_node_api,
    batch_add_nodes_api,
    start_nodes_api,
    stop_nodes_api,
    get_nodes_status_api,
    get_nodes_config_api,
)

# Create the nodes MCP server
mcp = FastMCP("nodes", instructions="Node management operations")


@mcp.tool()
async def add_node(
    ctx: Context,
    node_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Add a node to the IBM Storage Scale cluster.

    Args:
        node_data: Node definition (see scalectl node command)
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: add_node")
    try:
        return await add_node_api(node_data=node_data, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to add node: {str(e)}")
        raise


@mcp.tool()
async def batch_add_nodes(
    ctx: Context,
    nodes_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Add one or more nodes to the IBM Storage Scale cluster.

    Args:
        nodes_data: Batch definition, e.g. {"accept_all": true, "nodes": [...]}
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: batch_add_nodes")
    try:
        return await batch_add_nodes_api(nodes_data=nodes_data, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to batch add nodes: {str(e)}")
        raise


@mcp.tool()
async def start_nodes(
    ctx: Context,
    start_data: Optional[dict] = None,
    domain: Optional[str] = None,
) -> Any:
    """Start the mmfsd service on one or more nodes.

    Args:
        start_data: Start parameters (see scalectl node command)
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: start_nodes")
    try:
        return await start_nodes_api(start_data=start_data, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to start nodes: {str(e)}")
        raise


@mcp.tool()
async def stop_nodes(
    ctx: Context,
    stop_data: Optional[dict] = None,
    domain: Optional[str] = None,
) -> Any:
    """Stop the mmfsd service on one or more nodes.

    Args:
        stop_data: Stop parameters (see scalectl node command)
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: stop_nodes")
    try:
        return await stop_nodes_api(stop_data=stop_data, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to stop nodes: {str(e)}")
        raise


@mcp.tool()
async def get_nodes_status(
    ctx: Context,
    target_nodes: Optional[str] = None,
    domain: Optional[str] = None,
) -> Any:
    """Check the mmfsd status of cluster nodes.

    Args:
        target_nodes: Target nodes (node numbers, ranges, names, IPs, classes)
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: get_nodes_status")
    try:
        return await get_nodes_status_api(target_nodes=target_nodes, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to get nodes status: {str(e)}")
        raise


@mcp.tool()
async def get_nodes_config(
    ctx: Context,
    domain: Optional[str] = None,
) -> Any:
    """List the configuration details about the node.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: get_nodes_config")
    try:
        return await get_nodes_config_api(domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to get nodes config: {str(e)}")
        raise
