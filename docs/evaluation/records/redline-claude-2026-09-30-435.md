# redline — claude — 2026-09-30 — #435

- **record** — `redline-claude-2026-09-30-435`
- **date** — `2026-09-30`
- **ticket** — `#435`
- **skill** — `redline`
- **provider family** — `claude`
- **model** — `claude-opus-5-5` at high deliberation, for every run session, every correction subagent and nested Proofread pass in it, and every judge
- **harness** — Claude Code 2.1.285
- **corpus commit** — `e7773344`

## Run conditions

Two arms over the four #362 drafts and the ten *Redline controls* rows, and one revise round on the seven inputs the ship rule sent back. The pre-change arm was staged from `e7773344`, the branch head when #435's build began. The candidate arm was staged from `12a1c7d2`, which carries the first wording. The revise round was staged from `77dd847a`, which carries the revised wording. The method is [#398's](../editorial-398/plan.md), with the changes #435's readiness addenda settle. It was frozen for this ticket in [`../editorial-435/plan.md`](../editorial-435/plan.md), before the first run. The whole evaluation is written up in [`../editorial-435/results.md`](../editorial-435/results.md), and every run's packet is under [`../editorial-435/runs/`](../editorial-435/runs/).

Each run was a fresh top-level Claude Code session started by [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py). The Formal Invocation was its whole prompt, and the editorial Skills and the Manager were staged by `git archive` into a private root of its own. Every run was judged by two fresh judges, blind to the arm, the model and the ticket, using #398's briefs byte for byte. No Codex Harness and no GPT model was started, controlled or invoked. The runs were made from 22:00 UTC on 29 September to 06:33 UTC on 30 September, all of it 30 September in the build's local time.

Three criteria are this evaluation's own:

- **`A2`**, read as the plan reads it. Every miss a judge records is read and put in one of four classes: the claim account (1), a statement about a text that the text contradicts (2), a statement true of its text that the judge faults for what it suggests (3), and an omission (4). A run fails `A2` here where it carries a class 1, 2 or 4 miss. One judge is enough, and class 3 is noted without failing it.
- **`O1`**.
- **`S1`**.

`R1` on the drafts and `C1` on the controls are recorded as the judges give them, and not scored. A clean control was run once per arm to a response target, as the plan declares; the protocol's file-target run was not made.

Six runs of the revise round's first attempt were cut off by an expired login, void under the plan's *Void runs*. Their packets are under [`../editorial-435/voided/`](../editorial-435/voided/), and each has an entry below after the counted runs.

## `pre-column-sv-r1`

- **fixture** — `column-sv-r1`, the #362 draft `docs/evaluation/editorial-362/runs/column-sv-r1/redline/work/input.md`, pre-change arm, staged from `e7773344`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with `Mallen` → `Bibliotekets mötesmall` in the headline and the dash set as a Swedish en dash; the missing standfirst, sections and call to action reported and not written, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1, 2 or 4 miss (class 3 noted below).
  - `R1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: *ett svenskt [tankstreck] med mellanslag (–)*, judge B: "med mellanslag" suggests spaces were added; the em dash already had spaces.

## `pre-column-sv-r2`

- **fixture** — `column-sv-r2`, the #362 draft `docs/evaluation/editorial-362/runs/column-sv-r2/redline/work/input.md`, pre-change arm, staged from `e7773344`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with the headline `Rutan som inte finns` → `Mötesmallen kanske behöver en fråga om syfte` and the dash set as a Swedish en dash; the missing standfirst and sections reported and not written, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `fail` — Class 1, the claim account, judge B: *Rubriken påstår nu, med förbehållet "kanske", att mötesmallen kan behöva en fråga om syfte* — does not note that the new headline recasts the proposed question as one about "syfte".
  - `R1` — recorded, not scored — judges fail / fail.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: *rubriken är reparerad*, judge B: the description of what changed is accurate; its classification as a repair is not (no visible defect). Recorded under #429. Recorded, not filed: the pre-change wording is not the one that shipped.

## `pre-opinion-en_GB-r1`

- **fixture** — `opinion-en_GB-r1`, the #362 draft `docs/evaluation/editorial-362/runs/opinion-en_GB-r1/redline/work/input.md`, pre-change arm, staged from `e7773344`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the opinion piece with the byline moved from the end to under the headline and the second and third subheadings rewritten; the missing standfirst reported, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `fail` — Class 1, the claim account, judge A: *[section 3 subheading] now calls for measuring staff time ... no longer mentions six months or keeping both routes open* — does not note that "staff time" is narrower than the sentence under the heading. Class 2, a statement about the text the text contradicts, judge A: *The first sentence under it repeated two of its three items in the same words* — overstates the case: "Six months"/"six-month trial", "both routes"/"both booking routes kept open"; close, not identical. Class 1, the claim account, judge B: *[section 3 subheading] now calls for measuring staff time ...* — does not report the narrowing to "staff" time or the change to an imperative. Class 4, a difference no statement reports, judge B: does not mention that the "on the table" echo in the final paragraph is lost.
  - `R1` — recorded, not scored — judges fail / fail.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: *Fixed — Byline in the wrong place*, judge A: describes a genre preference as a defect; the description of what changed is correct. *[defects named for the byline and both subheadings]*, judge B: placement is taste; "motive" defect contestable; a heading that previews its section is normal. Recorded under #429. The rewrite a class 2 statement describes is recorded under #429; the false statement counts here. Recorded, not filed: the pre-change wording is not the one that shipped.

## `pre-opinion-en_GB-r2`

- **fixture** — `opinion-en_GB-r2`, the #362 draft `docs/evaluation/editorial-362/runs/opinion-en_GB-r2/redline/work/input.md`, pre-change arm, staged from `e7773344`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the opinion piece with `Keep the telephone` → `Keep telephone booking` in the headline, `By` added to the byline, the last section opening `The board can` and `channel` → `route` three times; the missing standfirst reported, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `fail` — Class 4, a difference no statement reports, judge A: does not mention that the headline change breaks the echo of the body's wording. Class 2, a statement about the text the text contradicts, judge A: *All the sentences that limit the claims are unchanged* — two sentences carrying limiting clauses each had one word changed ("channels" to "routes"); read literally "unchanged" is wrong. Class 2, a statement about the text the text contradicts, judge B: *All the sentences that limit the claims are unchanged, including ... the disclaimer about the administration's motives* — inaccurate: the disclaimer sentence changed ("channels" to "routes"), though its limit did not.
  - `R1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: *a reader skimming the headline couldn't tell the piece is about booking venues*, judge A: overstates what is a working shorthand. *[finding 3's reason for the headline]*, judge B: a taste judgement presented as a defect. Recorded under #429. Recorded, not filed: the pre-change wording is not the one that shipped.

