"""IBM Storage Scale Configuration Management MCP Server.

Configuration tools for the administration daemon (scaleadmd) and IO daemon
(mmfsd) settings.
"""

from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v3.config import (
    get_admin_config_api,
    get_admin_config_attribute_api,
    update_admin_config_api,
    get_cluster_config_api,
    get_cluster_config_attribute_api,
    update_cluster_config_api,
)

# Create the config MCP server
mcp = FastMCP("config", instructions="Configuration management operations")


@mcp.tool()
async def get_admin_config(
    ctx: Context,
    page_size: Optional[int] = None,
    page_token: Optional[str] = None,
    running: Optional[bool] = None,
    domain: Optional[str] = None,
) -> Any:
    """List the configuration data for the administration daemon (scaleadmd).

    Args:
        page_size: Number of items to return per request
        page_token: Token to navigate to the next page
        running: Display the configuration value running on the node
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: get_admin_config")
    try:
        return await get_admin_config_api(
            page_size=page_size, page_token=page_token, running=running, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to get admin config: {str(e)}")
        raise


@mcp.tool()
async def get_admin_config_attribute(
    ctx: Context,
    name: str,
    running: Optional[bool] = None,
    domain: Optional[str] = None,
) -> Any:
    """Get the admin daemon configuration value for a specified attribute.

    Args:
        name: Attribute name
        running: Display the configuration value running on the node
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: get_admin_config_attribute with name={name}")
    try:
        return await get_admin_config_attribute_api(
            name=name, running=running, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to get admin config attribute {name}: {str(e)}")
        raise


@mcp.tool()
async def update_admin_config(
    ctx: Context,
    config_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Batch-update configuration values of the administration daemon.

    Args:
        config_data: Configuration updates to apply
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: update_admin_config")
    try:
        return await update_admin_config_api(config_data=config_data, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to update admin config: {str(e)}")
        raise


@mcp.tool()
async def get_cluster_config(
    ctx: Context,
    view: Optional[str] = None,
    page_size: Optional[int] = None,
    page_token: Optional[str] = None,
    running: Optional[bool] = None,
    domain: Optional[str] = None,
) -> Any:
    """List the configuration data for the IO daemon (mmfsd).

    Args:
        view: View for configuration values (ALL, AFM, NSD_RAID, TRACE,
            MMHEALTH)
        page_size: Number of items to return per request
        page_token: Token to navigate to the next page
        running: Display the configuration value running on the node
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: get_cluster_config")
    try:
        return await get_cluster_config_api(
            view=view,
            page_size=page_size,
            page_token=page_token,
            running=running,
            domain=domain,
        )
    except Exception as e:
        await ctx.error(f"Failed to get cluster config: {str(e)}")
        raise


@mcp.tool()
async def get_cluster_config_attribute(
    ctx: Context,
    name: str,
    running: Optional[bool] = None,
    domain: Optional[str] = None,
) -> Any:
    """Get the IO daemon configuration value for a specified attribute.

    Args:
        name: Attribute name
        running: Display the configuration value running on the node
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: get_cluster_config_attribute with name={name}")
    try:
        return await get_cluster_config_attribute_api(
            name=name, running=running, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to get cluster config attribute {name}: {str(e)}")
        raise


@mcp.tool()
async def update_cluster_config(
    ctx: Context,
    config_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Batch-update configuration values of the IO daemon (mmfsd).

    Args:
        config_data: Configuration updates to apply
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: update_cluster_config")
    try:
        return await update_cluster_config_api(config_data=config_data, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to update cluster config: {str(e)}")
        raise
