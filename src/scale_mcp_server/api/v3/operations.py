"""IBM Storage Scale Operations endpoints.

Operations endpoints for tracking and managing long-running operations (LRO),
following the 6.0.1 native REST API, plus a client-side polling helper.
"""

import asyncio
import time
from typing import Any

from scale_mcp_server.utils.client import StorageScaleAPIError, StorageScaleClient


def _domain_headers(domain: str | None) -> dict[str, str]:
    """Build request headers for the optional X-StorageScaleDomain."""
    headers: dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain
    return headers


async def list_operations_api(
    page_size: int | None = None,
    page_token: str | None = None,
    domain: str | None = None,
) -> Any:
    """List information about all long-running operations (LROs).

    Args:
        page_size: Number of items to return per request
        page_token: Token to navigate to the next page
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the list of operations

    Raises:
        StorageScaleAPIError: If API call fails
    """
    params: dict[str, Any] = {}
    if page_size is not None:
        params["page_size"] = page_size
    if page_token is not None:
        params["page_token"] = page_token

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                "/scalemgmt/v3/operations",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to list operations: {str(e)}") from e


async def get_operation_api(
    operation_id: str,
    domain: str | None = None,
) -> Any:
    """List details of an existing LRO.

    Args:
        operation_id: Operation ID of the LRO
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing operation details

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/operations/{operation_id}",
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to get operation '{operation_id}': {str(e)}") from e


async def get_operation_output_api(
    operation_id: str,
    byte_offset: int | None = None,
    domain: str | None = None,
) -> Any:
    """Display message output from an LRO.

    Args:
        operation_id: Operation ID of the LRO
        byte_offset: Offset in bytes to start reading the console output
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the operation output

    Raises:
        StorageScaleAPIError: If API call fails
    """
    params: dict[str, Any] = {}
    if byte_offset is not None:
        params["byte_offset"] = byte_offset

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/operations/{operation_id}/output",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to get output for operation '{operation_id}': {str(e)}") from e


async def cancel_operation_api(
    operation_id: str,
    domain: str | None = None,
) -> Any:
    """Cancel an LRO.

    All operations attempt to stop; if an operation is too far along,
    termination might not be possible.

    Args:
        operation_id: Operation ID of the LRO to cancel
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing cancellation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/operations/{operation_id}:cancel",
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to cancel operation '{operation_id}': {str(e)}") from e


async def wait_for_operation_api(
    operation_id: str,
    poll_interval: float = 2.0,
    timeout: float = 120.0,
    domain: str | None = None,
) -> Any:
    """Poll an LRO until it reports done, or the timeout elapses.

    This is a client-side convenience: the native REST API has no blocking
    wait endpoint, so this repeatedly issues GET /operations/{id}.

    Args:
        operation_id: Operation ID of the LRO
        poll_interval: Seconds to sleep between polls
        timeout: Maximum seconds to wait before raising
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        The final operation resource (with done == true)

    Raises:
        StorageScaleAPIError: If a poll fails or the timeout elapses
    """
    deadline = time.monotonic() + timeout
    while True:
        operation = await get_operation_api(operation_id, domain=domain)
        if isinstance(operation, dict) and operation.get("done"):
            return operation
        if time.monotonic() >= deadline:
            raise StorageScaleAPIError(f"Timed out after {timeout}s waiting for operation '{operation_id}'")
        await asyncio.sleep(poll_interval)


async def delete_operation_api(
    operation_id: str,
    domain: str | None = None,
) -> Any:
    """Delete an existing LRO record.

    Args:
        operation_id: Operation ID of the LRO to delete
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing deletion status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.delete(
                f"/scalemgmt/v3/operations/{operation_id}",
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to delete operation '{operation_id}': {str(e)}") from e
