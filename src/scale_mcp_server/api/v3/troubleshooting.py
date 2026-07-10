"""IBM Storage Scale Troubleshooting operations.

Troubleshooting endpoints for advanced diagnostics and problem resolution.
"""

from typing import Optional, Any, Dict
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


async def get_troubleshooting_info_api(
    domain: Optional[str] = None,
) -> Any:
    """Get general troubleshooting information.

    Retrieves general troubleshooting information and diagnostic data.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing troubleshooting information

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get("/scalemgmt/v3/troubleshooting", headers=headers)
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get troubleshooting information: {str(e)}"
        ) from e


async def collect_diagnostics_api(
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

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/troubleshooting:collect",
                json=collection_data,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to collect diagnostics: {str(e)}"
        ) from e


async def get_logs_api(
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

    Raises:
        StorageScaleAPIError: If API call fails
    """
    query_params: Dict[str, Any] = {}
    if component:
        query_params["component"] = component
    if level:
        query_params["level"] = level
    if lines is not None:
        query_params["lines"] = lines

    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get(
                "/scalemgmt/v3/troubleshooting/logs",
                params=query_params,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to get logs: {str(e)}") from e


async def run_diagnostic_test_api(
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

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/troubleshooting:test",
                json=test_data,
                headers=headers,
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to run diagnostic test: {str(e)}"
        ) from e
