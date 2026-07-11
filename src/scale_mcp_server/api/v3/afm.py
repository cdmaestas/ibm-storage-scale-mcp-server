"""IBM Storage Scale Active File Management (AFM) operations.

AFM endpoints for managing Active File Management filesets in IBM Storage Scale.
Endpoints follow the 6.0.1 native REST API:
/scalemgmt/v3/filesystems/{filesystem}/filesets/[{fileset}/]afm...
"""

from typing import Optional, Any, Dict
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


def _domain_headers(domain: Optional[str]) -> Dict[str, str]:
    """Build request headers for the optional X-StorageScaleDomain."""
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain
    return headers


async def list_afm_states_api(
    filesystem: str,
    domain: Optional[str] = None,
) -> Any:
    """List the AFM state of all AFM filesets in a filesystem.

    Args:
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the AFM state of all AFM filesets

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets/afm/state",
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to list AFM states for filesystem '{filesystem}': {str(e)}"
        ) from e


async def get_afm_state_api(
    filesystem: str,
    fileset: str,
    domain: Optional[str] = None,
) -> Any:
    """Describe the AFM state of a specific AFM fileset.

    Args:
        filesystem: Filesystem name
        fileset: AFM fileset name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the AFM fileset state

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/afm/state",
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get AFM state for fileset '{fileset}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def check_afm_dirty_api(
    filesystem: str,
    fileset: str,
    dir_path: Optional[str] = None,
    dirty_data: Optional[bool] = None,
    escaped_chars: Optional[bool] = None,
    domain: Optional[str] = None,
) -> Any:
    """Find all modified (dirty) directories and files in an AFM fileset.

    Args:
        filesystem: Filesystem name
        fileset: AFM fileset name
        dir_path: Path under the AFM fileset to check for dirty files
        dirty_data: Calculate the total data of modified files
        escaped_chars: List modified directories and files with escaped characters
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the dirty file information

    Raises:
        StorageScaleAPIError: If API call fails
    """
    params: Dict[str, Any] = {}
    if dir_path is not None:
        params["dir_path"] = dir_path
    if dirty_data is not None:
        params["dirty_data"] = dirty_data
    if escaped_chars is not None:
        params["escaped_chars"] = escaped_chars

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/afm/checkdirty",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to check dirty files for AFM fileset '{fileset}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def check_afm_uncached_api(
    filesystem: str,
    fileset: str,
    dir_path: Optional[str] = None,
    check_unmigrated: Optional[bool] = None,
    escaped_chars: Optional[bool] = None,
    domain: Optional[str] = None,
) -> Any:
    """Find all uncached directories, files, and orphan files in an AFM fileset.

    Args:
        filesystem: Filesystem name
        fileset: AFM fileset name
        dir_path: Path under the AFM fileset to check for uncached files
        check_unmigrated: List non-migrated directories, files, and orphans
        escaped_chars: List entries with escaped characters
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the uncached file information

    Raises:
        StorageScaleAPIError: If API call fails
    """
    params: Dict[str, Any] = {}
    if dir_path is not None:
        params["dir_path"] = dir_path
    if check_unmigrated is not None:
        params["check_unmigrated"] = check_unmigrated
    if escaped_chars is not None:
        params["escaped_chars"] = escaped_chars

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/afm/checkuncached",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to check uncached files for AFM fileset '{fileset}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def flush_afm_queue_api(
    filesystem: str,
    fileset: str,
    domain: Optional[str] = None,
) -> Any:
    """Flush all pending queued operations for an AFM fileset.

    Args:
        filesystem: Filesystem name
        fileset: AFM fileset name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the flush operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/afm/flushqueue",
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to flush queue for AFM fileset '{fileset}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def resume_afm_requeued_api(
    filesystem: str,
    fileset: str,
    domain: Optional[str] = None,
) -> Any:
    """Resume all pending requeued operations for an AFM fileset.

    Args:
        filesystem: Filesystem name
        fileset: AFM fileset name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the resume operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/afm/resumerequeued",
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to resume requeued operations for AFM fileset '{fileset}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def resync_afm_fileset_api(
    filesystem: str,
    fileset: str,
    domain: Optional[str] = None,
) -> Any:
    """Resync all files from cache to home for a single-writer mode AFM fileset.

    Args:
        filesystem: Filesystem name
        fileset: AFM fileset name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the resync operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/afm/resync",
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to resync AFM fileset '{fileset}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def start_afm_fileset_api(
    filesystem: str,
    fileset: str,
    domain: Optional[str] = None,
) -> Any:
    """Start operations for an AFM fileset.

    Args:
        filesystem: Filesystem name
        fileset: AFM fileset name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the start operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/afm:start",
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to start AFM fileset '{fileset}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def stop_afm_fileset_api(
    filesystem: str,
    fileset: str,
    domain: Optional[str] = None,
) -> Any:
    """Stop all operations for an AFM fileset.

    Args:
        filesystem: Filesystem name
        fileset: AFM fileset name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the stop operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/afm:stop",
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to stop AFM fileset '{fileset}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def reset_afm_local_api(
    filesystem: str,
    fileset: str,
    file_path: str,
    domain: Optional[str] = None,
) -> Any:
    """Reset the local bit for a filepath in an AFM fileset.

    Args:
        filesystem: Filesystem name
        fileset: AFM fileset name
        file_path: Filepath for which to reset the local bit
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.patch(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/afm:resetlocal",
                json={"path": file_path},
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to reset local bit for '{file_path}' in AFM fileset '{fileset}': {str(e)}"
        ) from e


async def set_afm_local_api(
    filesystem: str,
    fileset: str,
    file_path: str,
    domain: Optional[str] = None,
) -> Any:
    """Set the local bit for a filepath in an AFM fileset.

    Args:
        filesystem: Filesystem name
        fileset: AFM fileset name
        file_path: Filepath for which to set the local bit
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.patch(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/afm:setlocal",
                json={"path": file_path},
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to set local bit for '{file_path}' in AFM fileset '{fileset}': {str(e)}"
        ) from e
