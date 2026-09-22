# redline — claude — 2026-09-22 — #364

- **record** — `redline-claude-2026-09-22-364`
- **date** — `2026-09-22`
- **ticket** — `#364`
- **skill** — `redline`
- **provider family** — `claude`
- **model** — `claude-opus-5` at high deliberation, for every run and for every judge
- **harness** — Claude Code 2.1.278
- **corpus commit** — `218e3be1`

## Run conditions

Seven source-blind `/redline` runs, one for each draft the `b`-arm `Write` rows delivered, in the order the frozen matrix lists them: three `case-question-en_GB`, two `case-study-en_US`, two `case-study-sv`. The matrix, the criteria and the seat were frozen before the first run in [`../editorial-364/plan.md`](../editorial-364/plan.md), the conclusion is drawn in [`../editorial-364/results.md`](../editorial-364/results.md), and every artefact is under [`../editorial-364/runs/b/`](../editorial-364/runs/b/). The seven run directories without the `-paired` suffix are the Write runs these replays are paired with, and the companion Write record for this ticket covers them; this record covers only the paired Redline runs and the criterion `K-redline` they serve.

**Source-blind.** Each run received `work/input.md` — the delivered Write draft of the row it is named after — and nothing else. No run saw the material that draft was written from, and no run could ask for it. The invocation carries no `--genre` and no `--language`: all three parameters are resolved from each draft's own `kntnt` map, and every reply says so.

