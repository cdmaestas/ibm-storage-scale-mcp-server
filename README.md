# IBM Storage Scale MCP Server

Model Context Protocol (MCP) server for interacting with IBM Storage Scale.

>[NOTE]
>This MCP server supports both StreamableHTTP and stdio transports. By default, it uses StreamableHTTP transport on `127.0.0.1:8000`.

## Installation Guide

### Prerequisites

- Python 3.12 or later
- UV package manager (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Node.js 22 and npx (optional, for file operations support)
  ```bash
  curl -fsSL https://rpm.nodesource.com/setup_22.x | sudo bash -
  sudo yum install -y nsolid
  ```

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/IBM/ibm-storage-scale-mcp-server.git
   cd ibm-storage-scale-mcp-server
   ```

2. **Install dependencies using uv**:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install .
   ```

2. **Configure Scale connection settings**:
   
   ```bash
   cp config/scale_config.ini.example config/scale_config.ini
   ```
   
   Edit [`config/scale_config.ini`](config/scale_config.ini) with your IBM Storage Scale cluster details:
   
   ```ini
   [scale_api]
   hostname = your-scale-cluster.example.com
   v2_port = 443
   v3_port = 46443
   timeout = 5.0
   
   [authorization]
   username = your-username
   password = your-password
   # true disables TLS certificate verification (self-signed cluster certs)
   allow_insecure = false
   # mTLS alternative to username/password (see below):
   # client_cert = /path/to/client-cert.pem
   # client_key = /path/to/client-key.pem
   # ca_cert = /path/to/ca-bundle.pem
   
   [domain]
   domain = your-domain

   [ssh]
   # SSH connection settings for remote CLI commands
   hostname = your-scale-node.example.com
   port = 22
   username = your-username
   password = your-ssh-password
   key_path = your-ssh-key  # Alternative to password authentication
   ```

   Replace the placeholder values with your actual Scale cluster credentials and connection details.

   **Note:** The `[ssh]` section is required for CLI-based tools that execute commands directly on Scale nodes (such as policy operations). You can use either password or SSH key authentication (precedence over password authentication).

   **Environment variable overrides:** every `[scale_api]` and
   `[authorization]` value can be supplied (or overridden) via environment
   variables, so containers and CI never need credentials on disk:

   | Variable | Overrides |
   |---|---|
   | `SCALE_API_HOSTNAME` | `scale_api.hostname` |
   | `SCALE_API_V2_PORT` / `SCALE_API_V3_PORT` | `scale_api.v2_port` / `v3_port` |
   | `SCALE_API_TIMEOUT` | `scale_api.timeout` |
   | `SCALE_API_USERNAME` / `SCALE_API_PASSWORD` | `authorization.username` / `password` |
   | `SCALE_API_ALLOW_INSECURE` | `authorization.allow_insecure` |
   | `SCALE_API_CLIENT_CERT` / `SCALE_API_CLIENT_KEY` | `authorization.client_cert` / `client_key` |
   | `SCALE_API_CA_CERT` | `authorization.ca_cert` |

   With environment variables set, the `config/scale_config.ini` file is
   optional for the REST API tools.

   **mTLS client-certificate authentication:** set `client_cert` (and
   `client_key` if the private key is not bundled into the cert file) to
   authenticate to the native REST API with a certificate instead of
   username/password. When a client certificate is configured and `password`
   is empty, no basic-auth header is sent. `ca_cert` points TLS verification
   at your cluster's CA bundle instead of the system trust store.

3. **Start the server using uv or python**:
   ```bash
   # Using uv (default: HTTP transport on localhost:8000)
   uv run scale-mcp-server
   ```

### Usage Examples

```bash
# Run with HTTP transport on default port (localhost:8000)
scale-mcp-server --transport http

# Run with HTTP transport binding to all interfaces
scale-mcp-server --transport http --host 0.0.0.0

# Run with HTTP transport on custom port
scale-mcp-server --transport http --port 3000

# Run with stdio transport
scale-mcp-server --transport stdio

# Run with custom host, port, and log level
scale-mcp-server --transport http --host 0.0.0.0 --port 3000 --log-level DEBUG
```

## Third-Party Integrations

The server supports optional third-party MCP server integrations to extend functionality beyond IBM Storage Scale management.

### File Operations

The server can optionally mount the [MCP filesystem server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) to provide local file operations alongside IBM Storage Scale management. This enables:

- Reading and writing files
- Creating and listing directories
- Moving files and directories
- Searching files with patterns
- Getting file metadata

**Usage:**
```bash
scale-mcp-server --transport http --filesystem-paths /path/to/dir1 /path/to/dir2
```

## Available Tools

The MCP server exposes the complete IBM Storage Scale 6.0.1 native REST API
(`/scalemgmt/v3`, all 144 documented endpoints) plus v2 health monitoring and
CLI-based tools — 152 tools in total.

### Native REST API (v3)

- **AFM (Active File Management)**: Fileset replication management
  - `list_afm_states`, `get_afm_state`: AFM state of all/one AFM fileset
  - `check_afm_dirty`, `check_afm_uncached`: Find modified / uncached files
  - `flush_afm_queue`, `resume_afm_requeued`: Queue management
  - `resync_afm_fileset`, `start_afm_fileset`, `stop_afm_fileset`: Sync control
  - `set_afm_local`, `reset_afm_local`: Manage the local bit on filepaths
- **AFMCOS (AFM to Cloud Object Storage)**
  - `get_cos_keys`, `set_cos_keys`, `delete_cos_keys`: Bucket key management
  - `configure_afmcos`: Configure an AFM-to-COS relationship for a fileset
  - `upload_afmcos_objects`, `download_afmcos_objects`, `evict_afmcos_objects`,
    `delete_afmcos_objects`, `reconcile_afmcos`: Object transfer operations
- **API Health**: `get_api_health`, `get_node_api_health` — health of the
  native REST API service (scaleadmd) on cluster nodes
- **Authorization (RBAC)**
  - `can_i`, `can_i_impersonate`: Permission checks
  - `list_rbac_domains`, `get_rbac_domain`, `create_rbac_domain`,
    `update_rbac_domain`, `delete_rbac_domain`: Domain management
  - `get_rbac_module`, `update_rbac_module`: Policy evaluation rule set
- **Clusters**: `list_clusters`, `create_cluster`, `migrate_cluster`,
  `list_cluster_trust`
- **Config**: Administration daemon (scaleadmd) and IO daemon (mmfsd) settings
  - `get_admin_config`, `get_admin_config_attribute`, `update_admin_config`
  - `get_cluster_config`, `get_cluster_config_attribute`, `update_cluster_config`
- **Diagnostics**: `get_node_version` — mmfsd version report of a node
- **Filesets**: `list_filesets`, `create_independent_fileset`,
  `create_dependent_fileset`, `get_fileset`, `update_fileset`, `delete_fileset`,
  `get_fileset_usage`, `link_fileset`, `unlink_fileset`
- **Filesystem Disks**
  - `list_filesystem_disks`, `get_filesystem_disk`, `get_disks_quorum`
  - `add_filesystem_disk`, `delete_filesystem_disk`,
    `batch_add_filesystem_disks`, `batch_delete_filesystem_disks`
- **Filesystems**
  - `list_filesystems`, `get_filesystem`, `create_filesystem`,
    `update_filesystem`, `delete_filesystem`
  - `get_mount_status`, `mount_filesystem`, `unmount_filesystem`,
    `mount_all_filesystems`, `unmount_all_filesystems`
  - `rebalance_filesystem`, `restripe_filesystem`
  - `list_directory`, `stat_directory`, `create_directory`, `delete_directory`
- **Health**: Convenience roll-ups over v3 status endpoints
  - `get_filesystem_health`, `get_node_health`, `get_node_diagnostics`,
    `get_cluster_health_summary`
- **Managers**: `set_cluster_manager`, `set_filesystem_manager`
- **Node Classes**: `list_node_classes`, `get_node_class`, `create_node_class`,
  `update_node_class`, `delete_node_class`
- **Nodes**: `add_node`, `batch_add_nodes`, `start_nodes`, `stop_nodes`,
  `get_nodes_status`, `get_nodes_config`
- **NSDs**: `list_nsds`, `get_nsd`, `create_nsd`, `update_nsd`, `delete_nsd`,
  `batch_create_nsds`, `batch_delete_nsds`
- **Operations (LRO)**: Track long-running operations returned by async requests
  - `list_operations`, `get_operation`, `get_operation_output`,
    `cancel_operation`, `delete_operation`
  - `wait_for_operation`: client-side polling until an LRO completes
- **Policies**: `get_policy`, `update_policy` — the file system policy
  (policy runs are CLI-based; see `apply_policy` below)
- **Quotas**
  - `list_quotas`, `set_quota`, `check_quotas`, `update_quota_config`
  - `list_fileset_quotas`, `set_fileset_quota`, `check_fileset_quotas`
- **Remote Clusters**: `list_remote_clusters`, `get_remote_cluster`,
  `add_remote_cluster`, `update_remote_cluster`, `delete_remote_cluster`,
  `authorize_remote_cluster`, `deauthorize_remote_cluster`,
  `refresh_remote_cluster`
- **Remote Filesystems**: `add_remote_filesystem`, `update_remote_filesystem`,
  `delete_remote_filesystem`
- **Snapshots**: Filesystem and fileset snapshots
  - `list_filesystem_snapshots`, `create_filesystem_snapshot`,
    `get_filesystem_snapshot`, `delete_filesystem_snapshot`
  - `list_fileset_snapshots`, `create_fileset_snapshot`, `get_fileset_snapshot`,
    `delete_fileset_snapshot`
  - `get_snapdir_settings`
- **Storage Pools**: `list_storage_pools`, `get_storage_pool`,
  `update_storage_pool`
- **Troubleshooting**: `clear_nsd_id`, `get_persistent_reserve_keys`,
  `clear_persistent_reserve_keys`
- **Version**: `get_version` — version of the scaleadmd service
- **XCP (parallel copy)**
  - `list_xcp_operations`, `get_xcp_operation`
  - `get_xcp_config`, `update_xcp_config`
  - `start_xcp_copy`, `sync_xcp`, `verify_xcp`

> [!NOTE]
> Many v3 write operations are asynchronous and return a long-running
> operation (LRO). Use the **Operations** tools to track, read output from,
> or cancel them.

### Health Monitoring (v2 GUI REST API)

The native v3 API does not expose `mmhealth`-style events; these tools use the
v2 GUI REST API (requires the Scale GUI, `v2_port` in the config):

- `get_filesystem_health_states`, `get_filesystem_health_events`
- `get_node_health_states`, `get_node_health_events`

### CLI Tools (via SSH)

- `apply_policy`: Run `mmapplypolicy` on a Scale node (policy execution is not
  available through the REST API); requires the `[ssh]` config section

## Usage and Integration

### Using MCP Inspector

The MCP server can be tested directly using [MCP Inspector](https://github.com/modelcontextprotocol/inspector).

#### Prerequisites

Follow the [setup instructions](https://github.com/modelcontextprotocol/inspector?tab=readme-ov-file#quick-start-ui-mode) from MCP Inspector.

#### Connecting via HTTP Transport

1. **Start the MCP server**:
   ```bash
   scale-mcp-server --transport http
   ```

2. **Connect MCP Inspector**:
   ```bash
   mcp-inspector http://localhost:8000
   ```

   ![Example](assets/mcp-inspector.png)

3. **Test the server**:
   - MCP Inspector will open in your browser
   - You can browse available tools
   - Test tool calls and verify responses

## Using with Agents

For a higher-level conversational interface, consider using the [IBM Storage Scale Agents](https://github.com/IBM/ibm-storage-scale-agents) which are built on top of this MCP server. The agents provide an intuitive way to manage IBM Storage Scale operations through natural language interactions.

## Development

Install the project with its dev dependency group and run the checks that CI
enforces (lint, format, tests, and a dependency vulnerability audit):

```bash
uv sync --all-groups
uv run ruff check src tests scripts
uv run ruff format --check src tests scripts
uv run pytest
uv run pip-audit
```

### Git hooks

Pre-commit hooks run ruff (lint + format) on staged Python and the full test
suite on push, using the same pinned tool versions as CI. Enable them once
after cloning:

```bash
uv run pre-commit install --hook-type pre-commit --hook-type pre-push
```

### Adding or changing endpoints

The tests need no cluster and no config file: every REST wrapper is exercised
against a mocked cluster and asserted to produce the documented HTTP method
and path (see `tests/contracts.py`). If you add or change an endpoint, update
the contract table in the same change and verify it against the
[IBM Storage Scale native REST API reference](https://www.ibm.com/docs/en/storage-scale/6.0.1?topic=reference-storage-scale-native-rest-api-endpoints),
and keep the README tool list in sync.

## Reporting Issues and Feedback

For issues, questions, or feature requests, please open an issue in the repository.

## Contributing Code

Contributions are welcome via Pull Requests. Please submit your very first Pull Request against the Developer's Certificate of Origin (DCO) located at [DCO.md](DCO.md) using your name and email address.

1. **Fork the repository** and create a new branch for your feature or bug fix
2. **Make your changes** following the existing code style and conventions
3. **Test your changes** thoroughly to ensure they work as expected
4. **Submit a pull request** with a clear description of your changes
5. **Sign the DCO** by adding your name and email address to the DCO.md file in your pull request

## Disclaimer

This software is provided "as is" without any warranties of any kind, including, but not limited to their installation, use, or performance. We are not responsible for any damage or charges or data loss incurred with their use. You are responsible for reviewing and testing any scripts you run thoroughly before use in any production environment. This content is subject to change without notice.
