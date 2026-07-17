"""IBM Storage Scale Diagnostic operations.

Diagnostics endpoints following the 6.0.1 native REST API: the mmfsd version
report of a node.
"""

from typing import Any

from scale_mcp_server.utils.client import StorageScaleAPIError, StorageScaleClient


async def get_node_version_api(
    node: str,
    domain: str | None = None,
) -> Any:
    """Get the mmfsd version of a node.

    Args:
        node: Node name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing node version information

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers: dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(f"/scalemgmt/v3/nodes/{node}/diagnostics/version", headers=headers)
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to get version for node '{node}': {str(e)}") from e
