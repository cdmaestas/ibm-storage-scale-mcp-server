"""IBM Storage Scale Configuration operations."""

from typing import Optional, Any, Dict
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


async def list_config_api(
    domain: Optional[str] = None,
) -> Any:
    """List all configuration parameters.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing configuration parameters

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get("/scalemgmt/v3/config", headers=headers)
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to list configuration: {str(e)}") from e


async def get_config_parameter_api(
    parameter: str,
    domain: Optional[str] = None,
) -> Any:
    """Get a specific configuration parameter.

    Args:
        parameter: Configuration parameter name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing parameter value

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/config/{parameter}", headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get configuration parameter '{parameter}': {str(e)}"
        ) from e


async def update_config_parameter_api(
    parameter: str,
    value_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Update a specific configuration parameter.

    Args:
        parameter: Configuration parameter name
        value_data: New parameter value
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing updated parameter

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.put(
                f"/scalemgmt/v3/config/{parameter}", json=value_data, headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to update configuration parameter '{parameter}': {str(e)}"
        ) from e


async def get_admin_config_api(
    domain: Optional[str] = None,
) -> Any:
    """Get admin configuration.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing admin configuration

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get("/scalemgmt/v3/config/admin", headers=headers)
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get admin configuration: {str(e)}"
        ) from e


async def update_admin_config_api(
    config_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Batch update admin configuration.

    Args:
        config_data: Configuration data (BatchUpdateAdminConfigRequest)
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing updated configuration

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.patch(
                "/scalemgmt/v3/config/admin:batchUpdate",
                json=config_data,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to update admin configuration: {str(e)}"
        ) from e
