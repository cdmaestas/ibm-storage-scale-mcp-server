"""IBM Storage Scale Troubleshooting operations.

Troubleshooting endpoints for recovering from error situations: clearing NSD
volume IDs and managing persistent reserve registration keys. Follows the
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


async def clear_nsd_id_api(
    id: str,
    node_name: str | None = None,
    domain: str | None = None,
) -> Any:
    """Delete the NSD volume ID from a device.

    Args:
        id: NSD volume ID to clear
        node_name: Node directly attached to the disk holding the NSD volume ID
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    params: dict[str, Any] = {"id": id}
    if node_name is not None:
        params["node_name"] = node_name

    try:
        async with StorageScaleClient() as client:
            return await client.delete(
                "/scalemgmt/v3/troubleshooting/nsds/clearID",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to clear NSD volume ID '{id}': {str(e)}") from e


async def get_persistent_reserve_keys_api(
    device: str,
    node_name: str | None = None,
    domain: str | None = None,
) -> Any:
    """Get persistent reserve registration key values from a device.

    Args:
        device: Device name
        node_name: Node directly attached to the device to read
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the persistent reserve keys

    Raises:
        StorageScaleAPIError: If API call fails
    """
    params: dict[str, Any] = {}
    if node_name is not None:
        params["node_name"] = node_name

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/troubleshooting/persistentReserve/{device}/keys",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to get persistent reserve keys for device '{device}': {str(e)}") from e


async def clear_persistent_reserve_keys_api(
    device: str,
    key: str | None = None,
    node_name: str | None = None,
    force: bool | None = None,
    domain: str | None = None,
) -> Any:
    """Delete the persistent reserve registration key from a device.

    Args:
        device: Device name
        key: Persistent reserve key used to clear the keys from the device;
            defaults to the IBM persistent reserve key if not provided
        node_name: Node where the device is attached
        force: Override clearing keys that were not created by IBM Storage Scale
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    params: dict[str, Any] = {}
    if key is not None:
        params["key"] = key
    if node_name is not None:
        params["node_name"] = node_name
    if force is not None:
        params["force"] = force

    try:
        async with StorageScaleClient() as client:
            return await client.delete(
                f"/scalemgmt/v3/troubleshooting/persistentReserve/{device}/keys",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to clear persistent reserve keys for device '{device}': {str(e)}") from e
