# Judgement B — control-web-copy-flawed

Sources read: `work/input.md` and `response.md` in this run directory, and nothing else.

## 1. Differences

Numbered D1–D21. "Before" is `work/input.md`; "after" is the fenced text in `response.md`.

| # | Before | After | Class |
|---|---|---|---|
| D1 | `# Unlock your association's full potential` | `# Review of one shared room in a housing association` | Repair of a visible defect (contentless title). Carries a small claim shift of **scope/meaning**: the body says the offer "covers one shared room", the new title calls the page a review *of* that room. The precise original claim survives verbatim in the body. |
| D2 | `Decision-makers in a complex reality face growing complexity.` | *(removed)* | Repair of a visible defect (abstract audience description that restates itself). Removal of a claim about decision-makers, **scope** — the passage itself is the finding. |
| D3 | `Take the thumb out and discover a fantastic journey.` | *(removed)* | Repair of a visible defect (idiom calque plus an unsupported promise). Removal of the "fantastic journey" claim, **scope/certainty** — the passage itself is the finding. |
| D4 | `## Start` | *(removed)* | Repair of a visible defect (opaque heading). |
| D5 | Link is the second element on the page, directly under `## Start` | Link is the last line, under the conditions paragraph | Repair of a visible defect (ordering); page-order change only, no claim altered. |
| D6 | `[Book and pay now](https://example.invalid/svale/intresse)` | `[Express your interest](https://example.invalid/svale/intresse)` | Repair of a visible defect **and** a change to what the action claims: **meaning** (and **certainty** about what the click does). The stated action now matches the destination the page itself describes. |
| D7 | `## It` | `## What the review costs and includes` | Repair of a visible defect (opaque heading; the new heading also governs the merged price/coverage/inclusions material). |
| D8 | `It costs SEK 4,800 including VAT.` | `The review costs SEK 4,800 including VAT and covers one shared room in one housing association. It includes:` | Repair of a visible defect (antecedentless pronoun; four-way fragmentation). Price and currency unchanged; the referent `It` → `The review` is drawn from the page's own last paragraph. |
| D9 | `## More` | *(removed)* | Repair of a visible defect (opaque/placeholder heading). |
| D10 | `It covers one shared room in one housing association.` | `…and covers one shared room in one housing association.` | Repair of a visible defect (merge); wording after the verb preserved word for word. |
| D11 | `## Again` | *(removed)* | Repair of a visible defect (opaque/placeholder heading). |
| D12 | `It includes a 45-minute video call with two board representatives.` | `- a 45-minute video call with two board representatives` | Repair of a visible defect (regrouping); the fact is preserved word for word under a shared `It includes:` stem. |
| D13 | `## Things` | *(removed)* | Repair of a visible defect (opaque/placeholder heading). |
| D14 | `It includes a written account of the booking steps, unclear points and two possible simplifications.` | `- a written account of the booking steps, unclear points and two possible simplifications` | Repair of a visible defect (regrouping and de-duplication of the repeated `It includes`); the fact is preserved word for word. |
| D15 | `## Important` | `## What happens when you express interest` | Repair of a visible defect (opaque heading). |
| D16 | `The link opens an expression-of-interest form…` | `The link below opens an expression-of-interest form…` | Repair consequent on D5. Adds one positional word; the positional statement is true of the new layout, so **meaning** is held constant relative to the page. |
| D17 | Six `##` sections, all prose, one sentence each | Two `##` sections, one of them carrying a two-item bulleted list | Formatting change, in service of D8/D12/D14. |
| D18 | No YAML frontmatter | No YAML frontmatter | No difference. |
| D19 | `https://example.invalid/svale/intresse` | `https://example.invalid/svale/intresse` | No difference — destination unchanged. |
| D20 | `It places no order, requires no payment details and books no meeting.` and `Svale replies by email within three working days to discuss whether the review is suitable and suggest a meeting time.` | Identical | No difference. |
| D21 | — | — | **No mechanical corrections of any kind.** Spelling, punctuation, grammar, dates, numbers and the `SEK 4,800` currency form are byte-identical wherever the passage survives. The reply states the mechanical pass ran last in en_US and found nothing; that is consistent with the text in front of me. |

## 2. The account

- **D1** — reported, finding 2 ("The title announced nothing about the page… The title now names the subject the text itself supplies") and listed under *Removed*. Accurate as to the removal. It does not flag that "covers one shared room" became a title reading "Review of one shared room"; that nuance is unreported, though slight.
- **D2** — reported, finding 3, quoting the sentence, and listed under *Removed*. Accurate.
- **D3** — reported, finding 4, quoting the sentence, naming both the calque and the unmet promise, and listed under *Removed* "including its promise of a fantastic journey". Accurate.
- **D4, D9, D11, D13** — reported, finding 5, which quotes all six labels, and *Removed* lists them. Accurate. One imprecision: finding 5 says "three of them were placeholders"; on the face of the input, "It", "More", "Again" and "Things" are all placeholders — four, not three. The difference itself is reported correctly; only the count is loose.
- **D5** — reported, finding 8 ("What the page actually is came last… They now precede the link"). Accurate.
- **D6** — reported, finding 1, quoting both the old label and the contradicting sentence. Accurate, and the most precisely argued finding in the reply.
- **D7, D15** — reported, finding 5's closing line ("The two remaining headings name their contents"). Reported, though the reply does not print the two new headings in the findings; they are visible in the returned text. Accurate.
- **D8** — reported twice: finding 6 (the antecedentless `It`) and finding 7 (the four-way split). Accurate, except that finding 6 says "The opening sentence now names the review, so the later 'It includes' has one" — the naming happens in the opening sentence of the section, not in an opening sentence of the page, which no longer exists. Substantively right, loosely worded.
- **D10, D12, D14, D17** — reported, finding 7 ("They are now one section with the two coordinate items as a list"). Accurate.
- **D16** — reported explicitly under *Changed — one*, with the reason and the finding it follows from. Accurate.
- **D18, D19, D20** — not individually reported as differences, correctly, because they are not differences. The closing paragraph of *Claims removed or changed* asserts their preservation item by item ("SEK 4,800 including VAT; one shared room in one housing association; the 45-minute video call…; three working days…"), and each assertion checks out against the returned text.
- **D21** — reported: "One mechanical pass ran last, in en_US, and found nothing to correct." Consistent with the two texts.
- **Nothing in the returned text is unreported.** Every difference I can find maps to a numbered finding or to the *Changed* entry.
- One statement in the reply sits oddly with its own list: the header says "Correction budget: the default of 1, and it was spent", above eight repairs. Read as one correction *round* it is coherent; read as one correction it is not. It reports no difference wrongly, so it does not affect the account's accuracy about the text, but it is the one line a reader could not check.
- Finding 9's framing is slightly off: "a reader is asked to pay SEK 4,800" — after finding 1, the returned page no longer asks anyone to pay. The underlying point (the page never says who performs the review) is correct and the price is indeed stated.
- "Nothing was written to disk: `input.md` is untouched" — not something I am in a position to verify from the two files I may read; I neither confirm nor dispute it.

