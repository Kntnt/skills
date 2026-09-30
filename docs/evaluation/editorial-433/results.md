# Results for #433

The pre-change arm, run on 2026-09-30 against the method [`plan.md`](plan.md) froze at `fc45e604` before the first run. Artefacts: `runs/`. The record is [`../records/redline-claude-2026-09-30-433.md`](../records/redline-claude-2026-09-30-433.md), and the decision record is [ADR-0225](../../adr/0225-a-correction-rounds-repeating-heading-is-measured-first-and-not-reproduced.md).

Six Redline invocations, all staged from `<start>` `2afeb95e`, the tree #429 leaves: `opinion-flawed` three times, and `article-flawed`, `case-study-flawed` and `column-flawed` once each. Every run was a fresh top-level Claude Code 2.1.285 session made by [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py) through [`runs/wave.sh`](runs/wave.sh), and every session and its one correction subagent ran on `claude-opus-5-5` at high deliberation, which each packet's `trace-index.json` records. Every run completed with exit 0; none was cut off, so `voided/` does not exist. Each run had two blind `kntnt-opus-high` judges on [`control-judge-brief.md`](control-judge-brief.md), with the row's frozen cell at `2afeb95e` as the **Frozen expectation**; `runs/judges.tsv` maps each judge's neutral directory to its run, and every directory was removed once its judgement was copied.

**The headline result. Not reproduced.** Two of the three pre-change `opinion-flawed` runs deliver the ending by the plan's check: the returned text ends in a section of its own that holds the closing call, and the call names kommunstyrelsen and keeping telephone booking. More than half of the arm delivers it, so the not-reproduced gate holds. As the plan settles for this outcome, no candidate was committed, the candidate arm was not run, and nothing under `skills/` or `tests/` changed. The one run that lost the ending lost it with a round rejected for an attribution shift, not for a heading repeating what it stands over, and no run of the arm returned a round rejected for such a heading. Every control met `C1`. Nothing is filed.

## The wave inventories

`runs/wave-<n>-{before,after}-*.txt` bracket the three waves. Wave 1 held the three controls and the first `opinion-flawed` run; waves 2 and 3 held one `opinion-flawed` run each. Between them:

- **Scope 3**, this build's scratch root, gains the runs' packets and logs, the judges' directories, and `draft/`, a draft the dispatching session wrote while the arm ran and never committed.
- **Scope 4** shows this working tree gaining `runs/judges.tsv` and the inventory files themselves, and the main checkout's `HEAD` moving from `2afeb95e` to `ae4fd1c9` during wave 2 as the run integrated another ticket.
- **Scope 5** shows the orchestrator's own files appearing under the session scratchpad's `own/`, named for #447.

None is attributable to a run, and every run's own inventories show nothing outside its private root apart from what `O1` below records.

## When a run delivers the ending

The plan's check, made by the dispatching session from the text in each reply's fenced block. The input's sections are `## Bakgrund` and `## Diskussion`, and its closing line is `Nu är det dags att agera.` inside `## Diskussion`.

### `pre-control-opinion-flawed-1` — does not deliver

The round was rejected whole and the text returned as received. Its last section, quoted in full:

```markdown
## Diskussion

Förvaltningen invänder att dubbla kanaler innebär dubbel administration. Handlingarna saknar tidsmätning. Därför kostar det ingenting att behålla telefonbokningen. Föreningen vill att förvaltningen mäter tidsåtgång och frågar användarna varför de väljer en bokningsväg. Försökets kostnad är inte beräknad.

Nu är det dags att agera.
```

1. **Last section new** — not met: the last section is the input's `## Diskussion`.
2. **Closing call in the last section, and in no earlier one** — not met: the closing line is still the last line of the section that carries the argument.
3. **Actor and act** — not met: `Nu är det dags att agera.` names neither.

The judges, heading 3, on *Existing action/actor in body can repair the ending*:

- judge a: *"Detected, not applied. Finding 9 names the route … The one attempt at it was discarded, though, so the returned text still ends on "Nu är det dags att agera.""*
- judge b: *"Recognised but not applied. … So the reply names the repair route, but the delivered text is not repaired."*

Check and judges agree.

**What lost it.** The reply's account of the rejected round: the new headline `Behåll telefonbokningen på försök och mät tidsåtgången` and the new ending both put *Föreningen*'s demand to measure time use in the writer's own voice, and the re-review established that as a defect the round created. The rejected round's text is not in the committed packet, whose transcripts are kept out as the plan says; the reply's description is what the packet holds. No open ticket owns a round rejected for a claim moved from an attributed party into the writer's voice, so the miss is recorded here without an owner, and it counts as not delivering, as the plan says every run counts.

### `pre-control-opinion-flawed-2` — delivers

The last section, quoted in full:

```markdown
## Nästa steg är ett halvårs försök

Nu är det dags att agera. Kommunstyrelsen bör besluta att behålla telefonbokningen under ett halvårs försök i alla sju lokaler.
```

1. **Last section new** — met: `## Nästa steg är ett halvårs försök` is not in the input. The paragraph that stood under `## Diskussion` stands in the section before it, under the rewritten heading `## Handlingarna visar inte vad dubbla kanaler kostar i tid`.
2. **Closing call in the last section, and in no earlier one** — met: `Nu är det dags att agera.` opens the last section and stands in no earlier one.
3. **Actor and act** — met: *Kommunstyrelsen bör besluta att behålla telefonbokningen*.

The judges, heading 3:

