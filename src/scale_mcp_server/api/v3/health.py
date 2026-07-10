"""IBM Storage Scale Health and Diagnostics operations (v3 API).

Note: The v3 API does not have dedicated /health endpoints like v2.
Instead, health information is obtained through:
- Node status endpoints (/nodes/status)
- Filesystem details endpoints (/filesystems/{name})
- Diagnostics endpoints (/nodes/{node}/diagnostics/*)
"""

from typing import Optional, Any, Dict
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


async def get_filesystem_health_api(
    filesystem: str,
    domain: Optional[str] = None,
) -> Any:
    """Get health information for a filesystem.

    In v3 API, filesystem health is obtained from the filesystem details endpoint.
    This provides mount status, capacity, and operational state.

    Args:
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing filesystem information including health indicators

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            result = await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}", headers=headers
            )
            # Extract health-relevant information
            if result and "filesystems" in result:
                fs_data = result["filesystems"][0] if result["filesystems"] else {}
                return {
                    "filesystem": filesystem,
                    "mount": {
                        "status": fs_data.get("mount", {}).get("status"),
                        "nodes": fs_data.get("mount", {}).get("nodes", []),
                    },
                    "config": {
                        "defaultMountPoint": fs_data.get("config", {}).get(
                            "defaultMountPoint"
                        ),
                        "automaticMountOption": fs_data.get("config", {}).get(
                            "automaticMountOption"
                        ),
                    },
                    "capacity": fs_data.get("capacity", {}),
                }
            return result
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get health information for filesystem '{filesystem}': {str(e)}"
        ) from e


async def get_node_health_api(
    node: Optional[str] = None,
    domain: Optional[str] = None,
) -> Any:
    """Get health/status information for nodes.

    In v3 API, node health is obtained from the nodes status endpoint.
    This provides daemon status, quorum status, and operational state.

    Args:
        node: Specific node name, or None for all nodes
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing node status information

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            result = await client.get("/scalemgmt/v3/nodes/status", headers=headers)

            # If specific node requested, filter the results
            if node and result and "nodes" in result:
                filtered_nodes = [
                    n for n in result["nodes"] if n.get("name") == node
                ]
                if filtered_nodes:
                    return {"nodes": filtered_nodes}
                else:
                    raise StorageScaleAPIError(f"Node '{node}' not found")

            return result
    except StorageScaleAPIError as e:
        node_info = f" for node '{node}'" if node else ""
        raise StorageScaleAPIError(
            f"Failed to get health/status information{node_info}: {str(e)}"
        ) from e


async def get_node_diagnostics_api(
    node: str,
    domain: Optional[str] = None,
) -> Any:
    """Get diagnostic information for a specific node.

    Args:
        node: Node name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing node diagnostic information including version

    Raises:
        StorageScaleAPIError: If API call fails
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
            f"Failed to get diagnostics for node '{node}': {str(e)}"
        ) from e


async def get_cluster_health_summary_api(
    domain: Optional[str] = None,
) -> Any:
    """Get overall cluster health summary.

    Combines information from multiple endpoints to provide a health overview.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing cluster health summary

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            # Get nodes status
            nodes_status = await client.get(
                "/scalemgmt/v3/nodes/status", headers=headers
            )

            # Get filesystems list
            filesystems = await client.get(
                "/scalemgmt/v3/filesystems", headers=headers
            )

            # Compile health summary
            summary = {
                "nodes": {
                    "total": len(nodes_status.get("nodes", [])),
                    "active": sum(
                        1
                        for n in nodes_status.get("nodes", [])
                        if n.get("status", {}).get("daemon") == "active"
                    ),
                    "details": nodes_status.get("nodes", []),
                },
                "filesystems": {
                    "total": len(filesystems.get("filesystems", [])),
                    "mounted": sum(
                        1
                        for fs in filesystems.get("filesystems", [])
                        if fs.get("mount", {}).get("status") == "mounted"
                    ),
                    "details": filesystems.get("filesystems", []),
                },
            }

            return summary
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get cluster health summary: {str(e)}"
        ) from e
