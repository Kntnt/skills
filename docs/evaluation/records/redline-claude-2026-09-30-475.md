# redline — claude — 2026-09-30 — #475

- **record** — `redline-claude-2026-09-30-475`
- **date** — `2026-09-30`
- **ticket** — `#475`
- **skill** — `redline`
- **provider family** — `claude`
- **model** — `claude-opus-5-5` at high deliberation, for every run session, every correction subagent, checker and nested Proofread pass in it, and every judge
- **harness** — Claude Code 2.1.285
- **corpus commit** — `41fd4c55`

## Run conditions

The evaluation covers two arms over the four #362 drafts and the ten *Redline controls* rows. Each of the five clean controls also ran once to a file, as the protocol's *A clean control* requires. The pre-change arm was staged from `41fd4c55`, the commit #475's build started from. The candidate arm was staged from `29d4b674`, which adds the reply checker (`skills/editorial/redline/references/reply-check.md`) and the step 11 instruction that starts it. The method is #435's, with the changes #475's readiness addenda settle. It was frozen for this ticket in [`../editorial-475/plan.md`](../editorial-475/plan.md) in `1c9303a0`, before the first run. The whole evaluation is written up in [`../editorial-475/results.md`](../editorial-475/results.md), and every run's packet is under [`../editorial-475/runs/`](../editorial-475/runs/).

**How each run was made.** Each run was a fresh top-level Claude Code session started by [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py). The Formal Invocation was its whole prompt. The editorial Skills and the Manager were staged by `git archive` into a private root of its own. The runs were made from 14:49 to 15:30 UTC on 30 September. No run was void.

**How each run was judged.** Every run was judged by two fresh judges, blind to the arm, the model and the ticket:

- the drafts with #435's `redline-judge-brief.md`;
- the response-target controls with #435's `control-judge-brief.md`;
- the file-target controls with #429's `control-judge-brief-file.md`.

Each brief was used byte for byte. No Codex Harness and no GPT model was started, controlled or invoked.

**This evaluation's own criteria.** There are four:

- **`A2`**, read as the plan reads it. Every miss a judge records is put in one of four classes:
  1. the claim account;
  2. a statement about a text that the text contradicts;
  3. a statement true of its text that the judge faults for what it suggests;
  4. an omission of a difference that moves no claim.

  A response-target run fails `A2` here where it carries a class 1 or class 2 miss. One judge is enough. Class 3 is noted without failing it. A file-target run's `A2` is recorded, not counted.
- **`C1`**, each control judge's heading-4 verdict. It passes where both judges pass. A clean control's `C1` is read from its file-target run and a flawed control's from its response-target run.
- **`O1`**.
- **`S1`**.

`R1` on the drafts is recorded as the judges give it, and not scored.

## `pre-column-sv-r1-a`

- **fixture** — `column-sv-r1`, `docs/evaluation/editorial-362/runs/column-sv-r1/redline/work/input.md`, pre-change arm, staged from `41fd4c55`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, differing from the input in 1 line, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `R1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: judge B on *Korrekturläsningen på slutet bytte det engelska långa tankstrecket i ”formuläret — bibliotekarien” m*.

## `pre-column-sv-r1-b`

- **fixture** — `column-sv-r1`, `docs/evaluation/editorial-362/runs/column-sv-r1/redline/work/input.md`, pre-change arm, staged from `41fd4c55`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, differing from the input in 1 line, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `R1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `pre-column-sv-r2-a`

- **fixture** — `column-sv-r2`, `docs/evaluation/editorial-362/runs/column-sv-r2/redline/work/input.md`, pre-change arm, staged from `41fd4c55`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, differing from the input in 2 lines, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `R1` — recorded, not scored — judges fail / fail.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: judge A on *Den gamla rubriken ”Rutan som inte finns” nämnde inget ämne*; judge B on *Den gamla rubriken ”Rutan som inte finns” nämnde inget ämne.*

## `pre-column-sv-r2-b`

