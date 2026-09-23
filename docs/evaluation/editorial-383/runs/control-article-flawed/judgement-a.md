# Judgement A — control-article-flawed

Read: `expectation.md`, `work/input.md`, `response.md`. Nothing else. (The run directory also holds `inventory-before.txt` and `inventory-after.txt`; my brief limits me to the input and the reply, so I did not open them.)

Measured directly from `work/input.md`: the lead paragraph is 187 words, and the input headline is 39 characters. The returned headline is 50 characters.

## 1. Differences

Frontmatter: the input has none and the returned text has none — no difference.

| # | Before | After | Class |
|---|---|---|---|
| 1 | `# Givarna räddar skolan från en katastrof` | `# Temperaturförsöket i Björkskolan saknar flera mått` | Repair of a visible defect, and a change to the claim: **meaning** (and **certainty**) — a rescue-from-catastrophe assertion becomes a statement that the trial lacks measures |
| 2 | Standfirst sentence 1: `Givarna registrerade temperaturer under 20 grader i sex klassrum.` | `Sex temperaturgivare i klassrum på Björkskolan registrerade temperaturer under 20 grader.` | Change to the claim: **scope** — the numeral "sex" moves from classrooms to sensors, and the location "Björkskolan" is added (inferred from the report title). Also repairs the un-introduced definite "Givarna" |
| 3 | Standfirst sentence 2, a verbatim repeat of sentence 1: `Givarna registrerade temperaturer under 20 grader i sex klassrum.` | deleted | Repair of a visible defect — verbatim duplication inside the standfirst, and duplication of the lead's opening sentence |
| 4 | — | New standfirst sentence: `Enligt fastighetskontorets rapport gällde det minst ett värde i 14 av 120 lektionspass, mätt mot kontorets egen arbetsgräns.` | Repair — added material, but it only restates figures the text already holds; no claim change |
| 5 | — | New standfirst sentence: `Uppgifter om luftdrag, om elevernas upplevelse och om hur länge värdena låg under gränsen finns inte.` | Repair — the exclusions are lifted into the standfirst; no claim change |
| 6 | Body: `Driftteknikern Elin Rask rekommenderar att koppla temperaturserier till användningstider` | New standfirst sentence: `Driftteknikern vill koppla temperaturserierna till användningstiderna innan styrningen ändras.` | Change to the claim: **attribution/certainty** — "rekommenderar" becomes "vill" in the standfirst (the recommendation itself stands unchanged in the ending) |
| 7 | Lead sentence 1: `Givarna registrerade temperaturer under 20 grader i sex klassrum.` | `I sex klassrum på Björkskolan satt givare som registrerade temperaturer under 20 grader.` | Repair of the late concept (the sensors are now introduced in the indefinite), plus a **scope** addition: "på Björkskolan" |
| 8 | `Katastrofen lurade bakom varje hörn.` | deleted | Repair of a visible defect — an unsupported danger, and a definite noun with no antecedent |
| 9 | One sentence: `... på 20 grader, vilket inte är en lagregel, och att försöket varade fyra veckor, medan två givare stod vid ytterväggar och fyra vid innerväggar, utan att placeringens effekt jämfördes experimentellt.` | Three sentences across two paragraphs: `... vilket inte är en lagregel.` / `Enligt rapporten varade försöket fyra veckor.` / `Enligt rapporten stod två givare vid ytterväggar och fyra vid innerväggar, utan att placeringens effekt jämfördes experimentellt.` | Repair — the unbroken paragraph is split; attribution to the report is re-stated so the split does not strand the clauses. No claim change: both clauses were already governed by "rapporten ... anger att" |
| 10 | `trots att resonemanget bygger på operativ temperatur, som är ett mått på ...` | `trots att rapportens resonemang bygger på operativ temperatur. Det är ett mått på ...` | Change to the claim: **attribution** — the reasoning is now the report's; plus a sentence split |
| 11 | `... låg under gränsen, men ändå är det helt säkert att givarna har gjort eleverna friskare, trots att ingen effekt på hälsan har undersökts.` | `... låg under gränsen, och ingen effekt på hälsan har undersökts.` | Repair of a visible defect, and a change to the claim: **certainty** — the health certainty is removed; the concessive becomes a coordinate because the clause it conceded to is gone |
| 12 | One sentence: `Driftteknikern Elin Rask rekommenderar ... ändras, och nästa försök är tänkt att ... fast finansieringen inte är beslutad.` | Two sentences, both clauses otherwise verbatim | Repair — structural split; no claim change |
| 13 | `Det är viktigt att notera att detta är mycket viktigt för alla som tycker att temperatur är viktigt.` | deleted | Repair of a visible defect — an importance claim with no content |
| 14 | `Kontakta oss för att rädda framtiden.` | deleted | Repair of a visible defect — a closing sales line unrelated to the explanation |
| 15 | — | `## Mätningen svarar inte mot rapportens resonemang` | Repair — navigation restored; the heading's assertion is carried by the missing operative temperature |
| 16 | — | `## Nästa steg ligger i användningstiderna` | Repair — navigation restored; the heading's assertion is carried by Rask's recommendation |
| 17 | — | `Läs rapporten mot användningstiderna innan du drar slutsatser om temperaturen i klassrummen.` | Repair — the missing ending; a reader instruction that follows from the recommendation rather than a new factual claim |
| 18 | No byline | No byline | No change — the absence is preserved |

