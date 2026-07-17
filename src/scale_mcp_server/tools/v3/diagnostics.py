"""IBM Storage Scale Diagnostics MCP Server."""

from typing import Any

from fastmcp import Context, FastMCP

from scale_mcp_server.api.v3.diagnostics import get_node_version_api

# Create the diagnostics MCP server
mcp = FastMCP("diagnostics", instructions="Diagnostics operations")


@mcp.tool()
async def get_node_version(
    ctx: Context,
    node: str,
    domain: str | None = None,
) -> Any:
    """Get the mmfsd version of a node.

    Args:
        node: Node name
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: get_node_version with node={node}")
    try:
        return await get_node_version_api(node=node, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to get version for node {node}: {str(e)}")
        raise
