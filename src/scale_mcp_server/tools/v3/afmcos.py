"""IBM Storage Scale AFMCOS MCP Server.

AFM to Cloud Object Storage tools for COS relationships and object transfers.
"""

from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v3.afmcos import (
    get_cos_keys_api,
    set_cos_keys_api,
    delete_cos_keys_api,
    configure_afmcos_api,
    delete_afmcos_objects_api,
    download_afmcos_objects_api,
    evict_afmcos_objects_api,
    reconcile_afmcos_api,
    upload_afmcos_objects_api,
)

# Create the afmcos MCP server
mcp = FastMCP("afmcos", instructions="AFM to Cloud Object Storage (AFMCOS) operations")


@mcp.tool()
async def get_cos_keys(
    ctx: Context,
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
    """
    await ctx.info(f"Tool called: get_cos_keys with bucket_name={bucket_name}")
    try:
        return await get_cos_keys_api(
            bucket_name=bucket_name,
            bucket_region=bucket_region,
            bucket_exportmap=bucket_exportmap,
            bucket_report=bucket_report,
            domain=domain,
        )
    except Exception as e:
        await ctx.error(f"Failed to get COS keys for {bucket_name}: {str(e)}")
        raise


@mcp.tool()
async def set_cos_keys(
    ctx: Context,
    bucket_name: str,
    bucket_coskeys: dict,
    domain: Optional[str] = None,
) -> Any:
    """Set keys for the given bucket for an AFM fileset.

    Args:
        bucket_name: Bucket name
        bucket_coskeys: Bucket key configuration (bucket_accesskey,
            bucket_secretkey, bucket_region, bucket_keyfile, bucket_exportmap)
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: set_cos_keys with bucket_name={bucket_name}")
    try:
        return await set_cos_keys_api(
            bucket_name=bucket_name, bucket_coskeys=bucket_coskeys, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to set COS keys for {bucket_name}: {str(e)}")
        raise


@mcp.tool()
async def delete_cos_keys(
    ctx: Context,
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
    """
    await ctx.info(f"Tool called: delete_cos_keys with bucket_name={bucket_name}")
    try:
        return await delete_cos_keys_api(
            bucket_name=bucket_name,
            bucket_region=bucket_region,
            bucket_exportmap=bucket_exportmap,
            domain=domain,
        )
    except Exception as e:
        await ctx.error(f"Failed to delete COS keys for {bucket_name}: {str(e)}")
        raise


@mcp.tool()
async def configure_afmcos(
    ctx: Context,
    filesystem: str,
    fileset: str,
    fileset_config: dict,
    domain: Optional[str] = None,
) -> Any:
    """Configure an AFM to cloud object storage relationship for a fileset.

    Args:
        filesystem: Filesystem name
        fileset: AFM fileset name
        fileset_config: AFM to COS configuration (bucket, endpoint, mode,
            prefix, quotas, etc.)
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(
        f"Tool called: configure_afmcos with filesystem={filesystem}, fileset={fileset}"
    )
    try:
        return await configure_afmcos_api(
            filesystem=filesystem,
            fileset=fileset,
            fileset_config=fileset_config,
            domain=domain,
        )
    except Exception as e:
        await ctx.error(f"Failed to configure AFMCOS for {fileset}: {str(e)}")
        raise


@mcp.tool()
async def delete_afmcos_objects(
    ctx: Context,
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
    """
    await ctx.info(
        f"Tool called: delete_afmcos_objects with filesystem={filesystem}, fileset={fileset}"
    )
    try:
        return await delete_afmcos_objects_api(
            filesystem=filesystem,
            fileset=fileset,
            delete_objects=delete_objects,
            domain=domain,
        )
    except Exception as e:
        await ctx.error(f"Failed to delete AFMCOS objects for {fileset}: {str(e)}")
        raise


@mcp.tool()
async def download_afmcos_objects(
    ctx: Context,
    filesystem: str,
    fileset: str,
    download_objects: dict,
    domain: Optional[str] = None,
) -> Any:
    """Download objects from cloud object storage to the local fileset cache.

    Args:
        filesystem: Filesystem name
        fileset: AFM fileset name
        download_objects: Download parameters (path_for_download, data,
            metadata, uid, gid, perm, etc.)
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(
        f"Tool called: download_afmcos_objects with filesystem={filesystem}, fileset={fileset}"
    )
    try:
        return await download_afmcos_objects_api(
            filesystem=filesystem,
            fileset=fileset,
            download_objects=download_objects,
            domain=domain,
        )
    except Exception as e:
        await ctx.error(f"Failed to download AFMCOS objects for {fileset}: {str(e)}")
        raise


@mcp.tool()
async def evict_afmcos_objects(
    ctx: Context,
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
    """
    await ctx.info(
        f"Tool called: evict_afmcos_objects with filesystem={filesystem}, fileset={fileset}"
    )
    try:
        return await evict_afmcos_objects_api(
            filesystem=filesystem,
            fileset=fileset,
            evict_objects=evict_objects,
            domain=domain,
        )
    except Exception as e:
        await ctx.error(f"Failed to evict AFMCOS objects for {fileset}: {str(e)}")
        raise


@mcp.tool()
async def reconcile_afmcos(
    ctx: Context,
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
    """
    await ctx.info(
        f"Tool called: reconcile_afmcos with filesystem={filesystem}, fileset={fileset}"
    )
    try:
        return await reconcile_afmcos_api(
            filesystem=filesystem,
            fileset=fileset,
            reconcile_objects=reconcile_objects,
            domain=domain,
        )
    except Exception as e:
        await ctx.error(f"Failed to reconcile AFMCOS objects for {fileset}: {str(e)}")
        raise


@mcp.tool()
async def upload_afmcos_objects(
    ctx: Context,
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
    """
    await ctx.info(
        f"Tool called: upload_afmcos_objects with filesystem={filesystem}, fileset={fileset}"
    )
    try:
        return await upload_afmcos_objects_api(
            filesystem=filesystem,
            fileset=fileset,
            upload_objects=upload_objects,
            domain=domain,
        )
    except Exception as e:
        await ctx.error(f"Failed to upload AFMCOS objects for {fileset}: {str(e)}")
        raise
