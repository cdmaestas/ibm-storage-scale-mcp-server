"""IBM Storage Scale Remote File System operations.

Remote file system endpoints (/scalemgmt/v3/filesystems/remote...) for
managing file systems owned by another cluster, following the 6.0.1 native
REST API.
"""

from typing import Optional, Any, Dict
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


def _domain_headers(domain: Optional[str]) -> Dict[str, str]:
    """Build request headers for the optional X-StorageScaleDomain."""
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain
    return headers


async def add_remote_filesystem_api(
    filesystem: dict,
    domain: Optional[str] = None,
) -> Any:
    """Add a remote file system owned by another IBM Storage Scale cluster.

    Args:
        filesystem: Remote file system definition
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the creation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/filesystems/remote",
                json=filesystem,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        name = filesystem.get("name", "unknown")
        raise StorageScaleAPIError(
            f"Failed to add remote filesystem '{name}': {str(e)}"
        ) from e


async def update_remote_filesystem_api(
    filesystem: str,
    filesystem_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Update the information associated with a remote file system.

    Args:
        filesystem: Remote file system name
        filesystem_data: Updated remote file system definition
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the update status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.patch(
                f"/scalemgmt/v3/filesystems/remote/{filesystem}",
                json=filesystem_data,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to update remote filesystem '{filesystem}': {str(e)}"
        ) from e


async def delete_remote_filesystem_api(
    filesystem: str,
    permanently_damaged: Optional[bool] = None,
    domain: Optional[str] = None,
) -> Any:
    """Delete a remote file system.

    Args:
        filesystem: Remote file system name
        permanently_damaged: Proceed with deletion even if the remote file
            system is permanently damaged
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the deletion status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    params: Dict[str, Any] = {}
    if permanently_damaged is not None:
        params["permanently_damaged"] = permanently_damaged

    try:
        async with StorageScaleClient() as client:
            return await client.delete(
                f"/scalemgmt/v3/filesystems/remote/{filesystem}",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to delete remote filesystem '{filesystem}': {str(e)}"
        ) from e
