"""IBM Storage Scale Node Classes MCP Server.

Node class tools for creating and managing user-defined node classes.
"""

from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v3.node_classes import (
    list_node_classes_api,
    get_node_class_api,
    create_node_class_api,
    update_node_class_api,
    delete_node_class_api,
)

# Create the node_classes MCP server
mcp = FastMCP("node_classes", instructions="Node class management operations")


@mcp.tool()
async def list_node_classes(
    ctx: Context,
    page_size: Optional[int] = None,
    page_token: Optional[str] = None,
    domain: Optional[str] = None,
) -> Any:
    """List all node classes registered to the cluster.

    Args:
        page_size: Number of items to return per request
        page_token: Token to navigate to the next page
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: list_node_classes")
    try:
        return await list_node_classes_api(
            page_size=page_size, page_token=page_token, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to list node classes: {str(e)}")
        raise


@mcp.tool()
async def get_node_class(
    ctx: Context,
    node_class: str,
    domain: Optional[str] = None,
) -> Any:
    """List the members of the specified node class.

    Args:
        node_class: Node class name
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: get_node_class with node_class={node_class}")
    try:
        return await get_node_class_api(node_class=node_class, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to get node class {node_class}: {str(e)}")
        raise


@mcp.tool()
async def create_node_class(
    ctx: Context,
    nodeclass_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Create a user-defined node class.

    Args:
        nodeclass_data: Node class definition, e.g.
            {"name": ..., "members": [...], "subclasses": [...]}
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: create_node_class")
    try:
        return await create_node_class_api(
            nodeclass_data=nodeclass_data, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to create node class: {str(e)}")
        raise


@mcp.tool()
async def update_node_class(
    ctx: Context,
    node_class: str,
    nodeclass_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Update an existing node class.

    Args:
        node_class: Node class name
        nodeclass_data: Updated node class definition
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: update_node_class with node_class={node_class}")
    try:
        return await update_node_class_api(
            node_class=node_class, nodeclass_data=nodeclass_data, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to update node class {node_class}: {str(e)}")
        raise


@mcp.tool()
async def delete_node_class(
    ctx: Context,
    node_class: str,
    domain: Optional[str] = None,
) -> Any:
    """Delete an existing node class.

    Args:
        node_class: Node class name
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: delete_node_class with node_class={node_class}")
    try:
        return await delete_node_class_api(node_class=node_class, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to delete node class {node_class}: {str(e)}")
        raise