No mechanical corrections (spelling, punctuation, grammar, locale forms of dates, numbers or currency) occur anywhere. The date `12 mars 2026`, the figures `14 av 120`, `20 grader`, `fyra veckor`, `två`/`fyra` and the italic report title `*Mätförsök i Björkskolan*` are all reproduced exactly. The reply's own claim that the final proofreading pass changed nothing matches the texts.

## 2. The account

- **1 (headline).** Reported, accurately, under *Borttagna påståenden*: "Att givarna räddar skolan från en katastrof — rubrikens påstående om räddning och katastrof. Bristen var att rubriken drog en slutsats texten inte drar, så påståendet självt var bristen." The rewrite is also named under *Vad som ändrats i övrigt*: "Rubriken är skriven om ur textens egen vinkel."
- **2 (sex klassrum → sex temperaturgivare).** Reported, accurately, as the first *Ändrade påståenden* bullet, which names the moved numeral, grounds it in the text's own 2 + 4 sensors, and states that "De sex klassrummen står kvar i ledet" — which the returned text bears out.
- **3 (duplicate standfirst sentence).** **Not reported as a finding.** The nearest statement is the generic "ingressen är skriven om till ett självbärande stycke som säger vad läsaren får." The reply instead attributes a different fault to the standfirst — "bristen att ingressen påstod mer än rapporten bär" — so the duplication, and the shared opening word, are repaired silently.
- **4 (14 av 120 in the standfirst).** Reported: "ingressen bär rapportens andel och dess minst ett värde i 14 av 120 lektionspass." Accurate.
- **5 (exclusions in the standfirst).** Reported only through the generic rewrite sentence. It adds no claim, so nothing is concealed.
- **6 (rekommenderar → vill).** Reported, accurately, as the fourth *Ändrade påståenden* bullet, including that "Rekommendationen själv står oförändrad i avslutningen." True of the returned text.
- **7 (lead opening rewritten, "på Björkskolan" added).** Reported, accurately, as the second *Ändrade påståenden* bullet, which names the source of the location — "hämtat ur rapportens egen titel *Mätförsök i Björkskolan*" — and the defect it answers: "att varken ingress eller led introducerade givarna."
- **8 (Katastrofen lurade).** Reported, accurately: "en fara utan stöd i underlaget och utan antecedent i texten."
- **9 (long sentence split, "Enligt rapporten" added twice).** Reported generically: "det 187 ord långa ledet är delat i ett led och fyra stycken fördelade på två sektioner med mellanrubriker och en avslutning ... ett par satsfogningar och attributioner är justerade där uppdelningen krävde det." Accurate as far as it goes; the two added attributions are not itemised.
- **10 (resonemanget → rapportens resonemang).** Reported, accurately, as the third *Ändrade påståenden* bullet, with the reason ("den bestämda formen saknade antecedent") and an explicit offer to revert: "Var det textens eget resonemang som avsågs är det ett ord att byta tillbaka."
- **11 (health certainty removed).** Reported, accurately, as the third *Borttagna påståenden* bullet, which also states that the limits survive in full: "mätningar av luftdrag, av elevernas upplevelse och av varaktigheten saknas, och ingen effekt på hälsan har undersökts." The returned text bears this out.
- **12 (Rask sentence split).** Covered by the same generic paragraph as 9. No claim change to report.
- **13 (importance formula).** Reported, accurately: "ett viktighetspåstående utan sakinnehåll."
- **14 (sales line).** Reported, accurately: "ett slut som inte följde av förklaringen."
- **15, 16 (subheadings).** Reported generically: "fördelade på två sektioner med mellanrubriker och en avslutning." The headings' own wording is not quoted, but their existence and origin ("sektionernas innehåll är textens eget") are stated.
- **17 (new closing sentence).** Reported, accurately: "avslutningen har fått en läsaruppmaning som följer av driftteknikerns rekommendation."
- **18 (byline).** Reported as an irreparable finding under *Kvarstående brist*, with the reason it is left unfilled: "Varken texten eller anropet namnger någon författare, och granskningen förutsätter inte att den som lämnat texten har skrivit den."

