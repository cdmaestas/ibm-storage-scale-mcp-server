"""IBM Storage Scale Filesystem Disk operations.

Filesystem disk endpoints for managing disks within filesystems.
"""

from typing import Optional, Any, Dict
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


async def list_filesystem_disks_api(
    filesystem: str,
    domain: Optional[str] = None,
) -> Any:
    """List all disks in a filesystem.

    Retrieves a list of all disks associated with the specified filesystem.

    Args:
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing list of filesystem disks

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/disks", headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to list disks for filesystem '{filesystem}': {str(e)}"
        ) from e


async def get_filesystem_disk_api(
    filesystem: str,
    disk: str,
    domain: Optional[str] = None,
) -> Any:
    """Get details of a specific disk in a filesystem.

    Retrieves detailed information about a specific disk in the filesystem.

    Args:
        filesystem: Filesystem name
        disk: Disk name or NSD name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing disk details

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/disks/{disk}",
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get disk '{disk}' for filesystem '{filesystem}': {str(e)}"
        ) from e


async def add_disks_to_filesystem_api(
    filesystem: str,
    disks_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Add disks to a filesystem.

    Adds one or more disks to the specified filesystem.

    Args:
        filesystem: Filesystem name
        disks_data: Data specifying disks to add
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
                f"/scalemgmt/v3/filesystems/{filesystem}/disks",
                json=disks_data,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to add disks to filesystem '{filesystem}': {str(e)}"
        ) from e


async def remove_disk_from_filesystem_api(
    filesystem: str,
    disk: str,
    domain: Optional[str] = None,
) -> Any:
    """Remove a disk from a filesystem.

    Removes the specified disk from the filesystem.

    Args:
        filesystem: Filesystem name
        disk: Disk name or NSD name to remove
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
                f"/scalemgmt/v3/filesystems/{filesystem}/disks/{disk}",
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to remove disk '{disk}' from filesystem '{filesystem}': {str(e)}"
        ) from e


async def update_filesystem_disk_api(
    filesystem: str,
    disk: str,
    disk_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Update disk configuration in a filesystem.

    Updates the configuration of a specific disk in the filesystem.

    Args:
        filesystem: Filesystem name
        disk: Disk name or NSD name
        disk_data: Updated disk configuration data
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
                f"/scalemgmt/v3/filesystems/{filesystem}/disks/{disk}",
                json=disk_data,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to update disk '{disk}' in filesystem '{filesystem}': {str(e)}"
        ) from e
