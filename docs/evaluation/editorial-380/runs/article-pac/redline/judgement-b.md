# Judgement B — article-pac, Redline

Genre in the text's own `kntnt` map: `article`. The fixed skeleton applies, and its counted requirements are judged on the script's figures.

## 1. Changes

Three differences between `redline/work/input.md` and `redline/delivered.md`.

1. **Headline.** Before: `A four-week trial shows when to look closer`. After: `Classroom temperature readings point to 14 lesson periods`. **Repair of a visible defect** (the headline did not name its subject and could not be understood alone), which also changes what the headline's claim is about: it moves from the trial's use to the trial's datum. Not an overclaim in either direction — the script gives 43 characters / 8 words before and 57 characters / 8 words after, both inside the 20–70-character requirement and inside the *should* of eight words and 60 characters.
2. **Section 1, paragraph 1.** Before: `Values were logged every five minutes for the whole period.` After: `… for the whole four weeks.` **Repair of a visible defect** — *period* elsewhere in the text means *lesson period*, so the sentence read as though logging covered one lesson. The span asserted is unchanged. Script: that paragraph goes from **33 to 34 words** (`parts.sections[0].paragraphs[0].words`).
3. **Section 3, paragraph 2.** Before: `A mean for the whole day could have hidden variation within lessons, and the report therefore presents lesson periods instead of one figure per day.` After: `A mean for the whole day could have hidden variation within lessons. The report presents lesson periods instead of one figure per day.` **A change to what a claim says — its modality.** The causal attribution is withdrawn: the text no longer says the report chose its unit *for that reason*. Both surviving propositions are unaltered. Script: that paragraph goes from 54 words / 2 sentences to 52 words / 3 sentences.

Nothing else differs. Frontmatter, standfirst, byline, lead, all four subheadings, the Rask quotation and every limiting sentence are byte-identical.

## 2. Headings

### Input

- `# A four-week trial shows when to look closer` — **statement**. No colon, not a question, no echo of the standfirst (which opens `Temperature sensors in six classrooms …`), no overclaim: the text carries `We know when we need to look more closely`. Its weakness is not on this list — it names neither the subject measured nor what is to be looked at.
- `## Fourteen of 120 lesson periods held a reading below 20 degrees` — **statement**. No echo of its first sentence (`Values were logged every five minutes …`); no overclaim — `at least one reading below 20 degrees Celsius` is the section's own wording.
- `## Ventilation, draught and radiant heat went unrecorded` — **statement**. No echo of its first sentence (`A sensor reports the temperature of the air …`); no overclaim — radiant heat is excluded by `the trial recorded air temperature only`.
- `## A count of periods is not a measure of how cold it got` — **statement**. No echo of its first sentence (`The report does not say how long …`); no overclaim.
- `## Pair the readings with usage times before changing the controls` — **statement** (directive). No echo of its first sentence (`Which lesson periods to examine, then, …`); no overclaim — the recommendation is Rask's, stated in the section.

### Returned text

- `# Classroom temperature readings point to 14 lesson periods` — **statement**, and a **partial echo**: it reuses the standfirst's opening content words (`Temperature sensors in six classrooms`), though not its phrasing and not its proposition, which is about what sensors can and cannot tell. No colon, not a question, no overclaim — `point to` is at or below the strength of `contained at least one reading below 20 degrees Celsius`, and it does not say anyone was cold.
- The four `##` headings are unchanged and carry the marks listed above.

## 3. G1 — pass

The article does an explanatory job for a property manager who knows heating but not measurement. The reader learns what was installed and for how long (`sensors in six classrooms at Björkskolan and left them there for four weeks`), what the single figure means (`Fourteen out of 120 counts the periods with at least one reading under the limit, and nothing beyond that`), what is outside the data (`Ventilation, draught and perceived temperature were not measured at all`), and what to do next (`pairing the temperature series with the times the rooms are used`). The angle — what a short trial can and cannot say — is announced in the standfirst and held to the last line. The headline change moved the shop window from the conclusion to the datum, but the angle inside the text is untouched.

## 4. G2 — pass

