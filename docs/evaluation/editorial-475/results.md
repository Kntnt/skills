# Results for #475

Both arms, run on 2026-09-30 from 14:49 to 15:30 UTC under the method [`plan.md`](plan.md) froze in `1c9303a0`, before the first run. Artefacts: `runs/`. No run was void. The record is [`../records/redline-claude-2026-09-30-475.md`](../records/redline-claude-2026-09-30-475.md).

Forty-six Redline invocations count, twenty-three in each arm, and each has two judgements, ninety-two in all. Every judge was a fresh `kntnt-opus-high` subagent, blind to the arm, the model and this ticket. Every run was a fresh top-level Claude Code 2.1.285 session made by [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py). Every trace is complete (`trace-status.json`), and the packets' `trace-index.json` files record `claude-opus-5-5` at high deliberation for all one hundred agents they hold: the sessions, their correction subagents and the candidate's checkers. No other seat ran. No Codex Harness and no GPT model was started, controlled or invoked. No source material was supplied: every run's working directory held `input.md` and nothing else when its session started.

**The headline result.** The fault reproduces: 5 of the pre-change arm's 18 response-target runs carry a class 1 or class 2 miss. The candidate carries one in 1 of its 18. That is at most half the pre-change share (27.8% against 5.6%), and no candidate run carries a class 2 miss that is a count or a length. **The Target is met.** One control that passed `C1` in the pre-change arm fails it in the candidate arm, `case-study-clean`. The change that fails it is a clean text reworded on findings no reader would feel, which #468 owns, so under *Whose miss* it is recorded there and **the Control is met**. No revise round is taken. **The candidate `29d4b674` ships.** Its two remaining misses, both in `post-control-case-study-clean`, are filed as #477 and #478.

## The runs

| Arm | Staged from | Runs |
| --- | --- | --- |
| pre-change | `41fd4c55` (`<start>`) | `pre-<draft>-a` and `-b` on each of the four drafts, `pre-control-<id>` once on each of the ten controls, and `pre-control-<id>-file` once on each of the five clean controls: 23 runs |
| candidate | `29d4b674` | the same twenty-three, named `post-…`: 23 runs |

The corpus commit is `41fd4c55` in both arms, and every run's `run.json` names the revision its arm was staged from. The inputs match the SHA-256 digests the plan pinned. The candidate was committed before the plan and before any install was staged. Runs went in seven lanes, as `runs/matrix.tsv` assigns them. Within a lane the arms alternated on each input, and no two runs on one input overlapped (#401).

## The candidate

`29d4b674` adds [`skills/editorial/redline/references/reply-check.md`](../../../skills/editorial/redline/references/reply-check.md), the checker's brief. Step 11 of Redline's `SKILL.md` gains the instruction that starts the checker, in place of *make that check on the drafted reply once step 9 has run*. For the four anatomy genres it also widens the final measurement to every run whose reply says anything about a text. The help page's reply paragraph says that a fresh reader checks the reply against both texts before delivery.

The checker is given:

- the text as it arrived;
- the delivered text;
- the drafted reply;
- for the four anatomy genres, the full output of step 6's measuring command run on the delivered text;
- two Library paths for the duties it applies: `delivery.md`'s *The truth of a report about the text*, and the claim-account sentences of `base.review.md`.

It is told nothing of the review's reasoning or the rounds. It returns two lists:

- every statement of the reply that the text it names contradicts;
- every claim-moving difference that the claim account leaves out or reports short.

The run corrects only the reply from them. The check is made once.

**The checker ran where it should.** Its brief opens with *You are checking one reply*, and the traces find that brief in 19 of the 23 candidate runs. Every one of those started after the run's last Proofread call. The four candidate runs without a checker are exactly the four that returned only the short no-change status: the response-target runs on `article-clean`, `column-clean`, `opinion-clean` and `web-copy-clean`. No pre-change run started one.

## How every `A2` miss was read

The plan's four classes, its reading of an `A2` miss and its split rule (one judge is enough) were applied to all ninety-two judgements. The reading was delegated to six fresh `kntnt-opus-high` subagents under [`runs/classify-brief.md`](runs/classify-brief.md), which states the plan's classes word for word. Each subagent was given only neutral directories, `<scratch>/c/<token>/`, with the run's input, reply, delivered file where there was one, the expectation for a control, and both judgements. Nothing in them named the arm or the revision. The mapping is `runs/classifiers.tsv`. Each classifier checked every class 2 candidate against the texts and counted where a count or length was at stake, and wrote `classes.json`. That file is kept in each run's packet. The builder then read every class 1 and class 2 call and the class 3 calls near the line, and changed none. The calls near the line are all class 3 in the pre-change arm:

