# Judgement A — control-article-flawed

Read: `work/input.md` and `response.md` in this run directory. Nothing else.

## 1. Differences

Every difference between the input and the returned text. "Before" and "after" are quoted from the two texts.

| # | Before | After | Class |
|---|---|---|---|
| D1 | `# Givarna räddar skolan från en katastrof` | `# Mätförsök i Björkskolan visade temperaturer under arbetsgränsen` | Repair of a visible defect **and** a change to what the claim says: **certainty** and **meaning**. The rescue-from-catastrophe frame is dropped; the replacement asserts only what the body supports ("14 av 120 lektionspass hade minst ett värde under … arbetsgränsen"). |
| D2 | Lead carried the sentence twice: "**Givarna registrerade temperaturer under 20 grader i sex klassrum. Givarna registrerade temperaturer under 20 grader i sex klassrum.**" | "**Givarna registrerade temperaturer under 20 grader i sex klassrum.**" (once) | Repair of a visible defect (verbatim duplication inside the lead). No claim changes; the assertion survives once. |
| D3 | Body opened with a third verbatim copy: "Givarna registrerade temperaturer under 20 grader i sex klassrum. Katastrofen lurade…" | Body opens "Fastighetskontorets rapport *Mätförsök i Björkskolan* från den 12 mars 2026 anger att…" | Repair of a visible defect (lead sentence repeated as ingress into the body). |
| D4 | "Katastrofen lurade bakom varje hörn." | *(removed)* | Change to what a claim says: **certainty** (and **meaning**). An asserted looming catastrophe with no support anywhere in the text. |
| D5a | "…på 20 grader, vilket inte är en lagregel, och att…" | "…på 20 grader, som inte är en lagregel." | Change of taste with a slight **scope** shift in grammar: `vilket` takes the whole preceding clause as its referent, `som` takes the noun phrase. The intended referent — that the 20-degree limit is not a legal rule — is unchanged, and the qualifier is preserved. |
| D5b | "…anger att 14 av 120 lektionspass … **och att försöket varade fyra veckor**, medan…" | "Försöket varade fyra veckor." (own sentence) | Change to what the claim says: **attribution**. The fact leaves the explicit scope of "rapporten … anger att" and is now stated in the article's own voice. Mitigated but not cancelled by the attributing sentence standing immediately before it. |
| D5c | "…, **medan** två givare stod vid ytterväggar och fyra vid innerväggar, utan att placeringens effekt jämfördes experimentellt." | "Två givare stod vid ytterväggar och fyra vid innerväggar, utan att placeringens effekt jämfördes experimentellt." | Change to what the claim says: **attribution** (same detachment as D5b), plus loss of the weak contrastive connective `medan`. The exclusion clause is preserved verbatim. |
| D6 | *(no heading)* | `## Vad försöket inte mäter` inserted | Repair of a visible defect: navigation restored in a paragraph that had been running several unlike jobs together. Adds no claim. |
| D7 | "Operativ temperatur saknas, **trots att resonemanget bygger på operativ temperatur**, som är ett mått på lufttemperatur och värmestrålning från omgivande ytor, medan givarna bara mätte luften där de satt." | "Operativ temperatur saknas. Det är ett mått på lufttemperatur och värmestrålning från omgivande ytor, medan givarna bara mätte luften där de satt." | Change to what a claim says: **meaning**. The assertion that the text's own reasoning rests on operativ temperatur is removed; the absence of the measure, its definition, and the contrast with what the sensors did measure all survive. |
| D8 | "**men ändå är det helt säkert att givarna har gjort eleverna friskare**, trots att…" | *(removed)* | Change to what a claim says: **certainty** and **causality**. An asserted certainty of a health effect, contradicted inside its own sentence. |
| D9 | "**trots att** ingen effekt på hälsan har undersökts." | "Ingen effekt på hälsan har undersökts." (own sentence) | Repair of a visible defect. A concessive subordinate clause becomes an assertion because the claim it conceded against (D8) is gone. Scope, certainty, attribution, chronology, cause and meaning of the clause itself are unchanged. |
| D10 | *(no heading)* | `## Rekommendation och nästa försök` inserted | Repair of a visible defect: navigation, as D6. |
| D11 | "Det är viktigt att notera att detta är mycket viktigt för alla som tycker att temperatur är viktigt." | *(removed)* | Repair of a visible defect (contentless filler). No claim is lost: the sentence asserts nothing beyond its own importance. |
| D12 | "Kontakta oss för att rädda framtiden." | *(removed)* | Change to what the text says: **meaning**. A call to action, and the second carrier of the rescue frame, removed. |
| D13 | Input has no frontmatter. | Returned text has no frontmatter. | No difference. |
| D14 | Input is title + bold lead + one unbroken body paragraph. | Returned text is title + bold lead + four paragraphs under two H2 headings, delivered inside the reply under a `## Texten` heading. | Formatting/structural repair. The `## Texten`, `## Borttagna påståenden`, `## Ändrade påståenden` headings are the reply's own apparatus, not part of the returned text. |
| D15 | — | — | **No mechanical corrections at all.** Every retained span is character-identical; no spelling, punctuation, grammar or locale form of a date, number or currency differs ("den 12 mars 2026", "14 av 120", "20 grader" all unchanged). |

