"""IBM Storage Scale Storage Pool operations.

Storage pool endpoints for listing and updating the storage pools of a file
system, following the 6.0.1 native REST API.
"""

from typing import Optional, Any, Dict
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


def _domain_headers(domain: Optional[str]) -> Dict[str, str]:
    """Build request headers for the optional X-StorageScaleDomain."""
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain
    return headers


async def list_storage_pools_api(
    filesystem: str,
    page_size: Optional[int] = None,
    page_token: Optional[str] = None,
    domain: Optional[str] = None,
) -> Any:
    """List storage pools for a filesystem.

    Args:
        filesystem: Filesystem name
        page_size: Number of items to return per request
        page_token: Token to navigate to the next page
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing storage pools information

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    params: Dict[str, Any] = {}
    if page_size is not None:
        params["page_size"] = page_size
    if page_token is not None:
        params["page_token"] = page_token

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/storagepools",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to list storage pools for filesystem '{filesystem}': {str(e)}"
        ) from e


async def get_storage_pool_api(
    filesystem: str,
    pool_name: str,
    domain: Optional[str] = None,
) -> Any:
    """Get information about a specific storage pool.

    Args:
        filesystem: Filesystem name
        pool_name: Storage pool name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing storage pool information

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/storagepools/{pool_name}",
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get storage pool '{pool_name}' for filesystem '{filesystem}': {str(e)}"
        ) from e


async def update_storage_pool_api(
    filesystem: str,
    pool_name: str,
    pool_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Update an existing storage pool of a filesystem.

    Args:
        filesystem: Filesystem name
        pool_name: Storage pool name
        pool_data: Updated storage pool definition
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the update status

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.patch(
                f"/scalemgmt/v3/filesystems/{filesystem}/storagepools/{pool_name}",
                json=pool_data,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to update storage pool '{pool_name}' for filesystem '{filesystem}': {str(e)}"
        ) from e
