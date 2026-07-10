"""IBM Storage Scale Node Class operations.

Node class endpoints for managing node classifications and groupings.
"""

from typing import Optional, Any, Dict
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


async def list_node_classes_api(
    domain: Optional[str] = None,
) -> Any:
    """List all node classes.

    Retrieves a list of all node classes in the cluster.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing list of node classes

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get("/scalemgmt/v3/nodeclasses", headers=headers)
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to list node classes: {str(e)}") from e


async def get_node_class_api(
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

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/nodeclasses/{node_class}", headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get node class '{node_class}': {str(e)}"
        ) from e


async def create_node_class_api(
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

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/nodeclasses", json=node_class_data, headers=headers
            )
    except StorageScaleAPIError as e:
        node_class_name = node_class_data.get("name", "unknown")
        raise StorageScaleAPIError(
            f"Failed to create node class '{node_class_name}': {str(e)}"
        ) from e


async def update_node_class_api(
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

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.put(
                f"/scalemgmt/v3/nodeclasses/{node_class}",
                json=node_class_data,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to update node class '{node_class}': {str(e)}"
        ) from e


async def delete_node_class_api(
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

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.delete(
                f"/scalemgmt/v3/nodeclasses/{node_class}", headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to delete node class '{node_class}': {str(e)}"
        ) from e


async def add_nodes_to_class_api(
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

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/nodeclasses/{node_class}:addNodes",
                json=nodes_data,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to add nodes to node class '{node_class}': {str(e)}"
        ) from e


async def remove_nodes_from_class_api(
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

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/nodeclasses/{node_class}:removeNodes",
                json=nodes_data,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to remove nodes from node class '{node_class}': {str(e)}"
        ) from e