- **fixture** — `column-sv-r2`, `docs/evaluation/editorial-362/runs/column-sv-r2/redline/work/input.md`, pre-change arm, staged from `41fd4c55`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, differing from the input in 2 lines, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `fail` — class 1, the claim account (changed), judge A: *Rubriken påstår nu att mötesmallen saknar en ruta för varför vi ses. Tidigare sade den bara att en viss ruta inte finns, utan att säga vilken. ... [finding 1:] påstår inte mer än texten gör*; class 1, the claim account (changed), judge B: *Rubriken påstår nu att mötesmallen saknar en ruta för varför vi ses. Tidigare sade den bara att en viss ruta inte finns, utan att säga vilken.*
  - `R1` — recorded, not scored — judges fail / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `pre-control-article-clean`

- **fixture** — `article-clean`, `docs/evaluation/corpus/editorial-quality/controls/article-clean.md`, pre-change arm, staged from `41fd4c55`
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the short no-change status in the response, with no text.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `C1` — recorded, not scored — judges pass / pass; a clean control's `C1` is read from its file-target run.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `pre-control-article-clean-file`

- **fixture** — `article-clean`, `docs/evaluation/corpus/editorial-quality/controls/article-clean.md`, pre-change arm, staged from `41fd4c55`
- **invocation** — `/redline --genre=article --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, differing from it in 1 line, and the run's account in the response.
- **side effects** — `work/output.md` created beside the input, as asked; nothing else: the runner's inventories of the private root show `work/input.md` unchanged and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — recorded, not counted — a file-target run; no judge records a class 1 or class 2 miss.
  - `C1` — `fail` — judges fail / fail at heading 4, read from the delivered `output.md`.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed, beyond the requested `work/output.md`.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: judge A on *Det nya påståendet är textens egen rekommendation, alltså Rasks råd och uppmaningen i slutet* (#468); judge B on *Rubriken upprepade ingressen (åtgärdat). ... Båda använde orden ”inte varför”* (#468); judge B on *Det nya påståendet är textens egen rekommendation, alltså Rasks råd och uppmaningen i slutet* (#468).

## `pre-control-article-flawed`

- **fixture** — `article-flawed`, `docs/evaluation/corpus/editorial-quality/controls/article-flawed.md`, pre-change arm, staged from `41fd4c55`
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, identical to the input, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `C1` — `pass` — judges pass / pass at heading 4.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `pre-control-case-study-clean`

- **fixture** — `case-study-clean`, `docs/evaluation/corpus/editorial-quality/controls/case-study-clean.md`, pre-change arm, staged from `41fd4c55`
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, differing from the input in 2 lines, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `fail` — class 1, the claim account (changed), judge A: *Ingressen lovar nu att visa vad underhållsgruppen gjorde och vad gruppens egna anteckningar visar. [...] Omfång, säkerhet och tidsföljd är desamma.*
  - `C1` — recorded, not scored — judges pass / fail; a clean control's `C1` is read from its file-target run.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: judge B on *Texten följer artikelanatomin utan avvikelser. Allt som skriptet räknar håller, och ingressen har 42* (#468); judge B on *Ingressen hade inte introducerat någon grupp eller några anteckningar, så den som läste ingressen en* (#468).

## `pre-control-case-study-clean-file`

- **fixture** — `case-study-clean`, `docs/evaluation/corpus/editorial-quality/controls/case-study-clean.md`, pre-change arm, staged from `41fd4c55`
- **invocation** — `/redline --genre=casestudy --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, byte-identical to it, and the run's account in the response.
- **side effects** — `work/output.md` created beside the input, as asked; nothing else: the runner's inventories of the private root show `work/input.md` unchanged and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — recorded, not counted — a file-target run; no judge records a class 1 or class 2 miss.
  - `C1` — `pass` — judges pass / pass at heading 4, read from the delivered `output.md`.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed, beyond the requested `work/output.md`.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `pre-control-case-study-flawed`

- **fixture** — `case-study-flawed`, `docs/evaluation/corpus/editorial-quality/controls/case-study-flawed.md`, pre-change arm, staged from `41fd4c55`
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, differing from the input in 7 lines, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `fail` — class 2 (round), judge A: *Rubrik, ingress och inledningsstycke skrevs om, och alla tre mellanrubriker ersattes.*
  - `C1` — `pass` — judges pass / pass at heading 4.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `pre-control-column-clean`

- **fixture** — `column-clean`, `docs/evaluation/corpus/editorial-quality/controls/column-clean.md`, pre-change arm, staged from `41fd4c55`
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, identical to the input, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `C1` — recorded, not scored — judges fail / pass; a clean control's `C1` is read from its file-target run.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: judge A on *Uppmaningen saknar ett eget avsnitt. ... Artikelanatomin kräver att slutet är ett eget avsnitt med e* (#464); judge B on *Uppmaningen saknar ett eget avsnitt. ... Artikelanatomin kräver att slutet är ett eget avsnitt med e* (#464).

