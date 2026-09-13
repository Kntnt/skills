---
name: hetzner
description: Provision and operate Hetzner Cloud servers and deploy or maintain their websites and applications through hcloud, SSH, and cloud-init. Use for Hetzner Cloud infrastructure or workloads hosted there; excludes Robot dedicated servers and Object Storage.
disable-model-invocation: false
argument-hint: '[<instruction>] [-- <instruction>]'
compatibility: Requires uv and the Kntnt Manager. Remote operations need hcloud, OpenSSH, network access, and credentials; deployment-file preparation works without those remote prerequisites.
metadata:
  kntnt.internal: "true"
  kntnt.binaries: "uv"
  kntnt.skills: ""
  kntnt.externals: ""
  kntnt.capabilities: ""
---

# hetzner

Run `uv run "$HERE/scripts/invoke.py"` — `$HERE` is the directory that holds this SKILL.md — with everything the user typed after the Skill name, verbatim and however many lines, on stdin. Exit 0: do what it prints. Any other exit: show what it printed to the user verbatim, and stop.

## Arguments

`operands` and `instruction` carry one instruction between them. With neither, use the task established in the conversation; if there is none, ask what the user wants to do on Hetzner.

## Establish the operation

1. Read the project's deployment documentation and existing infrastructure, configuration, and release files. Resolve the target Hetzner project/context, environment, resource identity, requested outcome, and existing authorization. Where several targets remain plausible, settle the target before any remote operation. Preparation or inspection alone authorizes no deployment.
2. Keep the project's chosen stack and source of truth. Manage resources already owned by Terraform or Ansible through that project's workflow; reconcile emergency changes back into it. For a new small setup, use hcloud for Cloud resources, cloud-init for bootstrap, and SSH for installation and deployment. Add a platform or configuration tool only when the task calls for it.
3. For Cloud access, check `hcloud version` and the relevant command's `--help`; use the [official CLI documentation](https://github.com/hetznercloud/cli/tree/main/docs) for missing details or installation. Check hcloud and SSH only when that operation needs them; local preparation can continue without remote tools or credentials. Resolve credentials through an existing named context or a securely supplied environment token. For a named context, prevent an ambient token from overriding it: use `env -u HCLOUD_TOKEN hcloud --context "$HCLOUD_CONTEXT" location list` to verify access and retain that environment/context selection on subsequent commands. In token-only mode, establish which project owns the credential and retain the same source. Verify resource ownership before mutation; a public catalog read establishes connectivity, not the intended project's identity.
4. Inspect current state, then perform only the requested operation using the relevant reference below. An uncertain write result requires reconciliation before another write. Finish with the actual verification result, including any unfinished work.

## Read for the current task

- Creating servers or changing networks, firewalls, disks, or bootstrap configuration: [provisioning.md](references/provisioning.md).
- Installing software, deploying or updating an app, or configuring its domain and HTTPS: [deployment.md](references/deployment.md).
- Failed or interrupted operations, rollback, backup restoration, or resource deletion: [recovery.md](references/recovery.md).

Read each applicable reference before its operation; a complete new deployment needs both provisioning and deployment. A bounded inspection needs only the relevant tool help and existing project documentation.

## Execution boundaries

Honor authorization already given for the target, cost, and action; avoid asking again merely because a command writes. Before a billed or destructive action whose scope is unsettled, prepare a concrete plan with the affected resources, current cost or data-loss consequence, and recovery path, then obtain the missing decision. Permission to deploy does not imply permission to rebuild an existing server, format a disk, or delete persistent data.

Discover available server types, images, locations, and prices at execution time. Obtain prices for the selected location and currency, including separately billed resources; the default `server-type list` table is not a price quote. Keep credentials in their existing secret mechanism, outside chat, committed files, and rendered command output. Filter structured reads locally to the fields needed; JSON, debug logs, user-data, and application logs can contain secrets.

Use bounded waits with a deadline and preserve command failures, including pipeline failures. After a timeout, inspect the resource or operation before retrying a create, deploy, migration, or other write. Stop dependent mutations when the outcome remains unknown. Report partially created resources and their costs; remove them only within established cleanup authorization.

## Delivery

Report the resolved target, resources changed or reused, release identity where applicable, checks actually completed, endpoint and cost where relevant, and any unresolved operation or recovery step. Distinguish prepared files, a running VM, completed cloud-init, a started service, and a healthy public application. For ongoing management, record non-secret resource IDs, configuration/release locations, verification commands, and recovery instructions in the project's existing deployment documentation; these belong to the project, not this Skill.
