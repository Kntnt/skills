# Judgement a

Run directory: `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/397.scratch/j/6368823c8661`
Files read: `work/input.md`, `response.md`.

## 1. Differences

Frontmatter: none before, none after. Formatting: the bold standfirst, the italic report title, the H1 and the single body paragraph are all kept. No mechanical corrections.

1. **Headline.** Before: "Givarna räddar skolan från en katastrof" (39 characters). After: "Björkskolans givare visade under 20 grader i 14 lektionspass" (60 characters). Class: repair of a visible defect (an unsupported catastrophe claim). The new headline shortens the report's finding a little (**scope**): "14 av 120 lektionspass hade minst ett värde under" becomes "visade under 20 grader i 14 lektionspass". It leaves out "minst ett värde" and "av 120". The meaning is close enough that I do not count it as a loss. The headline grew by 21 characters. The run says nothing about headline length, and I do not know the limit, so I cannot tell whether the new headline still meets it.
2. **Standfirst.** Before: the same sentence twice, "Givarna registrerade temperaturer under 20 grader i sex klassrum." After: "Ett mätförsök på fyra veckor registrerade temperaturer under 20 grader i sex klassrum på Björkskolan. Här får du veta vad fastighetskontorets rapport visar, vad som inte mättes och vad en drifttekniker rekommenderar innan styrningen ändras." Class: repair of a visible defect (duplication, and an echo of the lead). One small **attribution** change: the six classrooms are placed "på Björkskolan", which the text implies through the report's title but never states. Every added fact is already in the body.
3. **Lead, opening sentence.** "Givarna registrerade temperaturer under 20 grader i sex klassrum." is moved from the start of the lead to follow the sentence on sensor placement. Class: repair of a visible defect (the lead opened like the standfirst). The claim is unchanged.
4. **"Katastrofen lurade bakom varje hörn."** Deleted. Class: a change to what a claim says (**certainty/meaning**). This is a legitimate removal of an unsupported claim.
5. **Report sentence split.** Before: "... vilket inte är en lagregel, och att försöket varade fyra veckor, medan två givare stod vid ytterväggar och fyra vid innerväggar, utan att ..." After: "... vilket inte är en lagregel. Enligt rapporten varade försöket fyra veckor. Två givare stod vid ytterväggar och fyra vid innerväggar, utan att ..." Class: repair of a visible defect (a run-on sentence, and a "medan" that implied a false relation). Two small **attribution** shifts. The four weeks are now explicitly the report's. The placement clause, which was loosely inside "anger att", now stands without attribution. The facts are unchanged.
6. **Operative temperature sentence.** Unchanged.
7. **Health claim.** Before: "..., men ändå är det helt säkert att givarna har gjort eleverna friskare, trots att ingen effekt på hälsan har undersökts." After: "..., och ingen effekt på hälsan har undersökts." Class: a change to what a claim says (**certainty/causality**). This is a legitimate removal. The limit that contradicts the claim is kept.
8. **Elin Rask sentence** (recommendation, November trial, undecided funding). Unchanged.
9. **"Det är viktigt att notera att detta är mycket viktigt för alla som tycker att temperatur är viktigt."** Deleted. Class: repair of a visible defect (empty filler). No claim is lost.
10. **"Kontakta oss för att rädda framtiden."** Replaced by "Läs rapportens siffror som lufttemperatur där givarna satt, inte som den temperatur eleverna upplevde." Class: repair of a visible defect (a sales line unrelated to the explanation), with new wording in the closing position (**meaning**: a reading instruction the text did not contain). The instruction follows from what the text states: the sensors measured only air, and operative temperature and pupils' experience are missing. It adds no new fact. It is a one-sentence replacement, not a written ending section.

## 2. The account

1. Reported: "Borttaget: Rubrikens påstående att givarna 'räddar skolan från en katastrof' ... rundan ersatte det med rapportens egen siffra." Accurate. The scope shortening and the length change are not mentioned.
2. Reported: "Ingressen upprepade samma mening två gånger och gör nu inte det. Den säger i stället vad artikeln handlar om och vad läsaren får ut av den." Accurate. The added "på Björkskolan" is not mentioned. It is minor.
3. Reported: "Inledningen börjar inte längre med samma mening som ingressen. Meningen om givarna står nu efter uppgiften om var givarna satt." Accurate.
4. Reported under "Påståenden som ändrats" as "Borttaget". Accurate.
5. Reported: "Ändrat: Att försöket varade fyra veckor tillskrivs nu uttryckligen rapporten", and "En lång mening har delats vid fogarna så att 'medan' inte längre antyder ett samband". Accurate. The placement clause losing its loose attribution is not called out separately, but the split that caused it is reported.
6. Not applicable (no change).
7. Reported under "Borttaget", with the kept limit quoted. Accurate.
8. Not applicable (no change).
9. Reported: "Den tomma frasen 'Det är viktigt att notera att …' är borta." Accurate.
10. Reported: "Uppmaningen 'Kontakta oss för att rädda framtiden.' saknade avsändare. Den har ersatts av en läsanvisning som bygger på det texten redan säger." Accurate about the change. The reason given ("saknade avsändare") differs from the corpus's (unrelated to the explanation).

