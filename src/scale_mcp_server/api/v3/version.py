"""IBM Storage Scale Version operations."""

from typing import Any

from scale_mcp_server.utils.client import StorageScaleAPIError, StorageScaleClient


async def get_version_api(
    domain: str | None = None,
) -> Any:
    """Get IBM Storage Scale version information.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing version information

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get("/scalemgmt/v3/version", headers=headers)
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to get version information: {str(e)}") from e
