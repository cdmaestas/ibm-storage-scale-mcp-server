"""IBM Storage Scale Remote Cluster operations.

Remote cluster endpoints for managing multi-cluster configurations and operations.
"""

from typing import Optional, Any, Dict
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


async def list_remote_clusters_api(
    domain: Optional[str] = None,
) -> Any:
    """List all remote clusters.

    Retrieves a list of all remote clusters configured in the system.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing list of remote clusters

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get("/scalemgmt/v3/remoteclusters", headers=headers)
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to list remote clusters: {str(e)}") from e


async def get_remote_cluster_api(
    cluster: str,
    domain: Optional[str] = None,
) -> Any:
    """Get details of a specific remote cluster.

    Retrieves detailed information about a specific remote cluster.

    Args:
        cluster: Remote cluster name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing remote cluster details

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/remoteclusters/{cluster}", headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get remote cluster '{cluster}': {str(e)}"
        ) from e


async def add_remote_cluster_api(
    cluster_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Add a new remote cluster.

    Adds a new remote cluster configuration.

    Args:
        cluster_data: Remote cluster configuration data
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/remoteclusters", json=cluster_data, headers=headers
            )
    except StorageScaleAPIError as e:
        cluster_name = cluster_data.get("name", "unknown")
        raise StorageScaleAPIError(
            f"Failed to add remote cluster '{cluster_name}': {str(e)}"
        ) from e


async def update_remote_cluster_api(
    cluster: str,
    cluster_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Update remote cluster configuration.

    Updates the configuration of a specific remote cluster.

    Args:
        cluster: Remote cluster name
        cluster_data: Updated cluster configuration data
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing update status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.put(
                f"/scalemgmt/v3/remoteclusters/{cluster}",
                json=cluster_data,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to update remote cluster '{cluster}': {str(e)}"
        ) from e


async def delete_remote_cluster_api(
    cluster: str,
    domain: Optional[str] = None,
) -> Any:
    """Delete a remote cluster.

    Removes the specified remote cluster configuration.

    Args:
        cluster: Remote cluster name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing deletion status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.delete(
                f"/scalemgmt/v3/remoteclusters/{cluster}", headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to delete remote cluster '{cluster}': {str(e)}"
        ) from e


async def list_remote_filesystems_api(
    cluster: str,
    domain: Optional[str] = None,
) -> Any:
    """List filesystems on a remote cluster.

    Retrieves a list of filesystems available on the specified remote cluster.

    Args:
        cluster: Remote cluster name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing list of remote filesystems

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/remoteclusters/{cluster}/filesystems", headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to list filesystems for remote cluster '{cluster}': {str(e)}"
        ) from e


async def get_remote_filesystem_api(
    cluster: str,
    filesystem: str,
    domain: Optional[str] = None,
) -> Any:
    """Get details of a filesystem on a remote cluster.

    Retrieves detailed information about a specific filesystem on a remote cluster.

    Args:
        cluster: Remote cluster name
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing remote filesystem details

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/remoteclusters/{cluster}/filesystems/{filesystem}",
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get filesystem '{filesystem}' on remote cluster '{cluster}': {str(e)}"
        ) from e
