"""IBM Storage Scale Troubleshooting MCP Server.

Troubleshooting tools for advanced diagnostics and problem resolution.
"""

from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v3.troubleshooting import (
    get_troubleshooting_info_api,
    collect_diagnostics_api,
    get_logs_api,
    run_diagnostic_test_api,
)

# Create the troubleshooting MCP server
mcp = FastMCP(
    "troubleshooting",
    instructions="Advanced diagnostics and troubleshooting operations",
)


@mcp.tool()
async def get_troubleshooting_info(
    ctx: Context,
    domain: Optional[str] = None,
) -> Any:
    """Get general troubleshooting information.

    Retrieves general troubleshooting information and diagnostic data.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing troubleshooting information
    """
    await ctx.info("Tool called: get_troubleshooting_info")
    await ctx.debug("Retrieving troubleshooting information")

    try:
        result = await get_troubleshooting_info_api(domain=domain)
        await ctx.info("Successfully retrieved troubleshooting information")
        return result
    except Exception as e:
        await ctx.error(f"Failed to get troubleshooting information: {str(e)}")
        raise


@mcp.tool()
async def collect_diagnostics(
    ctx: Context,
    collection_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Collect diagnostic data.

    Initiates collection of diagnostic data for troubleshooting purposes.

    Args:
        collection_data: Data specifying what diagnostics to collect
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing collection status and operation ID
    """
    await ctx.info("Tool called: collect_diagnostics")
    await ctx.debug("Initiating diagnostic data collection")

    try:
        result = await collect_diagnostics_api(
            collection_data=collection_data, domain=domain
        )
        await ctx.info("Successfully initiated diagnostic collection")
        return result
    except Exception as e:
        await ctx.error(f"Failed to collect diagnostics: {str(e)}")
        raise


@mcp.tool()
async def get_logs(
    ctx: Context,
    component: Optional[str] = None,
    level: Optional[str] = None,
    lines: Optional[int] = None,
    domain: Optional[str] = None,
) -> Any:
    """Get system logs.

    Retrieves system logs for troubleshooting purposes.

    Args:
        component: Specific component to get logs for (optional)
        level: Log level filter (e.g., 'ERROR', 'WARNING', 'INFO')
        lines: Number of log lines to retrieve
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing log data
    """
    await ctx.info("Tool called: get_logs")
    await ctx.debug(f"Retrieving logs (component: {component}, level: {level})")

    try:
        result = await get_logs_api(
            component=component, level=level, lines=lines, domain=domain
        )
        await ctx.info("Successfully retrieved logs")
        return result
    except Exception as e:
        await ctx.error(f"Failed to get logs: {str(e)}")
        raise


@mcp.tool()
async def run_diagnostic_test(
    ctx: Context,
    test_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Run a diagnostic test.

    Executes a specific diagnostic test for troubleshooting.

    Args:
        test_data: Data specifying which test to run and parameters
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing test results or operation ID
    """
    await ctx.info("Tool called: run_diagnostic_test")
    await ctx.debug("Running diagnostic test")

    try:
        result = await run_diagnostic_test_api(test_data=test_data, domain=domain)
        await ctx.info("Successfully ran diagnostic test")
        return result
    except Exception as e:
        await ctx.error(f"Failed to run diagnostic test: {str(e)}")
        raise
