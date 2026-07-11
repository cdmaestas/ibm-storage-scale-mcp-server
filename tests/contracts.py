"""Endpoint contract table: every REST API wrapper and the request it must produce.

Generated from the api modules after they were verified 1:1 against the IBM
Storage Scale 6.0.1 native REST API documentation (144 v3 endpoints; the four
v2 entries are GUI REST API health endpoints). If a function changes the
method or path it sends, the corresponding contract here must be updated
deliberately - alongside a check against the official endpoint reference:
https://www.ibm.com/docs/en/storage-scale/6.0.1?topic=reference-storage-scale-native-rest-api-endpoints
"""

from typing import NamedTuple


class C(NamedTuple):
    module: str  # dotted path under scale_mcp_server.api
    func: str  # api function name
    kwargs: dict  # minimal required arguments
    method: str  # expected HTTP method
    path: str  # expected URL path template ({placeholders} filled from kwargs)


CONTRACTS = [
    # --- v2/filesystems ---
    C("v2.filesystems", "get_filesystem_health_states_api", {'filesystem': 'test-filesystem'}, "GET", "/scalemgmt/v2/cluster/filesystems/{filesystem}/health/state"),
    C("v2.filesystems", "get_filesystem_health_events_api", {'filesystem_name': 'test-filesystem-name'}, "GET", "/scalemgmt/v2/cluster/filesystems/{filesystem_name}/health/events"),
    # --- v2/nodes ---
    C("v2.nodes", "get_node_health_states_api", {'name': 'test-name'}, "GET", "/scalemgmt/v2/nodes/{name}/health/states"),
    C("v2.nodes", "get_node_health_events_api", {'name': 'test-name'}, "GET", "/scalemgmt/v2/nodes/{name}/health/events"),
    # --- v3/afm ---
    C("v3.afm", "list_afm_states_api", {'filesystem': 'test-filesystem'}, "GET", "/scalemgmt/v3/filesystems/{filesystem}/filesets/afm/state"),
    C("v3.afm", "get_afm_state_api", {'filesystem': 'test-filesystem', 'fileset': 'test-fileset'}, "GET", "/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/afm/state"),
    C("v3.afm", "check_afm_dirty_api", {'filesystem': 'test-filesystem', 'fileset': 'test-fileset'}, "GET", "/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/afm/checkdirty"),
    C("v3.afm", "check_afm_uncached_api", {'filesystem': 'test-filesystem', 'fileset': 'test-fileset'}, "GET", "/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/afm/checkuncached"),
    C("v3.afm", "flush_afm_queue_api", {'filesystem': 'test-filesystem', 'fileset': 'test-fileset'}, "POST", "/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/afm/flushqueue"),
    C("v3.afm", "resume_afm_requeued_api", {'filesystem': 'test-filesystem', 'fileset': 'test-fileset'}, "POST", "/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/afm/resumerequeued"),
    C("v3.afm", "resync_afm_fileset_api", {'filesystem': 'test-filesystem', 'fileset': 'test-fileset'}, "POST", "/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/afm/resync"),
    C("v3.afm", "start_afm_fileset_api", {'filesystem': 'test-filesystem', 'fileset': 'test-fileset'}, "POST", "/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/afm:start"),
    C("v3.afm", "stop_afm_fileset_api", {'filesystem': 'test-filesystem', 'fileset': 'test-fileset'}, "POST", "/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/afm:stop"),
    C("v3.afm", "reset_afm_local_api", {'filesystem': 'test-filesystem', 'fileset': 'test-fileset', 'file_path': 'test-file-path'}, "PATCH", "/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/afm:resetlocal"),
    C("v3.afm", "set_afm_local_api", {'filesystem': 'test-filesystem', 'fileset': 'test-fileset', 'file_path': 'test-file-path'}, "PATCH", "/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/afm:setlocal"),
    # --- v3/afmcos ---
    C("v3.afmcos", "get_cos_keys_api", {'bucket_name': 'test-bucket-name'}, "GET", "/scalemgmt/v3/buckets/{bucket_name}/afmcos/getcoskeys"),
    C("v3.afmcos", "set_cos_keys_api", {'bucket_name': 'test-bucket-name', 'bucket_coskeys': {'key': 'value'}}, "PUT", "/scalemgmt/v3/buckets/{bucket_name}/afmcos/setcoskeys"),
    C("v3.afmcos", "delete_cos_keys_api", {'bucket_name': 'test-bucket-name'}, "DELETE", "/scalemgmt/v3/buckets/{bucket_name}/afmcos/delcoskeys"),
    C("v3.afmcos", "configure_afmcos_api", {'filesystem': 'test-filesystem', 'fileset': 'test-fileset', 'fileset_config': {'key': 'value'}}, "PUT", "/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/afmcos/configure"),
    C("v3.afmcos", "delete_afmcos_objects_api", {'filesystem': 'test-filesystem', 'fileset': 'test-fileset', 'delete_objects': {'key': 'value'}}, "POST", "/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/afmcos/delete"),
    C("v3.afmcos", "download_afmcos_objects_api", {'filesystem': 'test-filesystem', 'fileset': 'test-fileset', 'download_objects': {'key': 'value'}}, "POST", "/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/afmcos/download"),
    C("v3.afmcos", "evict_afmcos_objects_api", {'filesystem': 'test-filesystem', 'fileset': 'test-fileset', 'evict_objects': {'key': 'value'}}, "POST", "/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/afmcos/evict"),
    C("v3.afmcos", "reconcile_afmcos_api", {'filesystem': 'test-filesystem', 'fileset': 'test-fileset', 'reconcile_objects': {'key': 'value'}}, "POST", "/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/afmcos/reconcile"),
    C("v3.afmcos", "upload_afmcos_objects_api", {'filesystem': 'test-filesystem', 'fileset': 'test-fileset', 'upload_objects': {'key': 'value'}}, "PUT", "/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/afmcos/upload"),
    # --- v3/api_health ---
    C("v3.api_health", "get_api_health_api", {}, "GET", "/scalemgmt/v3/apihealth"),
    C("v3.api_health", "get_node_api_health_api", {'node_name': 'test-node-name'}, "GET", "/scalemgmt/v3/apihealth/{node_name}"),
    # --- v3/authorization ---
    C("v3.authorization", "can_i_api", {'action': 'test-action', 'resource': 'test-resource'}, "POST", "/scalemgmt/v3/authorization/cani"),
    C("v3.authorization", "can_i_impersonate_api", {'action': 'test-action', 'resource': 'test-resource', 'user': 'test-user'}, "POST", "/scalemgmt/v3/authorization/cani:impersonate"),
    C("v3.authorization", "list_rbac_domains_api", {}, "GET", "/scalemgmt/v3/authorization/domains"),
    C("v3.authorization", "create_rbac_domain_api", {'domain_data': {'key': 'value'}}, "POST", "/scalemgmt/v3/authorization/domains"),
    C("v3.authorization", "get_rbac_domain_api", {'name': 'test-name'}, "GET", "/scalemgmt/v3/authorization/domains/{name}"),
    C("v3.authorization", "update_rbac_domain_api", {'name': 'test-name', 'domain_data': {'key': 'value'}}, "PATCH", "/scalemgmt/v3/authorization/domains/{name}"),
    C("v3.authorization", "delete_rbac_domain_api", {'name': 'test-name'}, "DELETE", "/scalemgmt/v3/authorization/domains/{name}"),
    C("v3.authorization", "get_rbac_module_api", {}, "GET", "/scalemgmt/v3/authorization/module"),
    C("v3.authorization", "update_rbac_module_api", {'module_data': {'key': 'value'}}, "PATCH", "/scalemgmt/v3/authorization/module"),
    # --- v3/clusters ---
    C("v3.clusters", "list_clusters_api", {}, "GET", "/scalemgmt/v3/clusters"),
    C("v3.clusters", "create_cluster_api", {'cluster_data': {'key': 'value'}}, "POST", "/scalemgmt/v3/clusters"),
    C("v3.clusters", "migrate_cluster_api", {}, "POST", "/scalemgmt/v3/clusters:migrate"),
    C("v3.clusters", "list_cluster_trust_api", {}, "GET", "/scalemgmt/v3/clusters/trust"),
    # --- v3/config ---
    C("v3.config", "get_admin_config_api", {}, "GET", "/scalemgmt/v3/config/admin"),
    C("v3.config", "get_admin_config_attribute_api", {'name': 'test-name'}, "GET", "/scalemgmt/v3/config/admin/{name}"),
    C("v3.config", "update_admin_config_api", {'config_data': {'key': 'value'}}, "PATCH", "/scalemgmt/v3/config/admin:batchUpdate"),
    C("v3.config", "get_cluster_config_api", {}, "GET", "/scalemgmt/v3/config/cluster"),
    C("v3.config", "get_cluster_config_attribute_api", {'name': 'test-name'}, "GET", "/scalemgmt/v3/config/cluster/{name}"),
    C("v3.config", "update_cluster_config_api", {'config_data': {'key': 'value'}}, "PATCH", "/scalemgmt/v3/config/cluster:batchUpdate"),
    # --- v3/diagnostics ---
    C("v3.diagnostics", "get_node_version_api", {'node': 'test-node'}, "GET", "/scalemgmt/v3/nodes/{node}/diagnostics/version"),
    # --- v3/filesets ---
    C("v3.filesets", "list_filesets_api", {'filesystem': 'test-filesystem'}, "GET", "/scalemgmt/v3/filesystems/{filesystem}/filesets"),
    C("v3.filesets", "create_fileset_api", {'filesystem': 'test-filesystem', 'fileset_data': {'key': 'value'}}, "POST", "/scalemgmt/v3/filesystems/{filesystem}/filesets"),
    C("v3.filesets", "get_fileset_api", {'filesystem': 'test-filesystem', 'fileset_name': 'test-fileset-name'}, "GET", "/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset_name}"),
    C("v3.filesets", "delete_fileset_api", {'filesystem': 'test-filesystem', 'fileset_name': 'test-fileset-name'}, "DELETE", "/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset_name}"),
    C("v3.filesets", "update_fileset_api", {'filesystem': 'test-filesystem', 'fileset_name': 'test-fileset-name', 'fileset_data': {'key': 'value'}}, "PATCH", "/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset_name}"),
    C("v3.filesets", "get_fileset_usage_api", {'filesystem': 'test-filesystem', 'fileset_name': 'test-fileset-name'}, "GET", "/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset_name}/usage"),
    C("v3.filesets", "link_fileset_api", {'filesystem': 'test-filesystem', 'fileset_name': 'test-fileset-name', 'link_data': {'key': 'value'}}, "POST", "/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset_name}:link"),
    C("v3.filesets", "unlink_fileset_api", {'filesystem': 'test-filesystem', 'fileset_name': 'test-fileset-name'}, "POST", "/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset_name}:unlink"),
    C("v3.filesets", "list_fileset_snapshots_api", {'filesystem': 'test-filesystem', 'fileset': 'test-fileset'}, "GET", "/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/snapshots"),
    C("v3.filesets", "create_fileset_snapshot_api", {'filesystem': 'test-filesystem', 'fileset': 'test-fileset', 'snapshot_data': {'key': 'value'}}, "POST", "/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/snapshots"),
    C("v3.filesets", "get_fileset_snapshot_api", {'filesystem': 'test-filesystem', 'fileset': 'test-fileset', 'snapshot_name': 'test-snapshot-name'}, "GET", "/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/snapshots/{snapshot_name}"),
    C("v3.filesets", "delete_fileset_snapshot_api", {'filesystem': 'test-filesystem', 'fileset': 'test-fileset', 'snapshot_name': 'test-snapshot-name'}, "DELETE", "/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/snapshots/{snapshot_name}"),
    C("v3.filesets", "batch_create_fileset_snapshots_api", {'filesystem': 'test-filesystem', 'snapshot_data': {'key': 'value'}}, "POST", "/scalemgmt/v3/filesystems/{filesystem}/filesets/snapshots:batchCreate"),
    C("v3.filesets", "batch_delete_fileset_snapshots_api", {'filesystem': 'test-filesystem', 'snapshot_data': {'key': 'value'}}, "POST", "/scalemgmt/v3/filesystems/{filesystem}/filesets/snapshots:batchDelete"),
    # --- v3/filesystem_disks ---
    C("v3.filesystem_disks", "list_filesystem_disks_api", {'filesystem': 'test-filesystem'}, "GET", "/scalemgmt/v3/filesystems/{filesystem}/disks"),
    C("v3.filesystem_disks", "get_filesystem_disk_api", {'filesystem': 'test-filesystem', 'disk_name': 'test-disk-name'}, "GET", "/scalemgmt/v3/filesystems/{filesystem}/disks/{disk_name}"),
    C("v3.filesystem_disks", "add_filesystem_disk_api", {'filesystem': 'test-filesystem'}, "POST", "/scalemgmt/v3/filesystems/{filesystem}/disks"),
    C("v3.filesystem_disks", "delete_filesystem_disk_api", {'filesystem': 'test-filesystem', 'disk_name': 'test-disk-name', 'continue_on_error': True}, "DELETE", "/scalemgmt/v3/filesystems/{filesystem}/disks/{disk_name}"),
    C("v3.filesystem_disks", "batch_add_filesystem_disks_api", {'filesystem': 'test-filesystem', 'disks_data': {'key': 'value'}}, "POST", "/scalemgmt/v3/filesystems/{filesystem}/disks:batchAdd"),
    C("v3.filesystem_disks", "batch_delete_filesystem_disks_api", {'filesystem': 'test-filesystem'}, "POST", "/scalemgmt/v3/filesystems/{filesystem}/disks:batchDelete"),
    C("v3.filesystem_disks", "get_disks_quorum_api", {'filesystem': 'test-filesystem'}, "GET", "/scalemgmt/v3/filesystems/{filesystem}/disksquorum"),
    # --- v3/filesystems ---
    C("v3.filesystems", "list_filesystems_api", {}, "GET", "/scalemgmt/v3/filesystems"),
    C("v3.filesystems", "get_filesystem_api", {'filesystem': 'test-filesystem'}, "GET", "/scalemgmt/v3/filesystems/{filesystem}"),
    C("v3.filesystems", "create_filesystem_api", {'filesystem_data': {'key': 'value'}}, "POST", "/scalemgmt/v3/filesystems"),
    C("v3.filesystems", "update_filesystem_api", {'filesystem': 'test-filesystem', 'filesystem_data': {'key': 'value'}}, "PATCH", "/scalemgmt/v3/filesystems/{filesystem}"),
    C("v3.filesystems", "delete_filesystem_api", {'name': 'test-name'}, "DELETE", "/scalemgmt/v3/filesystems/{name}"),
    C("v3.filesystems", "get_mount_status_api", {'filesystem': 'test-filesystem'}, "GET", "/scalemgmt/v3/filesystems/{filesystem}:mount"),
    C("v3.filesystems", "mount_filesystem_api", {'name': 'test-name'}, "POST", "/scalemgmt/v3/filesystems/{name}:mount"),
    C("v3.filesystems", "unmount_filesystem_api", {'name': 'test-name'}, "POST", "/scalemgmt/v3/filesystems/{name}:unmount"),
    C("v3.filesystems", "mount_all_filesystems_api", {}, "POST", "/scalemgmt/v3/filesystems:mount"),
    C("v3.filesystems", "unmount_all_filesystems_api", {}, "POST", "/scalemgmt/v3/filesystems:unmount"),
    C("v3.filesystems", "rebalance_filesystem_api", {'filesystem': 'test-filesystem'}, "POST", "/scalemgmt/v3/filesystems/{filesystem}:rebalance"),
    C("v3.filesystems", "restripe_filesystem_api", {'filesystem': 'test-filesystem'}, "POST", "/scalemgmt/v3/filesystems/{filesystem}:restripe"),
    C("v3.filesystems", "list_directory_api", {'filesystem': 'test-filesystem', 'dirpath': 'test-dirpath'}, "GET", "/scalemgmt/v3/filesystems/{filesystem}/directory/{dirpath}"),
    C("v3.filesystems", "stat_directory_api", {'filesystem': 'test-filesystem', 'dirpath': 'test-dirpath'}, "GET", "/scalemgmt/v3/filesystems/{filesystem}/directory/{dirpath}:stat"),
    C("v3.filesystems", "create_directory_api", {'filesystem': 'test-filesystem', 'dirpath': 'test-dirpath'}, "POST", "/scalemgmt/v3/filesystems/{filesystem}/directory/{dirpath}"),
    C("v3.filesystems", "delete_directory_api", {'filesystem': 'test-filesystem', 'dirpath': 'test-dirpath'}, "DELETE", "/scalemgmt/v3/filesystems/{filesystem}/directory/{dirpath}"),
    # --- v3/managers ---
    C("v3.managers", "set_cluster_manager_api", {'manager_data': {'key': 'value'}}, "POST", "/scalemgmt/v3/clusters/manager"),
    C("v3.managers", "set_filesystem_manager_api", {'filesystem': 'test-filesystem', 'manager_data': {'key': 'value'}}, "POST", "/scalemgmt/v3/filesystems/{filesystem}/manager"),
    # --- v3/node_classes ---
    C("v3.node_classes", "list_node_classes_api", {}, "GET", "/scalemgmt/v3/nodeclasses"),
    C("v3.node_classes", "get_node_class_api", {'node_class': 'test-node-class'}, "GET", "/scalemgmt/v3/nodeclasses/{node_class}"),
    C("v3.node_classes", "create_node_class_api", {'nodeclass_data': {'key': 'value'}}, "POST", "/scalemgmt/v3/nodeclasses"),
    C("v3.node_classes", "update_node_class_api", {'node_class': 'test-node-class', 'nodeclass_data': {'key': 'value'}}, "PATCH", "/scalemgmt/v3/nodeclasses/{node_class}"),
    C("v3.node_classes", "delete_node_class_api", {'node_class': 'test-node-class'}, "DELETE", "/scalemgmt/v3/nodeclasses/{node_class}"),
    # --- v3/nodes ---
    C("v3.nodes", "add_node_api", {'node_data': {'key': 'value'}}, "POST", "/scalemgmt/v3/nodes"),
    C("v3.nodes", "batch_add_nodes_api", {'nodes_data': {'key': 'value'}}, "POST", "/scalemgmt/v3/nodes:batchAdd"),
    C("v3.nodes", "start_nodes_api", {}, "POST", "/scalemgmt/v3/nodes:start"),
    C("v3.nodes", "stop_nodes_api", {}, "POST", "/scalemgmt/v3/nodes:stop"),
    C("v3.nodes", "get_nodes_status_api", {}, "GET", "/scalemgmt/v3/nodes/status"),
    C("v3.nodes", "get_nodes_config_api", {}, "GET", "/scalemgmt/v3/nodes/config"),
    # --- v3/nsds ---
    C("v3.nsds", "list_nsds_api", {}, "GET", "/scalemgmt/v3/nsds"),
    C("v3.nsds", "get_nsd_api", {'nsd_name': 'test-nsd-name'}, "GET", "/scalemgmt/v3/nsds/{nsd_name}"),
    C("v3.nsds", "create_nsd_api", {'nsd_data': {'key': 'value'}}, "POST", "/scalemgmt/v3/nsds"),
    C("v3.nsds", "update_nsd_api", {'nsd_name': 'test-nsd-name', 'nsd_data': {'key': 'value'}}, "PATCH", "/scalemgmt/v3/nsds/{nsd_name}"),
    C("v3.nsds", "delete_nsd_api", {'nsd_name': 'test-nsd-name'}, "DELETE", "/scalemgmt/v3/nsds/{nsd_name}"),
    C("v3.nsds", "batch_create_nsds_api", {'nsds_data': {'key': 'value'}}, "POST", "/scalemgmt/v3/nsds:batchCreate"),
    C("v3.nsds", "batch_delete_nsds_api", {'nsds_data': {'key': 'value'}}, "POST", "/scalemgmt/v3/nsds:batchDelete"),
    # --- v3/operations ---
    C("v3.operations", "list_operations_api", {}, "GET", "/scalemgmt/v3/operations"),
    C("v3.operations", "get_operation_api", {'operation_id': 'test-operation-id'}, "GET", "/scalemgmt/v3/operations/{operation_id}"),
    C("v3.operations", "get_operation_output_api", {'operation_id': 'test-operation-id'}, "GET", "/scalemgmt/v3/operations/{operation_id}/output"),
    C("v3.operations", "cancel_operation_api", {'operation_id': 'test-operation-id'}, "POST", "/scalemgmt/v3/operations/{operation_id}:cancel"),
    C("v3.operations", "delete_operation_api", {'operation_id': 'test-operation-id'}, "DELETE", "/scalemgmt/v3/operations/{operation_id}"),
    # --- v3/policies ---
    C("v3.policies", "get_policy_api", {'filesystem': 'test-filesystem'}, "GET", "/scalemgmt/v3/filesystems/{filesystem}/policy"),
    C("v3.policies", "update_policy_api", {'filesystem': 'test-filesystem', 'policy': {'key': 'value'}}, "PATCH", "/scalemgmt/v3/filesystems/{filesystem}/policy"),
    # --- v3/quotas ---
    C("v3.quotas", "list_quotas_api", {'filesystem': 'test-filesystem'}, "GET", "/scalemgmt/v3/filesystems/{filesystem}/quotas"),
    C("v3.quotas", "set_quota_api", {'filesystem': 'test-filesystem', 'quota_data': {'key': 'value'}}, "PUT", "/scalemgmt/v3/filesystems/{filesystem}/quotas"),
    C("v3.quotas", "check_quotas_api", {'filesystem': 'test-filesystem'}, "POST", "/scalemgmt/v3/filesystems/{filesystem}/quotas"),
    C("v3.quotas", "update_quota_config_api", {'filesystem': 'test-filesystem', 'config_data': {'key': 'value'}}, "POST", "/scalemgmt/v3/filesystems/{filesystem}/quotas/config"),
    C("v3.quotas", "list_fileset_quotas_api", {'filesystem': 'test-filesystem', 'fileset': 'test-fileset'}, "GET", "/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/quotas"),
    C("v3.quotas", "set_fileset_quota_api", {'filesystem': 'test-filesystem', 'fileset': 'test-fileset', 'quota_data': {'key': 'value'}}, "PUT", "/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/quotas"),
    C("v3.quotas", "check_fileset_quotas_api", {'filesystem': 'test-filesystem', 'fileset': 'test-fileset'}, "POST", "/scalemgmt/v3/filesystems/{filesystem}/filesets/{fileset}/quotas"),
    # --- v3/remote_clusters ---
    C("v3.remote_clusters", "list_remote_clusters_api", {}, "GET", "/scalemgmt/v3/clusters/remote"),
    C("v3.remote_clusters", "get_remote_cluster_api", {'name': 'test-name'}, "GET", "/scalemgmt/v3/clusters/remote/{name}"),
    C("v3.remote_clusters", "add_remote_cluster_api", {'remote_cluster': {'key': 'value'}}, "POST", "/scalemgmt/v3/clusters/remote"),
    C("v3.remote_clusters", "update_remote_cluster_api", {'name': 'test-name', 'remote_cluster': {'key': 'value'}}, "PATCH", "/scalemgmt/v3/clusters/remote/{name}"),
    C("v3.remote_clusters", "delete_remote_cluster_api", {'name': 'test-name'}, "DELETE", "/scalemgmt/v3/clusters/remote/{name}"),
    C("v3.remote_clusters", "authorize_remote_cluster_api", {'authorization': {'key': 'value'}}, "POST", "/scalemgmt/v3/clusters/remote/authorized"),
    C("v3.remote_clusters", "deauthorize_remote_cluster_api", {'name': 'test-name'}, "DELETE", "/scalemgmt/v3/clusters/remote/authorized/{name}"),
    C("v3.remote_clusters", "refresh_remote_cluster_api", {'name': 'test-name'}, "POST", "/scalemgmt/v3/clusters/remote/{name}/refresh"),
    # --- v3/remote_filesystems ---
    C("v3.remote_filesystems", "add_remote_filesystem_api", {'filesystem': {'key': 'value'}}, "POST", "/scalemgmt/v3/filesystems/remote"),
    C("v3.remote_filesystems", "update_remote_filesystem_api", {'filesystem': 'test-filesystem', 'filesystem_data': {'key': 'value'}}, "PATCH", "/scalemgmt/v3/filesystems/remote/{filesystem}"),
    C("v3.remote_filesystems", "delete_remote_filesystem_api", {'filesystem': 'test-filesystem'}, "DELETE", "/scalemgmt/v3/filesystems/remote/{filesystem}"),
    # --- v3/snapshots ---
    C("v3.snapshots", "list_snapshots_api", {'filesystem': 'test-filesystem'}, "GET", "/scalemgmt/v3/filesystems/{filesystem}/snapshots"),
    C("v3.snapshots", "create_snapshot_api", {'filesystem': 'test-filesystem', 'snapshot_data': {'key': 'value'}}, "POST", "/scalemgmt/v3/filesystems/{filesystem}/snapshots"),
    C("v3.snapshots", "get_snapshot_api", {'filesystem': 'test-filesystem', 'snapshot_name': 'test-snapshot-name'}, "GET", "/scalemgmt/v3/filesystems/{filesystem}/snapshots/{snapshot_name}"),
    C("v3.snapshots", "delete_snapshot_api", {'filesystem': 'test-filesystem', 'snapshot_name': 'test-snapshot-name'}, "DELETE", "/scalemgmt/v3/filesystems/{filesystem}/snapshots/{snapshot_name}"),
    C("v3.snapshots", "batch_delete_snapshots_api", {'filesystem': 'test-filesystem', 'snapshot_data': {'key': 'value'}}, "POST", "/scalemgmt/v3/filesystems/{filesystem}/snapshots:batchDelete"),
    C("v3.snapshots", "get_snapdir_settings_api", {'filesystem': 'test-filesystem'}, "GET", "/scalemgmt/v3/filesystems/{filesystem}/snapshots:snapdir"),
    # --- v3/storage_pools ---
    C("v3.storage_pools", "list_storage_pools_api", {'filesystem': 'test-filesystem'}, "GET", "/scalemgmt/v3/filesystems/{filesystem}/storagepools"),
    C("v3.storage_pools", "get_storage_pool_api", {'filesystem': 'test-filesystem', 'pool_name': 'test-pool-name'}, "GET", "/scalemgmt/v3/filesystems/{filesystem}/storagepools/{pool_name}"),
    C("v3.storage_pools", "update_storage_pool_api", {'filesystem': 'test-filesystem', 'pool_name': 'test-pool-name', 'pool_data': {'key': 'value'}}, "PATCH", "/scalemgmt/v3/filesystems/{filesystem}/storagepools/{pool_name}"),
    # --- v3/troubleshooting ---
    C("v3.troubleshooting", "clear_nsd_id_api", {'id': 'test-id'}, "DELETE", "/scalemgmt/v3/troubleshooting/nsds/clearID"),
    C("v3.troubleshooting", "get_persistent_reserve_keys_api", {'device': 'test-device'}, "GET", "/scalemgmt/v3/troubleshooting/persistentReserve/{device}/keys"),
    C("v3.troubleshooting", "clear_persistent_reserve_keys_api", {'device': 'test-device'}, "DELETE", "/scalemgmt/v3/troubleshooting/persistentReserve/{device}/keys"),
    # --- v3/version ---
    C("v3.version", "get_version_api", {}, "GET", "/scalemgmt/v3/version"),
    # --- v3/xcp ---
    C("v3.xcp", "list_xcp_operations_api", {}, "GET", "/scalemgmt/v3/xcp"),
    C("v3.xcp", "get_xcp_operation_api", {'id': 'test-id'}, "GET", "/scalemgmt/v3/xcp/{id}"),
    C("v3.xcp", "get_xcp_config_api", {}, "GET", "/scalemgmt/v3/xcp/config"),
    C("v3.xcp", "update_xcp_config_api", {'config_data': {'key': 'value'}}, "PATCH", "/scalemgmt/v3/xcp/config"),
    C("v3.xcp", "enable_xcp_copy_api", {'copy_data': {'key': 'value'}}, "PATCH", "/scalemgmt/v3/xcp:enable"),
    C("v3.xcp", "sync_xcp_api", {'sync_data': {'key': 'value'}}, "PATCH", "/scalemgmt/v3/xcp:sync"),
    C("v3.xcp", "verify_xcp_api", {'verify_data': {'key': 'value'}}, "PATCH", "/scalemgmt/v3/xcp:verify"),
]