Every part is present in the anatomy's order and each does its own job. The script's `parts` map shows headline, standfirst, byline, lead, four sections and no `other`. The standfirst stands alone at **49 words in one paragraph** (`parts.standfirst.words`, `paragraphs`), inside the 60-word requirement, and states the text's scope without depending on the headline. The byline (`By Thomas Barregren`) is present, so the missing-byline report does not arise; nothing in the text or the reply claims a different author. The lead is **53 words in one paragraph** and precedes the first `##`, and it begins the work rather than restating the standfirst: it supplies the occasion and closes on `The readings answer a narrower question than that one`. The body is explanatory across four sections. The ending shows that expectation met — `Which lesson periods to examine, then, is the narrower question these four weeks answer` — and the call to action is the useful next step the explanation supports: `Before the controls are changed, she recommends pairing the temperature series with the times the rooms are used`. It is non-commercial, which the assignment warrants. The subheadings each state their own section's angle and stand alone; the script gives 62, 53, 54 and 63 characters, all inside the 70-character requirement.

## 5. P1 — pass

The reasoning is followable and the unfamiliar concept is introduced before it is used: `Operative temperature — a measure that takes in both the air temperature and the heat radiating from the surrounding surfaces — is a different quantity, and the trial recorded air temperature only`. Transitions are real, not decorative (`Nor does the trial supply anything to set that figure against`; `Which lesson periods to examine, then, …`). Conclusions stay proportionate to the visible support: `it is a count with its exclusions rather than a verdict`, and the text nowhere calls 14 of 120 high or low. The technical substance survives in full — five-minute logging, two exterior and four interior placements never compared experimentally, the working limit as against a legal requirement.

One local loss, introduced by change 3: `A mean for the whole day could have hidden variation within lessons. The report presents lesson periods instead of one figure per day.` The reader must now infer the relation between the two sentences that the text previously stated. Adjacency still carries it, so this is a qualitative concern rather than a break in the reasoning.

## 6. W1 — pass

A web reader can orient without losing the continuous explanation. The script reports `conforms: true`, `failures: []` and `norms: []` for the returned text, so no counted requirement and no *should* is breached: the headline is **57 characters / 8 words** (inside the *should* of 60 characters and eight words), the subheadings are **62, 53, 54 and 63 characters**, no heading sits below the second level, and the longest paragraph is **66 words** (`parts.sections[3].paragraphs[1].words`), under the 80-word *should*. Read across the whole text, *most* holds both ways: **9 of 10 paragraphs run to two or three sentences** and **4 of 4 sections to two or three paragraphs** (`typical`). Standfirst and lead are complementary and open on different first words — `Temperature` against `In` — and the body completes what the standfirst promised: what was established, what was not measured, what to record before the controls change, in that order. Density is even; no section fragments.

## 7. L1 — pass

The prose reads as written in English, not translated into it. `Two of the sensors stood near exterior walls and four on interior walls`, `Ventilation, draught and radiant heat went unrecorded`, `so it is a count with its exclusions rather than a verdict` are native constructions, and the quotation is idiomatic (`We know when we need to look more closely. We still don't know why it got cold just then`) rather than word-for-word Scandinavian. No Swedish word order, no calqued preposition. The one Swedish item is the italicised report title, correctly left untranslated.

## 8. L2 — pass

`en_GB` governs throughout. Spelling: `draught`, not `draft`. Punctuation: single quotation marks around the quotation, with the comma inside before `Rask said`, and spaced em dashes used consistently. Date form `dated 12 March 2026` and `In January 2026` are British. Measurements stay as the text had them — `below 20 degrees Celsius`, `every five minutes` — with no invented conversion, no currency, and no new date. The Skill's three changes introduced no locale item of their own.

## 9. T2 — pass

