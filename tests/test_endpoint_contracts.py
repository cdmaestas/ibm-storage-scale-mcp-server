"""Contract tests: each api function must hit its documented endpoint.

Every wrapper in scale_mcp_server.api is called with minimal arguments against
a mocked cluster, and the HTTP method and URL path of the request it produced
are asserted against the contract table in contracts.py.
"""

import importlib

import pytest

from contracts import CONTRACTS


@pytest.mark.parametrize(
    "contract", CONTRACTS, ids=[f"{c.module}.{c.func}" for c in CONTRACTS]
)
async def test_endpoint_contract(contract, mock_api):
    module = importlib.import_module(f"scale_mcp_server.api.{contract.module}")
    func = getattr(module, contract.func)

    result = await func(**contract.kwargs)

    assert result == {"status": "ok"}
    assert len(mock_api.calls) == 1, "expected exactly one HTTP request"
    request = mock_api.calls.last.request
    expected_path = contract.path.format(**contract.kwargs)
    assert request.method == contract.method
    assert request.url.path == expected_path


async def test_domain_header_is_sent(mock_api):
    """The optional domain argument must become the X-StorageScaleDomain header."""
    from scale_mcp_server.api.v3.version import get_version_api

    await get_version_api(domain="MyDomain")

    request = mock_api.calls.last.request
    assert request.headers["X-StorageScaleDomain"] == "MyDomain"


async def test_api_error_is_wrapped(mock_api):
    """HTTP errors must surface as StorageScaleAPIError, not raw httpx errors."""
    import httpx

    from scale_mcp_server.api.v3.version import get_version_api
    from scale_mcp_server.utils.client import StorageScaleAPIError

    mock_api.route(host="testhost").mock(
        return_value=httpx.Response(500, json={"message": "boom"})
    )

    with pytest.raises(StorageScaleAPIError):
        await get_version_api()
