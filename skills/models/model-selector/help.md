# model-selector

## NAME

model-selector - choose the model and deliberation level that finishes work for the least money

## SYNOPSIS

**/model-selector** [**--json**] [**--scope=**_SCOPE_] [**--kind=**_KIND_] [**--data=**_PATH_] [*WORK*] [**--** *INSTRUCTION*]

**/model-selector** **setup** [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **status** [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **update** [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **evidence** [**--data=**_PATH_] [*KIND*] [**--** *INSTRUCTION*]

**/model-selector** **reset** [**--evidence**] [**--yes**] [**--data=**_PATH_] [**--** *INSTRUCTION*]

## DESCRIPTION

Describe a piece of work and get back the model and deliberation level expected to finish it for the least money — first the models this machine's own measurements say will get the job done, and among those the one whose price per finished job is lowest: what one attempt costs divided by its chance of success, because an attempt that fails bought nothing, left the work still to do, and is paid for again. A model unlikely to finish is never chosen for being cheap. About one call in ten of the reversible kind tries a cheaper point instead, moving either the model or the deliberation level but never both, because a store that only ever runs its favourite never finds out that something cheaper would have sufficed. The answer says when it was one of those, and what the measurements would otherwise have chosen.

The answer names one model, one deliberation level, how to launch it, what one attempt is expected to cost and how long it takes, how likely it is to succeed, what a finished job is expected to cost and how long it takes — one attempt's price and elapsed time each divided by that chance, the total the answer was ranked on — and what that estimate rests on: this machine's own measurements of that exact kind of work, measurements of the same model at other work, or the model's published capability with nothing local behind it. Alternatives come with it, so a dominated candidate can be seen losing.

There is no answer that means *start nothing*. With no profile, an empty catalogue or nothing reachable, the answer is the seat you already have, with a note saying why. Skills that route delegated work call the same engine directly and read the answer as JSON. A caller that is a script rather than a Harness says so with `--harness=process`, and is answered with a command it can start rather than a subagent only an agent can name; where the work it is launching writes nothing, `--read-only` asks for the command that grants no way to.

`setup` is a short interview, held once: which Harnesses this covers, which providers you want suggestions from, which of their models, and how each provider is paid for on each channel — a subscription plan and its tier, an API rate card, or both at once where you reach the same provider two ways. Nothing that can be looked up is asked of you. Without a profile the Skill still answers, treating every catalogue model the detected Harnesses can reach as available, and `status` says so.

Enabling this Skill installs session lifecycle hooks into every supported Harness on this machine, in the Global layer, and those hooks are what make the answers get better. They measure a unit of work — an instruction and the answer to it — and only where the unit was a job: delegated work that was substantial — three or more changing tool calls, or sixty seconds, or four thousand output tokens — and work of the session's own that was substantial and ran for ten minutes or more besides. Quick questions, short exchanges and short turns of your own are discarded with no trace, so an ordinary conversational session contributes nothing at all. Nothing runs while work is in flight: a subagent's record is read when that subagent stops, and the session's own record when the session ends, and those two moments are the only ones a hook is installed at.

Where nothing else has established how a finished unit went, one call to a model your profile makes reachable reads that unit's instruction and its result and returns a score and a line of reason. It is chosen as the work it is — reviewing what somebody else finished against a standard — and at high stakes, because nothing downstream catches a wrong score: among the points the measurements are confident clear that bar, the one whose price per finished job is lowest, rather than the cheapest point there is — and where a model has already been measured reviewing on this machine and clears it, the judge is chosen among those before any point that is only estimated. The call itself is one bounded exchange whichever way it is asked for, so what the kind buys is a judge that can read the work rather than a cheaper call. Those two excerpts are used to make the call and are stored nowhere. What is retained is one row per unit: the kind, the model, the deliberation level, the score and who established it, the token counts the Harness exposed, the cost those tokens price at, the elapsed time, and whether the work was routed. Prompts, responses, reasoning, diffs, file contents, terminal output and absolute paths are never copied, because the row is built by copying named fields rather than by removing unwanted ones.

The public facts this Skill reasons from — which models exist, what each supports, what each costs, and what each provider's subscriptions are called — are read off the providers' own pages by the agent running `update`. A script has no web tool and does not pretend to one. So the network is reached by `update`, and by `setup` where it begins with that same reading because the catalogue has gone stale, and by nothing else at all; every other command works from what is already on disk. What was read is validated before it is stored: an entry with nothing to attribute it to is discarded by name, a rate card in a currency other than USD or a unit other than per million tokens is refused rather than converted, and `capability` is never fetched, being a seeded prior that measurement refines.

Nothing waits for you. There is no queue to work through and no reminder placed where a model would read it. Disabling the Skill removes every hook it installed and keeps what was measured; `reset --evidence` is the separate act that discards the measurement, and you have to ask for it by name.

## COMMANDS

**setup**

Hold the interview and write the profile: Harnesses, providers, models, and how each provider is paid for on each channel. Run it again to review an existing profile.

**status**

Report the profile and its age, how fresh the catalogue's own facts are, what has been measured, how many units wait to be graded and how long the oldest has waited, whether the judge is at its daily cap and when the cap frees, and the health of each Harness integration. It asks nothing, changes nothing, and reaches nothing.

**update**

Read the providers' own pages and adopt what they say — model lists, rate cards, and the subscriptions each provider markets — into the catalogue. The reading is the agent's; validating it, merging it and writing it is the Skill's. An entry arriving without a source it can attribute is discarded rather than stored, and a document that is not the catalogue's shape at all is refused whole.

**evidence**

Report what has been measured, grouped by kind, model and deliberation level, with the counts and dates behind each figure. An optional operand narrows it to one kind.

**reset**

Discard the profile and hold the interview again. With **--evidence**, discard what this machine measured as well. The catalogue is public fact and is kept either way.

## OPTIONS

**--json**

Emit the selection response as the engine returned it, with nothing added: the answer as a machine reads it, rather than rendered for a person. Valid on the bare form and no other. A Skill that routes delegated work does not come through here at all — it runs `scripts/selection.py`, which answers in that shape and no other.

**--scope=**_SCOPE_

Which models may be considered: `limited` for your own provider's, `callable` for those plus every model this Harness can reach through a Bridge and your profile has a channel for, or `all` for the whole catalogue whether it can be reached or not. The default is `callable`. For a caller that is a process rather than a Harness, `callable` means what this machine can start, and every point takes the same test — your own provider's included, a seat being no evidence that the CLI behind it is installed: a Bridge plans a command for the point, your profile has a channel for it, and that command's binary is on the `PATH` here. Scope is a statement about reachability, never about preference.

**--kind=**_KIND_

The class of work, which is what an estimate is keyed on: `mechanical`, `implement`, `design`, `debug`, `review`, `analyze`, `prose`, or `converse`. Omitted, the work you described is classified into one of them. A finer description belongs in the work text, where it is kept and reported without splitting the comparison.

**--data=**_PATH_

Use *PATH* as the profile, catalogue and measurement directory instead of `~/.kntnt/model-selector/`. Every command means the same directory by it.

**--evidence**

For `reset`, discard this machine's measurement as well as the profile: the measurement store, the units still waiting to be graded, and the capture directory. The Harness hooks stay installed and keep measuring.

**--yes**

Answer `reset`'s confirmation yes rather than asking, for an unattended run. Valid only with `reset`.

## FILES

**~/.kntnt/model-selector/profile.json**

What the interview settled: Harnesses, providers, enabled models, and one payment channel per provider and Harness. It holds no credentials. **--data** relocates it, and everything below it.

**~/.kntnt/model-selector/catalogue.json**

World facts adopted over the shipped seed — exact model identities, family aliases, supported deliberation levels, rate cards, and the subscriptions each provider markets, each carrying the address it was read from and the date it was read. The capability figures beside them are the seed's own, refined by measurement rather than by fetching.

**~/.kntnt/model-selector/measurements.jsonl**

One append-only row per measured unit of work. Keyed by kind, model and deliberation level, and carrying no text from the work itself.

**~/.kntnt/model-selector/pending.jsonl**

Units that have been seen and not yet graded. Working state, and it goes with **--evidence** — as does the `capture/` directory beside it, which an earlier design filled with per-session drafts and nothing writes any more.

**Generated subagent definitions**

One file per enabled Anthropic model and supported deliberation level, written into the Harness's own agents directory, prefixed so they are identifiable, and rewritten by every `setup`. Editing one is pointless; they are the only files this collection writes there.

## DIAGNOSTICS

An incomplete form, an unsupported combination, or an option with no work to do on the form it was given with is refused rather than ignored. The Skill names the error, prints the addressed command's SYNOPSIS, changes nothing, and points at that command's own help page. An option written after the work text is out of order and is refused the same way; a dash-prefixed word this Skill declares no option for is part of the work text.

Nothing the selection engine answers is a refusal. A missing profile, an empty catalogue and an unreachable model are each a degraded answer naming your own seat, with a note saying which it was — a caller that must be stopped is stopped by something that knows what the work is worth.

A page that says what the catalogue already held is a successful `update`. An `update` in a Harness with no web tool says so and changes nothing. A figure no measurement supports is reported absent rather than as a zero.

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

`uv` runs the shipped selection engine, the interview's writer, the catalogue's own reader and validator, and the capture hooks. The network is reached by `update` and by `setup`, and by nothing else; every other command works from what is already on disk. Reading a provider's page needs whatever web tool your Harness gives the agent, and where it gives none, `update` says so and changes nothing. Grading a finished unit calls one model, chosen as the cheapest your own profile makes reachable that the measurements are confident in, and stops rather than inventing a number where none can be reached.

## SEE ALSO

**/model-selector setup --help**, **/model-selector status --help**, **/model-selector evidence --help**, **/kntnt select**
