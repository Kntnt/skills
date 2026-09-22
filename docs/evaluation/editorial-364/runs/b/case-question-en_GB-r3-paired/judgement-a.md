# Judgement — case-question-en_GB-r3-paired

## 1. Every difference between input and delivered text

A full mechanical diff of the two files returns exactly four hunks. Nothing else in the article — frontmatter, title, standfirst, byline, third heading, every body paragraph, both quotations — differs by a single character.

| # | Before | After | Kind |
|---|--------|-------|------|
| 1 | Lead sentence: “Fenwick Instrument Repairs services brass and woodwind instruments.” | “Fenwick Instrument Repairs services brass and woodwind instruments, **and kept its jobs on separate paper sheets**.” | Repair of a defect visible in the text (the before-state sat only in the standfirst), carrying an **addition to what the body claims**. The added claim is restated from the same text’s standfirst (“Jobs split across separate paper sheets went onto one shared bench schedule”), so it introduces no fact the text did not already carry; its subject (Fenwick), chronology (past, pre-trial) and scope (its jobs) match the standfirst. |
| 2 | Heading: “The team agreed the terms before Benchline configured them” | “Fenwick set the job statuses before Benchline configured them” | Repair of a defect visible in the text. Two defects: “the terms” had no resolvable referent in the section, and in `en_GB` *agreed the terms* idiomatically denotes settling a contract, which the section is not about. Also a **claim change by subject and specificity**: “the team” → “Fenwick”, “the terms” → “the job statuses”. Both are supported by the paragraph directly beneath — “The workshop defined the statuses itself and decided who would update them” — and the chronology (“before Benchline configured them”) is unchanged and matches “Benchline configured those choices”. |
| 3 | Bridge: “Benchline’s case writer asked workshop manager Priya Vale **by email** what the team had to settle before the schedule was useful.” | “**In an email interview**, Benchline’s case writer asked workshop manager Priya Vale what the team had to settle before the schedule was useful.” | Repair of a defect visible in the text (the definite “the interview” two sections later had no antecedent), carrying a **small claim change of characterisation**: an emailed question-and-answer is relabelled *an email interview*. The label is not invented — the input itself calls the exchange “the interview” in the second section — so the change imports the text’s own later word to its first mention. The medium (“email”) is retained, not lost. |
| 4 | Heading: “Neither document measures repair speed” | “The trial evidence does not measure repair speed” | Repair of a defect visible in the text. “Neither document” presupposed two documents the reader had never been given, and one of the two sources the section weighs is an interview, not a document. **Claim change by subject and scope**: from two unnamed documents to “the trial evidence”. The widened subject is exactly what the section’s closing sentence asserts (“The summary and the interview carry the team’s reported experience, not a measured improvement in repair speed”), and the negative modality is unchanged. |

No mechanical corrections (spelling, punctuation, grammar, locale form) were made; none was needed. No change of taste was made. Nothing was deleted: the removals at 2 and 4 are heading replacements, and the removal at 3 is a repositioning of “by email” inside the same clause.

## 2. Bridges into quotations

The input carries two quotations, both direct speech from Priya Vale.

### Quotation 1 (“We had to agree what ready for work meant…”)

- **Bridge as the input carries it:** “Benchline’s case writer asked workshop manager Priya Vale by email what the team had to settle before the schedule was useful. Vale answered:”
- **Bridge as the delivered text carries it:** “In an email interview, Benchline’s case writer asked workshop manager Priya Vale what the team had to settle before the schedule was useful. Vale answered:”
- **Class before: (b).** It names the attribution (Benchline’s case writer, Priya Vale, workshop manager), the occasion (the question, put by email) and the question’s topic — “what the team had to settle before the schedule was useful” — and stops there. It does not deliver the answer. The quotation’s payload is the *content* of what had to be settled (the meaning of *ready for work*) and the reason it mattered (a part in the building need not have reached the right bench); the bridge supplies neither. Naming the topic a quotation then speaks to is not class (a).
- **Class after: (b).** Unchanged in kind. The only added words are “In an email interview”, which name the occasion — squarely class (b) territory — and the speech tag remains bare attribution (“Vale answered”).
- **Where it came back changed:** the reply’s finding 3 names the change explicitly and gives the reason (“the exchange is named as an email interview where it first appears”). The change supplies **no** event, fact, name or figure the rest of the text does not carry: “interview” is the input’s own word for this exchange in the second section, and “email” was already in the input’s bridge. **Nothing the input’s bridge carried was lost** — the emailed medium, the asker, the asked, her role and the question topic all survive verbatim in the delivered clause.

### Quotation 2 (“I would use it again for new jobs…”)