## `pre-control-column-clean-file`

- **fixture** — `column-clean`, `docs/evaluation/corpus/editorial-quality/controls/column-clean.md`, pre-change arm, staged from `41fd4c55`
- **invocation** — `/redline --genre=column --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, differing from it in 1 line, and the run's account in the response.
- **side effects** — `work/output.md` created beside the input, as asked; nothing else: the runner's inventories of the private root show `work/input.md` unchanged and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — recorded, not counted — a file-target run; no judge records a class 1 or class 2 miss.
  - `C1` — `fail` — judges fail / fail at heading 4, read from the delivered `output.md` (#464).
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed, beyond the requested `work/output.md`.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: judge A on *Avslutningen var inte ett eget avsnitt. Uppmaningen ("Prova ändå frågan nästa gång du bokar ett möte* (#464); judge B on *Avslutningen var inte ett eget avsnitt* (#464).

## `pre-control-column-flawed`

- **fixture** — `column-flawed`, `docs/evaluation/corpus/editorial-quality/controls/column-flawed.md`, pre-change arm, staged from `41fd4c55`
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, differing from the input in 2 lines, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `C1` — `pass` — judges pass / pass at heading 4.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `pre-control-opinion-clean`

- **fixture** — `opinion-clean`, `docs/evaluation/corpus/editorial-quality/controls/opinion-clean.md`, pre-change arm, staged from `41fd4c55`
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, differing from the input in 1 line, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `fail` — class 2 (finding), judge A: *En läsare som hoppar över den fetade ingressen fick inte veta att telefonbokningen var den väg texten vill behålla. Det framgick först i nästa avsnitt*; class 2 (finding), judge B: *Det skrev ”båda bokningsvägarna” utan att säga vilka de två vägarna var. ... En läsare som hoppar över den fetade ingressen fick inte veta att telefonbokningen var den väg texten vill behålla. Det fra*.
  - `C1` — recorded, not scored — judges fail / fail; a clean control's `C1` is read from its file-target run.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: judge B on *Ändrat påstående. I inledningsstycket står nu uttryckligen att de två vägar som ska prövas i alla sj* (#468).

## `pre-control-opinion-clean-file`

- **fixture** — `opinion-clean`, `docs/evaluation/corpus/editorial-quality/controls/opinion-clean.md`, pre-change arm, staged from `41fd4c55`
- **invocation** — `/redline --genre=opinion --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, byte-identical to it, and the run's account in the response.
- **side effects** — `work/output.md` created beside the input, as asked; nothing else: the runner's inventories of the private root show `work/input.md` unchanged and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — recorded, not counted — a file-target run; no judge records a class 1 or class 2 miss.
  - `C1` — `pass` — judges pass / pass at heading 4, read from the delivered `output.md`.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed, beyond the requested `work/output.md`.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `pre-control-opinion-flawed`

- **fixture** — `opinion-flawed`, `docs/evaluation/corpus/editorial-quality/controls/opinion-flawed.md`, pre-change arm, staged from `41fd4c55`
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, identical to the input, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `C1` — `pass` — judges pass / pass at heading 4.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `pre-control-web-copy-clean`

- **fixture** — `web-copy-clean`, `docs/evaluation/corpus/editorial-quality/controls/web-copy-clean.md`, pre-change arm, staged from `41fd4c55`
- **invocation** — `/redline --genre=webcopy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the short no-change status in the response, with no text.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `C1` — recorded, not scored — judges pass / pass; a clean control's `C1` is read from its file-target run.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `pre-control-web-copy-clean-file`

- **fixture** — `web-copy-clean`, `docs/evaluation/corpus/editorial-quality/controls/web-copy-clean.md`, pre-change arm, staged from `41fd4c55`
- **invocation** — `/redline --genre=webcopy --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, byte-identical to it, and the run's account in the response.
- **side effects** — `work/output.md` created beside the input, as asked; nothing else: the runner's inventories of the private root show `work/input.md` unchanged and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — recorded, not counted — a file-target run; no judge records a class 1 or class 2 miss.
  - `C1` — `pass` — judges pass / pass at heading 4, read from the delivered `output.md`.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed, beyond the requested `work/output.md`.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `pre-control-web-copy-flawed`

