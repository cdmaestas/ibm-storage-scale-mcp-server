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
   allow_insecure = true
   
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

The MCP server provides comprehensive IBM Storage Scale management capabilities through various tool categories:

### Core Management (v3 API)
- **API Health**: REST API service health monitoring
  - `get_api_health`: Check API service health and availability
  - `get_api_status`: Get detailed API status and version information
- **Authorization**: Authentication and session management
  - `login`: Authenticate and create a session
  - `logout`: Logout and invalidate session
  - `refresh_token`: Refresh authentication token
  - `get_session_info`: Get current session information
- **AFM (Active File Management)**: Manage AFM filesets for data replication
  - `list_afm_filesets`: List all AFM filesets
  - `get_afm_fileset`: Get AFM configuration for a fileset
  - `create_afm_fileset`: Create new AFM fileset
  - `update_afm_fileset`: Update AFM configuration
  - `delete_afm_fileset`: Delete AFM configuration
  - `prefetch_afm_fileset`: Prefetch data from source
  - `resync_afm_fileset`: Resynchronize with source
  - `get_afm_fileset_status`: Get AFM fileset status
- **AFMCOS (AFM to Cloud Object Storage)**: Manage AFM filesets for cloud storage
  - `list_afmcos_filesets`: List all AFMCOS filesets
  - `get_afmcos_fileset`: Get AFMCOS configuration
  - `create_afmcos_fileset`: Create AFMCOS fileset
  - `update_afmcos_fileset`: Update AFMCOS configuration
  - `delete_afmcos_fileset`: Delete AFMCOS configuration
  - `prefetch_afmcos_fileset`: Prefetch data from cloud
  - `evict_afmcos_fileset`: Evict cached data
  - `get_afmcos_fileset_status`: Get AFMCOS fileset status
- **Clusters**: Cluster configuration and management
- **Config**: System configuration operations
  - `list_config`: List all configuration parameters
  - `get_config_parameter`: Get specific configuration parameter
  - `update_config_parameter`: Update configuration parameter
- **Diagnostics**: System diagnostics and troubleshooting
  - `get_node_version`: Get node version information
  - `collect_diagnostics`: Collect diagnostic data
  - `get_diagnostics_status`: Get diagnostic collection status
- **Filesets**: Fileset creation, management, and operations
- **Filesystem Disks**: Disk management within filesystems
  - `list_filesystem_disks`: List all disks in a filesystem
  - `get_filesystem_disk`: Get disk details
  - `add_disks_to_filesystem`: Add disks to filesystem
  - `remove_disk_from_filesystem`: Remove disk from filesystem
  - `update_filesystem_disk`: Update disk configuration
- **Filesystems**: Filesystem operations (create, mount, unmount, list, etc.)
  - `list_filesystems`: List all filesystems
  - `get_filesystem`: Get filesystem details
  - `create_filesystem`: Create new filesystem
  - `update_filesystem`: Update filesystem configuration
  - `delete_filesystem`: Delete filesystem
  - `mount_filesystem`: Mount filesystem
  - `unmount_filesystem`: Unmount filesystem
  - `mount_all_filesystems`: Mount all filesystems
  - `unmount_all_filesystems`: Unmount all filesystems
- **Health**: Health monitoring and status checks
  - `get_filesystem_health`: Get filesystem health indicators
  - `get_node_health`: Get node health/status information
  - `get_node_diagnostics`: Get detailed node diagnostics
  - `get_cluster_health_summary`: Get comprehensive cluster health overview
- **Managers**: Manager node operations and configuration
  - `list_managers`: List all manager nodes
  - `get_manager`: Get manager node details
  - `add_manager`: Add new manager node
  - `remove_manager`: Remove manager node
  - `update_manager`: Update manager configuration
- **Node Classes**: Node classification and grouping
  - `list_node_classes`: List all node classes
  - `get_node_class`: Get node class details
  - `create_node_class`: Create new node class
  - `update_node_class`: Update node class
  - `delete_node_class`: Delete node class
  - `add_nodes_to_class`: Add nodes to class
  - `remove_nodes_from_class`: Remove nodes from class
- **Nodes**: Node management and operations
  - `list_nodes`: List all nodes
  - `get_node`: Get node details
  - `add_node`: Add new node
  - `update_node`: Update node configuration
  - `delete_node`: Remove node
  - `get_node_config`: Get node configuration
  - `get_node_status`: Get node status
  - `batch_add_nodes`: Add multiple nodes
  - `start_nodes`: Start specified nodes
  - `stop_nodes`: Stop specified nodes
