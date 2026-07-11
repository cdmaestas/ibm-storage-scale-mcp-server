"""IBM Storage Scale Policy operations.

Policy endpoints for listing and updating the file system policy, following
the 6.0.1 native REST API. Policy runs (mmapplypolicy) are not available via
the native REST API; see the CLI policy tools for that.
"""

from typing import Optional, Any, Dict
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


def _domain_headers(domain: Optional[str]) -> Dict[str, str]:
    """Build request headers for the optional X-StorageScaleDomain."""
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain
    return headers


async def get_policy_api(
    filesystem: str,
    domain: Optional[str] = None,
) -> Any:
    """List information about the file system policy.

    Args:
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing the file system policy

    Raises:
        StorageScaleAPIError: If API call fails
    """
    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/policy",
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get policy for filesystem '{filesystem}': {str(e)}"
        ) from e


async def update_policy_api(
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

    Returns:
        Dictionary containing the update status

    Raises:
        StorageScaleAPIError: If API call fails
    """
    params: Dict[str, Any] = {}
    if test_only is not None:
        params["test_only"] = test_only

    try:
        async with StorageScaleClient() as client:
            return await client.patch(
                f"/scalemgmt/v3/filesystems/{filesystem}/policy",
                json=policy,
                params=params,
                headers=_domain_headers(domain),
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to update policy for filesystem '{filesystem}': {str(e)}"
        ) from e