- `pre-opinion-en_GB-r1-a`: *Four recommended limits are exceeded* over three bullets. It is four limits: the headline breaks two, its words and its characters.
- `pre-control-case-study-clean`, judge B: *42 ord* over a standfirst the expectation measures at 40. The reply's figure is right, and 40 is the input's measurement, not a limit.

Reading either of them the other way would raise the pre-change share and not the candidate's. The one candidate call near the line is `post-column-sv-r2-a`, judge B: the reply says *Den dubbla betydelsen är borta*, and the judge accepts it and faults only its framing of the loss as a gain in clarity. The reply reports the loss, so the call is class 3. Read as class 1, it would make the candidate's share 2 of 18, still at most half of 5 of 18.

The classes are the plan's:

1. the claim account;
2. a counted miss outside it;
3. recorded, not counted, where the statement is true of its text and the judge faults what it suggests or its framing of a change as a repair;
4. an omission.

Rows are per judge. The reply's words and the judge's are quoted or closely paraphrased. File-target runs are listed too; their misses are recorded and not counted.

### Pre-change arm

| Run | Judge | Class | Kind | Owner | The reply | The judge |
| --- | --- | --- | --- | --- | --- | --- |
| `pre-column-sv-r1-a` | B | 3 recorded |  |  | Korrekturläsningen på slutet bytte det engelska långa tankstrecket i ”formuläret — bibliotekarien” mot ett svenskt tankstreck med mellanslag. | The phrase "med mellanslag" could suggest that spaces were added. They were already in the input, and the returned text has a spaced en dash as the reply says, so the description of the result is correct. |
| `pre-column-sv-r2-a` | A | 3 recorded |  |  | Den gamla rubriken ”Rutan som inte finns” nämnde inget ämne. | What the account gets wrong is the headline's status. It calls the old headline a defect ("nämnde inget ämne") where this judgement finds working voice. |
| `pre-column-sv-r2-a` | B | 3 recorded |  |  | Den gamla rubriken ”Rutan som inte finns” nämnde inget ämne. | The account is accurate. It frames the change as a repaired defect, which I do not accept. |
| `pre-column-sv-r2-b` | A | 1 claim account | changed |  | Rubriken påstår nu att mötesmallen saknar en ruta för varför vi ses. Tidigare sade den bara att en viss ruta inte finns, utan att säga vilken. ... [finding 1:] påstår inte mer än texten gör. | The reply's statement that the headline "påstår inte mer än texten gör" is defensible, but it does not mention that the body's first-named missing box is a *beslut* box and not a *varför* box. |
| `pre-column-sv-r2-b` | B | 1 claim account | changed |  | Rubriken påstår nu att mötesmallen saknar en ruta för varför vi ses. Tidigare sade den bara att en viss ruta inte finns, utan att säga vilken. | The reply does not mention that the body names the missing box as a decision box rather than a why box, but its claim that "Stödet finns i texten" holds. |
| `pre-control-article-clean-file` | A | 3 recorded |  | #468 | Det nya påståendet är textens egen rekommendation, alltså Rasks råd och uppmaningen i slutet. | The reply does not say that the recommendation has moved from Rask to the article's own voice. That shift in attribution goes unreported. |
| `pre-control-article-clean-file` | B | 3 recorded |  | #468 | Rubriken upprepade ingressen (åtgärdat). ... Båda använde orden ”inte varför”. | The account is inaccurate in how it classifies the change. It calls a working headline a defect ("upprepade ingressen"). |
| `pre-control-article-clean-file` | B | 3 recorded |  | #468 | Det nya påståendet är textens egen rekommendation, alltså Rasks råd och uppmaningen i slutet. | It never says that the recommendation, which the body attributes to Rask, now appears without attribution. |
| `pre-control-case-study-clean` | A | 1 claim account | changed | #468 | Ingressen lovar nu att visa vad underhållsgruppen gjorde och vad gruppens egna anteckningar visar. [...] Omfång, säkerhet och tidsföljd är desamma. | It says scope, certainty and chronology are unchanged but does not mention attribution, where "anteckningarna" is now pinned to "gruppens egna anteckningar". |
| `pre-control-case-study-clean` | B | 3 recorded |  | #468 | Texten följer artikelanatomin utan avvikelser. Allt som skriptet räknar håller, och ingressen har 42 ord i ett stycke. | The reply's anatomy paragraph is inaccurate [...] the returned standfirst is two words over that [40-word] limit. The reply presents the new length as compliant and never says its edit changed the count. |
| `pre-control-case-study-clean` | B | 3 recorded |  | #468 | Ingressen hade inte introducerat någon grupp eller några anteckningar, så den som läste ingressen ensam kunde inte avgöra vilka som avsågs. | Class: a change of taste, presented as the repair of a visible defect. [...] "gruppen" follows "Arbetsledaren Maya Lind", and a reader resolves it easily, so this is taste rather than a concrete visible defect. |
| `pre-control-case-study-flawed` | A | **2 counted** | round |  | Rubrik, ingress och inledningsstycke skrevs om, och alla tre mellanrubriker ersattes. | The closing summary is slightly inaccurate: "alla tre mellanrubriker ersattes". Two were replaced and one was added. |
| `pre-control-column-clean` | A | 3 recorded |  | #464 | Uppmaningen saknar ett eget avsnitt. ... Artikelanatomin kräver att slutet är ett eget avsnitt med en egen mellanrubrik. ... Texten uppfyller därför inte anatomin fullt ut. | This finding is therefore a false positive against a clean text. |
| `pre-control-column-clean` | B | 3 recorded |  | #464 | Uppmaningen saknar ett eget avsnitt. ... Artikelanatomin kräver att slutet är ett eget avsnitt med en egen mellanrubrik. ... Texten uppfyller därför inte anatomin fullt ut. | This is a false positive. ... It also tells the reader that "någon" should write a new subheading, so a clean text is left with a request to change it. |
| `pre-control-column-clean-file` | A | 3 recorded |  | #464 | Avslutningen var inte ett eget avsnitt. Uppmaningen ("Prova ändå frågan nästa gång du bokar ett möte …") stod som ett tillägg sist i avsnittet "Ännu en ruta, och ändå vill jag prova". [...] En läsare som skummar mellanrubrikerna fick därför ingen ingång till avslutningen | The justification is not accurate. It claims a defect [...] but the text conforms to the anatomy, so this is a false finding. (Heading 1: a change of taste presented as the repair of a visible defect.) |
| `pre-control-column-clean-file` | B | 3 recorded |  | #464 | Avslutningen var inte ett eget avsnitt. | Class: a structural change of taste presented as the repair of a defect. [...] That is a structural preference, not a concrete visible defect |
| `pre-control-opinion-clean` | A | **2 counted** | finding | #468 | En läsare som hoppar över den fetade ingressen fick inte veta att telefonbokningen var den väg texten vill behålla. Det framgick först i nästa avsnitt. | The reply's justification is inaccurate. ... That overlooks the headline "Avskaffa inte telefonbokningen på ett antagande", which comes before the paragraph. It also overlooks "enbart digital bokning" in the paragraph's own first sentence ... The defect it claims is not visible in the text. |
| `pre-control-opinion-clean` | B | **2 counted** | finding | #468 | Det skrev ”båda bokningsvägarna” utan att säga vilka de två vägarna var. ... En läsare som hoppar över den fetade ingressen fick inte veta att telefonbokningen var den väg texten vill behålla. Det framgick först i nästa avsnitt. | The reason it gives is not accurate. ... In fact the same paragraph opens with "enbart digital bokning", and the heading and standfirst directly above it name "telefonbokningen". |
| `pre-control-opinion-clean` | B | 3 recorded |  | #468 | Ändrat påstående. I inledningsstycket står nu uttryckligen att de två vägar som ska prövas i alla sju lokaler under ett halvår är digital bokning och telefonbokning. Tidigare angav stycket inte vilka de var. ... Båda vägarna fanns redan i texten | The reply also files the insertion as a changed claim, which over-reports it: no claim changed. On the side of caution, that is harmless. |
| `pre-control-web-copy-flawed` | A | 3 recorded |  |  | four one-sentence sections became one sentence and a two-item list | One wording slip: the summary says the four sections became "one sentence and a two-item list", but the result is two sentences ("...including VAT. It includes:") followed by the list. ... The slip is minor. |
| `pre-opinion-en_GB-r1-a` | A | 3 recorded |  |  | Four recommended limits are exceeded, and I didn't treat them as findings: | It says "Four recommended limits are exceeded" but lists three. |
| `pre-opinion-en_GB-r1-a` | A | 3 recorded |  |  | Two short passages in the lead and the second section were reworded, as listed above. | "Two short passages in the lead and the second section" is loose. The reworded paragraph sits under the second H2, which is the third block of the text if the lead counts as one. |
| `pre-opinion-en_GB-r1-a` | B | 3 recorded |  |  | The byline was at the end instead of after the headline (fixed). | The reply calls this a fix, but it is a matter of taste (see D2). The description of the change is still accurate. |
| `pre-opinion-en_GB-r1-a` | B | 3 recorded |  |  | Four recommended limits are exceeded, and I didn't treat them as findings: | The reply says "Four recommended limits are exceeded" but lists only three. Neither misstates a change. |
| `pre-opinion-en_GB-r1-a` | B | 3 recorded |  |  | Two short passages in the lead and the second section were reworded, as listed above. | "Other changes" places the second reworded passage in "the second section", but it is in the second H2 section, which is the third block of the text. |
| `pre-opinion-en_GB-r1-b` | A | 3 recorded |  |  | Author name in the wrong place (fixed). … Readers went through the whole argument, including its "I" and "We", before learning who was making it. | The reply calls the change a fix of a defect … That describes a preference, not a visible error, but the change itself is described accurately. |
| `pre-opinion-en_GB-r1-b` | A | 3 recorded |  |  | Changed (finding 3): in the proposed trial, officers now do the time recording and the user survey, not "the administration". | The reply does not mention that the definite article was dropped, which is a trivial omission. |
| `pre-opinion-en_GB-r2-a` | A | 3 recorded |  |  | Byline (fixed). The byline read *Sanna Ek, spokesperson for Öppna beslut*. An English byline takes the form "By <author>", so it now reads *By Sanna Ek, spokesperson for Öppna beslut*. | The reply presents a convention as a rule. The wording change it describes is exactly the one made. [...] the byline "By" is a matter of convention, not a concrete defect. It is a change of taste, even though the reply calls it a fix. |
| `pre-opinion-en_GB-r2-a` | B | 3 recorded |  |  | Byline (fixed). [...] An English byline takes the form "By <author>", so it now reads *By Sanna Ek, spokesperson for Öppna beslut*. | The reply presents the change as a fix required by a rule. The input does not support that, since the original form is not an error. The before and after quoted in the reply are exact. |
| `pre-opinion-en_GB-r2-b` | A | **2 counted** | count |  | Apart from the two changes to claims above, this run changed three things: it put the byline in the English form; it named the board in the body of the ending; it named the two booking routes in the lead. | "Changes overall" also counts it [the lead change] a second time, which does no harm. |
| `pre-opinion-en_GB-r2-b` | A | 3 recorded |  |  | Byline: it didn't use the English form "By <author>", so it read like an unlabelled caption. It now starts with "By". | The change is reported accurately. Calling it a defect is the Skill's own judgement: the original was not unlabelled in any way that blocked the reader. |
| `pre-opinion-en_GB-r2-b` | A | 3 recorded |  |  | Changed: the lead now says the two routes to keep are web and telephone (fix 3). The text already said this in the section on the pilot. | The report is accurate, but it over-classifies the change as a claim change. Its own words ("the text already said this") show that the claim is the same. |
| `pre-opinion-en_GB-r2-b` | B | **2 counted** | count |  | Apart from the two changes to claims above, this run changed three things | The account has one inaccuracy, in its tally. ... lists the lead's two routes among the three. That change is already one of the "two changes to claims". Taken together, the reply implies five changes where there are four. |
| `pre-opinion-en_GB-r2-b` | B | 3 recorded |  |  | Byline: it didn't use the English form "By <author>", so it read like an unlabelled caption. It now starts with "By". | The change is reported, but the reply presents a taste preference as a defect. |
| `pre-opinion-en_GB-r2-b` | B | 3 recorded |  |  | Changed: the lead now says the two routes to keep are web and telephone (fix 3). The text already said this in the section on the pilot. | Counting it as a claim change is conservative but harmless. |
| `pre-opinion-en_GB-r2-b` | B | 3 recorded |  |  | Changed: section "Six months would produce the figures". The author's position now names the cost to be weighed as the double administration, so it can no longer be read as the trial's cost (fix 4). | The reply does not mention the other possible reading, per-route handling work, but it does not misstate the change. |