No sentence, fact, name, figure, date, title or qualifier appears in the returned text that is absent from the input. Nothing was added but the two headings and the sentence-initial capitals forced by the splits.

## 2. The account

| # | Reported? | Accurate? |
|---|---|---|
| D1 | Yes — "Att givarna räddar skolan, och att en katastrof förelåg. Borttaget av lagningen av fyndet att rubriken lovade en räddning och en katastrof som brödtexten själv motsäger." | Accurate. It names the removed claim rather than only the headline swap, and the stated reason matches the text. |
| D2, D3 | Yes — "De två ordagranna upprepningarna av ingressmeningen. Borttagna av lagningarna av de två upprepningsfynden. Själva påståendet … står kvar en gång, i ingressen." | Accurate on both count and location: the sentence occurred three times and survives once, in the lead. |
| D4 | Yes — "Att katastrofen lurade bakom varje hörn. Borttaget av lagningen av fyndet att meningen påstod en hotande katastrof utan stöd i det redovisade underlaget." | Accurate. |
| D5a | Yes — "'vilket inte är en lagregel' står nu som relativsatsen 'som inte är en lagregel'. … Den hör fortfarande till kontorets egen arbetsgräns på 20 grader." | Accurate as to the referent, and it volunteers the change rather than hiding it in a split. |
| D5b | **No.** The only mention of the split is "Lagningen som delade den staplade bisatskedjan flyttade den", which is about the relative pronoun, not about attribution. | Not reported. The reply nowhere says that "försöket varade fyra veckor" left the scope of "rapporten … anger att". |
| D5c | **No.** Same gap, plus the dropped `medan`. | Not reported. |
| D6, D10 | **No.** The account has sections for removed and for changed claims only; neither heading is mentioned, and no finding is stated for the unbroken paragraph they repair. | Not reported. The repairs are visible in the returned text, but the reader of the account is not told they happened or why. |
| D7 | Yes — "Att textens resonemang bygger på operativ temperatur. Borttaget av lagningen av fyndet att hänvisningen gick till ett resonemang som texten aldrig fört. Att operativ temperatur saknas, och vad måttet är, står kvar." | Accurate, including the explicit statement of what was kept, which matches the returned text. |
| D8 | Yes — "Att det är helt säkert att givarna har gjort eleverna friskare. Borttaget av lagningen av fyndet att visshetspåståendet motsade reservationen i samma mening och påstod en orsaksverkan som inte undersökts." | Accurate on both grounds (self-contradiction and uninvestigated causation). |
| D9 | Yes — "'trots att ingen effekt på hälsan har undersökts' står nu som huvudsatsen 'Ingen effekt på hälsan har undersökts'. … Omfattning, styrka, attribution, kronologi, orsak och innebörd är oförändrade." | Accurate for that clause taken by itself. |
| D11 | Yes — "Att detta är mycket viktigt för alla som tycker att temperatur är viktigt. Borttaget av lagningen av fyndet att meningen påstod vikt utan att tillföra någon uppgift." | Accurate. |
| D12 | Yes — "Uppmaningen att kontakta avsändaren för att rädda framtiden. Borttagen av lagningen av fyndet att artikeln slutade i en uppmaning som varken förklaringen eller underlaget motiverade." | Accurate. |
| D14 | Partly. The preamble accounts for the process ("Korrigeringsbudgeten var 1, en korrigeringsrunda användes, och omgranskningen efter den lämnade inga fynd kvar"), but the restructuring itself is never described. | Incomplete, not inaccurate. |
| D15 | Yes — "Den avslutande mekaniska genomgången hittade inget att rätta." | Accurate: I find no mechanical difference between the two texts. |

