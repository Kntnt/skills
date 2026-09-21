# Judgement B — article-en_GB / write

Genre: `article` (brief: "pedagogisk webbartikel"; metadata `genre: article`). The fixed skeleton applies, so a counted requirement fails on the script's count.

## 1. Outcome

**Delivered.** `delivered.md` exists and the reply carries the full draft in a fenced block under "## The draft".

**Two source comparisons completed.** `evidence/srccheck/` holds `task-1.md` + `report-1.md` and `task-2.md` + `report-2.md`. Each report ends with an explicit completion status: report 1, "**Complete.** All 29 draft passages …"; report 2, "Comparison complete. The whole draft — title, lead, byline, all four section headings and all body paragraphs — was compared". The two tasks name different drafts (`draft.md`, `draft-2.md`), so they are two comparisons and not one repeated. The reply agrees: "Two comparisons ran, each on a fresh agent with its own context and no history."

**The delivered prose is byte-identical to the last prose a checker saw.** `diff evidence/srccheck/draft-2.md delivered.md` reports one hunk only, `0a1,6`: the six lines of `kntnt` front matter added at the top. Every prose line is unchanged — no repair was made after the second comparison, and the reply says so ("after the final comparison the prose no longer changes — what is delivered is exactly the prose that comparison read").

Between the two comparisons the writer did change the draft: `diff draft.md draft-2.md` shows five changed lines — the two repairs report 1 asked for (the standfirst's "from January 2026", the November trial's "the sensors in the same positions"), two consequential rewrites in the standfirst/lead and first body paragraph, and the deletion of the authorial aside "Every word there carries weight." That last cut was made under no checker finding; the reply discloses it ("one authorial aside was cut at the same time"). The repaired prose was then compared in full, so nothing rests on an uncompared edit.

## 2. Headings

- `# Temperature sensors show when to look, not why` — **statement**. No colon, no question. Not an echo: the standfirst shares the theme but none of the wording. No overclaim: the body carries both halves — "What it marks out is which lesson periods are worth a closer look" and "the trial does not say why".
- `## Each reading is the air temperature at a single point` — **statement**. No echo of its first sentence ("The office placed sensors in six classrooms in January 2026, and they logged a value every five minutes for four weeks"). No overclaim.
- `## The count says how many periods, never how cold or how long` — **statement**. No echo of "Twenty degrees was the office's own working limit for the trial". No overclaim; both negatives are the report's own stated silences.
- `## The office reports by lesson and plans a second trial` — **statement**. No echo of "A daily average could have buried all of this." Not an **overclaim** in the mark's sense: the body says "A second trial is planned for November" at the same strength. The ordinal is unsupported by the material in both places, which is an `F1` matter and not a heading-versus-text one.
- `## Where to look next is what this trial delivers` — **statement**. No echo of "So the trial does not say why Björkskolan's classrooms turned cold." No overclaim.

No heading is a label, none uses a colon for a verb, and none is a question.

## 3. F1 — fail

Nearly the whole draft holds. I checked every factual passage against the Swedish and found the hard things right: the figure carries its quantifier and its restriction ("Fourteen of 120 **recorded** lesson periods … contained **at least one** reading below 20 degrees Celsius" ← "14 av totalt 120 registrerade lektionspass innehöll minst en mätning under 20 grader Celsius"); the threshold's status is stated exactly ("the office's own working limit for the trial, not a claim about a legal requirement" ← "kontorets egen arbetsgräns för försöket, inte ett påstående om ett rättsligt krav"); the evaluative characterisation the brief forbids is refused in so many words ("it is neither a high count nor a low one — it is a count, from six rooms, over four weeks"); the possibility modality of the daily mean survives ("could have buried", "can hide" ← "kan dölja"); "No adjustment's effect has been measured yet" keeps "ännu"; "its funding is not decided" keeps "inte beslutad"; and none of the forbidden inferences — saving, health, cause, sensor effect, legal rule — appears. The translated remark preserves meaning, certainty ("ännu inte" → "still don't"), stance and the distinctive "just då" → "just then", and leaves the impersonal *det* unfilled as "it", which is right because the material does not settle the referent.

Two passages nonetheless go beyond the material, and both stand in the delivered text.

**(a) "A second trial is planned for November", and the subheading "The office reports by lesson and plans a second trial".** The material says "Nästa försök planeras för november" — *the next* trial. "Second" is an ordinal the material never gives: nothing in it states that the January 2026 trial was the office's or the school's first. A case compatible with the material: an earlier measurement trial at Björkskolan in 2024. "Nästa försök planeras för november" still holds; "a second trial" is then false. No supplied sentence excludes that case. This is an unsupported addition, small but real, and it reaches the reader twice, once in a subheading. Keep unknown apart from absent: the material's silence about earlier trials is not a statement that there were none.

