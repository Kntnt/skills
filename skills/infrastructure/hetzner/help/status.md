# hetzner status

## NAME

hetzner status - list the projects the agents can reach, and their key

## SYNOPSIS

**/hetzner** **status** [**--** *INSTRUCTION*]

## DESCRIPTION

`status` lists every hcloud context, marks the active one, and says for each whether the Hetzner API accepts its token and how many servers it sees. A token that is not accepted is named with hcloud's reason.

It then says whether the agents' key `~/.ssh/kntnt-agent` exists and shows its public half. Per context, it says whether the project holds a key named `kntnt-agent`, which is what a server created there gets at creation.

It closes with the `setup` that is owed, where one is. No token is printed, and nothing is changed.

## FILES

`~/.config/hcloud/cli.toml`

hcloud's own configuration, whose contexts are listed.

`~/.ssh/kntnt-agent.pub`

The public half of the agents' key.

## DIAGNOSTICS

Without hcloud, no context can be listed; the key is still reported. An option with no work to do is refused rather than ignored: the Skill names the error, prints this SYNOPSIS, changes nothing, and points at `/hetzner status --help`.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*], the optional Contextual Instruction behind the reserved separator. The full contract is in the Manager's Collection Library at `library/references/invocation-envelope.md`.

## DEPENDENCIES

`uv` runs the Skill's engine, and hcloud lists the contexts and asks each project what it holds.

## SEE ALSO

**/hetzner setup --help**, **/hetzner --help**
