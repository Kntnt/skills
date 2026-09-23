# cloudns

## NAME

cloudns - read and change DNS zones and records at ClouDNS

## SYNOPSIS

**/cloudns** [**--** *INSTRUCTION*]

**/cloudns** **setup** [**--yes**] [*SUB-USER*] [**--** *INSTRUCTION*]

**/cloudns** **status** [**--** *INSTRUCTION*]

## DESCRIPTION

Say what you want changed in DNS at ClouDNS after the separator, such as `/cloudns -- point www.example.com at 192.0.2.10`, and the Skill reads the zone, plans the change record by record, applies it through the ClouDNS API, reads the zone again to verify it, and reports what changed and what the service answered. Without an instruction it works on the DNS task already established in the conversation, or asks for one.

It acts as a ClouDNS API sub-user, never as the account's main API user, so it can reach exactly the zones delegated to that sub-user and nothing wider. A zone the sub-user cannot see is reported as not delegated, and the Skill stops there rather than looking for another way in.

The sub-user's password is drawn by `setup`, stored in the Credential File and put on the clipboard for you to paste into the ClouDNS panel. It never appears in the conversation or in anything the Skill prints.

A deletion, and an import that replaces a zone's existing records, cannot be undone at ClouDNS. They are made only where you asked for them or a decision you already made covers them.

## COMMANDS

**setup**

Draw a new password for the sub-user, write the Credential File, put the password on the clipboard, and tell you the ClouDNS panel steps only you can take. With **--yes** it rotates a credential already held.

**status**

Check the credential with ClouDNS and list the zones the sub-user can see, which are the zones the Skill may touch.

## POSITIONAL ARGUMENTS

*SUB-USER*

The name of the ClouDNS API sub-user, for `setup` only. The default is `kntnt-agent`.

## OPTIONS

**--yes**

For `setup` only: replace the credential the Credential File already holds with a new password. This is the rotation.

## FILES

**~/.kntnt/cloudns/credentials.json**

The Credential File, holding `sub-auth-user` and `auth-password`, readable by you alone (mode `0600`). `setup` writes it; every call reads it and refuses a file group or world may read. `KNTNT_HOME`, where set, replaces your home directory in the path.

## DIAGNOSTICS

An invalid form is refused rather than ignored. The Skill names the error, prints the SYNOPSIS for the most specific page, changes nothing, and points to that page. A flag is refused rather than ignored where it has no work to do here, and a flag written after an operand is out of order and refused.

The root form takes no operand, so a change written without the separator, such as `/cloudns point www.example.com at 192.0.2.10`, is refused as an unknown command. Write it after `--`.

A call that deletes — its API path's last segment begins with `delete` — or that carries `delete-existing-records=1` is refused before anything is sent unless the Skill asserts that you asked for it or a decision you already made covers it.

`setup` refuses to overwrite a credential the Credential File already holds unless **--yes** is given, and names the keys it would have replaced.

A missing Credential File stops every remote operation with a pointer to `/cloudns setup`. A Credential File that group or world may read is refused, naming its mode and the mode it needs.

## EXAMPLES

**/cloudns -- delete the TXT record _acme-challenge on example.com**

Delete one record you named. The Skill lists the zone first, shows the record it will delete, and deletes it because you asked for exactly that.

**/cloudns setup --yes**

Rotate the password: a new one is drawn, stored and put on the clipboard, and you paste it as the sub-user's new password in the ClouDNS panel.

**/cloudns setup dns-bot**

Make the credential for a sub-user named `dns-bot` rather than `kntnt-agent`.

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

**/cloudns setup --help**, **/cloudns status --help**, **/hetzner --help**
