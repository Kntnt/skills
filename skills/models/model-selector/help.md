# model-selector

## NAME

model-selector - compare configured AI model systems by price and performance

## SYNOPSIS

**/model-selector** [**recommend**] [**--decision=route**|**--decision=renew**] [**--budget=**_AMOUNT_|**--quality=**_SCORE_] [**--data=**_PATH_] [*WORKLOAD*] [**--** *INSTRUCTION*]

**/model-selector** **context** [**--data=**_PATH_] *PATH* [**--** *INSTRUCTION*]

**/model-selector** **route** *PATH* [**--** *INSTRUCTION*]

**/model-selector** (**chart**|**compare**) [**--decision=route**|**--decision=renew**] [**--data=**_PATH_] *WORKLOAD* [**--** *INSTRUCTION*]

**/model-selector** **setup** [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **config** [**show**|**history**] [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **config** **reset** [**--evidence**] [**--yes**] [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **config** **add** [**--data=**_PATH_] (**model**|**channel**) [**--** *INSTRUCTION*]

**/model-selector** **config** (**edit**|**remove**) [**--data=**_PATH_] (**model**|**channel**) *ID* [**--** *INSTRUCTION*]

**/model-selector** **update** [**--force**] [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **observe** **--artifact=**_PATH_ [**--import** [**--data=**_PATH_]] *PATH* [**--** *INSTRUCTION*]

**/model-selector** **record** [**--data=**_PATH_] *PATH* [**--** *INSTRUCTION*]

**/model-selector** **status** [**--data=**_PATH_] [**--** *INSTRUCTION*]

## DESCRIPTION

`model-selector` compares complete model configurations: exact model, reasoning control, serving mode, Harness, tools, policies, access channel, and current commercial terms.

Run `setup` first to record available models and channels. The reusable profile contains no credentials.

Recommendations use comparable Pareto frontiers. Cash, quota, credits, latency, and quality stay separate unless you provide a common valuation.

Without representative matched measurements, cold start chooses the weakest plausibly capable enabled model and its lowest plausibly sufficient supported reasoning control. Reversible checked work may move one adjacent Rung after verified failure: the next reasoning control on the same model, or the next model up by capability where that scale is exhausted or the Harness carries the control.

High-consequence or irreversible work without a trustworthy checker uses the strongest plausible enabled configuration and refuses unsafe exploration.

Every result labels its evidence source, date, uncertainty, exclusions, and missing evidence. Bundled public data is a prior, not local measurement.

Enabling this Skill installs session lifecycle integration into each supported Detected Harness in the Global layer. It retains only the Seat a session ran on, usage counts, timestamps, and opaque identifiers — never prompts, responses, reasoning, file contents, or paths. Disabling the Skill removes every entry this integration owns and keeps what was already measured.

That integration also refreshes the Skill's own public sources unattended. At a session's end it conditionally re-retrieves the model, capability, and benchmark index pages your configuration already names and that have fallen due — one connection at a time, within a two-second budget, sending no credential and no identifier of you or your machine — and writes each source's own check state under the data directory. It reads no page for its content, starts no model, and writes no other evidence. Pricing pages, subscription terms, and gateway rate cards are never retrieved this way; `status` reports them as due and `update` is what checks them. Disabling the Skill removes this with the rest of the integration.

## COMMANDS

**recommend** [*WORKLOAD*]

Choose one exact configuration and report its nearest cheaper and stronger comparable frontier neighbours. Bare `/model-selector` uses this command when the current workload is unambiguous.

**context** *PATH*

Derive a complete route artifact from persisted selections and exact runtime Harness facts, or validate and carry a frozen snapshot unchanged for a later routing call.

**route** *PATH*

Resolve one versioned structured request or ordered batch into exact, Harness-native launch decisions and a reusable frozen snapshot without setup, network access, evaluation, or persistent writes.

**chart** *WORKLOAD*

Build the applicable frontiers without choosing one winner, then emit compact tables and plotting-ready CSV.

**compare** *WORKLOAD*

An alias of `chart`.

**setup**

Create the initial profile or perform a complete guided review of the existing profile.

**config**

Display or revise the model and access-channel profile. Its page lists every configuration subcommand.

**update**

Perform one bounded refresh of due model indexes, first-party capability sources, commercial terms, and benchmark releases. Changed capability claims append low-confidence prior records without rewriting history. Known immutable model detail pages and existing local run keys are not fetched or executed again.

**observe** *PATH*

Turn completed routed attempts into sanitized run observations in a caller-owned artifact. Only an external judgement establishes an outcome and unavailable measurements stay `null`. Without **--import** it writes no ledger and the artifact waits for `record`; with it, a routed caller's machine-judged observations are filed in the same call.

**record** *PATH*

Validate and append unseen local evaluation observations. Conflicting historical observations are preserved rather than overwritten.

**status**

Report the profile, evidence vintage, due sources, gaps, provisional facts, and capture's own health without network access or writes.

## OPTIONS

**--artifact=**_PATH_

Write the observations into the caller-owned artifact at *PATH*, creating it when absent and merging into it when present. Required by `observe` and valid with no other command.

**--import**

For `observe`, file this call's machine-judged observations in the evidence ledger and rebuild only the frontiers whose eligible run set changed. An outcome a frozen rubric or a person established is never filed by it, and a ledger refusal is reported rather than raised.

**--data=**_PATH_

Use *PATH* as the profile and evidence directory. Valid with every command except `route`, which reads neither, and on `observe` only with **--import**, which is the one thing that command writes evidence for. The default is `~/.kntnt/model-selector/`.

**--decision=route**, **--decision=renew**

For `recommend`, `chart`, and `compare`, compare marginal routing economics now or whether a fixed subscription fee earns renewal. `route` is the default.

**--budget=**_AMOUNT_

For `recommend`, select the highest conservative quality within a budget when every eligible point uses a comparable cost unit. Mutually exclusive with `--quality`.

**--quality=**_SCORE_

For `recommend`, select the lowest conservative comparable cost that clears the quality floor. Mutually exclusive with `--budget`.

**--force**

For `update`, check every relevant mutable index once regardless of cadence. Known immutable details and existing observations remain untouched.

**--evidence**

For `config reset`, discard this machine's own measurement — the evidence ledger and its derived frontiers, the quota store, the Standing Policy override and its history, capture and the Usage Record store — after confirmation, while keeping the profile, its history, and researched public facts. Valid only for `config reset`; bare `config reset` removes the profile and keeps this same measurement.

**--yes**

Answer `--evidence`'s confirmation yes rather than asking, for an unattended run. Valid only combined with `--evidence`, and refused rather than ignored on every other form, `config reset` bare included.

## OUTPUT

`recommend` starts with one evidence banner: `🔵 HEURISTISK STARTPUNKT`, `🟠 BLANDAD EVIDENS`, or `🟢 MÄTDATABASERAD REKOMMENDATION`. It states the classification reason, confidence, missing evidence, and whether the result is an exploration start or production recommendation.

`context` returns ordered requests beside derived current context or an unchanged frozen snapshot. `route` returns ordered `selected`, `inherit`, or `refused` decisions and a reproducible frozen snapshot. Selections carry Harness-native launch arguments; refusals carry stable reasons.

A recommendation names the exact configuration, decision rule, comparable neighbours, exclusions, uncertainty, and staleness. Insufficient evidence produces a small discriminating evaluation instead of an invented rank.

After a blue or orange banner, `Snabbaste vägen till mätdata` provides a bounded sequential and parallel experiment brief and a `record`-compatible artifact. `recommend` plans the experiment but performs no network request, evaluation, or write.

`Observerad förbrukning` follows, reporting what each named model has actually cost and taken from this machine's own Usage Records, with the count, the vintage and the deliberations behind each figure. Matching is by model alone, so two points differing only in deliberation carry the same figures, and none of it enters a frontier or chooses anything.

`chart` and `compare` keep cash, quota, and renewal views separate unless explicit shadow prices create a common axis, and carry the same usage figures as columns. Missing metrics are `null`, never zero.

`update` reports every checked source and appended change. A discovered model is not Enabled automatically. `status` reports what the unattended session-end refresh keeps current and what it may never retrieve, naming `update` for each.

## FILES

**~/.kntnt/model-selector/config.json**

The default active profile and revision history. **--data** relocates it.

**~/.kntnt/model-selector/capture/**

Temporary per-session drafts. A draft is deleted the moment its session ends.

**~/.kntnt/model-selector/source-states.jsonl**

One mutable row per public source, updated in place, recording when each was last looked at, last retrieved, and last seen to change.

**Evidence ledger**

Append-only effective-dated observations under the selected data directory.

**~/.kntnt/model-selector/usage-records.jsonl**

Append-only Usage Records, one per Seat a finished session ran on, beside the evidence ledger. Carries no outcome and is never quality.

## DIAGNOSTICS

An incomplete form, unsupported combination, or option with no work to do is refused rather than ignored. The Skill names the error, prints the addressed command's SYNOPSIS, changes nothing, and points to that command's `--help` page. An operand written before an option is out of order and is refused the same way.

No changed source is a successful `update`. Unreachable or insufficient evidence is reported without turning unavailable data into a zero or an invented comparison.

## EXAMPLES

**/model-selector recommend --decision=route repository refactor**

Select an exact configured system for a repository-refactoring workload using marginal routing economics.

**/model-selector route ./routing-request.json**

Resolve a caller-owned request artifact without changing profile or evidence state.

**/model-selector context ./context-request.json**

Derive the complete route input from stored selections and caller-supplied runtime facts without setup or writes.

**/model-selector update --force**

Check every relevant mutable source once while retaining known immutable details and recorded observations.

## INVOCATION ENVELOPE

[**--** *INSTRUCTION*] adds an optional Contextual Instruction. The first standalone, unquoted `--` is the reserved separator. Everything before it is the Formal Invocation; everything after it, including later `--` tokens, is guidance. The guidance may start on the same line or after blank lines and must contain non-whitespace text.

`--force`, `foo--bar`, `` `--` ``, and `"--"` are not separators. Without the separator, the whole payload remains formal input, including later lines and paragraphs.

After validating the Formal Invocation, the Skill uses guidance to clarify or narrow open choices. Guidance cannot contradict formal input or an invariant, widen the Skill, bypass a gate, or request unrelated work. Redundant but applicable guidance is valid. Applicable Conversation Context follows the same limits.

Malformed formal input or an empty instruction takes the syntax refusal. The Skill names the error, prints the addressed SYNOPSIS, changes nothing, and points to help. Context on an exact help route takes the context refusal without rendering the page.

Valid but irrelevant, unaddressable, materially ambiguous, conflicting, or scope-widening guidance takes the distinct context refusal. The Skill names the guidance and its boundary, reports the mutation outcome, prints no synopsis, and stops without applying a valid remainder.

Unaddressable guidance can affect nothing inside the Skill's contract. Guidance settled by a documented precedence is suppressed instead: the run continues and reports the suppression where useful. Suppression for one parameter does not invalidate guidance that applies to another.

Before the first side effect, the Skill uses available read-only checks to identify unusable guidance. If a conflict appears only after a legitimate effect, it stops before the next effect and reports the exact partial outcome. It rolls nothing back unless atomic behaviour was promised.

A nested Skill receives only relevant guidance through an explicit Contextual Instruction. Successful execution requires no context acknowledgement; an existing report names a materially changed choice where useful.

The following schematic cases pin the split independently of any one Skill's Formal Invocation grammar; `\n\n` denotes two newline characters in one payload.

| Case | Envelope | Formal Invocation | Contextual Instruction | Outcome |
| --- | --- | --- | --- | --- |
| Same line | `/skill --force -- Preserve deployment facts` | `/skill --force` | `Preserve deployment facts` | Envelope valid; formal grammar next |
| Blank lines | `/skill --force --\n\nPreserve deployment facts` | `/skill --force` | `Preserve deployment facts` | Envelope valid; formal grammar next |
| Empty suffix | `/skill --force --   ` | `/skill --force` | — | Syntax refusal |
| Later separator | `/skill -- Preserve -- deployment facts` | `/skill` | `Preserve -- deployment facts` | Envelope valid; formal grammar next |
| No separator | `/skill Preserve deployment facts` | `/skill Preserve deployment facts` | — | No split; formal grammar decides |
| Attached and quoted | ``/skill --force foo--bar `--` "--"`` | ``/skill --force foo--bar `--` "--"`` | — | No split; formal grammar decides |
| Exact help | `/skill --help -- Explain this page` | `/skill --help` | `Explain this page` | Context refusal; render nothing |

## DEPENDENCIES

`uv` runs the shipped offline routing module. Network access is used only by `update`; every other command operates on bundled or locally stored evidence and reports insufficiency.

## SEE ALSO

**/model-selector recommend --help**, **/model-selector config --help**, **/model-selector status --help**, **/kntnt select**
