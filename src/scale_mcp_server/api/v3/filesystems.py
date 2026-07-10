"""IBM Storage Scale Filesystem operations."""

from typing import Optional, Any, Dict
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


async def list_filesystems_api(
    domain: Optional[str] = None,
) -> Any:
    """List all filesystems.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing filesystem information

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get("/scalemgmt/v3/filesystems", headers=headers)
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to list filesystems: {str(e)}") from e


async def get_filesystem_api(
    filesystem: str,
    domain: Optional[str] = None,
) -> Any:
    """Get detailed information about a specific filesystem.

    Args:
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing detailed filesystem information

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}", headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get filesystem '{filesystem}': {str(e)}"
        ) from e


async def create_filesystem_api(
    filesystem_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Create a new filesystem.

    Args:
        filesystem_data: Filesystem configuration data
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing created filesystem information

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/filesystems", json=filesystem_data, headers=headers
            )
    except StorageScaleAPIError as e:
        fs_name = filesystem_data.get("filesystemName", "unknown")
        raise StorageScaleAPIError(
            f"Failed to create filesystem '{fs_name}': {str(e)}"
        ) from e


async def update_filesystem_api(
    filesystem: str,
    filesystem_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Update filesystem configuration.

    Args:
        filesystem: Filesystem name
        filesystem_data: Updated filesystem configuration data
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing updated filesystem information

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.put(
                f"/scalemgmt/v3/filesystems/{filesystem}",
                json=filesystem_data,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to update filesystem '{filesystem}': {str(e)}"
        ) from e


async def delete_filesystem_api(
    name: str,
    domain: Optional[str] = None,
) -> Any:
    """Delete a filesystem.

    Args:
        name: Filesystem name
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
                f"/scalemgmt/v3/filesystems/{name}", headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to delete filesystem '{name}': {str(e)}"
        ) from e


async def mount_filesystem_api(
    name: str,
    nodes: Optional[str] = None,
    domain: Optional[str] = None,
) -> Any:
    """Mount a filesystem.

    Args:
        name: Filesystem name
        nodes: Comma-separated list of node names
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing mount operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    query_params: Dict[str, Any] = {}
    if nodes:
        query_params["nodes"] = nodes

    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{name}:mount",
                params=query_params,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to mount filesystem '{name}': {str(e)}"
        ) from e


async def unmount_filesystem_api(
    name: str,
    nodes: Optional[str] = None,
    force: Optional[bool] = None,
    domain: Optional[str] = None,
) -> Any:
    """Unmount a filesystem.

    Args:
        name: Filesystem name
        nodes: Comma-separated list of node names
        force: Force unmount
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing unmount operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    query_params: Dict[str, Any] = {}
    if nodes:
        query_params["nodes"] = nodes
    if force is not None:
        query_params["force"] = str(force).lower()

    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{name}:unmount",
                params=query_params,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to unmount filesystem '{name}': {str(e)}"
        ) from e


async def mount_all_filesystems_api(
    domain: Optional[str] = None,
) -> Any:
    """Mount all filesystems.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing mount operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.post("/scalemgmt/v3/filesystems:mount", headers=headers)
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to mount all filesystems: {str(e)}") from e


async def unmount_all_filesystems_api(
    domain: Optional[str] = None,
) -> Any:
    """Unmount all filesystems.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing unmount operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/filesystems:unmount", headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to unmount all filesystems: {str(e)}"
        ) from e
