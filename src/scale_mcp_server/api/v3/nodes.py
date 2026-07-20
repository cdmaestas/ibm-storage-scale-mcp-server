"""IBM Storage Scale Node operations.

Node endpoints for adding nodes to the cluster, starting/stopping the mmfsd
service, and displaying node status/configuration, following the 6.0.1
native REST API.
"""

from typing import Any

from scale_mcp_server.utils.client import StorageScaleAPIError, StorageScaleClient


def _domain_headers(domain: str | None) -> dict[str, str]:
    """Build request headers for the optional X-StorageScaleDomain."""
    headers: dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain
    return headers


async def add_node_api(
    node_data: dict,
    domain: str | None = None,
) -> Any:
    """Add a node to the IBM Storage Scale cluster.

    Args:
        node_data: Node definition (see scalectl node command)
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the creation status

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/nodes",
                json=node_data,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        name = node_data.get("node_name", "unknown")
        raise StorageScaleAPIError(f"Failed to add node '{name}': {str(e)}") from e


async def batch_add_nodes_api(
    nodes_data: dict,
    domain: str | None = None,
) -> Any:
    """Add one or more nodes to the IBM Storage Scale cluster.

    Args:
        nodes_data: Batch definition, e.g. {"accept_all": true, "nodes": [...]}
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the batch add status

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/nodes:batchAdd",
                json=nodes_data,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to batch add nodes: {str(e)}") from e


async def start_nodes_api(
    start_data: dict | None = None,
    domain: str | None = None,
) -> Any:
    """Start the mmfsd service on one or more nodes.

    Args:
        start_data: Start parameters (see scalectl node command); LRO
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the start operation status

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/nodes:start",
                json=start_data if start_data is not None else {},
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to start nodes: {str(e)}") from e


async def stop_nodes_api(
    stop_data: dict | None = None,
    domain: str | None = None,
) -> Any:
    """Stop the mmfsd service on one or more nodes.

    Args:
        stop_data: Stop parameters (see scalectl node command); LRO
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the stop operation status

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/nodes:stop",
                json=stop_data if stop_data is not None else {},
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to stop nodes: {str(e)}") from e


async def get_nodes_status_api(
    target_nodes: str | None = None,
    domain: str | None = None,
) -> Any:
    """Check the mmfsd status of cluster nodes.

    Args:
        target_nodes: Target nodes (node numbers, ranges, names, IPs, classes)
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing node status information

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    params: dict[str, Any] = {}
    if target_nodes is not None:
        params["target_nodes"] = target_nodes

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                "/scalemgmt/v3/nodes/status",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to get nodes status: {str(e)}") from e


async def get_nodes_config_api(
    domain: str | None = None,
) -> Any:
    """List the configuration details about the node.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing node configuration

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.get("/scalemgmt/v3/nodes/config", headers=_domain_headers(domain))
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to get nodes config: {str(e)}") from e
