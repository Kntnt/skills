# hetzner setup

## NAME

hetzner setup - put a project's API token on this machine, and give the agents a key of their own

## SYNOPSIS

**/hetzner** **setup** [**--yes**] *PROJECT* [**--** *INSTRUCTION*]

## DESCRIPTION

`setup` first tells you how to create the token: in the Hetzner Console, open the project, then Security, API tokens, Generate API token, with Read & Write permission, and copy it. Paste it nowhere. The Skill waits for your word that it is copied.

The token then goes from the clipboard into hcloud's own configuration as a context named *PROJECT*. It stands in the environment of that one `hcloud context create` call and nowhere else: not in an argument, not on a terminal, not in the conversation, and not in any file of this Skill.

`setup` verifies the token by listing the project's servers and reports how many there are. It leaves the active hcloud context as it found it, because the Skill names its context on every call.

Once per machine, it makes the agents' own SSH key, `~/.ssh/kntnt-agent`: an ed25519 key without a passphrase, since the point of the key is that nobody is there to type one. A second `setup` leaves the key as it is. It registers the public half in the project under the name `kntnt-agent` where the project holds no key of that name, so a server created there gets it at creation.

Last, it prints the public key and both ways to admit the agents to a server that already exists, each opened by the condition it applies under. Either way the agents get a user `kntnt-agent` of their own with passwordless `sudo`, rather than root's login. The private key is never printed and never copied anywhere.

A configuration tool such as Ansible manages a server when it converges the server's accounts or SSH configuration. On a server a configuration tool manages, the agents are declared as an administrator of their own through that tool, in the workflow of the project at hand, the repository you run `setup` in, and the tool's converge puts them on the server. On a server nothing converges, a procedure admits them: run it as root on each such server.

`setup` reads the project at hand for such a tool. It prints the tool's way first where it finds one, and the procedure first where it finds none, as when you run it outside any repository.

## POSITIONAL ARGUMENTS

*PROJECT*

The project's name exactly as the Console shows it. The context carries that name, which is how an instruction naming the project reaches it.

## OPTIONS

**--yes**

Replace a context named *PROJECT* that already exists with the token on the clipboard. That is how a token is rotated: create a new one in the Console, copy it, and run `setup --yes` *PROJECT*.

## FILES

`~/.config/hcloud/cli.toml`

hcloud's own configuration, where the context and its token are written.

`~/.ssh/kntnt-agent`

The agents' private key, with `kntnt-agent.pub` beside it.

## DIAGNOSTICS

Where a context named *PROJECT* already exists, `setup` refuses without `--yes`, names it, and changes nothing. Everything after `setup` and its flag is the project's name, so a sentence written there becomes one.

An empty clipboard, a missing hcloud or `ssh-keygen`, and a token the Hetzner API does not accept are each reported with what to do. A token that is not accepted leaves its context in place, and `setup --yes` *PROJECT* with the right token replaces it. Where `--yes` has deleted the old context and the new one could not be created, the report says so, and `setup` *PROJECT* creates it again.

An option with no work to do is refused rather than ignored, and so is one written after the operand: the Skill names the error, prints this SYNOPSIS, changes nothing, and points at `/hetzner setup --help`.

## EXAMPLES

Rotate the token of `kntnt-wordpress`, after copying a new one in the Console.

```
/hetzner setup --yes kntnt-wordpress
```

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*], the optional Contextual Instruction behind the reserved separator. The full contract is in the Manager's Collection Library at `library/references/invocation-envelope.md`.

## DEPENDENCIES

`uv` runs the Skill's engine. hcloud holds the context, `ssh-keygen` makes the key, and a clipboard tool — `pbpaste` on macOS, `wl-paste`, `xclip` or `xsel` on Linux — reads the token. The Collection Library's credentials script hands the token to hcloud.

## SEE ALSO

**/hetzner status --help**, **/hetzner --help**
