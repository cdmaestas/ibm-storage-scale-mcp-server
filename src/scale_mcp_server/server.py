import argparse
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as package_version
from pathlib import Path

from fastmcp import FastMCP

from scale_mcp_server.adapters.fileops import initialize_fileops_client
from scale_mcp_server.tools.cli import policies as cli_policies
from scale_mcp_server.tools.third_party import fileops
from scale_mcp_server.tools.v2 import (
    filesystems_health,
    nodes_health,
)
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
from scale_mcp_server.utils.read_config import read_config, setup_logging


def _server_version() -> str:
    """Version from the installed package metadata (single source: pyproject)."""
    try:
        return package_version("scale-mcp-server")
    except PackageNotFoundError:
        return "0.0.0+uninstalled"


def main():
    parser = argparse.ArgumentParser(
        description="IBM Storage Scale MCP Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with HTTP transport on default port 8000 (localhost only)
  scale-mcp-server --transport http

  # Run with HTTP transport binding to all interfaces
  scale-mcp-server --transport http --host 0.0.0.0

  # Run with HTTP transport on custom port
  scale-mcp-server --transport http --port 3000

  # Run with stdio transport
  scale-mcp-server --transport stdio

  # Run with custom log level
  scale-mcp-server --transport http --port 8000 --log-level DEBUG

  # Run with filesystem paths for file operations
  scale-mcp-server --transport http --filesystem-paths /data /home/user/projects
        """,
    )

    parser.add_argument(
        "--transport",
        type=str,
        choices=["stdio", "http"],
        default="http",
        help="Transport method to use: stdio or http (StreamableHTTP, default: http)",
    )

    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host address to bind to for http transport (default: 127.0.0.1). Use 0.0.0.0 to bind to all interfaces.",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port number for http transport (default: 8000).",
    )

    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Log level for the MCP server (default: INFO).",
    )

    parser.add_argument(
        "--filesystem-paths",
        type=str,
        nargs="+",
        help="Allowed directory paths for filesystem operations (space-separated). "
        "These paths will be mounted to the filesystem MCP server.",
    )

    args = parser.parse_args()

    # Load configuration
    config_path = Path(__file__).parent.parent.parent / "config" / "mcp_config.ini"
    try:
        config_data = read_config(config_path=config_path)
    except FileNotFoundError as e:
        parser.error(str(e))
    setup_logging(config_data)

    # Initialize MCP server
    mcp = FastMCP(name="scale-mcp-server", version=_server_version())

    # Mounting sub-servers
    mcp.mount(afm.mcp)
    mcp.mount(afmcos.mcp)
    mcp.mount(api_health.mcp)
    mcp.mount(authorization.mcp)
    mcp.mount(clusters.mcp)
    mcp.mount(config.mcp)
    mcp.mount(diagnostics.mcp)
    mcp.mount(filesets.mcp)
    mcp.mount(filesystem_disks.mcp)
    mcp.mount(filesystems.mcp)
    mcp.mount(health.mcp)
    mcp.mount(managers.mcp)
    mcp.mount(node_classes.mcp)
    mcp.mount(nodes.mcp)
    mcp.mount(nsds.mcp)
    mcp.mount(operations.mcp)
    mcp.mount(policies.mcp)
    mcp.mount(quotas.mcp)
    mcp.mount(remote_clusters.mcp)
    mcp.mount(remote_filesystems.mcp)
    mcp.mount(snapshots.mcp)
    mcp.mount(storage_pools.mcp)
    mcp.mount(troubleshooting.mcp)
    mcp.mount(version.mcp)
    mcp.mount(xcp.mcp)
    # V2
    mcp.mount(nodes_health.mcp)
    mcp.mount(filesystems_health.mcp)
    # CLI tools
    mcp.mount(cli_policies.mcp)

    # Setup fileops tools if paths are provided
    if args.filesystem_paths:
        try:
            # Initialize the fileops client with allowed paths
            initialize_fileops_client(args.filesystem_paths)
            # Mount the file operations tools
            mcp.mount(fileops.mcp)
            print(f"Registered file operations tools with allowed paths: {', '.join(args.filesystem_paths)}")
            print("The file operations server supports MCP Roots protocol for dynamic directory access.")
        except Exception as e:
            print(f"Error: Could not setup file operations tools: {e}")
            print("  File operations will not be available.")
            print("  Make sure Node.js and npx are installed.")
            raise

    fastmcp_config = config_data.get("fastmcp", {})
    log_level = args.log_level if args.log_level else fastmcp_config.get("level", "INFO")

    run_kwargs = {"transport": args.transport, "log_level": log_level}

    # Host and port are valid for http transport
    if args.transport == "http":
        run_kwargs["host"] = args.host
        run_kwargs["port"] = args.port

    # Run the MCP server
    mcp.run(**run_kwargs)
