"""IBM Storage Scale Policy operations."""

from typing import Optional, Any, Dict
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


async def list_policies_api(
    filesystem: str,
    domain: Optional[str] = None,
) -> Any:
    """List all policies for a filesystem.

    Args:
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing list of policies

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/policies", headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to list policies for filesystem '{filesystem}': {str(e)}"
        ) from e


async def get_policy_api(
    filesystem: str,
    policy_name: Optional[str] = None,
    domain: Optional[str] = None,
) -> Any:
    """Get policy for a filesystem.

    Args:
        filesystem: Filesystem name
        policy_name: Optional policy name to get specific policy
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing policy information

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    endpoint = f"/scalemgmt/v3/filesystems/{filesystem}/policy"
    if policy_name:
        endpoint = f"/scalemgmt/v3/filesystems/{filesystem}/policies/{policy_name}"

    try:
        async with StorageScaleClient() as client:
            return await client.get(endpoint, headers=headers)
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get policy for filesystem '{filesystem}': {str(e)}"
        ) from e


async def create_policy_api(
    filesystem: str,
    policy_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Create a new policy for a filesystem.

    Args:
        filesystem: Filesystem name
        policy_data: Policy configuration data
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing created policy information

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{filesystem}/policies",
                json=policy_data,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        policy_name = policy_data.get("policyName", "unknown")
        raise StorageScaleAPIError(
            f"Failed to create policy '{policy_name}' for filesystem '{filesystem}': {str(e)}"
        ) from e


async def delete_policy_api(
    filesystem: str,
    policy_name: str,
    domain: Optional[str] = None,
) -> Any:
    """Delete a policy from a filesystem.

    Args:
        filesystem: Filesystem name
        policy_name: Policy name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing deletion status

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.delete(
                f"/scalemgmt/v3/filesystems/{filesystem}/policies/{policy_name}",
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to delete policy '{policy_name}' for filesystem '{filesystem}': {str(e)}"
        ) from e


async def update_policy_api(
    filesystem: str,
    policy_name: str,
    policy_data: dict,
    domain: Optional[str] = None,
) -> Any:
    """Update a specific policy for a filesystem.

    Args:
        filesystem: Filesystem name
        policy_name: Policy name
        policy_data: Policy configuration data
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing updated policy information

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.put(
                f"/scalemgmt/v3/filesystems/{filesystem}/policies/{policy_name}",
                json=policy_data,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to update policy '{policy_name}' for filesystem '{filesystem}': {str(e)}"
        ) from e


async def run_policy_api(
    filesystem: str,
    policy_name: str,
    options: Optional[dict] = None,
    domain: Optional[str] = None,
) -> Any:
    """Run/execute a policy on a filesystem.

    Args:
        filesystem: Filesystem name
        policy_name: Policy name to execute
        options: Optional execution options (e.g., nodes, test mode)
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing execution status and job information

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    body = options if options is not None else {}

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{filesystem}/policies/{policy_name}:run",
                json=body,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to run policy '{policy_name}' for filesystem '{filesystem}': {str(e)}"
        ) from e


async def list_policy_jobs_api(
    filesystem: str,
    domain: Optional[str] = None,
) -> Any:
    """List policy execution jobs for a filesystem.

    Args:
        filesystem: Filesystem name
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing list of policy jobs

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/policies/jobs", headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to list policy jobs for filesystem '{filesystem}': {str(e)}"
        ) from e


async def get_policy_job_api(
    filesystem: str,
    job_id: str,
    domain: Optional[str] = None,
) -> Any:
    """Get details of a specific policy execution job.

    Args:
        filesystem: Filesystem name
        job_id: Policy job identifier
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing policy job details

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                f"/scalemgmt/v3/filesystems/{filesystem}/policies/jobs/{job_id}",
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get policy job '{job_id}' for filesystem '{filesystem}': {str(e)}"
        ) from e


async def cancel_policy_job_api(
    filesystem: str,
    job_id: str,
    domain: Optional[str] = None,
) -> Any:
    """Cancel a running policy execution job.

    Args:
        filesystem: Filesystem name
        job_id: Policy job identifier
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing cancellation status

    Raises:
        StorageScaleAPIError: If the API request fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                f"/scalemgmt/v3/filesystems/{filesystem}/policies/jobs/{job_id}:cancel",
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to cancel policy job '{job_id}' for filesystem '{filesystem}': {str(e)}"
        ) from e
