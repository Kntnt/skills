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

Read the current profile and evidence from *PATH* only when the request does not carry a snapshot. The public Skill adapter consumes this flag while it derives the canonical `context`; the internal script receives only the resulting artifact path. The default is `~/.model-selector/`. Route never writes there.

## OUTPUT

One JSON object conforming to `references/route-response.schema.json`, with `schema_version`, `snapshot`, and ordered `decisions`. Reusing `snapshot` reproduces routing from its frozen profile revision, evidence, Harness inventory, main seat, native mappings, commercial facts, and override policy instead of adopting later state.

## DIAGNOSTICS

A malformed artifact is refused before routing. Invalid CLI arguments, unreadable paths, and malformed JSON produce a machine-readable top-level `artifact_refusal`, an empty decision list, exit status 2, and no traceback. Request-level invalid profile state, ambiguous or unavailable overrides, unknown safety ceiling, above-main override, unrepresentable verdict inheritance, and an empty safe candidate set produce stable refused decisions with no launch instruction. An operand written before an option is out of order and is refused the same way.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv` runs the shipped offline routing module.

## SEE ALSO

**/model-selector recommend --help**, **/model-selector status --help**
