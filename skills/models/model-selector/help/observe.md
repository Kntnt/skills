# model-selector observe

## NAME

model-selector observe - turn judged routed attempts into an importable artifact

## SYNOPSIS

**/model-selector** **observe** **--artifact=**_PATH_ [**--import** [**--data=**_PATH_]] *PATH* [**--** *INSTRUCTION*]

## DESCRIPTION

Read completed routed attempts from *PATH* and write sanitized observations to **--artifact**. Each attempt yields one observation or stable refusal in input order. Importability uses the same validation as `/model-selector record`.

Observations are statistical metadata, not transcripts. They include routed and served configurations, opaque identities, workload stratum, outcome authority, available usage, cost, quota, latency, provenance, and sanitized artifact hashes. Missing measurements remain `null`.

Prompts, responses, reasoning, source material, diffs, terminal output, secrets, credentials, complete transcripts, and unnecessary absolute paths are excluded.

Only an independent verifier, objective checker, frozen rubric, declared failure signal, or explicit user confirmation establishes an outcome. Self-report is refused. Non-model failures remain infrastructure errors or abstentions and never lower measured quality.

Observe is offline, non-interactive, and idempotent. It performs no setup, research, evaluation, or profile write. Identical attempts add nothing; conflicting identities overwrite neither side.

Without **--import** this command imports nothing, and the artifact waits in caller-owned scratch for `/model-selector record`. With it, the observations an independent verifier, objective checker, or declared failure signal established, and the conditions no model produced, are filed in the same call; a frozen rubric and a person's own word are never filed by it. Orchestrate's verdict path reaches the same shared implementation directly.

## POSITIONAL ARGUMENTS

*PATH*

A UTF-8 JSON artifact with `schema_version: 1` and an ordered `attempts` array. See `references/run-observations.md` for the complete schema.

## OPTIONS

**--artifact=**_PATH_

Create or merge the caller-owned observation artifact at *PATH*.

**--import**

File the machine-judged observations of this call in the evidence ledger, rebuilding only the derived frontiers whose eligible run set changed and evaluating the Standing Policy of every cohort the import touched. A routed caller asks for this; the verb keeps its single side effect without it.

**--data=**_PATH_

Use *PATH* instead of `~/.kntnt/model-selector/` as the evidence directory **--import** writes. Valid only alongside it, this command reading no evidence of its own.

## OUTPUT

One JSON object naming the artifact, the run keys newly written to it, the identical ones skipped, any conflicting identities, and one stable refusal per attempt that could not become an observation.

With **--import** it also carries the import account: the identities filed, the identical ones the ledger already held, the conflicting ones it kept both sides of, every refusal with its stable code, and each touched cohort's Standing Policy answer. Without the flag that account is `null`.

## DIAGNOSTICS

Invalid arguments, paths, JSON, or Envelope produce top-level `artifact_refusal`, exit status 2, and no traceback.

Unjudged, unlaunched, interrupted, self-graded, or unsanitized attempts receive individual stable refusals while valid peers remain. Out-of-order arguments are refused.

A ledger that refuses or cannot be written is reported in the import account and never raised: the work an observation describes is already done, and the exit status stays 0. **--data** written without **--import** is an unsupported option rather than a hint.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv` runs the shipped offline observation module.

## SEE ALSO

**/model-selector record --help**, **/model-selector route --help**
