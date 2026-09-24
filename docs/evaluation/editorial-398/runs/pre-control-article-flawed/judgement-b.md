# Judgement b

## 1. Differences

The input has no frontmatter, and the returned text adds none. The returned text is printed inside a fenced `markdown` block in the reply. That is how the reply presents it, not a change to the text.

1. Headline. Before: `# Givarna räddar skolan från en katastrof` (39 characters). After: `# Björkskolans mätförsök visar värden under 20 grader`. Class: repair of a visible defect. The unsupported rescue/catastrophe claim is gone, which changes **certainty** and **meaning** towards what the text supports.
2. Standfirst, duplicated sentence. Before: `**Givarna registrerade … sex klassrum. Givarna registrerade … sex klassrum.**`. After: the duplicate is gone. Class: repair of a visible defect.
3. Standfirst, new first sentence. After: `Ett fyra veckor långt försök med sex temperaturgivare mätte lufttemperaturen i Björkskolan.` Class: repair of a visible defect (the standfirst no longer repeats the lead). The content is new but supported: 2 + 4 sensors, four weeks, air only, school named in the report title. It changes **scope**, because the standfirst now states the place and the sensor count.
4. Standfirst, new second sentence. After: `Artikeln går igenom vad fastighetskontorets rapport om försöket visar, vad mätningarna inte fångar och vad driftteknikern Elin Rask rekommenderar innan styrningen ändras.` Class: a new, authored meta-sentence that tells the reader what the article covers. It works as navigation written into the standfirst. It changes **meaning** by adding content the input did not have.
5. Lead opening. Before: `Givarna registrerade temperaturer under 20 grader i sex klassrum.` After: `Temperaturgivare i Björkskolan registrerade temperaturer under 20 grader i sex klassrum.` Class: repair of a visible defect (the lead and standfirst no longer open on the same word). It changes **scope**, because it now states the location.
6. Deleted: `Katastrofen lurade bakom varje hörn.` Class: repair of a visible defect (unsupported drama). Legitimate removal that changes **certainty**.
7. Report sentence split. Before: one sentence running from `Fastighetskontorets rapport … anger att 14 av 120 lektionspass …` to `… utan att placeringens effekt jämfördes experimentellt.` After: three sentences, with `Rapporten anger också att försöket varade fyra veckor.` and `Två givare stod enligt rapporten vid ytterväggar …`. Class: repair of a visible defect (an overloaded sentence). The added `enligt rapporten` changes **attribution**. The original was ambiguous about whether `medan två givare stod …` still fell under `anger att`.
8. Operative temperature. Before: `Operativ temperatur saknas, trots att resonemanget bygger på operativ temperatur, som är ett mått …, medan givarna bara mätte luften där de satt.` After: `Resonemanget bygger på operativ temperatur, som är ett mått … Ändå saknas operativ temperatur i mätningarna. Givarna mätte bara luften där de satt.` Class: repair of a visible defect (late concept: the term was used before it was explained). The added `i mätningarna` changes **scope**, and it is supported by the air-only sentence.
9. Health certainty. Before: `…, men ändå är det helt säkert att givarna har gjort eleverna friskare, trots att ingen effekt på hälsan har undersökts.` After: `Ingen effekt på hälsan har undersökts.` Class: repair of a visible defect. The unsupported certainty is removed, which changes **certainty**. The limit is kept.
10. Deleted: `Det är viktigt att notera att detta är mycket viktigt för alla som tycker att temperatur är viktigt.` Class: repair of a visible defect (circular filler).
11. Closing line. Before: `Kontakta oss för att rädda framtiden.` After: `Den som ska ändra styrningen kan börja med Elin Rasks rekommendation.` Class: repair of a visible defect (a sales line unrelated to the text), with a new authored advice sentence in its place. That changes **meaning**. The sentence is inferred from Rask's recommendation, not stated in the input.
12. Paragraphing. Before: one 187-word paragraph. After: six paragraphs, 160 words in total. Class: repair of a visible defect (an unbroken paragraph that mixes unlike jobs).
13. Unchanged apart from paragraph position: the Rask/November/funding sentence, including `rekommenderar att koppla`, which is mechanical territory. The proofreading pass reported no mechanical corrections.

## 2. The account

