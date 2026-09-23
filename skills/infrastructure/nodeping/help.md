# nodeping

## NAME

nodeping - read and change uptime monitoring at NodePing

## SYNOPSIS

**/nodeping** [**--** *INSTRUCTION*]

**/nodeping** **setup** [**--yes**] [**--** *INSTRUCTION*]

**/nodeping** **status** [**--** *INSTRUCTION*]

## DESCRIPTION

`nodeping` inspects and changes uptime monitoring at NodePing on the user's behalf: checks, their results and uptime, contacts, contact groups, schedules and notifications. The instruction says what to do and arrives behind the reserved separator; with none, the Skill uses the task established in the conversation, or asks what is wanted.

It reads what exists before it writes, matches a check or a contact by its label and target rather than by a guessed id, applies the change, and reads again to verify it. The report says what changed, what the service answered, and what remains.

The Skill acts with NodePing's API token, which reaches the whole account and every subaccount; the service offers no narrower token. A deletion is sent only within authorization the user has already given. Disabling a check is not a deletion, since the check can be enabled again.

The token is stored once, with `setup`, in a file only its owner can read, and never passes through the conversation. `status` checks that the service accepts it.

## COMMANDS

**setup**

Store the API token from the clipboard in the Credential File, then check it as `status` does. Replacing a stored token needs **--yes**.

**status**

Ask the service for the account the stored token reaches, and report its name and id or the service's refusal.

## OPTIONS

**--yes**

With `setup`, replace the token the Credential File already holds. Use it to rotate the token after regenerating it at NodePing.

## FILES

**~/.kntnt/nodeping/credentials.json**

The Credential File. It holds one key, `token`, and must be readable by its owner alone (mode `0600`); the Skill refuses a file whose mode admits group or world. `KNTNT_HOME`, where set, replaces `~`. Revoke the token by regenerating it in NodePing's panel, under Account Settings and then API.

## DIAGNOSTICS

An invalid form is refused rather than ignored. The Skill names the error, prints the SYNOPSIS for the most specific page, changes nothing, and points to that page's `--help`. A flag is refused rather than ignored where it has no work to do here, so **--yes** outside `setup` is refused.

An instruction written without the reserved separator is read as an unknown command and refused: write `/nodeping -- add a check for kntnt.se`, not `/nodeping add a check for kntnt.se`. `setup` and `status` take no operand.

`setup` without **--yes** refuses to overwrite a token the Credential File already holds, and writes nothing.

A deletion is refused unless the user has authorized it, in both of its spellings: the `DELETE` method, and an `action` parameter whose value is `delete` in any case, in the query string or the JSON parameters. NodePing accepts either, so the gate covers both.

A missing Credential File stops the Skill with a pointer to `/nodeping setup`; a file that group or world may read is refused, naming the mode it needs. Where the service cannot be reached, the outcome of a write is unknown, and the Skill reads the object again before any retry.

## EXAMPLES

**/nodeping -- add an HTTP check for https://kntnt.se/ every five minutes, notifying thomas@example.com**

Look for an existing check with that target, create one only where none exists, and read it back.

**/nodeping -- remove the check for staging.kntnt.se; I authorize the deletion**

Find the check by its target, state what will be deleted, delete it, and confirm it is gone. Without the authorization, the Skill presents the plan and asks for it before deleting.

**/nodeping setup --yes**

Rotate the token: regenerate it in NodePing's panel, copy it, and say when it is on the clipboard. The Skill replaces the stored token and checks that the service accepts the new one.

**/nodeping status**

Report which account the stored token reaches.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

**Binaries**

`uv` on `PATH`.

**Skills**

The Kntnt Manager must be installed so the invocation engine and the Collection Library can run.

**Remote operations**

Network access and a NodePing API token, stored with `setup`. `setup` reads the clipboard through the platform's own tool: `pbpaste` on macOS, `wl-paste`, `xclip` or `xsel` on Linux, and PowerShell on Windows. Help, and `setup`'s writing of the file, need no network.

## SEE ALSO

**/nodeping setup --help**, **/nodeping status --help**, **/hetzner**, **/kntnt select**
