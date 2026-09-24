# Results for #399

Ten runs of the control `case-study-clean`, five against each install, run on 2026-09-24 against the method [`plan.md`](plan.md) froze before the first run. Artefacts: `runs/`. The record is [`../records/redline-claude-2026-09-24-399.md`](../records/redline-claude-2026-09-24-399.md).

**What the measurement shows: the second outcome.** Measured on `claude-opus-5-5`, the post-change install missed `C1` in one of its five runs and the pre-change install in one of its five. Both counts fall in the minority band, both arms missed at least once, and the post-change count is not below the pre-change count, so the pair 1 / 1 is the second outcome the plan fixed in advance. The miss belongs to the headline contract's authority over a subheading that already conforms, which is the territory of [#397](https://github.com/Kntnt/skills/issues/397) and [#400](https://github.com/Kntnt/skills/issues/400), and not to the six files #383 changed. #383's miss on `claude-opus-5` is not re-tested.

## The two installs and the mapping

| Run | Install | Returned |
| --- | --- | --- |
| `case-study-clean-01` | pre-change, `3167fb68` | no-change status |
| `case-study-clean-02` | post-change, `5af1390d` | no-change status |
| `case-study-clean-03` | pre-change, `3167fb68` | no-change status |
| `case-study-clean-04` | post-change, `5af1390d` | no-change status |
| `case-study-clean-05` | pre-change, `3167fb68` | no-change status |
| `case-study-clean-06` | post-change, `5af1390d` | no-change status |
| `case-study-clean-07` | pre-change, `3167fb68` | no-change status |
| `case-study-clean-08` | post-change, `5af1390d` | two subheadings rewritten |
| `case-study-clean-09` | pre-change, `3167fb68` | one subheading rewritten |
| `case-study-clean-10` | post-change, `5af1390d` | no-change status |

Both installs were staged as the plan says, 84 files each, differing in Redline's `SKILL.md`, `help.md` and `references/correction.md`, the Library's `anti-slop.md` and `base.review.md`, `kntnt/catalog.json`, and Unslop's three files, which Redline does not load. Every run's before-and-after inventory carries the same install digest before and after: `d151c9e6…` for every pre-change run and `ac26123b…` for every post-change run.

## How the runs were launched

The plan names each run a fresh `kntnt-opus-high` subagent. The first dispatch of `case-study-clean-01`, at 00:28 UTC, was made as a subagent of this session and came back refused: Redline's Capability check found that the run could start no subagent of its own, and none of its tools could. A second probe confirmed it: a subagent this session starts is given no tool that starts a further agent. #383's runs, which did start correction subagents, were dispatched from a session that could give them that tool; this session is itself a subagent, one level further down. That attempt reviewed nothing, is void, and is kept under [`runs/void/case-study-clean-01-attempt-1/`](runs/void/case-study-clean-01-attempt-1/), with its wave inventories beside it in `runs/void/`.

Every counted run was therefore made as a fresh top-level Claude Code session running the `kntnt-opus-high` agent definition, started by [`runs/launch.py`](runs/launch.py) with these options, [`runs/sessions.json`](runs/sessions.json) holding the argument vector exactly as it was passed:

```text
claude --print --agent=kntnt-opus-high --model=claude-opus-5-5 --effort=high --dangerously-skip-permissions --strict-mcp-config --output-format=stream-json --verbose
```

in the run's `work/` directory, with the dispatch message the plan specifies — the turn file's text followed by the three lines naming the working directory, the run directory and the invocation — on stdin, and nothing else. The copy in `runs/` is the launcher as it ran, with its imports split and its layout set by the repository's linter and formatter; nothing it does changed. That is the same seat, the same freshness and the same message; what changed is only that the run is a session of its own rather than a subagent, which is what lets it start the correction subagent Redline requires. [`runs/sessions.json`](runs/sessions.json) records for each run the argument vector, the digest of the prompt, the Claude Code version (2.1.281), the session's model (`claude-opus-5-5` in all ten), whether a subagent tool was available (it was in all ten), which subagents the run started, and the models its usage names. The session transcripts themselves were kept in this ticket's scratch directory and are not part of this record: no criterion here is answered from a Harness trace.

Two runs started a correction subagent. `case-study-clean-08` started a `kntnt-opus-high` subagent, which ran `claude-opus-5-5`. `case-study-clean-09` started a `general-purpose` subagent, which inherits the session's model; its usage names only `claude-opus-5-5`, and at what deliberation it ran is not in what this evaluation kept. In every run the nested Proofread pass was followed from the staged `proofread/SKILL.md` inside the run's own session, as in #383.

Judges were fresh `kntnt-opus-high` subagents of this session, which launch `claude-opus-5-5` at high deliberation; a judge starts no agent, so the nesting limit does not reach them. All twenty were dispatched after the tenth run, eight at a time at most, each with the dispatch message in [`runs/judge-dispatch.md`](runs/judge-dispatch.md) — the control brief byte for byte, the judge's letter, the run's scratch path, the **Frozen expectation** paragraph and the path of `expectation.md` — and each wrote its judgement into the run directory before the directory was copied here. No judgement was voided.