## `pre-control-article-clean`

- **fixture** — `article-clean`, the control `docs/evaluation/corpus/editorial-quality/controls/article-clean.md`, pre-change arm, staged from `e7773344`
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the article with the headline `Mätförsöket i Björkskolan visar när, inte varför` → `Björkskolans mätvärden behöver läsas mot rummens användning`; the lead's unkept promise about sensor placement reported and not written, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `fail` — Class 1, the claim account, judge A: *Nu: Björkskolans mätvärden behöver läsas mot rummens användning. Det är en rekommendation* — does not mention that the recommendation is Rask's or that it dropped the "innan styrningen ändras" condition. Class 1, the claim account, judge B: *en rekommendation med samma styrka som textens egen uppmaning* — less accurate: does not admit that the headline no longer carries the result.
  - `C1` — recorded, not scored — judges fail / fail.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: *Rubriken upprepade ingressens andra mening (åtgärdat); Inledningsstycket lovar något om givarnas placering som texten aldrig följer upp*, judge A: both findings are false positives on a conforming text; the change is not a defect repair. Recorded under #429. Recorded, not filed: the pre-change wording is not the one that shipped.

## `pre-control-article-flawed`

- **fixture** — `article-flawed`, the control `docs/evaluation/corpus/editorial-quality/controls/article-flawed.md`, pre-change arm, staged from `e7773344`
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the article with the headline and standfirst rewritten, the catastrophe, health-certainty and importance sentences cut, a long sentence split and the single body paragraph split into four; the unclear `resonemanget`, the unanchored `Kontakta oss` and the missing byline and subheadings reported, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `fail` — Class 1, the claim account, judge A: *[Uppgiften om sex klassrum] finns kvar ordagrant i brödtexten, nu sist i första stycket* — the small implicit attribution effect of the move is not mentioned. Class 1, the claim account, judge B: *[same entry]* — the slight attribution drift from the new position is not mentioned.
  - `C1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Recorded, not filed: the pre-change wording is not the one that shipped.

## `pre-control-case-study-clean`

- **fixture** — `case-study-clean`, the control `docs/evaluation/corpus/editorial-quality/controls/case-study-clean.md`, pre-change arm, staged from `e7773344`
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the case study with the headline, the body's first sentence and the second subheading rewritten; nothing left unresolved, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `fail` — Class 1, the claim account, judge A: *[Rubriken] påstår nu att Elm Quays arbetsledare ser nytta ... vilar på Linds egna ord* — partly inaccurate: does not report the loss of the qualification the same sentence puts on that benefit. Class 1, the claim account, judge B: *[same entry]* — accurate but incomplete: the preparation caveat left out of the headline is not mentioned.
  - `C1` — recorded, not scored — judges fail / fail.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: *beskrev en åtgärd i stället för kundens nytta; [scope overclaim]*, judge A: taste reasons presented as defects; the scope overclaim is resolved by the standfirst's first sentence. Recorded under #429. Recorded, not filed: the pre-change wording is not the one that shipped.

## `pre-control-case-study-flawed`

- **fixture** — `case-study-flawed`, the control `docs/evaluation/corpus/editorial-quality/controls/case-study-flawed.md`, pre-change arm, staged from `e7773344`
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the case study returned unchanged except `arbetsbelastningen` → `arbetsbelastningarna`, its one correction round rejected and reverted; nine findings reported, among them the headline, the doubled standfirst, the vendor boasting, the causal claim and the missing byline, call to action and customer background, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1, 2 or 4 miss.
  - `C1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `pre-control-column-clean`

- **fixture** — `column-clean`, the control `docs/evaluation/corpus/editorial-quality/controls/column-clean.md`, pre-change arm, staged from `e7773344`
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with the headline `Mötesmallen har en ruta för allt utom varför` → `Mötesmallen har rutor för tid, inte för varför`; nothing left unresolved, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1, 2 or 4 miss (class 3 noted below).
  - `C1` — recorded, not scored — judges fail / fail.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: *[Rubriken] ... överdrev vad mallen innehåller*, judge A: reads a deliberate figure of speech as a factual overclaim; the change is described correctly but the finding is not a defect. Recorded under #429.

