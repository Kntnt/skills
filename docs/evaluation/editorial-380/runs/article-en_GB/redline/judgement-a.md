# Redline judgement — article-en_GB

Genre from the text's own `kntnt` map: `article`. The fixed anatomy applies; the script's figures are requirements where the reference states them plainly, and `should`/`most` are read as the brief directs.

## 1. Changes

Exactly one difference between `redline/work/input.md` and `redline/delivered.md`.

- Before: `So the trial does not say why Björkskolan's classrooms turned cold.` → After: `So the trial does not say why the temperature in Björkskolan's classrooms fell below the limit.` — **a change to what a claim says (strength and scope)**, and the repair of a visible defect. The negated clause still presupposes its complement, so the input asserted in the article's own voice that the classrooms *turned cold* — a characterisation the same text withholds two sections earlier (`The report is equally silent on whether the pupils were cold; nobody measured that`) and (`so it is neither a high count nor a low one — it is a count, from six rooms, over four weeks`). The replacement states only what sections one and two establish: readings under the office's own 20-degree working limit. No other byte differs; the metadata block, the byline, both quotations and every other sentence are unchanged.

No mechanical corrections were made. No removals. No other change of any kind.

## 2. Headings

### Input

- `# Temperature sensors show when to look, not why` — **statement**
- `## Each reading is the air temperature at a single point` — **statement**
- `## The count says how many periods, never how cold or how long` — **statement**
- `## The office reports by lesson and plans a second trial` — **statement**
- `## Where to look next is what this trial delivers` — **statement**

No heading in the input is a label, carries a colon standing in for a verb, or is a question. None echoes the standfirst or the first sentence beneath it: the standfirst opens `Lervik's property office spent four weeks measuring…` against the headline's `Temperature sensors show…`, and each section's opening sentence (`The office placed sensors…`, `Twenty degrees was the office's own working limit…`, `A daily average could have buried all of this.`, `So the trial does not say why…`) shares no phrasing with its subheading. No overclaim: each subheading names a boundary the section then establishes, and the headline's `not why` is the article's own settled position.

### Returned text

- `# Temperature sensors show when to look, not why` — **statement**
- `## Each reading is the air temperature at a single point` — **statement**
- `## The count says how many periods, never how cold or how long` — **statement**
- `## The office reports by lesson and plans a second trial` — **statement**
- `## Where to look next is what this trial delivers` — **statement**

Identical marks. The headings are byte-identical to the input's; only the fourth section's opening sentence changed, and it still shares no phrasing with `Where to look next is what this trial delivers`.

## 3. Criteria on the returned text

### G1 — pass

The named reader is a municipal property manager who knows heating systems but not measurement technique, and the article is built for exactly that gap. The reader learns what a sensor does and does not report (`Each sensor reports the air temperature at its own position, and nothing else. Operative temperature — the measure that combines air temperature with radiant heat from the surrounding surfaces — is a different quantity, and the trial did not collect it`), what the headline figure counts (`'At least one reading' is not a duration. The report does not say how long the temperature stayed under the limit in any of those 14 periods, so a single five-minute sample and a whole lesson below the line count alike`), and why the office chose lesson periods over a daily mean. The angle — what a short trial can and cannot establish — is announced in the headline and held to the last sentence (`A trial this size narrows the question; reading it as an answer is the mistake it invites`). The craft is journalistic and disciplined: a quoted operations technician, a dated placement, an explicit refusal to call 14 of 120 high or low.

### G2 — pass

The anatomy's parts appear in order and each does its own job. The script's `parts` map lists `headline`, `standfirst`, `byline`, `lead` and four `sections`, with `other: []` — nothing sits outside the skeleton. The headline `Temperature sensors show when to look, not why` (script: 46 characters, 8 words) states the angle and is understood alone. The standfirst (script: 47 words, 1 paragraph) stands by itself and promises three things. The byline `By Thomas Barregren` names an author, so there is nothing for a Redline run to report as missing. The lead (script: 53 words, 1 paragraph) begins the work with the figure and comes before the first H2. Four sections carry the explanatory body. The ending shows the lead's expectation met and closes on a genuine next step that the explanation supports — `link the temperature series to the times the rooms are in use, before changing anything in the control system` — with nothing commercial, which is what an explanatory article warrants here.

