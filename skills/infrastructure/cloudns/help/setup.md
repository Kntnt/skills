# cloudns setup

## NAME

cloudns setup - make or rotate the ClouDNS sub-user credential

## SYNOPSIS

**/cloudns** **setup** [**--yes**] [*SUB-USER*] [**--** *INSTRUCTION*]

## DESCRIPTION

`setup` draws a new password, writes it with the sub-user's name to the Credential File, and puts the password on the clipboard. It never shows the password.

It then tells you what only you can do, in this order: in the ClouDNS panel under **API & Resellers → API Sub-Users → Add new sub-user**, create a sub-user with that name; paste the password from the clipboard as its **auth-password**; set **DNS zones** to at least the number of zones the agent will manage, and **DNS records** likewise; choose **Access level: Read and write**; and leave **IP address** blank or restrict it, as you decide. Separately, delegate each zone the agent may touch to that sub-user, from the zone's own management in the panel.

Run `/cloudns status` afterwards: it confirms that ClouDNS accepts the credential and lists the zones that actually came through, which are the zones the Skill may touch.

Running `setup --yes` again is the rotation. A new password is drawn and put on the clipboard, and you paste it as the sub-user's new password in the panel; until you do, ClouDNS still expects the old one.

## POSITIONAL ARGUMENTS

*SUB-USER*

The name of the ClouDNS API sub-user. The default is `kntnt-agent`.

## OPTIONS

**--yes**

Replace the credential the Credential File already holds. Without it, `setup` refuses where a credential is already held.

## FILES

**~/.kntnt/cloudns/credentials.json**

The Credential File `setup` writes, holding `sub-auth-user` and `auth-password`, in a directory of mode `0700` and at mode `0600`. `KNTNT_HOME`, where set, replaces your home directory in the path.

## DIAGNOSTICS

An invalid form is refused rather than ignored. The Skill names the error, prints this page's SYNOPSIS, changes nothing, and points at `/cloudns setup --help`. A flag is refused rather than ignored where it has no work to do here, and **--yes** written after *SUB-USER* is out of order and refused.

A credential already held is not overwritten without **--yes**: `setup` names the key it would have replaced, says that **--yes** rotates it, and writes nothing. The operand takes the rest of the line, so prose written after `setup` becomes a sub-user's name; on a machine that already holds a credential, that is refused by this same rule.

Where no clipboard tool is found, nothing is written, and the message says how to write the Credential File by hand instead.

## EXAMPLES

**/cloudns setup**

Make the credential for a sub-user named `kntnt-agent`.

**/cloudns setup --yes**

Rotate the password of the sub-user the Skill already holds a credential for.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

**Binaries**

`uv` on `PATH`, which runs the engine and the Manager's Credential File writer.

**Skills**

The Manager must be Enabled so the invocation can be read and the credential written.

**Services**

Remote operations need network access and a ClouDNS API sub-user with the zones it may touch delegated to it. `setup` also needs a clipboard tool — `pbcopy` on macOS, `wl-copy`, `xclip` or `xsel` on Linux, `clip` on Windows — or a Credential File written by hand. Help and `setup`'s file writing reach no network.

## SEE ALSO

**/cloudns --help**, **/cloudns status --help**
