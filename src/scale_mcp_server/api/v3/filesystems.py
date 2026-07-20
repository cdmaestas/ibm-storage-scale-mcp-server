"""IBM Storage Scale Filesystem operations.

File system endpoints, including mount state, rebalance/restripe, and
directory operations, following the 6.0.1 native REST API.
"""

from typing import Any

from scale_mcp_server.utils.client import StorageScaleAPIError, StorageScaleClient


def _domain_headers(domain: str | None) -> dict[str, str]:
    """Build request headers for the optional X-StorageScaleDomain."""
    headers: dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain
    return headers


async def list_filesystems_api(
    page_size: int | None = None,
    page_token: str | None = None,
    domain: str | None = None,
) -> Any:
    """List all filesystems registered in the cluster.

    Args:
        page_size: Number of items to return per request
        page_token: Token to navigate to the next page
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing filesystem information

    Raises:
        StorageScaleAPIError: If API call fails
    """
    params: dict[str, Any] = {}
    if page_size is not None:
        params["page_size"] = page_size
    if page_token is not None:
        params["page_token"] = page_token

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                "/scalemgmt/v3/filesystems",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to list filesystems: {str(e)}") from e


async def get_filesystem_api(
    filesystem: str,
    domain: str | None = None,
) -> Any:
    """Get detailed information about a specific filesystem.

    Args:
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing detailed filesystem information

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}",
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to get filesystem '{filesystem}': {str(e)}") from e


async def create_filesystem_api(
    filesystem_data: dict,
    domain: str | None = None,
) -> Any:
    """Create a new filesystem.

    Args:
        filesystem_data: Filesystem configuration data
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing created filesystem information

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/filesystems",
                json=filesystem_data,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        fs_name = filesystem_data.get("name", "unknown")
        raise StorageScaleAPIError(f"Failed to create filesystem '{fs_name}': {str(e)}") from e


async def update_filesystem_api(
    filesystem: str,
    filesystem_data: dict,
    domain: str | None = None,
) -> Any:
    """Update the attributes of a filesystem.

    Some attributes (name, default_mount_point, drive_letter, dmapi_enabled,
    maintenance_mode, ...) require the file system to be unmounted.

    Args:
        filesystem: Filesystem name
        filesystem_data: Updated filesystem attributes
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing updated filesystem information

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.patch(
                f"/scalemgmt/v3/filesystems/{filesystem}",
                json=filesystem_data,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to update filesystem '{filesystem}': {str(e)}") from e


async def delete_filesystem_api(
    name: str,
    permanently_damaged: bool | None = None,
    domain: str | None = None,
) -> Any:
    """Delete a filesystem.

    Args:
        name: Filesystem name
        permanently_damaged: Proceed with deletion even if disks are
            permanently damaged
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing deletion status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    params: dict[str, Any] = {}
    if permanently_damaged is not None:
        params["permanently_damaged"] = permanently_damaged

    try:
        async with StorageScaleClient() as client:
            return await client.delete(
                f"/scalemgmt/v3/filesystems/{name}",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to delete filesystem '{name}': {str(e)}") from e


async def get_mount_status_api(
    filesystem: str,
    cluster_name: str | None = None,
    domain: str | None = None,
) -> Any:
    """List the mount state of a filesystem.

    Includes the type of mount and the nodes where the file system is mounted.

    Args:
        filesystem: Filesystem name
        cluster_name: Cluster name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the mount state

    Raises:
        StorageScaleAPIError: If API call fails
    """
    params: dict[str, Any] = {}
    if cluster_name is not None:
        params["cluster_name"] = cluster_name

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}:mount",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to get mount status for filesystem '{filesystem}': {str(e)}") from e


async def mount_filesystem_api(
    name: str,
    mount_data: dict | None = None,
    domain: str | None = None,
) -> Any:
    """Mount a filesystem on one or more nodes.

    If no target nodes are specified, the file system is mounted only on the
    node where the request is issued.

    Args:
        name: Filesystem name
        mount_data: Mount parameters, e.g. {"mount_options": ...,
            "mount_point": ..., "target_nodes": [...]}
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing mount operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{name}:mount",
                json=mount_data if mount_data is not None else {},
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to mount filesystem '{name}': {str(e)}") from e


async def unmount_filesystem_api(
    name: str,
    unmount_data: dict | None = None,
    domain: str | None = None,
) -> Any:
    """Unmount a filesystem from one or more nodes.

    If no target nodes are specified, the file system is unmounted only from
    the node where the request is issued.

    Args:
        name: Filesystem name
        unmount_data: Unmount parameters, e.g. {"force": ...,
            "target_nodes": [...]}
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing unmount operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{name}:unmount",
                json=unmount_data if unmount_data is not None else {},
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to unmount filesystem '{name}': {str(e)}") from e


