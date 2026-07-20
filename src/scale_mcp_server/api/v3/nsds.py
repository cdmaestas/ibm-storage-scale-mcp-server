"""IBM Storage Scale NSD operations.

NSD endpoints for creating and managing network-shared disks, following the
6.0.1 native REST API.
"""

from typing import Any

from scale_mcp_server.utils.client import StorageScaleAPIError, StorageScaleClient


def _domain_headers(domain: str | None) -> dict[str, str]:
    """Build request headers for the optional X-StorageScaleDomain."""
    headers: dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain
    return headers


async def list_nsds_api(
    not_assigned: bool | None = None,
    filesystem_device: str | None = None,
    view: str | None = None,
    page_size: int | None = None,
    page_token: str | None = None,
    domain: str | None = None,
) -> Any:
    """List all NSDs (Network Shared Disks).

    Args:
        not_assigned: List all disks that do not belong to any file system
        filesystem_device: List all disks of the specified file system device
        view: View for NSD content (local-node, all-nodes, all-nsds, long,
            extended)
        page_size: Number of items to return per request
        page_token: Token to navigate to the next page
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing NSDs information

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    params: dict[str, Any] = {}
    if not_assigned is not None:
        params["not_assigned"] = not_assigned
    if filesystem_device is not None:
        params["filesystem_device"] = filesystem_device
    if view is not None:
        params["view"] = view
    if page_size is not None:
        params["page_size"] = page_size
    if page_token is not None:
        params["page_token"] = page_token

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                "/scalemgmt/v3/nsds",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to list NSDs: {str(e)}") from e


async def get_nsd_api(
    nsd_name: str,
    view: str | None = None,
    domain: str | None = None,
) -> Any:
    """Get information about a specific NSD.

    Args:
        nsd_name: NSD name
        view: View for NSD content (local-node, all-nodes, all-nsds, long,
            extended)
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing NSD information

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    params: dict[str, Any] = {}
    if view is not None:
        params["view"] = view

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/nsds/{nsd_name}",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to get NSD '{nsd_name}': {str(e)}") from e


async def create_nsd_api(
    nsd_data: dict,
    no_verify: bool | None = None,
    domain: str | None = None,
) -> Any:
    """Create an NSD in the cluster.

    Args:
        nsd_data: NSD definition
        no_verify: Do not verify that the physical disk is unused before
            creating the NSD
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the creation status

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    params: dict[str, Any] = {}
    if no_verify is not None:
        params["no_verify"] = no_verify

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/nsds",
                json=nsd_data,
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        name = nsd_data.get("name", "unknown")
        raise StorageScaleAPIError(f"Failed to create NSD '{name}': {str(e)}") from e


async def update_nsd_api(
    nsd_name: str,
    nsd_data: dict,
    domain: str | None = None,
) -> Any:
    """Update an existing NSD (for example, the assigned NSD servers).

    Args:
        nsd_name: NSD name
        nsd_data: Updated NSD definition
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the update status

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.patch(
                f"/scalemgmt/v3/nsds/{nsd_name}",
                json=nsd_data,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to update NSD '{nsd_name}': {str(e)}") from e


async def delete_nsd_api(
    nsd_name: str,
    domain: str | None = None,
) -> Any:
    """Delete an existing NSD.

    Args:
        nsd_name: NSD name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the deletion status

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.delete(f"/scalemgmt/v3/nsds/{nsd_name}", headers=_domain_headers(domain))
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to delete NSD '{nsd_name}': {str(e)}") from e


async def batch_create_nsds_api(
    nsds_data: dict,
    domain: str | None = None,
) -> Any:
    """Create one or more NSDs (LRO).

    Args:
        nsds_data: Batch NSD definitions
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the batch create status

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/nsds:batchCreate",
                json=nsds_data,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to batch create NSDs: {str(e)}") from e


async def batch_delete_nsds_api(
    nsds_data: dict,
    domain: str | None = None,
) -> Any:
    """Delete one or more NSDs (LRO).

    Args:
        nsds_data: Batch NSD deletion parameters
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the batch delete status

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/nsds:batchDelete",
                json=nsds_data,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to batch delete NSDs: {str(e)}") from e
