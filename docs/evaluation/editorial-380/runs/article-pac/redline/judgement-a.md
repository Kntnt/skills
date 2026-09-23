# Redline judgement A — row `article-pac`

Genre from the text's own `kntnt` map: `article`. The fixed anatomy therefore applies, and its counted
requirements are judged on the script's figures in `anatomy-input.json` and `anatomy-delivered.json`.
Both files report `"conforms": true`, `"failures": []` and `"norms": []`.

## 1. Changes

Three differences between `redline/work/input.md` and `redline/delivered.md`.

1. **Headline.** Before: `A four-week trial shows when to look closer` (script: 43 characters, 8 words).
   After: `Classroom temperature readings point to 14 lesson periods` (script: 57 characters, 8 words).
   **Repair of a visible defect.** The anatomy requires a headline understood on its own; the original
   named no subject matter at all — a reader meeting it in a list could not tell that the text is about
   classroom temperature measurement. The replacement names the subject and the finding. It is not an
   overclaim: it does not say the rooms or the pupils were cold. Counted scales did not force the change
   and did not forbid it — the original met the 20–70-character requirement and the *should* of at most
   eight words and 60 characters, and so does the replacement. This is a qualitative repair, not a
   counted finding against a requirement the text met.
2. **Section 1, first paragraph.** Before: `Values were logged every five minutes for the whole period.`
   After: `Values were logged every five minutes for the whole four weeks.` (script: that paragraph moves from
   33 to 34 words, sentences_estimate 2 in both.) **Repair of a visible defect** — a disambiguation.
   Throughout the text `period` denotes a lesson period (`14 of the 120 recorded lesson periods`), so
   `the whole period` was locally ambiguous. The span named is the same one the lead already gives
   (`left them there for four weeks`). No claim moved.
3. **Section 3, second paragraph.** Before: `A mean for the whole day could have hidden variation within
   lessons, and the report therefore presents lesson periods instead of one figure per day.` After:
   `A mean for the whole day could have hidden variation within lessons. The report presents lesson
   periods instead of one figure per day.` (script: that paragraph moves from 54 words / sentences_estimate
   2 to 52 words / sentences_estimate 3.) **A change to what a claim says** — its relation and, with it,
   its attribution. Both propositions survive; what is deleted is the assertion that the first is the
   report's stated reason for the second. Nothing else in the text sources the report for a rationale,
   only for the count and the date, so the edit lowers an attributed causal claim to two adjacent
   statements.

Nothing else differs. Frontmatter, standfirst, byline, lead, all four subheadings, the Swedish report
title and its italics, the quotation and the closing recommendation are byte-identical.

## 2. Headings

### Input

- `# A four-week trial shows when to look closer` — **statement**, **echo** (the standfirst repeats the
  phrasing: `what a four-week trial at one school established`).
- `## Fourteen of 120 lesson periods held a reading below 20 degrees` — **statement**.
- `## Ventilation, draught and radiant heat went unrecorded` — **statement**.
- `## A count of periods is not a measure of how cold it got` — **statement**.
- `## Pair the readings with usage times before changing the controls` — **statement**.

### Returned text

- `# Classroom temperature readings point to 14 lesson periods` — **statement**, **echo** (the standfirst
  opens `Temperature sensors in six classrooms`, so headline and standfirst share their content words).
- `## Fourteen of 120 lesson periods held a reading below 20 degrees` — **statement**. First sentence under
  it is `Values were logged every five minutes for the whole four weeks`, so no echo; the section's own
  figure is stated at the text's strength (`at least one reading below 20 degrees Celsius`), no overclaim.
- `## Ventilation, draught and radiant heat went unrecorded` — **statement**. First sentence under it is
  about what a sensor reports, so no echo.
- `## A count of periods is not a measure of how cold it got` — **statement**.
- `## Pair the readings with usage times before changing the controls` — **statement**.

No subheading is a label, none uses a colon for a verb, none is a question, and none carries a figure,
name or conclusion the section does not carry. The one mark that changed is which words the headline
shares with the standfirst; both the input headline and the returned headline carry an echo, so the
edit neither introduced nor removed that trait.

## 3. Criteria on the returned text

### G1 — pass

The article does the explanatory job for a property manager who knows heating plant but not measurement.
The reader learns what a sensor does and does not report — `A sensor reports the temperature of the air at
the point where it is mounted, and nothing else about the room` — what a different quantity would have
measured (`Operative temperature — a measure that takes in both the air temperature and the heat radiating
from the surrounding surfaces`), what the headline figure does not mean (`Fourteen out of 120 counts the
periods with at least one reading under the limit, and nothing beyond that`), and what to do next. The
angle — what a short trial can and cannot establish — is recognisable from the standfirst through every
section. The count is never called high or low, and the 20-degree line is held as `the office's own working
limit for the trial, not a claim about a legal requirement`.

### G2 — pass

