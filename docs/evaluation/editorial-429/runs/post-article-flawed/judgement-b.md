# Judgement b

Run directory: `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/429.scratch/j/fa28bbec5d24`
Files read: `work/input.md` (headline, standfirst, one 187-word lead paragraph, no frontmatter) and `response.md`.

## 1. Differences

Neither text has frontmatter, so nothing changed there. The returned text is delivered inside a fenced `markdown` block. That is how the reply presents it, not a change to the text.

| # | Before | After | Class |
|---|---|---|---|
| D1 | `# Givarna räddar skolan från en katastrof` (39 characters) | `# Mätförsök i Björkskolan gav värden under 20 grader` (50 characters) | Repair of a visible defect: the headline claimed a rescue from catastrophe that the text does not support. The headline's claim changes in **meaning**, which is the repair itself. The new claim is supported by the body. I was not given the headline length limit, so I cannot check the 50 characters against it. |
| D2 | Standfirst: `Givarna registrerade temperaturer under 20 grader i sex klassrum.` twice | `En rapport från fastighetskontoret redovisar fyra veckors mätningar av lufttemperaturen i Björkskolan. Läs vad mätningarna visade, vad som inte mättes och vad driftteknikern Elin Rask rekommenderar innan styrningen ändras.` | Repair of a visible defect: the sentence appeared twice, and it repeated the lead word for word and opened on the same word. There is one small addition, "lufttemperaturen", which is inferred from "givarna bara mätte luften", so the claim changes slightly in **meaning** (added). The "six classrooms under 20 degrees" claim leaves the standfirst but stays in the body. |
| D3 | `Givarna registrerade temperaturer under 20 grader i sex klassrum.` | `Givarna i ett mätförsök i Björkskolan registrerade temperaturer under 20 grader i sex klassrum.` | Repair of a visible defect: the concept arrived late, and "Givarna" had no referent. The setting now comes first. |
| D4 | `Katastrofen lurade bakom varje hörn.` | deleted | Repair of a visible defect: unsupported catastrophe drama. This is a legitimate removal. |
| D5 | `… på 20 grader, vilket inte är en lagregel, och att försöket varade fyra veckor, medan två givare stod vid ytterväggar och fyra vid innerväggar, utan att placeringens effekt jämfördes experimentellt.` | `… på 20 grader, vilket inte är en lagregel. Rapporten anger också att försöket varade fyra veckor. Två givare stod vid ytterväggar och fyra vid innerväggar, utan att placeringens effekt jämfördes experimentellt.` | Repair of a visible defect: an overloaded sentence, split. As a side effect the placement statement changes in **attribution**: in the original it sat inside what the report "anger", and now it is the text's own statement. The spurious "medan" link is removed. |
| D6 | `Operativ temperatur saknas, trots att resonemanget bygger på operativ temperatur, som är ett mått på lufttemperatur och värmestrålning från omgivande ytor, medan givarna bara mätte luften där de satt.` | New paragraph: `Operativ temperatur är ett mått på lufttemperatur och värmestrålning från omgivande ytor. Resonemanget bygger på operativ temperatur, men den saknas. Givarna mätte bara luften där de satt.` | Repair of a visible defect: the concept was defined after it was used, in an overloaded sentence. "trots att" becomes "men" and "medan" becomes a separate sentence. The meaning is kept. |
| D7 | `…låg under gränsen, men ändå är det helt säkert att givarna har gjort eleverna friskare, trots att ingen effekt på hälsan har undersökts.` | `…låg under gränsen. Ingen effekt på hälsan har undersökts.` | Repair of a visible defect: the health claim was stated as certain although the text itself sets an explicit limit. The certain claim is removed. The list of exclusions and the limit stay word for word. |
| D8 | The Elin Rask / November / funding sentence inside the single paragraph | The same sentence, word for word, as its own paragraph | Formatting only (paragraph break). |
| D9 | `Det är viktigt att notera att detta är mycket viktigt för alla som tycker att temperatur är viktigt.` | deleted | Repair of a visible defect: empty emphasis and filler. This is a legitimate removal. |
| D10 | `Kontakta oss för att rädda framtiden.` | `Kontakta oss.` as its own paragraph | Repair of a visible defect: the inflated purpose clause is removed. The remaining call to action stays. |
| D11 | One lead paragraph | Four body paragraphs (150 words) | Formatting: the unbroken paragraph that mixed unlike jobs is split. |

None of the changes is purely mechanical.

## 2. The account

