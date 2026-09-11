# model-selector

## NAME

model-selector - choose the model and deliberation level that finishes work for the least money, or soonest

## SYNOPSIS

**/model-selector** [**--json**] [**--scope=**_SCOPE_] [**--kind=**_KIND_] [**--data=**_PATH_] [*WORK*] [**--** *INSTRUCTION*]

**/model-selector** **setup** [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **status** [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **update** [**--data=**_PATH_] [**--** *INSTRUCTION*]

**/model-selector** **evidence** [**--data=**_PATH_] [*KIND*] [**--** *INSTRUCTION*]

**/model-selector** **objective** [**--data=**_PATH_] [**time**|**cost**] [**--** *INSTRUCTION*]

**/model-selector** **reset** [**--evidence**] [**--yes**] [**--data=**_PATH_] [**--** *INSTRUCTION*]

## DESCRIPTION

Describe a piece of work and get back the model and deliberation level expected to finish it for the least money, or in the least time where you have made that your standing choice — first the models this machine's own measurements say will get the job done, and among those the one whose price per finished job is lowest: what one attempt costs divided by its chance of success, because an attempt that fails bought nothing, left the work still to do, and is paid for again. A model unlikely to finish is never chosen for being cheap. About one call in ten of the reversible kind tries a cheaper point instead, moving either the model or the deliberation level but never both, because a store that only ever runs its favourite never finds out that something cheaper would have sufficed. The answer says when it was one of those, and what the measurements would otherwise have chosen.

The answer names one model, one deliberation level, how to launch it, what one attempt is expected to cost and how long it takes, how likely it is to succeed, what a finished job is expected to cost and how long it takes — one attempt's price and elapsed time each divided by that chance, the total the answer was ranked on — and what that estimate rests on: this machine's own measurements of that exact kind of work, measurements of the same model at other work, or the model's published capability with nothing local behind it. Alternatives come with it, so a dominated candidate can be seen losing.

Whether work is ordered on money or on time is one fact about you — how much of your subscription is left this week — so it is set once, with `objective`, and every Skill that routes work inherits it rather than growing a flag of its own. An answer asked for with no `--objective` ranks on your standing choice, a caller's own `--objective` wins over it, and with nothing set the answer ranks on cost, because running out of quota mid-week stops everything while a slower job is only slower. The answer names the objective it ranked on and whether it came from the caller, your standing choice, or the default.

There is no answer that means *start nothing*. With no valid profile, an empty catalogue or nothing reachable, the answer is the seat you already have, with a note saying why. Skills that route delegated work call the same engine directly and read the answer as JSON. A caller that is a script rather than a Harness says so with `--harness=process`, and is answered with a command it can start rather than a subagent only an agent can name; where the work it is launching writes nothing, `--read-only` asks for the command that grants no way to.

`setup` is a short interview, held once: which Harnesses this covers, which makers you want models from — Claude, GPT, Grok — and how each is paid for on each channel — a subscription plan and its tier, an API rate card, or both at once where you reach the same maker two ways. Every model a maker you choose offers is then a candidate, one it releases later included. You do not pick models one by one: the measurements decide between them, and a model you want for one piece of work is named with `--model`. Nothing that can be looked up is asked of you. Without a profile — or with one from before makers were chosen, or one that cannot be read — every answer not locked to a model is the seat you already have, with a note naming `setup`, and `status` says the same.

Enabling this Skill installs session lifecycle hooks into every supported Harness on this machine, in the Global layer, and those hooks are what make the answers get better. They measure a unit of work — an instruction and the answer to it — and only where the unit was a job: delegated work that was substantial — three or more changing tool calls, or sixty seconds, or four thousand output tokens — and work of the session's own that was substantial and ran for ten minutes or more besides. Quick questions, short exchanges and short turns of your own are discarded with no trace, so an ordinary conversational session contributes nothing at all. Nothing runs while work is in flight: a subagent's record is read when that subagent stops, and the session's own record when the session ends, and those two moments are the only ones a hook is installed at.

Where nothing else has established how a finished unit went, one call to a model your profile makes reachable reads that unit's instruction and its result and returns a score and a line of reason. It is chosen as the work it is — reviewing what somebody else finished against a standard — at high stakes, because nothing downstream catches a wrong score, and on cost whatever your standing choice, nobody waiting on a grade: among the points the measurements are confident clear that bar, the one whose price per finished job is lowest, rather than the cheapest point there is — and where a model has already been measured reviewing on this machine and clears it, the judge is chosen among those before any point that is only estimated. The call itself is one bounded exchange whichever way it is asked for, so what the kind buys is a judge that can read the work rather than a cheaper call. Those two excerpts are used to make the call and are stored nowhere. What is retained is one row per unit: the kind, the model, the deliberation level, the score and who established it, the token counts the Harness exposed, the cost those tokens price at, the elapsed time, and whether the work was routed. Prompts, responses, reasoning, diffs, file contents, terminal output and absolute paths are never copied, because the row is built by copying named fields rather than by removing unwanted ones.

The public facts this Skill reasons from — which models exist, what each supports, what each costs, and what each provider's subscriptions are called — reach it two ways. The catalogue pass asks Claude Code and Codex which models your account is offered, at which deliberation levels, and asks OpenRouter's public model list what each costs per token category, when it was released, and which Grok models there are; it starts no model and reads nothing else. Enabling this Skill on macOS installs one job into your own `launchd` account, `com.kntnt.model-selector.refresh`, that runs the pass once a day at 05:00 local time, on waking where the Mac slept through that time, and whenever the job is loaded: at Enabling itself, at each login, and when the Manager's refresh reloads a job that changed. Only the first of those runs on a given UTC day does anything. On an operating system with no scheduler adapter, `status` says the job is unsatisfied and the pass runs only when you start it. You can start it by hand at any time, from this Skill's directory, as `uv run scripts/catalogue.py refresh [--data=PATH]`, and it runs whether or not the day's pass already has. Either way one pass runs at a time, each source is given thirty seconds and the whole pass three hundred, and a pass that runs out of time keeps the facts it had; the daily pass says so in `status`, and a pass you start by hand says so in its own answer. The agent running `update` reads the providers' own pages, which is where the subscriptions are found. So the network is reached by the catalogue pass, by `update`, and by `setup` where it begins with that same reading because the catalogue has gone stale, and by nothing else at all. The catalogue pass is the one thing that reaches it unattended, and then only those three structured lists: nothing unattended runs a model or reads a page, and every other command works from what is already on disk. What either brings is validated before it is stored: an entry with nothing to attribute it to is discarded by name, a rate card in a currency other than USD or a unit other than per million tokens is refused rather than converted, a price that is neither null nor a finite, non-negative number is refused, and `capability`, a seeded prior that measurement refines, is never fetched. The prices are the ones OpenRouter publishes, per token category, never its blended average. A model missing from its maker's complete list on three consecutive days is removed from the catalogue, and every measurement row and waiting unit of it is deleted; a list that could not be read, or was read only in part, is no observation, and a model failing to run never counts. Every change the pass makes is journalled with its old and new value, and `status` shows when it last ran, what each source said, the changes of the last seven days, and every model it has removed.

Nothing waits for you. There is no queue to work through and no reminder placed where a model would read it. Disabling the Skill removes every hook it installed and the daily job, leaves every other job in your `launchd` account alone, and keeps what was measured; `reset --evidence` is the separate act that discards the measurement, and you have to ask for it by name. The one other deletion is of a model its maker no longer lists, whose own rows go when the catalogue pass removes it.

## COMMANDS

**setup**

Hold the interview and write the profile: Harnesses, the makers whose models you want, and how each maker is paid for on each channel. Run it again to review an existing profile.

**status**

Report the profile and its age, how fresh the catalogue's own facts are, when the catalogue pass last ran and what each of its sources said, the catalogue changes of the last seven days, every model the pass has removed with the three days it was missing and how many measurement rows and waiting units have been deleted for it, what has been measured, how many units wait to be graded and how long the oldest has waited, whether the judge is at its daily cap and when the cap frees, and the health of each Harness integration. It asks nothing, changes nothing, and reaches nothing.

**update**

Read the providers' own pages and adopt what they say — model lists, rate cards, and the subscriptions each provider markets — into the catalogue. The reading is the agent's; validating it, merging it and writing it is the Skill's. An entry arriving without a source it can attribute is discarded rather than stored, and a document that is not the catalogue's shape at all is refused whole.

**evidence**

Report what has been measured, grouped by kind, model and deliberation level, with the counts and dates behind each figure. An optional operand narrows it to one kind.

**objective**

Set the standing choice between time and cost that every answer asked for with no `--objective` ranks on, or, without an operand, say which is in force and whether it is your choice or the default. It survives `setup` and `update`.

**reset**

Discard the profile and the standing objective, and hold the interview again. With **--evidence**, discard what this machine measured as well. The catalogue is public fact and is kept either way.

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

What the interview settled: Harnesses, the makers whose models you want, and one payment channel per maker and Harness. It holds no list of models, every model a chosen maker offers being eligible, and no credentials. **--data** relocates it, and everything below it.

**~/.kntnt/model-selector/objective.json**

Your standing choice between time and cost, written by `objective` alone and kept apart from the profile so that `setup` and `update` leave it standing. Absent, answers rank on cost. `reset` removes it.

**~/.kntnt/model-selector/catalogue.json**

World facts written over the shipped seed by the catalogue pass and by `update` — exact model identities, family aliases, supported deliberation levels, rate cards, the slug OpenRouter routes each model by, and the subscriptions each provider markets, each carrying the address it was read from and the date it was read. The capability figures beside them are the seed's own, refined by measurement rather than by fetching.

**~/.kntnt/model-selector/catalogue-journal.jsonl**

One append-only row per change a catalogue pass made — a model added or removed, or a price, level, alias, threshold, release date or slug moved — with its old and new value, the source that said so, and when. `status` shows the rows of the last seven days.

**~/.kntnt/model-selector/refresh.json**

What the last catalogue pass did: when it ran, and for each source whether it was read completely, only in part, or not at all, with the reason, and how many changes it made.

**~/.kntnt/model-selector/refresh-marker.json**

The daily pass's own record: the UTC day it last ran, when it ended, and which bound it hit, if any — `whole-pass`, or `source:` and the name of a source. It allows the daily job one attempt a day. A pass you start by hand neither reads it nor writes it.

**~/.kntnt/model-selector/refresh.lock**

Held while a catalogue pass runs, so a second pass started meanwhile does nothing. One older than fifteen minutes was left by a process that died, and is taken over.

**~/Library/LaunchAgents/com.kntnt.model-selector.refresh.plist**

The daily job, on macOS: `uv`'s absolute path, the `PATH` of whoever installed it, 05:00 local time, and a run at load. It is written when the Skill is Enabled and deleted when it is Disabled, and **--data** does not move it: the job always runs against `~/.kntnt/model-selector/`. Editing it is pointless; the next install writes it again.

**~/.kntnt/model-selector/lifecycle.json**

Which models the catalogue pass has found missing from their maker's list, and on which consecutive days, and which it has removed: when, on which three days, and how many measurement rows and waiting units have been deleted for each so far. It masks the shipped seed's copy of a removed model, so no release of the Skill brings it back. It is catalogue state rather than measurement, and `reset --evidence` leaves it alone.

**~/.kntnt/model-selector/measurements.jsonl**

One row per measured unit of work, appended and never edited. Keyed by kind, model and deliberation level, and carrying no text from the work itself. A model's rows are deleted when the catalogue pass removes the model.

**~/.kntnt/model-selector/pending.jsonl**

Units that have been seen and not yet graded. Working state, and it goes with **--evidence** — as does the `capture/` directory beside it, which an earlier design filled with per-session drafts and nothing writes any more.

**Generated subagent definitions**

One file per Anthropic model and supported deliberation level wherever Anthropic is a maker you chose, written into the Harness's own agents directory, prefixed so they are identifiable, and rewritten by every `setup` and by every catalogue pass that changes the catalogue. Without a valid profile they are left as they are. Editing one is pointless; they are the only files this collection writes there.

## DIAGNOSTICS

An incomplete form, an unsupported combination, or an option with no work to do on the form it was given with is refused rather than ignored. The Skill names the error, prints the addressed command's SYNOPSIS, changes nothing, and points at that command's own help page. An option written after the work text is out of order and is refused the same way; a dash-prefixed word this Skill declares no option for is part of the work text.

Nothing the selection engine answers is a refusal. A missing or unusable profile, an empty catalogue and an unreachable model are each a degraded answer naming your own seat, with a note saying which it was — a caller that must be stopped is stopped by something that knows what the work is worth.

A page that says what the catalogue already held is a successful `update`. An `update` in a Harness with no web tool says so and changes nothing. A figure no measurement supports is reported absent rather than as a zero.

## EXAMPLES

**/model-selector rewrite the payment reconciliation module against the new schema**

Classify the work, then name the model and deliberation level expected to finish it for the least money, or soonest where time is your standing choice, with its nearest alternatives.

**/model-selector --scope=all --kind=design what should the retry policy be**

Consider the whole catalogue, including models this machine cannot currently reach, for a decision about what to build.

**/model-selector objective time**

Order every answer asked for with no `--objective` on how long a finished job takes, until `objective cost` sets it back.

**/model-selector evidence debug**

Report every measured group for debugging work, with the counts and dates behind each figure.

**/model-selector reset --evidence --yes**

Discard the profile and the measurement without being asked to confirm.

## INVOCATION ENVELOPE

Every form above ends with [**--** *INSTRUCTION*]. The first standalone, unquoted `--` token is the reserved separator: everything before it is the Formal Invocation and everything after it is a Contextual Instruction, natural-language guidance that may clarify or narrow choices this Skill leaves open but cannot contradict the formal input, widen the Skill, or disable a required gate.

That contract belongs to the collection rather than to this page, and it is stated once, in the Collection Library the Manager ships, at `library/references/invocation-envelope.md`: the separator's quoted and attached forms, the boundaries this guidance and applicable Conversation Context are held to, the syntax refusal a malformed Envelope or Formal Invocation takes, the distinct context refusal unusable guidance takes, what a documented precedence suppresses rather than refuses, and how guidance is passed on to a nested Skill.

## DEPENDENCIES

`uv` runs the shipped selection engine, the interview's writer, the catalogue's own reader and validator, and the capture hooks. On macOS, `launchctl` loads and unloads the job that runs the catalogue pass daily; on an operating system with no scheduler adapter, the pass runs only when started by hand. The network is reached by the catalogue pass — which starts Claude Code and Codex only to ask for their model lists, and fetches OpenRouter's public model list, and is the one thing that reaches it unattended — by `update` and by `setup`, and by nothing else; every other command works from what is already on disk. Reading a provider's page needs whatever web tool your Harness gives the agent, and where it gives none, `update` says so and changes nothing. Grading a finished unit calls one model, chosen, among those your own profile makes reachable that the measurements are confident in, as the one whose price per finished job is lowest, and stops rather than inventing a number where none can be reached.

## SEE ALSO

**/model-selector setup --help**, **/model-selector status --help**, **/model-selector evidence --help**, **/model-selector objective --help**, **/kntnt select**
