# model-selector observe

## NAME

model-selector observe - turn judged routed attempts into an importable artifact

## SYNOPSIS

**/model-selector** **observe** *PATH* **--artifact=**_PATH_ [**--** *INSTRUCTION*]

## DESCRIPTION

Read completed routed attempts from *PATH* and write the sanitized run observations they establish into the caller-owned artifact named by **--artifact**. Each attempt is answered in input order, either by one observation or by one stable refusal, and the artifact is reported as importable only when every observation in it passes exactly the validation `/model-selector record` applies.

An observation is statistical metadata rather than a transcript. It carries the exact routed point and the point that actually served, opaque session and task identity, workload stratum, benchmark identity, outcome with its external authority and checker, available token, tool, cost, quota, and latency facts, retries, both instants, provenance, and sanitized artifact hashes. It never carries prompts, responses, reasoning, ticket or source bodies, source files, diffs, terminal output, secrets, credentials, complete transcripts, or absolute paths where an opaque identity is sufficient. Every measurement the environment did not expose stays an explicit `null`.

Only an external judgement establishes a decisive outcome: an independent verifier, an objective checker, a frozen rubric, a declared failure signal, or explicit user confirmation. A builder's or a subagent's self-report is refused rather than recorded, and a mechanical hinder, an open decision, a discovered dependency, a tracker failure, or a merge collision is retained as an infrastructure error or an abstention that never lowers a configuration's quality. A route decision no judgement completed remains audit data and is not serialized at all.

Observe is offline, non-interactive, and idempotent. It starts no setup, performs no network access, research, or evaluation, and writes no profile, evidence ledger, or derived frontier. Repeating an identical attempt adds nothing to the artifact, and an identity already present with different content is surfaced as a conflict that overwrites neither side. Nothing is imported here: the artifact stays in caller-owned scratch until the user invokes `/model-selector record` on it.

## POSITIONAL ARGUMENTS

*PATH*

A UTF-8 JSON artifact holding integer `schema_version: 1` and an ordered `attempts` array. Each attempt carries its immutable route decision, opaque identities, workload stratum, attempt index, benchmark identity, active Harness, externally established outcome, completion instant, and whatever usage, cost, quota, and latency facts the environment exposed. The complete contract is `references/run-observations.md`.

## OPTIONS

**--artifact=**_PATH_

Write the observations into the artifact at *PATH*, creating it when absent and merging into it when present. The file belongs to the caller, is normally a scratch path of the run that produced the attempts, and is the path an explicit import is later given.

## OUTPUT

One JSON object naming the artifact, the run keys newly written to it, the identical ones skipped, any conflicting identities, and one stable refusal per attempt that could not become an observation.

## DIAGNOSTICS

Invalid arguments, an unreadable path, malformed JSON, and a malformed envelope produce a machine-readable top-level `artifact_refusal`, exit status 2, and no traceback. An attempt that no external judgement established, that launched nothing, that was interrupted, that was graded by its own author, or that carries material rather than identities is refused individually and named with its stable code, leaving its peers' results intact.

## INVOCATION ENVELOPE

[**--** *INSTRUCTION*] introduces an optional Contextual Instruction after the formal input. The first standalone, unquoted `--` token is the reserved separator; everything before it remains Formal Invocation and everything after it is instruction, including later `--` tokens. The instruction may start on the same line or after blank lines and must contain non-whitespace text. Attached or quoted forms such as `--force`, `foo--bar`, `` `--` ``, and `"--"` remain formal data. Without the separator, the complete payload remains formal input, including later lines and paragraphs.

A Contextual Instruction is read and used as natural-language guidance after the Formal Invocation is valid. Redundant but applicable guidance is valid. It may clarify or narrow choices the Skill leaves open and overrides older preferences within those choices, but cannot contradict formal input or an invariant, widen the Skill, disable a required gate, or request work outside its contract. Applicable guidance from Conversation Context has the same boundaries and need not be copied into the Invocation Envelope.

An empty instruction or malformed Formal Invocation takes the syntax refusal: the Skill names the error, prints the addressed SYNOPSIS, changes nothing, and points to help. Valid but irrelevant, ineffective, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal: the Skill names the guidance and boundary, reports the mutation outcome, prints no synopsis, and stops without partial application. Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict can only be discovered after a legitimate effect, the Skill stops before the next effect, reports the exact partial outcome, and does not roll work back unless it already promises atomic behaviour. Context on an exact help route is refused without rendering the help page.

When this Skill invokes another Skill, it passes only relevant guidance through an explicit Contextual Instruction in that Skill's own Invocation Envelope; it never forwards an outer instruction blindly. Successful execution adds no mandatory context acknowledgement, while an existing report identifies a materially changed choice when that choice belongs there.

## DEPENDENCIES

`uv` runs the shipped offline observation module.

## SEE ALSO

**/model-selector record --help**, **/model-selector route --help**