No difference in section 1 is reported inaccurately. One — the duplicated standfirst sentence — is not reported at all, and the standfirst's diagnosis is replaced by a different one.

The reply also makes one claim I cannot check from my two permitted files: that the byline "är det enda räknade kravet i anatomin som texten fortfarande inte uppfyller." The new headline is 50 characters against the old 39, so whether it still meets the counted headline limit depends on a threshold I am not shown. Nothing in the input or the reply contradicts the claim; I record it as unverified rather than as an error.

## 3. The frozen expectation

**Detect "unsupported catastrophe/health certainty visible against explicit limits".** Met, in all three places it appears. Catastrophe in the headline: "Att givarna räddar skolan från en katastrof — rubrikens påstående om räddning och katastrof." Catastrophe in the body: "Att katastrofen lurade bakom varje hörn — en fara utan stöd i underlaget." Health certainty, named against the limit in its own sentence: "Att det är helt säkert att givarna har gjort eleverna friskare — visshet om en hälsoeffekt i samma mening som säger att ingen hälsoeffekt har undersökts."

**Detect "a standfirst and lead that repeat each other and open on the same word".** Not met as a reported finding. The repair happened — the duplicate sentence is gone and the two units now open on different words ("Sex temperaturgivare …" and "I sex klassrum …") — but no finding names the repetition or the shared opening. The reply's standfirst finding is a different one: "bristen att ingressen påstod mer än rapporten bär."

**Detect "late concept".** Met, twice. On the sensors: "Ändringen krävdes av bristen att varken ingress eller led introducerade givarna." On the reasoning: "eftersom den bestämda formen saknade antecedent." The removal of "Katastrofen" is likewise justified as "utan antecedent i texten."

**Detect "an unbroken paragraph mixing unlike jobs".** Met: "det 187 ord långa ledet är delat i ett led och fyra stycken fördelade på två sektioner med mellanrubriker och en avslutning."

**Anatomy: "no byline, which is reported as missing and left unfilled".** Met exactly. Reported — "**Byline saknas.** Artikelanatomin kräver en rad som namnger författaren; mätningen rapporterar den som frånvarande" — and left unfilled: "Raden är därför inte ifylld." The returned text carries no byline.

**Anatomy: "a 187-word lead".** Met, and named with the figure: "det 187 ord långa ledet". I measured the input lead at exactly 187 words.

