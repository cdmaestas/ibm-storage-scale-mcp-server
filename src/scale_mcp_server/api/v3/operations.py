"""IBM Storage Scale Operations endpoints.

Operations endpoints for tracking and managing long-running asynchronous operations.
"""

from typing import Optional, Any, Dict
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


async def list_operations_api(
    filter: Optional[str] = None,
    domain: Optional[str] = None,
) -> Any:
    """List all operations.

    Retrieves a list of operations, optionally filtered by status or other criteria.

    Args:
        filter: Filter expression (e.g., 'status=running', 'status=completed')
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing list of operations

    Raises:
        StorageScaleAPIError: If API call fails
    """
    query_params: Dict[str, Any] = {}
    if filter:
        query_params["filter"] = filter

    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                "/scalemgmt/v3/operations", params=query_params, headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to list operations: {str(e)}") from e


async def get_operation_api(
    operation_id: str,
    domain: Optional[str] = None,
) -> Any:
    """Get details of a specific operation.

    Retrieves detailed information about a specific operation including its
    status, progress, and results.

    Args:
        operation_id: Operation ID
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing operation details

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/operations/{operation_id}", headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get operation '{operation_id}': {str(e)}"
        ) from e


async def cancel_operation_api(
    operation_id: str,
    domain: Optional[str] = None,
) -> Any:
    """Cancel a running operation.

    Attempts to cancel a running operation. Not all operations can be cancelled.

    Args:
        operation_id: Operation ID to cancel
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
                f"/scalemgmt/v3/operations/{operation_id}", headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to cancel operation '{operation_id}': {str(e)}"
        ) from e


async def wait_for_operation_api(
    operation_id: str,
    timeout: Optional[int] = None,
    domain: Optional[str] = None,
) -> Any:
    """Wait for an operation to complete.

    Polls an operation until it completes or times out.

    Args:
        operation_id: Operation ID to wait for
        timeout: Maximum time to wait in seconds (optional)
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing final operation status

    Raises:
        StorageScaleAPIError: If API call fails or operation times out
    """
    query_params: Dict[str, Any] = {}
    if timeout is not None:
        query_params["timeout"] = timeout

    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/operations/{operation_id}:wait",
                params=query_params,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to wait for operation '{operation_id}': {str(e)}"
        ) from e
