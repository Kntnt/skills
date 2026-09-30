# Judgement: brief run, draft mode

The run directory holds `conversation.md` and `brief.md` only. It has no `work/`, so `notes.md` could not be read. Checks of what counts as "supplied" rest on the brief's own attributions ("Enligt anteckningarna …", "Materialet anger …") and on the reply.

**B1, mode and language: pass.** The user asked "Gör ett utkast till en brief från anteckningarna" and the Skill delivered a draft in one turn. The reply and the brief are both in Swedish, the user's working language.

**B2, the headings and markers: pass.** The brief has twelve Swedish headings, from "## 1. Vad är uppdraget?" to "## 12. Vilka källor känner du till, och vad behöver du ta reda på?", in template order. The only markers are `[MISSING:` (9) and `[SUGGESTED:` (33), both with English tokens.

**B3, message and conclusion: pass.** Question 3 has a marked gap plus a suggestion ("Norrmyra bibliotek är en mötesplats för hela orten, nu även på söndagar"). Question 9 has a separate marked gap plus a suggestion ("Från och med söndag 1 november 2026 har Norrmyra bibliotek öppet …"). The chain check includes the line "Är slutsatsen det som strukturen landar i, bär den budskapet, och ligger den inom varumärkets mandat?"

**B4, no grading, few follow-ups: pass.** No answer is marked or graded as weak. The run is a single-turn draft, so it asks 0 follow-ups. The three decisions listed in the reply (angle, message, conclusion) are the readiness blockers the standard requires it to name, not repeated questions. No suggestion is made twice.

**B5, no demand for evidence: pass (borderline).** The Skill asks for no links or evidence and uses no unsubstantiated marker, and all ten open questions are listed under question 12. Two things come close to the line. Question 5 comments "Att det är första gången på tio år är en uppgift som bör kontrolleras", and the reply says "vilket inte är kontrollerat". Both refer the point to question 12 rather than grading the answer, which is why this still passes.

**B6, readiness: pass.** My own check:
- Condition 1 fails, because angle (5), message (3) and conclusion (9) each have only `[MISSING]` plus an unconfirmed `[SUGGESTED]`.
- Condition 2 holds, because questions 1–11 all have answers or suggestions, and question 1 gives both genre and language.
- Condition 3 holds, because the angle line and the conclusion line both answer "Delvis", with no *no*.

So the brief is not enough to write. The Skill agrees: "Inte ännu. Vinkeln, budskapet och slutsatsen saknas …". It names all three decisions and says the open questions do not block.

**B7, the structure question: pass.** Question 7 has "Hela texten i en mening" marked `[SUGGESTED]` and a nine-step sketch. Every step the material does not carry is `[SUGGESTED]`. The steps drawn from the material are left unmarked: the Karin Ek quote, the contact details, and "Materialet har inget andra citat … Inget citat skrivs för att fylla platsen." No fact is invented for a step. Missing facts, such as what visitors can do and whether the change is permanent, are sent to question 12, and the ten-year claim is conditioned: "om uppgiften bekräftas".

**B8, metadata: pass.** The map holds `genre: pressrelease` and `language: sv`, and no `technique`. That is what I expected. The genre's own form appears only as a `[SUGGESTED]` in question 7, and the rule omits `technique` whether the genre's form was chosen or nothing is settled. `language` comes from question 1 ("Svenska (`sv`)").

**B9, the chain check: pass.** It is a draft, so RIV and all six chain-check lines are written as `[SUGGESTED: …]`. Each line answers ja, nej or delvis with a short reason, for example "[SUGGESTED: Nej. Skissen håller tron på många barnfamiljer … utanför …]".

**B10, review and offers: pass.** The reply offers a gap interview: "Vill du att vi går igenom luckorna i en intervju, en fråga i taget?"

**F1, truth: pass (limited verification).** Inferences are consistently marked. Examples: the brand promise ("Enligt anteckningarna … [SUGGESTED: Det är varumärkets löfte.]"), the mandate, the tone, the reader's knowledge, and the standard description ("utifrån det materialet ger"). The brief invents no source, figure or brand detail. The genre limits it cites (70 characters, 60 words) are presented as genre rules. One small inference is left unmarked in question 4: "Därför måste datumet stå i rubriken eller sammanfattningen." It is a structural recommendation, not a fact or brand detail presented as supplied. The material itself was not available to check against.

**G1: skipped: checked against the repository, not a run.**

**G2: skipped: checked against the repository, not a run.**
