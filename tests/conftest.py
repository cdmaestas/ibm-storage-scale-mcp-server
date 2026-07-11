"""Shared fixtures for the scale-mcp-server test suite."""

import httpx
import pytest
import respx

import scale_mcp_server.utils.client as client_module

TEST_CONFIG = {
    "scale_api": {
        "hostname": "testhost",
        "v2_port": 443,
        "v3_port": 46443,
        "timeout": 5.0,
    },
    "authorization": {
        "username": "testuser",
        "password": "testpass",
        "allow_insecure": True,
    },
}


@pytest.fixture(autouse=True)
def test_config(monkeypatch):
    """Point StorageScaleClient at a fixed test config instead of the ini file."""
    monkeypatch.setattr(client_module, "read_config", lambda config_path: TEST_CONFIG)


@pytest.fixture
def mock_api():
    """Intercept all HTTP traffic to the test cluster and record requests."""
    with respx.mock(assert_all_called=False) as router:
        router.route(host="testhost").mock(
            return_value=httpx.Response(200, json={"status": "ok"})
        )
        yield router