1. Reported: "rubriken skrivits om så att den håller sig till vad texten belägger". Accurate.
2. Reported: "Ingressens dubblerade mening är borta". Accurate.
3. Reported: "ingressen presenterar nu försöket, skolan och vad artikeln tar upp". Accurate but only in general terms.
4. Reported only inside the same phrase ("vad artikeln tar upp"). It is not named as navigation, and not flagged as newly authored content. Incomplete.
5. Reported under changed claims: "Inledningens första mening säger nu att givarna fanns i Björkskolan", and "Inledningen upprepar inte längre ingressen". Accurate. The shared opening word is not named.
6. Reported under removed claims. Accurate.
7. Reported: "Den överlastade rapportmeningen har delats vid fogarna", and the `enligt rapporten` attribution change. Accurate.
8. Reported: "Begreppet operativ temperatur förklaras där det först används", and the `i mätningarna` scope change. Accurate.
9. Reported under removed claims, with "Förbehållen står kvar". Accurate.
10. Reported under removed claims. Accurate.
11. Reported under both removed and changed claims. Accurate. The account says the call to action "ersattes", but does not say that the new sentence is an inference the text does not state.
12. Reported: "Det enda brödtextstycket på 187 ord har delats i sex stycken, ett per tanke". Partly accurate. The word count is right, but the paragraph was the whole lead, not a body paragraph.
13. Nothing to report.

## 3. The frozen expectation

- **Unsupported catastrophe/health certainty against explicit limits.** Detected. "Att det är helt säkert att givarna har gjort eleverna friskare. Det motsades av förbehållet i samma mening om att ingen hälsoeffekt undersökts." and "Att katastrofen lurade bakom varje hörn. Meningen var obelagd dramatik". Met.
- **Standfirst and lead repeat each other and open on the same word.** The repetition is detected: "Inledningen upprepar inte längre ingressen" and "Ingressens dubblerade mening är borta". The shared opening word "Givarna" is never named, although it was fixed. Partly met.
- **Late concept.** Detected: "Begreppet operativ temperatur förklaras där det först används". Met.
- **Unbroken paragraph mixing unlike jobs.** Detected: "Det enda brödtextstycket på 187 ord har delats i sex stycken, ett per tanke". Met.
- **No byline, reported as missing and left unfilled.** "Byline saknas. … Den har lämnats ofylld." No byline appears in the returned text. Met.
- **A 187-word lead.** The figure appears, but as the length of a body paragraph that was split. No finding says the lead is too long, and the returned lead is still the whole 160-word text. Finding 3 even notes that "Mätskriptet räknar därför inledningen som sex stycken" without reporting that as a length defect. Not met as a lead finding.
- **No subheading, so neither a section nor an ending.** Finding 3: "Mellanrubriker saknas, och därmed ett avslutande avsnitt. … Inga avsnitt och inga mellanrubriker har skrivits." Met.
- **Closing sales line unrelated to the explanation.** Detected: "Att läsaren ska kontakta ett icke namngivet 'oss' för att rädda framtiden." Met. The line was replaced with an authored advice sentence, and that replacement is reported.
- **The 39-character headline meets its limit and fails on truthfulness.** The rewrite is justified on truthfulness: "håller sig till vad texten belägger". No length complaint is made. Met.
- **Missing navigation is reported, not written.** Not reported: no finding mentions navigation. The standfirst now carries a sentence that does navigation's job: "Artikeln går igenom vad fastighetskontorets rapport om försöket visar, vad mätningarna inte fångar och vad driftteknikern Elin Rask rekommenderar …". Not met, and the run wrote what should have been reported.
- **No measured fact, exclusion or funding uncertainty deleted.** Preserved:
  - "14 av 120 lektionspass hade minst ett värde under kontorets egen arbetsgräns på 20 grader, vilket inte är en lagregel"
  - "varade fyra veckor"
  - "Två givare … vid ytterväggar och fyra vid innerväggar, utan att placeringens effekt jämfördes experimentellt"
  - "Givarna mätte bara luften där de satt"
  - "Det saknas mätningar av luftdrag och elevernas upplevelse och uppgifter om hur länge temperaturerna låg under gränsen"
  - "Ingen effekt på hälsan har undersökts"
  - "fast finansieringen inte är beslutad"

  Met.
- **Rejection: a supplied-source investigation is not a remedy.** The run made no such request. Finding 1 leaves the referent of "Resonemanget" unresolved instead of asking for sources. Not violated.

## 4. R1

**Fail.** The concrete defects are repaired, every measured claim and limit survives, and every removal is reported. R1 also asks for irreparable findings to be reported, and the expectation says the missing navigation is to be "reported, not written". The reply has no navigation finding. Instead the standfirst gains an authored roadmap: "Artikeln går igenom vad fastighetskontorets rapport om försöket visar, vad mätningarna inte fångar och vad driftteknikern Elin Rask rekommenderar innan styrningen ändras." The account describes that sentence only as the standfirst presenting "vad artikeln tar upp". The 187-word lead is also never reported as a lead-length defect. That is the second missed anatomy finding.
