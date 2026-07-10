"""IBM Storage Scale Node Classes MCP Server.

Node class management tools for organizing and managing node classifications.
"""

from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v3.node_classes import (
    list_node_classes_api,
    get_node_class_api,
    create_node_class_api,
    update_node_class_api,
    delete_node_class_api,
    add_nodes_to_class_api,
    remove_nodes_from_class_api,
)

# Create the node classes MCP server
mcp = FastMCP(
    "node_classes",
    instructions="Node class management and organization operations",
)


@mcp.tool()
async def list_node_classes(
    ctx: Context,
    domain: Optional[str] = None,
) -> Any:
    """List all node classes.

    Retrieves a list of all node classes in the cluster.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing list of node classes
    """
    await ctx.info("Tool called: list_node_classes")
    await ctx.debug("Retrieving list of node classes")

    try:
        result = await list_node_classes_api(domain=domain)
        await ctx.info("Successfully retrieved node classes list")
        return result
    except Exception as e:
        await ctx.error(f"Failed to list node classes: {str(e)}")
        raise


@mcp.tool()
async def get_node_class(
    ctx: Context,
    node_class: str,
    domain: Optional[str] = None,
) -> Any:
    """Get details of a specific node class.

    Retrieves detailed information about a specific node class including
    its members and configuration.

    Args:
        node_class: Node class name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing node class details
    """
    await ctx.info(f"Tool called: get_node_class for: {node_class}")
    await ctx.debug(f"Retrieving details for node class: {node_class}")

    try:
        result = await get_node_class_api(node_class=node_class, domain=domain)
        await ctx.info(f"Successfully retrieved node class: {node_class}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to get node class {node_class}: {str(e)}")
        raise


@mcp.tool()
async def create_node_class(
    ctx: Context,
    node_class_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Create a new node class.

    Creates a new node class with the specified configuration.

    Args:
        node_class_data: Node class configuration data
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing creation status
    """
    node_class_name = node_class_data.get("name", "unknown")
    await ctx.info(f"Tool called: create_node_class for: {node_class_name}")
    await ctx.debug(f"Creating node class: {node_class_name}")

    try:
        result = await create_node_class_api(
            node_class_data=node_class_data, domain=domain
        )
        await ctx.info(f"Successfully created node class: {node_class_name}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to create node class {node_class_name}: {str(e)}")
        raise


@mcp.tool()
async def update_node_class(
    ctx: Context,
    node_class: str,
    node_class_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Update an existing node class.

    Updates the configuration of an existing node class.

    Args:
        node_class: Node class name
        node_class_data: Updated node class configuration data
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing update status
    """
    await ctx.info(f"Tool called: update_node_class for: {node_class}")
    await ctx.debug(f"Updating node class: {node_class}")

    try:
        result = await update_node_class_api(
            node_class=node_class, node_class_data=node_class_data, domain=domain
        )
        await ctx.info(f"Successfully updated node class: {node_class}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to update node class {node_class}: {str(e)}")
        raise


@mcp.tool()
async def delete_node_class(
    ctx: Context,
    node_class: str,
    domain: Optional[str] = None,
) -> Any:
    """Delete a node class.

    Deletes the specified node class from the cluster.

    Args:
        node_class: Node class name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing deletion status
    """
    await ctx.info(f"Tool called: delete_node_class for: {node_class}")
    await ctx.debug(f"Deleting node class: {node_class}")

    try:
        result = await delete_node_class_api(node_class=node_class, domain=domain)
        await ctx.info(f"Successfully deleted node class: {node_class}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to delete node class {node_class}: {str(e)}")
        raise


@mcp.tool()
async def add_nodes_to_class(
    ctx: Context,
    node_class: str,
    nodes_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Add nodes to a node class.

    Adds one or more nodes to the specified node class.

    Args:
        node_class: Node class name
        nodes_data: Data specifying nodes to add
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing operation status
    """
    await ctx.info(f"Tool called: add_nodes_to_class for: {node_class}")
    await ctx.debug(f"Adding nodes to node class: {node_class}")

    try:
        result = await add_nodes_to_class_api(
            node_class=node_class, nodes_data=nodes_data, domain=domain
        )
        await ctx.info(f"Successfully added nodes to node class: {node_class}")
        return result
    except Exception as e:
        await ctx.error(f"Failed to add nodes to node class {node_class}: {str(e)}")
        raise


@mcp.tool()
async def remove_nodes_from_class(
    ctx: Context,
    node_class: str,
    nodes_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Remove nodes from a node class.

    Removes one or more nodes from the specified node class.

    Args:
        node_class: Node class name
        nodes_data: Data specifying nodes to remove
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing operation status
    """
    await ctx.info(f"Tool called: remove_nodes_from_class for: {node_class}")
    await ctx.debug(f"Removing nodes from node class: {node_class}")

    try:
        result = await remove_nodes_from_class_api(
            node_class=node_class, nodes_data=nodes_data, domain=domain
        )
        await ctx.info(f"Successfully removed nodes from node class: {node_class}")
        return result
    except Exception as e:
        await ctx.error(
            f"Failed to remove nodes from node class {node_class}: {str(e)}"
        )
        raise