### Candidate arm

| Run | Judge | Class | Kind | Owner | The reply | The judge |
| --- | --- | --- | --- | --- | --- | --- |
| `post-column-sv-r1-a` | B | 3 recorded |  |  | Mätningen räknar därför det inledande stycket som sju stycken, men det felet följer bara av att avsnitten saknas. | The sentence "Mätningen räknar därför det inledande stycket som sju stycken" is muddled. |
| `post-column-sv-r2-a` | A | 3 recorded |  | #468 | ”Rutan som inte finns” angav inget ämne. | The account is candid and correct. It does call the headline a defect ("angav inget ämne"), and I do not accept that it is one (see section 4). |
| `post-column-sv-r2-a` | B | 3 recorded |  | #468 | Den dubbla betydelsen är borta. | The account is accurate. It describes the loss of the double meaning as a gain in clarity rather than as a cost. |
| `post-column-sv-r2-b` | A | 3 recorded |  |  | Åtgärdat – rubriken namngav inget ämne. ”Rutan som inte finns” säger att en ruta saknas men inte var. En läsare som bara ser rubriken, i en lista eller ett sökresultat, kan inte avgöra att texten handlar om en mötesmall. | The Skill presents this as the repair of a visible defect: a headline that names no subject. The input has no such defect. [...] It is the diagnosis that falls short, not the reporting: the reply calls the original headline a defect |
| `post-column-sv-r2-b` | B | 3 recorded |  |  | Åtgärdat – rubriken namngav inget ämne. | The reply still presents the change as the repair of a defect ("rubriken namngav inget ämne"). I do not accept that classification (see §1), but the reply does not misstate what changed. |
| `post-control-case-study-clean` | A | 1 claim account | changed | #468 | Det är nu Maya Lind som berättar vad försöket krävde, inte anteckningar. | Finding 4 also says what the trial required "kommer från den berättande texten och från Maya Linds citat". The rewrite then gives the whole of it to Lind, and that attribution change is not reported. |
| `post-control-case-study-clean` | A | **2 counted** | finding | #468 | Men texten redovisar bara en intern försöksanteckning från Elm Quay, och den säger uttryckligen att skillnaden i mediantid inte beror på programvaran. | The text says only that the note "tillskriver … inte skillnaden programvaran" (does not attribute the difference to the software). That is a refusal to attribute, not a denial of cause, so the finding raises the certainty of a qualified statement. |
| `post-control-case-study-clean` | A | 3 recorded |  | #463 | Rubriken – ”Elm Quay samlade reparationsärendena” var för generell. Bestämd form utan avgränsning lät som att Elm Quay hade samlat alla sina reparationsärenden. [...] (and the opening: "Jag hittade fyra fel i texten") | The input headline has no visible defect, so this is a change of taste that also changes scope. [...] The reply's opening, "Jag hittade fyra fel i texten", presents four defects in a text the reply itself says "följer artikelanatomin utan avvikelse". |
| `post-control-case-study-clean` | A | 3 recorded |  | #468 | Inledningen, andra meningen – ”Försöket” i bestämd form syftade bara tillbaka på ingressen. | Class: a change of taste. The definite form points back to the standfirst, which is ordinary in an article. The claim is unchanged. |
| `post-control-case-study-clean` | B | 1 claim account | changed | #468 | Det är nu Maya Lind som berättar vad försöket krävde, inte anteckningar. | The reply also says the requirements come "från den berättande texten och från Maya Linds citat", yet its fix credits them to Lind alone. [...] The new attribution is slightly inaccurate. Part of what the trial required is stated by the narrator, not by Lind: Svale configured the log and trained six staff. |
| `post-control-case-study-clean` | B | **2 counted** | finding | #468 | den säger uttryckligen att skillnaden i mediantid inte beror på programvaran. | The finding's rationale misstates the source [...] the note declines to attribute the difference and does not deny a software effect. The finding therefore turns a withheld attribution into a denial. |
| `post-control-case-study-clean` | B | 3 recorded |  | #463 | Rubriken – ”Elm Quay samlade reparationsärendena” var för generell. [...] Den som bara såg rubriken fick inte veta att det var ett avgränsat försök. | The case for calling it a visible defect is weak, because the standfirst straight below already limits the trial to two buildings and eight weeks. Mostly a change of taste. |
| `post-control-case-study-clean` | B | 3 recorded |  | #468 | Inledningen, andra meningen – ”Försöket” i bestämd form syftade bara tillbaka på ingressen. | Class: a change of taste, or at most a marginal referent repair. The meaning is unchanged. [...] Finding 3 is taste too. |
| `post-control-case-study-clean-file` | A | 3 recorded |  | #468 | Inledningen, andra meningen. ”Försöket” syftade på ett försök som bara ingressen berättade om. Den som läser brödtexten utan ingressen fick själv räkna ut att loggen prövades i ett försök. | Finding 2 ... demands that the intro repeat what the standfirst directly above it has just said. That is a preference, not a visible defect. |
| `post-control-case-study-clean-file` | B | 3 recorded |  | #468 | Inledningen, andra meningen. ”Försöket” syftade på ett försök som bara ingressen berättade om. | Finding 2 in particular treats an ordinary Swedish definite reference, which points back to a trial that the headline and standfirst have just introduced, as a defect. |
| `post-control-case-study-clean-file` | B | 3 recorded |  | #468 | Mätskriptet mätte gränserna på den levererade texten: rubriken har 36 tecken, ingressen 43 ord och inledningen 48 ord. | The reply does not mention that the standfirst now runs to 43 words where it had 40, although it prints 43 as a measurement. |
| `post-control-column-clean-file` | A | 3 recorded |  | #464 | Slutet saknade ett eget avsnitt. ... Det sista avsnittet, ”Ännu en ruta, och ändå vill jag prova”, innehöll både förslaget och textens avslutande uppmaning. ... Artikelanatomin kräver att slutet är ett eget avsnitt med en egen mellanrubrik. | The text conforms, so a correct run reports no structural finding. ... Per the standard this is a false finding, and the run changed the text because of it. |
| `post-control-column-clean-file` | A | 3 recorded |  | #464 | Texten följer artikelanatomin. Mätskriptet godkänner de räknade kraven i den levererade texten. ... Det finns två avvikelser från normerna, men ingen av dem är ett fynd ... Förslagsavsnittet och slutet består nu av ett stycke var. | The reply also contradicts itself. It ends by saying "Texten följer artikelanatomin", yet that is true only of the text it delivered. The same reply also lists a paragraph-count deviation that its own repair created. |
| `post-control-column-clean-file` | B | 3 recorded |  | #464 | Krav: Artikelanatomin kräver att slutet är ett eget avsnitt med en egen mellanrubrik. ... Reparation: Slutstycket står nu oförändrat under en ny mellanrubrik | What is not accurate is the premise. The reply presents the change as the repair of a defect ("Artikelanatomin kräver att slutet är ett eget avsnitt med en egen mellanrubrik"), but the standard says the text already conforms to the anatomy. |
| `post-control-opinion-flawed` | A | 3 recorded |  |  | Övriga delar finns i rätt ordning. Sista avsnittet är ett eget slutavsnitt, och varje mellanrubrik beskriver sitt avsnitt. | The anatomy line at the top ... describes the returned text, not the input. Read alone it could mislead, but the heading repairs listed below it make clear what was wrong before. |
| `post-control-opinion-flawed` | A | 3 recorded |  |  | Ändrade: Mellanrubriken ”Kommunstyrelsen bör ge telefonbokningen en chans” återger förslaget i första stycket som en rekommendation. Den nämner varken ”ett halvårs”, ”försök” eller ”i alla sju lokaler”, och den lägger till en inramning | It is filed under "Ändrade" although it is new text, which is a minor filing quirk that does not mislead. |
| `post-opinion-en_GB-r1-a` | A | 3 recorded |  |  | Before, readers didn't learn who was making the argument until the last line. That meant "Öppna beslut proposes…" and "We make no claim to have funded or costed that trial" in the third section came before they knew Öppna beslut is the author's organisation. | The reason the Skill gives is weaker than its report of the change. [...] the text marks the author's side before the end: "Öppna beslut proposes…" is followed straight away by "We make no claim…". (D1: a change of taste; the input shows no visible defect here.) |
| `post-opinion-en_GB-r1-a` | A | 3 recorded |  |  | Without that paragraph, the body never says what the board is being asked to decide: removing phone booking from all seven community venues from September. The reader only meets "a channel for good" in section 2. | That overstates the case, because section 2 and the final section together make the decision clear. |
| `post-opinion-en_GB-r1-a` | B | 3 recorded |  |  | Fixed: the byline was in the wrong place and the wrong form. [...] Before, readers didn't learn who was making the argument until the last line. | That problem is weak when checked against the input [...] So this is not the repair of a visible defect. [...] The Skill calls it "Fixed", that is, a defect. As said above, I rate it as taste, but the reply describes the actual edit correctly. |
| `post-opinion-en_GB-r1-b` | B | 3 recorded |  | #468 | Byline out of place (repaired). ... A reader therefore met "Öppna beslut proposes…" and "We make no claim…" without knowing that the author speaks for Öppna beslut. | That reading is defensible but weak. A closing sign-off is a standard form for an opinion piece, and "Öppna beslut proposes" already names the proposer in the sentence before "We make no claim". |
| `post-opinion-en_GB-r1-b` | B | 3 recorded |  | #468 | Lead relied on the headline (repaired). The lead said "the council executive board" and "all seven community venues" without saying whose. | The Skill presents this as the repair of a visible defect ("Lead relied on the headline"). I do not find a defect a reader would stumble on, because the lead sits directly under a headline that names Lervik. |
| `post-opinion-en_GB-r2-a` | A | 3 recorded |  |  | Fixed: the byline lacked the English "By" form. … Directly under the headline, it could be read as a caption or a credit line. | The reply calls this a defect ("could be read as a caption or a credit line"). I judge it a matter of taste, but the change itself is described correctly. |
| `post-opinion-en_GB-r2-a` | B | 3 recorded |  |  | Fixed: the byline lacked the English "By" form. … Directly under the headline, it could be read as a caption or a credit line. | The reply calls it a defect ("it could be read as a caption or a credit line"). I class it as taste, but the report of the change is accurate. |
| `post-opinion-en_GB-r2-b` | A | 3 recorded |  |  | "It" relied on the subheading to supply "the board". Without the subheading, the nearest possible meanings were "each route" and "the people who use it". | The reason it gives, that "It" could be read as "each route" or "the people who use it", is weak. The report of the change itself is exact. |
| `post-opinion-en_GB-r2-b` | B | 3 recorded |  |  | One claim changed: the lead now says the two routes are the telephone and the web (finding 3). Before, the lead left the second route unnamed, although the third section already named it. | The account overstates its own change here: the claim's content does not change, because the body already said it. That errs towards disclosure, so it does not misreport. |