The parts stand in the anatomy's order and the script finds them all: `headline`, `standfirst`, `byline`,
`lead`, four `sections`, and `"other": []` — nothing outside the skeleton. Each does its own job.

- Headline: `Classroom temperature readings point to 14 lesson periods` — 57 characters on the script's
  figure, inside the 20–70-character requirement; it states the angle of the whole and is understood
  without the standfirst.
- Standfirst: 49 words, `sentences_estimate` 2, `paragraphs` 1 — one paragraph as required and inside the
  60-word requirement. It stands alone: `This is what a four-week trial at one school established, what it
  did not measure, and what to record before the controls are changed.`
- Byline: `By Thomas Barregren` — an author is named, so there is no missing byline to report.
- Lead: 53 words, `paragraphs` 1, and it precedes the first `##`. It begins the work rather than restating
  the standfirst, ending `The readings answer a narrower question than that one.`
- Body: four explanatory sections, each with a subheading inside the 70-character requirement (62, 53, 54,
  63 characters) and each with at least one paragraph (two each).
- Ending: the call to action is the next step the explanation supports — `Before the controls are changed,
  she recommends pairing the temperature series with the times the rooms are used` — and it meets the
  expectation the lead set. It is not commercial.

### P1 — pass

Unfamiliar concepts arrive before use: operative temperature is glossed in the same sentence that
introduces it, and the limit is defined before the count leans on it. Conclusions stay proportionate to
visible support — `so it is a count with its exclusions rather than a verdict` — and the technical substance
survives whole (five-minute logging, sensor placement on exterior versus interior walls, placements never
compared experimentally, air temperature against operative temperature). One transition is weaker than it
was: `A mean for the whole day could have hidden variation within lessons. The report presents lesson periods
instead of one figure per day.` The connective is gone, but the two sentences remain adjacent in one
paragraph and the relation is still readable, so no reader loses the reasoning.

### W1 — pass

Every counted requirement is met on the script's figures, and `"failures": []` and `"norms": []` in
`anatomy-delivered.json` confirm that no requirement and no *should* is breached.

- Headline: 57 characters, 8 words — inside the requirement, and not past the *should* of eight words or
  60 characters.
- No paragraph passes 80 words: the longest the script reports is the closing paragraph at 66 words.
- No section passes three paragraphs: all four `sections` carry two.
- No heading below the second level: the script finds `headline` plus four section `subheading`s and
  `"other": []`.
- Standfirst and lead open on different first words (`Temperature` against `In`).
- The *most* statements are read across the whole text and hold there: `paragraphs_of_two_or_three_sentences`
  9 of `paragraphs` 10, and `sections_of_two_or_three_paragraphs` 4 of `sections` 4. The one four-sentence
  paragraph is not a failure, because *most* is never read against a single paragraph.

Subheadings are informative enough to be entered from — `A count of periods is not a measure of how cold it
got` tells a scanning reader what that stretch settles. Nothing is fragmented into density: the explanation
runs continuously and the voice is the same from the lead to the close.

### L1 — pass

The prose reads as native British English, not as translated Swedish. `Complaints about cold air had come in`
and `What the air did as it moved through a room, and what anyone sitting in it experienced, is therefore
outside the data` are idiomatic English constructions, not Swedish word order carried across. The quotation
is rendered idiomatically — `We know when we need to look more closely. We still don't know why it got cold
just then` — rather than word-for-word. The one Swedish string, the report title `Mätförsök i Björkskolan`,
is a proper name and correctly left in Swedish and italicised.

### L2 — pass

`en_GB` governs throughout. Spelling: `draught`, `metre`-free but `Celsius` spelled out. Date form: `12 March
2026` and `In January 2026`, day-before-month with no comma. Numbers: `20 degrees Celsius`, `every five
minutes`, and `14 of the 120` — figures for the data, words for small spans, held consistently. Quotation
marks are single, which is established British practice, and the practice is used consistently; it is
preserved rather than converted. No currency appears, and no new date or conversion was invented — the two
dates in the returned text are the two that were in the input.

## 4. T2 — pass

The text's own `kntnt` metadata names `technique: pac`, and the reply confirms it was read from there, so
the criterion applies.

- **Factual starting point / question.** The lead gives it without invention: `Complaints about cold air had
  come in, and the office wanted to know whether they coincided with low temperatures during lesson time.`
- **Analysis.** Three sections do the work in order: what was logged and how the sensors sat, what the
  instrument cannot see (`the trial recorded air temperature only`; `Ventilation, draught and perceived
  temperature were not measured at all`), and what the number itself is worth (`Nor does the trial supply
  anything to set that figure against — no norm, no target, no capacity`).
- **Warranted conclusion.** The close draws only what the analysis carries: `Which lesson periods to examine,
  then, is the narrower question these four weeks answer`, and the recommendation to pair the series with
  usage times before changing the controls.