- **NSDs**: Network Shared Disk management
- **Operations**: Long-running operation tracking and management
  - `list_operations`: List all operations with optional filtering
  - `get_operation`: Get operation details and status
  - `cancel_operation`: Cancel a running operation
  - `wait_for_operation`: Wait for operation completion
- **Policies**: Policy management and execution
  - `list_policies`: List all policies
  - `get_policy`: Get policy details
  - `create_policy`: Create new policy
  - `update_policy`: Update policy
  - `delete_policy`: Delete policy
  - `run_policy`: Execute policy
  - `list_policy_jobs`: List policy execution jobs
  - `get_policy_job`: Get policy job details
  - `cancel_policy_job`: Cancel running policy job
- **Quotas**: Quota management
  - `list_quotas`: List all quotas for filesystem
  - `get_quota`: Get specific quota details
  - `set_quota`: Set or update quota
  - `delete_quota`: Delete quota
  - `list_fileset_quotas`: List quotas for fileset
  - `get_fileset_quota`: Get fileset quota details
  - `set_fileset_quota`: Set fileset quota
  - `delete_fileset_quota`: Delete fileset quota
- **Remote Clusters**: Multi-cluster management and AFM operations
  - `list_remote_clusters`: List configured remote clusters
  - `get_remote_cluster`: Get remote cluster details
  - `add_remote_cluster`: Add remote cluster configuration
  - `update_remote_cluster`: Update remote cluster
  - `delete_remote_cluster`: Delete remote cluster
- **Remote Filesystems**: Manage filesystems on remote clusters
  - `list_remote_filesystems`: List filesystems on remote cluster
  - `get_remote_filesystem`: Get remote filesystem details
  - `mount_remote_filesystem`: Mount remote filesystem locally
  - `unmount_remote_filesystem`: Unmount remote filesystem
  - `get_remote_filesystem_status`: Get remote filesystem status
- **Snapshots**: Snapshot operations
- **Storage Pools**: Storage pool management
  - `list_storage_pools`: List storage pools
  - `get_storage_pool`: Get storage pool details
  - `create_storage_pool`: Create new storage pool
  - `update_storage_pool`: Update storage pool
  - `delete_storage_pool`: Delete storage pool
- **Troubleshooting**: Advanced diagnostics and problem resolution
  - `get_troubleshooting_info`: Get troubleshooting information
  - `collect_diagnostics`: Collect diagnostic data
  - `get_logs`: Retrieve system logs
  - `run_diagnostic_test`: Execute diagnostic tests
- **Version**: Version information
- **XCP (eXtreme Copy)**: Parallel file copy and synchronization operations
  - `list_xcp_operations`: List all XCP operations
  - `get_xcp_operation`: Get XCP operation details
  - `create_xcp_copy`: Create parallel copy operation
  - `create_xcp_sync`: Create parallel sync operation
  - `cancel_xcp_operation`: Cancel running XCP operation
  - `get_xcp_operation_status`: Get operation status
  - `get_xcp_operation_logs`: Get operation logs

### Legacy Tools (v2 API - Deprecated)
- **Filesystem Health (v2)**: Legacy filesystem health monitoring
  - ⚠️ DEPRECATED: Use `health_v3` tools instead
- **Node Health (v2)**: Legacy node health monitoring
  - ⚠️ DEPRECATED: Use `health_v3` tools instead

### CLI Tools
- **Policies (CLI)**: Direct CLI-based policy operations via SSH

### Migration from v2 to v3 Health Monitoring

The v2 health endpoints (`/scalemgmt/v2/*/health/*`) have been replaced with v3 alternatives:

| v2 Tool | v3 Replacement | Notes |
|---------|----------------|-------|
| `get_filesystem_health_states` | `get_filesystem_health` | Uses `/v3/filesystems/{name}` endpoint |
| `get_filesystem_health_events` | `get_filesystem_health` | Consolidated into single tool |
| `get_node_health_states` | `get_node_health` | Uses `/v3/nodes/status` endpoint |
| `get_node_health_events` | `get_node_health` | Consolidated into single tool |
| N/A | `get_node_diagnostics` | New: Uses `/v3/nodes/{node}/diagnostics/version` |
| N/A | `get_cluster_health_summary` | New: Comprehensive cluster overview |

**Why migrate?**
- v3 API is the current standard for IBM Storage Scale
- Better performance and reliability
- Consolidated health information in fewer API calls
- Active development and support

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
