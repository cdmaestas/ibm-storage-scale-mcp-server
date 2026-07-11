"""IBM Storage Scale Authorization MCP Server.

Role-based access control (RBAC) tools: domains, permission checks, and the
policy evaluation module.
"""

from typing import Optional, Any
from fastmcp import FastMCP, Context
from scale_mcp_server.api.v3.authorization import (
    can_i_api,
    can_i_impersonate_api,
    list_rbac_domains_api,
    create_rbac_domain_api,
    get_rbac_domain_api,
    update_rbac_domain_api,
    delete_rbac_domain_api,
    get_rbac_module_api,
    update_rbac_module_api,
)

# Create the authorization MCP server
mcp = FastMCP("authorization", instructions="RBAC authorization operations")


@mcp.tool()
async def can_i(
    ctx: Context,
    action: str,
    resource: str,
    domain: Optional[str] = None,
) -> Any:
    """Check whether the current user may perform an action on a resource.

    Args:
        action: Action to test (update, link, unmount, cani, stop, create,
            delete, get, unlink, mount, impersonate, start, restripe)
        resource: Resource endpoint to test access against
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: can_i with action={action}, resource={resource}")
    try:
        return await can_i_api(action=action, resource=resource, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed authorization check for {action} on {resource}: {str(e)}")
        raise


@mcp.tool()
async def can_i_impersonate(
    ctx: Context,
    action: str,
    resource: str,
    user: str,
    domain: Optional[str] = None,
) -> Any:
    """Check whether a specified user may perform an action on a resource.

    Args:
        action: Action to test (update, link, unmount, cani, stop, create,
            delete, get, unlink, mount, impersonate, start, restripe)
        resource: Resource endpoint to test access against
        user: User to test access for
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(
        f"Tool called: can_i_impersonate with user={user}, action={action}, resource={resource}"
    )
    try:
        return await can_i_impersonate_api(
            action=action, resource=resource, user=user, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed impersonation check for {user}: {str(e)}")
        raise


@mcp.tool()
async def list_rbac_domains(
    ctx: Context,
    page_size: Optional[int] = None,
    page_token: Optional[str] = None,
    domain: Optional[str] = None,
) -> Any:
    """List information about all RBAC domains.

    Args:
        page_size: Number of items to return per request
        page_token: Token to navigate to the next page
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: list_rbac_domains")
    try:
        return await list_rbac_domains_api(
            page_size=page_size, page_token=page_token, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to list RBAC domains: {str(e)}")
        raise


@mcp.tool()
async def create_rbac_domain(
    ctx: Context,
    domain_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Create an RBAC domain.

    Args:
        domain_data: Domain definition (resources, users/roles, actions)
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: create_rbac_domain")
    try:
        return await create_rbac_domain_api(domain_data=domain_data, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to create RBAC domain: {str(e)}")
        raise


@mcp.tool()
async def get_rbac_domain(
    ctx: Context,
    name: str,
    domain: Optional[str] = None,
) -> Any:
    """Get information about a specific RBAC domain.

    Args:
        name: RBAC domain name
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: get_rbac_domain with name={name}")
    try:
        return await get_rbac_domain_api(name=name, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to get RBAC domain {name}: {str(e)}")
        raise


@mcp.tool()
async def update_rbac_domain(
    ctx: Context,
    name: str,
    domain_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Update an RBAC domain (permissions, memberships, resource groups).

    Args:
        name: RBAC domain name
        domain_data: Updated domain definition
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: update_rbac_domain with name={name}")
    try:
        return await update_rbac_domain_api(
            name=name, domain_data=domain_data, domain=domain
        )
    except Exception as e:
        await ctx.error(f"Failed to update RBAC domain {name}: {str(e)}")
        raise


@mcp.tool()
async def delete_rbac_domain(
    ctx: Context,
    name: str,
    domain: Optional[str] = None,
) -> Any:
    """Delete an RBAC domain.

    Args:
        name: RBAC domain name
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info(f"Tool called: delete_rbac_domain with name={name}")
    try:
        return await delete_rbac_domain_api(name=name, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to delete RBAC domain {name}: {str(e)}")
        raise


@mcp.tool()
async def get_rbac_module(
    ctx: Context,
    domain: Optional[str] = None,
) -> Any:
    """Get the current RBAC policy evaluation rule set.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: get_rbac_module")
    try:
        return await get_rbac_module_api(domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to get RBAC module: {str(e)}")
        raise


@mcp.tool()
async def update_rbac_module(
    ctx: Context,
    module_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Update the customer-defined RBAC policy rule set.

    Args:
        module_data: Policy rule set definition
        domain: Domain to be authorized against (default 'StorageScaleDomain')
    """
    await ctx.info("Tool called: update_rbac_module")
    try:
        return await update_rbac_module_api(module_data=module_data, domain=domain)
    except Exception as e:
        await ctx.error(f"Failed to update RBAC module: {str(e)}")
        raise
