"""HTTP client for the IBM Storage Scale REST APIs.

Settings are read once (config file overlaid with SCALE_API_* environment
variables) and connections are pooled in a shared httpx.AsyncClient per event
loop, instead of re-reading the config and opening a new TLS connection for
every request.
"""

import asyncio
import os
import weakref
from pathlib import Path
from typing import Any

import httpx
from fastmcp.utilities.logging import get_logger

from scale_mcp_server.utils.read_config import read_config

logger = get_logger(__name__)

_CONFIG_PATH = Path(__file__).parent.parent.parent.parent / "config" / "scale_config.ini"

_settings_cache: dict[str, Any] | None = None

# One shared AsyncClient per (event loop, base URL); entries disappear with
# their loop so a dead loop's pooled connections are never reused.
_shared_clients: "weakref.WeakKeyDictionary[asyncio.AbstractEventLoop, dict[str, httpx.AsyncClient]]" = (
    weakref.WeakKeyDictionary()
)


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ("1", "true", "yes", "on")


def load_settings(refresh: bool = False) -> dict[str, Any]:
    """Resolve connection settings once and cache them.

    The config file is optional; every value can come from (or be overridden
    by) SCALE_API_HOSTNAME, SCALE_API_V2_PORT, SCALE_API_V3_PORT,
    SCALE_API_TIMEOUT, SCALE_API_USERNAME, SCALE_API_PASSWORD,
    SCALE_API_ALLOW_INSECURE, SCALE_API_CLIENT_CERT, SCALE_API_CLIENT_KEY,
    and SCALE_API_CA_CERT.
    """
    global _settings_cache
    if _settings_cache is not None and not refresh:
        return _settings_cache

    config = read_config(config_path=_CONFIG_PATH) if _CONFIG_PATH.is_file() else {}
    api = dict(config.get("scale_api", {}))
    auth = dict(config.get("authorization", {}))
    env = os.environ

    settings = {
        "hostname": env.get("SCALE_API_HOSTNAME", api.get("hostname", "localhost")),
        "v2_port": int(env.get("SCALE_API_V2_PORT", api.get("v2_port", 443))),
        "v3_port": int(env.get("SCALE_API_V3_PORT", api.get("v3_port", 46443))),
        "timeout": float(env.get("SCALE_API_TIMEOUT", api.get("timeout", 5.0))),
        "username": env.get("SCALE_API_USERNAME", auth.get("username", "admin")),
        "password": env.get("SCALE_API_PASSWORD", auth.get("password", "")),
        "allow_insecure": _as_bool(env.get("SCALE_API_ALLOW_INSECURE", auth.get("allow_insecure", False))),
        # mTLS: PEM client certificate (and separate key, if not bundled into
        # the cert file) presented to the cluster, plus an optional CA bundle
        # used to verify the server certificate.
        "client_cert": env.get("SCALE_API_CLIENT_CERT", auth.get("client_cert")) or None,
        "client_key": env.get("SCALE_API_CLIENT_KEY", auth.get("client_key")) or None,
        "ca_cert": env.get("SCALE_API_CA_CERT", auth.get("ca_cert")) or None,
    }
    for key in ("client_cert", "client_key", "ca_cert"):
        if settings[key]:
            settings[key] = os.path.expanduser(settings[key])
            if not Path(settings[key]).is_file():
                raise FileNotFoundError(f"{key} file '{settings[key]}' does not exist")
    _settings_cache = settings
    return settings


class StorageScaleAPIError(Exception):
    """Exception raised for Storage Scale API errors.

    Attributes:
        status_code: HTTP status code when the server responded, else None
        details: Parsed JSON error body (or raw text) when available
    """

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        details: Any = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.details = details


