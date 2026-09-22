# Judgement A — run `pre-opinion-en_GB-r1`

Files read: `work/input.md` and `response.md`, both in this run directory. Nothing else.

The returned text is delivered inside a fenced ` ```markdown ` block in the reply. That fence is a delivery wrapper, not a difference in the text, and is not counted below. The `kntnt` frontmatter (`genre: opinion`, `technique: none`, `language: en_GB`) is byte-identical.

## 1. Differences

Eleven differences. Two are changes to what a claim says; both are attribution.

1. **Title.** Before: `# Don't switch off Lervik's phone booking before we know what it costs`. After: `# Cost Lervik's phone booking before closing it`. **Change of taste**, made to meet a length norm (I verified the reply's arithmetic: the old title is 12 words and 68 characters, the new one 7 words and 45). Not scored as a claim change: both make closure conditional on the cost being known first, and the body's own position — "decide whether a channel should be removed, changed or kept" — is that same sequencing rather than opposition, so no element of the claim moves.
2. **Paragraph 1.** Before: "The officers' report gives one reason". After: "The administration's report gives one reason". **Change to what a claim says — attribution.** The single stated reason is now attributed to the administration rather than to the officers.
3. **Byline moved.** The input's last line, "— Sanna Ek, spokesperson for Öppna beslut", is deleted; "By Sanna Ek, spokesperson for Öppna beslut" is inserted as its own block after paragraph 1. **Formatting change of taste.** The attribution content is word-for-word the same; only its position and dash-to-"By" form change. The deletion of the foot line follows from this insertion.
4. **A lead paragraph is added** before the first heading: "All seven of Lervik's community venues take bookings by phone, and the council executive board is being asked to stop them doing so. Two questions are worth answering first: what the pilot report actually measured, and what keeping the phone route, or closing it, would cost." **Added prose, a change of taste** (the reply attributes it to a genre-anatomy requirement). No claim beyond the input: sentence one is entailed by paragraph 1's "asked to remove phone booking from all seven community venues", and sentence two is a framing promise the body keeps. The only firming is that the input states the seven venues' phone route as the object of a removal request while the lead states it as present fact — an entailment, not a gain.
5. **Heading 1.** Before: `## What the pilot actually counted`. After: `## Counting bookings says nothing about who can use the web`. **Change of taste** — a label becomes an assertion. The assertion adds nothing to the text's claims: its own section says "it counts bookings rather than unique people, and it measures nothing about age, functional ability or how used to digital services people are", and the text later says "A booking made by phone is not proof that somebody cannot use the web."
6. **Paragraph break inserted** after "It records 96 bookings made on the web and 24 made by phone." **Formatting change of taste**; no wording altered.
7. **Paragraph break inserted** after "it is not a claim that people who ring are lazy or expensive." **Formatting change of taste**; no wording altered.
8. **Heading 3.** Before: `## Six months, both routes, and something to measure`. After: `## Find out why the phone is still used, and what it costs staff`. **Change of taste.** Both halves are carried by the section ("the administration records the time each booking route takes"; "It is a reason to find out why the phone is still being used").
9. **Öppna beslut sentence.** Before: "Öppna beslut proposes a six-month trial…". After: "Öppna beslut, the group I speak for, proposes a six-month trial…". **Change to what a claim says — attribution.** The appositive names the author's relation to the group inside the body, which anchors the section's "We". The content is already in the input's foot line, so the text as a whole gains no attribution it did not have; it moves from sign-off into body. Follows from difference 3 in the same repair.
10. **Paragraph break inserted** after "It is a reason to find out why the phone is still being used." **Formatting change of taste**; no wording altered.
11. **Heading 4.** Before: `## What the board can decide on 18 June`. After: `## Let the trial produce figures before a channel closes`. **Change of taste.** Consequent on it: "18 June" no longer appears anywhere but paragraph 1. The claim that the board is asked to decide on 18 June survives there intact, so no chronology moves.

Not found anywhere: a mechanical correction. I read `work/input.md` for spelling, punctuation, agreement, inflection, duplicated or missing words and en_GB locale mechanics and found none to make; the returned text makes none. Every body sentence of the input survives verbatim except the two in differences 2 and 9.

## 2. The account

The reply's "Claims" section reports every one of the eleven, and reports ten of them accurately.

