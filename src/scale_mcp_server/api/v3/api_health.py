"""IBM Storage Scale API Health operations.

API-health endpoints for the health status of the administration daemon
(scaleadmd) on cluster nodes, following the 6.0.1 native REST API.
"""

from typing import Optional, Any, Dict
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


def _domain_headers(domain: Optional[str]) -> Dict[str, str]:
    """Build request headers for the optional X-StorageScaleDomain."""
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain
    return headers


async def get_api_health_api(
    page_size: Optional[int] = None,
    page_token: Optional[str] = None,
    domain: Optional[str] = None,
) -> Any:
    """List the health status of the native REST API services on nodes.

    Args:
        page_size: Number of items to return per request
        page_token: Token to navigate to the next page
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing API health status information

    Raises:
        StorageScaleAPIError: If API call fails
    """
    params: Dict[str, Any] = {}
    if page_size is not None:
        params["page_size"] = page_size
    if page_token is not None:
        params["page_token"] = page_token

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                "/scalemgmt/v3/apihealth",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to get API health: {str(e)}") from e


async def get_node_api_health_api(
    node_name: str,
    domain: Optional[str] = None,
) -> Any:
    """Get the health status of the native REST API service on a node.

    Args:
        node_name: Node name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the node's API health status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/apihealth/{node_name}",
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get API health for node '{node_name}': {str(e)}"
        ) from e