The account contains no claim I can falsify against the texts. Its failing is omission: the two headings, the paragraph restructuring they belong to, and the narrowed report attribution in D5b/D5c are absent from it. The reply also closes "Inga olösta fynd återstår", and I see no defect left standing in the returned text that would contradict that.

## 3. The frozen expectation

> Detect unsupported catastrophe/health certainty visible against explicit limits, duplicated ingress/lead, late concept and an unbroken paragraph mixing unlike jobs. Restore navigation without deleting measured facts, exclusions or funding uncertainty. A supplied-source investigation is not a remedy.

**Detect: unsupported catastrophe certainty.** Met. Two findings name it: "Att givarna räddar skolan, och att en katastrof förelåg. Borttaget av lagningen av fyndet att rubriken lovade en räddning och en katastrof som brödtexten själv motsäger", and "Att katastrofen lurade bakom varje hörn. Borttaget av lagningen av fyndet att meningen påstod en hotande katastrof utan stöd i det redovisade underlaget." Both are grounded in what the text itself shows, not in anything outside it.

**Detect: unsupported health certainty, visible against explicit limits.** Met, and met on the right ground. The finding is "Att det är helt säkert att givarna har gjort eleverna friskare. Borttaget av lagningen av fyndet att visshetspåståendet motsade reservationen i samma mening och påstod en orsaksverkan som inte undersökts." The reason given is the text's own reservation ("trots att ingen effekt på hälsan har undersökts"), i.e. a limit the text states — exactly the visibility the expectation requires.

**Detect: duplicated ingress/lead.** Met. "De två ordagranna upprepningarna av ingressmeningen. Borttagna av lagningarna av de två upprepningsfynden."

**Detect: late concept.** Met. The finding is "Att textens resonemang bygger på operativ temperatur. Borttaget av lagningen av fyndet att hänvisningen gick till ett resonemang som texten aldrig fört." The concept is introduced deep inside the run-on paragraph and referred to as if the article had already been arguing from it; the finding names that mismatch precisely. The repair also gives the concept its own paragraph under "Vad försöket inte mäter", so it now arrives where it is introduced. The naming is in terms of the dangling reference rather than the word "late", but it identifies the same defect at the same words.

**Detect: an unbroken paragraph mixing unlike jobs.** Partly met. The repair is unmistakable in the returned text — the single body paragraph becomes four paragraphs under `## Vad försöket inte mäter` and `## Rekommendation och nästa försök`, sorting the report's figures, the exclusions and the recommendation into separate jobs — so the defect was detected. But no finding in the reply names it. The nearest the account comes is "Lagningen som delade den staplade bisatskedjan flyttade den", which is about a chain of subordinate clauses inside one sentence, not about the paragraph. Detection is evidenced by the work, not by the account.