## Per run

`R1` is each judge's verdict under heading 4 of the control brief. A run misses `C1` where either judge fails `R1`. `A1` and `A2` are derived from the judges' *Differences* and *The account* by #383's rules and are recorded on post-change runs only; on pre-change runs they are `skipped`, because #383's plan defines them on post-change runs only and `A1` tests a closing summary the pre-change product does not have.

| Run | Arm | `R1` A / B | `C1` | `A1` | `A2` | `O1` | `S1` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `case-study-clean-01` | pre | pass / pass | met | skipped | skipped | pass | pass |
| `case-study-clean-02` | post | pass / pass | met | pass | pass | pass | pass |
| `case-study-clean-03` | pre | pass / pass | met | skipped | skipped | pass | pass |
| `case-study-clean-04` | post | pass / pass | met | pass | pass | pass | pass |
| `case-study-clean-05` | pre | pass / pass | met | skipped | skipped | pass | pass |
| `case-study-clean-06` | post | pass / pass | met | pass | pass | pass | pass |
| `case-study-clean-07` | pre | pass / pass | met | skipped | skipped | pass | pass |
| `case-study-clean-08` | post | **fail / fail** | **missed** | **fail** | **fail** | pass | pass |
| `case-study-clean-09` | pre | **fail / fail** | **missed** | skipped | skipped | pass | pass |
| `case-study-clean-10` | post | pass / pass | met | pass | pass | pass | pass |

No run split its judges on `R1`, and none split on `A2`.

**The eight runs that met `C1`** each returned the short no-change status, in Swedish, reporting no finding: for example `Ingen ändring behövdes. Texten följer kraven för genren kundcase på svenska …` (`01`) and `Texten behövde inga ändringar. Granskningen mot genren kundcase på svenska gav inga fynd …` (`02`). All sixteen judgements find no difference, every preservation clause met and every named rejection avoided. On the four post-change runs among them, `A1` holds because there is no difference to count, and `A2` holds on both judges: each finds the no-change statement accurate and nothing left uncovered.

**`case-study-clean-08`, post-change — missed.** Two differences, both paratext:

- `## Två perioder med olika arbetsbelastning` (39 characters) became `## Mediantiden sjönk till två arbetsdagar, men belastningen skilde sig` (67). Both judges class it as a change of taste; both add that it changes the heading's meaning, putting the result before the caveat, and that it leaves the 36–39-character band the expectation records the text as meeting. The reply's finding 1 gives the reason as `Rubriken … saknade verb. Den nämnde bara förbehållet och inte vad avsnittet redovisar.`
- `## Kunden vill ge förberedelserna mer tid` (38) became `## Maya Lind vill ge förberedelserna mer tid` (41). Both judges class it as a change to what a claim says, in attribution — judge B adds scope — and both call it defensible but not the repair of a visible defect. The reply reports it as finding 2 and again as a changed claim.
- `R1` fails on both: *clean texts may not be rewritten to satisfy taste*, decided on finding 1.
- `A1` **fails**: both judges class the section 2 subheading rewrite as a change of taste, which is the first limb of #383's counting rule.
- `A2` **fails** on both judges. Judge A finds `alla räknade krav i artikelanatomin är uppfyllda` false against the returned text, reading the expectation's 36–39-character band as the limit, and finds the length change left out of the account. Judge B finds the reply's reason `ett namn som brödtexten aldrig inför` inaccurate, the body introducing the customer as `Kundcaset`, and the length change and the shift of emphasis left out of the account; B records the anatomy statement as unverified rather than false. **An evaluator's note, which changes no verdict:** the staged `article-anatomy.md` sets the subheading limit at *at most 70 characters*, so `alla räknade krav … är uppfyllda` is true against the resource the run measured with. The judges were handed no measured figure, as in #383, which declared that limit of the control brief.

**`case-study-clean-09`, pre-change — missed.** One difference: `## Två perioder med olika arbetsbelastning` (39) became `## Mediantiden till tilldelning sjönk från tre arbetsdagar till två` (64), on the finding that the heading `saknade verb och sa inte vad avsnittet visar`. Judge A classes it as a change to what a claim says, in causality and certainty; judge B as a change of taste that also moves causality and scope. Both read the new heading as stating the result without its caveat in a supplier-published case. Both fail `R1` on the same clause. Both also find the account complete and accurate: the run reported its own repair as having created a finding it could not resolve — `Den nya mellanrubriken … ger resultatet utan dess förbehåll`, *unresolved, arisen through the correction*, with the budget spent — and listed the caveat's removal from the heading among the changed claims.

## Reading the result

| Arm | `C1` misses | Band |
| --- | --- | --- |
| pre-change, `3167fb68` | 1 of 5 (`09`) | minority |
| post-change, `5af1390d` | 1 of 5 (`08`) | minority |

