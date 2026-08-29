# model-selector capture

## NAME

model-selector capture - opt in to automatic local run-evidence capture

## SYNOPSIS

**/model-selector** **capture** **--on** [**--harness=**_NAME_] [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **capture** **--off** [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **capture** **--status** [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **capture** **--review=**_IDENTITY_ **--action=save**|**--action=failed**|**--action=ignore** [**--data=**_PATH_] [**--** *INSTRUCTION*]

## DESCRIPTION

Capture turns ordinary work in Claude Code, Codex, or OpenCode into local Model Selector evidence.

It is explicit opt-in because **--on** installs persistent lifecycle integration. Nothing is captured before consent, and **--off** removes every owned hook without deleting accepted evidence.

During substantive work, the integration records bounded lifecycle, usage, checker, quota, and latency metadata. Eligible completed work becomes one normalized observation; temporary data is then removed.

Only an external checker, frozen rubric, declared failure signal, or user confirmation establishes success or failure. Unjudged work waits for **--review** in a bounded pending store.

Hooks perform local metadata I/O only: no network request, model call, test run, repository-wide hash, transcript scan, or background daemon. Capture failures never interrupt the session.

## OPTIONS

**--on**

Install capture into each selected Harness, or every supported detected Harness by default. Repeating the command repairs the existing installation. Unsupported lifecycle capability is reported as Unsatisfied.

**--off**

Remove every owned hook and adapter, verifying the result per Harness. Accepted evidence remains. Disabling the Skill performs the same cleanup.

**--status**

Report enablement, adapter health, pending-review count and age, storage use, and retention bounds. It also reconciles abandoned drafts without network access.

**--review=**_IDENTITY_

Settle one pending capture listed by **--status**. Requires **--action**.

**--action=save**, **--action=failed**, **--action=ignore**

Record the reviewed work as success or failure, or discard it. Saved outcomes carry explicit user confirmation.

**--harness=**_NAME_

Select `claude-code`, `codex`, or `opencode`; repeat for several. Without this option, every supported detected Harness is selected.

**--data=**_PATH_

Use *PATH* instead of `~/.kntnt/model-selector/` for capture data, evidence, and derived frontiers.

## RETAINED DATA

Capture retains opaque session and task IDs; timestamps and Harness; exact model configuration; tool and policy fingerprints; checker result; token, tool, retry, fallback, cost, quota, and latency measurements; provenance; and sanitized artifact hashes.

It never retains full prompts, responses, reasoning, source files, diffs, terminal output, secrets, credentials, complete transcripts, or unnecessary absolute paths. An allow-list controls every copied field.

## RETENTION

Imported, empty, and irrelevant drafts are deleted. Pending and failed captures are limited to 30 days, 100 drafts, and 1 MiB; oldest entries go first. Cleanup runs at session start or **--status**, never in a daemon. Accepted evidence is not subject to these limits.

## OUTPUT

One JSON object reporting the requested installation, removal, status, or review result.

## DIAGNOSTICS

An unsupported Harness is reported as an Unsatisfied integration capability rather than silently skipped. An installation or removal that only partly applied is reported per Harness and never as a complete one. A failure inside the hook path is swallowed by design and never reaches the session it was called from.

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