**(b) "So the trial does not say why Björkskolan's classrooms turned cold."** The assertion — no cause follows — is exactly the material's "Ingen … orsak till kyla … följer av materialet", and is right. Its presupposition is not. The only statement in the material that it turned cold is Rask's, and hers is bounded: "Vi vet ännu inte varför det blev kallt **just då**." The office's motive supplies complaints ("klagomål på kall luft"), which are complaints and not findings, and the report is expressly silent on whether the pupils were cold ("Den säger heller inte om eleverna frös"). The draft states the cold in the narrator's own voice, of "Björkskolan's classrooms" as a class, with no time restriction. A compatible case: the sub-limit readings fell in two of the six rooms on a handful of January mornings. Rask's sentence holds; "Björkskolan's classrooms turned cold", as a statement about the school's classrooms, fails. The reader effect is sharpest inside this article, which two paragraphs earlier declined to call 14 of 120 high or low and recorded the report's silence about the pupils — and then, in the author's voice, grants the cold as established.

Neither is an invented event, person, figure or attribute; both are widenings of scope and modality in the author's voice. Both are named in the reply's delivery account, which is why the run is not an unreported-findings rejection — but a reported finding is still a defect of the text, so `F1` fails.

Nothing else I tested became a finding. "what anyone in the room felt" for "upplevd temperatur" is loose, but the list it sits in ("Ventilation, draught and …") fixes the thermal reading, and the Swedish is equally agentless; "nobody measured that" rests on the agentless "mättes inte"; "never compared experimentally" is scoped by its own clause ("so the trial settles nothing about that difference"). Defensible as written. The report's title and date and the office's motive are omitted, which misattributes nothing.

## 4. G1 — pass

The named reader is a municipal property manager who knows heating systems but not measurement technique. The article tells that reader what the figure does and does not license, in their own working terms: "'At least one reading' is not a duration. The report does not say how long the temperature stayed under the limit in any of those 14 periods, so a single five-minute sample and a whole lesson below the line count alike." The angle the brief set — what a short trial can and cannot say — is announced in the standfirst ("Here is what a study that size can establish about the warmth in a school, and what it cannot") and sustained to the last line ("A trial this size narrows the question; reading it as an answer is the mistake it invites"). The craft is explanatory rather than promotional, as the brief required, and the technique is kept rather than thrown away: sampling interval, sensor siting, the un-compared placement, operative versus air temperature, and reporting by lesson period rather than daily mean all survive. The reader leaves able to do something: link the series to usage times before touching the control system.

## 5. G2 — pass

The parts appear in the anatomy's order, and the script measures all of them: `"conforms": true`, `"failures": []`, `"norms": []`.

- **Headline** — `"characters": 46`, `"words": 8`: inside the 20–70-character requirement. It states the angle of the whole and is understood alone.
- **Standfirst** — `"words": 47`, `"paragraphs": 1`: inside the 60-word maximum and the one-paragraph requirement. It stands alone: who, where, how long, what was measured, and what the piece will settle, with no dependence on the headline.
- **Byline** — `"text": "By Thomas Barregren"`. The brief names no author ("Ingen byline är given"), so the invoking user's name is the right fill, and the Write run states it in the delivery account: "The brief names no author, so the byline carries your own name, Thomas Barregren."
- **Lead** — `"words": 53`, `"paragraphs": 1`, and it precedes the first H2. It begins the work rather than restating the standfirst: it puts the figure on the table and sets the three-part plan the body follows.
- **Sections** — four, with `"paragraphs"` of 2, 3, 2 and 2; every section has at least one paragraph. Each does a distinct job: what a reading is, what the count is, what the office did and plans, what the trial yields. The body is explanatory throughout.
- **Ending** — "Where to look next is what this trial delivers" closes on the expectation the lead raised and carries the call to action the explanation supports: "link the temperature series to the times the rooms are in use, before changing anything in the control system." It is a useful next step for the named reader, it grows out of Rask's own recommendation, and it is non-commercial, as the brief demanded ("Ingen kommersiell uppmaning").

No subheading repeats the standfirst or its own first sentence, and none claims more than its section carries.

## 6. P1 — pass