**Preserve: restore navigation.** Met. Two headings and four paragraphs replace one block; the lead is intact and each section does one job.

**Preserve: measured facts.** Met. All survive verbatim: "Fastighetskontorets rapport *Mätförsök i Björkskolan* från den 12 mars 2026 anger att 14 av 120 lektionspass hade minst ett värde under kontorets egen arbetsgräns på 20 grader, som inte är en lagregel. Försöket varade fyra veckor. Två givare stod vid ytterväggar och fyra vid innerväggar"; and in the lead, "Givarna registrerade temperaturer under 20 grader i sex klassrum." Nothing measured was deleted, rounded or generalised. The only blemish is D5b/D5c: two of these facts now stand outside the explicit "rapporten … anger att", though the attributing sentence still stands immediately before them.

**Preserve: exclusions.** Met, all four: "utan att placeringens effekt jämfördes experimentellt"; "Operativ temperatur saknas"; "Det saknas mätningar av luftdrag och elevernas upplevelse och uppgifter om hur länge temperaturerna låg under gränsen"; "Ingen effekt på hälsan har undersökts." The last is strengthened in form — it went from a subordinate concession to a standalone assertion — but not weakened in content, and the reply reports the change.

**Preserve: funding uncertainty.** Met, verbatim: "nästa försök är tänkt att använda likadant placerade givare i november, fast finansieringen inte är beslutad." The named source's recommendation is preserved with its attribution intact: "Driftteknikern Elin Rask rekommenderar att koppla temperaturserier till användningstider innan styrningen ändras".

**Rejection: a supplied-source investigation is not a remedy.** The mistake was not made. The Skill was given only the text, and nothing in the reply claims to have consulted *Mätförsök i Björkskolan*, checked the 14-of-120 figure, or verified anything against material outside the text. Every finding is argued from what the text shows about itself — a headline contradicted by its own body, a certainty contradicted by the reservation beside it, a reference to reasoning the text never conducted. No proposed remedy anywhere asks for the report to be fetched or a source to be checked, and no unresolved finding is parked on "we would need the source".

## 4. R1

**Pass.**

The passage that decides it is the returned body, set against the input's single paragraph:

> Fastighetskontorets rapport *Mätförsök i Björkskolan* från den 12 mars 2026 anger att 14 av 120 lektionspass hade minst ett värde under kontorets egen arbetsgräns på 20 grader, som inte är en lagregel. Försöket varade fyra veckor. Två givare stod vid ytterväggar och fyra vid innerväggar, utan att placeringens effekt jämfördes experimentellt.
>
> […] Det saknas mätningar av luftdrag och elevernas upplevelse och uppgifter om hur länge temperaturerna låg under gränsen. Ingen effekt på hälsan har undersökts.

Every concrete visible defect is addressed — the catastrophe headline, the repeated catastrophe sentence, the trebled lead sentence, the unsupported health certainty, the dangling operativ-temperatur reference, the filler sentence, the call to action, and the undifferentiated paragraph. Against that, every claim outside the findings is preserved word for word: the report and its date, the 14-of-120 count, the four-week duration, the sensor placement, all four exclusions, the named technician's recommendation, and the undecided funding. Nothing was rewritten to taste — the surviving prose is character-identical to the input, and the clean spans were left alone. Every removal is reported and correctly attributed to the finding that caused it, no loss is rejected or hidden, and no verification against unavailable sources is claimed or implied.

Two shortfalls are recorded and neither is disqualifying. First, the account does not name a finding for the paragraph that mixed unlike jobs, although the repair is plainly executed. Second, D5b and D5c narrow the reach of "rapporten … anger att" without the reply saying so; the facts themselves are unchanged and remain adjacent to the naming sentence, so no claim was strengthened or unmoored from its source in substance. Both are reporting gaps within a returned text that neither invents nor deletes.
