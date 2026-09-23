# Provisioning and bootstrap

## Reconcile before creating

Inventory the selected project's resources and the project's recorded IDs. Reuse a matching resource only after checking its owner/environment and relevant configuration. A name collision or a timeout is not evidence that a resource is absent. Record newly returned IDs immediately so a partial run can resume without recreating what succeeded. Labels aid discovery; they do not alone authorize deleting or adopting a resource.

Resolve size, architecture, location, OS image, connectivity, and storage from the workload. Query the current catalog and `server-type describe` or structured pricing for the selected location. Account for public IPs, disks, backups, snapshots, and load balancers when used. Scaling CPU or disk, rebuilding a server, and restoring an image have different reversibility; check the current tool's help before choosing one.

Keep infrastructure and bootstrap files in the project's existing layout. Where none exists, create only the files the task needs and document their purpose. Use a durable deployment note for target context, resource IDs, completed stages, and remaining actions. Keep secret values out of the note and bootstrap payload.

## Create in dependency order

Prepare and validate the actual cloud-init configuration, firewall rules, and software installation sources before creating a billed server. Use a supported system image with compatible architecture. Validate cloud-config with `cloud-init schema` when available; a YAML parse alone does not establish schema validity. If validation tooling is unavailable, report that limitation rather than claim validation passed.

Resolve the user's public SSH key, retaining its existing private-key mechanism. Create or reuse the necessary network/subnet and firewall, then attach them when creating the server. Limit SSH ingress to the established administrator access path, covering IPv6 as well as IPv4 where enabled; expose HTTP/HTTPS where the workload needs them. Keep databases private unless public access is explicitly part of the design. Published container ports may bypass host firewall rules, so verify the effective cloud and host rules together.

Use the installed command's help for positional arguments and flags. In particular, network, server, firewall, and DNS commands do not share a uniform `--resource` naming convention. Send bootstrap through the documented user-data input and capture structured create output. Wait for the specific API action where available and inspect its result; a successful request submission is not completed configuration.

For an existing disk, establish its filesystem, mount, contents, and intended ownership before attachment or resizing. Formatting requires explicit authorization for that disk's data loss. For a private load-balancer target, select private addressing explicitly and verify target health and reachability.

## Establish trusted access

Bind SSH access to the verified server identity. Reuse an already trusted known_hosts entry for that same server. For a new or replaced server, obtain its host-key fingerprint through a trusted channel, such as running `ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub` in that server's console, then compare the presented key. `ssh-keyscan` collects keys but does not authenticate them. An IP reused after deletion is a reason to verify the new key before replacing its old known_hosts entry; it is not a reason to disable host-key checking. If no trusted verification path is available, resolve that access requirement before connecting.

Wait with a deadline for SSH, then run `cloud-init status --wait` remotely and inspect its exit status and reported errors. Bound that remote command using the host's available timeout facility. A running VM or an open SSH port can precede completed cloud-init. Verify installed packages and services actually needed by the workload before reporting bootstrap complete.

Before changing SSH users, ports, authentication, or firewall rules, verify the replacement access path, validate the SSH configuration, and retain an existing working session or console recovery path. Close the old path only after a separate connection succeeds with the intended user and key.

## Existing servers

Inspect the OS, running services, ports, mounts, and configuration ownership before installing or upgrading software. Avoid rerunning first-boot scripts to update a live host. Use the project's Ansible roles where present; otherwise make small state-aware changes with validation before reload. Check whether a restart or reboot affects a running workload and retain the established maintenance scope.

## Sources

- [hcloud tutorials and command reference](https://github.com/hetznercloud/cli/tree/main/docs)
- [Hetzner server and cloud-init FAQ](https://docs.hetzner.com/cloud/servers/faq/)
- [cloud-init schema and status commands](https://docs.cloud-init.io/en/latest/reference/cli.html)
- [Waiting for cloud-init](https://docs.cloud-init.io/en/latest/howto/wait_for_cloud_init.html)