### P1 — pass

Every unfamiliar concept arrives before it is used: operative temperature is defined in the clause that introduces it; the 20-degree line is identified as `the office's own working limit for the trial, not a claim about a legal requirement` before the count is measured against it; the daily-average problem is explained before the report's choice is justified. Transitions are real rather than connective filler (`Measured against it,…`, `A daily average could have buried all of this.`, `So the trial does not say why…`). Conclusions are proportionate to visible support throughout, and the repaired closing clause now matches the support exactly. Useful technical substance survives: sensor placement, five-minute sampling, the operative-temperature distinction, the unmeasured ventilation and draught. One residual slip: `No adjustment's effect has been measured yet` presupposes adjustments the text never states were made. The reply reports this as a finding it could not repair without the office's report, which it does not have; it is judged here as a remaining, minor problem of the returned text, and the detection is scored under `R1`. It does not break the reader's ability to follow the reasoning.

### W1 — pass

Every counted requirement is met on the script's figures, and the script reports `conforms: true`, `failures: []`, `norms: []` for the returned text. Headline 46 characters (20–70). Standfirst 47 words (at most 60), 1 paragraph. Lead 1 paragraph. Subheadings 53, 59, 53 and 46 characters (at most 70). Every section holds at least one paragraph. No `should` is departed from: the headline is 8 words and 46 characters (not past eight words or 60 characters); the longest paragraphs are 53, 51, 51, 50 and 49 words (none over 80); no section exceeds three paragraphs; no heading falls below the second level (`other: []`); and the standfirst opens on `Lervik's` against the lead's `Fourteen`, so they do not share a first word. Read across the whole text, `most` holds comfortably: the script gives `paragraphs: 11`, `paragraphs_of_two_or_three_sentences: 11`, `sections: 4`, `sections_of_two_or_three_paragraphs: 4`. The headings are informative statements that let a scanner orient, and the standfirst and lead complement rather than duplicate — the standfirst frames the question, the lead supplies the figure. The body covers everything the standfirst promises about what the study can and cannot establish. No density or fragmentation loss.

### L1 — pass

The prose reads as native British English with no Swedish substrate showing, though the source material is Swedish. Idiomatic constructions a translator would not reach for: `A daily average could have buried all of this`, `so a single five-minute sample and a whole lesson below the line count alike`, `What it marks out is which lesson periods are worth a closer look`, `reading it as an answer is the mistake it invites`. Syntax is English throughout — no calqued `already now`, no `possibility to`, no Swedish compound run into an English noun phrase. Rask's quotation is rendered idiomatically with its meaning intact (`We know when we need to look more closely. We still don't know why it turned cold just then.`), which is what the material permits.

### L2 — pass

en_GB governs. Spelling: `draught` rather than the US `draft`, and `metre`-class forms do not arise. Punctuation: single quotation marks throughout (`'At least one reading' is not a duration`, and Rask's quoted speech), consistently applied — established variation preserved, not invented. Numbers: `Fourteen of 120` spelled at sentence start and `14 of the 120` in numeral form mid-sentence; `20 degrees Celsius` and `every five minutes` follow British practice. Dates: `in January 2026` and `for November`, with no numeric form to localise. No currency appears, so no conversion was possible or attempted, and no new factual date was introduced by the one change.

## 4. T2 — skipped

No technique is named in the text's metadata or in the reply. The returned text's `kntnt` map carries `technique: none`, and the reply states `with **no technique**` and explains that `technique: none` is the map refusing an arc. Nothing is judged under this criterion, and no technique is inferred from the shape of the prose.

## 5. R1 — pass

**The one changed claim is reported, and reported accurately.** The reply's *Claim account* quotes the original clause, states plainly that it asserted the classrooms turned cold, cites the two passages in which the article refuses that characterisation, gives the reason the article's own prose cannot borrow the strength of Rask's quotation, quotes the replacement clause, and states what survives unchanged (`The bound the sentence carries — that the trial does not say why — survives unweakened, and Rask's quotation is untouched`). Checked against the two files, every part of that account is true. The account's closing claim, `Nothing else in the artifact was altered by the correction`, is exactly right: the diff is one line.

