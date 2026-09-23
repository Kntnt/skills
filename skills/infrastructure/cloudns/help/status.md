# cloudns status

## NAME

cloudns status - check the ClouDNS credential and list the zones it reaches

## SYNOPSIS

**/cloudns** **status** [**--** *INSTRUCTION*]

## DESCRIPTION

`status` asks ClouDNS whether it accepts the credential the Credential File holds, and reports which sub-user it is and whether it was accepted. Where it was, it lists every zone the sub-user can see; those are exactly the zones delegated to it or created by it, and so exactly the zones the Skill may touch.

Where ClouDNS refuses the credential, `status` relays the service's own description of why, and says that the panel step may not be done yet: the sub-user not created, or the password not pasted. Where the Credential File is missing, it says so and names `/cloudns setup`.

It changes nothing, and it prints the sub-user's name but never the password.

## FILES

**~/.kntnt/cloudns/credentials.json**

The Credential File `status` reads. A file group or world may read is refused, naming its mode.

## DIAGNOSTICS

An invalid form is refused rather than ignored. The Skill names the error, prints this page's SYNOPSIS, changes nothing, and points at `/cloudns status --help`. A flag is refused rather than ignored where it has no work to do here, so **--yes** is refused, and so is any operand.

## EXAMPLES

**/cloudns status**

Confirm the credential after `setup`, and see which zones came through.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

**Binaries**

`uv` on `PATH`, which runs the engine and the Manager's Credential File writer.

**Skills**

The Manager must be Enabled so the invocation can be read and the credential written.

**Services**

Remote operations need network access and a ClouDNS API sub-user with the existing zones it may touch delegated to it, and a **DNS zones** quota with room for the zones it is to create. `setup` also needs a clipboard tool — `pbcopy` on macOS, `wl-copy`, `xclip` or `xsel` on Linux, `clip` on Windows — or a Credential File written by hand. Help and `setup`'s file writing reach no network.

## SEE ALSO

**/cloudns --help**, **/cloudns setup --help**
