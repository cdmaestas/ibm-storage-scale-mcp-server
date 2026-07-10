"""IBM Storage Scale XCP (eXtreme Copy) operations.

XCP endpoints for performing parallel file copies and synchronization operations.
"""

from typing import Optional, Any, Dict
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


async def list_xcp_operations_api(
    domain: Optional[str] = None,
) -> Any:
    """List all XCP operations.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing list of XCP operations

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get("/scalemgmt/v3/xcp", headers=headers)
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to list XCP operations: {str(e)}") from e


async def get_xcp_operation_api(
    operation_id: str,
    domain: Optional[str] = None,
) -> Any:
    """Get details of a specific XCP operation.

    Args:
        operation_id: XCP operation identifier
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing XCP operation details

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/xcp/{operation_id}", headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get XCP operation '{operation_id}': {str(e)}"
        ) from e


async def create_xcp_copy_api(
    copy_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Create a new XCP copy operation.

    Initiates a parallel file copy operation from source to target.

    Args:
        copy_data: XCP copy configuration data including source and target paths
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing operation ID and status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/xcp:copy", json=copy_data, headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to create XCP copy operation: {str(e)}") from e


async def create_xcp_sync_api(
    sync_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Create a new XCP sync operation.

    Initiates a parallel file synchronization operation from source to target.

    Args:
        sync_data: XCP sync configuration data including source and target paths
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing operation ID and status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/xcp:sync", json=sync_data, headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to create XCP sync operation: {str(e)}") from e


async def cancel_xcp_operation_api(
    operation_id: str,
    domain: Optional[str] = None,
) -> Any:
    """Cancel a running XCP operation.

    Args:
        operation_id: XCP operation identifier
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing cancellation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.delete(
                f"/scalemgmt/v3/xcp/{operation_id}", headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to cancel XCP operation '{operation_id}': {str(e)}"
        ) from e


async def get_xcp_operation_status_api(
    operation_id: str,
    domain: Optional[str] = None,
) -> Any:
    """Get status of an XCP operation.

    Args:
        operation_id: XCP operation identifier
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing operation status and progress

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/xcp/{operation_id}/status", headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get status for XCP operation '{operation_id}': {str(e)}"
        ) from e


async def get_xcp_operation_logs_api(
    operation_id: str,
    domain: Optional[str] = None,
) -> Any:
    """Get logs for an XCP operation.

    Args:
        operation_id: XCP operation identifier
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing operation logs

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/xcp/{operation_id}/logs", headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get logs for XCP operation '{operation_id}': {str(e)}"
        ) from e
