# hetzner

## NAME

hetzner - provision Hetzner Cloud servers and operate their websites and applications

## SYNOPSIS

**/hetzner** [*INSTRUCTION*] [**--** *INSTRUCTION*]

## DESCRIPTION

`hetzner` prepares or executes the requested infrastructure, software installation, deployment, update, recovery, or cleanup operation on Hetzner Cloud. It reads the project's existing deployment files and resolves the target project and resources before acting. With no instruction it uses the established conversation task, or asks what operation is wanted when none exists.

For a small new setup it uses the official hcloud CLI, cloud-init, and SSH. Existing Terraform, Ansible, service-manager, or deployment-platform workflows remain the source of truth. App-specific configuration and release commands are written in the project; the Skill supplies the procedure for operating them.

Remote changes use authorization already established for the target, cost, and action. Missing decisions are resolved against a concrete plan before the affected operation. Inspection or file preparation alone does not deploy anything, and permission to deploy does not include unrelated data deletion or server rebuilding.

Provisioning finishes with verified bootstrap and access. A web deployment finishes with the expected application response through its public hostname and valid HTTPS where requested. Partial or failed operations are reported with their actual state and remaining resources; an uncertain write is reconciled before retrying it.

The Skill handles Hetzner Cloud and its hosted workloads. Hetzner Robot dedicated servers and Object Storage are outside its scope. It supplies agent instructions, not a transactional provisioning engine or a preselected application stack.

## POSITIONAL ARGUMENTS

*INSTRUCTION*

The requested operation and any constraints, such as project, environment, application, domain, budget, or maintenance window. The free-text operand and the Contextual Instruction behind the reserved separator carry one instruction; both spellings have the same meaning.

## DIAGNOSTICS

This grammar declares no options or subcommands. A dash-prefixed token is read as an operand carrying instruction text. A malformed Envelope, such as a reserved separator without an instruction, is refused rather than ignored; the Skill prints the error and SYNOPSIS, changes nothing, and points to `/hetzner --help`.

An unresolved target, missing access, or unknown result from a write blocks dependent remote operations. The Skill reports what can still be prepared locally and what decision or evidence is needed. It does not report a running VM as a completed application deployment or a successful backup as a tested restore.

## EXAMPLES

Prepare a deployment without creating resources.

```
/hetzner Prepare this project's cloud-init and deployment files; do not create a server yet.
```

Continue a previously authorized deployment in its established context.

```
/hetzner -- Continue the staging deployment we agreed on and verify its HTTPS endpoint.
```

Investigate an interrupted operation before repeating it.

```
/hetzner Check whether the timed-out server creation succeeded in staging.
```

## INVOCATION ENVELOPE

Every form ends with [**--** *INSTRUCTION*], the optional Contextual Instruction behind the reserved separator. The full contract is in the Manager's Collection Library at `library/references/invocation-envelope.md`.

## DEPENDENCIES

`uv` and the Kntnt Manager run the invocation engine. No peer Skill or Harness Capability is required. Both Claude Code and Codex can use the same shipped files.

Remote Cloud operations additionally need hcloud, network access, and a token for the selected project; server operations need OpenSSH and the appropriate key/access. These are checked for the requested operation, so local preparation and help remain available without remote prerequisites. Install missing tools from their official sources only within the task's authorized scope; missing credentials are supplied through the user's secret mechanism, not the conversation.

## SEE ALSO

**/kntnt select**