## `pre-control-column-flawed`

- **fixture** — `column-flawed`, the control `docs/evaluation/corpus/editorial-quality/controls/column-flawed.md`, pre-change arm, staged from `e7773344`
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with the headline `Möten förändrar allt` → `Mötesmallen saknar plats för det vi ska förstå tillsammans`, two filler sentences and the `Sammanfattningsvis` paragraph cut; the contradiction in the first paragraph, the unconnected scene, and the missing standfirst, sections and call to action reported and not written, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1, 2 or 4 miss.
  - `C1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `pre-control-opinion-clean`

- **fixture** — `opinion-clean`, the control `docs/evaluation/corpus/editorial-quality/controls/opinion-clean.md`, pre-change arm, staged from `e7773344`
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — no text returned: the reply says no change was needed, and gives its account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1, 2 or 4 miss.
  - `C1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `pre-control-opinion-flawed`

- **fixture** — `opinion-flawed`, the control `docs/evaluation/corpus/editorial-quality/controls/opinion-flawed.md`, pre-change arm, staged from `e7773344`
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the opinion piece with the headline and both subheadings rewritten, the `Alla vet` sentence and the `Därför` conclusion cut, the 20 percent claim limited to bookings, and a closing section with its own subheading and a call to the board added; the missing standfirst and the unintroduced `Föreningen` reported, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1, 2 or 4 miss.
  - `C1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `pre-control-web-copy-clean`

- **fixture** — `web-copy-clean`, the control `docs/evaluation/corpus/editorial-quality/controls/web-copy-clean.md`, pre-change arm, staged from `e7773344`
- **invocation** — `/redline --genre=webcopy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the web page with `inom tre arbetsdagar` added to the body under the last subheading; the unlocated form reported and not written, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1, 2 or 4 miss (class 3 noted below).
  - `C1` — recorded, not scored — judges fail / fail.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: *Åtgärdat: svarstiden stod bara i underrubriken ... Den som läste avsnittet utan rubriken fick därför inte veta när svaret kommer*, judge A: the defect label is wrong; the reply describes the edit accurately but misclassifies its nature. Recorded under #432.

## `pre-control-web-copy-flawed`

- **fixture** — `web-copy-flawed`, the control `docs/evaluation/corpus/editorial-quality/controls/web-copy-flawed.md`, pre-change arm, staged from `e7773344`
- **invocation** — `/redline --genre=webcopy --language=en_US --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the web page with the headline rewritten, the opening paragraph replaced by the offer's four facts in one paragraph, six subheadings reduced to one new one, and the link relabelled `Express interest` and moved below the offer; what the review examines and who Svale is reported, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1, 2 or 4 miss.
  - `C1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `post-column-sv-r1-a`

- **fixture** — `column-sv-r1`, the #362 draft `docs/evaluation/editorial-362/runs/column-sv-r1/redline/work/input.md`, candidate arm, first wording, staged from `12a1c7d2`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column unchanged except the dash set as a Swedish en dash; the missing standfirst, sections and call to action reported and not written, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1, 2 or 4 miss (class 3 noted below).
  - `R1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: *ett svenskt tankstreck med mellanslag (–)*, judge B: small imprecision: the em dash already had spaces, so "med mellanslag" describes the result, not a change.

## `post-column-sv-r1-b`

- **fixture** — `column-sv-r1`, the #362 draft `docs/evaluation/editorial-362/runs/column-sv-r1/redline/work/input.md`, candidate arm, first wording, staged from `12a1c7d2`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with `Mallen har en ruta` → `Bibliotekets mötesmall har rutor` in the headline and the dash set as a Swedish en dash; the missing standfirst, sections and call to action reported and not written, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `fail` — Class 2, a statement about the text the text contradicts, both judges: *Resten av texten är orörd.* — contradicted by the dash change; the reply reports the dash at its end, so it contradicts itself. Class 1, the claim account, both judges: *Rubriken säger nu att bibliotekets mötesmall har rutor för allt utom poängen* — never says outright that the singular became a plural. Class 4, a difference no statement reports, judge B: says nothing about the lost echo of "ännu en ruta".
  - `R1` — recorded, not scored — judges pass / fail.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: *ett svenskt tankstreck med mellanslag (–)*, judge A: describes the result correctly, though the input already had the spaces. Recorded, not filed: the revised wording replaced the first on this input.

## `post-column-sv-r2-a`

- **fixture** — `column-sv-r2`, the #362 draft `docs/evaluation/editorial-362/runs/column-sv-r2/redline/work/input.md`, candidate arm, first wording, staged from `12a1c7d2`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with the headline `Rutan som inte finns` → `Bibliotekets mötesmall borde kanske fråga varför vi träffas` and the dash set as a Swedish en dash; the missing standfirst, sections and call to action reported and not written, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `fail` — Class 1, the claim account, judge A: *Borttagna eller tillagda påståenden: inga* — less accurate: holds only if the headline's new normative claim counts as a change rather than an addition, which is how the reply frames it.
  - `R1` — recorded, not scored — judges fail / fail.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: *En rättning gjordes och godtogs*, judge A: nothing in the two files shows who accepted it. *Rubriken ... gick inte att förstå utan att läsa texten*, judge A: the old headline presented as a defect; the report of what changed is accurate. *gick inte att förstå utan att läsa texten; upprepade dessutom första styckets formulering*, judge B: its justification is not accurate as a defect claim: a taste judgement, and a deliberate echo. Recorded under #429. Recorded, not filed: the revised wording replaced the first on this input.

## `post-column-sv-r2-b`

- **fixture** — `column-sv-r2`, the #362 draft `docs/evaluation/editorial-362/runs/column-sv-r2/redline/work/input.md`, candidate arm, first wording, staged from `12a1c7d2`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with the headline `Rutan som inte finns` → `Bibliotekets mötesmall frågar efter tiden men inte syftet` and the dash set as a Swedish en dash; the missing standfirst, sections and closing section, and the new headline echoing the opening paragraph, reported and not written, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1, 2 or 4 miss (class 3 noted below).
  - `R1` — recorded, not scored — judges fail / fail.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: *ett svenskt med mellanslag (–)*, both judges: "med mellanslag" could be read as saying spaces were added; the resulting form is described correctly. *Rubriken (åtgärdat) ... så vag*, both judges: disagrees with the "repair" label; the reply does not misstate what changed. Recorded under #429.

## `post-opinion-en_GB-r1-a`

- **fixture** — `opinion-en_GB-r1`, the #362 draft `docs/evaluation/editorial-362/runs/opinion-en_GB-r1/redline/work/input.md`, candidate arm, first wording, staged from `12a1c7d2`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the opinion piece with the byline moved up, `Lervik's` added to the lead and the third subheading rewritten; the missing standfirst reported, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `fail` — Class 2, a statement about the text the text contradicts, both judges: *[the old subheading] also said nothing about the rest of the section* — overstated: "something to measure" pointed at the measuring the section describes.
  - `R1` — recorded, not scored — judges pass / fail.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: *Byline in the wrong place*, judge A: the Skill's framing of a convention, not a visible defect. *readers met the argument ... without knowing who was making it until the last line*, judge B: overstates the problem: section 3 names Öppna beslut as the proposer. Recorded under #429. The rewrite a class 2 statement describes is recorded under #429; the false statement counts here. Recorded, not filed: the revised wording replaced the first on this input.

