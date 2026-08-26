# The evaluation protocol

How a run of the [fixture corpus](corpus/README.md) against an editorial Skill is judged, what it writes down, and who is allowed to run it. The corpus supplies the material; this document supplies everything else, so that two runs made weeks apart in different provider families can be compared by reading their records rather than by re-running anything.

The decision this protocol materialises is [ADR-0093](../adr/0093-one-corpus-evaluated-separately-inside-each-provider-family.md).

## What an evaluation is

An evaluation runs the corpus against one Skill, as a user of that Skill would, in a real supported Harness. It is not a pytest suite and produces no assertions about sentences. It produces records: one per fixture run, in the format below, saying what was invoked, what came back, what happened on disk, and how each criterion was judged.

An evaluation asserts nothing about exact prose and makes no claim that a model writes perfectly or finds every error. Where it finds a real defect, the defect is written down as its own ticket against the Skill. It is never absorbed by softening a criterion or editing the corpus, which would leave the wave with a corpus that describes what was built instead of what was specified.

## Blinded semantic judging

A criterion is normally a question answerable from the delivered artifact and the recorded side effects alone. Where a contract governs loading and its observance cannot be inferred from either, the criterion is answerable from the recorded Harness trace instead. Judging remains blinded: the judgement is made against criteria fixed before the run, from what the run produced, and not from knowing which model produced it, not by comparison with another family's record, and not by comparison with a reference text somebody wrote earlier. Where the evaluator is also the judge — which it usually is — every fixture is judged before any other family's record is opened.

Several valid texts pass. Two drafts from the same brief may share no sentence and both be correct, and a criterion that would separate them on wording is a criterion written wrongly. What a criterion tests is whether the contract held.

Five things fail regardless of how well the output reads, and no criterion may be written that would let one of them pass:

- **An unsupported fact** — a claim, number, attribution, certainty, scope, chronology, or causal link that the supplied material does not carry. A caveat the source states and the output drops belongs here too: dropping it asserts a confidence the material refuses.
- **Wrong locale behaviour** — mechanics, spelling, punctuation, or date and number conventions applied for a locale other than the resolved one, and valid forms of the resolved locale treated as errors.
- **A substantive edit** from a Skill contracted to mechanical correction — wording, meaning, tone, structure, facts, formatting, code, or metadata changed by a pass that was asked only to correct mechanics, including changes that improve the text.
- **An unresolved mandatory finding** — a finding the contract requires to be resolved or reported, delivered as neither. A finding the run could not resolve is a pass when it is reported with the artifact and a failure when it disappears.
- **An incorrect side effect** — a file created, replaced, moved, or removed where the output contract does not allow it; a partial effect left behind after a refusal; a permission changed to make a forbidden write possible; a source mutated without the explicit authorisation the contract requires.

A criterion may be judged `skipped`, and a skipped criterion says why in the same line. A fixture not run is recorded as skipped with its reason rather than left out of the record, because a record silently missing a fixture reads later as a fixture that passed.

## The recording format

One record per evaluation, holding one entry per fixture run. [`record-template.md`](record-template.md) is the skeleton; records live in [`records/`](records/README.md) and are named `<skill>-<provider-family>-<YYYY-MM-DD>.md`. Where a re-run lands on the same date as the record it follows, the name takes the issue it was run for after the date, because the convention above has nowhere else to put two records of one Skill and one family on one day.

The record's own header carries the identity of the run:

- **record** — the record's own name, matching its filename.
- **date** — the date the run was made, ISO 8601.
- **ticket** — the issue the run was made for.
- **skill** — the Skill under evaluation.
- **provider family** — `claude` or `gpt`. One family per record, and never both.
- **model** — the exact model the Harness ran, as the Harness names it.
- **harness** — the Harness the run happened in, with its version where it exposes one.
- **corpus commit** — the short commit of this repository the corpus was taken from. Two records are comparable only where this matches.

Each fixture entry carries what was asked and what happened:

- **fixture** — the fixture's name from the corpus index.
- **invocation** — the Formal Invocation as it was actually typed, verbatim.
- **contextual instruction** — any natural-language guidance supplied beside it, verbatim, or `none`.
- **output target** — where the result was directed, or `response`.
- **observed delivery** — what came back and where it landed, in a sentence. Not the text itself.
- **side effects** — every file created, replaced, or removed, and `none` where that is what happened. This is the half of the record that is checked rather than described, so it is written from the filesystem and not from the Skill's report of itself.
- **criteria** — one line per criterion: its identifier, `pass`, `fail`, or `skipped`, and one sentence of evidence. A `fail` names which of the five rejections it is.
- **unresolved findings** — findings delivered with the artifact and left unresolved, or `none`.
- **defects filed** — the issue numbers opened for defects this fixture exposed, or `none`.
- **notes** — anything a later reader of this record needs and the fields above do not hold.

Records are append-only in practice. A re-run is a new record, and the earlier one stays: what a configuration did on a given day is history, and a later repair does not change it.

## Provider isolation

This is a hard constraint on whoever runs an evaluation, and it holds in both directions.

**A Codex session runs only GPT-family evaluations.** It does not start, control, or invoke a Claude Harness or a Claude model, directly or through any tool, script, or subagent.

**A Claude session runs only Claude-family evaluations.** It does not start, control, or invoke a Codex Harness or a GPT model, directly or through any tool, script, or subagent.

The shared corpus is therefore run in separate provider-native sessions, and the families are compared afterwards by reading the records. No cross-provider orchestration exists in the corpus, in this protocol, or in any tooling around them, and none is to be added: a comparison is made by a person reading two records, which is why the recording format above is worth having at all.

A record names one provider family. A run that would need both is two runs.