The technique is named in the returned text's own metadata (`technique: pac`). The factual starting point is stated without crisis: `Complaints about cold air had come in, and the office wanted to know whether they coincided with low temperatures during lesson time.` The analysis runs through three sections — what the figure is, what the instrument cannot see, what the count is not — and the conclusion is warranted by exactly that analysis and no more: `it is a count with its exclusions rather than a verdict`, therefore `pairing the temperature series with the times the rooms are used` before any change to the controls. No invented triumph; the close admits `the funding has not been decided`. The headline change shifts which end of the chain is advertised, from the conclusion to the starting datum — both are valid PAC openings, so this is not scored against it.

## 10. R1 — pass

**Every change is reported, and reported accurately.**

- Headline rewrite — reported, under *The headline's claim was rewritten*, quoting both versions and stating the reason (`named neither what had been measured nor what the reader would be looking more closely at`). The account's own claim about the new headline — `it does not say that the classrooms, or anyone in them, were cold` — is true of the delivered text.
- Causal relation removed — reported, under *A causal relation was removed*, quoting the sentence before and stating the effect exactly: `The two sentences now stand separately and both claims survive.` That is what the diff shows.
- `for the whole period` → `for the whole four weeks` — reported, with the correct characterisation that it `names the same span and moved no claim`.

**Removals:** none beyond the conjunction and adverb in change 3, which is reported. **Claims changed:** one, reported. The account's blanket statement is verifiable and holds: the working limit as against a legal requirement, the undocumented placement comparison, the unmeasured ventilation, draught and perceived temperature, the unrecorded duration below the limit and the unmeasured effect of adjustments all return unaltered. The Rask quotation is byte-identical. No mechanical editing beyond the two-word substitution, no side effect on frontmatter or structure.

**Findings against things the text already satisfied:** none. The Skill made no finding against a counted requirement — the input's script figures show `conforms: true`, `failures: []`, `norms: []`, and it touched no count. It read no *most* against a single paragraph or section, and left no *should* departure standing that it should have left standing.

**Visible defects not addressed:** none that reach the level of a defect. The final paragraph runs to four sentences, but *most* is read across the text and 9 of 10 paragraphs are within two or three, so it is not a finding.

**Changes of taste to passages that already worked:** the headline is the borderline case and I do not score it as taste. The anatomy requires a headline understood on its own, and `A four-week trial shows when to look closer` names neither the subject nor the object of the looking; a property manager meeting it in a feed cannot tell whether it is for them. That is a real, visible defect, and the count requirement it met is not the requirement it failed. The repair carries two costs worth recording without failing the criterion: the new headline is slightly elliptical (what the readings point to those fourteen periods *for* is left implicit) and it now shares its content words with the standfirst's opening, where the old one shared none. Change 3 is the second borderline case: attributing a rationale to a document the text cites only for a count and a date is a claim the text alone cannot support, so the repair is defensible, at the price of the connective named under P1.

Nothing is left unresolved and nothing is reported as irreparable, so no remaining-quality label attaches on that ground.

## 11. Source loss

**Yes — one, in change 3.** `write/work/source.md` states the causal relation the Skill removed, in its own words:

> Ett medelvärde för hela dagen kan dölja variation under lektionerna. Rapporten redovisar **därför** lektionspass i stället för ett enda dygnsmedelvärde.

The source's `därför` licenses precisely what the input said and the returned text no longer says — that the report presents lesson periods *because* a whole-day mean could hide within-lesson variation. The change (`… within lessons, and the report therefore presents lesson periods …` → `… within lessons. The report presents lesson periods …`) therefore withdraws a relation the material supplied, leaving the text carrying less than the reporting warranted. The Skill could not know this, since it had the text alone and the text sources the report only for the count and its date; the finding was reasonable on the evidence available. No caveat, no careful formulation of what is and is not claimed, and no named limit was removed: every exclusion in the source (duration, pupils' comfort, the six rooms and four weeks, ventilation, draught, perceived temperature, the working limit as against a legal requirement) survives in the returned text.

A second, smaller note that is not a loss: the source's angle is `vad ett kort mätförsök kan och inte kan säga`, which the old headline was nearer to; the new headline leads on the figure the source forbids anyone to call high or low (`14 av 120 saknar normjämförelse: kalla det inte högt/lågt`). `point to 14 lesson periods` does not characterise the figure, so the prohibition is not broken.
