"""IBM Storage Scale Filesystem Disk operations.

File system disk endpoints for adding, deleting, and retrieving disks in a
file system, following the 6.0.1 native REST API.
"""

from typing import Optional, Any, Dict
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


def _domain_headers(domain: Optional[str]) -> Dict[str, str]:
    """Build request headers for the optional X-StorageScaleDomain."""
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain
    return headers


async def list_filesystem_disks_api(
    filesystem: str,
    page_size: Optional[int] = None,
    page_token: Optional[str] = None,
    domain: Optional[str] = None,
) -> Any:
    """List all disks in a filesystem.

    Args:
        filesystem: Filesystem name
        page_size: Number of items to return per request
        page_token: Token to navigate to the next page
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing list of filesystem disks

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
                f"/scalemgmt/v3/filesystems/{filesystem}/disks",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to list disks for filesystem '{filesystem}': {str(e)}"
        ) from e


async def get_filesystem_disk_api(
    filesystem: str,
    disk_name: str,
    domain: Optional[str] = None,
) -> Any:
    """Get the current configuration and state of a disk in a filesystem.

    Args:
        filesystem: Filesystem name
        disk_name: Disk name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing disk details

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/disks/{disk_name}",
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get disk '{disk_name}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def add_filesystem_disk_api(
    filesystem: str,
    disk_data: Optional[dict] = None,
    verify_disks: Optional[bool] = None,
    target_nodes: Optional[str] = None,
    domain: Optional[str] = None,
) -> Any:
    """Add disks to a filesystem.

    The file system does not need to be mounted and can be in use.

    Args:
        filesystem: Filesystem name
        disk_data: Disk definition to add
        verify_disks: Verify the disks do not belong to an existing filesystem
        target_nodes: Target nodes (node numbers, ranges, names, IPs, classes)
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the add operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    params: Dict[str, Any] = {}
    if verify_disks is not None:
        params["verify_disks"] = verify_disks
    if target_nodes is not None:
        params["target_nodes"] = target_nodes

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{filesystem}/disks",
                json=disk_data if disk_data is not None else {},
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to add disks to filesystem '{filesystem}': {str(e)}"
        ) from e


async def delete_filesystem_disk_api(
    filesystem: str,
    disk_name: str,
    continue_on_error: bool,
    qos_class: Optional[str] = None,
    rebalance_strategy: Optional[str] = None,
    minimal_copy: Optional[bool] = None,
    preserve_replication: Optional[bool] = None,
    target_nodes: Optional[str] = None,
    permanently_damaged: Optional[bool] = None,
    pit_continue_on_error: Optional[bool] = None,
    domain: Optional[str] = None,
) -> Any:
    """Delete an existing filesystem disk, migrating its data to other disks.

    Args:
        filesystem: Filesystem name
        disk_name: Disk name
        continue_on_error: Continue deleting remaining files on errors
        qos_class: Quality of service class for IO operations
        rebalance_strategy: Rebalance strategy ('strict', 'no_rebalance',
            'default')
        minimal_copy: Minimal copying of data located only on the deleted disk
        preserve_replication: Preserve the replication factor of all files
        target_nodes: Target nodes (node numbers, ranges, names, IPs, classes)
        permanently_damaged: Proceed regardless of permanently damaged disks
        pit_continue_on_error: Continue deleting remaining files on PIT errors
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the delete operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    params: Dict[str, Any] = {"continue_on_error": continue_on_error}
    if qos_class is not None:
        params["qos_class"] = qos_class
    if rebalance_strategy is not None:
        params["rebalance_strategy"] = rebalance_strategy
    if minimal_copy is not None:
        params["minimal_copy"] = minimal_copy
    if preserve_replication is not None:
        params["preserve_replication"] = preserve_replication
    if target_nodes is not None:
        params["target_nodes"] = target_nodes
    if permanently_damaged is not None:
        params["permanently_damaged"] = permanently_damaged
    if pit_continue_on_error is not None:
        params["pit_continue_on_error"] = pit_continue_on_error

    try:
        async with StorageScaleClient() as client:
            return await client.delete(
                f"/scalemgmt/v3/filesystems/{filesystem}/disks/{disk_name}",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to delete disk '{disk_name}' from filesystem '{filesystem}': {str(e)}"
        ) from e


async def batch_add_filesystem_disks_api(
    filesystem: str,
    disks_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Add a batch of disks to a filesystem.

    Args:
        filesystem: Filesystem name
        disks_data: Batch disk definitions
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the batch add status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{filesystem}/disks:batchAdd",
                json=disks_data,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to batch add disks to filesystem '{filesystem}': {str(e)}"
        ) from e


async def batch_delete_filesystem_disks_api(
    filesystem: str,
    disk_names: Optional[str] = None,
    qos_class: Optional[str] = None,
    rebalance_strategy: Optional[str] = None,
    minimal_copy: Optional[bool] = None,
    preserve_replication: Optional[bool] = None,
    target_nodes: Optional[str] = None,
    pit_continues_on_error: Optional[bool] = None,
    domain: Optional[str] = None,
) -> Any:
    """Delete a batch of disks from a filesystem.

    Args:
        filesystem: Filesystem name
        disk_names: Names of the disks to delete
        qos_class: Quality of service class for IO operations
        rebalance_strategy: Rebalance strategy (NO_REBALANCE, DEFAULT_STRATEGY,
            STRICT_STRATEGY)
        minimal_copy: Minimal copying of data located only on deleted disks
        preserve_replication: Preserve replication of all files and metadata
        target_nodes: Target nodes (node numbers, ranges, names, IPs, classes)
        pit_continues_on_error: Continue repairing remaining files on PIT errors
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the batch delete status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    params: Dict[str, Any] = {}
    if disk_names is not None:
        params["disk_names"] = disk_names
    if qos_class is not None:
        params["qos_class"] = qos_class
    if rebalance_strategy is not None:
        params["rebalance_strategy"] = rebalance_strategy
    if minimal_copy is not None:
        params["minimal_copy"] = minimal_copy
    if preserve_replication is not None:
        params["preserve_replication"] = preserve_replication
    if target_nodes is not None:
        params["target_nodes"] = target_nodes
    if pit_continues_on_error is not None:
        params["pit_continues_on_error"] = pit_continues_on_error

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{filesystem}/disks:batchDelete",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to batch delete disks from filesystem '{filesystem}': {str(e)}"
        ) from e


async def get_disks_quorum_api(
    filesystem: str,
    domain: Optional[str] = None,
) -> Any:
    """List information about the file system descriptor (disk) quorum.

    Args:
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing disk quorum information

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/disksquorum",
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get disk quorum for filesystem '{filesystem}': {str(e)}"
        ) from e