## The shares

A run carries a miss where either judge records a class 1 or class 2 miss in it. The Target reads the eighteen response-target runs of each arm; no file-target run carries a class 1 or class 2 miss in either arm.

| Arm | Runs carrying a miss | Share |
| --- | --- | --- |
| Pre-change | `pre-column-sv-r2-b` (class 1), `pre-control-case-study-clean` (class 1), `pre-control-case-study-flawed` (class 2, a round), `pre-control-opinion-clean` (class 2, a finding), `pre-opinion-en_GB-r2-b` (class 2, a count) | 5 of 18, 27.8% |
| Candidate | `post-control-case-study-clean` (class 1 and class 2, a finding) | 1 of 18, 5.6% |

Each pre-change run carries one distinct miss. `post-control-case-study-clean` carries two: a class 2 statement about the text as received, and a class 1 entry about an attribution. Both judges record both.

## Reproduced

**Met.** Five pre-change runs carry a class 1 or class 2 miss, and the plan asks for one:

- `pre-column-sv-r2-b`, both judges, class 1. The headline entry says the new headline names a box *för varför vi ses*. It does not say that the body's missing box is one for the decision, so the change moved the headline's meaning.
- `pre-control-case-study-clean`, judge A, class 1. The standfirst entry says scope, certainty and chronology are unchanged. It leaves out the attribution the rewrite added: *anteckningarna* became *gruppens egna anteckningar*.
- `pre-control-case-study-flawed`, judge A, class 2. The reply says *alla tre mellanrubriker ersattes*. The input has two subheadings; the third was added, not replaced.
- `pre-control-opinion-clean`, both judges, class 2. A finding says that a reader who skips the standfirst learned only in the next section that telephone booking is the route to keep. The headline above that paragraph already says so.
- `pre-opinion-en_GB-r2-b`, both judges, class 2. The reply says the run changed three things apart from the two claim changes. There were four differences in all, two of them the claim changes, so two others, not three.

