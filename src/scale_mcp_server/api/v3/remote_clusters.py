"""IBM Storage Scale Remote Cluster operations.

Remote cluster endpoints (/scalemgmt/v3/clusters/remote...) for managing
owning/accessing cluster relationships, following the 6.0.1 native REST API.
"""

from typing import Any

from scale_mcp_server.utils.client import StorageScaleAPIError, StorageScaleClient


def _domain_headers(domain: str | None) -> dict[str, str]:
    """Build request headers for the optional X-StorageScaleDomain."""
    headers: dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain
    return headers


async def list_remote_clusters_api(
    page_size: int | None = None,
    page_token: str | None = None,
    view: str | None = None,
    domain: str | None = None,
) -> Any:
    """List remote clusters known to the accessing cluster.

    Args:
        page_size: Number of items to return per request
        page_token: Token to navigate to the next page
        view: View for remote cluster contents ('basic' or 'full')
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing remote cluster information

    Raises:
        StorageScaleAPIError: If API call fails
    """
    params: dict[str, Any] = {}
    if page_size is not None:
        params["page_size"] = page_size
    if page_token is not None:
        params["page_token"] = page_token
    if view is not None:
        params["view"] = view

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                "/scalemgmt/v3/clusters/remote",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to list remote clusters: {str(e)}") from e


async def get_remote_cluster_api(
    name: str,
    view: str | None = None,
    domain: str | None = None,
) -> Any:
    """Retrieve details about a remote cluster.

    Args:
        name: Remote cluster name
        view: View for remote cluster contents ('basic' or 'full')
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing remote cluster details

    Raises:
        StorageScaleAPIError: If API call fails
    """
    params: dict[str, Any] = {}
    if view is not None:
        params["view"] = view

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/clusters/remote/{name}",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to get remote cluster '{name}': {str(e)}") from e


async def add_remote_cluster_api(
    remote_cluster: dict,
    domain: str | None = None,
) -> Any:
    """Add an owning cluster to the set of remote clusters known to this cluster.

    Args:
        remote_cluster: Remote cluster definition; required parameters are
            'name' and 'contact-nodes'
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the creation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/clusters/remote",
                json=remote_cluster,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        name = remote_cluster.get("name", "unknown")
        raise StorageScaleAPIError(f"Failed to add remote cluster '{name}': {str(e)}") from e


async def update_remote_cluster_api(
    name: str,
    remote_cluster: dict,
    resource_update: bool | None = None,
    domain: str | None = None,
) -> Any:
    """Update information associated with a remote cluster.

    Args:
        name: Remote cluster name
        remote_cluster: Updated remote cluster definition
        resource_update: Update the resource authorization information
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the update status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    params: dict[str, Any] = {}
    if resource_update is not None:
        params["resource_update"] = resource_update

    try:
        async with StorageScaleClient() as client:
            return await client.patch(
                f"/scalemgmt/v3/clusters/remote/{name}",
                json=remote_cluster,
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to update remote cluster '{name}': {str(e)}") from e


async def delete_remote_cluster_api(
    name: str,
    force: bool | None = None,
    domain: str | None = None,
) -> Any:
    """Delete an owning cluster definition from the accessing cluster.

    Args:
        name: Remote cluster name
        force: Force deletion of the owning cluster definition
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the deletion status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    params: dict[str, Any] = {}
    if force is not None:
        params["force"] = force

    try:
        async with StorageScaleClient() as client:
            return await client.delete(
                f"/scalemgmt/v3/clusters/remote/{name}",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to delete remote cluster '{name}': {str(e)}") from e


async def authorize_remote_cluster_api(
    authorization: dict,
    domain: str | None = None,
) -> Any:
    """Authorize an accessing cluster to access resources on the owning cluster.

    Args:
        authorization: Authorization definition; required parameter is 'name'.
            If filesystem_resources or fileset_resources are provided,
            disposition 'GRANT' is required.
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the authorization status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/clusters/remote/authorized",
                json=authorization,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        name = authorization.get("name", "unknown")
        raise StorageScaleAPIError(f"Failed to authorize remote cluster '{name}': {str(e)}") from e


async def deauthorize_remote_cluster_api(
    name: str,
    domain: str | None = None,
) -> Any:
    """Delete the authorization of an accessing cluster on the owning cluster.

    Args:
        name: Remote cluster name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the deletion status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.delete(
                f"/scalemgmt/v3/clusters/remote/authorized/{name}",
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to deauthorize remote cluster '{name}': {str(e)}") from e


async def refresh_remote_cluster_api(
    name: str,
    domain: str | None = None,
) -> Any:
    """Refresh the information of an owning cluster on the accessing cluster.

    Initiates a new cluster key exchange protocol for an existing owning
    cluster definition.

    Args:
        name: Remote cluster name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the refresh status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/clusters/remote/{name}/refresh",
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to refresh remote cluster '{name}': {str(e)}") from e
