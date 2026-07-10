"""IBM Storage Scale API Health operations.

API health endpoints for monitoring the REST API service status and availability.
"""

from typing import Optional, Any, Dict
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


async def get_api_health_api(
    domain: Optional[str] = None,
) -> Any:
    """Get API health status.

    Checks the health and availability of the Scale REST API service.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing API health status information

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get("/scalemgmt/v3/apihealth", headers=headers)
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to get API health: {str(e)}") from e


async def get_api_status_api(
    domain: Optional[str] = None,
) -> Any:
    """Get detailed API status information.

    Retrieves detailed status information about the Scale REST API service
    including version, uptime, and service state.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing detailed API status information

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get("/scalemgmt/v3/apihealth/status", headers=headers)
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to get API status: {str(e)}") from e