- **Bridge as the input carries it:** “The manager approved continued use for new jobs, and postponed adding the backlog until the team had reviewed its status definitions. Asked whether the choice would be made again, and what would change, Vale answered:”
- **Bridge as the delivered text carries it:** identical, word for word.
- **Class before: (b) for the bridging clause proper; the sentence standing before it is (a).** The clause immediately before the quotation — “Asked whether the choice would be made again, and what would change, Vale answered” — is a speech tag that carries the question put and the attribution, and no more: class (b). The narrative sentence standing before *that*, however, already delivers what the quotation is there to deliver: “approved continued use for new jobs” pre-states “I would use it again for new jobs”, and “postponed adding the backlog until the team had reviewed its status definitions” pre-states “I would allow another week to check the status names before adding the backlog”. Read as the whole run-up, a reader meets the quotation as the bridge said again — class (a). The section heading, “Vale would allow an extra week for the status names”, compounds this, though a heading is not a bridge.
- **Class after: unchanged — (b) for the clause, (a) for the sentence before it.** Not one character differs.
- **Where it came back changed:** it did not. The reply does not report this pre-statement as a finding; it is a real weakness in the input that the review did not raise. It is, however, a missed improvement rather than damage, and R1 asks whether the review preserved what it did not find — it did.

## 3. The quotations themselves

| Quotation | Wording returned | Verdict |
|---|---|---|
| ‘We had to agree what ready for work meant. A part being in the building did not always mean that it had reached the right bench.’ | Character-for-character identical, including the `en_GB` single curly quotation marks and the unquoted *ready for work*. | Unchanged. Meaning, stance, certainty, the reservation carried by “did not always mean”, and Vale’s plain workshop voice all intact. |
| ‘I would use it again for new jobs. I would allow another week to check the status names before adding the backlog.’ | Character-for-character identical. | Unchanged. The conditional modality (“I would”), the limit (“for new jobs”), the hedge (“another week to check”) and the voice all intact. |

No quotation was trimmed, merged, paraphrased, re-punctuated or moved. Both remain attributed to Vale in the same section and the same order.

## 4. R1 — **PASS**

**Concrete visible defects addressed.** All four applied changes answer defects legible in the text itself, with no appeal to absent material: a body that never said what the schedule replaced; a heading whose referent (“the terms”) resolved to nothing and whose `en_GB` idiom pointed at a contract; a definite first mention (“the interview”) with no antecedent; a heading presupposing two documents the reader had not been given and miscounting an interview as one. None depends on knowing the supplier deck, the workshop summary or any source the Skill did not have.

**Working material preserved.** The argument is untouched: the text’s two load-bearing restraints — that the summary does not measure repair duration, revenue or customer satisfaction, and that summary and interview carry reported experience rather than a measured improvement — came through verbatim. Both quotations came through verbatim. The standfirst, byline, third heading, the 38-job figure, the 23 February 2026 date, the January 2026 start, the six-week span, the four staff and the one online session are all unaltered. Nothing was rewritten to taste: three of the four sections’ prose is byte-identical, and the review declined to touch paragraphs under the headings it rewrote, saying so.

**Removals and changed claims, against what the reply reports.**

- Lead addition (“and kept its jobs on separate paper sheets”) — **reported, finding 1, accurately**, including its provenance (“from the text’s own material”). One imprecision: the closing claim account says “No claim was removed, and none was left standing with its scope, certainty, attribution, chronology, causality or meaning moved,” which is true as far as it goes but does not state that a claim was *added* to the body. Finding 1 states it plainly, so the reply as a whole does not mislead.
- “The team agreed the terms…” removed for “Fenwick set the job statuses…” — **reported, finding 2, accurately**, with both defects named and the promise that the paragraphs beneath are untouched, which holds.
- “by email” repositioned as “In an email interview” — **reported, finding 3, accurately**; the stated reason (a definite first mention) is exactly the defect in the text.
- “Neither document…” removed for “The trial evidence…” — **reported, finding 4, accurately**, including the miscount of the interview as a document, which the section’s own closing sentence confirms.
- Nothing was changed that the reply fails to name, and the reply names nothing it did not change: the four findings map one-to-one onto the four diff hunks.

**The irreparable finding.** Finding 5 — no call to action at the ending — is declared unresolved rather than repaired, on the stated ground that the account supplies no offer, link or contact route and one would have to be invented. This is the correct disposal: the text was left exactly as it was, and the matter handed to a person. The Skill did not excuse itself with material it never had, nor invent a next step to close a finding.

**Counted against it, and not enough to fail.** The review left the strongest bridge defect in the text: the sentence before quotation 2 says the quotation’s content in advance, making the quotation an echo. That is an unfound defect, not a caused one, and R1 does not require exhaustiveness. Against it stand four accurate repairs, two verbatim quotations, an honestly unresolved fifth finding and a claim account that matches the diff.
