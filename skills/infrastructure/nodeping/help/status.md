# nodeping status

## NAME

nodeping status - report the NodePing account the stored token reaches

## SYNOPSIS

**/nodeping status** [**--** *INSTRUCTION*]

## DESCRIPTION

`nodeping status` asks NodePing for the account the stored API token reaches and reports its name and id, and each subaccount's where the service lists them. Where the service refuses the token, it relays the refusal; a token that is wrong or has been regenerated is replaced with `/nodeping setup --yes`.

It changes nothing and prints no value of the token.

## FILES

**~/.kntnt/nodeping/credentials.json**

The Credential File the token is read from. `KNTNT_HOME`, where set, replaces `~`.

## DIAGNOSTICS

An invalid form is refused rather than ignored. The Skill names the error, prints this page's SYNOPSIS, changes nothing, and points at `/nodeping status --help`. A flag is refused rather than ignored where it has no work to do here, so **--yes** is refused, and so is any word after `status`.

A missing Credential File is reported with a pointer to `/nodeping setup`, and a file that group or world may read is refused, naming the mode it needs. Where the service cannot be reached, the Skill says so.

## EXAMPLES

**/nodeping status**

Report the account's name and id, or the service's refusal.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

**Binaries**

`uv` on `PATH`.

**Skills**

The Kntnt Manager must be installed so the invocation engine and the Collection Library can run.

**Network**

Network access and a NodePing API token stored with `/nodeping setup`.

## SEE ALSO

**/nodeping --help**, **/nodeping setup --help**
