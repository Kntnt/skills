# Results for #380

Sixteen runs made on 2026-09-21 against the method [`plan.md`](plan.md) froze before the first one, at `2026-09-21T15:59:48Z`. Artefacts are beside this file, one directory per row, each with the Write side in `write/` and the source-blind Redline side in `redline/`. The records are [`../../records/write-claude-2026-09-21-380.md`](../../records/write-claude-2026-09-21-380.md) and [`../../records/redline-claude-2026-09-21-380.md`](../../records/redline-claude-2026-09-21-380.md).

## What the evaluation found

- Sixteen invocations and thirty-two judgements, every run and every judge a fresh `claude-opus-5` subagent at high deliberation. Every row carries every criterion the matrix applies to its side.
- **All eight Write runs delivered, and all eight delivered the prose their final comparison read, byte for byte.** #362's Claude-family evaluation had one delivery that repaired prose after its last comparison and shipped it unread; nothing of that kind happened here.
- **The outcome [#376](https://github.com/Kntnt/skills/issues/376) decided is what these runs do.** Five of the eight ended with a finding their last comparison left standing, and each of the five delivered the prose unchanged and reported every remaining finding beside the draft, with the passage, what the material carries instead and the checker's proposed smallest repair. Three of those five open the reply by saying the draft is delivered with known defects before saying anything else about it.
- **`F1` fails on five of the eight Write rows, and every one of the five is a residual the delivery account named.** No unsupported passage was found that no checker saw and no account reported, so no Write row earns a defect ticket of its own.
- **The anatomy is not where these texts fail.** The five `article` and `opinion` drafts all measure `conforms: true` with no norm departure, before and after review. The three `web-copy` texts measure `conforms: false` for an absent byline and an absent lead, which is description rather than failure: the corpus binds that skeleton to the four article genres only.
- **Redline's side is one failure in sixty-seven judged lines.** Seven of the eight reviews are clean on every criterion; `opinion-sv-r2` fails `R1` for deleting a clause from a conforming text and reporting the deletion under a claim of equivalence that does not hold, with two further edits unreported. That is [#383](https://github.com/Kntnt/skills/issues/383), already open.
- **Half the reviews lost something the material required.** In four of the eight rows a source-blind change removed or weakened a formulation `source.md` warranted — twice a causal connective the source itself carries, twice a clause bounding what the text claims. Redline cannot know this by contract, and no judge counted it against `R1`; it is filed as its own question, [#392](https://github.com/Kntnt/skills/issues/392).
- **Contract loading and Redline's closing Proofread pass stayed unobserved in this family.** `T1` and `R2` are `skipped` on all sixteen entries: both are answerable only from a Harness trace, and a session cannot read the transcript of a subagent it started. So this evaluation does not settle whether the scoped loading happened, and **it does not settle whether Redline's closing Proofread pass ran** — the question the ticket opens with stays open. The trace-bearing harness is [#388](https://github.com/Kntnt/skills/issues/388).
- **`T2` was exercised for the first time in this family.** All three explicit technique rows carry their technique in the delivered metadata and in the account, both judges pass `T2` on both sides of each, and no technique was inferred on any of the five rows that selected none.
- Nothing was written outside each run's own directory. The staged install is byte-identical before and after the wave, every `work/source.md` and `work/input.md` is unchanged, and every `work/scratch/` is empty.

## The eight Write runs

`A / B` marks a split; the verdict recorded is the one before the bracket, and the dissent is in the entry's `notes`. `T1` and `R2` are `skipped` on all eight and are not repeated here.

| Row | Outcome | Judge class | Comparisons | Delivered = last compared prose | Remaining findings reported | Checker findings | Wall |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `article-sv` | delivered | valid delivery | 1 | yes | none; the account carries the checker's one editorial question | 1: disputed | 803 s |
| `article-en_GB` | delivered | valid delivery | 2 | yes | 2, each with passage, material and repair | 4 supported, all seen; 2 repaired, 2 reported | 1286 s |
| `web-copy-sv` | delivered | valid delivery | 2 | yes | 2, with passage, material and repair | 4 supported, 1 disputed (the headline's definite genitive) | 928 s |
| `opinion-sv-r1` | delivered | valid delivery | 2 | yes | 1, with passage, material and repair | 3 supported and repaired, 1 disputed | 1108 s |
| `opinion-sv-r2` | delivered | valid delivery | 2 | yes | none; the last comparison reported nothing | 4 supported and repaired, 2 editorial questions disputed | 1174 s |
| `article-abt` | delivered | valid delivery | 2 | yes | 1, with passage, material and repair | 4 supported (3 repaired, 1 reported), 2 disputed | 1029 s |
| `article-pac` | delivered | valid delivery | 2 | yes | 3, each with passage, material and repair | 5 supported, 2 disputed | 1149 s |
| `web-copy-abt` | delivered | valid delivery | 2 | yes | 2, plus one editorial question | 2 supported, 1 disputed (A: 2 supported) | 876 s |

Median Write wall time 1069 seconds. No run stopped, so no row has a `not delivered` line and no Redline entry is `skipped`.

Every "delivered = last compared prose" above was established by a judge comparing `delivered.md` with the last draft under `evidence/`, not from the run's own account. On seven rows the two are identical except for the `kntnt` frontmatter the delivery wrapper adds, which is metadata and not prose; on `article-sv` they are identical byte for byte.

### The five residuals, and why none is a new defect

The plan fixed this before the runs: a residual the delivery account names is not a new defect and gets no ticket, and the run's `F1` line still reads `fail` for that passage.

| Row | The passage the account reports | What the material carries instead |
| --- | --- | --- |
| `article-en_GB` | "A second trial is planned for November" | `Nästa försök planeras för november` — the next, not the second |
| `article-en_GB` | "why Björkskolan's classrooms turned cold" | Rask's `varför det blev kallt just då`, hers and time-bounded |
| `opinion-sv-r1` | "Bakom förslaget ligger åtta veckors försök i två av sju lokaler" | `Motivet i utlåtandet är att personalen ska slippa föra in uppgifter i två flöden`; nothing links the proposal to the pilot |
| `article-abt` | "En temperaturgivare svarar på en fråga i taget: hur varm är luften där utrustningen sitter?" | `En givare mäter temperaturen där den sitter`, and separately that this trial measured air only |
| `article-pac` | "when the air dropped below a chosen limit", and "left them there for four weeks" | a sampled reading at the sensor, and four weeks of recording rather than of installation |
| `web-copy-abt` | "Uppdraget består av två delar:" | `Genomgången omfattar … och …`, which enumerates without closing the list |
| `web-copy-sv` | the headline's `föreningens gemensamma lokal`, and "passar er" | `en gemensam lokal`, and `för att stämma av om uppdraget passar` with no complement |

`web-copy-sv`'s two are reported the same way but both judges class the text itself as passing `F1`, so that row's `F1` line reads `pass` with the two reported findings named.

## The eight Redline runs

| Row | Outcome | Script, input | Script, delivered | G1 | G2 | P1 | W1 | L1 | L2 | T2 | R1 | O1 | Wall |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `article-sv` | changed | exit 0 | exit 0 | pass | pass | pass | pass | pass | pass | skipped | pass (A fail / B pass) | pass | 863 s |
| `article-en_GB` | changed | exit 0 | exit 0 | pass | pass | pass | pass | pass | pass | skipped | pass | pass | 540 s |
| `web-copy-sv` | no change | exit 1 | exit 1 | pass | pass | pass | pass | pass | pass | skipped | pass | pass | 324 s |
| `opinion-sv-r1` | changed | exit 0 | exit 0 | pass | pass | pass | pass | pass | pass | skipped | pass | pass | 587 s |
| `opinion-sv-r2` | changed | exit 0 | exit 0 | pass | pass | pass | pass | pass | pass | skipped | **fail** (A pass / B fail) | pass | 795 s |
| `article-abt` | changed | exit 0 | exit 0 | pass | pass | pass | pass | pass | pass | pass | pass | pass | 576 s |
| `article-pac` | changed | exit 0 | exit 0 | pass | pass | pass | pass | pass | pass | pass | pass | pass | 727 s |
| `web-copy-abt` | changed | exit 1 | exit 1 | pass | pass | pass | pass | pass | pass | pass | pass | pass | 506 s |

Median Redline wall time 582 seconds. The two `exit 1` rows are the `web-copy` texts, failing on an absent byline and an absent lead that the genre does not require.

Sixty-seven criterion lines are judged on each side. On the Write side sixty-two pass and five fail, every failure `F1` and every one a reported residual. On the Redline side sixty-six pass and one fails. Forty-two lines are `skipped` across the two records — `T1` and `R2` on all sixteen entries, and `T2` on the ten entries of the five rows that selected no technique.

## What the two sides did to each other

- **Redline repaired one of Write's own residuals.** On `article-en_GB` the single change it made was the second residual above, `why Björkskolan's classrooms turned cold` → `why the temperature in Björkskolan's classrooms fell below the limit`, found from the text alone because the article refuses that characterisation twice in its own voice. It reported the change accurately and left the other residual standing.
- **Redline kept every other residual.** The `article-abt`, `article-pac`, `web-copy-abt`, `web-copy-sv` and `opinion-sv-r1` residuals all survive review untouched, which is what a source-blind pass can be expected to do: each of them needs the material to see.
- **Twice a causal connective went out that the source licensed.** `article-sv` removed `därför` from `Rapporten redovisar därför lektionspass i stället för ett enda dygnsmedelvärde`, and `article-pac` removed the `therefore` of the same sentence in English, both diagnosing it as a reason the text does not support. The source states it: `Rapporten redovisar därför lektionspass i stället för ett enda dygnsmedelvärde`. Four judgements name it independently.
- **Twice a bounding clause went out.** `article-abt` replaced the subheading `Effekten av eventuella justeringar är inte mätt`, which was the text's only carrier of the source's `Inga justeringars effekt har ännu mätts`; `opinion-sv-r2` deleted `inte om att de som ringer skulle vara lata eller dyra`, which carries the source's `Förvaltningens verkliga invändning … är dubbel administration, inte att telefonanvändare är lata eller dyra`.
- None of these counts against `R1`: the Skill has no access to the material by contract, and every judge said so. They are recorded as [#392](https://github.com/Kntnt/skills/issues/392), a question about how the two Skills meet rather than a bug in either.

## Method

Eight things about how this wave was made, declared here rather than inferred from the artefacts.

1. **One rolling wave.** The eight Write runs were dispatched together; each row's Redline run was dispatched as soon as that row's Write reply had been saved, extracted and measured, and each pair of judges as soon as its artefact was complete. The scope-3 and scope-4 inventories were therefore taken once, before the first dispatch and after the last judgement, as `wave-1-before.txt`, `wave-1-after.txt`, `wave-1-before-repo.txt` and `wave-1-after-repo.txt` beside `runs/`.
2. **The concurrency ceiling shaped the order, not the content.** The Harness runs at most twenty subagents at once and a Write run holds its checkers, so several judges were queued and dispatched as slots freed. No run and no judgement was affected; only the order they were started in.
3. **Wall time is the evaluator's measurement**, taken from the dispatch timestamp to the modification time of the reply the run saved as `response.md`. A Write row's clock starts at the single wave dispatch, `2026-09-21T16:00:17Z`; a Redline row's starts at its own `start-epoch.txt`.
4. **Each judge was pointed at a byte copy of its frozen brief by path**, in the evaluator's own directory in the staging area, rather than having the text pasted into its turn, plus one evaluator sentence: if the judgement file write is refused, reply with the whole judgement. No judge's write was refused, and every judgement in this tree is its judge's own.
5. **`delivered.md` was extracted from `response.md` mechanically**, by taking the longest fenced code block, which the delivery contract makes the whole Text Artifact. The throwaway script that did it is not kept: every `delivered.md` sits beside the `response.md` it came from, so the extraction is checkable by eye against the rule stated here. For `web-copy-sv`'s Redline reply, which is a short no-change status carrying no fence, `delivered.md` is a byte copy of `work/input.md` and the entry says `no change`.
6. **Two checkers could not write their report files**, because the staging area sits under a `.git` directory their sessions treat as protected — `article-sv` says so in its account, and `web-copy-abt`'s first checker's report never reached `evidence/` at all, its reply reaching the run truncated at the start. Both runs saved what they received and both comparisons carry a completion status, so both count as complete; `web-copy-abt`'s first claim accounting cannot be reviewed, and the record says so. This is the staging area's doing, not the Skill's. The process table was sampled repeatedly while the runs were in flight and held no `until [ -f … ]` wait loop at any point, so the shape of [#391](https://github.com/Kntnt/skills/issues/391) did not appear here.
7. **The repository working copy was untouched.** `git -C /Users/thomas/Projects/skills rev-parse HEAD` and `git status --porcelain --untracked-files=all` are identical before and after, and this ticket's own working tree is byte-identical across the wave — the evaluator wrote nothing in it while a run was in flight. The Skills, the measuring script and the fixtures were taken from `8a37e57e` with `git archive` and `git show`, never from a working copy, and the staged install is byte-identical to the repository at that commit after the wave as before it.
8. **One judge used a scratch file of its own** outside the inventory scope, `/tmp/x.md`, and deleted it; the evaluator confirmed it was gone. It is a judge's file, not a Skill's, and no criterion rests on it.

`O1` and the `side effects` field in both records were read by the evaluator from each run's `inventory-before.txt` and `inventory-after.txt`, never from a run's report of itself. In all sixteen the diff adds only the evaluator's own files, and the staged install appears in no diff. The wave-level diff outside the run tree holds only the evaluator's own helpers — `agents.txt`, `queue.txt`, the extraction script, `post-write.sh`, `post-redline.sh` — and the inventories themselves.

## Defects

- **[#392](https://github.com/Kntnt/skills/issues/392) — a source-blind review removes what the material required, and nothing downstream notices.** Filed by this evaluation. Four of eight rows, two of them the same sentence in two languages.
- **[#383](https://github.com/Kntnt/skills/issues/383) — Redline changes a clean passage outside any finding and omits changes from its account.** Already open; cited rather than filed again. `opinion-sv-r2` is the `R1` failure above; `opinion-sv-r1`'s account is a bare count of three findings naming none of them; `web-copy-abt` leaves one of four changes out of a list it introduces as complete; `article-sv` reports its headline rewrite without naming that it reseated the trial with the school.
- **[#388](https://github.com/Kntnt/skills/issues/388) — a trace-bearing Claude-family evaluation harness.** Already open; both records name it against every `T1` and `R2` line.
- No Write row earns a ticket. Every `F1` failure is a residual its own delivery account reported, which the plan fixed in advance as not a new defect.
