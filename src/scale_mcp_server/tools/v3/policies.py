"""IBM Storage Scale Policy Management MCP Server.

Policy tools for listing and updating the file system policy. Policy runs
(mmapplypolicy) are handled by the CLI policy tools.
"""

from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v3.policies import (
    get_policy_api,
    update_policy_api,
)

# Create the policies MCP server
mcp = FastMCP("policies", instructions="File system policy operations")


@mcp.tool()
async def get_policy(
    ctx: Context,
    filesystem: str,
    domain: Optional[str] = None,
) -> Any:
    """List information about the file system policy.

    Args:
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: get_policy with filesystem={filesystem}")
    try:
        return await get_policy_api(filesystem=filesystem, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to get policy for {filesystem}: {str(e)}")
        raise


@mcp.tool()
async def update_policy(
    ctx: Context,
    filesystem: str,
    policy: dict,
    test_only: Optional[bool] = None,
    domain: Optional[str] = None,
) -> Any:
    """Update the file system policy.

    Args:
        filesystem: Filesystem name
        policy: Policy definition to install
        test_only: Only test the validity of the policy without installing it
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: update_policy with filesystem={filesystem}")
    try:
        return await update_policy_api(
            filesystem=filesystem, policy=policy, test_only=test_only, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to update policy for {filesystem}: {str(e)}")
        raise
