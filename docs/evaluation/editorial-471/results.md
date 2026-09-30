# Results for #471: a brief is a direction, and follows the template of twelve questions

Measured on 2026-09-30, between 17:44 and 18:03 UTC, in Claude Code 2.1.285 on `claude-opus-5-5` at high deliberation, as every packet's `trace-index.json` records for the session and every nested agent; every judge a fresh `kntnt-opus-high` subagent. The method is [`plan.md`](plan.md), frozen in the first candidate's commit before the first run.

## The two candidates

- **`6b426730`**, the first candidate: the rewritten `writing-brief.md`, Brief's `SKILL.md` and `help.md`, the count-free surfaces, their tests, the catalog, and the runner's extension. All eight planned runs were staged from it; the three Write runs took the briefs its Brief runs delivered.
- **`761663b7`**, the revised candidate, the evaluation's one revise round. In `SKILL.md` it makes the chain check name the question that would resolve a *partly* or a *no* once, as a suggestion rather than a new follow-up, and take a confirmation or a move on as the answer; it says that the check gives the angle, the message and the conclusion no new allowance; and it tells a draft to mark a condition, a boundary or a choice it proposes, or takes from the genre rather than the material, as `[SUGGESTED: …]`. The three Brief runs that missed were run again from it, as `revise-interview-sv`, `revise-interview-en` and `revise-draft`.

