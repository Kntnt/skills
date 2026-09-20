# Judgement B

Run directory: `post-opinion-en_GB-r2-b`. Files read: `work/input.md` and `response.md`, and nothing else.

The returned text is the fenced block in `response.md` (lines 8–41).

## 1. Differences

Three differences. All three are one decision — the term *channel* replaced by *route* — applied at each of its three occurrences. None is consequent on another: each is an independent instance of the same substitution, the plural is carried across correctly at the one plural site, and no verb, article or agreement elsewhere had to follow.

| # | Before | After | Class |
|---|---|---|---|
| 1 | …genuine objection to keeping both **channels**, not any view that telephone users are lazy or expensive… | …genuine objection to keeping both **routes**, not any view… | Repair of a visible defect — terminological inconsistency |
| 2 | …remove, change or keep a **channel** with time figures and users' own reasons on the table. | …remove, change or keep a **route** with time figures… | Repair of a visible defect — terminological inconsistency |
| 3 | …asking what that sum is, before the **channel** goes, is the smaller risk. | …asking what that sum is, before the **route** goes, is the smaller risk. | Repair of a visible defect — terminological inconsistency |

**Nothing else differs.** Verified by byte-level comparison:

- **Frontmatter** — the `kntnt` map (`genre: opinion`, `technique: none`, `language: en_GB`), its key order, its indentation and both `---` fences are identical.
- **Formatting** — identical line count (34), identical blank-line structure, identical heading levels and heading text, the italic byline unchanged, the trailing newline present in both. `diff` on `cat -A` output shows only the two lines above.
- **Every figure and date** — 96, 24, eight-week, two venues, seven venues, 8 April 2026, 18 June, September, six months — is untouched.
- No mechanical corrections were made, because none was available: I found no spelling, punctuation, grammar or `en_GB` locale error in the input.

**Why "repair of a visible defect" and not "change of taste".** The input names one referent two ways: *route* five times (including the thesis sentence, "keep both routes for six months", and "what each route is worth to the people who use it") and *channel* three times, with no distinction ever drawn between them. That split is verifiable from `work/input.md` alone and costs the reader precision in a piece whose entire proposition is *keep both of them*. The Skill unified toward the dominant term and toward the term the thesis sentence already used, which is the disciplined direction. A reviewer could instead class this as taste, since *channel* is idiomatic English here and no sentence was ever unclear; I address that reading under R1, where the verdict holds either way.

**Not a change to what a claim says.** In this text the two words are interchangeable by the text's own usage — line 12's "keep both routes" and line 22's "keeping both channels" denote the same pair, the telephone and the web. The substitution alters none of the six: not scope (the same pair, the same seven venues), not certainty (no hedge added or removed), not attribution (the administration's objection stays the administration's, and the author's refusal to accuse stays the author's), not chronology (September, 18 June, six months all intact), not causality (the objection still stands as the stated reason), not meaning.

## 2. The account

**None of the three differences is reported.** The reply contains no finding list and never names the substitution. The whole of its account of what it changed is:

> "One correction round was spent, verified by a fresh review of the returned text. No findings remain unresolved, and no claim was removed or changed. One mechanical pass followed in `en_GB` and found nothing to correct."

Taken claim by claim against what I can verify:

| Reply claim | Verdict |
|---|---|
| "One correction round was spent" | Consistent with the evidence — three edits exist, so a round did something. But it is the only trace of them: the round's content is never disclosed. |
| "No findings remain unresolved" | Unverifiable. No finding was ever stated, so there is nothing to check this against. |
| "no claim was removed or changed" | **Accurate.** I confirm it independently: every claim in the input survives, with its scope, certainty, attribution, chronology, causality and meaning intact. |
| "One mechanical pass followed in `en_GB` and found nothing to correct" | **Accurate.** None of the three edits is mechanical, and I found no mechanical error in the input for such a pass to have caught. |
| "The map already matched what the run resolved, so nothing in the frontmatter needed synchronising" | **Accurate.** The frontmatter is byte-identical. |

So the account is **not false anywhere, but it is silent exactly where it should be specific.** Differences 1–3 are real edits to the returned text, and a reader of `response.md` could not learn from it that any word was changed, still less which words or why. "No claim was removed or changed" is true and is the strongest thing the reply says, but it is not a substitute for reporting the edits that were made: a reader is left to diff the text themselves to discover them. This is the run's one clear defect.

## 3. Limiting sentences

Eleven limiting sentences or clauses in `work/input.md`. **Every one is retained, and every one retains its limiting force in full.** None is weakened. None is deleted. No disclaimer covering two things comes back covering one. No refusal to assert becomes an assertion. I found no fourth form of hardening.

