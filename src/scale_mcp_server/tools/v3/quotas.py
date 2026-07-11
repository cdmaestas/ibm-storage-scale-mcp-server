"""IBM Storage Scale Quota Management MCP Server.

Quota tools for file system and fileset quotas.
"""

from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v3.quotas import (
    list_quotas_api,
    set_quota_api,
    check_quotas_api,
    update_quota_config_api,
    list_fileset_quotas_api,
    set_fileset_quota_api,
    check_fileset_quotas_api,
)

# Create the quotas MCP server
mcp = FastMCP("quotas", instructions="Quota management operations")


@mcp.tool()
async def list_quotas(
    ctx: Context,
    filesystem: str,
    page_size: Optional[int] = None,
    page_token: Optional[str] = None,
    show_perfileset_quotas: Optional[bool] = None,
    default: Optional[bool] = None,
    filter: Optional[str] = None,
    domain: Optional[str] = None,
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
    """
    await ctx.info(f"Tool called: list_quotas with filesystem={filesystem}")
    try:
        return await list_quotas_api(
            filesystem=filesystem,
            page_size=page_size,
            page_token=page_token,
            show_perfileset_quotas=show_perfileset_quotas,
            default=default,
            filter=filter,
            domain=domain,
        )
    except Exception as e:
        await ctx.error(f"Failed to list quotas for {filesystem}: {str(e)}")
        raise


@mcp.tool()
async def set_quota(
    ctx: Context,
    filesystem: str,
    quota_data: dict,
    default: Optional[bool] = None,
    domain: Optional[str] = None,
) -> Any:
    """Set quota limits for a file system.

    Args:
        filesystem: Filesystem name
        quota_data: Quota definition, e.g. {"quota": {"name": ..., "type":
            "QUOTA_TYPE_USER", "block_soft_limit_bytes": ..., ...}}
        default: Set default quota limits
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: set_quota with filesystem={filesystem}")
    try:
        return await set_quota_api(
            filesystem=filesystem, quota_data=quota_data, default=default, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to set quota for {filesystem}: {str(e)}")
        raise


@mcp.tool()
async def check_quotas(
    ctx: Context,
    filesystem: str,
    check_data: Optional[dict] = None,
    domain: Optional[str] = None,
) -> Any:
    """Check quotas for a file system (mmcheckquota equivalent).

    Args:
        filesystem: Filesystem name
        check_data: Check parameters (verbose, threads, report_diff,
            target_nodes, qos_class)
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: check_quotas with filesystem={filesystem}")
    try:
        return await check_quotas_api(
            filesystem=filesystem, check_data=check_data, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to check quotas for {filesystem}: {str(e)}")
        raise


@mcp.tool()
async def update_quota_config(
    ctx: Context,
    filesystem: str,
    config_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Update quota configuration (defaults and enforcement) for a file system.

    Args:
        filesystem: Filesystem name
        config_data: Quota configuration, e.g. {"default_quotas": "YES",
            "enforcement": "YES", "quota_type": ["QUOTA_TYPE_USER"]}
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: update_quota_config with filesystem={filesystem}")
    try:
        return await update_quota_config_api(
            filesystem=filesystem, config_data=config_data, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to update quota config for {filesystem}: {str(e)}")
        raise


@mcp.tool()
async def list_fileset_quotas(
    ctx: Context,
    filesystem: str,
    fileset: str,
    page_size: Optional[int] = None,
    page_token: Optional[str] = None,
    default: Optional[bool] = None,
    domain: Optional[str] = None,
) -> Any:
    """Retrieve quota information for a specific fileset.

    Args:
        filesystem: Filesystem name
        fileset: Fileset name
        page_size: Number of items per page
        page_token: Token for pagination
        default: Show default quota limits
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(
        f"Tool called: list_fileset_quotas with filesystem={filesystem}, fileset={fileset}"
    )
    try:
        return await list_fileset_quotas_api(
            filesystem=filesystem,
            fileset=fileset,
            page_size=page_size,
            page_token=page_token,
            default=default,
            domain=domain,
        )
    except Exception as e:
        await ctx.error(f"Failed to list quotas for fileset {fileset}: {str(e)}")
        raise


@mcp.tool()
async def set_fileset_quota(
    ctx: Context,
    filesystem: str,
    fileset: str,
    quota_data: dict,
    default: Optional[bool] = None,
    domain: Optional[str] = None,
) -> Any:
    """Set quota limits for a specific fileset.

    Args:
        filesystem: Filesystem name
        fileset: Fileset name
        quota_data: Quota definition, e.g. {"quota": {"name": ..., "type":
            "QUOTA_TYPE_USER", "block_soft_limit_bytes": ..., ...}}
        default: Set default quota limits for user and group quota types
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(
        f"Tool called: set_fileset_quota with filesystem={filesystem}, fileset={fileset}"
    )
    try:
        return await set_fileset_quota_api(
            filesystem=filesystem,
            fileset=fileset,
            quota_data=quota_data,
            default=default,
            domain=domain,
        )
    except Exception as e:
        await ctx.error(f"Failed to set quota for fileset {fileset}: {str(e)}")
        raise


@mcp.tool()
async def check_fileset_quotas(
    ctx: Context,
    filesystem: str,
    fileset: str,
    check_data: Optional[dict] = None,
    domain: Optional[str] = None,
) -> Any:
    """Check user and group quotas for a specific fileset.

    Args:
        filesystem: Filesystem name
        fileset: Fileset name
        check_data: Check parameters (verbose, threads, report_diff,
            target_nodes, qos_class)
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(
        f"Tool called: check_fileset_quotas with filesystem={filesystem}, fileset={fileset}"
    )
    try:
        return await check_fileset_quotas_api(
            filesystem=filesystem, fileset=fileset, check_data=check_data, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to check quotas for fileset {fileset}: {str(e)}")
        raise