## `post-opinion-en_GB-r1-b`

- **fixture** — `opinion-en_GB-r1`, the #362 draft `docs/evaluation/editorial-362/runs/opinion-en_GB-r1/redline/work/input.md`, candidate arm, first wording, staged from `12a1c7d2`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the opinion piece with the byline moved from the end to below the opening paragraph, `Lervik's` added in three places and the third subheading rewritten; a missing lead reported, the opening paragraph taken as the standfirst, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `fail` — Class 1, the claim account, judge A: *The section 3 subheading now says the proposal is to measure staff time ...* — does not mention that the heading is now an instruction or that it drops "voluntarily". Class 2, a statement about the text the text contradicts, judge B: *This wording is drawn from the rest of the section* — inaccurate: the reply's own later note shows that "staff time" comes from section 2. Class 1, the claim account, judge B: *[section 3 subheading entry]* — does not report that "voluntarily" is gone from the heading's paraphrase, or that the heading became an imperative.
  - `R1` — recorded, not scored — judges fail / fail.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: *The standfirst didn't say which council*, judge A: not accurate as a diagnosis: the title directly above names Lervik (the paragraph itself did not). *[byline] with the author still unnamed*, judge A: treats a convention as a defect. *[byline reason]*, judge B: presents an ordinary end sign-off as a defect. *the body ... never says what the pilot tested*, judge B: doubtful: section 1 says what the pilot covered and counted (it does not say what the pilot tested). Recorded under #429. The rewrite a class 2 statement describes is recorded under #429; the false statement counts here. Recorded, not filed: the revised wording replaced the first on this input.

## `post-opinion-en_GB-r2-a`

- **fixture** — `opinion-en_GB-r2`, the #362 draft `docs/evaluation/editorial-362/runs/opinion-en_GB-r2/redline/work/input.md`, candidate arm, first wording, staged from `12a1c7d2`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the opinion piece with `Keep the telephone` → `Keep telephone booking` in the headline, `By` added to the byline, `telephone and web` added to the lead, the last section opening `The board can` and `channel` → `route` three times; the missing standfirst reported, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1, 2 or 4 miss (class 3 noted below).
  - `R1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: *Changed (headline, finding 2): the headline now says what should be kept ... telephone booking of venues*, judge A: accurate description, but overstates the edit by calling it a claim change (judge B: more cautious, not a misreport). *[headline] didn't say what was being kept; [byline] read like a caption*, judge A: judgements of taste presented as defects. Recorded under #429.

## `post-opinion-en_GB-r2-b`

- **fixture** — `opinion-en_GB-r2`, the #362 draft `docs/evaluation/editorial-362/runs/opinion-en_GB-r2/redline/work/input.md`, candidate arm, first wording, staged from `12a1c7d2`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the opinion piece with `Keep the telephone` → `Keep telephone booking` in the headline, `By` added to the byline, `telephone and web` added to the lead, the last section opening `The board can` and `channel` → `route` three times; the missing standfirst reported, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `fail` — Class 2, a statement about the text the text contradicts, both judges: *"It can adopt…", only made sense by reading the subheading, because the board was named nowhere else* — false: the board is named in the lead and in section 4.
  - `R1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: *Changed, headline (repair 3)*, judge A: over-classifies it as a changed claim, but describes the text correctly. *[byline] could read as a caption*, judge B: a matter of taste, not a defect (and the headline over-reported as a changed claim). Recorded under #429. Recorded, not filed: the revised wording replaced the first on this input.

## `post-control-article-clean`

