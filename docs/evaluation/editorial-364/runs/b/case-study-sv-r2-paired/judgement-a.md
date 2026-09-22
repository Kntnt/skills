# Judgement — case-study-sv-r2-paired (R1)

## 1. Every difference between input and delivered text

| # | Before | After | Kind |
|---|--------|-------|------|
| 1 | `# Elm Quay fick en gemensam bild av felanmälningarna` | `# Elm Quay testade en ärendelogg i två hus` | **Change to what a claim says** (strength and scope: a completed, company-wide outcome becomes a trial in two buildings). The delivered scope is what the body supports; the input title was not. Reported, accurately, twice: as fixed finding 1 and again under *Påståenden*. The repair also introduces `ärendelogg`, a noun the rest of the text never uses — a new defect, which the reply itself names as standing finding 2. |
| 2 | `I september 2025 bestämde … att pröva en gemensam felanmälningslogg i två av husen.` | `I september 2025 beslutade … att på prov samla felanmälningarna från två av husen i en enda logg.` | **Repair of a defect visible in the text** — the input lead repeated seven words of the deck verbatim (*en gemensam felanmälningslogg i två av husen*). Reported as fixed finding 4. Claim identical: same date, same actor, same two buildings, same trial, same single log; `bestämde`→`beslutade` is a synonym. Nothing added that the text does not otherwise carry. |
| 3 | `## Leverantören konfigurerade, teamet bestämde kategorierna` | `## Underhållsteamet bestämde hur felanmälningarna skulle sorteras` | **Repair of a defect visible in the text** — the input subhead repeated the section's first sentence (*konfigurerade*) and said in the writer's words what the quotation says in the speaker's. Reported as fixed finding 3. No fact added: `sorteras` renders the `kategorierna` the section and the quotation both carry. But see §2: the new subhead still states the team owned the categories, which is what the quotation is there to deliver — the defect is reduced, not removed, and the reply does not say so. |
| 4 | `## Arbetsledaren skulle göra om testet med mer förberedelse` | `## Arbetsledarens omdöme kommer med villkor` | **Repair of a defect visible in the text** — the input subhead said the following quotation in advance in near-identical words. Reported as fixed finding 2, and the reply also reports, as standing finding 3, that the replacement now withholds the answer. No claim lost: *skulle göra om testet* and *mer förberedelse* both survive verbatim in the quotation below. |
| 5 | `— ` (em dash, U+2014) opening each of the three dialogue lines (ll. 20, 22, 34) | `– ` (en dash, U+2013) | **Mechanical / locale correction** — Swedish *talstreck*. Defensible, and the quoted wording is untouched. **Not reported anywhere in the reply**, neither among the fixed findings nor under *Påståenden* (which covers only claims). The one unaccounted-for change in the run. |

No other difference exists: frontmatter, deck, byline, all three quotations' wording, the metrics section in full, the closing paragraph and the link are byte-identical.

## 2. Bridges into quotations (every quotation in the input, in order)

**Q1** — `— Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort. Kategorierna var våra; Svale hjälpte oss att lägga in dem i loggen, säger Maya Lind, arbetsledare för underhållet.`

- **Bridge, input:** `Svale Systems konfigurerade loggen och utbildade sex medarbetare vid två tillfällen. Telefonanmälan behölls för de boende.` — **class (c)**: *utbildade sex medarbetare vid två tillfällen* and *Telefonanmälan behölls för de boende* are facts the quotation does not carry.
- **Bridge, delivered:** identical, word for word — **class (c)**, same words.
- **Changed?** No. Nothing lost, nothing supplied.
- **Speech tag:** `säger Maya Lind, arbetsledare för underhållet` — **class (b)** both sides, unchanged; the title identifies the speaker and no more.
- **Note on the heading above it:** `## Leverantören konfigurerade, teamet bestämde kategorierna` → `## Underhållsteamet bestämde hur felanmälningarna skulle sorteras`. It is not the bridge (a narrative sentence stands between it and the quotation), but it is pre-saying territory: the input heading was **(a)** for the quotation's second clause (*teamet bestämde kategorierna* ≈ *Kategorierna var våra*), and the delivered heading is still **(a)** for that same clause — *Underhållsteamet bestämde hur felanmälningarna skulle sorteras* is the quotation's point in the writer's voice. The reply claims this finding fixed; it is mitigated (the `konfigurerade` echo is gone, the *Leverantören/teamet* split is gone) but not eliminated, and the reply does not say so. No new fact enters: `sorteras` is the text's own `kategorierna`.

**Q2** — `— Vi lade mer tid på att enas om kategorierna än på att registrera de första anmälningarna. Den tiden skulle jag avsätta innan nästa hus drar i gång, säger hon.`

- **Bridge, input:** none — the quotation follows Q1 directly, with only the tag `säger hon`. **Class (b)**: bare attribution.
- **Bridge, delivered:** none; `säger hon` unchanged. **Class (b)**.
- **Changed?** No, apart from the opening dash glyph (difference 5). Nothing lost, nothing supplied.

