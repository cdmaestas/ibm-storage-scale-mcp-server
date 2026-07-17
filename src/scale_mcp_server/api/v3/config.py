"""IBM Storage Scale Configuration operations.

Configuration endpoints for the administration daemon (scaleadmd) and IO
daemon (mmfsd) settings, following the 6.0.1 native REST API.
"""

from typing import Any

from scale_mcp_server.utils.client import StorageScaleAPIError, StorageScaleClient


def _domain_headers(domain: str | None) -> dict[str, str]:
    """Build request headers for the optional X-StorageScaleDomain."""
    headers: dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain
    return headers


async def get_admin_config_api(
    page_size: int | None = None,
    page_token: str | None = None,
    running: bool | None = None,
    domain: str | None = None,
) -> Any:
    """List the configuration data for the administration daemon (scaleadmd).

    Args:
        page_size: Number of items to return per request
        page_token: Token to navigate to the next page
        running: Display the configuration value running on the node
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the admin daemon configuration

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    params: dict[str, Any] = {}
    if page_size is not None:
        params["page_size"] = page_size
    if page_token is not None:
        params["page_token"] = page_token
    if running is not None:
        params["running"] = running

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                "/scalemgmt/v3/config/admin",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to get admin config: {str(e)}") from e


async def get_admin_config_attribute_api(
    name: str,
    running: bool | None = None,
    domain: str | None = None,
) -> Any:
    """Get the admin daemon configuration value for a specified attribute.

    Args:
        name: Attribute name
        running: Display the configuration value running on the node
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the attribute value

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    params: dict[str, Any] = {}
    if running is not None:
        params["running"] = running

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/config/admin/{name}",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to get admin config attribute '{name}': {str(e)}") from e


async def update_admin_config_api(
    config_data: dict,
    domain: str | None = None,
) -> Any:
    """Batch-update configuration values of the administration daemon.

    Args:
        config_data: Configuration updates to apply
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the update status

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.patch(
                "/scalemgmt/v3/config/admin:batchUpdate",
                json=config_data,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to update admin config: {str(e)}") from e


async def get_cluster_config_api(
    view: str | None = None,
    page_size: int | None = None,
    page_token: str | None = None,
    running: bool | None = None,
    domain: str | None = None,
) -> Any:
    """List the configuration data for the IO daemon (mmfsd).

    Args:
        view: View for configuration values (ALL, AFM, NSD_RAID, TRACE, MMHEALTH)
        page_size: Number of items to return per request
        page_token: Token to navigate to the next page
        running: Display the configuration value running on the node
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the cluster (IO daemon) configuration

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    params: dict[str, Any] = {}
    if view is not None:
        params["view"] = view
    if page_size is not None:
        params["page_size"] = page_size
    if page_token is not None:
        params["page_token"] = page_token
    if running is not None:
        params["running"] = running

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                "/scalemgmt/v3/config/cluster",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to get cluster config: {str(e)}") from e


async def get_cluster_config_attribute_api(
    name: str,
    running: bool | None = None,
    domain: str | None = None,
) -> Any:
    """Get the IO daemon configuration value for a specified attribute.

    Args:
        name: Attribute name
        running: Display the configuration value running on the node
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the attribute value

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    params: dict[str, Any] = {}
    if running is not None:
        params["running"] = running

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/config/cluster/{name}",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to get cluster config attribute '{name}': {str(e)}") from e


async def update_cluster_config_api(
    config_data: dict,
    domain: str | None = None,
) -> Any:
    """Batch-update configuration values of the IO daemon (mmfsd).

    Args:
        config_data: Configuration updates to apply
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the update status

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.patch(
                "/scalemgmt/v3/config/cluster:batchUpdate",
                json=config_data,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to update cluster config: {str(e)}") from e