async def mount_all_filesystems_api(
    mount_data: dict | None = None,
    domain: str | None = None,
) -> Any:
    """Mount all existing filesystems.

    Args:
        mount_data: Mount parameters, e.g. {"mount_options": ...,
            "target_nodes": [...]}
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing mount operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/filesystems:mount",
                json=mount_data if mount_data is not None else {},
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to mount all filesystems: {str(e)}") from e


async def unmount_all_filesystems_api(
    unmount_data: dict | None = None,
    domain: str | None = None,
) -> Any:
    """Unmount all filesystems on one or more nodes.

    Args:
        unmount_data: Unmount parameters, e.g. {"force": ...,
            "target_nodes": [...]}
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing unmount operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/filesystems:unmount",
                json=unmount_data if unmount_data is not None else {},
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to unmount all filesystems: {str(e)}") from e


async def rebalance_filesystem_api(
    filesystem: str,
    rebalance_strategy: str | None = None,
    metadata_only: bool | None = None,
    target_nodes: str | None = None,
    pit_continue_on_error: bool | None = None,
    qos_class: str | None = None,
    domain: str | None = None,
) -> Any:
    """Rebalance the filesystem by distributing file blocks evenly across disks.

    Args:
        filesystem: Filesystem name
        rebalance_strategy: Rebalance strategy ('strict', 'no_rebalance',
            'default')
        metadata_only: Limit the operation to metadata blocks
        target_nodes: Target nodes (node numbers, ranges, names, IPs, classes)
        pit_continue_on_error: Continue repairing remaining files on PIT errors
        qos_class: Quality of service class for IO operations
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the rebalance operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    params: dict[str, Any] = {}
    if rebalance_strategy is not None:
        params["rebalance_strategy"] = rebalance_strategy
    if metadata_only is not None:
        params["metadata_only"] = metadata_only
    if target_nodes is not None:
        params["target_nodes"] = target_nodes
    if pit_continue_on_error is not None:
        params["pit_continue_on_error"] = pit_continue_on_error
    if qos_class is not None:
        params["qos_class"] = qos_class

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{filesystem}:rebalance",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to rebalance filesystem '{filesystem}': {str(e)}") from e


async def restripe_filesystem_api(
    filesystem: str,
    restripe_operation: str | None = None,
    metadata_only: bool | None = None,
    target_nodes: str | None = None,
    pit_continue_on_error: bool | None = None,
    qos_class: str | None = None,
    domain: str | None = None,
) -> Any:
    """Restripe the filesystem, restoring replication of all files.

    Also completes any incomplete or deferred file compression or
    decompression and redistributes data based on disk state changes.

    Args:
        filesystem: Filesystem name
        restripe_operation: Restripe operation strategy
        metadata_only: Limit the operation to metadata blocks
        target_nodes: Target nodes (node numbers, ranges, names, IPs, classes)
        pit_continue_on_error: Continue repairing remaining files on PIT errors
        qos_class: Quality of service class for IO operations
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the restripe operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    params: dict[str, Any] = {}
    if restripe_operation is not None:
        params["restripe_operation"] = restripe_operation
    if metadata_only is not None:
        params["metadata_only"] = metadata_only
    if target_nodes is not None:
        params["target_nodes"] = target_nodes
    if pit_continue_on_error is not None:
        params["pit_continue_on_error"] = pit_continue_on_error
    if qos_class is not None:
        params["qos_class"] = qos_class

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{filesystem}:restripe",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to restripe filesystem '{filesystem}': {str(e)}") from e


async def list_directory_api(
    filesystem: str,
    dirpath: str,
    page_size: int | None = None,
    page_token: str | None = None,
    domain: str | None = None,
) -> Any:
    """Get information about the contents of a filesystem directory.

    Args:
        filesystem: Filesystem name
        dirpath: Path of the filesystem directory
        page_size: Number of items to return per request
        page_token: Token to navigate to the next page
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the directory contents

    Raises:
        StorageScaleAPIError: If API call fails
    """
    params: dict[str, Any] = {}
    if page_size is not None:
        params["page_size"] = page_size
    if page_token is not None:
        params["page_token"] = page_token

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/directory/{dirpath}",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to list directory '{dirpath}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def stat_directory_api(
    filesystem: str,
    dirpath: str,
    domain: str | None = None,
) -> Any:
    """Get detailed information (stat) of a filesystem directory.

    Args:
        filesystem: Filesystem name
        dirpath: Path of the filesystem directory
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing directory stat details

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/directory/{dirpath}:stat",
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to stat directory '{dirpath}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def create_directory_api(
    filesystem: str,
    dirpath: str,
    directory_data: dict | None = None,
    domain: str | None = None,
) -> Any:
    """Create a filesystem directory.

    Args:
        filesystem: Filesystem name
        dirpath: Path of the filesystem directory to create
        directory_data: Directory creation parameters
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the creation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{filesystem}/directory/{dirpath}",
                json=directory_data if directory_data is not None else {},
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to create directory '{dirpath}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def delete_directory_api(
    filesystem: str,
    dirpath: str,
    force: bool | None = None,
    domain: str | None = None,
) -> Any:
    """Delete a directory from a mounted filesystem.

    Fileset junction directories and directories containing immutable files
    cannot be deleted.

    Args:
        filesystem: Filesystem name
        dirpath: Path of the filesystem directory to delete
        force: Forcefully delete the directory even if it is not empty
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
                f"/scalemgmt/v3/filesystems/{filesystem}/directory/{dirpath}",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to delete directory '{dirpath}' in filesystem '{filesystem}': {str(e)}"
        ) from e