**No removals.** The reply says `One claim changed; none removed`, which the file comparison confirms.

**The change is a repair, not taste.** The defect is visible in the text alone: a negated clause carries its complement as a presupposition, so an article whose entire subject is the boundary between established and unestablished was crossing that boundary in its own closing argument. It is not a `most` count read against one paragraph, not a `should` the text had good reason to leave, and not a rewrite of clean prose to satisfy a preference. The repair is minimal — one clause, no ripple. The script confirms the text conformed before and after (`conforms: true`, `failures: []` in both files), so no anatomy requirement was invented as a pretext.

**The unresolved finding is reported and correctly classed as irreparable.** The reply names it, locates it (`No adjustment's effect has been measured yet` presupposing adjustments the text never states), explains the reader consequence, and states why it cannot be closed from the text: `The missing fact is whether an adjustment was made, and that fact is nowhere in the artifact; supplying it would be invention`. That judgement is correct on the evidence available to a source-blind reviewer — every rewrite that keeps the limit keeps the presupposition, and every rewrite that drops the presupposition either invents a fact or costs the reader the limit. This is a method limit, not a failure to act. Its text is still labelled as carrying a remaining quality problem, noted under `P1`.

**Voice, arguments, quotations and claims outside the finding are preserved.** Both quotations are byte-identical. The headline, standfirst, byline, lead, all four subheadings, the metadata block and ten of the eleven paragraphs are untouched. The article's characteristic moves — the refusal to call 14 high or low, the operative-temperature distinction, the explicit non-legal status of the 20-degree line — all survive.

**Visible defects not addressed:** none beyond the one reported as irreparable. No unsupported fact was introduced, the locale is unchanged and correct, no substantive editing was performed under cover of mechanics (the reply states the mechanical pass `found nothing to correct`, which the byte-level comparison confirms), the one unresolved finding is reported, and there are no side effects — the frontmatter, the byline and the file's structure are as they arrived. None of the protocol's five unconditional rejections is triggered.

**Changes of taste to passages that already worked:** none. The Skill made exactly one change, and it was not a matter of taste.

## 6. Source loss

**No.** Nothing the source required was removed or altered.

The only change replaced `why Björkskolan's classrooms turned cold` with `why the temperature in Björkskolan's classrooms fell below the limit`. The source's *Forbidden inferences* state `Ingen besparing, bättre hälsa, orsak till kyla, effekt av givarna eller lagregel följer av materialet` and `14 av 120 saknar normjämförelse: kalla det inte högt/lågt`. The change moves away from the forbidden characterisation rather than toward it: it stops the article's own voice from treating the cold as an established fact while leaving intact the sentence that denies a cause (`the trial does not say why`).

Every caveat the source carries is still present in the returned text:

- `Den säger inte hur länge temperaturen låg under gränsen` → `The report does not say how long the temperature stayed under the limit in any of those 14 periods`.
- `Den säger heller inte om eleverna frös` → `The report is equally silent on whether the pupils were cold; nobody measured that`.
- `Gränsen 20 grader var kontorets egen arbetsgräns för försöket, inte ett påstående om ett rättsligt krav` → `Twenty degrees was the office's own working limit for the trial, not a claim about a legal requirement`. This caveat is what licenses the new wording `fell below the limit`, since the limit is defined two sections earlier as the office's own.
- `Mätningarna omfattar bara dessa sex rum och dessa fyra veckor` → `it is a count, from six rooms, over four weeks`.
- `Ventilation, luftdrag och upplevd temperatur mättes inte` → `Ventilation, draught and what anyone in the room felt went unmeasured too`.
- `Givarnas placering dokumenterades men jämfördes inte experimentellt` → `Those positions were documented but never compared experimentally, so the trial settles nothing about that difference`.
- `finansiering är inte beslutad` → `its funding is not decided`.
- Rask's verbatim statement, which the source permits to be rendered idiomatically with its meaning preserved, is untouched by the change and remains attributed to her.

No named limit, stated caveat or careful formulation of what is and is not claimed was lost.
