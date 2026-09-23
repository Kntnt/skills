# Software and application deployment

## Establish the project's deployment contract

Resolve the source revision or immutable artifact, runtime and architecture, build/start commands, secret sources, service user, persistent paths, database changes, domain, health checks, and release/restore procedure. Read existing deployment files first. Settle missing decisions that affect the result while preparing independent files and checks.

Keep reusable server procedures in this Skill and application-specific commands in the project. For a new deployment, create the necessary project-owned service/proxy configuration and installation/deploy routine, with recorded versions and validation commands. Choose system services, containers, Ansible, or an existing platform according to the project; Hetzner alone implies none of these choices. An installed Coolify or Dokploy instance remains the owner of the workloads it manages.

## Install and stage

Use supported package sources for the selected OS/runtime. Inspect external installation scripts and resolve their version before execution; validate a downloaded release against its publisher's checksum/signature when supplied. Establish existing installation state before running an installer on a host with services or persistent data.

Stage the selected release and validate its configuration before changing the live service. Keep writable data outside replaceable release directories. Supply secrets through the established secret mechanism with restrictive access, avoiding transcript output and committed `.env` files. Run the service with the intended non-root identity and only the permissions it needs. That identity is the service's own; the agent's is `kntnt-agent`, and host operations run as it through `sudo`, as root only where the instruction says so, as [access.md](access.md) states.

For updates, retain the currently deployed artifact and effective configuration until the new release is verified. Identify whether schema migrations remain compatible with the previous release. A code rollback cannot undo a destructive migration; establish a consistent backup and a recovery or forward-fix decision before executing such a migration. Read [recovery.md](recovery.md) before a deployment that depends on rollback or restore.

## Domain and HTTPS

Inspect the current authoritative DNS provider and records. Change records there; creating a Hetzner zone does not delegate a registered domain. Preserve unrelated records and coordinate TTL/cutover with the current service. Configure AAAA only when the intended IPv6 path actually serves the application; a stale AAAA can break a working IPv4 deployment.

Validate the chosen proxy/webserver configuration before reloading. Obtain and renew TLS through the project's existing certificate mechanism or an appropriate ACME-capable service. Confirm the domain, challenge reachability, certificate names, and renewal mechanism. Keep HTTP reachable when the chosen challenge method needs it. A provider-managed load-balancer certificate is not a certificate installed on an arbitrary origin server.

## Activate and verify

Activate the staged release using the project's service manager or deployment platform. Track its actual service state or specific deployment job through completion with a deadline. On uncertain results, read the state and logs before another deploy or restart. Bound logs and filter secrets before returning output.

Verify the expected application response locally and through the intended public hostname with certificate validation enabled. Check the expected status/content or application health endpoint, not merely TCP reachability. Cover both published address families and any proxy/load-balancer path. For a stateful application, verify required dependencies or a safe application-level read as appropriate.

Report success only when the requested service and endpoint checks pass. A DNS propagation delay, failed certificate issuance, or unhealthy dependency remains unfinished work even if deployment exited zero. Apply the established recovery procedure when a cutover fails; keep the previous release and evidence until the outcome is resolved.

Record the deployed revision/artifact, changed configuration, verification commands/results, and next update/rollback procedure in the project's deployment documentation. Distinguish a backup configured from one completed and a restore procedure written from one tested.
