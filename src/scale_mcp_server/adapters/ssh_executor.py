"""SSH command executor for IBM Storage Scale MCP Server.

This module provides remote command execution via SSH using paramiko.
"""

import logging
from typing import Any

import paramiko

from .base import (
    CommandError,
    CommandExecutionError,
    CommandExecutorInterface,
    CommandResult,
    SSHConnectionError,
)

logger = logging.getLogger(__name__)


class SSHCommandExecutor(CommandExecutorInterface):
    """Execute commands remotely via SSH.

    This executor runs commands on a remote host using SSH protocol
    via the paramiko library. It manages SSH connections and provides
    automatic connection handling.
    """

    def __init__(
        self,
        host: str,
        username: str,
        password: str | None = None,
        key_filename: str | None = None,
        port: int = 22,
        command_timeout: int = 30,
        auto_add_host_keys: bool = False,
    ):
        """Initialize the SSH command executor.

        Args:
            host: Remote host address
            username: SSH username
            password: SSH password (optional if using key)
            key_filename: Path to SSH private key file (optional)
            port: SSH port (default: 22)
            command_timeout: Maximum execution time in seconds (default: 30)
            auto_add_host_keys: If True, automatically trust unknown SSH host
                keys (paramiko AutoAddPolicy). This is insecure - it exposes
                the connection to man-in-the-middle attacks - and defaults to
                False, meaning the host must be present in the known_hosts
                store or the connection is rejected.

        Raises:
            CommandError: If configuration is invalid
        """
        if not host:
            raise CommandError("host is required for SSH execution")
        if not username:
            raise CommandError("username is required for SSH execution")
        if not password and not key_filename:
            raise CommandError("Either password or key_filename must be provided for SSH authentication")

        self.host = host
        self.username = username
        self.password = password
        self.key_filename = key_filename
        self.port = port
        self.command_timeout = command_timeout
        self.auto_add_host_keys = auto_add_host_keys
        self.ssh_client: Any | None = None

        logger.info(f"SSHCommandExecutor initialized for {username}@{host}:{port} with timeout={command_timeout}s")

    def connect(self) -> None:
        """Establish SSH connection.

        Raises:
            SSHConnectionError: If connection fails
        """
        if self.ssh_client:
            logger.debug("SSH connection already established")
            return

        try:
            self.ssh_client = paramiko.SSHClient()  # type: ignore
            # Trust the system/user known_hosts store for host verification.
            self.ssh_client.load_system_host_keys()  # type: ignore
            if self.auto_add_host_keys:
                logger.warning(
                    "auto_add_host_keys is enabled: unknown SSH host keys will "
                    "be trusted automatically (susceptible to MITM attacks)."
                )
                self.ssh_client.set_missing_host_key_policy(  # type: ignore
                    paramiko.AutoAddPolicy()
                )
            else:
                self.ssh_client.set_missing_host_key_policy(  # type: ignore
                    paramiko.RejectPolicy()
                )

            connect_kwargs = {
                "hostname": self.host,
                "port": self.port,
                "username": self.username,
                "timeout": self.command_timeout,
            }

            if self.password:
                connect_kwargs["password"] = self.password
            if self.key_filename:
                connect_kwargs["key_filename"] = self.key_filename

            logger.info(f"Connecting to {self.username}@{self.host}:{self.port}")
            self.ssh_client.connect(**connect_kwargs)
            logger.info(f"SSH connection established to {self.host}")

        except Exception as e:
            error_msg = f"Failed to connect to {self.host}: {str(e)}"
            logger.error(error_msg)
            raise SSHConnectionError(error_msg) from e

    def disconnect(self) -> None:
        """Close SSH connection."""
        if self.ssh_client:
            self.ssh_client.close()
            self.ssh_client = None
            logger.info(f"SSH connection to {self.host} closed")

    def execute(self, command: list[str], **kwargs) -> CommandResult:
        """Execute a command via SSH on the remote host.

        Args:
            command: Command and arguments as a list
            **kwargs: Additional parameters (ignored for SSH execution)

        Returns:
            CommandResult: Unified result structure with stdout, stderr, and returncode

        Raises:
            CommandExecutionError: If command execution fails, including when
                the command exceeds the configured timeout
            SSHConnectionError: If SSH connection fails

        Note:
            Parameters like 'shell' and 'cwd' are not applicable to SSH
            execution and will be ignored if provided.
        """
        command_str = " ".join(command)

        try:
            # Connect if not already connected
            if not self.ssh_client:
                self.connect()

            logger.info(f"Executing SSH command on {self.host}: {command_str}")

            stdin, stdout, stderr = self.ssh_client.exec_command(  # type: ignore
                command_str, timeout=self.command_timeout
            )

            # Wait for command to complete and get exit status
            exit_code = stdout.channel.recv_exit_status()
            stdout_str = stdout.read().decode("utf-8")
            stderr_str = stderr.read().decode("utf-8")

            command_result = CommandResult(
                stdout=stdout_str, stderr=stderr_str, returncode=exit_code, command=command_str
            )

            if command_result.success:
                logger.info("SSH command executed successfully (exit code: 0)")
            else:
                logger.warning(f"SSH command failed with exit code {exit_code}")

            return command_result

        except Exception as e:
            error_msg = f"SSH command execution failed: {str(e)}"
            logger.error(error_msg)
            raise CommandExecutionError(error_msg) from e

    def __enter__(self):
        """Context manager entry - establish connection."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - close connection."""
        self.disconnect()

    def __del__(self):
        """Cleanup on deletion."""
        self.disconnect()