## 3. The frozen expectation

### Detect

**"Swedish idiom calque"** — reported. Finding 4: *"'Take the thumb out and discover a fantastic journey.' carried an idiom across from another language word for word, and promised an experience the page's own account — a 45-minute video call and a written account — cannot meet."* The finding names the calque and quotes it. It says "another language" rather than Swedish, which is the honest limit of what one text in English can establish. **Met.**

**"abstract audience description"** — reported. Finding 3: *"The opening sentence was empty. 'Decision-makers in a complex reality face growing complexity.' could have been moved in front of a different text without loss, and restated itself inside its own clause."* **Met.**

**"opaque fragmented headings"** — reported on both halves. Opacity, finding 5: *"'Start', 'It', 'More', 'Again', 'Things' and 'Important' gave a scanning reader no orientation and three of them were placeholders."* Fragmentation, finding 7: *"Four coordinate facts were split across four one-sentence sections. Price, coverage, the call and the written account describe one offer and had to be reassembled from four fragments."* **Met.**

**"misleading Book and pay action contradicted by the page"** — reported. Finding 1: *"The page's only action read 'Book and pay now', while the last section said the same link opens a form that 'places no order, requires no payment details and books no meeting' — it promised exactly the three things the destination refuses."* This is the expectation's central defect and it is named with the contradiction spelled out. **Met.**

### Preserve

**Price** — preserved: *"The review costs SEK 4,800 including VAT"*. Amount, currency and the VAT qualifier all intact. **Met.**

**Scope** — preserved word for word: *"covers one shared room in one housing association"*, including both instances of "one". **Met.**

**Timing** — preserved on both clocks: *"a 45-minute video call"* and *"Svale replies by email within three working days"*. **Met.**

**Deliverables** — preserved word for word as the two list items: *"a 45-minute video call with two board representatives"* and *"a written account of the booking steps, unclear points and two possible simplifications"*. **Met.**

**Conditions** — preserved word for word, and this is the passage the whole control turns on: *"It places no order, requires no payment details and books no meeting. Svale replies by email within three working days to discuss whether the review is suitable and suggest a meeting time."* The form's three fields — *"asking for a name, association and email address"* — are likewise untouched, and the order of conditions before action is now correct rather than reversed. **Met.**

**Destination** — preserved exactly: `https://example.invalid/svale/intresse`. Only the label changed. **Met.**

### Rejections

**"Existing content permits useful regrouping without a brief"** — this clause licenses the regrouping rather than forbidding it, and the run stayed inside the licence. Every word of the new title, the two new headings and the merged sentence is drawn from material already on the page ("review" and "housing association" from the closing paragraph, "costs… includes… express interest" from the sections themselves). Nothing was imported from outside the text. The one thing the page genuinely lacks — who performs the review — was left unrepaired and declared instead, finding 9: *"This was left standing deliberately: repairing it means asserting a fact the source text does not contain."* That is the corpus's licensed outcome: a reported finding retained because the text does not hold the fact. **The run did not make this mistake.**

**No unavailable-source verification** — the reply nowhere claims to have checked the URL, the price, Svale's identity or anything else outside the text; it explicitly declines to supply the one fact it would have had to fetch. **The run did not make this mistake.**

**No taste rewriting of clean material** — every surviving sentence returns byte-identical. The four removals and the label change each sit under a named finding. **The run did not make this mistake.**

## 4. R1

**Pass.**

The passage that decides it is the preserved conditions paragraph set against the changed label. Before, the page's only action read `[Book and pay now]` above a paragraph saying the same link *"places no order, requires no payment details and books no meeting"*. After, the label reads `[Express your interest]`, the paragraph is unchanged to the word, and the link sits beneath it. The defect the whole text is built around was detected, named against its own contradicting sentence, and repaired by changing the false side rather than the true one — while price, scope, timing, deliverables, the form's fields, the three-working-day reply and the destination URL all return intact. Removals are confined to passages that were themselves findings, each is listed, and the one finding that would have required a fact the text does not hold is declared unresolved instead of invented. The residual imperfections — the title's drift from "covers" to "of", a miscount of placeholders, the "budget of 1" line, and finding 9's mention of paying — are small, and none of them is a lost claim or an unreported change.
