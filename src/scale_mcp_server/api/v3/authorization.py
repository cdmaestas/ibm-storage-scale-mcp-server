"""IBM Storage Scale Authorization operations.

Authorization endpoints for managing authentication sessions and tokens.
"""

from typing import Optional, Any, Dict
from scale_mcp_server.utils.client import StorageScaleClient, StorageScaleAPIError


async def login_api(
    username: str,
    password: str,
    domain: Optional[str] = None,
) -> Any:
    """Authenticate and create a session.

    Creates an authenticated session and returns session tokens.

    Args:
        username: Username for authentication
        password: Password for authentication
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing authentication tokens and session information

    Raises:
        StorageScaleAPIError: If authentication fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    auth_data = {
        "username": username,
        "password": password,
    }

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/login", json=auth_data, headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to authenticate: {str(e)}") from e


async def logout_api(
    domain: Optional[str] = None,
) -> Any:
    """Logout and invalidate the current session.

    Terminates the current authenticated session and invalidates tokens.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing logout status

    Raises:
        StorageScaleAPIError: If logout fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.post("/scalemgmt/v3/logout", headers=headers)
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to logout: {str(e)}") from e


async def refresh_token_api(
    refresh_token: str,
    domain: Optional[str] = None,
) -> Any:
    """Refresh authentication token.

    Refreshes the authentication token using a valid refresh token.

    Args:
        refresh_token: Valid refresh token
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing new authentication tokens

    Raises:
        StorageScaleAPIError: If token refresh fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    token_data = {
        "refreshToken": refresh_token,
    }

    try:
        async with StorageScaleClient() as client:
            return await client.post(
                "/scalemgmt/v3/token", json=token_data, headers=headers
            )
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(f"Failed to refresh token: {str(e)}") from e


async def get_session_info_api(
    domain: Optional[str] = None,
) -> Any:
    """Get current session information.

    Retrieves information about the current authenticated session.

    Args:
        domain: Domain to be authorized against (default 'StorageScaleDomain')

    Returns:
        Dictionary containing session information

    Raises:
        StorageScaleAPIError: If API call fails
    """
    headers: Dict[str, str] = {}
    if domain:
        headers["X-StorageScaleDomain"] = domain

    try:
        async with StorageScaleClient() as client:
            return await client.get("/scalemgmt/v3/session", headers=headers)
    except StorageScaleAPIError as e:
        raise StorageScaleAPIError(
            f"Failed to get session information: {str(e)}"
        ) from e