Unfamiliar concepts arrive before they are used, which is what the brief asked for. Operative temperature is defined at the point of introduction — "Operative temperature — the measure that combines air temperature with radiant heat from the surrounding surfaces — is a different quantity, and the trial did not collect it" — and only then does the argument lean on the distinction. "At least one reading" is quoted and unpacked before its consequence is drawn. The daily-mean paragraph explains why lesson periods are the reporting unit rather than asserting it.

The transitions are real, not decorative: "Measured against it…" turns the working limit into the count; "A daily average could have buried all of this" carries the previous section's silences into the reporting choice; "So the trial does not say why…" marks the turn to the ending. Conclusions stay proportionate to visible support — the count is given with its exclusions and explicitly not graded, and the placement difference is closed off ("never compared experimentally, so the trial settles nothing about that difference") rather than speculated on. Technical substance survives intact: five-minute interval, four weeks, six rooms, two external and four internal walls, air versus operative temperature, lesson period versus daily mean.

## 7. W1 — pass

The script reports `"conforms": true` with `"failures": []` and `"norms": []` — no counted requirement is outside its bound and no *should* departure was recorded.

- Paragraphs: `"paragraphs": 11`, `"paragraphs_of_two_or_three_sentences": 11`. The *most* statement holds across the whole text, and it is read across the text rather than against any single paragraph.
- Sections: `"sections": 4`, `"sections_of_two_or_three_paragraphs": 4`. Same reading.
- The longest paragraph the script measures is 51 words ("Each sensor reports the air temperature at its own position…" and "After the trial, operations technician Elin Rask…"), well inside the 80-word norm, so no paragraph-length departure arises.
- Heading levels: the `parts` carry one headline and four subheadings, with `"other": []` — no level below the second.
- Headline: `"characters": 46`, `"words": 8` — inside both the requirement and the eight-word/60-character norm.
- Standfirst and lead open on different first words: "Lervik's" against "Fourteen".

Standfirst and lead complement rather than duplicate: the standfirst frames the trial and the question, the lead puts the figure up and states what reading it properly requires. The body is complete when the standfirst is covered — "what a study that size can establish … and what it cannot" is answered section by section and closed in the ending. The subheadings are informative enough to orient a scanner on their own, and the voice runs continuously through them; nothing is fragmented into bullet lists or stub paragraphs, and no density loss occurs. I find no actual reader loss.

## 8. L1 — pass

The prose reads as natively written British English, not as translated Swedish. Idiom and syntax are English throughout: "A daily average could have buried all of this", "so a single five-minute sample and a whole lesson below the line count alike", "The report is equally silent on whether the pupils were cold", "reading it as an answer is the mistake it invites". The register is the understated British one — the strong claims are stated plainly with no intensifier propping them up ("it is a count, from six rooms, over four weeks"). The present perfect sits where British usage puts it: "No adjustment's effect has been measured yet."

No Swedish phrasing survives into the English. The quotation is rendered as English speech rather than Swedish word order — "Vi vet när vi behöver titta närmare" becomes "We know when we need to look more closely", with the contracted "We still don't know" that spoken British English would use. Terms of art are the English ones: "operative temperature", "draught", "control system", "operations technician", "caretaker" — not calques on "styrningen", "driftteknikern" or "vaktmästare".

## 9. L2 — pass

`en_GB` governs throughout, and this is separable from the idiom judged under `L1`.

- Spelling: "draught" rather than the American "draft" — the British form, and the one that matters here. No `-ize`/`-ise` conflict arises in the text, so the house-style choice is not tested; the invariant `-yse` group does not occur.
- Quotation marks: single as the outer mark, at both "'At least one reading'" and the Rask quotation. Consistent across the document, which is what British practice requires.
- Numbers: "Fourteen of 120" spells the sentence-initial numeral and leaves the rest in figures; "14 of the 120", "20 degrees Celsius", "Twenty degrees" sentence-initial, "five minutes", "four weeks", "six classrooms". Consistent and idiomatic.
- Dates: "January 2026" and "November" are carried in the material's own form. No new factual date is invented — in particular the November trial is given no year, and the report's date is simply not used.
- No currency appears, so no conversion could be invented.
- Diacritics preserved: "Björkskolan" throughout.
- Punctuation: spaced em dashes used consistently as the parenthetical mark; semicolons used correctly ("…when each room is used; its funding is not decided").

## 10. T2 — skipped

`T2 — skipped — no technique is named in the text's metadata or in the reply.` The delivered text's `kntnt` map reads `technique: none`, and the reply's resolution list says "**Technique:** none. … The draft therefore carries no imposed arc". I infer no technique from the shape of the prose and judge nothing under this criterion.

## 11. Checker findings

