"""IBM Storage Scale Manager operations.

Manager endpoints for managing manager node operations and configuration.
"""

from typing import Optional, Any, Dict
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


async def list_managers_api(
    domain: Optional[str] = None,
) -> Any:
    """List all manager nodes.

    Retrieves a list of all manager nodes in the cluster.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing list of manager nodes

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get("/scalemgmt/v3/managers", headers=headers)
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to list managers: {str(e)}") from e


async def get_manager_api(
    manager: str,
    domain: Optional[str] = None,
) -> Any:
    """Get details of a specific manager node.

    Retrieves detailed information about a specific manager node.

    Args:
        manager: Manager node name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing manager node details

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/managers/{manager}", headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get manager '{manager}': {str(e)}"
        ) from e


async def add_manager_api(
    manager_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Add a new manager node.

    Adds a new manager node to the cluster.

    Args:
        manager_data: Manager node configuration data
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
                "/scalemgmt/v3/managers", json=manager_data, headers=headers
            )
    except StorageScaleAPIError as e:
        manager_name = manager_data.get("name", "unknown")
        raise StorageScaleAPIError(
            f"Failed to add manager '{manager_name}': {str(e)}"
        ) from e


async def remove_manager_api(
    manager: str,
    domain: Optional[str] = None,
) -> Any:
    """Remove a manager node.

    Removes the specified manager node from the cluster.

    Args:
        manager: Manager node name
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
            return await client.delete(
                f"/scalemgmt/v3/managers/{manager}", headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to remove manager '{manager}': {str(e)}"
        ) from e


async def update_manager_api(
    manager: str,
    manager_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Update manager node configuration.

    Updates the configuration of a specific manager node.

    Args:
        manager: Manager node name
        manager_data: Updated manager configuration data
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
                f"/scalemgmt/v3/managers/{manager}",
                json=manager_data,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to update manager '{manager}': {str(e)}"
        ) from e
