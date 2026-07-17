"""IBM Storage Scale Cluster operations.

Cluster endpoints for creating and managing the local cluster, following the
6.0.1 native REST API. Remote cluster endpoints live in remote_clusters.py.
"""

from typing import Any

from scale_mcp_server.utils.client import StorageScaleAPIError, StorageScaleClient


def _domain_headers(domain: str | None) -> dict[str, str]:
    """Build request headers for the optional X-StorageScaleDomain."""
    headers: dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain
    return headers


async def list_clusters_api(
    view: str | None = None,
    domain: str | None = None,
) -> Any:
    """List information about the local cluster.

    Args:
        view: Level of detail to return (basic, ces, cnfs, node-comments)
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing cluster information

    Raises:
        StorageScaleAPIError: If API call fails
    """
    params: dict[str, Any] = {}
    if view:
        params["view"] = view

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                "/scalemgmt/v3/clusters",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to list clusters: {str(e)}") from e


async def create_cluster_api(
    cluster_data: dict,
    domain: str | None = None,
) -> Any:
    """Create an IBM Storage Scale cluster.

    When a cluster is created, the first node is automatically designated as
    both a quorum and manager node.

    Args:
        cluster_data: Cluster definition (see scalectl cluster command)
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the creation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/clusters",
                json=cluster_data,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to create cluster: {str(e)}") from e


async def migrate_cluster_api(
    precheck: bool | None = None,
    domain: str | None = None,
) -> Any:
    """Migrate a legacy cluster to the native REST API.

    Args:
        precheck: Run a cluster migration precheck only
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the migration status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    body: dict[str, Any] = {}
    if precheck is not None:
        body["precheck"] = precheck

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/clusters:migrate",
                json=body,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to migrate cluster: {str(e)}") from e


async def list_cluster_trust_api(
    end_point: str | None = None,
    domain: str | None = None,
) -> Any:
    """List all CA chains that are currently trusted by the local cluster.

    Args:
        end_point: Filter the results by the specified endpoint subject name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing trusted CA chain information

    Raises:
        StorageScaleAPIError: If API call fails
    """
    params: dict[str, Any] = {}
    if end_point is not None:
        params["end_point"] = end_point

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                "/scalemgmt/v3/clusters/trust",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to list cluster trust: {str(e)}") from e