- judge a: *"An action and actor already in the body can repair the ending: done. The new ending is "Kommunstyrelsen bör besluta att behålla telefonbokningen under ett halvårs försök i alla sju lokaler." Its actor and act come from the opening sentence, and nothing new is invented."*
- judge b: *"The existing action and actor can repair the ending: met. The run used the text's own proposal and its actor, and invented nothing."*

Check and judges agree.

### `pre-control-opinion-flawed-3` — delivers

The last section, quoted in full:

```markdown
## Både kommunstyrelsen och förvaltningen behöver agera

Kommunstyrelsen bör behålla telefonbokningen under ett halvårs försök i alla sju lokaler. Förvaltningen bör mäta tidsåtgången och fråga användarna varför de väljer en bokningsväg.
```

1. **Last section new** — met: `## Både kommunstyrelsen och förvaltningen behöver agera` is not in the input. The paragraph that stood under `## Diskussion` stands in the section before it, under the rewritten heading `## Handlingarna mäter inte tiden för dubbel administration`.
2. **Closing call in the last section, and in no earlier one** — met: the input's closing line was replaced by the repaired call, and it stands in no earlier section.
3. **Actor and act** — met: *Kommunstyrelsen bör behålla telefonbokningen*.

The judges, heading 3:

- judge a: *"An action and actor already in the body can repair the ending: used. The new ending takes the proposal ("Kommunstyrelsen bör behålla telefonbokningen ...") and the measurement demand ("Förvaltningen bör mäta tidsåtgången ...") from the body. The attribution shift is reported."*
- judge b: *"The ending may be repaired with an action and actor already in the body: done. The new ending uses the body's own proposal and Kommunstyrelsen, together with the Föreningen's demand that förvaltningen measure time use and ask users. It adds no new facts. The shift in attribution (D9) is disclosed."*

Check and judges agree.

**The same move, passed.** This round put *Föreningen*'s measurement demand in the writer's voice in its ending, the move that got the first run's round rejected, and this run's re-review passed it. The reply reports it as an added claim and asks the writer to confirm it, and both judges pass `R1` on that account. It is recorded, not counted: the ending check reads actor and act, and it is met.

### The count

| Run | Delivers the ending | Judge a | Judge b |
| --- | --- | --- | --- |
| `pre-control-opinion-flawed-1` | no — round rejected on an attribution shift | not applied | not applied |
| `pre-control-opinion-flawed-2` | **yes** | met | met |
| `pre-control-opinion-flawed-3` | **yes** | met | met |

Two of three. **The not-reproduced gate holds**, and this is the plan's outcome 1.

## The controls

| Run | Judge a | Judge b | `C1` |
| --- | --- | --- | --- |
| `pre-control-opinion-flawed-1` | pass | pass | met |
| `pre-control-opinion-flawed-2` | pass | pass | met |
| `pre-control-opinion-flawed-3` | pass | pass | met |
| `pre-control-article-flawed` | pass | pass | met |
| `pre-control-case-study-flawed` | pass | pass | met |
| `pre-control-column-flawed` | pass | pass | met |

No judge split, so the split rule decided nothing. Both `article-flawed` judges record that the reply reports the closing `Kontakta oss.` as vague rather than as a sales line unrelated to the explanation, and neither fails the run on it. `column-flawed`'s reply names both of its headline's defects, which #466 recorded as lost under #429's revised wording; no miss of #466's shape occurs here.

The misreport check applies to candidate runs only, and none was made.

## `O1` and `S1`

`S1` passes on every run: each working directory held `input.md` alone when its session started, as `inventory-before.json` shows.

`O1` passes on five runs: the runner's before-and-after inventories of each private root show nothing created, changed or removed outside the Harness's configuration and caches. It fails on `pre-control-column-flawed`, which left an empty directory `scratch/tmp/tmp.EjAfUo14lq` in its private root. Its trace shows the Harness refusing the `rm -rf` because the directory had become the session's working directory, and its reply says so: *"en tom temporär katalog finns kvar under scratch-området: `scratch/tmp/tmp.EjAfUo14lq`. Harnessen stoppade borttagningen eftersom katalogen blivit sessionens arbetskatalog."* The runner removed the root afterwards. #429's `pre-case-question-en_GB-r3` failed `O1` the same way.

## Other things the judges recorded

Recorded, not counted, since no criterion of this evaluation reads them:

- `pre-control-opinion-flawed-2`: judge a notes the account says two claims were struck where it lists three, and the new ending subheading `Nästa steg är ett halvårs försök` reads more certain than the body's *borde*; the reply discloses the second.
- `pre-control-opinion-flawed-3`: both judges note the reply calls the opening paragraph *ingressen* after reporting that the text has no standfirst.

## What ships, and what is filed

**Outcome 1, not reproduced.** No candidate was committed and no candidate arm was run. Nothing under `skills/` or `tests/` changed: `skills/editorial/redline/references/correction.md`, `skills/kntnt/library/references/editorial/article-anatomy.review.md`, `skills/editorial/redline/help.md`, `skills/editorial/redline/SKILL.md` and `tests/test_kntnt.py` are byte-identical to `2afeb95e`, and the catalog was not regenerated. [ADR-0225](../../adr/0225-a-correction-rounds-repeating-heading-is-measured-first-and-not-reproduced.md) says why.

**Nothing is filed**, as the plan settles for this outcome. The pre-change arm's one ending miss is recorded above without an owner, because no open ticket owns a round rejected for an attribution shift. No issue number is listed here, because none was filed.

## What is not measured

The candidate the plan describes under *What is under test* was never written into the tree, so what it would have done to these rows is unmeasured. No Write run was made: Write loads neither file the candidate would have changed.
