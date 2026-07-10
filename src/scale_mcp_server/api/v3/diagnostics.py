"""IBM Storage Scale Diagnostic operations."""

from typing import Optional, Any, Dict
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


async def get_node_version_api(
    node: str,
    domain: Optional[str] = None,
) -> Any:
    """Get version information for a specific node.

    Args:
        node: Node name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing node version information

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/nodes/{node}/diagnostics/version", headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get version for node '{node}': {str(e)}"
        ) from e


async def collect_diagnostics_api(
    options: Optional[dict] = None,
    domain: Optional[str] = None,
) -> Any:
    """Collect diagnostic information from the cluster.

    Args:
        options: Optional diagnostic collection options
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing diagnostic collection status

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    body = options if options is not None else {}

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/diagnostics:collect", json=body, headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to collect diagnostics: {str(e)}"
        ) from e


async def get_diagnostics_status_api(
    job_id: str,
    domain: Optional[str] = None,
) -> Any:
    """Get status of a diagnostic collection job.

    Args:
        job_id: Diagnostic job identifier
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing diagnostic job status

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/diagnostics/{job_id}", headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get diagnostics status for job '{job_id}': {str(e)}"
        ) from e
