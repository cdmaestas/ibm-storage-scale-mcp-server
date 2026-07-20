"""IBM Storage Scale Quota operations.

Quota endpoints for managing quota information for file systems and filesets,
following the 6.0.1 native REST API.
"""

from typing import Any

from scale_mcp_server.utils.client import StorageScaleAPIError, StorageScaleClient


def _domain_headers(domain: str | None) -> dict[str, str]:
    """Build request headers for the optional X-StorageScaleDomain."""
    headers: dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain
    return headers


async def list_quotas_api(
    filesystem: str,
    page_size: int | None = None,
    page_token: str | None = None,
    show_perfileset_quotas: bool | None = None,
    default: bool | None = None,
    filter: str | None = None,
    domain: str | None = None,
) -> Any:
    """Retrieve quota information for a file system.

    Args:
        filesystem: Filesystem name
        page_size: Number of items per page
        page_token: Token for pagination
        show_perfileset_quotas: Show per-fileset quotas
        default: Show default quota limits
        filter: Filter expression for quotas
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing quota information

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    params: dict[str, Any] = {}
    if page_size is not None:
        params["page_size"] = page_size
    if page_token is not None:
        params["page_token"] = page_token
    if show_perfileset_quotas is not None:
        params["show_perfileset_quotas"] = show_perfileset_quotas
    if default is not None:
        params["default"] = default
    if filter is not None:
        params["filter"] = filter

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/quotas",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to list quotas for filesystem '{filesystem}': {str(e)}") from e


async def set_quota_api(
    filesystem: str,
    quota_data: dict,
    default: bool | None = None,
    domain: str | None = None,
) -> Any:
    """Set quota limits for a file system.

    Args:
        filesystem: Filesystem name
        quota_data: Quota definition, e.g. {"quota": {"name": ..., "type":
            "QUOTA_TYPE_USER", "block_soft_limit_bytes": ..., ...}}
        default: Set default quota limits for user, group, and fileset types
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the operation status

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    params: dict[str, Any] = {}
    if default is not None:
        params["default"] = default

    try:
        async with StorageScaleClient() as client:
            return await client.put(
                f"/scalemgmt/v3/filesystems/{filesystem}/quotas",
                json=quota_data,
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to set quota for filesystem '{filesystem}': {str(e)}") from e


async def check_quotas_api(
    filesystem: str,
    check_data: dict | None = None,
    domain: str | None = None,
) -> Any:
    """Check quotas for a file system (mmcheckquota equivalent).

    Args:
        filesystem: Filesystem name
        check_data: Check parameters, e.g. {"verbose": true, "threads": 16,
            "report_diff": true, "target_nodes": [...], "qos_class": ...}
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the check operation status

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{filesystem}/quotas",
                json=check_data if check_data is not None else {},
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to check quotas for filesystem '{filesystem}': {str(e)}") from e


async def update_quota_config_api(
    filesystem: str,
    config_data: dict,
    domain: str | None = None,
) -> Any:
    """Update quota configuration settings for a file system.

    Configures default quotas and enforcement for users, groups, or filesets.

    Args:
        filesystem: Filesystem name
        config_data: Quota configuration, e.g. {"default_quotas": "YES",
            "enforcement": "YES", "quota_type": ["QUOTA_TYPE_USER"]}
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the operation status

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{filesystem}/quotas/config",
                json=config_data,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to update quota config for filesystem '{filesystem}': {str(e)}") from e


async def list_fileset_quotas_api(
    filesystem: str,
    fileset: str,
    page_size: int | None = None,
    page_token: str | None = None,
    default: bool | None = None,
    domain: str | None = None,
) -> Any:
    """Retrieve quota information for a specific fileset.

    Args:
        filesystem: Filesystem name
        fileset: Fileset name
        page_size: Number of items per page
        page_token: Token for pagination
        default: Show default quota limits
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing fileset quota information

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    params: dict[str, Any] = {}
    if page_size is not None:
        params["page_size"] = page_size
    if page_token is not None:
        params["page_token"] = page_token
    if default is not None:
        params["default"] = default

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/quotas",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to list quotas for fileset '{fileset}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def set_fileset_quota_api(
    filesystem: str,
    fileset: str,
    quota_data: dict,
    default: bool | None = None,
    domain: str | None = None,
) -> Any:
    """Set quota limits for a specific fileset.

    Args:
        filesystem: Filesystem name
        fileset: Fileset name
        quota_data: Quota definition, e.g. {"quota": {"name": ..., "type":
            "QUOTA_TYPE_USER", "block_soft_limit_bytes": ..., ...}}
        default: Set default quota limits for user and group quota types
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the operation status

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    params: dict[str, Any] = {}
    if default is not None:
        params["default"] = default

    try:
        async with StorageScaleClient() as client:
            return await client.put(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/quotas",
                json=quota_data,
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to set quota for fileset '{fileset}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def check_fileset_quotas_api(
    filesystem: str,
    fileset: str,
    check_data: dict | None = None,
    domain: str | None = None,
) -> Any:
    """Check user and group quotas for a specific fileset.

    Args:
        filesystem: Filesystem name
        fileset: Fileset name
        check_data: Check parameters, e.g. {"verbose": true, "threads": 16,
            "report_diff": true, "target_nodes": [...], "qos_class": ...}
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the check operation status

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/quotas",
                json=check_data if check_data is not None else {},
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to check quotas for fileset '{fileset}' in filesystem '{filesystem}': {str(e)}"
        ) from e