No crisis and no triumph is invented. The conclusion is held at the strength the support allows, and the
remaining ignorance is stated rather than closed over: `We still don't know why it got cold just then.`

## 5. R1 — pass

**Every change is reported, and reported accurately.**

- The headline rewrite is reported under **The headline's claim was rewritten**, quoting both forms and
  giving the reason. The account's added claim — that the new headline `does not say that the classrooms, or
  anyone in them, were cold` — is true of the delivered line.
- The dropped causal relation is reported under **A causal relation was removed**, quoting the sentence as it
  stood and naming precisely what went: `therefore handed the writer's own reasoning to a named, dated
  document`. The account's summary `The two sentences now stand separately and both claims survive` matches
  the delivered text.
- The `whole period` → `whole four weeks` change is reported in the closing paragraph as `the third repair`,
  with the reason and the correct statement that it `names the same span and moved no claim`.

The account's blanket sentence — `No claim was removed, and no sentence that bounds what the text asserts was
touched` — sits beside an itemised removal of a causal relation, which reads awkwardly, but it is not
inaccurate: it enumerates the bounding sentences that survive (the working limit against a legal requirement,
the placements never compared experimentally, the unmeasured ventilation, draught and perceived temperature,
the unrecorded duration below the limit, the unmeasured effect of any adjustment), and every one of those is
in `redline/delivered.md` unchanged. The itemisation above it prevents the sentence from concealing anything.

**No unresolved mandatory finding is withheld.** The reply states `nothing is left unresolved`, and no defect
is visible in the returned text that the account leaves unnamed.

**No removal is unreported and no claim was strengthened.** Both claim-bearing edits move in the safe
direction — the headline holds at the text's own strength, the causal edit lowers an attribution rather than
raising one. Quotations, arguments, figures and the report's title and date are preserved exactly.

**Visible defects not addressed:** none found. The script reports `"conforms": true`, `"failures": []` and
`"norms": []` for the returned text, the prose carries no contradiction against itself, and the closing
mechanical pass's verdict that there was nothing to correct is borne out — no misspelling, agreement error or
punctuation fault is present in the input that survives into the delivered text.

**Changes of taste to passages that already worked:** none that the criterion forbids, with one borderline
case named. The removal of `therefore` touches a sentence that read well, and a source-blind reviewer cannot
know whether the rationale came from the report or from the writer. But the concern is legible in the text
alone — the text sources the report for the count and the date and for nothing else — so the edit is a
response to a visible attribution problem rather than a preference, and it is reported in full. No *most*
count was read against a single paragraph or section, no *should* the text had reason to leave was enforced,
and no counted requirement the text already met was cited as a finding: the original headline satisfied the
20–70-character requirement at 43 characters and the *should* at 8 words, and the account does not pretend
otherwise — it argues from the anatomy's requirement that a headline be understood on its own, which is not
a counted line.

The budget was spent on three small edits rather than on a rewrite; nine of ten paragraphs are untouched.

**No unavailable-source verification was attempted.** The reply reasons only from what the text itself
sources.

## 6. Source loss

*Separate from every criterion above: the Skill did not have `write/work/source.md` and could not have known
any of this.*

**One change removes something the source supplied.**

The source states the rationale as the report's own, with the causal adverb attached to the report:

> Ett medelvärde för hela dagen kan dölja variation under lektionerna. Rapporten redovisar **därför**
> lektionspass i stället för ett enda dygnsmedelvärde.

The input carried that relation faithfully — `A mean for the whole day could have hidden variation within
lessons, and the report **therefore** presents lesson periods instead of one figure per day` — and the change
deletes it:

> A mean for the whole day could have hidden variation within lessons. The report presents lesson periods
> instead of one figure per day.

What is lost is not a caveat but a careful sourced formulation: the source attributes the choice of unit to
the report and gives the report's reason for it. After the edit the text no longer says that the report chose
lesson periods for that reason; the two facts sit side by side and the connection is left to the reader. The
Skill's stated ground — that the text sources the report only for the count and the date — is sound reasoning
from the text alone, and the direction of the error is the cautious one, but the source did warrant the word
that was cut.

**No other source requirement was touched.** The changes leave every stated limit intact: the six rooms and
four weeks, `placements were documented, but they were never compared experimentally`, `Ventilation, draught
and perceived temperature were not measured at all`, `does not say how long any reading stayed under the
limit`, `does not say whether the pupils were cold`, `the office's own working limit for the trial, not a
claim about a legal requirement`, and `no adjustment has yet had its effect measured`. The forbidden
inferences stay forbidden: the new headline does not call 14 of 120 high or low, asserts no cause of the cold,
no saving, no health effect and no legal rule, and the brief's `Ingen kommersiell uppmaning` is respected. The
brief gives no byline (`Ingen byline är given`), and the text's `By Thomas Barregren` — the invoking user —
was left as it stood.