The claim "Korrekturläsningen på slutet hittade inga mekaniska fel att rätta" is consistent: the diff contains no mechanical corrections.

## 3. The frozen expectation

**Detect**

- *Unsupported catastrophe/health certainty visible against explicit limits*: **met.** "Borttaget: 'Katastrofen lurade bakom varje hörn.' Påståendet att en katastrof hotade hade inget stöd i texten." and "Borttaget: 'men ändå är det helt säkert att givarna har gjort eleverna friskare'. Den samtidiga uppgiften att ingen hälsoeffekt har undersökts motsade påståendet."
- *Standfirst and lead that repeat each other and open on the same word*: **met.** "Ingressen upprepade samma mening två gånger" and "Inledningen börjar inte längre med samma mening som ingressen." The finding names the shared sentence, which contains the shared opening word. It does not name the word itself.
- *Late concept*: **partly met.** Finding 1, "Vems resonemang?", names the operative-temperature passage: "Texten har inte presenterat något resonemang ... ser inte varför det spelar roll att operativ temperatur saknas." It sees that the concept the argument rests on has no frame. It files this as a dangling reference that needs a missing fact. It does not say the concept arrives late, after the numbers it should frame, and it does not move it.
- *Unbroken paragraph mixing unlike jobs*: **met.** Finding 3: "Hela brödtexten ligger i ett enda stycke ... Stycket rymmer flera tankar: rapportens resultat, hur mätningen gjordes, vad som inte mättes, rekommendationen och nästa försök."
- *No byline, reported as missing and left unfilled*: **met.** Finding 2: "Byline saknas. ... En person behöver fylla i den." The returned text has no byline.
- *A 187-word lead*: **met.** Finding 3: "inledningen, som mäts till 158 ord. Normen är högst 80 ord." The input lead is 187 words. The reply measured its returned lead, which is 158 words after the deletions. The overlength is reported.
- *No subheading anywhere, so the body has neither a section nor an ending*: **met.** Finding 3: "Mellanrubriker och sektioner saknas, också den avslutande sektionen."
- *A closing sales line unrelated to the explanation*: **met, with a different reason.** "Uppmaningen 'Kontakta oss för att rädda framtiden.' saknade avsändare." The line is found and removed. The reply calls it senderless rather than unrelated.
- *The 39-character headline meets its limit and fails on truthfulness instead*: **met.** It is flagged only for truthfulness: "Rubrikens påstående ... Texten stödde det inte". There is no false length finding.

**Preserve**

- *The missing navigation is reported, not written*: **met.** "Därför har inga rubriker skrivits och stycket har inte delats. Det avgör en person." The returned text has no subheadings. The replacement closing sentence is one line in the lead paragraph, not an ending section.
- *No measured fact, exclusion or funding uncertainty is deleted*: **met.** Everything is kept: "14 av 120 lektionspass", "arbetsgräns på 20 grader, vilket inte är en lagregel", "fyra veckor", "Två givare stod vid ytterväggar och fyra vid innerväggar, utan att placeringens effekt jämfördes experimentellt", "Operativ temperatur saknas", "Det saknas mätningar av luftdrag och elevernas upplevelse och uppgifter om hur länge temperaturerna låg under gränsen", "ingen effekt på hälsan har undersökts", "fast finansieringen inte är beslutad", "sex klassrum" and "12 mars 2026".

**Rejection**

- *A supplied-source investigation is not a remedy*: **not committed.** No finding asks for the source or proposes verifying against it. Finding 1 ends "Frågan kan inte lösas utan en uppgift som texten saknar" and leaves the question with the author.

## 4. R1

**Pass.** Every visible defect the text shows is either repaired or reported. That covers the two unsupported certainties, the headline, the duplicated standfirst, the echo in the lead, the filler, the sales line, the missing byline and the missing sections. Every measured fact, exclusion and the funding uncertainty survive, as the "Borttaget" entries and the returned lead show: "... och ingen effekt på hälsan har undersökts. ... fast finansieringen inte är beslutad." All legitimate removals are reported accurately. The Skill wrote no navigation and no byline, and it verified nothing against an unavailable source. Two things are weaker. The late concept is only partly detected: it is reported as an unanchored "resonemanget", not as a concept arriving late. The new 60-character headline's length is not accounted for. Neither is a loss of voice, argument or claim.
