"""IBM Storage Scale CLI Policy Tools."""

import json
import logging
import os
from pathlib import Path

from fastmcp import FastMCP

from scale_mcp_server.adapters.base import CommandError
from scale_mcp_server.adapters.ssh_executor import SSHCommandExecutor
from scale_mcp_server.utils.helpers import clean_output
from scale_mcp_server.utils.read_config import read_config

logger = logging.getLogger(__name__)

# Create the CLI MCP server
mcp = FastMCP("scale-cli", instructions="IBM Storage Scale CLI command operations via SSH")


def _load_ssh_settings() -> dict:
    """Load and validate SSH connection settings from the config file.

    Loaded lazily at tool-call time so that importing this module (and thus
    starting the server or running tests) does not require a config file.
    """
    config_path = Path(__file__).resolve().parents[4] / "config" / "scale_config.ini"
    if not config_path.is_file():
        raise FileNotFoundError(f"Config file '{config_path}' does not exist.")
    config = read_config(config_path)

    if "ssh" not in config:
        raise ValueError("Missing [ssh] section in configuration file")

    ssh_config = config["ssh"]
    if not ssh_config.get("hostname"):
        raise ValueError("Missing 'hostname' in [ssh] configuration")
    if not ssh_config.get("username"):
        raise ValueError("Missing 'username' in [ssh] configuration")

    key_path = ssh_config.get("key_path") or None
    if key_path:
        key_path = os.path.expanduser(key_path)

    auto_add = str(ssh_config.get("auto_add_host_keys", "false")).strip().lower() in (
        "1",
        "true",
        "yes",
        "on",
    )

    return {
        "host": ssh_config["hostname"],
        "port": int(ssh_config.get("port", 22)),
        "username": ssh_config["username"],
        "password": ssh_config.get("password") or None,
        "key_filename": key_path,
        # Same default timeout as the HTTP API
        "command_timeout": int(float(config.get("scale_api", {}).get("timeout", 5.0))),
        "auto_add_host_keys": auto_add,
    }


@mcp.tool()
def apply_policy(filesystem: str) -> str:
    """Execute mmapplypolicy command to apply the ILM policy on a filesystem.

    This command applies the policy that was provided.
    It extracts the policy from filesystem metadata and executes it.

    Args:
        filesystem: The filesystem name (e.g., 'fs1')

    Returns:
        str: Command output and execution status
    """
    try:
        # Create SSH executor with configured timeout
        ssh = _load_ssh_settings()
        executor = SSHCommandExecutor(
            host=ssh["host"],
            username=ssh["username"],
            password=ssh["password"] if not ssh["key_filename"] else None,
            key_filename=ssh["key_filename"],
            port=ssh["port"],
            command_timeout=ssh["command_timeout"],
            auto_add_host_keys=ssh["auto_add_host_keys"],
        )

        # Execute mmapplypolicy directly without extracting policy to file
        command = ["mmapplypolicy", filesystem, "-I", "yes"]
        logger.info(f"Running policy on filesystem '{filesystem}'")

        # Execute via SSH using context manager
        with executor:
            result = executor.execute(command)

        # Return structured JSON response for agent consumption
        response = {
            "status": "success" if result.success else "failed",
            "filesystem": filesystem,
            "exit_code": result.returncode,
            "output": clean_output(result.stdout),
            "error": clean_output(result.stderr) if not result.success else None,
        }

        if not result.success:
            raise CommandError(json.dumps(response))

        return json.dumps(response)

    except CommandError as e:
        logger.error(f"Failed to execute policy: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise
