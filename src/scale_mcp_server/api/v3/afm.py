"""IBM Storage Scale Active File Management (AFM) operations.

AFM endpoints for managing Active File Management filesets in IBM Storage Scale.
"""

from typing import Optional, Any, Dict
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


async def list_afm_filesets_api(
    filesystem: str,
    domain: Optional[str] = None,
) -> Any:
    """List all AFM filesets in a filesystem.

    Args:
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing AFM filesets information

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/afm", headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to list AFM filesets for filesystem '{filesystem}': {str(e)}"
        ) from e


async def get_afm_fileset_api(
    filesystem: str,
    fileset: str,
    domain: Optional[str] = None,
) -> Any:
    """Get AFM configuration for a specific fileset.

    Args:
        filesystem: Filesystem name
        fileset: Fileset name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing AFM fileset configuration

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/afm/{fileset}",
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get AFM configuration for fileset '{fileset}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def create_afm_fileset_api(
    filesystem: str,
    afm_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Create an AFM fileset.

    Args:
        filesystem: Filesystem name
        afm_data: AFM fileset configuration data
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
                f"/scalemgmt/v3/filesystems/{filesystem}/afm",
                json=afm_data,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        fileset_name = afm_data.get("filesetName", "unknown")
        raise StorageScaleAPIError(
            f"Failed to create AFM fileset '{fileset_name}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def update_afm_fileset_api(
    filesystem: str,
    fileset: str,
    afm_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Update AFM configuration for a fileset.

    Args:
        filesystem: Filesystem name
        fileset: Fileset name
        afm_data: Updated AFM configuration data
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
                f"/scalemgmt/v3/filesystems/{filesystem}/afm/{fileset}",
                json=afm_data,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to update AFM configuration for fileset '{fileset}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def delete_afm_fileset_api(
    filesystem: str,
    fileset: str,
    domain: Optional[str] = None,
) -> Any:
    """Delete AFM configuration from a fileset.

    Args:
        filesystem: Filesystem name
        fileset: Fileset name
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
                f"/scalemgmt/v3/filesystems/{filesystem}/afm/{fileset}",
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to delete AFM configuration for fileset '{fileset}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def prefetch_afm_fileset_api(
    filesystem: str,
    fileset: str,
    prefetch_data: Optional[dict] = None,
    domain: Optional[str] = None,
) -> Any:
    """Prefetch data for an AFM fileset.

    Args:
        filesystem: Filesystem name
        fileset: Fileset name
        prefetch_data: Optional prefetch configuration
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing prefetch operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    body = prefetch_data if prefetch_data is not None else {}

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{filesystem}/afm/{fileset}:prefetch",
                json=body,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to prefetch data for AFM fileset '{fileset}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def resync_afm_fileset_api(
    filesystem: str,
    fileset: str,
    resync_data: Optional[dict] = None,
    domain: Optional[str] = None,
) -> Any:
    """Resynchronize an AFM fileset with its source.

    Args:
        filesystem: Filesystem name
        fileset: Fileset name
        resync_data: Optional resync configuration
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing resync operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    body = resync_data if resync_data is not None else {}

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{filesystem}/afm/{fileset}:resync",
                json=body,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to resync AFM fileset '{fileset}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def get_afm_fileset_status_api(
    filesystem: str,
    fileset: str,
    domain: Optional[str] = None,
) -> Any:
    """Get status of an AFM fileset.

    Args:
        filesystem: Filesystem name
        fileset: Fileset name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing AFM fileset status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/afm/{fileset}/status",
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get status for AFM fileset '{fileset}' in filesystem '{filesystem}': {str(e)}"
        ) from e
