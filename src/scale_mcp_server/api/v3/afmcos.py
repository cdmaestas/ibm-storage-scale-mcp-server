"""IBM Storage Scale Active File Management to Cloud Object Storage (AFMCOS) operations.

AFMCOS endpoints for managing Active File Management to Cloud Object Storage operations.
"""

from typing import Optional, Any, Dict
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


async def list_afmcos_filesets_api(
    filesystem: str,
    domain: Optional[str] = None,
) -> Any:
    """List all AFMCOS filesets in a filesystem.

    Args:
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing AFMCOS filesets information

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/afmcos", headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to list AFMCOS filesets for filesystem '{filesystem}': {str(e)}"
        ) from e


async def get_afmcos_fileset_api(
    filesystem: str,
    fileset: str,
    domain: Optional[str] = None,
) -> Any:
    """Get AFMCOS configuration for a specific fileset.

    Args:
        filesystem: Filesystem name
        fileset: Fileset name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing AFMCOS fileset configuration

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/afmcos/{fileset}",
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get AFMCOS configuration for fileset '{fileset}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def create_afmcos_fileset_api(
    filesystem: str,
    afmcos_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Create an AFMCOS fileset.

    Args:
        filesystem: Filesystem name
        afmcos_data: AFMCOS fileset configuration data
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
                f"/scalemgmt/v3/filesystems/{filesystem}/afmcos",
                json=afmcos_data,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        fileset_name = afmcos_data.get("filesetName", "unknown")
        raise StorageScaleAPIError(
            f"Failed to create AFMCOS fileset '{fileset_name}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def update_afmcos_fileset_api(
    filesystem: str,
    fileset: str,
    afmcos_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Update AFMCOS configuration for a fileset.

    Args:
        filesystem: Filesystem name
        fileset: Fileset name
        afmcos_data: Updated AFMCOS configuration data
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
                f"/scalemgmt/v3/filesystems/{filesystem}/afmcos/{fileset}",
                json=afmcos_data,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to update AFMCOS configuration for fileset '{fileset}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def delete_afmcos_fileset_api(
    filesystem: str,
    fileset: str,
    domain: Optional[str] = None,
) -> Any:
    """Delete AFMCOS configuration from a fileset.

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
                f"/scalemgmt/v3/filesystems/{filesystem}/afmcos/{fileset}",
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to delete AFMCOS configuration for fileset '{fileset}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def prefetch_afmcos_fileset_api(
    filesystem: str,
    fileset: str,
    prefetch_data: Optional[dict] = None,
    domain: Optional[str] = None,
) -> Any:
    """Prefetch data from cloud object storage for an AFMCOS fileset.

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
                f"/scalemgmt/v3/filesystems/{filesystem}/afmcos/{fileset}:prefetch",
                json=body,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to prefetch data for AFMCOS fileset '{fileset}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def evict_afmcos_fileset_api(
    filesystem: str,
    fileset: str,
    evict_data: Optional[dict] = None,
    domain: Optional[str] = None,
) -> Any:
    """Evict cached data from an AFMCOS fileset.

    Args:
        filesystem: Filesystem name
        fileset: Fileset name
        evict_data: Optional eviction configuration
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing eviction operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    body = evict_data if evict_data is not None else {}

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{filesystem}/afmcos/{fileset}:evict",
                json=body,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to evict data for AFMCOS fileset '{fileset}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def get_afmcos_fileset_status_api(
    filesystem: str,
    fileset: str,
    domain: Optional[str] = None,
) -> Any:
    """Get status of an AFMCOS fileset.

    Args:
        filesystem: Filesystem name
        fileset: Fileset name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing AFMCOS fileset status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/afmcos/{fileset}/status",
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get status for AFMCOS fileset '{fileset}' in filesystem '{filesystem}': {str(e)}"
        ) from e
