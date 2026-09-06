---
name: model-selector
description: Choose the model and deliberation level that completes delegated work at the lowest total cost, when another Skill requires Model Selector's public select interface. Do not use implicitly for setup, status, update, evidence, or reset.
disable-model-invocation: false
argument-hint: "[--json] [--scope=limited|callable|all] [--kind=<kind>] [--data=<path>] [<work>] | setup [--data=<path>] | status [--data=<path>] | update [--force] [--data=<path>] | evidence [--data=<path>] [<kind>] | reset [--evidence] [--yes] [--data=<path>] [-- <instruction>]"
compatibility: Requires uv
metadata:
  kntnt.internal: "true"
  kntnt.binaries: "uv"
  kntnt.skills: ""
  kntnt.externals: ""
  kntnt.capabilities: ""
  kntnt.integrations: "scripts/capture.py"
---

# model-selector

Which model, at which deliberation level, finishes a piece of work for the least money — answered from what this machine has measured rather than from reputation. The answer is advice. No form of it means *start nothing*: where the profile is missing, the catalogue empty or nothing reachable, it names the seat the caller already has and says why.

`$HERE` is the directory that contains this SKILL.md, and `$MANAGER` is the Manager directory: `$HERE/../kntnt/` if it exists, else `kntnt/` under a Global harness skills directory (`~/.claude/skills`, `~/.config/opencode/skills`, or wherever another Harness keeps them). Neither found: tell the user to install the Manager (`npx skills add Kntnt/skills`) and stop. `$LIBRARY` is `$MANAGER/library/` — absent, tell the user to run `/kntnt update`, then stop.

Run `uv run "$MANAGER/scripts/kntnt.py" invoke --here="$HERE"` with the invocation payload — everything the user typed after `/model-selector`, verbatim, however many lines — on stdin. On exit 0, answer the `capabilities` in its `dependencies` first: for each one, say whether its `confirm` sentence is true of you, and where it is not, give its `how`, change nothing, and stop. Then continue from the JSON. On any other exit print its stdout verbatim and stop: it has already printed what the user is to see, and none of that text is yours to write.

In the JSON, `path` is the command path as a list, `flags` holds each flag the user wrote — `true` where it stood bare, its value where it carried one, a list of values where it was repeated — `operands` is what followed the flags, in order, and `instruction` is the Contextual Instruction, or `null`, applied as `$LIBRARY/references/invocation-envelope.md` says.

## Arguments

`<work>` describes the job in the user's own words. Where it is absent the job is the task at hand, and you write the description yourself: a sentence or two saying what is to be built, decided, found or written.

`--kind=<kind>` names the class of work, which is what an estimate is keyed on. Where it is absent you classify the work into exactly one of eight: `mechanical`, a fully specified change needing no judgement; `implement`, building to a written spec with judgement inside a fenced scope; `design`, deciding what to build at all; `debug`, finding a cause in a system that misbehaves; `review`, judging somebody else's work against a standard; `analyze`, reading a lot and reporting a little; `prose`, writing or editing text a person will read; `converse`, a short exchange with a person. There is no ninth kind, and a finer description of the job belongs in `<work>`, which is kept and reported and never splits the comparison.

`--scope=limited` admits the caller's own provider. `--scope=callable`, the default, adds every model this Harness can reach through a Bridge and the profile has a channel for. `--scope=all` admits the whole catalogue, reachable or not. Scope says what may be called, never what is preferred.

`--json` says a machine is reading the answer rather than a person.

`--data=<path>` puts the profile, the catalogue and the measurement store somewhere other than `~/.kntnt/model-selector/`. Every command takes it and every command means the same directory by it.

On `evidence`, `<kind>` narrows the account to that one kind, spelled as above.

`--force` makes `update` check every mutable source rather than only the ones the shipped cadence has made due. `--evidence` widens `reset` from the user's answers to the measurement as well. `--yes` answers the one question `reset` asks.

## The answer

This is the bare invocation. The data directory is the `--data=<path>` value where the user gave one and `~/.kntnt/model-selector/` otherwise; every command below means that directory.

Run:

    uv run "$HERE/scripts/selection.py" --kind=<kind> --scope=<scope> --harness=<harness> --seat=<model>@<level> [--data=<directory>]

