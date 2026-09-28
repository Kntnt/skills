# Judgement a

Files read: `work/input.md` and `response.md`. The fenced text in `response.md` (lines 6–10) was diffed against `work/input.md`. They are byte-identical, including the trailing newline. Neither file has frontmatter.

## 1. Differences

None. The returned text is identical to the input: the headline, the bold standfirst, the one body paragraph and the Markdown formatting (`#`, `**…**`, `*Mätförsök i Björkskolan*`) all match. No mechanical correction, repair, change of taste or change to a claim was made.

## 2. The account

Nothing changed, so there is no difference to account for. The reply's statements about the returned text are accurate:

- "Texten levereras oförändrad." True.
- "Den levererade texten är byte för byte densamma som den som kom in. Inget påstående i den har tagits bort, ändrats eller lagts till." True. The diff shows no change.
- "Korrekturläsningen efteråt hittade inga mekaniska fel." This is consistent with the text: no mechanical change appears.
- The reply also describes a rejected correction round, which rewrote the headline and the first standfirst sentence and was then fully reverted. None of it is in the returned text, and the reply says so ("Inget från omgången finns kvar i den levererade texten"). Its reason for the rejection is plausible: the new headline "Mätförsök i Björkskolan fann värden under 20 grader" would have repeated the standfirst.

## 3. The frozen expectation

**Detect: unsupported catastrophe/health certainty, visible against explicit limits.** Met. Finding 11 says: "Här påstås ett säkert orsakssamband utan stöd, och förbehållet i samma mening motsäger det." Finding 6, on "Katastrofen lurade bakom varje hörn.", says: "ren dramatik utan stöd … motsägs den av textens egna förbehåll". Finding 1 says: "Texten beskriver varken en katastrof eller en räddning och säger tvärtom att ingen effekt på hälsan har undersökts."

**Detect: a standfirst and lead that repeat each other and open on the same word.** Met. Finding 5 says: "Brödtexten börjar med ingressens mening ordagrant, så texten börjar två gånger. Den står också i bestämd form, ”Givarna” …". A verbatim match covers the shared opening word "Givarna". Finding 2 separately flags that the standfirst repeats its own sentence: "Ingressen har samma mening två gånger, ordagrant."

**Detect: a late concept.** Met, though not in those words. Finding 5 says: "Rapporten och Björkskolan nämns först i tredje meningen. Den som hoppar över ingressen möter givare som ingen har presenterat." Finding 10 adds that "resonemanget … bygger på operativ temperatur" names a line of reasoning the text never introduced. Neither finding uses the word "late", but the late arrival of the subject that grounds the text is named and located.

**Detect: an unbroken paragraph mixing unlike jobs.** Met. Finding 7 says: "Brödtexten är ett enda stycke på 187 ord … Det rymmer flera tankar: resultatet och försökets upplägg, vad mätningen saknar, hälsopåståendet, rekommendationen och nästa försök samt avslutningen."

**Anatomy: no byline, reported as missing and left unfilled.** Met. Finding 4 says: "Byline saknas. Ingenstans namnges någon författare, så den lämnas åt en människa att fylla i." The returned text has no invented byline.

**Anatomy: a 187-word lead.** Partly met. The reply measures the right object and the right number ("ett enda stycke på 187 ord (uppmätt …)"). However, it judges that length against the paragraph norm ("Normen är högst 80 ord"), not against a limit for the lead. Elsewhere it treats the lead as just the opening sentence ("inledningen upprepar ingressen (fynd 5)"). So the length is detected, but it is never reported as a lead that exceeds its own limit.

**Anatomy: no subheading anywhere, so the body has neither a section nor an ending.** Met. Finding 8 says: "Mellanrubriker, avsnitt och ett eget avslutande avsnitt saknas. Anatomiskriptet mätte att både byline och avsnitt saknas (exit 1)." The closing paragraph adds: "avslutningen saknas (fynd 8 och 13)".

**Anatomy: a closing sales line unrelated to the explanation.** Met. Finding 13 says: "”Kontakta oss för att rädda framtiden.” … ”oss” identifieras ingenstans och uppmaningen följer inte av texten."

**The 39-character headline meets its limit and fails on truthfulness instead.** Met. Finding 1 faults the headline for making a claim the text does not carry, and adds: "Rubriken håller sig inom anatomins gränser (39 tecken, 6 ord)." I measured the headline at 39 characters.

**Preserve: the missing navigation is reported, not written.** Met. Finding 8 reports it and says "Delarna lämnas åt en människa att skriva." The returned text has no subheadings.

**Preserve: no measured fact, exclusion or funding uncertainty is deleted.** Met, because the text is unchanged. The returned text still has "14 av 120 lektionspass hade minst ett värde under kontorets egen arbetsgräns på 20 grader, vilket inte är en lagregel", "försöket varade fyra veckor", "två givare stod vid ytterväggar och fyra vid innerväggar, utan att placeringens effekt jämfördes experimentellt", "Det saknas mätningar av luftdrag och elevernas upplevelse och uppgifter om hur länge temperaturerna låg under gränsen", "trots att ingen effekt på hälsan har undersökts" and "fast finansieringen inte är beslutad". Finding 11 also says explicitly that the exclusions should stay: "Förbehållet och uppräkningen av vad som inte mättes är gränsdragningar som ska stå kvar."

**Rejection: a supplied-source investigation is not a remedy.** Not violated. The reply proposes no investigation of the report or any other source, and verifies nothing against unavailable material. Where facts are missing (a byline, a sender, a contact route), it leaves them to a human.

## 4. R1

**Pass.**

The deciding passage is "Den levererade texten är byte för byte densamma som den som kom in. Inget påstående i den har tagits bort, ändrats eller lagts till." Together with the thirteen located findings, this meets the criterion. Every visible defect in the frozen expectation is named at its passage, except the lead-length framing, which is only partly met. No claim, quotation, exclusion or voice was lost. Nothing was checked against unavailable sources. The account is accurate. The corpus scores detection and preservation apart from the quality of the final text, so leaving the findings unresolved after the one rejected round does not fail R1.

One weakness that does not change the verdict: several defects needed no outside facts and could have been fixed in the one round. These are the doubled standfirst sentence, the filler sentence "Det är viktigt att notera …" and the "helt säkert" certainty, which the text's own limits contradict. The Skill discarded the whole round because of one new defect in the headline and standfirst, so none of them was repaired.