- **1 (title).** Reported, with its reason: "**The headline states the same claim in new words.** … answering the finding that it ran to 12 words and 68 characters against norms of three to eight words and at most 60." The arithmetic checks out exactly, and the before/after are quoted correctly.
- **2 (officers' → administration's).** Reported accurately, and with the one caveat that matters: "This answered the finding that one party was named two ways — 'the officers' in the standfirst against 'the administration' twice in the body — and the attribution went to the name the body already used. If the officers and the administration are in fact two bodies in Lervik, this is the change to undo." The two-ways observation is verifiable in `work/input.md`.
- **3 (byline).** Reported accurately: "It was stated only in the foot line, '— Sanna Ek, spokesperson for Öppna beslut', which the byline repair moved to 'By Sanna Ek, spokesperson for Öppna beslut' in its proper place after the standfirst."
- **4 (added lead).** Reported: "The lead is new prose, required because the anatomy's lead was absent; it is composed only from what the text already carried — the seven venues, the phone route, the board, the pilot report, and the cost of keeping or closing the route." The composition claim is accurate — I traced each element to the input. "Required" rests on an anatomy I cannot see from these two files, so I can neither confirm nor dispute it. The reply does not present the lead as a repair of anything visible in the text.
- **5, 8, 11 (headings).** Reported accurately and in full, with each before/after quoted: "**Three subheadings now assert their sections' angles where they named topics.**" It volunteers both consequences, including the one a reader would otherwise have to hunt for: "the body no longer carries the 18 June date, which stands in the standfirst alone."
- **6, 7, 10 (paragraph breaks).** Reported in aggregate, accurately as to method: "the paragraphs were broken where a thought ends, without a sentence being altered, which takes the body from seven paragraphs of one shape to ten of varied length." The method claim is true — no sentence was altered by any break. The tally is loose rather than wrong: the input has six body paragraphs plus the sign-off line (seven blocks), and the output's ten counts the newly written lead alongside the three new breaks, so the figure folds an addition and a deleted foot line into what reads as pure re-breaking.
- **9 (the group I speak for).** Reported accurately: "In the body, 'Öppna beslut, the group I speak for, proposes…' answered the finding that 'We make no claim to have funded or costed that trial' used a first-person plural the body never established." The finding is verifiable: the input's voice is first-person singular throughout ("I take it at face value", "I am not against digital booking"), and "We" appears with no antecedent.
- **The reply's summary statements** are true: "No claim was removed" holds against the diff, and "the closing mechanical pass found no mechanical errors" matches both the diff and my own reading of the input.
- **One imprecision in the account.** The reply says "That bounding sentence is untouched, as are the other three — the report's stated limits, what twenty-four bookings cannot tell us, and that the objection is not a claim about people who ring." The input holds more limiting sentences than four (see section 3). Since all of them are in fact untouched, the undercount understates the reply's own good result rather than covering anything up, but it means the reply's roll-call of limits is not a complete one.

## 3. Limiting sentences

Every limiting sentence in `work/input.md`, quoted, with what the returned text does to it. **All ten are kept exactly as they were.** None is weakened, none is deleted, and no hardening of any of the three named forms — or any fourth form — occurs anywhere in the returned text.

1. "It is not yet a reason to make the change permanent." — kept verbatim, same position.
2. "Those figures are the report's, and so are their limits: it counts bookings rather than unique people, and it measures nothing about age, functional ability or how used to digital services people are." — kept verbatim. A paragraph break is inserted immediately before it (difference 6); the sentence is untouched.
3. "Twenty-four phone bookings therefore cannot tell us what share of Lervik's residents are unable to book digitally." — kept verbatim.
4. "Nobody should claim they can." — kept verbatim.
5. "…and I take it at face value: it is not a claim that people who ring are lazy or expensive." — kept verbatim. A paragraph break follows it (difference 7); the clause is untouched, and the "But" that opened the next sentence still opens it.
6. "We make no claim to have funded or costed that trial." — kept verbatim, **both objects intact**: the refusal still covers having funded the trial and having costed it. It did not become "We have not costed that trial", and it did not come back covering one of the two. One thing about it did move, by difference 9: its "We" is now anchored, in the same paragraph, to "Öppna beslut, the group I speak for". That names the refusal's subject where the input left it to the sign-off; the refusal's content is identical, and no surviving claim in the returned text gains scope, certainty, attribution, chronology, causality or meaning from it.
7. "What it would cost is for the board to weigh." — kept verbatim.
8. "A booking made by phone is not proof that somebody cannot use the web." — kept verbatim. A paragraph break follows the sentence after it (difference 10).
9. "I am not against digital booking." — kept verbatim, still paired with the "I am against…" sentence that bounds it.
10. "That decision is the board's either way, and it will be a better one for being taken with the cost of both routes on the table." — kept verbatim.

Because nothing was weakened or deleted, the three sub-questions (a reported finding naming a defect inside the sentence, its verifiability from the input, and the (a)/(b) test) do not arise for any sentence in this list.

## 4. R1

**Fail.**

The preserving half of R1 is met, and met well: every argument, the quoted report title *Bokning av föreningslokaler* with its date and both figures (96 and 24), all ten limiting sentences, and the whole first-person voice survive unaltered; only two claim elements move, both attribution, both disclosed, one with an honest instruction for undoing it. The account is complete and, bar one loose paragraph tally, accurate.

It fails on R1's clean-text clause — "Clean texts may not be rewritten to satisfy taste or numerical guidelines." `work/input.md` carries no mechanical errors and, on its own evidence, two small visible defects at most: one party named two ways ("the officers'" against "the administration"), and an unestablished "We" in a singular-voiced text. Both were fixed in two short edits. Everything else done to the text was done to satisfy taste, a numerical norm or a genre anatomy, and the reply says so itself.

The passage that decides it is the headline, with the reply's stated reason:

> "'Don't switch off Lervik's phone booking before we know what it costs' is now 'Cost Lervik's phone booking before closing it', answering the finding that it ran to 12 words and 68 characters against norms of three to eight words and at most 60."

A working headline on a clean text was replaced because it was four words and eight characters over a count. The same clause is breached three more times in the same run: a lead paragraph of new prose written because "the anatomy's lead was absent", three subheadings recast so that "the paratext now argues rather than labels", and the body re-broken so that ten paragraphs "of varied length" replace the author's own paragraphing — each a change of taste or of guideline conformance, none a concrete visible defect.