The kinds match #451–#462: false statements about a text, and claim-account entries short of what a change did. The same statements did not recur.

## The Target

**Met.**

- **The share.** The candidate's 1 of 18 is at most half the pre-change arm's 5 of 18, which would allow 2.5.
- **No false count or length in the candidate.** The candidate's one class 2 miss is a finding's description of the text as received: *den säger uttryckligen att skillnaden i mediantid inte beror på programvaran*, where the note only declines to credit the software. It is not a count or a length. The pre-change arm's false count (`pre-opinion-en_GB-r2-b`) and false round statement (`pre-control-case-study-flawed`) have no counterpart in the candidate arm.

The candidate's drafts carry no class 1 or class 2 miss in any of their eight runs, against two in the pre-change arm's eight. The checker did not catch the two misses of the one candidate run that carries any, `post-control-case-study-clean`, a run whose text changes #463 and #468 own.

## The Control

`C1` is each control judge's heading-4 verdict. A control passes in an arm where both judges pass it. A clean control's `C1` is read from its file-target run, whose judges read the delivered `work/output.md`. A flawed control's is read from its response-target run.

| Control | Pre-change | Candidate |
| --- | --- | --- |
| `article-clean` (file) | fail / fail: headline rewritten | pass / pass: *Under 14 av 120* → *Vid 14 av 120* in the standfirst, a repair both judges accept |
| `case-study-clean` (file) | pass / pass: unchanged | **fail / fail**: standfirst and intro reworded on two reference findings |
| `column-clean` (file) | fail / fail: a subheading added over the ending (#464) | fail / fail: a subheading added over the ending (#464) |
| `opinion-clean` (file) | pass / pass | pass / pass |
| `web-copy-clean` (file) | pass / pass | pass / pass |
| `article-flawed`, `case-study-flawed`, `column-flawed`, `opinion-flawed`, `web-copy-flawed` | pass / pass on each | pass / pass on each |

Only `case-study-clean` passed in the pre-change arm and fails in the candidate arm. In `post-control-case-study-clean-file`:

- the standfirst's *gruppen … anteckningarna* became *underhållsgruppen … gruppens anteckningar från försöket*, on the finding that neither had a referent in the standfirst;
- the intro's *Försöket pågick* became *Loggen prövades i ett försök som pågick*, on the finding that the definite form pointed back only to the standfirst.

Judge A calls the intro edit a change of taste and the standfirst edit easier to defend. Judge B fails both as a clean text treated as defective. Neither judge faults the reply's account of them.

**Whose miss.** The plan names #468 as owning *a clean text changed over a loss no reader suffers*, and the readiness addendum glosses it as *a clean text changed*. This is that behaviour, and it is not the checker's:

- The checker never touches the text. It starts after the mechanical pass that produced the final text, and it returns lists about the reply only.
- The same rewrite of the same standfirst appears in the pre-change arm's response-target run on this control. There *anteckningarna* became *gruppens egna anteckningar*.

So the failure is recorded under #468 and is not a Control miss. **The Control is met.** Read the other way, the Control would be missed on `case-study-clean`. The protocol's revise round would then run on `case-study-clean` alone, against a revised candidate with nothing in its reach to revise, since the text changes come before the checker is started.

## No revise round, and what ships

The candidate meets the Target and the Control on its first reading. So under *What ships* item 2, **the candidate ships as committed in `29d4b674`**. Nothing is reverted. *Not reproduced* does not apply, and the halving is met, so no decision record is owed; the reserved number `0235` is left unused.

## Whose miss

The plan names the open tickets whose behaviour a run of these inputs can show: #463, #464 and #468.

- **#463**, `case-study-clean`'s headline rewritten as an overclaim. Its change appears in `post-control-case-study-clean`, whose headline finding judges class 3. The false statement and the short entry in the same run count here.
- **#464**, a subheading added over `column-clean`'s ending. It appears in `pre-control-column-clean-file` and `post-control-column-clean-file`, which fail `C1` in both arms. It also appears in `pre-control-column-clean`'s rolled-back attempt. The judges' class 3 remarks on the finding are recorded under it.
- **#468**, a clean text changed. It appears in `pre-control-case-study-clean`, `pre-control-opinion-clean`, `post-control-case-study-clean` and `post-control-case-study-clean-file`, and in `pre-control-article-clean-file`'s headline rewrite. Class 1 and class 2 misses about those changes count here, as the addenda say. The `C1` failure of `post-control-case-study-clean-file` is recorded under #468.

**Filed from this evaluation.** Each is its own `needs-triage` issue naming #475. They are every class 1 and class 2 miss of the candidate reading that ships:

- #477, class 2: *den säger uttryckligen att skillnaden i mediantid inte beror på programvaran*, of a note that only declines to credit the software.
- #478, class 1: *Det är nu Maya Lind som berättar vad försöket krävde*, which does not say that the narrator's own statements of what the trial required now read as Lind's.

No class 4 miss was recorded in either arm. The pre-change arm's misses belong to the product this change replaces. They are recorded above and not filed.

## Also recorded: `R1` on the drafts

The pairs are judge A / judge B. `R1` is recorded, not scored.

- Pre-change: pass / pass on both `column-sv-r1` runs and all four `opinion-en_GB` runs; fail / fail and fail / pass on the two `column-sv-r2` runs.
- Candidate: pass / pass on both `column-sv-r1` runs and all four `opinion-en_GB` runs; fail / fail on both `column-sv-r2` runs.

The failures are the column's figurative headline rewritten, the behaviour #429 addressed.

## Side effects

`O1` is met on all forty-six runs, and `S1` with it.

- **The runner's inventories.** Each packet's `filesystem-changes.json` is computed from the runner's before-and-after inventories of the run's private root. It shows no created, removed or changed path outside the Harness's own configuration directory and caches, with one exception: each file-target run created `work/output.md`, the effect it asked for. One run, `post-control-case-study-clean-file`, also left macOS's Python bytecode cache under its private `HOME/Library/Caches`.
- **The input and the Skills.** `work/input.md` is unchanged in every run, and the staged Skills are byte-identical before and after.
- **Cleanup.** The runner removed every private root (`cleanup.json`).

All forty-six runs were one wave, read around it into `runs/wave-1-before-*.txt` and `runs/wave-1-after-*.txt`. Every change is attributed by path, and none is a run's:

- **This working tree.** Only the wave inventories' own files appeared.
- **The main checkout.** `HEAD` moved from `e8263354` to `b3af5f7f`: the orchestrating run integrated other tickets.
- **The session scratchpad.** It gained the orchestrator's `own/amend-469-1.md`, `own/integrate-463.json` and `own/integrate-469.json`, and its `own/fill.py` changed. It also gained `out.md`. A judge of this build reported writing that file as scratch and deleting it; it was gone when checked after the wave.
- **This build's scratch root.** Its after-listing holds this build's inputs, packets, logs, tools and judge and classifier directories, and nothing else.

Each judge's directory held only its inputs and its judgement when it was collected, and each was removed once its judgement was copied. Each judge was given its brief's text, unchanged, in the message that dispatched it.

## What is not measured

- Unslop carries the same claim account, is out of #475's scope, and is neither changed nor run. The checker lives in Redline's own `references/`, so no other Skill reaches it.
- `T1` and `R2` are `skipped`. Every packet keeps its trace, so they can be judged from it later.
- `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` and `T2` are `skipped`, because `A2`, `C1`, `O1` and `S1` are this evaluation's criteria.
- What the checker returned in each run, and which statements the run corrected from it, is in the transcripts under `runs/post-*/transcripts/` and was not read into this result. The Target reads the delivered reply, as the plan says.
