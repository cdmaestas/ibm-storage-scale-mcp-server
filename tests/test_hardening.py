"""Tests for hardening changes: loud config failures and SSH host-key policy."""

import paramiko
import pytest

import scale_mcp_server.adapters.ssh_executor as ssh_module
from scale_mcp_server.adapters.ssh_executor import SSHCommandExecutor
from scale_mcp_server.utils.read_config import read_config


def test_read_config_missing_file_raises(tmp_path):
    """A missing config file must raise, not print-and-exit."""
    with pytest.raises(FileNotFoundError):
        read_config(tmp_path / "does-not-exist.ini")


class _FakeSSHClient:
    """Records the host-key policy set on it; no real connection is made."""

    def __init__(self):
        self.policy = None
        self.loaded_system_keys = False

    def load_system_host_keys(self):
        self.loaded_system_keys = True

    def set_missing_host_key_policy(self, policy):
        self.policy = policy

    def connect(self, **kwargs):
        pass

    def close(self):
        pass


@pytest.fixture
def fake_ssh(monkeypatch):
    created = []

    def factory():
        client = _FakeSSHClient()
        created.append(client)
        return client

    monkeypatch.setattr(ssh_module.paramiko, "SSHClient", factory)
    return created


def test_ssh_defaults_to_reject_policy(fake_ssh):
    executor = SSHCommandExecutor(host="node1", username="admin", password="pw")
    executor.connect()
    client = fake_ssh[0]
    assert client.loaded_system_keys is True
    assert isinstance(client.policy, paramiko.RejectPolicy)


def test_ssh_auto_add_opt_in(fake_ssh):
    executor = SSHCommandExecutor(host="node1", username="admin", password="pw", auto_add_host_keys=True)
    executor.connect()
    client = fake_ssh[0]
    assert isinstance(client.policy, paramiko.AutoAddPolicy)
