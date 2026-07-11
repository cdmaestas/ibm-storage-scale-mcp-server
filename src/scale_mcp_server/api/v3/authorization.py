"""IBM Storage Scale Authorization (RBAC) operations.

Authorization endpoints for managing role-based access control: domains,
permission checks (cani), and the policy evaluation module. Follows the
6.0.1 native REST API. Note: the native REST API authenticates with
mTLS/basic auth per request; there are no login/token endpoints.
"""

from typing import Optional, Any, Dict
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


def _domain_headers(domain: Optional[str]) -> Dict[str, str]:
    """Build request headers for the optional X-StorageScaleDomain."""
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain
    return headers


async def can_i_api(
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

    Returns:
        Dictionary containing the authorization decision

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/authorization/cani",
                json={"action": action, "resource": resource},
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to check authorization for action '{action}' on '{resource}': {str(e)}"
        ) from e


async def can_i_impersonate_api(
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

    Returns:
        Dictionary containing the authorization decision

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/authorization/cani:impersonate",
                json={"action": action, "resource": resource, "user": user},
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to check authorization for user '{user}', action '{action}' on '{resource}': {str(e)}"
        ) from e


async def list_rbac_domains_api(
    page_size: Optional[int] = None,
    page_token: Optional[str] = None,
    domain: Optional[str] = None,
) -> Any:
    """List information about all RBAC domains.

    Args:
        page_size: Number of items to return per request
        page_token: Token to navigate to the next page
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the RBAC domains

    Raises:
        StorageScaleAPIError: If API call fails
    """
    params: Dict[str, Any] = {}
    if page_size is not None:
        params["page_size"] = page_size
    if page_token is not None:
        params["page_token"] = page_token

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                "/scalemgmt/v3/authorization/domains",
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to list RBAC domains: {str(e)}") from e


async def create_rbac_domain_api(
    domain_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Create an RBAC domain.

    Args:
        domain_data: Domain definition (resources, users/roles, actions)
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the creation status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/authorization/domains",
                json=domain_data,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        name = domain_data.get("name", "unknown")
        raise StorageScaleAPIError(
            f"Failed to create RBAC domain '{name}': {str(e)}"
        ) from e


async def get_rbac_domain_api(
    name: str,
    domain: Optional[str] = None,
) -> Any:
    """Get information about a specific RBAC domain.

    Args:
        name: RBAC domain name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the RBAC domain details

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/authorization/domains/{name}",
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get RBAC domain '{name}': {str(e)}"
        ) from e


async def update_rbac_domain_api(
    name: str,
    domain_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Update an RBAC domain (permissions, memberships, resource groups).

    Args:
        name: RBAC domain name
        domain_data: Updated domain definition
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the update status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.patch(
                f"/scalemgmt/v3/authorization/domains/{name}",
                json=domain_data,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to update RBAC domain '{name}': {str(e)}"
        ) from e


async def delete_rbac_domain_api(
    name: str,
    domain: Optional[str] = None,
) -> Any:
    """Delete an RBAC domain.

    Args:
        name: RBAC domain name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the deletion status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.delete(
                f"/scalemgmt/v3/authorization/domains/{name}",
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to delete RBAC domain '{name}': {str(e)}"
        ) from e


async def get_rbac_module_api(
    domain: Optional[str] = None,
) -> Any:
    """Get the current RBAC policy evaluation rule set.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the policy evaluation rule set

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.get(
                "/scalemgmt/v3/authorization/module",
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to get RBAC module: {str(e)}") from e


async def update_rbac_module_api(
    module_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Update the customer-defined RBAC policy rule set.

    Args:
        module_data: Policy rule set definition
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the update status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.patch(
                "/scalemgmt/v3/authorization/module",
                json=module_data,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to update RBAC module: {str(e)}") from e