The work itself is never passed in. Classifying it is your job and `--kind` is the whole of what the arithmetic reads, so nothing here writes a brief to disk or sends one anywhere.

A caller that has to classify work and cannot read this page asks for the vocabulary itself:

    uv run "$HERE/scripts/selection.py" --kinds

That prints the eight kinds and the one sentence that tells each from the others, and nothing besides. It reads no profile, no catalogue and no measurement, so it answers the same on every machine — it is there for the machine caller that has to classify the work it is about to delegate and has no business reading this Skill's data to find out what it may classify it as.

`--harness` is the Harness you are running in and `--seat` is your own model and its deliberation level. Only you know those two, and `limited` scope and the inheritance floor are both measured against them. Add `--stakes=high` where the work is irreversible or has no checker behind it, and leave it off otherwise: high stakes is what says this call is not one to experiment on, nothing standing behind it to catch a cheaper point that turned out not to do the job. Add `--repo=<path>` where a Bridge command would need a working directory. Where the user named a model or a level — in `<work>`, in the Contextual Instruction, or in whatever sent you here — pass it as `--model=<token>` or `--deliberation=<level>`: it is honoured, and where the point as stated cannot be launched the answer says exactly what differs.

With `--json`, emit the response verbatim and add nothing beside it. A machine is reading it, and every word of prose there is a word that machine has to parse past.

Without `--json`, render the same answer for a person:

- The model and the deliberation level, and how it is launched. `launch.how` is `claude-code-agent` — a generated subagent definition named by `subagent_type` — or `bridge-command`, an argv to run as a process, or `inherit`, which carries no launch argument and means the caller's own seat.
- What it is expected to cost and how likely it is to finish, from `expected`. The cost is the list value of the tokens, whoever pays for them, so a subscription seat and an API seat are one number and comparable. The chance of finishing is what decided the answer and the cost only ordered what was left: among the points the measurements say will finish the job, the cheapest was taken, and price never bought a lower chance of finishing.
- What the answer rests on, from `basis`. `measured` is this machine's own rows for exactly this kind, model and level. `pooled` is rows for that model at other kinds or levels. `prior` is the model's published capability against this kind's difficulty, with no local row behind it at all. `inherit` is nothing reachable, so the seat already in hand stands.
- The alternatives it beat, and `note` wherever it is not null.

Two identical questions can come back with different answers, and that is this working rather than failing. About one reversible call in ten is spent trying the boundary instead of taking the answer: it moves one dimension of the answer and only one — either the model or the deliberation level, never both, so that what the attempt teaches is about one variable — and takes the cheapest point one step away that its own spread says could still do the job. That is how a point with little behind it gets tried at all, and therefore the only way this machine ever learns that something cheaper would have done. `explored` names that dimension, or is null on the ordinary answer, and where it is not null `note` says what the measurements would have chosen instead. A high-stakes request, a request carrying a model or a deliberation lock, and a request naming the point that just failed are answered rather than explored.

## Setup

Read `$HERE/references/setup.md` and hold the interview it scripts: which Harnesses are covered, which providers, which of those providers' models, and then how each provider is paid for on each channel. One question at a time, nothing asked again that the user has already made unambiguous, and nothing asked that can be fetched — prices, model lists, the subscriptions a provider sells and its own positioning are all the machine's job. Show the assembled profile in full before it is written.

Hand it to the script rather than editing the file:

    uv run "$HERE/scripts/setup_apply.py" [--data=<directory>] <path-to-profile-json>

Render its report: the revision written, its `notes`, and the generated subagent definitions written and removed. Each note names an answer the catalogue could not account for — a plan it does not hold, a gateway with no rate card — and each is recorded as given rather than refused, so the user is who decides what to do about it. Where it says the definitions directory had to be created, pass that on — Claude Code reads that directory as a session starts, so those definitions reach sessions started from now on rather than this one.

## Status

Report what this Skill knows, how fresh it is and what it wants from the user. Nothing here asks a question, changes anything or reaches the network.

