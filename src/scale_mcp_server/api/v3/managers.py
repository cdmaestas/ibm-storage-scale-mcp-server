"""IBM Storage Scale Manager operations.

Manager endpoints for updating the cluster manager node and file system
manager nodes, following the 6.0.1 native REST API.
"""

from typing import Optional, Any, Dict
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


def _domain_headers(domain: Optional[str]) -> Dict[str, str]:
    """Build request headers for the optional X-StorageScaleDomain."""
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain
    return headers


async def set_cluster_manager_api(
    manager_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Update the cluster manager node.

    Args:
        manager_data: Request body identifying the new cluster manager node
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/clusters/manager",
                json=manager_data,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to set cluster manager: {str(e)}"
        ) from e


async def set_filesystem_manager_api(
    filesystem: str,
    manager_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Update the manager node of an existing file system.

    Args:
        filesystem: Filesystem name
        manager_data: Request body identifying the new file system manager node
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{filesystem}/manager",
                json=manager_data,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to set manager for filesystem '{filesystem}': {str(e)}"
        ) from e