- **fixture** — `web-copy-flawed`, `docs/evaluation/corpus/editorial-quality/controls/web-copy-flawed.md`, pre-change arm, staged from `41fd4c55`
- **invocation** — `/redline --genre=webcopy --language=en_US --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, differing from the input in 6 lines, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `C1` — `pass` — judges pass / pass at heading 4.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: judge A on *four one-sentence sections became one sentence and a two-item list*.

## `pre-opinion-en_GB-r1-a`

- **fixture** — `opinion-en_GB-r1`, `docs/evaluation/editorial-362/runs/opinion-en_GB-r1/redline/work/input.md`, pre-change arm, staged from `41fd4c55`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, differing from the input in 3 lines, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `R1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: judge A on *Four recommended limits are exceeded, and I didn't treat them as findings:*; judge A on *Two short passages in the lead and the second section were reworded, as listed above*; judge B on *The byline was at the end instead of after the headline (fixed)*; judge B on *Four recommended limits are exceeded, and I didn't treat them as findings:*; judge B on *Two short passages in the lead and the second section were reworded, as listed above.*

## `pre-opinion-en_GB-r1-b`

- **fixture** — `opinion-en_GB-r1`, `docs/evaluation/editorial-362/runs/opinion-en_GB-r1/redline/work/input.md`, pre-change arm, staged from `41fd4c55`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, differing from the input in 4 lines, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `R1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: judge A on *Author name in the wrong place (fixed). … Readers went through the whole argument, including its "I"*; judge A on *Changed (finding 3): in the proposed trial, officers now do the time recording and the user survey,*.

## `pre-opinion-en_GB-r2-a`

- **fixture** — `opinion-en_GB-r2`, `docs/evaluation/editorial-362/runs/opinion-en_GB-r2/redline/work/input.md`, pre-change arm, staged from `41fd4c55`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, differing from the input in 2 lines, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `R1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: judge A on *Byline (fixed). The byline read *Sanna Ek, spokesperson for Öppna beslut*. An English byline takes t*; judge B on *Byline (fixed). [...] An English byline takes the form "By <author>", so it now reads *By Sanna Ek,*.

## `pre-opinion-en_GB-r2-b`

- **fixture** — `opinion-en_GB-r2`, `docs/evaluation/editorial-362/runs/opinion-en_GB-r2/redline/work/input.md`, pre-change arm, staged from `41fd4c55`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, differing from the input in 4 lines, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `fail` — class 2 (count), judge A: *Apart from the two changes to claims above, this run changed three things: it put the byline in the English form; it named the board in the body of the ending; it named the two booking routes in the l*; class 2 (count), judge B: *Apart from the two changes to claims above, this run changed three things*.
  - `R1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: judge A on *Byline: it didn't use the English form "By <author>", so it read like an unlabelled caption. It now*; judge A on *Changed: the lead now says the two routes to keep are web and telephone (fix 3). The text already sa*; judge B on *Byline: it didn't use the English form "By <author>", so it read like an unlabelled caption. It now*; judge B on *Changed: the lead now says the two routes to keep are web and telephone (fix 3). The text already sa*; judge B on *Changed: section "Six months would produce the figures". The author's position now names the cost to*.

## `post-column-sv-r1-a`

- **fixture** — `column-sv-r1`, `docs/evaluation/editorial-362/runs/column-sv-r1/redline/work/input.md`, candidate arm, staged from `29d4b674`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, differing from the input in 1 line, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `R1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: judge B on *Mätningen räknar därför det inledande stycket som sju stycken, men det felet följer bara av att avsn*.

## `post-column-sv-r1-b`

