# Judgement b

## 1. Differences

None. I extracted the fenced text from `response.md` and compared it with `work/input.md` using `cmp`. The two are byte-identical: the same headline, the same bold standfirst with its duplicated sentence, the same single body paragraph (187 words), the same formatting, and no frontmatter in either file. No mechanical correction, no repair, no change of taste and no change to any claim.

## 2. The account

Nothing changed, so the account has no difference to report. What it does say about the text is accurate:

- "Texten levereras oförändrad." True.
- "Den levererade texten är byte för byte densamma som den som kom in. Inget påstående i den har tagits bort, ändrats eller lagts till." True, confirmed with `cmp`.
- "Korrekturläsningen efteråt hittade inga mekaniska fel." Consistent with the returned text. That pass is not the Skill's own work, so it is not scored here.
- The rejected correction round is described openly and in detail: a new headline, "Mätförsök i Björkskolan fann värden under 20 grader", and a new first standfirst sentence. According to the reply, the round was rejected because the new headline repeated the standfirst, and the text was restored exactly. None of this appears in the delivered text, and the reply says so.

## 3. The frozen expectation

**Detect**

- *Unsupported catastrophe/health certainty visible against explicit limits*: detected. Finding 1 says the headline "påstår något texten inte bär … säger tvärtom att ingen effekt på hälsan har undersökts". Finding 6 says "Katastrofen lurade bakom varje hörn" is "ren dramatik utan stöd … motsägs den av textens egna förbehåll". Finding 11 says "Här påstås ett säkert orsakssamband utan stöd, och förbehållet i samma mening motsäger det."
- *Standfirst and lead repeat each other and open on the same word*: detected. Finding 5 says "Brödtexten börjar med ingressens mening ordagrant, så texten börjar två gånger. Den står också i bestämd form, ”Givarna” …" Finding 2 also reports that the standfirst repeats its own sentence.
- *Late concept*: detected. Finding 5 says "Rapporten och Björkskolan nämns först i tredje meningen. Den som hoppar över ingressen möter givare som ingen har presenterat." Finding 3 says the standfirst "nämner inte skolan, mätförsöket eller vad artikeln ger läsaren". Finding 10 adds that "resonemanget" has no referent.
- *Unbroken paragraph mixing unlike jobs*: detected. Finding 7 says "Brödtexten är ett enda stycke på 187 ord … rymmer flera tankar: resultatet och försökets upplägg, vad mätningen saknar, hälsopåståendet, rekommendationen och nästa försök samt avslutningen."
- *No byline, reported missing and left unfilled*: detected and handled correctly. Finding 4 says "Byline saknas. … så den lämnas åt en människa att fylla i." The returned text has no invented byline.
- *A 187-word lead*: detected in substance. Finding 7 measures the 187 words ("uppmätt"), and the closing note calls the paragraph "inledningen". The reply judges it against the paragraph norm ("högst 80 ord"), not against a lead-length limit, but it names the right passage and the right figure.
- *No subheading, so neither a section nor an ending*: detected. Finding 8 says "Mellanrubriker, avsnitt och ett eget avslutande avsnitt saknas. Anatomiskriptet mätte att både byline och avsnitt saknas". The closing note repeats "avslutningen saknas (fynd 8 och 13)".
- *Closing sales line unrelated to the explanation*: detected. Finding 13 says "”Kontakta oss för att rädda framtiden.” … ”oss” identifieras ingenstans och uppmaningen följer inte av texten."
- *39-character headline meets its limit and fails on truthfulness*: detected exactly as expected. Finding 1 fails the headline on truthfulness and adds "Rubriken håller sig inom anatomins gränser (39 tecken, 6 ord)." I counted 39 characters.

**Preserve**

- *Missing navigation reported, not written*: preserved. The returned text has no subheadings. Finding 8 says "Delarna lämnas åt en människa att skriva."
- *No measured fact deleted*: preserved. "14 av 120 lektionspass hade minst ett värde under kontorets egen arbetsgräns på 20 grader", "försöket varade fyra veckor" and "två givare stod vid ytterväggar och fyra vid innerväggar" are all still in the text.
- *No exclusion deleted*: preserved. "vilket inte är en lagregel", "utan att placeringens effekt jämfördes experimentellt", "Operativ temperatur saknas", "Det saknas mätningar av luftdrag och elevernas upplevelse och uppgifter om hur länge temperaturerna låg under gränsen" and "trots att ingen effekt på hälsan har undersökts" are all still in the text. Finding 11 also says explicitly that these limits "ska stå kvar".
- *No funding uncertainty deleted*: preserved. "fast finansieringen inte är beslutad" is still in the text.

**Rejections**

- *A supplied-source investigation is not a remedy*: the run did not make this mistake. No finding asks for the source report, a check against sources or further research. Unresolved parts are left for a human to write (findings 4 and 8), or described as not recoverable from the text (finding 13: "ett användbart nästa steg kan inte hämtas ur den").

**Minor observations, none decisive**

- Finding 9 reads "medan" as a causal or connecting claim between duration and placement. That is a stretch. It is only a finding, though, and it changed no text.
- The returned text still contains defects that could have been removed without any outside facts: the duplicated standfirst sentence, "Katastrofen lurade bakom varje hörn", "helt säkert", and the circular filler sentence. They remain because the single correction round was rejected and the budget of 1 was used up. That is a matter of final-text quality. The corpus scores it separately from detection and preservation.

## 4. R1

**Pass.** Every defect the expectation names is reported concretely, against the passage that carries it. Nothing outside the findings changed: the reply's statement "Den levererade texten är byte för byte densamma som den som kom in. Inget påstående i den har tagits bort, ändrats eller lagts till" is confirmed by `cmp`. The single correction round that would have introduced a new defect (headline echoing the standfirst) was rejected and fully reverted, and the reply reports it openly. No unavailable source was asked for or verified against, and the clean parts of the text were not rewritten. Leaving the reported findings unresolved in the final text is a quality shortfall that the corpus scores separately. It is not a loss of voice, argument or claim.
