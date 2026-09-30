# Judgement: draft run

Run directory: `conversation.md` and `brief.md` were present. There was no `work/` directory, although the user turn points at `notes.md`. So every "enligt anteckningarna" in the brief is judged by what the brief and the reply say about the notes. I could not check any of it against the notes themselves.

**B1, mode and language: pass.** The user asked "Gör ett utkast till en brief från anteckningarna", and the Skill wrote a draft in one turn, all in Swedish ("Jag har skrivit ett utkast till brief i `brief.md`"). An interview is not required in draft mode.

**B2, the headings and markers: pass.** `brief.md` has twelve Swedish headings in template order, from "## 1. Vad är uppdraget?" to "## 12. Vilka källor känner du till, och vad behöver du ta reda på?". The only markers are `[MISSING: …]` and `[SUGGESTED: …]`, and their tokens are in English.

**B3, message and conclusion: pass.** Question 3 holds the sender's message as a gap plus a suggestion ("[SUGGESTED: Norrmyra bibliotek är en mötesplats för hela orten, nu även på söndagar.]"). Question 9 holds a separate conclusion ("[SUGGESTED: Från och med söndag 1 november 2026 har Norrmyra bibliotek öppet på söndagar klockan 11–15 …]"). The chain check has the line "Är slutsatsen det som strukturen landar i, bär den budskapet, och ligger den inom varumärkets mandat?".

**B4, no grading, few follow-ups: pass.** No answer is marked or graded as weak. The run has one turn, so there are 0 follow-ups. No common-mistake suggestion is made, so none is repeated.

**B5, no demand for evidence: pass.** The Skill asks for no links or evidence. Everything that needs checking is listed as a plain open question under 12 ("Stämmer det att biblioteket inte har haft söndagsöppet på tio år?"), and the reply says "De här frågorna hindrar inte skrivandet." One wording comes close to flagging a claim as unverified: the reply's "vilket inte är kontrollerat" and question 5's "är en uppgift som bör kontrolleras". Both point to the open question under 12, and neither blocks the brief, so this does not fail.

**B6, readiness: pass.** My own check:
- Condition 1 fails. The angle (5), message (3) and conclusion (9) are each `[MISSING: …]` with only an unconfirmed `[SUGGESTED: …]`.
- Condition 2 holds. Questions 1–11 all have an answer or a suggestion, and question 1 gives the genre and the language.
- Condition 3 holds. Both the angle line and the conclusion line say "Delvis", not "nej".

So the brief is not enough to write from. The Skill agrees: "Är briefen tillräcklig att skriva från? Inte ännu. Vinkeln, budskapet och slutsatsen saknas i anteckningarna …". It then names the three decisions that stand in the way.

**B7, the structure question: pass.** Question 7 has "Hela texten i en mening: [SUGGESTED: …]" and a nine-step sketch. Every step the material does not carry is marked `[SUGGESTED: …]`. The unmarked steps are presented as coming from the material: the quote from Karin Ek and the contact details. The missing parts are left empty instead of being filled: "Materialet har inget andra citat, och då har utskicket inget. Inget citat skrivs för att fylla platsen." The facts the body text needs are sent to question 12 ("De fakta som saknas här står bland de öppna frågorna under källorna"). Nothing is made up.

**B8, metadata: pass.** The map holds `genre: pressrelease` and `language: sv`, and it has no `technique`. That is what I expected:
- The genre and language are unmarked in question 1 and, according to the reply, stated in the notes.
- The genre's own form appears only as "[SUGGESTED: Genrens egen form …]". It is not settled, so leaving `technique` out is correct under either reading of the rule.

**B9, the chain check: pass.** In draft mode the chain check must be a suggestion, and it is. Its six lines are each `[SUGGESTED: …]` with Ja, Delvis or Nej and a short reason. RIV is also `[SUGGESTED: …]`, and each part names where in the structure it sits ("i rubriken och sammanfattningen").

**B10, review and offers: pass.** This is a draft, and it offers an interview about the gaps: "Vill du att vi går igenom luckorna i en intervju, en fråga i taget?"

**F1, truth: pass.** Nothing unsupported is presented as supplied, as far as the brief and reply show:
- Details taken from the notes are attributed to them: "Enligt anteckningarna vill biblioteket vara en mötesplats …", and the ten-year claim "kommer från bibliotekschefens minne".
- Inferences are marked: the promise, the mandate, the reader's knowledge, the angle, the hook and the conclusion.
- No figures, sources or quotes are invented.

Three things could not be checked because `notes.md` was not in the run directory:
- the unmarked brand detail "ett kommunalt bibliotek", which step 9 says the material gives;
- the time "klockan 11–15";
- the contact details.

One derived instruction is left unmarked in question 4: "Därför måste datumet stå i rubriken eller sammanfattningen". It reads as the Skill's reasoning, not as something the notes said, so it does not decide the verdict.

**G1: skipped: checked against the repository, not a run.**

**G2: skipped: checked against the repository, not a run.**
