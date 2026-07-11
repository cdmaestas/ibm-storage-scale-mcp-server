"""IBM Storage Scale AFM to Cloud Object Storage (AFMCOS) operations.

AFMCOS endpoints for managing AFM-to-COS relationships and object transfers,
following the 6.0.1 native REST API.
"""

from typing import Optional, Any, Dict
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


def _domain_headers(domain: Optional[str]) -> Dict[str, str]:
    """Build request headers for the optional X-StorageScaleDomain."""
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain
    return headers


async def get_cos_keys_api(
    bucket_name: str,
    bucket_region: Optional[str] = None,
    bucket_exportmap: Optional[str] = None,
    bucket_report: Optional[str] = None,
    domain: Optional[str] = None,
) -> Any:
    """Retrieve keys for the given bucket for an AFM fileset.

    Args:
        bucket_name: Bucket name
        bucket_region: Server name with the bucket ([Region@]Server)
        bucket_exportmap: Exportmap name with the bucket
        bucket_report: Set with bucket name 'all' to list all bucket keys
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the bucket keys

    Raises:
        StorageScaleAPIError: If API call fails
    """
    params: Dict[str, Any] = {}
    if bucket_region is not None:
        params["bucket_region"] = bucket_region
    if bucket_exportmap is not None:
        params["bucket_exportmap"] = bucket_exportmap
    if bucket_report is not None:
        params["bucket_report"] = bucket_report

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/buckets/{bucket_name}/afmcos/getcoskeys",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get COS keys for bucket '{bucket_name}': {str(e)}"
        ) from e


async def set_cos_keys_api(
    bucket_name: str,
    bucket_coskeys: dict,
    domain: Optional[str] = None,
) -> Any:
    """Set keys for the given bucket for an AFM fileset.

    Args:
        bucket_name: Bucket name
        bucket_coskeys: Bucket key configuration, e.g. {"bucket_accesskey": ...,
            "bucket_secretkey": ..., "bucket_region": ..., "bucket_keyfile": ...,
            "bucket_exportmap": ...}
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.put(
                f"/scalemgmt/v3/buckets/{bucket_name}/afmcos/setcoskeys",
                json=bucket_coskeys,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to set COS keys for bucket '{bucket_name}': {str(e)}"
        ) from e


async def delete_cos_keys_api(
    bucket_name: str,
    bucket_region: Optional[str] = None,
    bucket_exportmap: Optional[str] = None,
    domain: Optional[str] = None,
) -> Any:
    """Delete keys for the given bucket for an AFM fileset.

    Args:
        bucket_name: Bucket name
        bucket_region: Server name with the bucket ([Region@]Server)
        bucket_exportmap: Exportmap name with the bucket
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    params: Dict[str, Any] = {}
    if bucket_region is not None:
        params["bucket_region"] = bucket_region
    if bucket_exportmap is not None:
        params["bucket_exportmap"] = bucket_exportmap

    try:
        async with StorageScaleClient() as client:
            return await client.delete(
                f"/scalemgmt/v3/buckets/{bucket_name}/afmcos/delcoskeys",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to delete COS keys for bucket '{bucket_name}': {str(e)}"
        ) from e


async def configure_afmcos_api(
    filesystem: str,
    fileset: str,
    fileset_config: dict,
    domain: Optional[str] = None,
) -> Any:
    """Configure an AFM to cloud object storage relationship for a fileset.

    Args:
        filesystem: Filesystem name
        fileset: AFM fileset name
        fileset_config: AFM to COS configuration parameters (bucket, endpoint,
            mode, prefix, quotas, etc.)
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.put(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/afmcos/configure",
                json=fileset_config,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to configure AFMCOS for fileset '{fileset}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def delete_afmcos_objects_api(
    filesystem: str,
    fileset: str,
    delete_objects: dict,
    domain: Optional[str] = None,
) -> Any:
    """Delete objects from cloud object storage for an AFM fileset.

    Args:
        filesystem: Filesystem name
        fileset: AFM fileset name
        delete_objects: Delete parameters (path_for_delete, fromcache_delete,
            fromtarget_delete, policy options, etc.)
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/afmcos/delete",
                json=delete_objects,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to delete AFMCOS objects for fileset '{fileset}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def download_afmcos_objects_api(
    filesystem: str,
    fileset: str,
    download_objects: dict,
    domain: Optional[str] = None,
) -> Any:
    """Download objects from cloud object storage to the local AFM fileset cache.

    Args:
        filesystem: Filesystem name
        fileset: AFM fileset name
        download_objects: Download parameters (path_for_download, data, metadata,
            uid, gid, perm, etc.)
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/afmcos/download",
                json=download_objects,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to download AFMCOS objects for fileset '{fileset}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def evict_afmcos_objects_api(
    filesystem: str,
    fileset: str,
    evict_objects: dict,
    domain: Optional[str] = None,
) -> Any:
    """Evict objects from the local cache of an AFM fileset.

    Args:
        filesystem: Filesystem name
        fileset: AFM fileset name
        evict_objects: Evict parameters (path_for_evict, evict_metadata,
            evict_validate, scale_node_object_list_path)
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/afmcos/evict",
                json=evict_objects,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to evict AFMCOS objects for fileset '{fileset}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def reconcile_afmcos_api(
    filesystem: str,
    fileset: str,
    reconcile_objects: dict,
    domain: Optional[str] = None,
) -> Any:
    """Reconcile objects between the local cache and cloud object storage.

    Args:
        filesystem: Filesystem name
        fileset: AFM fileset name
        reconcile_objects: Reconcile parameters (path_for_reconcile,
            evict_reconcile, policy options, etc.)
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/afmcos/reconcile",
                json=reconcile_objects,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to reconcile AFMCOS objects for fileset '{fileset}' in filesystem '{filesystem}': {str(e)}"
        ) from e


async def upload_afmcos_objects_api(
    filesystem: str,
    fileset: str,
    upload_objects: dict,
    domain: Optional[str] = None,
) -> Any:
    """Upload objects from the local AFM fileset to cloud object storage.

    Args:
        filesystem: Filesystem name
        fileset: AFM fileset name
        upload_objects: Upload parameters (path_for_upload, evict_upload,
            scale_node_object_list_path)
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the operation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.put(
                f"/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/afmcos/upload",
                json=upload_objects,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to upload AFMCOS objects for fileset '{fileset}' in filesystem '{filesystem}': {str(e)}"
        ) from e