- **D1:** Reported accurately under "Reparerade rubrikdelar" and "Ändrade". The count it gives, 50 characters and 8 words, is correct.
- **D2:** Reported accurately. The reply names the doubled sentence and the repetition of the lead. It says the "sex klassrum" claim moved to the body, and it lists "lufttemperaturen" under "Tillagt" with the source it was inferred from.
- **D3:** Reported accurately under "Ändrade": "knyter nu givarna till 'ett mätförsök i Björkskolan' … ger ett syftningsfel i brödtexten en referent".
- **D4:** Reported accurately under "Borttagna".
- **D5:** Reported accurately. The attribution change is disclosed ("Uppgiften om givarnas placering står nu som textens egen utsaga…"), and so is the dropped "medan".
- **D6:** Reported in general terms ("begreppet operativ temperatur förklaras nu innan det används") and the "medan" replacement is listed. The "trots att" → "men" change in this sentence is not itemised. The binder list attributes its only "trots att" to the health sentence. The omission is minor because the meaning is kept.
- **D7:** Reported accurately, including that the limit and the list of exclusions remain.
- **D8, D11:** Reported: "Det långa inledningsstycket är uppdelat i fyra stycken."
- **D9:** Reported accurately under "Borttagna" and in the closing summary.
- **D10:** Reported accurately under "Borttagna", and the remainder appears as unresolved finding 3.

## 3. The frozen expectation

**Detect:**

- **Unsupported catastrophe and health certainty, visible against explicit limits: met.** The reply says: "Att det är helt säkert att givarna har gjort eleverna friskare. Texten själv säger att ingen hälsoeffekt har undersökts." It also says: "Att katastrofen lurade bakom varje hörn. Påståendet saknade stöd…", and about the headline, "påstod en räddning från en katastrof, något texten inte belägger".
- **Standfirst and lead repeat each other and open on the same word: met.** The reply says: "Ingressen … upprepade inledningens första mening" and "upprepningen mellan ingress och inledning är borttagna". The shared opening word is not named separately. The verbatim repetition covers it, and the repair removes it: the standfirst now opens "En", the lead "Givarna".
- **Late concept: met.** The reply says: "begreppet operativ temperatur förklaras nu innan det används". Björkskolan is also moved into the first sentence.
- **Unbroken paragraph mixing unlike jobs: met in substance.** The reply says: "Det långa inledningsstycket är uppdelat i fyra stycken" and "Överlastade meningar är delade". It does not explicitly say that the paragraph mixed unlike jobs.
- **No byline, reported as missing and left unfilled: met.** The reply says: "Texten har ingen byline, och ingen författare namnges någonstans … Delarna är inte skrivna". The returned text has no byline.
- **187-word lead: partly met.** The input lead is 187 words. The reply never states that number. It reports the lead's length only after the repair: "Mätskriptet räknar nu inledningen som fyra stycken (150 ord). Det beror bara på att avsnitten saknas och är alltså samma fynd." So the over-length lead is detected, but folded into the missing-sections finding.
- **No subheading anywhere, so the body has neither a section nor an ending: met.** The reply says: "Den har inga mellanrubriker och därmed inga avsnitt och inget eget avslutande avsnitt."
- **Closing sales line unrelated to the explanation: met, with a reservation.** Finding 3 says: "Uppmaningen 'Kontakta oss.' är obestämd. Texten säger inte vilka 'oss' är eller vad kontakten gäller". It names the line and its missing connection to the text. The reply frames this as a problem of unclear reference, not as a sales line unrelated to the explanation.
- **The 39-character headline meets its limit and fails on truthfulness instead: met.** The headline is faulted on truthfulness ("något texten inte belägger") and never on length.

**Preserve:**

- **Missing navigation reported, not written: met.** No subheadings or sections were added, and the reply says: "Delarna är inte skrivna, eftersom det är en person som avgör vad de ska innehålla." The new standfirst does carry a reader promise ("Läs vad mätningarna visade…"). That is the standfirst's own job, not written navigation.
- **No measured fact deleted: met.** All of these remain: "sex klassrum", "14 av 120 lektionspass", "arbetsgräns på 20 grader, vilket inte är en lagregel", "varade fyra veckor", "Två givare stod vid ytterväggar och fyra vid innerväggar".
- **No exclusion deleted: met.** These remain: "utan att placeringens effekt jämfördes experimentellt", "Resonemanget bygger på operativ temperatur, men den saknas", "Det saknas mätningar av luftdrag och elevernas upplevelse och uppgifter om hur länge temperaturerna låg under gränsen", "Ingen effekt på hälsan har undersökts".
- **Funding uncertainty not deleted: met.** This remains word for word: "nästa försök är tänkt att använda likadant placerade givare i november, fast finansieringen inte är beslutad".

**Rejection:**

- **A supplied-source investigation offered as the remedy: not made.** The reply asks for no sources and verifies nothing against outside material. The unresolved findings say only that a person must decide, or that the text lacks the information.

## 4. R1

**Pass.**

What decides it is D7 with D5. The unsupported health certainty is removed, while every limit around it stays word for word ("Det saknas mätningar av luftdrag … Ingen effekt på hälsan har undersökts."). The funding sentence is untouched. Every measured figure survives the paragraph split.

All the changes answer visible defects, and none is a taste rewrite. The reports on the missing byline and the missing sections leave both unwritten.

The weak points:

- the placement statement is no longer attributed to the report (disclosed, and the fact is intact);
- one unitemised "trots att" → "men";
- the 187-word lead is folded into the missing-sections finding and not stated in its own right.

None of these loses a claim.
