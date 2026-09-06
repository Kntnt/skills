# model-selector

## NAME

model-selector - choose the model and deliberation level that finishes work for the least money

## SYNOPSIS

**/model-selector** [**--json**] [**--scope=**_SCOPE_] [**--kind=**_KIND_] [**--data=**_PATH_] [*WORK*] [**--** *INSTRUCTION*]

**/model-selector** **setup** [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **status** [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **update** [**--force**] [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **evidence** [**--data=**_PATH_] [*KIND*] [**--** *INSTRUCTION*]

**/model-selector** **reset** [**--evidence**] [**--yes**] [**--data=**_PATH_] [**--** *INSTRUCTION*]

## DESCRIPTION

Describe a piece of work and get back the model and deliberation level expected to finish it for the least money — not the cheapest model, but the one whose price divided by its chances of getting the job done is lowest. An attempt that fails bought nothing and left the work still to do, which is why a weak model has to be several times cheaper before it wins.

The answer names one model, one deliberation level, how to launch it, what it is expected to cost, how likely it is to succeed, and what that estimate rests on: this machine's own measurements of that exact kind of work, measurements of the same model at other work, or the model's published capability with nothing local behind it. Alternatives come with it, so a dominated candidate can be seen losing.

There is no answer that means *start nothing*. With no profile, an empty catalogue or nothing reachable, the answer is the seat you already have, with a note saying why. Skills that route delegated work call the same engine directly and read the answer as JSON.

`setup` is a short interview, held once: which Harnesses this covers, which providers you want suggestions from, which of their models, and how each provider is paid for on each channel — a subscription plan and its tier, an API rate card, or both at once where you reach the same provider two ways. Nothing that can be looked up is asked of you. Without a profile the Skill still answers, treating every catalogue model the detected Harnesses can reach as available, and `status` says so.

Enabling this Skill installs session lifecycle hooks into every supported Harness on this machine, in the Global layer, and those hooks are what make the answers get better. They measure a unit of work — an instruction and the answer to it — and only where the unit was substantial: three or more changing tool calls, or sixty seconds, or four thousand output tokens. Quick questions and short exchanges are discarded with no trace, so an ordinary conversational session contributes nothing at all.

Where nothing else has established how a finished unit went, one call to the cheapest model your profile makes reachable reads that unit's instruction and its result and returns a score and a line of reason. Those two excerpts are used to make the call and are stored nowhere. What is retained is one row per unit: the kind, the model, the deliberation level, the score and who established it, the token counts the Harness exposed, the cost those tokens price at, the elapsed time, and whether the work was routed. Prompts, responses, reasoning, diffs, file contents, terminal output and absolute paths are never copied, because the row is built by copying named fields rather than by removing unwanted ones.

Those same hooks run one bounded refresh of the public facts at a session's end: a conditional re-fetch of the model lists, capability figures and rate cards that have fallen due, one connection at a time, within a small time budget, sending no credential and no identifier of you or your machine. It reads no page for anything but those facts, starts no model, and discards a fact that arrives without a source it can attribute. `update` is the same pass run by hand, and `status` is where it is reported.

Nothing waits for you. There is no queue to work through and no reminder placed where a model would read it. Disabling the Skill removes every hook it installed — the measuring and the refresh alike — and keeps what was measured; `reset --evidence` is the separate act that discards the measurement, and you have to ask for it by name.

## COMMANDS

**setup**

Hold the interview and write the profile: Harnesses, providers, models, and how each provider is paid for on each channel. Run it again to review an existing profile.

**status**

Report the profile and its age, how current the catalogue is, what the unattended refresh is waiting on, what has been measured, and the health of each Harness integration. It asks nothing and changes nothing.

**update**

Fetch what can be fetched now — model lists, capability figures, and rate cards — into the catalogue, one connection at a time and within a bounded budget. A price arriving without a source it can attribute is discarded rather than stored.

**evidence**

Report what has been measured, grouped by kind, model and deliberation level, with the counts and dates behind each figure. An optional operand narrows it to one kind.

**reset**

Discard the profile and hold the interview again. With **--evidence**, discard what this machine measured as well. The catalogue is public fact and is kept either way.

## OPTIONS

**--json**

Emit the selection response as the engine returned it, with nothing added. This is what a Skill routing delegated work reads; without it the same answer is rendered for a person. Valid on the bare form and no other.

**--scope=**_SCOPE_

Which models may be considered: `limited` for your own provider's, `callable` for those plus every model this Harness can reach through a Bridge and your profile has a channel for, or `all` for the whole catalogue whether it can be reached or not. The default is `callable`. Scope is a statement about reachability, never about preference.

**--kind=**_KIND_

The class of work, which is what an estimate is keyed on: `mechanical`, `implement`, `design`, `debug`, `review`, `analyze`, `prose`, or `converse`. Omitted, the work you described is classified into one of them. A finer description belongs in the work text, where it is kept and reported without splitting the comparison.

**--data=**_PATH_

Use *PATH* as the profile, catalogue and measurement directory instead of `~/.kntnt/model-selector/`. Every command means the same directory by it.

**--force**

For `update`, check every mutable source once rather than only those the shipped cadence has made due. The cadences ship with the Skill and the profile does not override them.

**--evidence**

For `reset`, discard this machine's measurement as well as the profile: the measurement store, the units still waiting to be graded, and the capture directory. The Harness hooks stay installed and keep measuring.

**--yes**

Answer `reset`'s confirmation yes rather than asking, for an unattended run. Valid only with `reset`.

## FILES

**~/.kntnt/model-selector/profile.json**

What the interview settled: Harnesses, providers, enabled models, and one payment channel per provider and Harness. It holds no credentials. **--data** relocates it, and everything below it.

**~/.kntnt/model-selector/catalogue.json**

World facts refreshed over the shipped seed — exact model identities, family aliases, supported deliberation levels, rate cards and capability figures, each carrying the address it came from and the date it was retrieved.

**~/.kntnt/model-selector/measurements.jsonl**

One append-only row per measured unit of work. Keyed by kind, model and deliberation level, and carrying no text from the work itself.

**~/.kntnt/model-selector/capture/**

In-flight per-session drafts, and `pending.jsonl` beside it holding units that have been seen and not yet graded. Both are working state and both go with **--evidence**.

**Generated subagent definitions**

One file per enabled Anthropic model and supported deliberation level, written into the Harness's own agents directory, prefixed so they are identifiable, and rewritten by every `setup`. Editing one is pointless; they are the only files this collection writes there.

## DIAGNOSTICS

An incomplete form, an unsupported combination, or an option with no work to do on the form it was given with is refused rather than ignored. The Skill names the error, prints the addressed command's SYNOPSIS, changes nothing, and points at that command's own help page. An option written after the work text is out of order and is refused the same way; a dash-prefixed word this Skill declares no option for is part of the work text.

Nothing the selection engine answers is a refusal. A missing profile, an empty catalogue and an unreachable model are each a degraded answer naming your own seat, with a note saying which it was — a caller that must be stopped is stopped by something that knows what the work is worth.

A source that did not change is a successful `update`. A figure no measurement supports is reported absent rather than as a zero.

## EXAMPLES

**/model-selector rewrite the payment reconciliation module against the new schema**

Classify the work, then name the model and deliberation level expected to finish it for the least money, with its nearest alternatives.

**/model-selector --scope=all --kind=design what should the retry policy be**

Consider the whole catalogue, including models this machine cannot currently reach, for a decision about what to build.

**/model-selector evidence debug**

Report every measured group for debugging work, with the counts and dates behind each figure.

**/model-selector reset --evidence --yes**

Discard the profile and the measurement without being asked to confirm.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv` runs the shipped selection engine, the interview's writer, the refresh pass and the capture hooks. Network access is used only by `update` and by the unattended refresh that follows a session; every other command works from what is already on disk. Grading a finished unit calls one model, chosen as the cheapest your own profile makes reachable, and stops rather than inventing a number where none can be reached.

## SEE ALSO

**/model-selector setup --help**, **/model-selector status --help**, **/model-selector evidence --help**, **/kntnt select**
