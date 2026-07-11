"""IBM Storage Scale AFM MCP Server.

Active File Management tools for AFM filesets.
"""

from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v3.afm import (
    list_afm_states_api,
    get_afm_state_api,
    check_afm_dirty_api,
    check_afm_uncached_api,
    flush_afm_queue_api,
    resume_afm_requeued_api,
    resync_afm_fileset_api,
    start_afm_fileset_api,
    stop_afm_fileset_api,
    reset_afm_local_api,
    set_afm_local_api,
)

# Create the afm MCP server
mcp = FastMCP("afm", instructions="Active File Management (AFM) operations")


@mcp.tool()
async def list_afm_states(
    ctx: Context,
    filesystem: str,
    domain: Optional[str] = None,
) -> Any:
    """List the AFM state of all AFM filesets in a filesystem.

    Args:
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: list_afm_states with filesystem={filesystem}")
    try:
        return await list_afm_states_api(filesystem=filesystem, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to list AFM states for {filesystem}: {str(e)}")
        raise


@mcp.tool()
async def get_afm_state(
    ctx: Context,
    filesystem: str,
    fileset: str,
    domain: Optional[str] = None,
) -> Any:
    """Describe the AFM state of a specific AFM fileset.

    Args:
        filesystem: Filesystem name
        fileset: AFM fileset name
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(
        f"Tool called: get_afm_state with filesystem={filesystem}, fileset={fileset}"
    )
    try:
        return await get_afm_state_api(
            filesystem=filesystem, fileset=fileset, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to get AFM state for {fileset}: {str(e)}")
        raise


@mcp.tool()
async def check_afm_dirty(
    ctx: Context,
    filesystem: str,
    fileset: str,
    dir_path: Optional[str] = None,
    dirty_data: Optional[bool] = None,
    escaped_chars: Optional[bool] = None,
    domain: Optional[str] = None,
) -> Any:
    """Find all modified (dirty) directories and files in an AFM fileset.

    Args:
        filesystem: Filesystem name
        fileset: AFM fileset name
        dir_path: Path under the AFM fileset to check
        dirty_data: Calculate the total data of modified files
        escaped_chars: List entries with escaped characters
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(
        f"Tool called: check_afm_dirty with filesystem={filesystem}, fileset={fileset}"
    )
    try:
        return await check_afm_dirty_api(
            filesystem=filesystem,
            fileset=fileset,
            dir_path=dir_path,
            dirty_data=dirty_data,
            escaped_chars=escaped_chars,
            domain=domain,
        )
    except Exception as e:
        await ctx.error(f"Failed to check dirty files for {fileset}: {str(e)}")
        raise


@mcp.tool()
async def check_afm_uncached(
    ctx: Context,
    filesystem: str,
    fileset: str,
    dir_path: Optional[str] = None,
    check_unmigrated: Optional[bool] = None,
    escaped_chars: Optional[bool] = None,
    domain: Optional[str] = None,
) -> Any:
    """Find all uncached directories, files, and orphan files in an AFM fileset.

    Args:
        filesystem: Filesystem name
        fileset: AFM fileset name
        dir_path: Path under the AFM fileset to check
        check_unmigrated: List non-migrated directories, files, and orphans
        escaped_chars: List entries with escaped characters
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(
        f"Tool called: check_afm_uncached with filesystem={filesystem}, fileset={fileset}"
    )
    try:
        return await check_afm_uncached_api(
            filesystem=filesystem,
            fileset=fileset,
            dir_path=dir_path,
            check_unmigrated=check_unmigrated,
            escaped_chars=escaped_chars,
            domain=domain,
        )
    except Exception as e:
        await ctx.error(f"Failed to check uncached files for {fileset}: {str(e)}")
        raise


@mcp.tool()
async def flush_afm_queue(
    ctx: Context,
    filesystem: str,
    fileset: str,
    domain: Optional[str] = None,
) -> Any:
    """Flush all pending queued operations for an AFM fileset.

    Args:
        filesystem: Filesystem name
        fileset: AFM fileset name
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(
        f"Tool called: flush_afm_queue with filesystem={filesystem}, fileset={fileset}"
    )
    try:
        return await flush_afm_queue_api(
            filesystem=filesystem, fileset=fileset, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to flush AFM queue for {fileset}: {str(e)}")
        raise


@mcp.tool()
async def resume_afm_requeued(
    ctx: Context,
    filesystem: str,
    fileset: str,
    domain: Optional[str] = None,
) -> Any:
    """Resume all pending requeued operations for an AFM fileset.

    Args:
        filesystem: Filesystem name
        fileset: AFM fileset name
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(
        f"Tool called: resume_afm_requeued with filesystem={filesystem}, fileset={fileset}"
    )
    try:
        return await resume_afm_requeued_api(
            filesystem=filesystem, fileset=fileset, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to resume requeued operations for {fileset}: {str(e)}")
        raise


@mcp.tool()
async def resync_afm_fileset(
    ctx: Context,
    filesystem: str,
    fileset: str,
    domain: Optional[str] = None,
) -> Any:
    """Resync all files from cache to home for a single-writer AFM fileset.

    Args:
        filesystem: Filesystem name
        fileset: AFM fileset name
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(
        f"Tool called: resync_afm_fileset with filesystem={filesystem}, fileset={fileset}"
    )
    try:
        return await resync_afm_fileset_api(
            filesystem=filesystem, fileset=fileset, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to resync AFM fileset {fileset}: {str(e)}")
        raise


@mcp.tool()
async def start_afm_fileset(
    ctx: Context,
    filesystem: str,
    fileset: str,
    domain: Optional[str] = None,
) -> Any:
    """Start operations for an AFM fileset.

    Args:
        filesystem: Filesystem name
        fileset: AFM fileset name
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(
        f"Tool called: start_afm_fileset with filesystem={filesystem}, fileset={fileset}"
    )
    try:
        return await start_afm_fileset_api(
            filesystem=filesystem, fileset=fileset, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to start AFM fileset {fileset}: {str(e)}")
        raise


@mcp.tool()
async def stop_afm_fileset(
    ctx: Context,
    filesystem: str,
    fileset: str,
    domain: Optional[str] = None,
) -> Any:
    """Stop all operations for an AFM fileset.

    Args:
        filesystem: Filesystem name
        fileset: AFM fileset name
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(
        f"Tool called: stop_afm_fileset with filesystem={filesystem}, fileset={fileset}"
    )
    try:
        return await stop_afm_fileset_api(
            filesystem=filesystem, fileset=fileset, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to stop AFM fileset {fileset}: {str(e)}")
        raise


@mcp.tool()
async def reset_afm_local(
    ctx: Context,
    filesystem: str,
    fileset: str,
    file_path: str,
    domain: Optional[str] = None,
) -> Any:
    """Reset the local bit for a filepath in an AFM fileset.

    Args:
        filesystem: Filesystem name
        fileset: AFM fileset name
        file_path: Filepath for which to reset the local bit
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(
        f"Tool called: reset_afm_local with filesystem={filesystem}, fileset={fileset}"
    )
    try:
        return await reset_afm_local_api(
            filesystem=filesystem,
            fileset=fileset,
            file_path=file_path,
            domain=domain,
        )
    except Exception as e:
        await ctx.error(f"Failed to reset local bit for {file_path}: {str(e)}")
        raise


@mcp.tool()
async def set_afm_local(
    ctx: Context,
    filesystem: str,
    fileset: str,
    file_path: str,
    domain: Optional[str] = None,
) -> Any:
    """Set the local bit for a filepath in an AFM fileset.

    Args:
        filesystem: Filesystem name
        fileset: AFM fileset name
        file_path: Filepath for which to set the local bit
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(
        f"Tool called: set_afm_local with filesystem={filesystem}, fileset={fileset}"
    )
    try:
        return await set_afm_local_api(
            filesystem=filesystem,
            fileset=fileset,
            file_path=file_path,
            domain=domain,
        )
    except Exception as e:
        await ctx.error(f"Failed to set local bit for {file_path}: {str(e)}")
        raise