Read `<directory>/profile.json` and say when it was answered and which Harnesses, providers, models and payment channels it holds. Where it is absent or will not validate, say so and name `/model-selector setup`: until then every catalogue model the detected Harnesses can reach counts as enabled, which is a wider pool than anyone chose. Say the same where `answered_at` is more than ninety days old, or where the catalogue holds a provider the profile has never been asked about.

Run `uv run "$HERE/scripts/refresh.py" status --data=<directory>` and render its account of the world facts: which sources are current, which are due, and which the unattended pass has never established. This is the one surface that pass is reported on, and a reminder placed anywhere a model reads would change the thing being measured.

Run `uv run "$HERE/scripts/capture.py" status --data=<directory>` and render measurement's own health: per Harness this collection has an adapter for, whether the integration is `healthy`, `gated`, `degraded`, `absent` or `unsatisfied`; whether that Harness's finished session record can supply measurements at all; how many units are waiting to be graded; and when the grader last ran. Where `retired` is not nought, say that the directory still holds that many files an earlier design of this Skill left behind, that nothing reads them, and that `reset --evidence` is what removes them.

Close with one line on what has been measured — how many rows, over what span of dates — read from the store as `## Evidence` reads it.

## Evidence

Report what has been measured and what an answer would therefore rest on. This reads and writes nothing.

    uv run "$HERE/scripts/evidence.py" [--data=<directory>] [<kind>]

It groups the store by kind, model and deliberation, those three being the whole of a measurement's identity, and reports per group how many rows, the mean grade and who established it, the mean cost and elapsed time, and the span of instants behind them. Render that: the row count is what separates a `measured` answer from a pooled one, and `## The answer` says what those words mean. Name the authorities it reports — `checker`, `judge`, `signal`, `user` — in that order, because a grade is worth what judged it.

A figure it reports as `null` is a figure no row carries, and it is said as absent rather than as zero: an absence read as a zero is how an unmeasured configuration becomes the cheapest thing on offer. Nought rows is an empty measurement rather than an error — say that nothing has been measured yet, and that measuring happens on its own while the Skill is Enabled, as `$HERE/references/measurement.md` sets out.

## Update

Fetch what can be fetched now, in one bounded pass:

    uv run "$HERE/scripts/refresh.py" refresh --data=<directory> [--force]

Then bring the generated subagent definitions into line with whatever the pass changed, because a catalogue that gained or lost a model has changed which of them ought to exist:

    uv run "$HERE/scripts/setup_apply.py" [--data=<directory>]

With no profile operand it syncs and writes no profile. Report the definitions written and removed, and where it says the directory had to be created, pass that on as `## Setup` does.

Pass `--force` only where the user wrote it; without it the pass checks what the shipped cadence has made due. Render what it reports: every source checked, every fact that changed, and every price it discarded for arriving without a source it could attribute. A pass in which nothing changed is a successful pass. A model it discovered that the profile does not enable is written to the catalogue and left disabled, and `status` is where the user is told they may want to adopt it.

## Reset

`reset` discards the answers the user gave and leaves the interview to be held again. `reset --evidence` additionally discards what this machine measured. Neither touches the catalogue, which is public fact this Skill can fetch again.

Name the exact paths under the selected directory before anything goes, with the size of each: `profile.json` always, and with `--evidence` also `measurements.jsonl`, `pending.jsonl`, the `capture/` directory, and whatever an earlier design of this Skill left in the directory. Get the counts for all but the first from `uv run "$HERE/scripts/capture.py" purge --data=<directory>` without `--yes`, which reports rather than removes; a path the directory does not hold is reported absent rather than as a failure, and the preview lists those absent paths so that the user can see the whole of what this verb knows about.

Obtain confirmation the way every destructive act in this collection does, or read it from a supplied `--yes`. A declined confirmation writes nothing. Confirmed, remove `profile.json`; with `--evidence`, also remove `measurements.jsonl` and run the same purge again as `purge --yes --data=<directory>`. Report what went, per path, by the count of rows or bytes the preview named — nothing here is migrated, backfilled or reinterpreted.

Say two things afterwards. The Harness hooks stay installed and keep measuring: discarding a measurement is not switching measurement off, and switching it off is unchecking this Skill in `/kntnt select`. And the generated subagent definitions are left where they are until the next `setup` rewrites the set.
