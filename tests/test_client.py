"""Behavior tests for StorageScaleClient: settings, pooling, errors, LRO wait."""

import httpx
import pytest
from conftest import REAL_LOAD_SETTINGS

import scale_mcp_server.utils.client as client_module
from scale_mcp_server.utils.client import StorageScaleAPIError, StorageScaleClient


async def test_shared_client_is_reused_within_a_loop(mock_api):
    """Default-constructed clients on one loop share a pooled httpx client."""
    async with StorageScaleClient() as a:
        pass
    async with StorageScaleClient() as b:
        pass
    assert a.session is b.session
    assert not a.session.is_closed, "shared session must survive context exit"


async def test_override_client_is_private_and_closed(mock_api):
    """Explicit overrides get a private client that closes on exit."""
    async with StorageScaleClient(base_url="https://testhost:46443") as c:
        assert c.session is not None
    assert c.session.is_closed


async def test_error_carries_status_and_details(mock_api):
    mock_api.route(host="testhost").mock(return_value=httpx.Response(422, json={"message": "invalid fileset"}))
    async with StorageScaleClient() as client:
        with pytest.raises(StorageScaleAPIError) as excinfo:
            await client.get("/scalemgmt/v3/filesystems")
    assert excinfo.value.status_code == 422
    assert excinfo.value.details == {"message": "invalid fileset"}
    assert "422" in str(excinfo.value)
    assert "invalid fileset" in str(excinfo.value)


async def test_empty_body_returns_empty_dict(mock_api):
    mock_api.route(host="testhost").mock(return_value=httpx.Response(204))
    async with StorageScaleClient() as client:
        assert await client.delete("/scalemgmt/v3/nsds/nsd1") == {}


def test_env_vars_override_settings(monkeypatch, tmp_path):
    """SCALE_API_* environment variables win, and the ini file is optional."""
    monkeypatch.setattr(client_module, "_CONFIG_PATH", tmp_path / "missing.ini")
    monkeypatch.setenv("SCALE_API_HOSTNAME", "env-host")
    monkeypatch.setenv("SCALE_API_PASSWORD", "env-pass")
    monkeypatch.setenv("SCALE_API_ALLOW_INSECURE", "false")

    settings = REAL_LOAD_SETTINGS(refresh=True)

    assert settings["hostname"] == "env-host"
    assert settings["password"] == "env-pass"
    assert settings["allow_insecure"] is False
    # untouched values fall back to defaults without a config file
    assert settings["v3_port"] == 46443

    # do not leak the cached env-derived settings into other tests
    client_module._settings_cache = None


async def test_wait_for_operation_polls_until_done(mock_api):
    from scale_mcp_server.api.v3.operations import wait_for_operation_api

    mock_api.route(host="testhost").mock(
        side_effect=[
            httpx.Response(200, json={"name": "op-1", "done": False}),
            httpx.Response(200, json={"name": "op-1", "done": True}),
        ]
    )

    result = await wait_for_operation_api("op-1", poll_interval=0.01, timeout=5.0)

    assert result["done"] is True
    assert len(mock_api.calls) == 2


async def test_wait_for_operation_times_out(mock_api):
    from scale_mcp_server.api.v3.operations import wait_for_operation_api

    mock_api.route(host="testhost").mock(return_value=httpx.Response(200, json={"name": "op-2", "done": False}))

    with pytest.raises(StorageScaleAPIError, match="Timed out"):
        await wait_for_operation_api("op-2", poll_interval=0.01, timeout=0.05)


def _mtls_settings(**overrides):
    from conftest import TEST_SETTINGS

    settings = dict(TEST_SETTINGS)
    settings.update({"client_cert": None, "client_key": None, "ca_cert": None})
    settings.update(overrides)
    return settings


def test_mtls_cert_and_ca_are_passed_to_httpx(monkeypatch, tmp_path):
    cert = tmp_path / "client.pem"
    key = tmp_path / "client.key"
    ca = tmp_path / "ca.pem"
    for f in (cert, key, ca):
        f.write_text("PEM")

    captured = {}

    class FakeAsyncClient:
        def __init__(self, **kwargs):
            captured.update(kwargs)
            self.is_closed = False

    monkeypatch.setattr(client_module.httpx, "AsyncClient", FakeAsyncClient)
    monkeypatch.setattr(
        client_module,
        "load_settings",
        lambda refresh=False: _mtls_settings(
            client_cert=str(cert),
            client_key=str(key),
            ca_cert=str(ca),
            password="",
            allow_insecure=False,
        ),
    )

    StorageScaleClient()

    assert captured["cert"] == (str(cert), str(key))
    assert captured["verify"] == str(ca)
    assert captured["auth"] is None, "no basic auth when cert-only"


def test_mtls_with_password_keeps_basic_auth(monkeypatch, tmp_path):
    cert = tmp_path / "client.pem"
    cert.write_text("PEM")

    captured = {}

    class FakeAsyncClient:
        def __init__(self, **kwargs):
            captured.update(kwargs)
            self.is_closed = False

    monkeypatch.setattr(client_module.httpx, "AsyncClient", FakeAsyncClient)
    monkeypatch.setattr(
        client_module,
        "load_settings",
        lambda refresh=False: _mtls_settings(client_cert=str(cert)),
    )

    StorageScaleClient()

    assert captured["cert"] == str(cert), "bundled cert passed as a single path"
    assert captured["auth"] == ("testuser", "testpass")


def test_missing_cert_file_raises(monkeypatch, tmp_path):
    monkeypatch.setattr(client_module, "_CONFIG_PATH", tmp_path / "missing.ini")
    monkeypatch.setenv("SCALE_API_CLIENT_CERT", str(tmp_path / "nope.pem"))

    with pytest.raises(FileNotFoundError, match="client_cert"):
        REAL_LOAD_SETTINGS(refresh=True)

    client_module._settings_cache = None


def test_no_cert_settings_leave_defaults_unchanged(monkeypatch):
    """Without mTLS config, auth and verification behave exactly as before."""
    captured = {}

    class FakeAsyncClient:
        def __init__(self, **kwargs):
            captured.update(kwargs)
            self.is_closed = False

    monkeypatch.setattr(client_module.httpx, "AsyncClient", FakeAsyncClient)
    monkeypatch.setattr(client_module, "load_settings", lambda refresh=False: _mtls_settings())

    StorageScaleClient()

    assert captured["cert"] is None
    assert captured["auth"] == ("testuser", "testpass")
    assert captured["verify"] is False, "allow_insecure=true in test settings"


def test_server_version_comes_from_package_metadata():
    from importlib.metadata import version as package_version

    from scale_mcp_server.server import _server_version

    assert _server_version() == package_version("scale-mcp-server")
