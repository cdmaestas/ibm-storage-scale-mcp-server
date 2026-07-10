"""IBM Storage Scale Remote Filesystem operations.

Remote filesystem endpoints for managing filesystems on remote clusters.
"""

from typing import Optional, Any, Dict
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


async def list_remote_filesystems_api(
    cluster: str,
    domain: Optional[str] = None,
) -> Any:
    """List filesystems on a remote cluster.

    Args:
        cluster: Remote cluster name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing list of remote filesystems

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/remoteclusters/{cluster}/filesystems", headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to list filesystems for remote cluster '{cluster}': {str(e)}"
        ) from e


async def get_remote_filesystem_api(
    cluster: str,
    filesystem: str,
    domain: Optional[str] = None,
) -> Any:
    """Get details of a filesystem on a remote cluster.

    Args:
        cluster: Remote cluster name
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing remote filesystem details

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/remoteclusters/{cluster}/filesystems/{filesystem}",
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get filesystem '{filesystem}' on remote cluster '{cluster}': {str(e)}"
        ) from e


async def mount_remote_filesystem_api(
    cluster: str,
    filesystem: str,
    mount_data: Optional[dict] = None,
    domain: Optional[str] = None,
) -> Any:
    """Mount a remote filesystem locally.

    Args:
        cluster: Remote cluster name
        filesystem: Filesystem name
        mount_data: Optional mount configuration
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing mount operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    body = mount_data if mount_data is not None else {}

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/remoteclusters/{cluster}/filesystems/{filesystem}:mount",
                json=body,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to mount filesystem '{filesystem}' from remote cluster '{cluster}': {str(e)}"
        ) from e


async def unmount_remote_filesystem_api(
    cluster: str,
    filesystem: str,
    unmount_data: Optional[dict] = None,
    domain: Optional[str] = None,
) -> Any:
    """Unmount a remote filesystem.

    Args:
        cluster: Remote cluster name
        filesystem: Filesystem name
        unmount_data: Optional unmount configuration
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing unmount operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    body = unmount_data if unmount_data is not None else {}

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/remoteclusters/{cluster}/filesystems/{filesystem}:unmount",
                json=body,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to unmount filesystem '{filesystem}' from remote cluster '{cluster}': {str(e)}"
        ) from e


async def get_remote_filesystem_status_api(
    cluster: str,
    filesystem: str,
    domain: Optional[str] = None,
) -> Any:
    """Get status of a remote filesystem.

    Args:
        cluster: Remote cluster name
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing remote filesystem status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/remoteclusters/{cluster}/filesystems/{filesystem}/status",
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get status for filesystem '{filesystem}' on remote cluster '{cluster}': {str(e)}"
        ) from e
