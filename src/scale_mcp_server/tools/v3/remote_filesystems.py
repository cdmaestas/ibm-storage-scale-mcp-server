"""IBM Storage Scale Remote Filesystems MCP Server.

Remote file system tools for file systems owned by another cluster.
"""

from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v3.remote_filesystems import (
    add_remote_filesystem_api,
    update_remote_filesystem_api,
    delete_remote_filesystem_api,
)

# Create the remote_filesystems MCP server
mcp = FastMCP(
    "remote_filesystems", instructions="Remote file system management operations"
)


@mcp.tool()
async def add_remote_filesystem(
    ctx: Context,
    filesystem: dict,
    domain: Optional[str] = None,
) -> Any:
    """Add a remote file system owned by another IBM Storage Scale cluster.

    Args:
        filesystem: Remote file system definition
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: add_remote_filesystem")
    try:
        return await add_remote_filesystem_api(filesystem=filesystem, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to add remote filesystem: {str(e)}")
        raise


@mcp.tool()
async def update_remote_filesystem(
    ctx: Context,
    filesystem: str,
    filesystem_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Update the information associated with a remote file system.

    Args:
        filesystem: Remote file system name
        filesystem_data: Updated remote file system definition
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: update_remote_filesystem with filesystem={filesystem}")
    try:
        return await update_remote_filesystem_api(
            filesystem=filesystem, filesystem_data=filesystem_data, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to update remote filesystem {filesystem}: {str(e)}")
        raise


@mcp.tool()
async def delete_remote_filesystem(
    ctx: Context,
    filesystem: str,
    permanently_damaged: Optional[bool] = None,
    domain: Optional[str] = None,
) -> Any:
    """Delete a remote file system.

    Args:
        filesystem: Remote file system name
        permanently_damaged: Proceed with deletion even if the remote file
            system is permanently damaged
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: delete_remote_filesystem with filesystem={filesystem}")
    try:
        return await delete_remote_filesystem_api(
            filesystem=filesystem,
            permanently_damaged=permanently_damaged,
            domain=domain,
        )
    except Exception as e:
        await ctx.error(f"Failed to delete remote filesystem {filesystem}: {str(e)}")
        raise
