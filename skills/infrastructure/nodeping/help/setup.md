# nodeping setup

## NAME

nodeping setup - store the NodePing API token and check that the service accepts it

## SYNOPSIS

**/nodeping setup** [**--yes**] [**--** *INSTRUCTION*]

## DESCRIPTION

`nodeping setup` asks you to copy the API token from NodePing's panel, under Account Settings and then API, and to say when it is on the clipboard. It then writes the token from the clipboard into the Credential File and checks it against the service as `status` does, so you hear in one answer that the file is written and whether NodePing accepts the token.

The token never passes through the conversation. Where the machine has no clipboard tool, the Skill names the file a person may write by hand instead.

To rotate the token, press Regenerate in the same place, which revokes the old one, copy the new one, and run `setup --yes`.

## OPTIONS

**--yes**

Replace the token the Credential File already holds. Without it, `setup` refuses to overwrite a stored token and writes nothing.

## FILES

**~/.kntnt/nodeping/credentials.json**

The Credential File, holding one key, `token`, readable by its owner alone (mode `0600`) in a directory only its owner can enter. `KNTNT_HOME`, where set, replaces `~`.

## DIAGNOSTICS

An invalid form is refused rather than ignored. The Skill names the error, prints this page's SYNOPSIS, changes nothing, and points at `/nodeping setup --help`. `setup` takes no operand, so any word after it is refused.

Without **--yes**, a Credential File that already holds a token is left as it is, and the clipboard is not read: the refusal names the file and the key, and says that **--yes** asserts the working token is meant to be replaced.

An empty clipboard, or no clipboard tool on the `PATH`, is refused with the path of the file to write by hand. A Credential File that group or world may read is refused, naming the mode it needs.

## EXAMPLES

**/nodeping setup**

Store the token for the first time and check it.

**/nodeping setup --yes**

Rotate the token after regenerating it in NodePing's panel.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

**Binaries**

`uv` on `PATH`.

**Skills**

The Kntnt Manager must be installed so the invocation engine and the Collection Library can run.

**Clipboard and network**

A clipboard tool: `pbpaste` on macOS, `wl-paste`, `xclip` or `xsel` on Linux, and PowerShell on Windows. Checking the token needs network access; writing the file does not.

## SEE ALSO

**/nodeping --help**, **/nodeping status --help**
