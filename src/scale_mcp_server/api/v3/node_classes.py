"""IBM Storage Scale Node Class operations.

Node class endpoints for creating and managing user-defined node classes,
following the 6.0.1 native REST API.
"""

from typing import Optional, Any, Dict
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


def _domain_headers(domain: Optional[str]) -> Dict[str, str]:
    """Build request headers for the optional X-StorageScaleDomain."""
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain
    return headers


async def list_node_classes_api(
    page_size: Optional[int] = None,
    page_token: Optional[str] = None,
    domain: Optional[str] = None,
) -> Any:
    """List all node classes registered to the cluster.

    Args:
        page_size: Number of items to return per request
        page_token: Token to navigate to the next page
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the list of node classes

    Raises:
        StorageScaleAPIError: If API call fails
    """
    params: Dict[str, Any] = {}
    if page_size is not None:
        params["page_size"] = page_size
    if page_token is not None:
        params["page_token"] = page_token

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                "/scalemgmt/v3/nodeclasses",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to list node classes: {str(e)}") from e


async def get_node_class_api(
    node_class: str,
    domain: Optional[str] = None,
) -> Any:
    """List the members of the specified node class.

    Args:
        node_class: Node class name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing node class details

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/nodeclasses/{node_class}",
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get node class '{node_class}': {str(e)}"
        ) from e


async def create_node_class_api(
    nodeclass_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Create a user-defined node class.

    Args:
        nodeclass_data: Node class definition, e.g.
            {"name": ..., "members": [...], "subclasses": [...]}
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the creation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/nodeclasses",
                json=nodeclass_data,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        name = nodeclass_data.get("name", "unknown")
        raise StorageScaleAPIError(
            f"Failed to create node class '{name}': {str(e)}"
        ) from e


async def update_node_class_api(
    node_class: str,
    nodeclass_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Update an existing node class.

    Args:
        node_class: Node class name
        nodeclass_data: Updated node class definition, e.g.
            {"name": ..., "members": [...], "subclasses": [...]}
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the update status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.patch(
                f"/scalemgmt/v3/nodeclasses/{node_class}",
                json=nodeclass_data,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to update node class '{node_class}': {str(e)}"
        ) from e


async def delete_node_class_api(
    node_class: str,
    domain: Optional[str] = None,
) -> Any:
    """Delete an existing node class.

    Args:
        node_class: Node class name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the deletion status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.delete(
                f"/scalemgmt/v3/nodeclasses/{node_class}",
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to delete node class '{node_class}': {str(e)}"
        ) from e