The plan fixed four readings before any run. The first outcome needs the post-change arm in the majority band (4 or 5) and the pre-change arm in the minority band; the post-change arm has 1, so it does not hold. The third needs 0 and 0; both arms have 1, so it does not hold. The second needs both arms to miss at least once, both counts in one band, and the post-change count at least the pre-change count; 1 / 1 is exactly that, so **the second outcome holds**, and nothing is inconclusive.

**The reasoning.** The pre-change install makes the miss #383 recorded against the post-change install, on the same subheading, for the same stated reason: #383's post-change reply gave `från en nominalfras utan verb till en sats som säger vad avsnittet säger`, and here run `09`, pre-change, gives `saknade verb och sa inte vad avsnittet visar` and run `08`, post-change, gives `saknade verb`. None of #383's six files is needed to produce it, because the install that lacks all six produces it too, and at the same rate within what five runs can show. What produces it is a review that treats a verbless subheading, or one that names a section's caveat instead of its result, as a defect in a text the corpus freezes as conforming — a judgement the headline contract makes about paratext, not one the trace check, the closing summary or the catalogue guard makes. The miss belongs to the headline contract's authority over a subheading that already conforms: #397 carries paratext authored into a finished text, and #400 a paratext change accounted for as something else, which is the shape of run `08`'s account giving a taste rewrite as a defect repaired. No ticket is filed, as the plan fixes for this outcome.

**What this does not establish.** Five runs per arm show that both installs miss occasionally, not the rate at which either does: 1 / 1 is the smallest pair the second outcome admits, and a pair of 0 / 1 or 1 / 0 would have read differently. The measurement is on `claude-opus-5-5`, and #383's miss on `claude-opus-5` is not re-tested. And the eight passes rest on a no-change status, which the next section qualifies.

## A declared limit: the clean-control rule landed after this staging was fixed

[`../protocol.md`](../protocol.md)'s section *A clean control*, added by [#404](https://github.com/Kntnt/skills/issues/404) on 2026-09-23 after this ticket's staging was settled against `c8c03eb1`, runs a clean control twice — once to the response and once to a file beside the input — and judges the criterion that the text comes back unchanged only from the file the file-target run delivered, never from the Skill's own statement that it changed nothing. This ticket fixes its matrix at ten response-target runs staged byte for byte from #383, with no extra runs on any outcome, and asks for both judges' `R1` recorded on every run; that is what was run and recorded.

So in the eight runs that returned the no-change status, the judges' `pass` on `R1` rests on the run's own statement that nothing changed, which the protocol does not count as evidence that the text would come back unchanged. The two misses are observed rewrites in a delivered text and stand on their own evidence. Scored strictly by the protocol, the eight response-target `R1` lines would be `skipped` with the file-target run named as what answers them, and no file-target run was made; that would leave each arm with one answerable run, which none of the four readings is defined over. The reading above is the one this ticket's criteria define, and this limit is stated beside it rather than folded into it.

## Side effects

`O1` — met on all ten counted runs, and `S1` with it. In every run the staged install's digest is identical before and after, `work/input.md` is unchanged (`32037623…`), and the run directory's only new file is the evaluator's `response.md`; every `work/` held `input.md` and nothing else when the turn was dispatched. `case-study-clean-05` left one empty directory behind, `scratch/`, in the run directory — the one place the turn allowed scratch — holding no file; a file inventory does not see an empty directory, it is stated here, and it was not carried into this tree. No other `scratch/` survived a run.

Scopes 3 and 4 were taken around every run into `runs/wave-NN-{before,after}-{scratch,repo}.txt`. Across all ten, the scratch root changed only by the run's own directory and the evaluator's files — its logs and the session transcript `launch.py` writes under `evaluator/streams/`. Neither checkout's `git status` changed apart from the evaluator's wave files in this worktree, and both stayed at `20133068`.

**The sibling and #401.** The shared lock `kntnt-orchestrate-runB-locks/case-study-clean` was taken before each run and removed as soon as its reply arrived. It was never found held: the void attempt and all ten runs took it at the first try. It was retaken within seconds of each release, so a sibling polling every 30 seconds may have waited until this evaluation's last run ended at 01:06 UTC. Because every run was a top-level session of its own, each run's correction subagent wrote under a session directory named for that run's working directory and session, not the scratchpad the sibling's subagents share; no file of the sibling's appears in any inventory here, no run reported a file changed under it, and nothing needed attributing.

## `T1`, `R2` and the rest

`T1` and `R2` are recorded `skipped` on every run: both are answerable only from a Harness trace, and #383's plan, whose method this one re-uses, answers neither. Every other criterion the corpus applies to a run of this kind — `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2`, `N1`, `N2`, `C2` — is recorded `skipped`, not being this evaluation's.

No revise round was run, no run beyond the ten counted was made apart from the voided first attempt, no decision record is written, and nothing shipped changes. `../corpus/editorial-quality/README.md` and `../editorial-383/runs/control-case-study-clean/expectation.md` are untouched.