**The revised candidate ships** (the plan's exit 2): over the re-run subset it has no miss, where the first candidate had three.

## Per run

A judged criterion is met only where both judges pass it. `T1` and `O1` were read by this session: `T1` from each packet's `trace-index.json` and the commands it records, `O1` from `filesystem-changes.json`. `G1` and `G2` concern the repository, not a run: every judge scored them `skipped`, and this session checked them against the candidate (below).

| Run | Staged from | Delivered | `B1` | `B2` | `B3` | `B4` | `B5` | `B6` | `B7` | `B8` | `B9` | `B10` | `F1` | `T1` | `O1` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `interview-sv` | `6b426730` | `brief.md`, 14 turns | met | met | met | **missed** (A fail, B fail) | met | met | met | met | met | n/a | met | met, `techniques/abt.md` | met |
| `interview-en` | `6b426730` | `brief.md`, 14 turns | met | met | met | **missed** (A fail, B fail) | met | met | met | met | met | n/a | met | met, `techniques/pac.md` | met |
| `draft` | `6b426730` | `brief.md` | met | met | met | met | met | met | **missed** (A pass, B fail) | met | met | met | met | met, `genres/pressrelease.md` | met |
| `review-new` | `6b426730` | `brief.md` | met | met | met | met | met | met | met | met | met | met | met | — | met |
| `review-old` | `6b426730` | `brief.md` | met | met | met | met | met | met | met | met | met | met | met | — | met |
| `revise-interview-sv` | `761663b7` | `brief.md`, 14 turns | met | met | met | met | met | met | met | met | met | n/a | met | met, `techniques/abt.md` | met |
| `revise-interview-en` | `761663b7` | `brief.md`, 14 turns | met | met | met | met | met | met | met | met | met | n/a | met | met, `techniques/pac.md` | met |
| `revise-draft` | `761663b7` | `brief.md` | met | met | met | met | met | met | met | met | met | met | met | met, `genres/pressrelease.md` | met |

| Run | Staged from | Brief taken from | Delivered | `W1` | `W2` | `O1` |
| --- | --- | --- | --- | --- | --- | --- |
| `write-interview` | `6b426730` | `interview-sv` | `draft.md`, with known defects named | met | missed on both judges, recorded under #376 | met |
| `write-draft` | `6b426730` | `draft` | `draft.md` | met | met | met |
| `write-review` | `6b426730` | `review-new` | `draft.md` | met | met | met |

### The three first-candidate misses

- **`B4` in both interviews.** Each interview's chain check found an inconsistency the answers did not settle: in `interview-sv`, a conclusion without the hook's *often*; in `interview-en`, a message saying the coordinators fix the overruns *themselves* beside an effect that needs the board's approval. Each asked about it at the check, asked again when the next turn confirmed the check without settling it, and asked a third time in the delivery account, after the conclusion's or the message's one follow-up had been spent. Both judges counted these as follow-ups beyond the allowance. The revised runs raised nothing twice: each interview asked one follow-up on the angle and one on the conclusion (Swedish), or one on the message (English), and took the confirmation as the answer.
- **`B7` in the draft.** Judge B found a condition of the Skill's own, *the ten-year claim is used only if confirmed*, written unmarked into a sketch step and into question 8, and judge A noted the genre-derived *the hook is the news* likewise unmarked but passed. The revised draft marks what the material does not carry, both judges agreeing.

### `T1`, from the trace

Every run that sketched read the resource its choice names, by a `cat` of that one file recorded in its trace: `interview-sv` and `revise-interview-sv` read `techniques/abt.md` (with `genres/article.md`), `interview-en` and `revise-interview-en` read `genres/report.md` and then `techniques/pac.md` for the report's own form, and `draft` and `revise-draft` read `genres/pressrelease.md`. No run read `article-anatomy.md`, `web-craft.md` or `headlines.md`; where those names occur in a trace, they occur inside the text of a genre file the run read. `review-old` also read `techniques/abt.md`, its brief's technique, though a review sketches nothing.

### `G1` and `G2`, from the repository

At `761663b7`, no file under `skills/` contains `docs.google.com`, and `writing-brief.md`'s question 3 says the message *need not appear in the text* while question 9 says the conclusion *carries the message*, and question 11's chain check asks *does it carry the message*. `tests/test_brief.py` holds all three.

### `O1`

In every run `filesystem-changes.json` shows exactly one file created outside the Harness's own files under the run's `HOME`: `work/brief.md` for a Brief run and `work/draft.md` for a Write run, the file the output target named. Nothing was changed or removed, the material was left unchanged, and the private root was removed (`cleanup.json`). The build's working tree read the same before and after the waves.

## What the runs show beyond the criteria

- **Readiness.** Every run's statement on whether the brief is enough to write agreed with both judges' own application of the rule. The two interviews, their revisions and `review-new` are enough to write with open research questions listed; `review-new` counts question 1 answered though its search phrase is missing. The drafts are not, their angle, message and conclusion being unconfirmed suggestions, and `review-old` is not, its question 3 being unanswered.
- **The older template.** `review-old` mapped the old *message* to question 9's conclusion, left question 3 unanswered, read the `[WEAK: …]` answer as an answer, reported the missing chain check as missing and proposed none. Both judges noted two parts left without a marker — question 4's *why now* and question 10's *way there* — and judge A that question 7 is called answered while its sentence and sketch are missing; neither judge failed a criterion on them.
- **Metadata.** Every map held the values both judges expected: `article`/`abt`/`sv`; `report`/`en_GB` with no technique for the report's own form, and no second language for the translation; `pressrelease`/`sv` with no technique; `webcopy`/`none`/`en_GB`; `casestudy`/`abt`/`sv`.
- **No evidence demanded.** No run marked a claim unsubstantiated or asked for a link as a condition. Judges called the revised draft's *should be checked* on the remembered ten-year figure, and the Swedish interview's rendering of the template's *link where you can*, close calls and passed them.

## `write-interview`'s `W2`

Both judges failed `W2`: the draft states the drying and wiping steps in a fixed order, which the brief gave only as examples with the order left open, and it carries the byline *Av Thomas*. The run's own account names the steps as known defects its final source comparison found, with the checker's repair, and delivers them disclosed, which is the shape `editorial-364` assigned to [#376](https://github.com/Kntnt/skills/issues/376); it is recorded under that number and not counted here, as `editorial-473` did. The byline is the article anatomy's own rule, *when it names none, the author is the user*, which the judges were not given; the reply says where the name came from and asks for it to be corrected. The brief it was given carries the steps as `till exempel`, so the miss does not follow from the brief.

## What is filed

Nothing. The three first-candidate misses are repaired in the revised candidate, which ships, and its runs left no miss; `write-interview`'s is #376's.

## Void judgements

The first two judges of `revise-draft` were given a directory without `work/notes.md`, a staging error of this session's, and could not check `F1` against the material. Their judgements are kept under [`voided/revise-draft-judges-without-material/`](voided/revise-draft-judges-without-material/), and two fresh judges judged the run from a complete directory. `runs/judges.tsv` records all four tokens.

## Decision record

None. The template and the Skill's new spirit are the maintainer's ruling, recorded in the ticket, and `writing-brief.md`, Brief's `SKILL.md` and the editorial README carry the rules where the next author reads them. ADR number `0231`, reserved for this ticket, is unused.
