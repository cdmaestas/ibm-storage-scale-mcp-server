"""IBM Storage Scale XCP (parallel copy) operations.

XCP endpoints for performing parallel file copies and synchronization within
a single IBM Storage Scale cluster, following the 6.0.1 native REST API.
Note: copy/sync/verify/enable are PATCH requests in the native API.
"""

from typing import Optional, Any, Dict
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


def _domain_headers(domain: Optional[str]) -> Dict[str, str]:
    """Build request headers for the optional X-StorageScaleDomain."""
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain
    return headers


async def list_xcp_operations_api(
    domain: Optional[str] = None,
) -> Any:
    """List configuration information of all currently running XCP operations.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing XCP operations

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.get(
                "/scalemgmt/v3/xcp", headers=_domain_headers(domain)
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to list XCP operations: {str(e)}") from e


async def get_xcp_operation_api(
    id: str,
    domain: Optional[str] = None,
) -> Any:
    """Retrieve configuration information of a specific XCP operation by ID.

    Args:
        id: XCP operation ID
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the XCP operation details

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/xcp/{id}", headers=_domain_headers(domain)
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get XCP operation '{id}': {str(e)}"
        ) from e


async def get_xcp_config_api(
    domain: Optional[str] = None,
) -> Any:
    """Retrieve the current XCP configuration limits for the cluster.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the XCP configuration

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.get(
                "/scalemgmt/v3/xcp/config", headers=_domain_headers(domain)
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to get XCP config: {str(e)}") from e


async def update_xcp_config_api(
    config_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Update the XCP configuration limits for the cluster.

    Args:
        config_data: Configuration updates, e.g.
            {"updates": {"max_files": ..., "max_parallel": ..., "max_threads": ...}}
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the update status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.patch(
                "/scalemgmt/v3/xcp/config",
                json=config_data,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to update XCP config: {str(e)}") from e


async def enable_xcp_copy_api(
    copy_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Start a parallel copy of files from a source to a target in the cluster.

    Supports copying within a file system, between file systems in the same
    cluster, from live file systems, and from snapshots. Cross-cluster copy is
    not supported.

    Args:
        copy_data: Copy parameters (source, target, nodes, thread_level,
            snapshot options, etc.)
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the operation ID and parameters

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.patch(
                "/scalemgmt/v3/xcp:enable",
                json=copy_data,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to start XCP copy: {str(e)}") from e


async def sync_xcp_api(
    sync_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Synchronize files from a source directory to a target directory.

    Copies only files that are missing or appear different, based on file size
    and last modification time.

    Args:
        sync_data: Sync parameters (source, target, snapshot options)
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the operation ID and parameters

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.patch(
                "/scalemgmt/v3/xcp:sync",
                json=sync_data,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to start XCP sync: {str(e)}") from e


async def verify_xcp_api(
    verify_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Compare metadata between a source and target of a previous XCP copy.

    Checks attributes for each object including file type, user/owner, group,
    and access rights.

    Args:
        verify_data: Verify parameters (source, target, check_attributes,
            snapshot options)
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the operation ID and parameters

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.patch(
                "/scalemgmt/v3/xcp:verify",
                json=verify_data,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to start XCP verify: {str(e)}") from e