**Q3** — `— Jag skulle välja att göra testet igen. Att ha en samlad bild av anmälningarna hjälper oss, men jag skulle lägga in en extra vecka för förberedelser, säger Maya Lind.`

- **Bridge, input:** the subhead standing immediately before it, `## Arbetsledaren skulle göra om testet med mer förberedelse` — **class (a)**: it delivers exactly what the quotation is there to deliver (would repeat the test; wants more preparation), in near-identical words, adding no understanding of its own. A reader who has read it meets the quotation as the subhead said again.
- **Bridge, delivered:** `## Arbetsledarens omdöme kommer med villkor` — **class (b)**: it names the subject (the supervisor's verdict) and the occasion of a reservation, without delivering the verdict or the reservation. It does not state that she would repeat the test, nor what the condition is.
- **Changed?** Yes. **The reply names the change** — as fixed finding 2, and again as standing finding 3, where it states plainly that the new subhead withholds the answer a subhead should give. **Nothing supplied**: *omdöme* and *villkor* are both carried by the quotation (*Jag skulle välja att göra testet igen … men*) and by the closing paragraph (*rekommenderar inte Svale till alla bostadsföretag*). **Nothing lost that the quotation does not carry**: everything the input bridge stated — the repeat, the extra preparation — stands verbatim in the quotation two lines below. The loss is of signposting, not of content, and the reply says so itself.
- **Speech tag:** `säger Maya Lind` — **class (b)** both sides, unchanged.

## 3. Quotations themselves

| Quotation | Wording returned | Reported | Meaning / stance / certainty / reservation / voice |
|---|---|---|---|
| Q1 (Lind, evening/morning shift, categories) | Unchanged, character for character, including the semicolon and the role in the tag. Only the preceding dialogue dash changed glyph. | Dash change unreported; wording needed no report. | Fully intact. *Kategorierna var våra* and the concession *Svale hjälpte oss* both survive with the speaker's emphasis. |
| Q2 (Lind, time spent agreeing categories) | Unchanged. Dash glyph only. | Same. | Fully intact, including the forward-looking modal *skulle … avsätta*. |
| Q3 (Lind, would repeat the test, with a week more prep) | Unchanged. Dash glyph only. | Same. | Fully intact: the endorsement, the hedge *men*, and the reservation *en extra vecka för förberedelser* all survive. The surrounding repair did not bleed into the quotation. |

No quotation was trimmed, merged, re-tagged, paraphrased or moved.

## 4. R1 — **Pass**

**Removals.** One claim was removed: `Elm Quay fick en gemensam bild av felanmälningarna`, which existed only in the title. The reply reports it, and reports it accurately — it says in so many words that the phrase survives nowhere in the text, that the title now says only that Elm Quay tested a log in two buildings, and that the title was the sole place the text asserted the company had gained a shared picture. This is a **legitimate removal**: the body says the test ran eight weeks in two of the buildings and has not been extended, so the input title overstated both completion and scope. No other sentence, clause, argument, figure or quotation was removed.

**Changed claims.** Only difference 1 changes what a claim says; it is the removal above and is reported accurately. Differences 2–4 are re-wordings that leave date, actor, scope, agent, modality and chronology as they were, and the reply's *Påståenden* paragraph correctly asserts that no body claim stands with altered reach, certainty, source, chronology, cause or sense.

**Preservation.** Every limiting sentence — no comparison with another vendor, the note's explicit refusal to attribute the difference to the software, cost/satisfaction/time-to-completion unmeasured, Lind not recommending Svale to all housing companies, emergencies and pre-ordered work excluded, the 31 reports, the 4 December 2025 date, the two-versus-three working days, the differing workloads — is untouched. Voice, tense and register are unchanged. Nothing was rewritten to taste: each of the four edits answers a defect a reader can see in the text alone (an overclaiming title, a subhead that says the quotation in advance, a subhead that repeats its own section's first sentence, a lead that repeats the deck verbatim), and the clean sections — the whole metrics section, the closing paragraph, the deck — were left alone.

**Unavailable-source discipline.** Correct on both sides. Standing finding 1 (the denominator for *två av husen*) is identified as irreparable from the text and explicitly left for material the Skill never had, rather than being filled with a guess; and no change is excused by material it never saw.

**Shortfalls, neither of them fatal.**
1. The em-dash → en-dash normalisation on all three dialogue lines is a real change to the delivered file and is reported nowhere. It is mechanical and locale-correct, and it does not touch wording, so it does not breach R1 — but the reply's account of what it changed is, strictly, incomplete.
2. The repaired first subhead still says in the writer's voice what Q1's second clause delivers in the speaker's (`Underhållsteamet bestämde hur felanmälningarna skulle sorteras` ≈ `Kategorierna var våra`). The reply lists that finding as fixed without noting the residue, while it did note the equivalent residue on the third subhead. An inconsistency in the account, not a loss in the text.

**Credit where it is due.** The reply is candid about the two defects its own single correction round created (the orphan term *ärendelogg*, the answer-withholding third subhead), attributes them to that round rather than to the input, explains why it did not spend a round repairing its own repair, and hands the two open wording decisions back. That is an accurate account of the state it left the text in.
