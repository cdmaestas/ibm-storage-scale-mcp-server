"""Registration tests: the composed server must expose the full tool surface."""

import re

from fastmcp import FastMCP

from scale_mcp_server.tools.cli import policies as cli_policies
from scale_mcp_server.tools.v2 import filesystems_health, nodes_health
from scale_mcp_server.tools.v3 import (
    afm,
    afmcos,
    api_health,
    authorization,
    clusters,
    config,
    diagnostics,
    filesets,
    filesystem_disks,
    filesystems,
    health,
    managers,
    node_classes,
    nodes,
    nsds,
    operations,
    policies,
    quotas,
    remote_clusters,
    remote_filesystems,
    snapshots,
    storage_pools,
    troubleshooting,
    version,
    xcp,
)

SUB_SERVERS = [
    afm, afmcos, api_health, authorization, clusters, config, diagnostics,
    filesets, filesystem_disks, filesystems, health, managers, node_classes,
    nodes, nsds, operations, policies, quotas, remote_clusters,
    remote_filesystems, snapshots, storage_pools, troubleshooting, version,
    xcp, nodes_health, filesystems_health, cli_policies,
]

EXPECTED_TOOL_COUNT = 151


async def _mounted_tools():
    mcp = FastMCP(name="scale-mcp-server-test")
    for module in SUB_SERVERS:
        mcp.mount(module.mcp)
    return await mcp.list_tools()


async def test_all_sub_servers_mount_and_register():
    tools = await _mounted_tools()
    assert len(tools) == EXPECTED_TOOL_COUNT


async def test_no_duplicate_tool_names():
    tools = await _mounted_tools()
    names = [t.name for t in tools]
    duplicates = {n for n in names if names.count(n) > 1}
    assert not duplicates, f"duplicate tool names: {duplicates}"


async def test_server_module_mounts_every_tool_package():
    """server.py must mount every module that defines an mcp sub-server."""
    from pathlib import Path

    server_src = (
        Path(__file__).parent.parent / "src" / "scale_mcp_server" / "server.py"
    ).read_text()
    mounted = set(re.findall(r"mcp\.mount\((\w+)\.mcp\)", server_src))

    # tools.cli.policies is imported in server.py under the alias cli_policies
    expected = {
        "afm", "afmcos", "api_health", "authorization", "clusters", "config",
        "diagnostics", "filesets", "filesystem_disks", "filesystems", "health",
        "managers", "node_classes", "nodes", "nsds", "operations", "policies",
        "quotas", "remote_clusters", "remote_filesystems", "snapshots",
        "storage_pools", "troubleshooting", "version", "xcp",
        "nodes_health", "filesystems_health", "cli_policies",
    }
    missing = expected - mounted
    assert not missing, f"sub-servers not mounted in server.py: {sorted(missing)}"