- **fixture** — `article-clean`, the control `docs/evaluation/corpus/editorial-quality/controls/article-clean.md`, candidate arm, first wording, staged from `12a1c7d2`
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the article returned unchanged, its one correction round (headline and the lead's third sentence) rejected and reverted; the headline, the lead repeating the standfirst and the unexplained sensor placement reported, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1, 2 or 4 miss (class 3 noted below).
  - `C1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: *[three findings: headline, lead repeats standfirst, placement never explained]*, judge A: detection-side false positives; none changed the text. *Leadens tredje mening upprepar standfirsten*, judge B: the overlap is loose: a signpost, not a repetition of a result; at most taste. Recorded under #429.

## `post-control-article-flawed`

- **fixture** — `article-flawed`, the control `docs/evaluation/corpus/editorial-quality/controls/article-flawed.md`, candidate arm, first wording, staged from `12a1c7d2`
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the article with the headline and standfirst rewritten, the catastrophe, health-certainty and importance sentences cut, `medan` → `och`, the office named in the first sentence and `för att rädda framtiden` cut; the unclear `resonemanget`, the unnamed `oss` and the missing byline and subheadings reported, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `fail` — Class 1, the claim account, judge A: *"medan" antydde ett samband ... Ordet är ersatt med "och"; Försökets längd och givarnas placering står nu som två fakta bredvid varandra, utan samband* — does not mention the lost reading of simultaneity (chronology); accurate at the level it claims.
  - `C1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — #458
- **notes** — none

## `post-control-case-study-clean`

- **fixture** — `case-study-clean`, the control `docs/evaluation/corpus/editorial-quality/controls/case-study-clean.md`, candidate arm, first wording, staged from `12a1c7d2`
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the case study with the headline, the standfirst's last sentence, the body's first sentence and the second subheading rewritten, and `arbetsbelastning` → `arbetsbelastningar`; nothing left unresolved, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `fail` — Class 1, the claim account, both judges: *Ändrat, rubriken: påstår nu att Elm Quays arbetsledare ser nytta i en gemensam reparationslogg* — does not say that the headline drops the condition in Lind's appraisal. Class 1, the claim account, both judges: *Ändrat, ingressen: anteckningarna anges nu som underhållsgruppens egna anteckningar från försöket* — nearly accurate: the returned text does not say "egna"; nor does the list mention "gruppen" becoming "Elm Quays underhållsgrupp". Class 1, the claim account, judge A: *Ändrat, brödtextens första mening: målet är detsamma* — does not mention that "få ut av" became "se … i".
  - `C1` — recorded, not scored — judges fail / fail.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — #459, #460, #461
- **notes** — Class 3, not counted: *Den bestämda formen ... sa att alla reparationsärenden samlades*, both judges: the reason is questionable: a reading the text does not force. Recorded under #429.

## `post-control-case-study-flawed`

- **fixture** — `case-study-flawed`, the control `docs/evaluation/corpus/editorial-quality/controls/case-study-flawed.md`, candidate arm, first wording, staged from `12a1c7d2`
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the case study with the headline, standfirst and opening rewritten, the first subheading replaced and its bridging sentence cut, `Resultatet bevisar allt` → `Försökets siffror kommer med ett förbehåll`, the causal sentence cut and a closing section with its own subheading added; the missing byline and call to action reported, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1, 2 or 4 miss.
  - `C1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `post-control-column-clean`

- **fixture** — `column-clean`, the control `docs/evaluation/corpus/editorial-quality/controls/column-clean.md`, candidate arm, first wording, staged from `12a1c7d2`
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with the headline `Mötesmallen har en ruta för allt utom varför` → `Mötesmallen saknar en ruta för varför` and the call-to-action paragraph given its own closing section under a new subheading; nothing left unresolved, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `fail` — Class 1, the claim account, both judges: *Ny mellanrubrik: »Vad frågan är värd återstår att pröva« ... texten påstår därmed inget utöver det den redan gjorde* — understates the change slightly: the heading turns the ending's hedge into a label for the section.
  - `C1` — recorded, not scored — judges fail / fail.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: *Avslutningen var inget eget avsnitt ... Den som skummade mellanrubrikerna hittade därför ingen avslutning*, judge B: wrong: the ending was not missing; the section heading already announced the invitation. *Rubriken sa mer än texten*, both judges: misreads a column's deliberate hyperbole as an overclaim. Recorded under #429. Recorded, not filed: the revised wording replaced the first on this input.

## `post-control-column-flawed`

- **fixture** — `column-flawed`, the control `docs/evaluation/corpus/editorial-quality/controls/column-flawed.md`, candidate arm, first wording, staged from `12a1c7d2`
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with the headline `Möten förändrar allt` → `Vår mötesmall saknar plats för gemensam förståelse`, two filler sentences and the `Sammanfattningsvis` paragraph cut; the contradiction in the first paragraph, the unconnected scene, and the missing standfirst, sections and call to action reported and not written, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1, 2 or 4 miss.
  - `C1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `post-control-opinion-clean`

- **fixture** — `opinion-clean`, the control `docs/evaluation/corpus/editorial-quality/controls/opinion-clean.md`, candidate arm, first wording, staged from `12a1c7d2`
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the opinion piece with the last subheading's `antagandet` → `ett antagande`; nothing left unresolved, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `fail` — Class 2, a statement about the text the text contradicts, both judges: *Den bestämda formen "antagandet" pekade på ett antagande som bara rubriken nämner, eftersom varken inledningen eller något avsnitt talar om något antagande* — false: the final section's closing sentence names it ("Ett antagande blir inte ett beslutsunderlag …").
  - `C1` — recorded, not scored — judges fail / fail.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: *Texten följer artikelns anatomi utan avvikelser*, judge A: wrong after the edit, measured against the 33–40-character range the frozen expectation reports (a description of the text, not an anatomy limit; the script reported no deviation). Recorded, not filed: the revised wording replaced the first on this input.

## `post-control-opinion-flawed`

- **fixture** — `opinion-flawed`, the control `docs/evaluation/corpus/editorial-quality/controls/opinion-flawed.md`, candidate arm, first wording, staged from `12a1c7d2`
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the opinion piece returned unchanged, its one correction round rejected and reverted; ten findings reported, among them the headline, the unsupported motive, the 20 percent claim, the `Därför` conclusion, the generic subheadings, the missing standfirst and the empty call to action, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1, 2 or 4 miss.
  - `C1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `post-control-web-copy-clean`

- **fixture** — `web-copy-clean`, the control `docs/evaluation/corpus/editorial-quality/controls/web-copy-clean.md`, candidate arm, first wording, staged from `12a1c7d2`
- **invocation** — `/redline --genre=webcopy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the web page with `inom tre arbetsdagar` added to the body under the last subheading; the unlocated form reported and not written, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1, 2 or 4 miss (class 3 noted below).
  - `C1` — recorded, not scored — judges fail / fail.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: *Den som läste avsnittets text fick alltså inte veta svarstiden*, both judges: inaccurate in presenting the change as a fix: treats the heading as if it were not part of what the reader reads. *Meningen hänvisar till "formuläret" utan att texten innehåller formuläret, anger var det finns*, judge A: a false positive: "formuläret" most plausibly means the page's own form. Recorded under #432.

## `post-control-web-copy-flawed`

- **fixture** — `web-copy-flawed`, the control `docs/evaluation/corpus/editorial-quality/controls/web-copy-flawed.md`, candidate arm, first wording, staged from `12a1c7d2`
- **invocation** — `/redline --genre=webcopy --language=en_US --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the web page with the headline rewritten, the opening paragraph replaced by the offer as a paragraph and two-item list, five empty subheadings cut, `Important` → `How to express interest`, the link relabelled and moved, `shared room` → `community room` and `working days` → `business days`; whose board is meant reported, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `fail` — Class 2, a statement about the text the text contradicts, judge A: *The paragraph explaining what the form does and doesn't do ... is word for word what it was.* — literally false: that paragraph holds the changed "business days".
  - `C1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: *The one budgeted correction was accepted*, judge B: the returned text contains the whole rebuild; every change is reported. Recorded, not filed: the revised wording replaced the first on this input.

## `revise-column-sv-r1-a`

- **fixture** — `column-sv-r1`, the #362 draft `docs/evaluation/editorial-362/runs/column-sv-r1/redline/work/input.md`, revise round, revised wording, staged from `77dd847a`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with `Mallen` → `Mötesmallen` in the headline and the dash set as a Swedish en dash; the missing standfirst, sections and call to action reported and not written, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1, 2 or 4 miss (class 3 noted below).
  - `R1` — recorded, not scored — judges fail / fail.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: *Den tidigare rubriken ... sa inte vilken mall det gällde*, judge B: the input headline has no concrete visible defect; a definite-article teaser headline is ordinary column practice. *ett svenskt tankstreck med mellanrum (–)*, judge B: "med mellanrum" could be read as saying spaces were added; the input already had them. Recorded under #429.

## `revise-column-sv-r1-b`

- **fixture** — `column-sv-r1`, the #362 draft `docs/evaluation/editorial-362/runs/column-sv-r1/redline/work/input.md`, revise round, revised wording, staged from `77dd847a`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with `Mallen` → `Mötesmallen` and `poängen` → `syftet` in the headline and the dash set as a Swedish en dash; the missing standfirst, sections and call to action reported and not written, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `fail` — Class 1, the claim account, judge A: *Rubriken säger nu att mötesmallen har en ruta för allt utom syftet* — does not say that the change narrows or moves the sense of "poängen"; presents it only as a gain in clarity. Class 4, a difference no statement reports, judge B: does not mention that the column's wordplay on "poängen" is lost.
  - `R1` — recorded, not scored — judges fail / fail.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — #454, #462
- **notes** — Class 3, not counted: *ett svenskt tankstreck med mellanslag (–)*, judge A: "med mellanslag" could suggest spaces were added; the resulting form is described correctly. *Rubriken var otydlig på egen hand*, judge A: the original headline shows no concrete visible defect; the rewrite follows a stand-alone-headline guideline. *[same dash]*, judge B: "med mellanslag" could suggest spaces were added; the input already had them. *Den som ser rubriken i en lista kunde därför inte avgöra vad texten handlar om*, judge B: no concrete visible defect: a teaser headline is ordinary for a column. Recorded under #429.

## `revise-column-sv-r2-a`

- **fixture** — `column-sv-r2`, the #362 draft `docs/evaluation/editorial-362/runs/column-sv-r2/redline/work/input.md`, revise round, revised wording, staged from `77dd847a`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with the headline `Rutan som inte finns` → `Mötesmallen hoppar över varför vi behöver varandras tid` and the dash set as a Swedish en dash; the missing standfirst, sections and call to action reported and not written, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `fail` — Class 1, the claim account, judge A: *Den nya säger att mötesmallen inte frågar varför vi behöver varandras tid* — does not name the framing change: "hoppar över", and the wish stated as the template's omission.
  - `R1` — recorded, not scored — judges fail / fail.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — #455
- **notes** — Class 3, not counted: *Rubriken – reparerad*, both judges: calls the headline a repair of a defect; a matter of taste. Recorded under #429.

## `revise-column-sv-r2-b`

- **fixture** — `column-sv-r2`, the #362 draft `docs/evaluation/editorial-362/runs/column-sv-r2/redline/work/input.md`, revise round, revised wording, staged from `77dd847a`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the column with the headline `Rutan som inte finns` → `Bibliotekets mötesmall frågar inte varför vi möts` and the dash set as a Swedish en dash; the missing standfirst, sections and call to action reported and not written, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `fail` — Class 1, the claim account, judge A: *Brödtexten bär det påståendet* — holds only by paraphrase: the body names the missing box as one for a decision.
  - `R1` — recorded, not scored — judges fail / fail.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — #456
- **notes** — Class 3, not counted: *rubriken gick inte att förstå utan texten*, both judges: the alleged defect is not visible in the input; an allusive column headline is a working voice choice. Recorded under #429.

## `revise-opinion-en_GB-r1-a`

- **fixture** — `opinion-en_GB-r1`, the #362 draft `docs/evaluation/editorial-362/runs/opinion-en_GB-r1/redline/work/input.md`, revise round, revised wording, staged from `77dd847a`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the opinion piece with the byline moved up, the pilot and motive paragraphs each split in two and the third subheading rewritten; the missing standfirst reported, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `fail` — Class 1, the claim account, judge A: *[third subheading entry]* — two effects go unreported: "the phone or the web" narrowed to "why people ring", and the added ordering word "First". Class 1, the claim account, judge B: *the board should first find out what each route costs staff* — does not mention the narrowing to "why people ring"; the gloss puts an actor on the finding-out that is neither in the heading nor in the body.
  - `R1` — recorded, not scored — judges fail / fail.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — #457
- **notes** — Class 3, not counted: *The byline was at the end*, both judges: stated reason is a judgement of taste, not a visible defect. Recorded under #429.

## `revise-opinion-en_GB-r1-b`

- **fixture** — `opinion-en_GB-r1`, the #362 draft `docs/evaluation/editorial-362/runs/opinion-en_GB-r1/redline/work/input.md`, revise round, revised wording, staged from `77dd847a`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the opinion piece with the byline moved up, `Lervik's` added to the lead and the third subheading rewritten; the missing standfirst reported, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1, 2 or 4 miss (class 3 noted below).
  - `R1` — recorded, not scored — judges fail / fail.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: *"the council executive board" didn't say which council; only the headline did*, judge A: true, but leaves out that section 1 also names Lervik ("Lervik's residents"); what it calls a defect is not a real one. *[third subheading] a list of nouns with no verb; repeated the first sentence under it*, judge A: preferences, not defects. *"Öppna beslut" (and the "We") appeared in section 3 without having been introduced*, judge B: overstated: Öppna beslut is introduced where it first appears ("Öppna beslut proposes …"). *the new heading states the author's demand, which the section's last sentence already makes*, judge B: the last sentence is a condition, not a demand; its wording ("set the work each route costs staff against what it is worth") is in that sentence. *a list of nouns with no verb*, judge B: applies equally to the second subheading, which was kept; a preference, not a visible defect. Recorded under #429.

## `revise-opinion-en_GB-r2-a`

- **fixture** — `opinion-en_GB-r2`, the #362 draft `docs/evaluation/editorial-362/runs/opinion-en_GB-r2/redline/work/input.md`, revise round, revised wording, staged from `77dd847a`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the opinion piece with `By` added to the byline, `telephone and web` added to the lead, `for which I am spokesperson` added after `Öppna beslut` in section 3 and the last section opening `The municipal executive board can`; the missing standfirst and what Öppna beslut is reported, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `fail` — Class 2, a statement about the text the text contradicts, both judges: *The body didn't say whose proposal it was, or who "we" were* — false: the input's body says "Öppna beslut proposes".
  - `R1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — #451
- **notes** — Class 3, not counted: *Byline: it lacked the English byline form*, both judges: overstates the problem: the byline worked as it was. Recorded under #429.

## `revise-opinion-en_GB-r2-b`

- **fixture** — `opinion-en_GB-r2`, the #362 draft `docs/evaluation/editorial-362/runs/opinion-en_GB-r2/redline/work/input.md`, revise round, revised wording, staged from `77dd847a`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the opinion piece with `By` added to the byline and the last section opening `The board can` instead of `It can`; the missing standfirst reported, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `fail` — Class 2, a statement about the text the text contradicts, judge B: *The final text measures as follows: … no paragraph is over 65 words* — the returned final paragraph is 66 words (65 in the input); the measuring script gives 66 on the returned text.
  - `R1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — #452
- **notes** — Class 3, not counted: *[byline] read like a caption, not a byline*, both judges: the description of the change is accurate; the reply frames taste as a defect. Recorded under #429.

## `revise-control-column-clean`

- **fixture** — `column-clean`, the control `docs/evaluation/corpus/editorial-quality/controls/column-clean.md`, revise round, revised wording, staged from `77dd847a`
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — no text returned: the reply says no change was needed, and gives its account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1, 2 or 4 miss.
  - `C1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `revise-control-opinion-clean`

- **fixture** — `opinion-clean`, the control `docs/evaluation/corpus/editorial-quality/controls/opinion-clean.md`, revise round, revised wording, staged from `77dd847a`
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the opinion piece with `digital bokning och telefonbokning` added after `båda bokningsvägarna` in the body's first paragraph; nothing left unresolved, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1, 2 or 4 miss.
  - `C1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `revise-control-web-copy-flawed`

- **fixture** — `web-copy-flawed`, the control `docs/evaluation/corpus/editorial-quality/controls/web-copy-flawed.md`, revise round, revised wording, staged from `77dd847a`
- **invocation** — `/redline --genre=webcopy --language=en_US --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the web page with the headline rewritten, the opening paragraph cut, the four one-sentence sections merged under `Price and contents of the review`, `Important` → `How to express interest`, the link relabelled and moved, and `working days` → `business days`; nothing left unresolved, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it, the staged Skills unchanged and no temporary file left; the root was removed.
- **criteria** —
  - `A2` — `fail` — Class 2, a statement about the text the text contradicts, both judges: *Seven headings became two* — the input has seven headings (one H1, six H2s); the output has three (one H1, two H2s).
  - `C1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — #453
- **notes** — Class 3, not counted: *I made one correction*, judge B: ambiguous beside "all six fixed"; it appears to mean one correction round.

## `revise-column-sv-r2-b`, void

- **fixture** — `column-sv-r2`, the #362 draft `docs/evaluation/editorial-362/runs/column-sv-r2/redline/work/input.md`, revise round, staged from `77dd847a`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — no delivery: the session ended with `terminal_reason: api_error` and returned only *Failed to authenticate. API Error: 401 OAuth access token has been revoked.*
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - every criterion — `skipped` — void: cut off by an expired login, which the plan's *Void runs* treats as a condition of the environment, not a finding. The packet is under `../editorial-435/voided/revise-column-sv-r2-b/`, and the run was made again from the same commit; its counted entry is above.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — not judged.

## `revise-opinion-en_GB-r1-b`, void

- **fixture** — `opinion-en_GB-r1`, the #362 draft `docs/evaluation/editorial-362/runs/opinion-en_GB-r1/redline/work/input.md`, revise round, staged from `77dd847a`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — no delivery: the session ended with `terminal_reason: api_error` and returned only *Failed to authenticate. API Error: 401 OAuth access token has been revoked.*
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - every criterion — `skipped` — void: cut off by an expired login, which the plan's *Void runs* treats as a condition of the environment, not a finding. The packet is under `../editorial-435/voided/revise-opinion-en_GB-r1-b/`, and the run was made again from the same commit; its counted entry is above.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — not judged.

## `revise-opinion-en_GB-r2-b`, void

- **fixture** — `opinion-en_GB-r2`, the #362 draft `docs/evaluation/editorial-362/runs/opinion-en_GB-r2/redline/work/input.md`, revise round, staged from `77dd847a`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — no delivery: the session ended with `terminal_reason: api_error` and returned only *Failed to authenticate. API Error: 401 OAuth access token has been revoked.*
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - every criterion — `skipped` — void: cut off by an expired login, which the plan's *Void runs* treats as a condition of the environment, not a finding. The packet is under `../editorial-435/voided/revise-opinion-en_GB-r2-b/`, and the run was made again from the same commit; its counted entry is above.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — not judged.

## `revise-control-column-clean`, void

- **fixture** — `column-clean`, the control `docs/evaluation/corpus/editorial-quality/controls/column-clean.md`, revise round, staged from `77dd847a`
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — no delivery: the session ended with `terminal_reason: api_error` and returned only *Failed to authenticate. API Error: 401 OAuth access token has been revoked.*
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - every criterion — `skipped` — void: cut off by an expired login, which the plan's *Void runs* treats as a condition of the environment, not a finding. The packet is under `../editorial-435/voided/revise-control-column-clean/`, and the run was made again from the same commit; its counted entry is above.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — not judged.

## `revise-control-opinion-clean`, void

- **fixture** — `opinion-clean`, the control `docs/evaluation/corpus/editorial-quality/controls/opinion-clean.md`, revise round, staged from `77dd847a`
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — no delivery: the session ended with `terminal_reason: api_error` and returned only *Failed to authenticate. API Error: 401 OAuth access token has been revoked.*
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - every criterion — `skipped` — void: cut off by an expired login, which the plan's *Void runs* treats as a condition of the environment, not a finding. The packet is under `../editorial-435/voided/revise-control-opinion-clean/`, and the run was made again from the same commit; its counted entry is above.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — not judged.

## `revise-control-web-copy-flawed`, void

- **fixture** — `web-copy-flawed`, the control `docs/evaluation/corpus/editorial-quality/controls/web-copy-flawed.md`, revise round, staged from `77dd847a`
- **invocation** — `/redline --genre=webcopy --language=en_US --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — no delivery: the session ended with `terminal_reason: api_error` and returned only *Failed to authenticate. API Error: 401 OAuth access token has been revoked.*
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged and no temporary file left; the root was removed.
- **criteria** —
  - every criterion — `skipped` — void: cut off by an expired login, which the plan's *Void runs* treats as a condition of the environment, not a finding. The packet is under `../editorial-435/voided/revise-control-web-copy-flawed/`, and the run was made again from the same commit; its counted entry is above.
- **unresolved findings** — none
- **defects filed** — none
- **notes** — not judged.