**Anatomy: "no subheading anywhere, so the body has neither a section nor an ending".** Met in substance, though stated as the remedy rather than as a named finding: the lead is divided "på två sektioner med mellanrubriker och en avslutning", and the reply asserts "Övriga brister som granskningen fann är åtgärdade." The returned text has `## Mätningen svarar inte mot rapportens resonemang`, `## Nästa steg ligger i användningstiderna`, and a closing paragraph ending in a reader instruction.

**Anatomy: "a closing sales line unrelated to the explanation".** Met: "Uppmaningen att kontakta avsändaren för att rädda framtiden — ett slut som inte följde av förklaringen."

**"The 39-character headline meets its limit and fails on truthfulness instead."** Met. The headline is treated purely as a truthfulness failure — "Bristen var att rubriken drog en slutsats texten inte drar, så påståendet självt var bristen" — with no length complaint anywhere in the reply.

**Preserve "measured facts".** Preserved. Every figure survives: "14 av 120 lektionspass hade minst ett värde under kontorets egen arbetsgräns på 20 grader, vilket inte är en lagregel"; "Enligt rapporten varade försöket fyra veckor"; "Enligt rapporten stod två givare vid ytterväggar och fyra vid innerväggar"; the report title and date "*Mätförsök i Björkskolan* från den 12 mars 2026"; "likadant placerade givare i november"; and Rask's recommendation verbatim, "Driftteknikern Elin Rask rekommenderar att koppla temperaturserier till användningstider innan styrningen ändras."

**Preserve "exclusions".** Preserved, all six: "utan att placeringens effekt jämfördes experimentellt"; "vilket inte är en lagregel"; "Operativ temperatur saknas"; "medan givarna bara mätte luften där de satt"; "Det saknas mätningar av luftdrag och elevernas upplevelse och uppgifter om hur länge temperaturerna låg under gränsen"; "ingen effekt på hälsan har undersökts."

**Preserve "funding uncertainty".** Preserved verbatim: "fast finansieringen inte är beslutad."

**"Restore navigation."** Done, as quoted above, and the sections are built from the text's own material.

**Rejection: "A supplied-source investigation is not a remedy."** Not made. No source material was available to the run, the reply claims no source reading, and it does not propose consulting one as a fix. Its verification claims are confined to the text itself and to machine measurement: "Anatomins räknade krav är maskinmätta" and "kontrollerade i en ny genomgång av den rättade texten."

**Rejection: clean text rewritten to taste or to numbers.** Not applicable in the direction the corpus fears — this text is not clean — and nothing in the returned text is changed for taste alone. Every difference in section 1 answers a defect, a numeral's placement, an attribution, or the anatomy's missing navigation.

**Rejection: "No unavailable-source verification."** Not made.

## 4. R1

**Pass.**

The passage that decides it is the third *Borttagna påståenden* bullet together with the sentence it acted on. The input welded an unsupported certainty to the very limits that refute it — "men ändå är det helt säkert att givarna har gjort eleverna friskare, trots att ingen effekt på hälsan har undersökts" — and the run removed exactly the certainty while leaving every limit standing: "Det saknas mätningar av luftdrag och elevernas upplevelse och uppgifter om hur länge temperaturerna låg under gränsen, och ingen effekt på hälsan har undersökts." It then reported precisely that, including what it did not touch: "Meningens begränsningar står kvar i sin helhet."

That is the pattern across the whole run. The four visible defects and the four anatomy defects are addressed; no measured fact, exclusion, funding caveat or quoted recommendation is lost; the four claim changes are each disclosed with the change and the reason, one with an explicit offer to revert; the byline is reported as missing and left unfilled rather than invented; and nothing is verified against material the run did not have.

The one blemish is a reporting gap, not a text failure: the duplicated standfirst sentence and the shared opening word are repaired without being named, and the standfirst is given a different diagnosis instead. Under R1 the removals, the rejected losses and the irreparable finding are all reported, so this does not tip the criterion, but it leaves the expectation's second detection clause unmet.
