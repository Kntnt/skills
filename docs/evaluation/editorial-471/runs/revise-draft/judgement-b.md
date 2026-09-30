# Judgement: brief run, draft mode

**B1, mode and language: pass.** The user asked for a draft ("Gör ett utkast till en brief från anteckningarna"), and the Skill wrote one from `notes.md` without an interview. The reply and `brief.md` are both in Swedish.

**B2, the headings and markers: pass.** `brief.md` has headings "## 1. Vad är uppdraget?" through "## 12. Vilka källor känner du till, och vad behöver du ta reda på?" in template order and in Swedish. The only markers are `[MISSING:` (9) and `[SUGGESTED:` (33), and both tokens stay in English.

**B3, message and conclusion: pass.** Question 3 has a marked gap and a separate suggestion ("[SUGGESTED: Norrmyra bibliotek är en mötesplats för hela orten, nu även på söndagar.]"). Question 9 has its own gap and conclusion ("[SUGGESTED: Från och med söndag 1 november 2026 har Norrmyra bibliotek öppet på söndagar …]"). The chain check includes the line "Är slutsatsen det som strukturen landar i, bär den budskapet, och ligger den inom varumärkets mandat?"

**B4, no grading, few follow-ups: pass.** No answer is marked or graded as weak. This was a draft in one turn, so there were 0 follow-ups. No suggestion is repeated as a question. The advice that the genre argues against an arc appears once in the brief (question 7) and is restated once in the reply's summary, but it is never asked.

**B5, no demand for evidence: pass.** The Skill asks for no links or evidence. The ten-year figure, which the notes say comes from memory, is listed as an open question under 12 ("Stämmer det att biblioteket inte har haft söndagsöppet på tio år?"). Question 5 has only a plain-text pointer to that question and no marker. Edge case: this pointer and the phrase "om uppgiften bekräftas" in sketch step 2 come close to flagging a claim. But they only route it to question 12 and add no unsubstantiated marker.

**B6, readiness: pass.** My application of the three conditions:
- Condition 1 fails. Angle (5), message (3) and conclusion (9) are each `[MISSING]` plus an unconfirmed `[SUGGESTED]`.
- Condition 2 holds. Question 1 has genre and language, and questions 2–11 each have an answer or a suggestion.
- Condition 3 holds. The angle line and the conclusion line both answer "Delvis", not "nej".

So the brief is not enough to write from. The Skill says "Inte ännu" and names the same three blockers as questions. It lists the other gaps separately without calling them blockers, and says the open research questions "hindrar inte skrivandet". The statement agrees with the conditions.

**B7, the structure question: pass.** Question 7 has "Hela texten i en mening: [SUGGESTED: …]" and a nine-step sketch. Every step the material does not carry is `[SUGGESTED]`. The unmarked steps carry only what the notes supply: the Karin Ek quote and the contact details. They also state absences, such as "Materialet har inget andra citat … Inget citat skrivs för att fylla platsen." Missing facts (what visitors can do, permanent or trial) become open questions under 12 and are not invented.

**B8, metadata: pass.** The map holds `genre: pressrelease` and `language: sv`, and no technique. I expected exactly that: the notes settle the genre and the language ("ett pressmeddelande på svenska"). The genre's own form is only suggested, so leaving out `technique` is correct.

**B9, the chain check: pass.** All six chain-check lines and all three RIV items are written as `[SUGGESTED: …]`, each with yes, no or partly and a reason. The standard asks for this in a draft.

**B10, review and offers: pass.** The reply ends with the draft's offer of a gap interview: "Vill du att vi går igenom luckorna i en intervju, en fråga i taget?"

**F1, truth: pass.** Everything presented as supplied comes from the notes: the kommunalt bibliotek, the 11–15 hours, the start date, the quote and the contact. Brand promise, mandate, tone, reader profile and the other inferences are `[SUGGESTED]`. Minor: two derived sentences in question 4 are not marked. They are "Därför måste datumet stå i rubriken eller sammanfattningen" and the reader's role ("Den som ska avgöra om det finns en nyhet här …"). Both are editorial inferences, not facts, sources or brand details, so they do not fail F1. I also confirmed that 1 November 2026 is a Sunday.

**G1:** skipped: checked against the repository, not a run.

**G2:** skipped: checked against the repository, not a run.
