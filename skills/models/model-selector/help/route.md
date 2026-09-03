# model-selector route

## NAME

model-selector route - resolve delegated work into exact launch decisions

## SYNOPSIS

**/model-selector route** *PATH* [**--** *INSTRUCTION*]

## DESCRIPTION

Read one versioned request or ordered batch from *PATH*. Return a frozen snapshot and one `selected`, `inherit`, or `refused` decision per input in the same order.

A selection includes its exact configuration, Harness-native launch arguments, evidence, exclusions, and bounded next escalation. That escalation is one adjacent Rung: the next mapped deliberation level on the same model, or the next enabled model up by capability where that scale is exhausted or the Harness carries the control, entered at the lowest level of its own the request still reaches, and never above the main seat. A refusal carries a stable reason and no launch override.

Where several measured configurations clear the quality floor and no one of them dominates the rest, the frozen `override_policy.objective` decides between them: `cost_first`, the default, takes the lowest observed cash and breaks a tie on the lowest Time to Verified Pass, and `time_first` reverses the two. Complete shadow prices the profile declared still take precedence over it, and a frontier the applicable order cannot separate — or one whose points do not all carry the means it compares — still inherits, audited.

Route is offline, non-interactive, and read-only. It never starts setup, performs research or evaluation, refreshes evidence, writes configuration, or writes the evidence ledger. A missing profile or evidence that cannot discriminate safely can yield audited inheritance; invalid or unsafe state yields refusal.

The portable deliberation values are `low`, `medium`, `high`, `xhigh`, and `max`. Omission selects automatically. Native names and numeric budgets are not public input. Each usable value resolves through the snapshot to a verified exact native value; unsupported values are refused rather than approximated.

## POSITIONAL ARGUMENTS

*PATH*

A UTF-8 JSON artifact conforming to `references/route-request.schema.json`, with `schema_version: 1`, ordered `requests`, and either a returned `snapshot` or current `context`. See `references/model-routing.md` for the full contract.

## OUTPUT

One JSON object conforming to `references/route-response.schema.json`, with `schema_version`, `snapshot`, and ordered `decisions`. Reusing `snapshot` reproduces routing from its frozen profile revision, evidence, Harness inventory, main seat, native mappings, commercial facts, and override policy instead of adopting later state.

## DIAGNOSTICS

Malformed artifacts, arguments, paths, and JSON produce top-level `artifact_refusal`, an empty decision list, exit status 2, and no traceback.

Unsafe or unrepresentable request state produces a stable refused decision with no launch instruction. Out-of-order arguments are refused.

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

`uv` runs the shipped offline routing module.

## SEE ALSO

**/model-selector recommend --help**, **/model-selector status --help**
