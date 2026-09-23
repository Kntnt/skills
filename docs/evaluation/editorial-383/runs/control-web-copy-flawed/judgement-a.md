# Judgement A — control-web-copy-flawed

Read: `work/input.md`, `response.md`, `expectation.md`. Nothing else.

## 1. Differences

| # | Before | After | Class |
|---|---|---|---|
| 1 | `# Unlock your association's full potential` | `# Review of your association's shared-room booking: SEK 4,800` | Repair of a visible defect (headline asserted a benefit nothing on the page supports), carrying a **meaning** change to what the headline claims: from a promise of unlocked potential to a naming of the thing sold. |
| 1a | (headline held no price; the price appeared once, as "SEK 4,800 including VAT") | headline now reads `SEK 4,800` bare | Change to a claim — **scope**. A qualification that stood on the only statement of the price is absent where the price is now first stated. The body statement keeps "including VAT", so the qualification is not lost from the text, only from the headline. |
| 1b | "It covers one shared room in one housing association" / "a written account of the booking steps" | headline calls the subject a "shared-room booking" | Change to a claim — **scope**, mild. The input says the review *covers* a shared room and accounts for *booking steps*; the headline fuses these into "shared-room booking". Inferred from two sentences that are both in the text, not from outside it. |
| 2 | `Decision-makers in a complex reality face growing complexity.` | removed | Repair of a visible defect (abstract audience description; the sentence restates its own subject and would sit in front of any text). Claim removed. |
| 3 | `Take the thumb out and discover a fantastic journey.` | removed | Repair of a visible defect (Swedish idiom calque, "ta tummen ur", plus a promise of a "fantastic journey" the page never keeps). Two claims removed. |
| 4 | `## Start` | `## Expressing interest and what happens next` | Repair of a visible defect (opaque one-word heading). |
| 5 | `[Book and pay now](https://example.invalid/svale/intresse)` | `[Express interest in a review](https://example.invalid/svale/intresse)` | Repair of a visible defect (the label promised an order and a payment the page's own last paragraph denies), carrying a **meaning** change to the action claimed. Destination unchanged, character for character. |
| 6 | `## It`, `## More`, `## Again`, `## Things` (four headings) | absorbed into one heading `## What the review covers and costs` | Repair of a visible defect (headings that declare nothing; four one-sentence sections of identical shape). |
| 7 | `## Important` | heading removed; its paragraph now sits under heading #4 | Repair of a visible defect (opaque heading) plus regrouping. |
| 8 | The link-explanation paragraph stood last, six headings after the link | It now stands immediately beneath the link | Repair of a visible defect (the correction to the action depended on a paragraph the reader met last). Regrouping only; wording untouched. |
| 9 | `It costs SEK 4,800 including VAT.` | `The review costs SEK 4,800 including VAT and covers one shared room in one housing association.` | Repair of a visible defect (a pronoun with no antecedent on the page), plus a sentence merge. The referent "review" is taken from the text's own last paragraph ("whether the review is suitable"). No scope, certainty or meaning moved: figure and qualification intact. |
| 10 | `It includes a 45-minute video call with two board representatives.` + `It includes a written account of the booking steps, unclear points and two possible simplifications.` | `It includes a 45-minute video call with two board representatives, and a written account of the booking steps, unclear points and two possible simplifications.` | Sentence merge under one `includes`. No claim change; every quantity and item survives verbatim. |
| 11 | Eight blocks in the order title, opener, CTA, price, scope, call, deliverables, link note | Five blocks in the order title, CTA section (CTA + link note), covers-and-costs section | Repair/regrouping. The call to action stays first, as in the input. |
| 12 | Plain Markdown, no frontmatter | Plain Markdown, no frontmatter; returned inside a ```markdown fence in the reply | Presentational only. Neither file has frontmatter, so none was altered. |

No mechanical corrections were made. Nothing in the returned text differs from the input in spelling, punctuation, grammar, or a locale form of a date, number or currency: "SEK 4,800", the comma decimal-free thousands separator, "45-minute" and "three working days" all stand as they arrived.

Claims in the input that survive untouched, word for word: "SEK 4,800 including VAT", "one shared room in one housing association", "a 45-minute video call with two board representatives", "a written account of the booking steps, unclear points and two possible simplifications", "The link opens an expression-of-interest form asking for a name, association and email address.", "It places no order, requires no payment details and books no meeting.", "Svale replies by email within three working days to discuss whether the review is suitable and suggest a meeting time."

Nothing in the returned text claims or implies that any source outside the text was consulted.

## 2. The account

- **#1 (headline rewritten)** — Reported, twice and accurately: "rewrote the headline so that it names what is on offer instead of asserting a benefit the page never shows", and the removal of the "full potential"/"unlock" promise is listed under removed claims with its reason.
- **#1a (bare price in the headline)** — Reported, accurately, and as the stronger of the two open findings: "The headline states the price without the qualification the body gives it… This defect was not in the text as it arrived, where the price appeared once and fully qualified. The repair of the headline finding put it there." It names the reader's cost and offers the two ways out. The reply also correctly attributes the defect to its own correction rather than to the input.
- **#1b ("shared-room booking")** — Not reported. The reply says only that the headline "names what is on offer". It does not flag that naming the subject a *booking* is an inference joining "covers one shared room" to "the booking steps". This is the single difference the account passes over. It is small and defensible from the text, but it is unreported.
- **#2 (audience sentence)** — Reported accurately, with the reason: "named the whole proposition as an opening that would sit in front of any text and as unsupported by any sentence on the page."
- **#3 (idiom and journey)** — Both halves reported: "the literally translated Swedish idiom" in *What else changed*, and "The promise of 'a fantastic journey.' … Removed by the repair of the second-sentence finding, which named it as a promise the page does not keep."
- **#4, #6, #7 (headings)** — Reported accurately and with the right count: "It replaced the six headings that declared nothing with two that say what their sections hold."
- **#5 (call to action)** — Reported accurately: "It relabelled the call to action, which had promised a booking and a payment that the form on the other end of the link makes neither."
- **#8 (paragraph moved up)** — Reported: "moved the paragraph explaining the link up to sit beside the link itself."
- **#9 (pronoun resolved)** — Reported: "named the review so that the sentences no longer open on a pronoun with nothing behind it."
- **#10, #11 (merges)** — Reported: "merged the four one-sentence sections of the same shape into one."
- **#12 / no mechanical changes** — Reported, and correct: "The closing mechanical pass found nothing to correct and changed no character." Verified against the two files.
- **Preservation claim** — The reply asserts the three link-bounding sentences are "preserved word for word", and lists "one shared room in one housing association", "45-minute", "two board representatives", "two possible simplifications" and "three working days". Every one of these checks out against `work/input.md`.
- **Removal count** — The reply says three claims were removed and nothing else. Correct, if "full potential"/"unlock", the complexity sentence and the "fantastic journey" are counted as the three; the idiom "take the thumb out" went with the third and is accounted for separately as wording rather than as a claim, which is fair — it asserts nothing.
- **Extra reported finding** — "Three working days" under en_US is raised as an open finding. By this brief's own rule it is a locale/register matter belonging to the mechanical pass; reporting it is not held against the Skill, and it is honest about the phrase having arrived that way.

## 3. The frozen expectation

The expectation names four things to detect, six to preserve, and one licence.

**Detect: "Swedish idiom calque."** Reported. *What else changed*: "the run cut the empty opening and the literally translated Swedish idiom". The calque is the input's "Take the thumb out"; it is gone from the returned text and named as such.

**Detect: "abstract audience description."** Reported. The removal entry reads: "**That decision-makers face growing complexity.** Removed by the repair of the opening-sentence finding, which named the whole proposition as an opening that would sit in front of any text and as unsupported by any sentence on the page." That is the audience sentence, named for exactly the defect the expectation has in mind.

**Detect: "opaque fragmented headings."** Reported. "It replaced the six headings that declared nothing with two that say what their sections hold", and the fragmentation itself: "merged the four one-sentence sections of the same shape into one."

**Detect: "misleading Book and pay action contradicted by the page."** Reported, and the contradiction is named as such: "It relabelled the call to action, which had promised a booking and a payment that the form on the other end of the link makes neither." The new label is "Express interest in a review".

**Preserve: price.** Preserved: "The review costs SEK 4,800 including VAT". The figure and the VAT qualification both survive in the body. The headline's bare "SEK 4,800" is the one wrinkle; it does not remove the qualification from the text, and the Skill itself files it as an open finding.

**Preserve: scope.** Preserved: "covers one shared room in one housing association".

**Preserve: timing.** Preserved: "a 45-minute video call" and "Svale replies by email within three working days".

**Preserve: deliverables.** Preserved: "a 45-minute video call with two board representatives, and a written account of the booking steps, unclear points and two possible simplifications".

**Preserve: conditions.** Preserved verbatim: "It places no order, requires no payment details and books no meeting", together with "to discuss whether the review is suitable and suggest a meeting time" and the form's three asked-for fields, "a name, association and email address".

**Preserve: destination.** Preserved: `https://example.invalid/svale/intresse`, unchanged.

**Licence: "Existing content permits useful regrouping without a brief."** Taken up, and correctly. The regrouping — two named sections, the link note lifted to sit beside the link, four identical stubs merged — draws on nothing that was not already on the page. No fact, quantity, name or condition in the returned text is absent from the input.

**Rejections.** The expectation names no rejection other than what the preserve clauses forbid, and the run made none of those mistakes: nothing preserved was dropped, no removal went unreported, and no claim rests on material the text does not hold. The run did not verify anything against an unavailable source, and does not pretend to have.

## 4. R1

**Pass.**

The run addressed every visible defect the text carried and reported each one, and it did so without touching a single load-bearing claim. The passage that decides it is the body sentence that carries the commercial content through the rewrite intact —

> "The review costs SEK 4,800 including VAT and covers one shared room in one housing association. It includes a 45-minute video call with two board representatives, and a written account of the booking steps, unclear points and two possible simplifications."

— set beside the link note, which survives word for word: "It places no order, requires no payment details and books no meeting." Four opaque headings, an empty opener, a calqued idiom and a false call to action were all repaired; nothing outside those findings was moved.

Against the pass stands one blemish: the rewritten headline prints "SEK 4,800" without "including VAT", a **scope** weakening introduced by a correction rather than inherited from the input. It does not carry R1 into failure, for three reasons. The qualification is still in the text, one section below. The headline was itself a finding, so the change sits inside findings rather than outside them. And the Skill diagnosed the defect in its own output, named it the reason the loop stopped, priced it for the reader ("the difference between SEK 4,800 and SEK 6,000") and handed back the two ways to settle it — which is what R1 asks of an irreparable finding, not something it counts as a concealed loss.

The one unreported difference, the headline's "shared-room booking", is an inference joining two sentences that are both on the page. It is not a claim brought in from outside, and its absence from the account is a small gap rather than a preservation failure.

No clean passage was rewritten to taste: every change lands on a defect the expectation names or on the fragmentation it licenses regrouping for. No mechanical correction was made at all, so nothing was mistaken for the proofreading pass's work.
