# model-selector capture

## NAME

model-selector capture - opt in to automatic local usage capture

## SYNOPSIS

**/model-selector** **capture** **--on** [**--harness=**_NAME_] [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **capture** **--off** [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **capture** **--status** [**--data=**_PATH_] [**--** *INSTRUCTION*]

## DESCRIPTION

Capture turns ordinary work in Claude Code, Codex, or OpenCode into a local Usage Record: what one finished session cost and how long it took on the exact Seat it ran on.

It is explicit opt-in because **--on** installs persistent lifecycle integration. Nothing is captured before consent, and **--off** removes every owned hook without deleting Usage Records already appended.

During substantive work, the integration records bounded lifecycle, Seat, and usage metadata. A session's end turns it into one Usage Record per Seat it ran on, appended immediately; temporary data is then removed.

Capture measures ordinary work; it never judges it. A Usage Record carries no outcome, no checker, and no Cohort, enters no derived frontier, and produces no evidence record. Nothing waits for a human, ever.

Hooks perform local metadata I/O only: no network request, model call, test run, repository-wide hash, transcript scan, or background daemon. Capture failures never interrupt the session.

## OPTIONS

**--on**

Install capture into each selected Harness, or every supported detected Harness by default. Repeating the command repairs the existing installation. Unsupported lifecycle capability is reported as Unsatisfied. Codex reviews a new or changed hook before running it; a Codex integration that installed correctly is reported gated — present, not yet active — naming what to do to clear the review.

**--off**

Remove every owned hook and adapter, verifying the result per Harness. Usage Records already appended remain. Disabling the Skill performs the same cleanup.

**--status**

Report enablement, adapter health, and storage use, without network access.

**--harness=**_NAME_

Select `claude-code`, `codex`, or `opencode`; repeat for several. Without this option, every supported detected Harness is selected.

**--data=**_PATH_

Use *PATH* instead of `~/.kntnt/model-selector/` for capture data, the evidence ledger, and the Usage Record store.

## RETAINED DATA

Capture retains the opaque session identity and usage key; the Harness and its inventory revision; the exact Seat — model, deliberation control, serving mode, access channel, and tool and policy fingerprints; the usage categories the environment exposed — tokens, tool calls, retries, cost, quota, latency, and fallback; and the two instants a Seat ran between.

It never retains full prompts, responses, reasoning, source files, diffs, terminal output, secrets, credentials, complete transcripts, or unnecessary absolute paths. An allow-list controls every copied field.

## OUTPUT

One JSON object reporting the requested installation, removal, or status result.

## DIAGNOSTICS

An unsupported Harness is reported as an Unsatisfied integration capability rather than silently skipped. A Harness that gates a new integration behind a user's trust review, as Codex does, is reported gated rather than healthy; this Skill never forges that trust decision or writes a trust record on the user's behalf. An installation or removal that only partly applied is reported per Harness and never as a complete one. A failure inside the hook path is swallowed by design and never reaches the session it was called from.

## INVOCATION ENVELOPE

[**--** *INSTRUCTION*] adds an optional Contextual Instruction. The first standalone, unquoted `--` is the reserved separator. Everything before it is the Formal Invocation; everything after it, including later `--` tokens, is guidance. The guidance may start on the same line or after blank lines and must contain non-whitespace text.

`--force`, `foo--bar`, `` `--` ``, and `"--"` are not separators. Without the separator, the whole payload remains formal input, including later lines and paragraphs.

After validating the Formal Invocation, the Skill uses guidance to clarify or narrow open choices. Guidance cannot contradict formal input or an invariant, widen the Skill, bypass a gate, or request unrelated work. Redundant but applicable guidance is valid. Applicable Conversation Context follows the same limits.

Malformed formal input or an empty instruction takes the syntax refusal. The Skill names the error, prints the addressed SYNOPSIS, changes nothing, and points to help. Context on an exact help route takes the context refusal without rendering the page.

Valid but irrelevant, unaddressable, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal. The Skill names the guidance and its boundary, reports the mutation outcome, prints no synopsis, and stops without applying a valid remainder.

Unaddressable guidance can affect nothing inside the Skill's contract. Guidance settled by a documented precedence is suppressed instead: the run continues and reports the suppression where useful. Suppression for one parameter does not invalidate guidance that applies to another.

Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict appears only after a legitimate effect, it stops before the next effect and reports the exact partial outcome. It rolls nothing back unless atomic behaviour was promised.

A nested Skill receives only relevant guidance through an explicit Contextual Instruction. Successful execution requires no context acknowledgement; an existing report names a materially changed choice where useful.

## DEPENDENCIES

`uv` runs the shipped offline capture module. The owned lifecycle integration requires Claude Code, Codex, or OpenCode; any other Harness reports the capability Unsatisfied.

## SEE ALSO

**/model-selector record --help**, **/model-selector observe --help**, **/model-selector status --help**