**The seat.** Every run is a fresh top-level Claude Code session started from the shell with `claude -p`, the child-session environment variables unset so the session is not a child, the working directory set to that run's `work/`, and Claude Code's own `--model`, `--effort` and `--permission-mode` flags set to `claude-opus-5`, `high` and `bypassPermissions`. A subagent of this harness has no agent-spawning tool, so a Redline run started in a subagent completes without the fresh correction seat its contract requires; that is [#394](https://github.com/Kntnt/skills/issues/394), and the session seat is the harness that satisfies it.

**The judges.** Two per run, each a fresh `kntnt-opus-high` subagent with no history, blind to the plan, the hypothesis, the expected answer and the model identity, reading `work/input.md`, `response.md` and `delivered.md` and nothing else. They need no seat of their own because they start nothing. Where they split, both readings are recorded below and neither is treated as the oracle. Their brief is [`../editorial-364/runs/redline-judge-brief.md`](../editorial-364/runs/redline-judge-brief.md), frozen with the plan.

**The bridge classing.** Each judge takes every quotation in the **input**, in order, and classes the bridge as the input carries it and as the delivered text carries it, in the plan's three classes: **(a)** it states what the quotation then says, adding no understanding of its own; **(b)** it names the subject, the occasion or the attribution and no more; **(c)** it carries a fact the quotation does not carry. This is the measurement the ticket exists for, so it is reported per row beside `R1`.

**`T1` and `R2` are recorded `skipped`** in every row, with the reason that a subagent's transcript is not readable from the session that started it. Nothing here claims either passed and nothing is failed for lacking them; the standing want of a trace-bearing Claude-family harness is [#388](https://github.com/Kntnt/skills/issues/388).

**The closing mechanical pass, measured mechanically.** In all seven rows the preserved `evidence/mechanical-pass-output.md` is byte-identical to `delivered.md`, so the mechanical pass is the last thing that touched the text in every run. In `case-question-en_GB-r1-paired`, `case-question-en_GB-r3-paired` and `case-study-en_US-r1-paired` it returned its input unchanged; in the other four it changed the text.

**Cleanup, read from a before-and-after inventory over every staged writable location.** The staged install `install-b` is byte-identical before the first run and after the last ([`../editorial-364/runs/install-b-before.txt`](../editorial-364/runs/install-b-before.txt), [`../editorial-364/runs/install-b-after.txt`](../editorial-364/runs/install-b-after.txt)). Every row's private scratch directory is empty or removed; each row's `work/` holds only its one input file; each row's `evidence/` holds exactly the two preserved mechanical-pass files. The per-row **side effects** entries below say this once each rather than repeating the inventory.

**Findings of a shape an open ticket owns** are recorded against that number and neither fixed nor filed again: [#377](https://github.com/Kntnt/skills/issues/377) (keep limiting sentences; report every change to a claim), [#383](https://github.com/Kntnt/skills/issues/383) (clean passages rewritten to taste outside any finding, mostly unreported), [#389](https://github.com/Kntnt/skills/issues/389) (a repair kept although the run's own re-review found it adds an unsupported claim), [#390](https://github.com/Kntnt/skills/issues/390) (a subheading repeating the sentence under it), [#392](https://github.com/Kntnt/skills/issues/392) (a source-blind review drops what the material required).

## `case-question-en_GB-r1-paired`

- **fixture** — the delivered `b`-arm Write draft of `case-question-en_GB-r1`, replayed whole as `input.md`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a changed artefact in the reply, with four findings, three repaired and one left unresolved; wall time 9m41s.
- **side effects** — `none` from the Skill; the run directory holds only what the evaluator's four instructions put there, `work/input.md` is unchanged, and `install-b` is byte-identical before and after.
- **criteria** —
  - `R1` — `pass` on both judges. Both read the four changes as answering defects visible in the text alone — a lead that restated the standfirst before advancing, two adjacent sentences using *it* for two different parties, and a heading whose every content word recurred beneath it — with both quotations, both bridges and both limiting sentences untouched. Both also record the same accuracy shortfall: the reply's blanket "No claim was removed and none was changed" covers a scope narrowing (*the work* → the two named job categories) and a relative clause whose antecedent is now indeterminate. Judge A: "the blanket sentence should have been qualified." That is [#377](https://github.com/Kntnt/skills/issues/377).
  - **bridge classing** — two quotations, neither bridge touched, and the judges agree on all four classes.
    - Q1, *Benchline's case writer asked workshop manager Priya Vale by email … Vale replied:* — **(b) → (b)**, unchanged. Judge B: "Naming the topic the quotation will speak about is not (a): the bridge nowhere says what the team had to settle."
    - Q2, *Asked whether the same choice would be made again, Vale wrote:* — **(b) → (b)**, unchanged.
    - Both judges note, and both refuse to class as a bridge, the new heading *Vale would give the status names another week*: a full sentence stands between it and the quotation, but it takes its content words from the quotation's second sentence. Judge B calls it "a weaker form" of the fault finding 3 removed. Unreported by the reply.
  - `G2`, `L1` — `pass` on the delivered artefact; no judge records a genre or idiom defect.
  - `T1`, `R2` — `skipped`.
- **unresolved findings** — one, delivered with the artefact: the ending carries no call to action, and no offer, link or contact route appears anywhere in the text, so writing one would mean inventing a fact. Both judges record this as the correct disposal.
- **defects filed** — recorded against [#377](https://github.com/Kntnt/skills/issues/377) and, for the heading that now anticipates the quotation beneath it, [#390](https://github.com/Kntnt/skills/issues/390).
- **notes** — The mechanical pass returned its input unchanged, which the reply states and the preserved files confirm.

## `case-question-en_GB-r2-paired`

- **fixture** — the delivered `b`-arm Write draft of `case-question-en_GB-r2`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a changed artefact in the reply; five findings, all repaired in the one budgeted round, and two further findings that the round's own repair created, both left unresolved; wall time 14m24s.
- **side effects** — `none` from the Skill; as above.
- **criteria** —
  - `R1` — **split. Judge B fails it; judge A passes it qualified.** Judge B fails on what was delivered: the subheading *The summary measures no outcomes* is "contradicted by the sentence immediately beneath it", the companion clause *Vale lets the schedule continue* "drops the 'for new jobs' limit … the condition the whole account turns on", and four further changes go unreported, "one of which moves a claim". Judge B's summary: "Disclosing a regression is not repairing it, and the run delivered the text with both in place." Judge A passes on the same evidence read the other way — "the single place where the delivered text is worse than the input is declared as an open finding rather than hidden" — and qualifies the pass because the claims account "states a total ('two') that the diff contradicts". Both judges identify the same nine differences and the same unreported set; they differ on whether a disclosed self-inflicted regression that ships fails the criterion.
  - **bridge classing** — two quotations. Both bridges came back changed, in wording only; **neither judge records a class change**, and the judges split on the class itself in both cases.
    - Q1, *Asked by email by Benchline's case writer what had to be settled first, Vale answered:* → *… manager Priya Vale answered:* — judge A **(c) → (c)**, on the ground that "by email" and "by Benchline's case writer" are facts the quotation does not carry; judge B **(b) → (b)**, taking the same words as occasion and attribution. Both record that the added *manager Priya* is attribution only, that nothing the text lacks is supplied — the standfirst already says *Manager Priya Vale* — that nothing is lost, and that the reply does not name the change.
    - Q2, *Vale's verdict comes with a condition and a delay:* → *Vale's verdict on the bench schedule comes …* — judge A **(b) → (b)**, because the bridge "labels the shape of what follows … without saying which condition or which delay"; judge B **(a) → (a)**, because "comes with a condition and a delay" maps one-to-one onto the quotation's two sentences. Both record the added phrase as unreported and as supplying nothing.
    - Both judges note, outside the classing, that the input's heading *Vale would use the schedule again for new jobs* pre-stated the quotation's first sentence and that the delivered heading no longer does — judge A: "the delivered heading no longer does. That is difference #7, and the reply does not report it."
  - `G2`, `L1` — `pass`; both quotations verbatim, en_GB mechanics correct in both directions.
  - `T1`, `R2` — `skipped`.
- **unresolved findings** — two, both delivered with the artefact and both in the second subheading, and both created by the round's own repair; the reply names the character count against the limit and says the budget was spent on the round that made them.
- **defects filed** — [#389](https://github.com/Kntnt/skills/issues/389) for the overclaiming subheading shipped after the run's own re-review found it; [#377](https://github.com/Kntnt/skills/issues/377) for the third claim-level move left out of the claims account; [#383](https://github.com/Kntnt/skills/issues/383) for the unfronted object and the restated referent, taste changes to prose the reply names no finding against.
- **notes** — The mechanical pass changed the text: both judges record the enclosing curly quotation marks stripped from inside the two blockquotes, wording untouched, and neither run nor reply names it.

## `case-question-en_GB-r3-paired`

- **fixture** — the delivered `b`-arm Write draft of `case-question-en_GB-r3`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a changed artefact in the reply; five findings, four repaired and one left unresolved; wall time 7m22s.
- **side effects** — `none` from the Skill; as above.
- **criteria** —
  - `R1` — `pass` on both judges, and the cleanest row in the wave. Both record that the four findings map one-to-one onto the four diff hunks, that the reply names nothing it did not change and changed nothing it does not name, and that no mechanical correction was made because none was available. Judge A: "The four findings map one-to-one onto the four diff hunks." Judge B checks the reply's own budget statement against the file and finds "no silent edits and no claimed edit that did not happen". Both note one imprecision: the claims account is written about existing claims and does not state that an assertion new to the body was added, although finding 1 says so plainly.
  - **bridge classing** — two quotations.
    - Q1, *Benchline's case writer asked workshop manager Priya Vale by email …* → *In an email interview, Benchline's case writer asked workshop manager Priya Vale …* — **(b) → (b)** on both judges. The change is **named by the reply**, as finding 3, and both judges confirm it supplies nothing the text does not carry: *interview* is the input's own later word and *email* was already in the input bridge. Nothing lost.
    - Q2, *Asked whether the choice would be made again, and what would change, Vale answered:* — unchanged, and **the judges split on the class**. Judge B: **(b) → (b)**, the preceding narrative sentence overlapping the quotation "is a separate narrative sentence, not the clause that leads into the quotation; the bridge proper stays (b)". Judge A gives the same **(b)** to the clause and classes the whole run-up **(a)**, because the sentence before it "already delivers what the quotation is there to deliver" — *approved continued use for new jobs* against *I would use it again for new jobs*. Judge A records this as a defect the run left unfound, "a missed improvement rather than damage".
  - `G2`, `L1` — `pass`; both quotations verbatim to the character, including the en_GB single curly marks.
  - `T1`, `R2` — `skipped`.
- **unresolved findings** — one: the ending carries no call to action and the text supplies no offer, link or contact route. Both judges record the disposal as correct.
- **defects filed** — `none` beyond what judge A's class-(a) run-up reading records as unfound; no judgement names a change this run made that an open ticket owns.
- **notes** — The mechanical pass returned its input unchanged.

## `case-study-en_US-r1-paired`

- **fixture** — the delivered `b`-arm Write draft of `case-study-en_US-r1`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a changed artefact in the reply; three findings repaired and three left open, two of them created by the round's own repairs; wall time 10m00s.
- **side effects** — `none` from the Skill; as above.
- **criteria** —
  - `R1` — `pass` on both judges, both of them counting costs against the pass. Both record that all three quotations came back character for character, that every limiting sentence survives, and that the reply declares its own regressions rather than claiming a clean result — judge B: "The run declares all of this rather than concealing it, so the account is trustworthy even where the work is not finished." Both hold two executions against it: the new first heading "repeats a different sentence in the same section" ([#390](https://github.com/Kntnt/skills/issues/390)), and the Q1 bridge no longer prepares its quotation.
  - **bridge classing** — three quotations, one bridge changed, **and this is the row where the judges split on the measurement itself**.
    - Q1, *The team designed the categories itself and kept telephone reporting open for residents.* → *The team kept telephone reporting open for residents.* — judge B classes it **(a) → (c)**: "*The team designed the categories itself* delivers, in the text's own voice, exactly what the quotation is there to deliver — *The categories were ours*", and what remains "is a fact the quotation does not carry". Judge A classes it **(c) → (c)**, reading the bridge whole: it "adds matter of its own, so (c) is the class, with an (a) defect inside it". On judge B's reading this is a class (a) bridge repaired to class (c); on judge A's the (a) clause went but the class did not move. Both record that the change **is named by the reply**, twice — as a repaired finding and as open finding 3 — that it supplies nothing the text does not carry, and that what left the narrative (*the team designed the categories*) survives only inside Lind's quoted *The categories were ours*, which judge B calls "a real, if small, loss of a narrative claim".
    - Q2, *Lind would plan the next building differently.* — unchanged, and **split**: judge A **(b) → (b)**, "it names the subject and the stance and stops"; judge B **(a) → (a)**, "*would plan the next building differently* states what the quotation then says". Judge B records it as "a class (a) bridge … in the input [that] the run left alone".
    - Q3, *Lind did not recommend Svale to every housing company, and her own appraisal carries a condition.* — **(c) → (c)** on both judges, unchanged. Judge A: "the text's most load-bearing bridge … and the round left it alone. Correct restraint."
  - `G2`, `L1` — `pass`; no mechanical or locale change was made and both judges find none was needed.
  - `T1`, `R2` — `skipped`.
- **unresolved findings** — three, all delivered with the artefact: the trial's two buildings still introduced by definite reference; the new first subheading; and the Q1 bridge that no longer prepares its quotation. The reply attributes the last two to its own round and stops rather than repairing its own work.
- **defects filed** — [#390](https://github.com/Kntnt/skills/issues/390) for the replacement heading that repeats a sentence in its own section; [#392](https://github.com/Kntnt/skills/issues/392) for the narrative assertion removed with no equivalent left outside the quotation; [#389](https://github.com/Kntnt/skills/issues/389) for keeping both repairs the run's own re-review found worse than what they replaced.
- **notes** — The mechanical pass returned its input unchanged, which the reply states ("found nothing to correct") and the preserved files confirm.

## `case-study-en_US-r2-paired`

- **fixture** — the delivered `b`-arm Write draft of `case-study-en_US-r2`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a changed artefact in the reply; four findings, three repaired and one left unresolved; wall time 11m01s.
- **side effects** — `none` from the Skill; as above.
- **criteria** —
  - `R1` — **split. Judge A fails it; judge B passes it with two blemishes.** Both judges find the same eight differences and agree on what each is. Judge A fails on the second subheading, *Median time to assignment fell by a day, and no cause is claimed*: "*Fell by a day* converts two static figures into a movement, which is the exact inference the trial note declines to license", the agentless *no cause is claimed* detaches the refusal from the note that makes it, and the count of 31 leaves the heading — "the review created the defect; it did not find it", and one further claim change (*stored separately* → *filed apart from one reported by email*) "is neither named nor defended". Judge B passes on the same facts, holding that "the claim account is complete enough that a reader can reconstruct the diff from it", and names as blemishes the softened characterisation of *manages* → *is responsible for* and the overstated heading "left standing rather than reverted". Both note that reverting the run's own change was available at zero budget cost and was not taken.
  - **bridge classing** — three quotations, **no bridge changed, and the judges agree on all six classes**.
    - Q1, *Maya Lind, the maintenance supervisor, puts the aim beside the division of work:* — **(b) → (b)**. Judge B: "Naming a subject the quotation then speaks about is not (a)."
    - Q2, *Lind's account returns to the categories.* — **(b) → (b)**.
    - Q3, *Her verdict is qualified, and she does not extend it to every housing company.* — **(c) → (c)**. Both judges record that the (c) element is an input-authored limiting statement and that it came through intact.
    - Both judges record that the pre-echo this run repaired sat two paragraphs before the bridge, not in it, and that the bridge itself was already clean and was correctly left alone. Judge A: "the run removed the earlier clause and left the bridge alone, which is the right end to cut."
  - `G2`, `L1` — `pass`; all four en_US locale corrections (*flats* → *apartments*, *staff* → *employees*, *working days* → *business days*, `4 December 2025` → `December 4, 2025,`) are correct and touch no figure or name, and all three quotations are verbatim.
  - `T1`, `R2` — `skipped`.
- **unresolved findings** — one, delivered with the artefact: the second subheading asserting a movement the section does not, reported in full, attributed to the run's own repair, and left for a person with the repair prescribed.
- **defects filed** — [#377](https://github.com/Kntnt/skills/issues/377), for the heading that moves the trial note's refusal to attribute away from the note and for the body claim change left out of the account; [#389](https://github.com/Kntnt/skills/issues/389), for shipping the repair the run's own re-review found unsupported.
- **notes** — The mechanical pass changed the text: it made the date correction, which the reply states as its own ("put the date of the trial note into the American convention").

## `case-study-sv-r1-paired`

- **fixture** — the delivered `b`-arm Write draft of `case-study-sv-r1`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a changed artefact in the reply, in Swedish; five findings, all five left standing, four of them created by the round's own repair; wall time 16m08s.
- **side effects** — `none` from the Skill; as above.
- **criteria** —
  - `R1` — **split. Judge B fails it; judge A passes it.** Both judges find the same nine differences. Judge B fails on two grounds: the run "shipped a lead stripped of the test's scope and a section stripped of what the vendor actually did", and it made two unreported changes to claims — the heading narrowed to *Mediantiden till tilldelning*, and the closing call to action turned from a statement into an imperative — under a closing sentence that denies them, *Inga andra påståenden ändrades*. "A review whose closing assurance is false about its own delivered text fails the criterion, however good the rest of its accounting is." Judge A passes on the same evidence, weighing that the run "disclosed its two substantive losses in its own words rather than hiding them behind the fixes that caused them", and records the same two unreported changes and the same overbroad closing sentence as what "keep[s] the pass from being clean".
  - **bridge classing** — three quotations, one bridge changed, **and both judges record the same class change**.
    - Q1 — bridge as input: *Kategorierna i loggen tog underhållsteamet fram själv, och de boende kunde fortsätta anmäla fel per telefon. Svale konfigurerade loggen och utbildade sex medarbetare vid två tillfällen. Testet pågick i åtta veckor.* Bridge as delivered: *De boende kunde fortsätta anmäla fel per telefon. Svale utbildade sex medarbetare vid två tillfällen. Testet pågick i åtta veckor.* **(a) → (c) on both judges.** Judge B: "decisively (a) through *Kategorierna i loggen tog underhållsteamet fram själv*, which says in advance exactly what the quotation is there to deliver". Judge A: "the leading clause settles the class." Both record that the change is named by the reply in finding 2 and in its removals list, that nothing new was supplied, and that one thing the quotation does not carry was lost outright — *Svale konfigurerade loggen* — which the reply itself states has no remaining equivalent. Judge B: "reporting an avoidable loss does not repair it."
    - Q2 — no narrative bridge; the only lead-in is the tag *skriver hon*. **(b) → (b)** on both judges, unchanged.
    - Q3, *Testet har ännu inte utvidgats. Teamet vill först se hur kategorierna fungerar för större reparationer, och Maya Lind rekommenderar inte Svale till alla bostadsföretag.* — **(c) → (c)** on both judges, unchanged.
  - `G2`, `L1` — `pass` on the delivered artefact. All three quotations came back word for word; the only change inside the quoted lines is the leading *talstreck* normalised from em dash to en dash, which both judges call locale-correct Swedish and both record as unreported.
  - `T1`, `R2` — `skipped`.
- **unresolved findings** — five, all delivered with the artefact: the lead's lost scope, the vendor's configuration step gone from the narrative, the replacement subheading covering its section worse, the trial's length now stated three times, and — the one not of the round's own making — that the text gives no basis for the supplier choice, which the reply classes as needing material the text does not hold.
- **defects filed** — [#392](https://github.com/Kntnt/skills/issues/392) for *Svale konfigurerade loggen* removed with no equivalent left; [#377](https://github.com/Kntnt/skills/issues/377) for the two unreported claim changes under a closing denial; [#383](https://github.com/Kntnt/skills/issues/383) for the call-to-action rewrite, which judge B calls "exactly the kind of rewrite-to-taste on working prose that R1 forbids"; [#389](https://github.com/Kntnt/skills/issues/389) for delivering the lead and the subheading its own re-review had already filed as worse.
- **notes** — The mechanical pass changed the text — it is where the three dashes moved — and the preserved output is byte-identical to what was delivered.

## `case-study-sv-r2-paired`

- **fixture** — the delivered `b`-arm Write draft of `case-study-sv-r2`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — a changed artefact in the reply, in Swedish; four findings repaired and three left standing, two of them created by the round's own repair; wall time 16m45s.
- **side effects** — `none` from the Skill; as above.
- **criteria** —
  - `R1` — `pass` on both judges. Both record that every defect acted on is visible in the text without any source — a headline asserting a finished, company-wide outcome the body never supports, two headings saying their quotations in advance, and a first body sentence repeating a seven-word run from the deck — and that nothing else moved. Judge B: "no hedge softened, no quotation reworded, no number, date, name or link altered, and no working sentence rewritten to taste." Both name the same single reporting gap, the *talstreck* normalisation, and both judge it mechanical and locale-correct. Judge B adds one overstatement in the reply: *finns inte kvar någonstans i texten* is a shade absolute, since Lind's quotation still says *Att ha en samlad bild av anmälningarna hjälper oss*. Judge A adds one inconsistency: the first subhead's residue is not noted although the third's is.
  - **bridge classing** — three quotations, one bridge changed, **and both judges record the same class change**.
    - Q1, *Svale Systems konfigurerade loggen och utbildade sex medarbetare vid två tillfällen. Telefonanmälan behölls för de boende.* — **(c) → (c)** on both judges, unchanged word for word. The judges split on the heading standing above that paragraph, which is not the bridge: judge A holds *Underhållsteamet bestämde hur felanmälningarna skulle sorteras* still **(a)** for the quotation's *Kategorierna var våra*, "mitigated … but not eliminated, and the reply does not say so"; judge B reads the same replacement as leaning "(a)/(b), nearer (b)", since it "no longer hands over the quotation's own words".
    - Q2 — no bridge; the quotation follows Q1 directly, with only the tag *säger hon*. **(b) → (b)** on both judges.
    - Q3 — the bridge is the subheading standing immediately before the quotation with no narrative between: *## Arbetsledaren skulle göra om testet med mer förberedelse* → *## Arbetsledarens omdöme kommer med villkor*. **(a) → (b) on both judges.** Judge B: "*skulle göra om testet* is *Jag skulle välja att göra testet igen*, and *med mer förberedelse* is *en extra vecka för förberedelser*. The reader meets the quotation already told what it delivers." Both record that the change is named by the reply twice — as a repaired finding and again as remaining finding 3, where the run concedes the replacement now withholds the answer — that nothing outside the text is supplied, and that nothing the quotation does not carry was lost.
  - `G2`, `L1` — `pass`; all three quotations verbatim, the dash normalisation locale-correct, and the counted limits machine-measured by the run.
  - `T1`, `R2` — `skipped`.
- **unresolved findings** — three, delivered with the artefact: the denominator for *två av husen*, which the reply classes as needing material the text does not hold; the orphan term *ärendelogg* introduced by its own headline repair; and the third subheading now withholding the answer. The reply states why it stopped: the budget was spent, and a further round would have repaired its own work.
- **defects filed** — [#389](https://github.com/Kntnt/skills/issues/389) for the two self-created defects delivered after the run's own re-review found them; [#377](https://github.com/Kntnt/skills/issues/377) for the unreported dash normalisation under a claims account that names no other change. No judgement records a fabricated fact, a lost limiting sentence or a touched quotation.
- **notes** — The mechanical pass changed the text — the three dashes — and the preserved output is byte-identical to what was delivered.

## What this record holds

Seven paired source-blind runs, fourteen judgements. `R1` passes on both judges in four rows — `case-question-en_GB-r1-paired`, `case-question-en_GB-r3-paired`, `case-study-en_US-r1-paired` and `case-study-sv-r2-paired` — and the three remaining rows are splits, each recorded above as the judgements state it: `case-question-en_GB-r2-paired` (judge B fails, judge A passes qualified), `case-study-en_US-r2-paired` (judge A fails, judge B passes with blemishes) and `case-study-sv-r1-paired` (judge B fails, judge A passes). No row is failed or passed here on a criterion softened or hardened to fit it, and no judge is treated as an oracle.

The seven inputs carry eighteen bridges between them. The two judges give the same class, before and after, on fourteen of them, and split on four: `case-question-en_GB-r2-paired` Q1 and Q2 and `case-study-en_US-r1-paired` Q1 and Q2. Two bridges changed class on both judges — `case-study-sv-r1-paired` Q1 from (a) to (c), and `case-study-sv-r2-paired` Q3 from (a) to (b) — and one changed class on one judge only, `case-study-en_US-r1-paired` Q1, (a) to (c) on judge B against (c) throughout on judge A. Every other bridge in the wave came back in the class it went in with. Two further splits are about what counts as a bridge rather than about a class: in `case-question-en_GB-r3-paired` Q2 both judges class the lead-in clause (b) and judge A classes the whole run-up (a), and in `case-study-sv-r2-paired` Q1 the judges differ over the heading two lines above the quotation, which neither treats as the bridge. What these measurements mean for the ticket is settled in [`../editorial-364/results.md`](../editorial-364/results.md), not here.
