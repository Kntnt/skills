# The evaluation protocol

How a run of the [fixture corpus](corpus/README.md) against an editorial Skill is judged, what it writes down, and who is allowed to run it. The corpus supplies the material; this document supplies everything else, so that two runs made weeks apart in different provider families can be compared by reading their records rather than by re-running anything.

The decision this protocol materialises is [ADR-0178](../adr/0178-how-a-text-is-written-reviewed-and-delivered.md).

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

## The trace a criterion is answered from

A criterion answerable from the trace is answerable only from a run whose trace was kept, and a Harness does not keep one by being used. Such a run is made through a runner that preserves it — [`editorial-329/harness/run.py`](editorial-329/harness/run.py) in the GPT family, [`editorial-388/harness/staged_run.py`](editorial-388/harness/staged_run.py) in the Claude family — each keeping the session's own record and every nested agent's record beside it, with enough parent and child identity to say who ran what and in what order.

What such a trace establishes is what it recorded: a file named in a tool argument was opened, a command was submitted and answered, an agent was started by this call and by no other. It never establishes what the run's own reply says the run did. Where a trace names a set rather than a file — a glob the shell expanded, a recursive search — it says the run looked somewhere and not which file it read, and a criterion resting on that says so in its line.

A trace missing a segment is recorded as missing. The criteria it would have answered are scored from what was kept, with the gap named in the same line, or `skipped` where nothing was kept that reaches them. An incomplete trace is never read as an absence of the thing it would have shown.

## A clean control

A clean control is any corpus control whose frozen expectation is that the text is returned unchanged. That is the definition, and the controls named here are examples of it, not a complete list: the five `*-clean` rows under *Redline controls* in the [editorial-quality matrix](corpus/editorial-quality/README.md); Proofread's `clean-en-GB` in the [corpus index](corpus/README.md); and the matrix's metadata controls prepared from `article-clean` whose expectation is that the text comes back unchanged, which as the matrix stands is `metadata-none` alone, its row saying to keep valid text. The other rows of that table expect no such thing, so they owe no second run — `flag-pac` least of all, since Redline's step 8 rewrites its `kntnt` map from `abt` to `pac`. The Redline run in a Write→Redline pipeline is not a clean control either, even when it ends in a no-change status: nothing froze an expectation that the draft it was handed comes back unchanged.

A clean control is run twice against the same install, each run in a fresh session of its own and staged the way the corpus stages any run:

1. **The response-target run** uses the invocation the corpus or the wave's plan gives, with `--output=response`. It is the evidence for whether the Skill returns the short no-change status that a user who asked for the text back should get, and its before-and-after inventory is the evidence for its side effects.
2. **The file-target run** uses the same Formal Invocation with `--output=response` replaced by a new file beside the input — `--output=output.md` in the matrix — and never by the input itself, because a run whose output path is its input path is refused. It is the evidence for what the install does to the text, and its inventory is read against a file target, where the one file created beside the input is the effect that was asked for. What makes it deliver a text at all is [`delivery.md`](../../skills/kntnt/library/references/delivery.md#when-nothing-changed): an explicitly selected different file still receives the complete Text Artifact when nothing changed, and Redline and Proofread both deliver through that contract.

The criterion that the text comes back unchanged — `R1` in the editorial-quality matrix, where *a clean text is not rewritten*, and the `Reject` line of `clean-en-GB`, which rejects *any change at all from a Skill contracted to mechanics* — is judged only from the file the file-target run delivered, compared with the input that same run was staged with. Every difference between the two is evidence for the judgement, and finding none is the evidence that the text came back unchanged. Two things are never evidence for it: the Skill's own statement that it changed nothing, and an inventory showing that the digest of `input.md` did not change. The first is the run's account of itself, and the second proves only that the source was not mutated; neither shows what the run would have delivered.

Neither run is a re-run of the other, and neither outranks it. Where the two disagree — the response-target run reports no change while the file-target run delivers a changed text, say — each is recorded as it happened and judged on its own evidence. In the response-target entry, a criterion that needs the delivered text is scored `skipped` where the run returned only a no-change status, and its line gives the reason: no text was delivered, and the file-target entry answers the criterion.

The two runs are recorded as two fixture entries, one for each output target. Both carry the same `fixture` name, and their `output target` fields tell them apart.

What a no-change reply to a response target can be held to is the same for every such reply, a clean control's or not. The test for each of the five rejections is whether a `fail` could be shown from the reply's own words, the staged input and the before-and-after inventory alone, without a delivered text. Where it could, the reply can be held to that rejection; where it could not, only a delivered text answers it, and for a clean control that text is the file-target run's.

- **An unsupported fact** — cannot: a fact the run added or a caveat it dropped would exist only in a text it delivered, and a no-change reply delivers none.
- **Wrong locale behaviour** — can, in what the reply itself says: a no-change status written in a language other than the Text Artifact's is wrong locale behaviour the reply shows on its own, because `delivery.md` binds the status to the artifact's language, whereas a locale applied to the text would show only in a delivered text.
- **A substantive edit** from a Skill contracted to mechanical correction — cannot: an edit exists only in the text that carries it, and the staged input shows what the text was rather than what the run made of it.
- **An unresolved mandatory finding** — can: the staged input shows a finding the contract requires to be resolved or reported, and a reply that delivers no text and does not name that finding has delivered it as neither.
- **An incorrect side effect** — can: side effects are read from the before-and-after inventory rather than from any text, and a response-targeted run has its inventory whether or not it delivered one.

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
- **side effects** — every file created, replaced, or removed, and `none` where that is what happened. This is the half of the record that is checked rather than described, so it is written from a before-and-after filesystem inventory and not from the Skill's report of itself. The inventory covers every writable location staged for the run, including the whole working copy and any separate Harness scratch area; inspecting only the directory that holds the supplied material cannot establish that a response-targeted run left nothing elsewhere.
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