- **fixture** — `column-sv-r1`, `docs/evaluation/editorial-362/runs/column-sv-r1/redline/work/input.md`, candidate arm, staged from `29d4b674`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, differing from the input in 1 line, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `R1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `post-column-sv-r2-a`

- **fixture** — `column-sv-r2`, `docs/evaluation/editorial-362/runs/column-sv-r2/redline/work/input.md`, candidate arm, staged from `29d4b674`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, differing from the input in 2 lines, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `R1` — recorded, not scored — judges fail / fail.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: judge A on *”Rutan som inte finns” angav inget ämne* (#468); judge B on *Den dubbla betydelsen är borta* (#468).

## `post-column-sv-r2-b`

- **fixture** — `column-sv-r2`, `docs/evaluation/editorial-362/runs/column-sv-r2/redline/work/input.md`, candidate arm, staged from `29d4b674`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, differing from the input in 2 lines, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `R1` — recorded, not scored — judges fail / fail.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: judge A on *Åtgärdat – rubriken namngav inget ämne. ”Rutan som inte finns” säger att en ruta saknas men inte var*; judge B on *Åtgärdat – rubriken namngav inget ämne.*

## `post-control-article-clean`

- **fixture** — `article-clean`, `docs/evaluation/corpus/editorial-quality/controls/article-clean.md`, candidate arm, staged from `29d4b674`
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the short no-change status in the response, with no text.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `C1` — recorded, not scored — judges pass / pass; a clean control's `C1` is read from its file-target run.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `post-control-article-clean-file`

- **fixture** — `article-clean`, `docs/evaluation/corpus/editorial-quality/controls/article-clean.md`, candidate arm, staged from `29d4b674`
- **invocation** — `/redline --genre=article --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, differing from it in 1 line, and the run's account in the response.
- **side effects** — `work/output.md` created beside the input, as asked; nothing else: the runner's inventories of the private root show `work/input.md` unchanged and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — recorded, not counted — a file-target run; no judge records a class 1 or class 2 miss.
  - `C1` — `pass` — judges pass / pass at heading 4, read from the delivered `output.md`.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed, beyond the requested `work/output.md`.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `post-control-article-flawed`