class StorageScaleClient:
    """IBM Storage Scale REST API client.

    Used as an async context manager. When constructed without overrides it
    borrows a shared, connection-pooled httpx.AsyncClient for the current
    event loop; explicit overrides get a private client that is closed on
    exit.
    """

    def __init__(
        self,
        base_url: str | None = None,
        username: str | None = None,
        password: str | None = None,
        verify_ssl: bool | None = None,
        timeout: float | None = None,
        api_version: str | None = None,
    ):
        settings = load_settings()
        port = settings["v2_port"] if api_version == "v2" else settings["v3_port"]

        self.base_url = (base_url or f"https://{settings['hostname']}:{port}").rstrip("/")
        self.username = username or settings["username"]
        self.password = password or settings["password"]

        client_cert = settings.get("client_cert")
        client_key = settings.get("client_key")
        self.cert = None
        if client_cert:
            self.cert = (client_cert, client_key) if client_key else client_cert

        # With a client certificate configured and no password, identity comes
        # from the certificate alone; do not send a basic-auth header.
        password_configured = bool(password or settings["password"])
        if self.cert and not password_configured:
            self.auth = None
        else:
            self.auth = (self.username, self.password)

        if verify_ssl is not None:
            verify = verify_ssl
        elif settings["allow_insecure"]:
            verify = False
        else:
            verify = settings.get("ca_cert") or True
        timeout_val = timeout or settings["timeout"]

        has_overrides = any(v is not None for v in (base_url, username, password, verify_ssl, timeout))
        self._owns_session = has_overrides
        if has_overrides:
            self.session = self._new_session(verify, timeout_val)
        else:
            self.session = self._shared_session(verify, timeout_val)

        logger.debug(f"Initialized StorageScaleClient for {self.base_url}")

    def _new_session(self, verify, timeout_val: float) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            base_url=self.base_url,
            auth=self.auth,
            cert=self.cert,
            timeout=httpx.Timeout(timeout=timeout_val),
            verify=verify,
        )

    def _shared_session(self, verify, timeout_val: float) -> httpx.AsyncClient:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            # No running loop (e.g. constructed synchronously); fall back to a
            # private client.
            self._owns_session = True
            return self._new_session(verify, timeout_val)

        loop_clients = _shared_clients.setdefault(loop, {})
        client = loop_clients.get(self.base_url)
        if client is None or client.is_closed:
            client = self._new_session(verify, timeout_val)
            loop_clients[self.base_url] = client
        return client

    async def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        """Execute a request and return the parsed JSON body."""
        try:
            logger.debug(f"{method} {endpoint}")
            response = await self.session.request(method, endpoint, **kwargs)
            response.raise_for_status()
            logger.debug(f"{method} {endpoint} - Status: {response.status_code}")
            if response.status_code == 204 or not response.content:
                return {}
            return response.json()
        except httpx.HTTPStatusError as e:
            status = e.response.status_code
            try:
                details = e.response.json()
            except ValueError:
                details = e.response.text
            message = None
            if isinstance(details, dict):
                message = details.get("message") or (details.get("error") or {}).get("message")
            logger.error(f"{method} {endpoint} failed with HTTP {status}: {details}")
            raise StorageScaleAPIError(
                f"API request failed with HTTP {status}" + (f": {message}" if message else ""),
                status_code=status,
                details=details,
            ) from e
        except httpx.HTTPError as e:
            logger.error(f"{method} {endpoint} failed: {e}")
            raise StorageScaleAPIError(f"API request failed: {e}") from e

    async def get(self, endpoint: str, **kwargs) -> Any:
        """Execute GET request."""
        return await self._request("GET", endpoint, **kwargs)

    async def post(self, endpoint: str, **kwargs) -> Any:
        """Execute POST request."""
        return await self._request("POST", endpoint, **kwargs)

    async def put(self, endpoint: str, **kwargs) -> Any:
        """Execute PUT request."""
        return await self._request("PUT", endpoint, **kwargs)

    async def patch(self, endpoint: str, **kwargs) -> Any:
        """Execute PATCH request."""
        return await self._request("PATCH", endpoint, **kwargs)

    async def delete(self, endpoint: str, **kwargs) -> Any:
        """Execute DELETE request."""
        return await self._request("DELETE", endpoint, **kwargs)

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit; only private clients are closed."""
        if self._owns_session:
            await self.session.aclose()