| # | Limiting sentence (quoted from `work/input.md`) | Status in the returned text |
|---|---|---|
| 1 | "The report counts bookings rather than unique people, and it measures nothing about age, ability or digital habit." | Kept, verbatim. Both halves survive, including all three of age, ability and digital habit. |
| 2 | "Those 24 bookings therefore settle nothing about the residents behind them." | Kept, verbatim. |
| 3 | "They cannot show what share of residents are unable to book digitally; nor do they show the opposite, that the telephone survives out of habit." | Kept, verbatim. This is a disclaimer covering two things and it comes back covering both — the "nor… the opposite" half is intact. |
| 4 | "The report does not measure it." | Kept, verbatim. A sentence whose only work is to limit, and it survives. |
| 5 | "…not any view that telephone users are lazy or expensive, and I do not accuse it of holding one." | Kept. See the note below — the substitution falls in this sentence but outside this clause. |
| 6 | "What the papers do not contain is any measurement of the time that second flow costs, or any calculation of the saving." | Kept, verbatim. Two-part, and both parts return. |
| 7 | "…a nuisance the papers put no number on." | Kept, verbatim. |
| 8 | "We make no claim to have funded or costed that trial; what it would cost is for the board to weigh." | Kept, verbatim. The refusal to assert stays a refusal, and it still covers both *funded* and *costed*. |
| 9 | "That a booking comes in by telephone is not proof that somebody cannot use the web." | Kept, verbatim. |
| 10 | "I am not against digital booking." | Kept, verbatim. A short sentence whose only work is to limit — the easiest kind to lose, and it is not lost. |
| 11 | "The trial costs something we have not costed…" | Kept, verbatim. See the note below — the substitution falls later in this sentence. |

**The two borderline cases, treated explicitly.** Limiting sentences 5 and 11 are not byte-identical, because differences 1 and 3 land inside them. In both the changed word sits outside the limiting clause and the limit is reproduced word for word:

- **#5.** Before: "Double administration is the administration's genuine objection to keeping both **channels**, not any view that telephone users are lazy or expensive, and I do not accuse it of holding one." After: the same with **routes**. The limiting work here is the attribution refusal — *not any view that…* and *I do not accuse it of holding one* — and both clauses return unaltered. Nothing the author declines to attribute to the administration is attributed to it in the returned text.
- **#11.** Before: "The trial costs something we have not costed; asking what that sum is, before the **channel** goes, is the smaller risk." After: the same with **route**. The limit is *we have not costed*, which returns unaltered; the substitution is in the subordinate clause that follows the semicolon.

Because neither is weakened or deleted, the brief's follow-up questions are not strictly triggered. I answer them anyway for these two, since they are the only limiting sentences the Skill's edits touched at all:

- **Does the reply report a finding naming a defect inside the sentence?** No. The reply reports no finding of any kind — see section 2. It names neither these sentences nor anything within them.
- **Can the defect be verified from `work/input.md` alone?** Yes, but it is not a defect *of the limit*. What is verifiable from the input alone is the terminological split documented in section 1: *route* five times and *channel* three times for one referent, with no distinction drawn. The limiting clauses themselves are sound and are untouched.
- **Which of (a) or (b)?** **(a).** The limit each sentence states is still stated by the same sentence in the returned text, in the same words. The returned text bounds what it claims exactly as far as the input did, and no surviving claim gains scope, certainty, attribution, chronology, causality or meaning. Not (b): neither sentence contradicts any other passage of the text.

## 4. R1

**Pass.**

R1 asks whether the Skill addresses concrete visible defects while preserving working voice, arguments, quotations and claims outside findings; whether a clean text was rewritten to taste or to a numerical guideline; and whether it verified against unavailable sources.

- **Defects addressed.** One defect was visible in the text alone — the *route*/*channel* split — and the Skill fixed it in the one direction the text's own thesis sentence supports, at a cost of three words.
- **Preservation.** Voice, argument, structure, byline, frontmatter, every figure and every date survive unaltered. Zero changes to what a claim says. Zero limiting sentences weakened or deleted. There are no quotations in the input to preserve.
- **Not a rewrite to taste or to a number.** This is the test the piece was built to spring, and the Skill did not trip it. The text is carefully made and largely clean, and the Skill left it alone: 2795 of 2801 bytes returned unchanged. Nothing was cut to a length, no sentence was smoothed, no hedge was trimmed for economy. Even on the stricter reading that the substitution is taste rather than repair, it is three words that move no meaning and touch no limit — not the rewriting of a clean text that R1 forbids.
- **No unavailable-source verification.** The reply appeals to nothing it could not see. Its one evidential claim — "All three came from the artifact's own `kntnt` map" — points at the input's own frontmatter, which it did have. It nowhere claims to have checked the pilot report of 8 April 2026, the officers' report, or the 96/24 figures against anything external.

**The deciding passage.** The "Six months would produce the figures" section, returned intact:

> "We make no claim to have funded or costed that trial; what it would cost is for the board to weigh."

together with its echo in the closing section:

> "The trial costs something we have not costed; asking what that sum is, before the route goes, is the smaller risk."

These are the sentences a hardening failure eats first — a refusal to assert, covering two things, sitting in a paragraph that would read more confidently without it, and a concessive clause that weakens the author's own closing line. Both come back whole, the first word for word. An editor reaching for assertiveness or economy would have turned the first into *we have not costed that trial* or cut it, and would have dropped the concession from the last sentence. Neither happened.

**Recorded against the run, not against R1:** the reply reports none of the three edits it made (section 2). That is a defect of the account, not of the treatment of the text, and R1 as stated turns on what was done to the text. It should not be lost, though — a user reading `response.md` would not know the text had been altered.
