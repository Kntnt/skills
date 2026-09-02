# model-selector context

## NAME

model-selector context - derive complete current routing context

## SYNOPSIS

**/model-selector context** [**--data=**_PATH_] *PATH* [**--** *INSTRUCTION*]

## DESCRIPTION

Read one versioned context request from *PATH*. A first-call request combines ordered route requests with exact runtime Harness and main-seat facts; the command reads the selected profile and shipped routing data, then returns a complete artifact accepted by `route`. A later-call request combines new ordered requests with a previously frozen snapshot and returns that snapshot byte-for-byte unchanged.

Context is offline, non-interactive, and read-only. It never starts setup, performs network access, research, evaluation, or evidence refresh, and never writes configuration, evidence, or any other persistent state. Missing or invalid configuration yields a `null` profile and audited inheritance rather than setup.

## POSITIONAL ARGUMENTS

*PATH*

A UTF-8 JSON artifact conforming to `references/context-request.schema.json`, with `schema_version: 1`, ordered `requests`, and exactly one of `runtime` or `snapshot`. Runtime names the active Harness, stable inventory identity, inheritance support and optional inheritance attestation whose `verified` value must equal that inventory identity, plus the exact main-seat model, surface, serving mode, portable and native deliberation, tools, policy, and optional channel. Context itself refuses a supplied snapshot whose frozen facts no longer match its `snapshot_identity`.

## OPTIONS

**--data=**_PATH_

Read `config.json` from *PATH*. The default is `~/.kntnt/model-selector/`; Context never writes there.

## OUTPUT

One JSON object with `schema_version`, the ordered `requests`, and either a complete current `context` or the supplied frozen `snapshot`. Current context retains every enabled validated selection, reports unavailable comparable ranks as `null`, specializes only adapters the active Harness can launch, and carries shipped override defaults. Commercial dimensions remain `null` until exact measurements exist.

## DIAGNOSTICS

Invalid forms produce `invalid_arguments`; unreadable paths produce `unreadable_artifact`; malformed JSON produces `malformed_json`; and structurally invalid runtime or snapshot input produces `invalid_context_input`. Every refusal is machine-readable, emits no traceback, and writes nothing. A flag is refused rather than ignored where it has no work to do here, because accepting an ignored flag would misrepresent the command's grammar.

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

`uv` runs the shipped offline context adapter.

## SEE ALSO

**/model-selector route --help**, **/model-selector status --help**