- **fixture** — `article-flawed`, `docs/evaluation/corpus/editorial-quality/controls/article-flawed.md`, candidate arm, staged from `29d4b674`
- **invocation** — `/redline --genre=article --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, differing from the input in 7 lines, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `C1` — `pass` — judges pass / pass at heading 4.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `post-control-case-study-clean`

- **fixture** — `case-study-clean`, `docs/evaluation/corpus/editorial-quality/controls/case-study-clean.md`, candidate arm, staged from `29d4b674`
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, differing from the input in 3 lines, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `fail` — class 2 (finding), judge A: *Men texten redovisar bara en intern försöksanteckning från Elm Quay, och den säger uttryckligen att skillnaden i mediantid inte beror på programvaran*; class 1, the claim account (changed), judge A: *Det är nu Maya Lind som berättar vad försöket krävde, inte anteckningar*; class 2 (finding), judge B: *den säger uttryckligen att skillnaden i mediantid inte beror på programvaran*; class 1, the claim account (changed), judge B: *Det är nu Maya Lind som berättar vad försöket krävde, inte anteckningar.*
  - `C1` — recorded, not scored — judges fail / fail; a clean control's `C1` is read from its file-target run.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — #477, #478
- **notes** — Class 3, not counted: judge A on *Rubriken – ”Elm Quay samlade reparationsärendena” var för generell. Bestämd form utan avgränsning lä* (#463); judge A on *Inledningen, andra meningen – ”Försöket” i bestämd form syftade bara tillbaka på ingressen* (#468); judge B on *Rubriken – ”Elm Quay samlade reparationsärendena” var för generell. [...] Den som bara såg rubriken* (#463); judge B on *Inledningen, andra meningen – ”Försöket” i bestämd form syftade bara tillbaka på ingressen* (#468).

## `post-control-case-study-clean-file`

- **fixture** — `case-study-clean`, `docs/evaluation/corpus/editorial-quality/controls/case-study-clean.md`, candidate arm, staged from `29d4b674`
- **invocation** — `/redline --genre=casestudy --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, differing from it in 2 lines, and the run's account in the response.
- **side effects** — `work/output.md` created beside the input, as asked, and macOS's Python bytecode cache under the private `HOME/Library/Caches`; nothing else: the runner's inventories of the private root show `work/input.md` unchanged and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — recorded, not counted — a file-target run; no judge records a class 1 or class 2 miss.
  - `C1` — `fail` — judges fail / fail at heading 4, read from the delivered `output.md` (recorded under #468; see results).
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed, beyond the requested `work/output.md`.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: judge A on *Inledningen, andra meningen. ”Försöket” syftade på ett försök som bara ingressen berättade om. Den s* (#468); judge B on *Inledningen, andra meningen. ”Försöket” syftade på ett försök som bara ingressen berättade om* (#468); judge B on *Mätskriptet mätte gränserna på den levererade texten: rubriken har 36 tecken, ingressen 43 ord och i* (#468).

## `post-control-case-study-flawed`

- **fixture** — `case-study-flawed`, `docs/evaluation/corpus/editorial-quality/controls/case-study-flawed.md`, candidate arm, staged from `29d4b674`
- **invocation** — `/redline --genre=casestudy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, differing from the input in 9 lines, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `C1` — `pass` — judges pass / pass at heading 4.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `post-control-column-clean`

- **fixture** — `column-clean`, `docs/evaluation/corpus/editorial-quality/controls/column-clean.md`, candidate arm, staged from `29d4b674`
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the short no-change status in the response, with no text.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `C1` — recorded, not scored — judges pass / pass; a clean control's `C1` is read from its file-target run.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `post-control-column-clean-file`

- **fixture** — `column-clean`, `docs/evaluation/corpus/editorial-quality/controls/column-clean.md`, candidate arm, staged from `29d4b674`
- **invocation** — `/redline --genre=column --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, differing from it in 1 line, and the run's account in the response.
- **side effects** — `work/output.md` created beside the input, as asked; nothing else: the runner's inventories of the private root show `work/input.md` unchanged and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — recorded, not counted — a file-target run; no judge records a class 1 or class 2 miss.
  - `C1` — `fail` — judges fail / fail at heading 4, read from the delivered `output.md` (#464).
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed, beyond the requested `work/output.md`.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: judge A on *Slutet saknade ett eget avsnitt. ... Det sista avsnittet, ”Ännu en ruta, och ändå vill jag prova”, i* (#464); judge A on *Texten följer artikelanatomin. Mätskriptet godkänner de räknade kraven i den levererade texten. ..* (#464); judge B on *Krav: Artikelanatomin kräver att slutet är ett eget avsnitt med en egen mellanrubrik. ... Reparation* (#464).

## `post-control-column-flawed`

- **fixture** — `column-flawed`, `docs/evaluation/corpus/editorial-quality/controls/column-flawed.md`, candidate arm, staged from `29d4b674`
- **invocation** — `/redline --genre=column --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, differing from the input in 2 lines, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `C1` — `pass` — judges pass / pass at heading 4.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `post-control-opinion-clean`

- **fixture** — `opinion-clean`, `docs/evaluation/corpus/editorial-quality/controls/opinion-clean.md`, candidate arm, staged from `29d4b674`
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the short no-change status in the response, with no text.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `C1` — recorded, not scored — judges pass / pass; a clean control's `C1` is read from its file-target run.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `post-control-opinion-clean-file`

- **fixture** — `opinion-clean`, `docs/evaluation/corpus/editorial-quality/controls/opinion-clean.md`, candidate arm, staged from `29d4b674`
- **invocation** — `/redline --genre=opinion --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, byte-identical to it, and the run's account in the response.
- **side effects** — `work/output.md` created beside the input, as asked; nothing else: the runner's inventories of the private root show `work/input.md` unchanged and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — recorded, not counted — a file-target run; no judge records a class 1 or class 2 miss.
  - `C1` — `pass` — judges pass / pass at heading 4, read from the delivered `output.md`.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed, beyond the requested `work/output.md`.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `post-control-opinion-flawed`

- **fixture** — `opinion-flawed`, `docs/evaluation/corpus/editorial-quality/controls/opinion-flawed.md`, candidate arm, staged from `29d4b674`
- **invocation** — `/redline --genre=opinion --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, differing from the input in 8 lines, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `C1` — `pass` — judges pass / pass at heading 4.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: judge A on *Övriga delar finns i rätt ordning. Sista avsnittet är ett eget slutavsnitt, och varje mellanrubrik b*; judge A on *Ändrade: Mellanrubriken ”Kommunstyrelsen bör ge telefonbokningen en chans” återger förslaget i först*.

## `post-control-web-copy-clean`

- **fixture** — `web-copy-clean`, `docs/evaluation/corpus/editorial-quality/controls/web-copy-clean.md`, candidate arm, staged from `29d4b674`
- **invocation** — `/redline --genre=webcopy --language=sv --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the short no-change status in the response, with no text.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `C1` — recorded, not scored — judges pass / pass; a clean control's `C1` is read from its file-target run.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `post-control-web-copy-clean-file`

- **fixture** — `web-copy-clean`, `docs/evaluation/corpus/editorial-quality/controls/web-copy-clean.md`, candidate arm, staged from `29d4b674`
- **invocation** — `/redline --genre=webcopy --language=sv --output=output.md input.md`
- **contextual instruction** — `none`
- **output target** — `output.md`
- **observed delivery** — `output.md` written beside the input, byte-identical to it, and the run's account in the response.
- **side effects** — `work/output.md` created beside the input, as asked; nothing else: the runner's inventories of the private root show `work/input.md` unchanged and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — recorded, not counted — a file-target run; no judge records a class 1 or class 2 miss.
  - `C1` — `pass` — judges pass / pass at heading 4, read from the delivered `output.md`.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed, beyond the requested `work/output.md`.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `post-control-web-copy-flawed`

- **fixture** — `web-copy-flawed`, `docs/evaluation/corpus/editorial-quality/controls/web-copy-flawed.md`, candidate arm, staged from `29d4b674`
- **invocation** — `/redline --genre=webcopy --language=en_US --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, differing from the input in 5 lines, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `C1` — `pass` — judges pass / pass at heading 4.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — none

## `post-opinion-en_GB-r1-a`

- **fixture** — `opinion-en_GB-r1`, `docs/evaluation/editorial-362/runs/opinion-en_GB-r1/redline/work/input.md`, candidate arm, staged from `29d4b674`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, differing from the input in 1 line, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `R1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: judge A on *Before, readers didn't learn who was making the argument until the last line. That meant "Öppna besl*; judge A on *Without that paragraph, the body never says what the board is being asked to decide: removing phone*; judge B on *Fixed: the byline was in the wrong place and the wrong form. [...] Before, readers didn't learn who*.

## `post-opinion-en_GB-r1-b`

- **fixture** — `opinion-en_GB-r1`, `docs/evaluation/editorial-362/runs/opinion-en_GB-r1/redline/work/input.md`, candidate arm, staged from `29d4b674`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, differing from the input in 2 lines, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `R1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: judge B on *Byline out of place (repaired). ... A reader therefore met "Öppna beslut proposes…" and "We make no* (#468); judge B on *Lead relied on the headline (repaired). The lead said "the council executive board" and "all seven c* (#468).

## `post-opinion-en_GB-r2-a`

- **fixture** — `opinion-en_GB-r2`, `docs/evaluation/editorial-362/runs/opinion-en_GB-r2/redline/work/input.md`, candidate arm, staged from `29d4b674`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, differing from the input in 3 lines, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `R1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: judge A on *Fixed: the byline lacked the English "By" form. … Directly under the headline, it could be read as a*; judge B on *Fixed: the byline lacked the English "By" form. … Directly under the headline, it could be read as a*.

## `post-opinion-en_GB-r2-b`

- **fixture** — `opinion-en_GB-r2`, `docs/evaluation/editorial-362/runs/opinion-en_GB-r2/redline/work/input.md`, candidate arm, staged from `29d4b674`
- **invocation** — `/redline --output=response input.md`
- **contextual instruction** — `none`
- **output target** — `response`
- **observed delivery** — the text in the response, differing from the input in 4 lines, and the run's account.
- **side effects** — `none`: the runner's inventories of the private root show `work/input.md` unchanged, nothing created beside it and the staged Skills unchanged; the root was removed.
- **criteria** —
  - `A2` — `pass` — no judge records a class 1 or class 2 miss.
  - `R1` — recorded, not scored — judges pass / pass.
  - `O1` — `pass` — no path outside the Harness's configuration and caches created, changed or removed.
  - `S1` — `pass` — `input.md` was the only file in the working directory when the session started.
  - `T1`, `R2` — `skipped` — not this evaluation's criteria; the packet keeps the trace.
  - `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2`, `T2` — `skipped` — not this evaluation's criteria.
- **unresolved findings** — as the reply lists them; see the packet's `response.txt`
- **defects filed** — none
- **notes** — Class 3, not counted: judge A on *"It" relied on the subheading to supply "the board". Without the subheading, the nearest possible me*; judge B on *One claim changed: the lead now says the two routes are the telephone and the web (finding 3). Befor*.