Report 1 (`evidence/srccheck/report-1.md`), on `draft.md`:

1. **F1 — the lead dates the measurement period to January 2026.** Passage: "Lervik's property office measured six classrooms at Björkskolan every five minutes for four weeks **from January 2026**." Alleged: the material dates only the sensors' placement to January ("satte i januari 2026 temperaturgivare"), and gives the four-week logging period a duration but no start. Writer: repaired — the standfirst now reads "spent four weeks measuring the air temperature in six classrooms at Björkskolan", with January moved into the body where it belongs to the placement. My class: **supported**. The material dates only the placement, and installation in late January with logging in February is compatible with every supplied sentence.
2. **F2 — "the sensors in the same positions" for the November trial.** Passage: "A second trial is planned for November, with **the sensors in the same positions** and notes on when each room is used". Alleged: "likadant placerade givare" says placed in the same manner and is indefinite; the draft fixed both the devices and the positions. Writer: repaired — "with sensors placed the same way". My class: **supported**. Same-manner placement in different rooms, with new devices, satisfies the Swedish and falsifies the draft, and nothing supplied excludes it.

Report 1 also records, expressly not as findings: an editorial question about "why Björkskolan's classrooms turned cold" (§4, no repair proposed), and notes on omissions, forbidden inferences, length and the byline (§5). I count these as what they say they are, and note that §4 is the same passage report 2 later raised as a finding — the first checker saw it and declined to call it one.

Report 2 (`evidence/srccheck/report-2.md`), on `draft-2.md`:

3. **Finding 1 — "a second trial" asserts an unsupported ordinal.** Passage: the subheading "The office reports by lesson and plans a second trial" and "A second trial is planned for November". Alleged: the material gives "Nästa försök" — the next, not the second — and never says the January trial was the first. Writer: not repaired; reported in the delivery account as remaining, with the checker's repair quoted. My class: **supported**, and minor.
4. **Finding 2 — "why Björkskolan's classrooms turned cold" widens the cold.** Passage: "So the trial does not say why Björkskolan's classrooms turned cold." Alleged: the denial of cause is supported, but the presupposition is asserted in the narrator's voice, across the school's classrooms and with no time restriction, where the material carries it only through Rask and only of the occasions in question. Writer: not repaired; reported in the delivery account as remaining. My class: **supported**.

**Was a real defect I found under `F1` seen by no checker?** No. Both defects I cite under `F1` are findings 3 and 4 above, raised by the second checker with the same passages and essentially the same reasoning. I found no unsupported addition that escaped both comparisons.

## 12. Remaining findings

The reply's delivery account opens "## Delivered with known defects" and reports two.

1. > "a second trial" asserts an ordinal the material does not give.

   Passage: the subheading "The office reports by lesson and plans a second trial", and "A second trial is planned for November". What the material carries instead: "Nästa försök planeras för november" — *the next* trial, with no statement that the January 2026 trial was the first. Proposed repair, as the account gives it: "plans another trial" in the subheading, and "Another trial is planned for November". Under `F1` this is a defect of the delivered text — see 3(a).

2. > "why Björkskolan's classrooms turned cold" widens the cold beyond what the material carries.

   Passage: "So the trial does not say why Björkskolan's classrooms turned cold." What the material carries instead: Rask's "Vi vet ännu inte varför det blev kallt **just då**", the complaints about cold air as complaints, and the report's silence on whether the pupils were cold. Proposed repair, as the account gives it: "So the trial does not say why it turned cold when it did", leaving the following quotation to carry the fact in the speaker's voice. Under `F1` this is a defect of the delivered text — see 3(b).

The account presents both accurately: the passages it quotes are the passages in the delivered prose, the material it cites is the material, and it does not soften either into a stylistic preference. It is candid that neither was repaired and why ("after the final comparison the prose no longer changes"), and it adds the byline check the brief's silence makes necessary. It reaches, though, for "neither is an established fact about the text" — on my own reading of `source.md`, both are defects, and the account's framing understates that.

## 13. Class of the run

**`valid delivery`.** The prose that was delivered had a completed comparison of its own: report 2 read `draft-2.md` in full and ends "Comparison complete", and the delivered file is that same prose byte for byte, with only the `kntnt` front matter added. The run did not withhold compared prose, so this is no stop of either kind. The two findings the last comparison left unrepaired were carried to the reader beside the draft, with passage, material and proposed repair — which is what the Skill's contract requires of a delivery that still has known defects. The text nonetheless carries a remaining quality problem: `F1` fails on those two passages, and both are single-sentence fixes away from clean.
