# Recovery and resource removal

## Interrupted or failed operations

Read the recorded context, resource IDs, last completed stage, and attempted operation. Query the actual resource/action/deployment state and inspect bounded logs. Resume from the first unmet condition once ownership and state are known; treat an HTTP timeout or lost SSH session as an unknown result, not proof the write failed. Avoid replaying a migration or first-boot script solely because its response was lost.

Preserve evidence needed for diagnosis, excluding secrets. Distinguish a harmless retriable read from a write that may already have taken effect. After a retry deadline or an unreconciled result, stop dependent changes and report the exact uncertain operation, resources still present, potential ongoing cost, and information needed to continue.

## Rollback and restore

For application rollback, restore the known previous artifact and configuration only if compatible with the current data/schema, then repeat service and public endpoint checks. Preserve the failed release's logs. Where rollback would lose data or violate migration compatibility, follow the agreed forward-fix or database restore plan rather than blindly redeploying old code.

For backup, identify every persistent component: database, uploads, attached volumes, and configuration/secret recovery mechanism. Establish consistency with the database's supported backup method or a planned quiescence window. Verify backup completion and integrity, preserve dump/pipeline failures, and record the recovery point and storage location. Hetzner server backups/snapshots do not include attached volumes; a snapshot is not by itself an application-consistent backup. Object Storage configuration is outside this Skill.

A restore test restores into an isolated destination, validates data and application behavior, and reports the measured result without replacing production. Creating a paid test server still needs authorization within the agreed cost/scope. A written restore procedure or a successful backup job is not a completed restore test. Before replacing production, settle acceptable data loss and downtime and retain the existing system until the replacement is verified where feasible.

## Deletion and cleanup

Identify exact resources by recorded ID in the resolved context and inspect their current attachments and ownership. Deleting a server, rebuilding from an image, formatting a disk, replacing a DNS zone, and removing a database volume are distinct destructive actions. Establish which is authorized and what data must survive; take any required backup before the destructive step.

Remove only resources whose ownership and deletion scope are established, accounting for dependency order and configured auto-delete behavior. Preserve shared networks, firewalls, DNS records, and keys still used elsewhere. An automatically allocated primary IP, detached volume, snapshot, or load balancer may remain billable after the server is gone; verify actual remaining resources rather than equating server deletion with zero cost.

Confirm deletion/termination through API state and report what remains, including retained billable resources. Preserve the resource record until reconciliation finishes. A failed listing is an error to resolve, never an empty inventory or a successful cleanup.

## Sources

- [Hetzner backups and snapshots FAQ](https://docs.hetzner.com/cloud/servers/backups-snapshots/faq/)
- [Hetzner Cloud API and resource actions](https://docs.hetzner.cloud/reference/cloud)
