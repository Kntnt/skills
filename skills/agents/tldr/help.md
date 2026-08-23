# tldr

## NAME

tldr - summarise the previous response or keep later responses concise

## SYNOPSIS

**/tldr** [*INSTRUCTION*...]

**/tldr** (**--on**|**--off**) [**--user**] [**--yes**]

**/tldr** **--status**

## DESCRIPTION

`tldr` has two modes of operation. Without a mode option it summarises what the agent has written since the user last spoke, together with any earlier context needed to understand that range. With `--on` or `--off` it controls a standing instruction that keeps later replies concise.

A summary contains what happened, what the agent decided on the user's behalf, and what still needs the user. All three parts appear even when nothing needs the user. It uses the conversation's language unless *INSTRUCTION* requests another language, range, focus, length, or format.

TL;DR mode applies to replies in the conversation, not to source files, documentation, comments, commit messages, or other artifacts. Short ordinary replies need no template; longer work reports retain a closing verdict that states what needs the user.

## POSITIONAL ARGUMENTS

*INSTRUCTION*...

Free-form instructions for the summary, in any language. They may widen the range, select a language, narrow the subject, or constrain the output.

## OPTIONS

**--on**

Enable TL;DR mode for the selected scope.

**--off**

Disable TL;DR mode for the selected scope.

**--status**

Report session and user state, the effective verdict, and any stale managed block. It changes nothing and cannot be combined with the other options.

**--user**

Target this Harness's user context instead of the current session. The Skill shows the file and exact managed block before writing.

**--yes**

Write or remove the user block without waiting for confirmation. It is valid only with `--on` or `--off`.

## SCOPES

**session**

The default. It applies only to the current conversation and is stored nowhere else. Context compaction may drop it.

**user**

A managed block in this Harness's global context file. There is no Project scope because reply length is a reader preference rather than a shared Project convention.

## DIAGNOSTICS

An incomplete or invalid form is refused rather than ignored. The Skill names the error, prints the SYNOPSIS, changes nothing, and points to `/tldr --help`. In particular, `/tldr --user` and `/tldr --yes` are invalid, while `/tldr --on --user --yes` is valid.

A summary that cannot cover the requested range because the preceding response is already short or context compaction removed part of it says so instead of presenting an incomplete result as complete.

## EXAMPLES

**/tldr bara säkerhetsdelen**

Summarise only the security-related part of the previous response.

**/tldr --on --user**

Show and confirm a user-level block that keeps later replies concise in the current Harness.

## DEPENDENCIES

None.

## SEE ALSO

**/delegation --help**, **/kntnt select**
