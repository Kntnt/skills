# model-selector route

## NAME

model-selector route - resolve delegated work into exact launch decisions

## SYNOPSIS

**/model-selector route** [**--data=**_PATH_] *PATH* [**--** *INSTRUCTION*]

## DESCRIPTION

Read one versioned structured request or an ordered batch from *PATH* and print a structured response containing a frozen routing snapshot and exactly one `selected`, `inherit`, or `refused` decision per input in the same order. A selected decision identifies its exact model, adapter, channel, surface, native deliberation control, serving mode, tools, policy, configuration fingerprint, complete Harness-native launch arguments, evidence class, provenance, exclusions, and bounded next escalation. Only a selected decision carries launch overrides; every refusal carries a stable reason.

Route is offline, non-interactive, and read-only. It never starts setup, performs research or evaluation, refreshes evidence, writes configuration, or writes the evidence ledger. A missing profile or evidence that cannot discriminate safely can yield audited inheritance; invalid or unsafe state yields refusal.

The portable deliberation values are `low`, `medium`, `high`, `xhigh`, and `max`. Omission selects automatically. Native names and numeric budgets are not public input. Each usable value resolves through the snapshot to a verified exact native value; unsupported values are refused rather than approximated.

## POSITIONAL ARGUMENTS

*PATH*

A UTF-8 JSON artifact conforming to `references/route-request.schema.json`. It is one envelope with integer `schema_version: 1`, an ordered `requests` array, and either a previously returned `snapshot` or current read-only `context` that the public Skill adapter derives from local profile/evidence and active Harness facts before invoking the internal script. The Model Routing Module in `references/model-routing.md` is the complete behavioral contract.

## OPTIONS

**--data=**_PATH_

Read the current profile and evidence from *PATH* only when the request does not carry a snapshot. The public Skill adapter consumes this flag while it derives the canonical `context`; the internal script receives only the resulting artifact path. The default is `~/.kntnt/model-selector/`. Route never writes there.

## OUTPUT

One JSON object conforming to `references/route-response.schema.json`, with `schema_version`, `snapshot`, and ordered `decisions`. Reusing `snapshot` reproduces routing from its frozen profile revision, evidence, Harness inventory, main seat, native mappings, commercial facts, and override policy instead of adopting later state.

## DIAGNOSTICS

A malformed artifact is refused before routing. Invalid CLI arguments, unreadable paths, and malformed JSON produce a machine-readable top-level `artifact_refusal`, an empty decision list, exit status 2, and no traceback. Request-level invalid profile state, ambiguous or unavailable overrides, unknown safety ceiling, above-main override, unrepresentable verdict inheritance, and an empty safe candidate set produce stable refused decisions with no launch instruction. An operand written before an option is out of order and is refused the same way.

## INVOCATION ENVELOPE

[**--** *INSTRUCTION*] introduces an optional Contextual Instruction after the formal input. The first standalone, unquoted `--` token is the reserved separator; everything before it remains Formal Invocation and everything after it is instruction, including later `--` tokens. The instruction may start on the same line or after blank lines and must contain non-whitespace text. Attached or quoted forms such as `--force`, `foo--bar`, `` `--` ``, and `"--"` remain formal data. Without the separator, the complete payload remains formal input, including later lines and paragraphs.

A Contextual Instruction is read and used as natural-language guidance after the Formal Invocation is valid. Redundant but applicable guidance is valid. It may clarify or narrow choices the Skill leaves open and overrides older preferences within those choices, but cannot contradict formal input or an invariant, widen the Skill, disable a required gate, or request work outside its contract. Applicable guidance from Conversation Context has the same boundaries and need not be copied into the Invocation Envelope.

An empty instruction or malformed Formal Invocation takes the syntax refusal: the Skill names the error, prints the addressed SYNOPSIS, changes nothing, and points to help. Valid but irrelevant, unaddressable, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal: the Skill names the guidance and boundary, reports the mutation outcome, prints no synopsis, and stops without partial application. Unaddressable is guidance with no addressable effect at all — guidance touching nothing this Skill's contract addresses — and never guidance a documented precedence has already settled against, which is suppressed instead: suppression is that precedence working, so the run continues and the delivery names the suppressed guidance beside the resolved configuration where saying so is useful. Only guidance that is part invalid — part conflicting, part scope-widening, or part unaddressable — goes unapplied as a whole; one parameter suppressed and another landing is an ordinary invocation. Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict can only be discovered after a legitimate effect, the Skill stops before the next effect, reports the exact partial outcome, and does not roll work back unless it already promises atomic behaviour. Context on an exact help route is refused without rendering the help page.

When this Skill invokes another Skill, it passes only relevant guidance through an explicit Contextual Instruction in that Skill's own Invocation Envelope; it never forwards an outer instruction blindly. Successful execution adds no mandatory context acknowledgement, while an existing report identifies a materially changed choice when that choice belongs there.

## DEPENDENCIES

`uv` runs the shipped offline routing module.

## SEE ALSO

**/model-selector recommend --help**, **/model-selector status --help**
