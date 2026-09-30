# Results for #435

Both arms and one revise round, run on 2026-09-30 (from 22:00 UTC on 29 September to 06:33 UTC on 30 September) under the method [`plan.md`](plan.md) froze in `8f6a87b3`, before the first run. Artefacts: `runs/`, and `voided/` for six runs an expired login cut off. The record is [`../records/redline-claude-2026-09-30-435.md`](../records/redline-claude-2026-09-30-435.md).

Forty-three Redline invocations count: fourteen in the pre-change arm, eighteen in the candidate arm and eleven in the revise round. Each has two judgements, eighty-six in all. Every judge was a fresh `kntnt-opus-high` subagent, blind to the arm, the model and this ticket. Every run was a fresh top-level Claude Code 2.1.285 session made by [`../editorial-388/harness/staged_run.py`](../editorial-388/harness/staged_run.py). Every trace is complete. The packets' `trace-index.json` files record `claude-opus-5-5` at high deliberation for all eighty-four agents they hold, sessions and correction subagents alike, and no other seat. No Codex Harness and no GPT model was started, controlled or invoked. No source material was supplied: every run's working directory held `input.md` and nothing else when its session started.

**The headline result.** The fault reproduces in the pre-change arm, but in 2 of its 14 runs and not as the six statements #435's body lists; none of those six recurred. Neither wording lowered the share of runs whose reply says something false about a text. The first wording carried a counted miss in 6 of 18 runs. With the revised wording read in its place on the inputs the ship rule sent back, the share is 3 of 18, against 2 of 14 before. So the Target is missed. The revised wording stopped every *unchanged* / *untouched* / *named nowhere else* statement the first wording's runs got wrong. Two counts about the delivered text are still false: *no paragraph is over 65 words* over a 66-word paragraph, and *Seven headings became two* where seven became three. The Control is missed on one input, `column-sv-r1`, over a changed claim whose entry does not say what the change did. **The revised wording ships**, as the ship rule says, because it has the lower share of counted runs over the revised inputs: 3 of 11, against the first wording's 6 of 11. Each remaining miss is filed, as #451 to #462.

## The runs

| Arm | Staged from | Runs |
| --- | --- | --- |
| pre-change | `e7773344` (`<start>`) | `pre-<draft>` once on each of the four drafts, and `pre-control-<id>` once on each of the ten controls: 14 runs |
| candidate | `12a1c7d2`, the first wording | `post-<draft>-a`, then `-b`, on each draft, and `post-control-<id>` once on each control: 18 runs |
| revise | `77dd847a`, the revised wording | `revise-<draft>-a` and `-b` on all four drafts, and `revise-control-<id>` on `column-clean`, `opinion-clean` and `web-copy-flawed`: 11 runs |

The corpus commit is `e7773344` in every arm. The inputs match the SHA-256 digests the plan pinned. The first wording was written and committed while the pre-change runs were in flight. The pre-change install is a `git archive` export of `e7773344` in every case, so no candidate reached a pre-change run. Runs on different inputs ran side by side in four lanes. Runs on one input ran one after the other, and no two runs on one input overlapped (#401).

**Void runs.** The revise round's first wave was cut off at 22:58 UTC on 29 September by an expired login. The harness's own words were `authentication_failed` and *401 OAuth access token has been revoked*. Six runs ended with `terminal_reason: api_error`, having returned only that message: `revise-column-sv-r2-b`, `revise-opinion-en_GB-r1-b`, `revise-opinion-en_GB-r2-b`, `revise-control-column-clean`, `revise-control-opinion-clean` and `revise-control-web-copy-flawed`. Under the plan's *Void runs*, each packet was moved whole to `voided/`, and each run was made again from the same commit once the login had been repaired, at 06:25 UTC on 30 September. None of the six was judged before it was voided. The four `revise-<draft>-a` runs and `revise-column-sv-r1-b` had completed before the interruption, and their eight judgements already written were each complete, with all four headings and a verdict. They were kept.

## The wordings

The first wording (`12a1c7d2`) adds a section, *The truth of a report about the text*, to `skills/kntnt/library/references/delivery.md`, immediately after *The language of a report about the text*, and names its subject in the opening paragraph's list. The section says:

- everything a run says about a text is true of the text it names, counts, lengths, grammatical labels, where a passage stands and what a round did to a passage among it;
- a statement about the delivered text is checked against the delivered text after the last change to it, the closing mechanical pass included;
- where a run measures a text with the Library's `scripts/article_anatomy.py`, a count or length is taken from that script's measurement of the text the statement is about;
- a statement about the text as it arrived says so;
- a statement that cannot be made true is left out.

Redline's step 11 and Unslop's step 9 point at it and call their claim-account and closing-paragraph sentences instances of it. Redline's step 11 says that for the four anatomy genres a count or length about the delivered text comes from step 6's measurement run again on the final Text Artifact from step 9. Both help pages say it in their reply paragraph.

The first wording's runs still wrote absolutes that one exception made false:

- *Resten av texten är orörd* beside a proofread dash;
- a paragraph *word for word what it was* beside its changed *business days*;
- the board *named nowhere else* where the lead names it;
- *antagandet* pointing at an assumption *bara rubriken nämner* where the last section names one;
- a heading's wording *drawn from the rest of the section* that came from another section.

The revised wording (`77dd847a`) therefore adds one paragraph to the shared section, and Redline's and Unslop's pointers now say when to make the check. The added paragraph says:

- the check is made on the reply as drafted, one statement at a time, once the text is final, against the passage each statement names rather than the run's memory of it;
- a finding written during the review is checked the same way against the text it was written about;
- a statement that something holds everywhere or nowhere is checked against every part of the text it covers, and names the exception or is narrowed;
- a statement of where wording came from, or where a passage stands, is checked by finding that passage.

## Reproduced

The pre-change arm reproduces the fault in 2 of its 14 runs, and the plan's *Reproduced* is met.

- `pre-opinion-en_GB-r1`, judge A: *The first sentence under it repeated two of its three items in the same words.* The items are *Six months* against *six-month trial*, and *both routes* against *both booking routes kept open*, which are close and not the same words.
- `pre-opinion-en_GB-r2`, both judges: *All the sentences that limit the claims are unchanged*. Two limiting sentences each had *channels* changed to *routes*.

None of the six statements #435's body lists recurred in the pre-change arm.

## Every `A2` miss, read and classed

Each miss is recorded below with its run, its judge, its class and, where one applies, its kind and the open ticket it is recorded under. The reply's words and the judge's are quoted or closely paraphrased. *#429(change)* marks a class 2 miss whose false statement counts here while the change it describes, a working heading rewritten, is #429's. The classes are the plan's:

1. the claim account;
2. a counted miss outside it;
3. recorded, not counted, where the statement is true of its text and the judge faults what it suggests or how it frames a change;
4. an omission.

### Pre-change arm

| Run | Judge | Class | Kind | Owner | The reply | The judge |
| --- | --- | --- | --- | --- | --- | --- |
| `pre-column-sv-r1` | B | 3 recorded |  |  | ett svenskt [tankstreck] med mellanslag (–) | "med mellanslag" suggests spaces were added; the em dash already had spaces |
| `pre-column-sv-r2` | B | 1 claim account | changed |  | Rubriken påstår nu, med förbehållet "kanske", att mötesmallen kan behöva en fråga om syfte | does not note that the new headline recasts the proposed question as one about "syfte" |
| `pre-column-sv-r2` | B | 3 recorded |  | #429 | rubriken är reparerad | the description of what changed is accurate; its classification as a repair is not (no visible defect) |
| `pre-opinion-en_GB-r1` | A | 1 claim account | changed |  | [section 3 subheading] now calls for measuring staff time ... no longer mentions six months or keeping both routes open | does not note that "staff time" is narrower than the sentence under the heading |
| `pre-opinion-en_GB-r1` | A | **2 counted** | finding | #429(change) | The first sentence under it repeated two of its three items in the same words | overstates the case: "Six months"/"six-month trial", "both routes"/"both booking routes kept open"; close, not identical |
| `pre-opinion-en_GB-r1` | A | 3 recorded |  | #429 | Fixed — Byline in the wrong place | describes a genre preference as a defect; the description of what changed is correct |
| `pre-opinion-en_GB-r1` | B | 1 claim account | changed |  | [section 3 subheading] now calls for measuring staff time ... | does not report the narrowing to "staff" time or the change to an imperative |
| `pre-opinion-en_GB-r1` | B | 4 omission |  |  | — (nothing the reply says) | does not mention that the "on the table" echo in the final paragraph is lost |
| `pre-opinion-en_GB-r1` | B | 3 recorded |  | #429 | [defects named for the byline and both subheadings] | placement is taste; "motive" defect contestable; a heading that previews its section is normal |
| `pre-opinion-en_GB-r2` | A | 3 recorded |  | #429 | a reader skimming the headline couldn't tell the piece is about booking venues | overstates what is a working shorthand |
| `pre-opinion-en_GB-r2` | A | 4 omission |  |  | — (nothing the reply says) | does not mention that the headline change breaks the echo of the body's wording |
| `pre-opinion-en_GB-r2` | A | **2 counted** | round |  | All the sentences that limit the claims are unchanged | two sentences carrying limiting clauses each had one word changed ("channels" to "routes"); read literally "unchanged" is wrong |
| `pre-opinion-en_GB-r2` | B | **2 counted** | round |  | All the sentences that limit the claims are unchanged, including ... the disclaimer about the administration's motives | inaccurate: the disclaimer sentence changed ("channels" to "routes"), though its limit did not |
| `pre-opinion-en_GB-r2` | B | 3 recorded |  | #429 | [finding 3's reason for the headline] | a taste judgement presented as a defect |
| `pre-control-article-clean` | A | 1 claim account | changed |  | Nu: Björkskolans mätvärden behöver läsas mot rummens användning. Det är en rekommendation | does not mention that the recommendation is Rask's or that it dropped the "innan styrningen ändras" condition |
| `pre-control-article-clean` | A | 3 recorded |  | #429 | Rubriken upprepade ingressens andra mening (åtgärdat); Inledningsstycket lovar något om givarnas placering som texten aldrig följer upp | both findings are false positives on a conforming text; the change is not a defect repair |
| `pre-control-article-clean` | B | 1 claim account | changed |  | en rekommendation med samma styrka som textens egen uppmaning | less accurate: does not admit that the headline no longer carries the result |
| `pre-control-article-flawed` | A | 1 claim account | changed |  | [Uppgiften om sex klassrum] finns kvar ordagrant i brödtexten, nu sist i första stycket | the small implicit attribution effect of the move is not mentioned |
| `pre-control-article-flawed` | B | 1 claim account | changed |  | [same entry] | the slight attribution drift from the new position is not mentioned |
| `pre-control-case-study-clean` | A | 1 claim account | changed |  | [Rubriken] påstår nu att Elm Quays arbetsledare ser nytta ... vilar på Linds egna ord | partly inaccurate: does not report the loss of the qualification the same sentence puts on that benefit |
| `pre-control-case-study-clean` | A | 3 recorded |  | #429 | beskrev en åtgärd i stället för kundens nytta; [scope overclaim] | taste reasons presented as defects; the scope overclaim is resolved by the standfirst's first sentence |
| `pre-control-case-study-clean` | B | 1 claim account | changed |  | [same entry] | accurate but incomplete: the preparation caveat left out of the headline is not mentioned |
| `pre-control-column-clean` | A | 3 recorded |  | #429 | [Rubriken] ... överdrev vad mallen innehåller | reads a deliberate figure of speech as a factual overclaim; the change is described correctly but the finding is not a defect |
| `pre-control-web-copy-clean` | A | 3 recorded |  | #432 | Åtgärdat: svarstiden stod bara i underrubriken ... Den som läste avsnittet utan rubriken fick därför inte veta när svaret kommer | the defect label is wrong; the reply describes the edit accurately but misclassifies its nature |

### Candidate arm, first wording (`12a1c7d2`)

| Run | Judge | Class | Kind | Owner | The reply | The judge |
| --- | --- | --- | --- | --- | --- | --- |
| `post-column-sv-r1-a` | B | 3 recorded |  |  | ett svenskt tankstreck med mellanslag (–) | small imprecision: the em dash already had spaces, so "med mellanslag" describes the result, not a change |
| `post-column-sv-r2-a` | A | 1 claim account | added |  | Borttagna eller tillagda påståenden: inga | less accurate: holds only if the headline's new normative claim counts as a change rather than an addition, which is how the reply frames it |
| `post-column-sv-r2-a` | A | 3 recorded |  |  | En rättning gjordes och godtogs | nothing in the two files shows who accepted it |
| `post-column-sv-r2-a` | A | 3 recorded |  | #429 | Rubriken ... gick inte att förstå utan att läsa texten | the old headline presented as a defect; the report of what changed is accurate |
| `post-column-sv-r2-a` | B | 3 recorded |  | #429 | gick inte att förstå utan att läsa texten; upprepade dessutom första styckets formulering | its justification is not accurate as a defect claim: a taste judgement, and a deliberate echo |
| `post-opinion-en_GB-r2-a` | A | 3 recorded |  |  | Changed (headline, finding 2): the headline now says what should be kept ... telephone booking of venues | accurate description, but overstates the edit by calling it a claim change (judge B: more cautious, not a misreport) |
| `post-opinion-en_GB-r2-a` | A | 3 recorded |  | #429 | [headline] didn't say what was being kept; [byline] read like a caption | judgements of taste presented as defects |
| `post-opinion-en_GB-r1-a` | A | **2 counted** | finding | #429(change) | [the old subheading] also said nothing about the rest of the section | overstated: "something to measure" pointed at the measuring the section describes |
| `post-opinion-en_GB-r1-a` | B | **2 counted** | finding | #429(change) | the same statement as the row above | partly inaccurate: its third element, "something to measure", does refer to the rest of the section |
| `post-opinion-en_GB-r1-a` | A | 3 recorded |  | #429 | Byline in the wrong place | the Skill's framing of a convention, not a visible defect |
| `post-opinion-en_GB-r1-a` | B | 3 recorded |  |  | readers met the argument ... without knowing who was making it until the last line | overstates the problem: section 3 names Öppna beslut as the proposer |
| `post-column-sv-r1-b` | A | **2 counted** | round |  | Resten av texten är orörd. | contradicted by the dash change; the reply reports the dash at its end, so it contradicts itself |
| `post-column-sv-r1-b` | B | **2 counted** | round |  | Resten av texten är orörd. | a small inconsistency: the closing paragraph corrects it by listing the dash |
| `post-column-sv-r1-b` | A | 1 claim account | changed |  | Rubriken säger nu att bibliotekets mötesmall har rutor för allt utom poängen | never says outright that the singular became a plural |
| `post-column-sv-r1-b` | B | 1 claim account | changed |  | the same statement as the row above | does not mention that "en ruta" became plural |
| `post-column-sv-r1-b` | B | 4 omission |  |  | — (nothing the reply says) | says nothing about the lost echo of "ännu en ruta" |
| `post-column-sv-r1-b` | A | 3 recorded |  |  | ett svenskt tankstreck med mellanslag (–) | describes the result correctly, though the input already had the spaces |
| `post-column-sv-r2-b` | A | 3 recorded |  |  | ett svenskt med mellanslag (–) | "med mellanslag" could be read as saying spaces were added; the resulting form is described correctly |
| `post-column-sv-r2-b` | B | 3 recorded |  |  | the same statement as the row above | a minor imprecision, not a misreport |
| `post-column-sv-r2-b` | A | 3 recorded |  | #429 | Rubriken (åtgärdat) ... så vag | disagrees with the "repair" label; the reply does not misstate what changed |
| `post-column-sv-r2-b` | B | 3 recorded |  | #429 | the same statement as the row above | presents the change as the repair of a defect, which the judge does not accept |
| `post-opinion-en_GB-r1-b` | A | 3 recorded |  |  | The standfirst didn't say which council | not accurate as a diagnosis: the title directly above names Lervik (the paragraph itself did not) |
| `post-opinion-en_GB-r1-b` | A | 3 recorded |  | #429 | [byline] with the author still unnamed | treats a convention as a defect |
| `post-opinion-en_GB-r1-b` | A | 1 claim account | changed |  | The section 3 subheading now says the proposal is to measure staff time ... | does not mention that the heading is now an instruction or that it drops "voluntarily" |
| `post-opinion-en_GB-r1-b` | B | 3 recorded |  | #429 | [byline reason] | presents an ordinary end sign-off as a defect |
| `post-opinion-en_GB-r1-b` | B | **2 counted** | placement | #429(change) | This wording is drawn from the rest of the section | inaccurate: the reply's own later note shows that "staff time" comes from section 2 |
| `post-opinion-en_GB-r1-b` | B | 1 claim account | changed |  | [section 3 subheading entry] | does not report that "voluntarily" is gone from the heading's paraphrase, or that the heading became an imperative |
| `post-opinion-en_GB-r1-b` | B | 3 recorded |  |  | the body ... never says what the pilot tested | doubtful: section 1 says what the pilot covered and counted (it does not say what the pilot tested) |
| `post-opinion-en_GB-r2-b` | A | **2 counted** | finding |  | "It can adopt…", only made sense by reading the subheading, because the board was named nowhere else | false: the board is named in the lead and in section 4 |
| `post-opinion-en_GB-r2-b` | B | **2 counted** | finding |  | the same statement as the row above | inaccurate: the lead names the executive board and section 4 says "for the board to weigh" |
| `post-opinion-en_GB-r2-b` | A | 3 recorded |  |  | Changed, headline (repair 3) | over-classifies it as a changed claim, but describes the text correctly |
| `post-opinion-en_GB-r2-b` | B | 3 recorded |  | #429 | [byline] could read as a caption | a matter of taste, not a defect (and the headline over-reported as a changed claim) |
| `post-control-article-clean` | A | 3 recorded |  | #429 | [three findings: headline, lead repeats standfirst, placement never explained] | detection-side false positives; none changed the text |
| `post-control-article-clean` | B | 3 recorded |  |  | Leadens tredje mening upprepar standfirsten | the overlap is loose: a signpost, not a repetition of a result; at most taste |
| `post-control-article-flawed` | A | 1 claim account | changed |  | "medan" antydde ett samband ... Ordet är ersatt med "och"; Försökets längd och givarnas placering står nu som två fakta bredvid varandra, utan samband | does not mention the lost reading of simultaneity (chronology); accurate at the level it claims |
| `post-control-case-study-clean` | A | 1 claim account | changed |  | Ändrat, rubriken: påstår nu att Elm Quays arbetsledare ser nytta i en gemensam reparationslogg | does not say that the headline drops the condition in Lind's appraisal |
| `post-control-case-study-clean` | B | 1 claim account | changed |  | the same statement as the row above | does not say that the headline drops the qualification in her appraisal |
| `post-control-case-study-clean` | A | 1 claim account | changed |  | Ändrat, ingressen: anteckningarna anges nu som underhållsgruppens egna anteckningar från försöket | nearly accurate: the returned text does not say "egna"; nor does the list mention "gruppen" becoming "Elm Quays underhållsgrupp" |
| `post-control-case-study-clean` | B | 1 claim account | changed |  | the same statement as the row above | mostly accurate: the returned standfirst does not contain "egna" |
| `post-control-case-study-clean` | A | 1 claim account | changed |  | Ändrat, brödtextens första mening: målet är detsamma | does not mention that "få ut av" became "se … i" |
| `post-control-case-study-clean` | A | 3 recorded |  | #429 | Den bestämda formen ... sa att alla reparationsärenden samlades | the reason is questionable: a reading the text does not force |
| `post-control-case-study-clean` | B | 3 recorded |  | #429 | the same statement as the row above | not a visible defect: a definite form in a headline is ordinary and the standfirst gives the scope at once |
| `post-control-opinion-clean` | A | **2 counted** | finding |  | Den bestämda formen "antagandet" pekade på ett antagande som bara rubriken nämner, eftersom varken inledningen eller något avsnitt talar om något antagande | false: the final section's closing sentence names it ("Ett antagande blir inte ett beslutsunderlag …") |
| `post-control-opinion-clean` | B | **2 counted** | finding |  | the same statement as the row above | false: the headline introduces "ett antagande" and the same section ends "Ett antagande blir inte ett beslutsunderlag …" |
| `post-control-opinion-clean` | A | 3 recorded |  |  | Texten följer artikelns anatomi utan avvikelser | wrong after the edit, measured against the 33–40-character range the frozen expectation reports (a description of the text, not an anatomy limit; the script reported no deviation) |
| `post-control-column-clean` | A | 1 claim account | added |  | Ny mellanrubrik: »Vad frågan är värd återstår att pröva« ... texten påstår därmed inget utöver det den redan gjorde | understates the change slightly: the heading turns the ending's hedge into a label for the section |
| `post-control-column-clean` | B | 1 claim account | added |  | the same statement as the row above | wrong: the heading is not neutral; it adds a new heading-level claim and separates "ändå" from what it answers |
| `post-control-column-clean` | B | 3 recorded |  |  | Avslutningen var inget eget avsnitt ... Den som skummade mellanrubrikerna hittade därför ingen avslutning | wrong: the ending was not missing; the section heading already announced the invitation |
| `post-control-column-clean` | B | 3 recorded |  | #429 | Rubriken sa mer än texten | misreads a column's deliberate hyperbole as an overclaim |
| `post-control-column-clean` | A | 3 recorded |  | #429 | the same statement as the row above | the premise that the headline was a defect is contestable; the change is described correctly |
| `post-control-web-copy-clean` | A | 3 recorded |  | #432 | Den som läste avsnittets text fick alltså inte veta svarstiden | inaccurate in presenting the change as a fix: treats the heading as if it were not part of what the reader reads |
| `post-control-web-copy-clean` | B | 3 recorded |  | #432 | the same statement as the row above | its reason for the change is wrong: treats the heading as outside the text a reader sees |
| `post-control-web-copy-clean` | A | 3 recorded |  | #432 | Meningen hänvisar till "formuläret" utan att texten innehåller formuläret, anger var det finns | a false positive: "formuläret" most plausibly means the page's own form |
| `post-control-web-copy-flawed` | A | **2 counted** | round |  | The paragraph explaining what the form does and doesn't do ... is word for word what it was. | literally false: that paragraph holds the changed "business days" |
| `post-control-web-copy-flawed` | B | 3 recorded |  |  | The one budgeted correction was accepted | the returned text contains the whole rebuild; every change is reported |

### Revise round, revised wording (`77dd847a`)

| Run | Judge | Class | Kind | Owner | The reply | The judge |
| --- | --- | --- | --- | --- | --- | --- |
| `revise-column-sv-r1-a` | B | 3 recorded |  | #429 | Den tidigare rubriken ... sa inte vilken mall det gällde | the input headline has no concrete visible defect; a definite-article teaser headline is ordinary column practice |
| `revise-column-sv-r1-a` | B | 3 recorded |  |  | ett svenskt tankstreck med mellanrum (–) | "med mellanrum" could be read as saying spaces were added; the input already had them |
| `revise-column-sv-r2-a` | A | 1 claim account | changed |  | Den nya säger att mötesmallen inte frågar varför vi behöver varandras tid | does not name the framing change: "hoppar över", and the wish stated as the template's omission |
| `revise-column-sv-r2-a` | A | 3 recorded |  | #429 | Rubriken – reparerad | calls the headline a repair of a defect; a matter of taste |
| `revise-column-sv-r2-a` | B | 3 recorded |  | #429 | Rubriken – reparerad | calls a taste judgement a repair; the report of the change is accurate |
| `revise-opinion-en_GB-r1-a` | A | 1 claim account | changed |  | [third subheading entry] | two effects go unreported: "the phone or the web" narrowed to "why people ring", and the added ordering word "First" |
| `revise-opinion-en_GB-r1-a` | A | 3 recorded |  | #429 | The byline was at the end | stated reason is a judgement of taste, not a visible defect |
| `revise-opinion-en_GB-r1-a` | B | 1 claim account | changed |  | the board should first find out what each route costs staff | does not mention the narrowing to "why people ring"; the gloss puts an actor on the finding-out that is neither in the heading nor in the body |
| `revise-opinion-en_GB-r1-a` | B | 3 recorded |  | #429 | The byline was at the end | frames a convention as a defect; the description of the change is correct |
| `revise-opinion-en_GB-r2-a` | A | **2 counted** | finding |  | The body didn't say whose proposal it was, or who "we" were | false: the input's body says "Öppna beslut proposes" |
| `revise-opinion-en_GB-r2-a` | B | **2 counted** | finding |  | the same statement as the row above | inaccurate: the input's body did say whose proposal it was ("Öppna beslut proposes") |
| `revise-opinion-en_GB-r2-a` | A | 3 recorded |  | #429 | Byline: it lacked the English byline form | overstates the problem: the byline worked as it was |
| `revise-opinion-en_GB-r2-a` | B | 3 recorded |  | #429 | the same statement as the row above | presents a matter of taste as a defect; the account of what changed is correct |
| `revise-column-sv-r1-b` | A | 1 claim account | changed |  | Rubriken säger nu att mötesmallen har en ruta för allt utom syftet | does not say that the change narrows or moves the sense of "poängen"; presents it only as a gain in clarity |
| `revise-column-sv-r1-b` | A | 3 recorded |  |  | ett svenskt tankstreck med mellanslag (–) | "med mellanslag" could suggest spaces were added; the resulting form is described correctly |
| `revise-column-sv-r1-b` | A | 3 recorded |  | #429 | Rubriken var otydlig på egen hand | the original headline shows no concrete visible defect; the rewrite follows a stand-alone-headline guideline |
| `revise-column-sv-r1-b` | B | 4 omission |  |  | — (nothing the reply says) | does not mention that the column's wordplay on "poängen" is lost |
| `revise-column-sv-r1-b` | B | 3 recorded |  |  | [same dash] | "med mellanslag" could suggest spaces were added; the input already had them |
| `revise-column-sv-r1-b` | B | 3 recorded |  | #429 | Den som ser rubriken i en lista kunde därför inte avgöra vad texten handlar om | no concrete visible defect: a teaser headline is ordinary for a column |
| `revise-column-sv-r2-b` | A | 1 claim account | changed |  | Brödtexten bär det påståendet | holds only by paraphrase: the body names the missing box as one for a decision |
| `revise-column-sv-r2-b` | A | 3 recorded |  | #429 | rubriken gick inte att förstå utan texten | the alleged defect is not visible in the input; an allusive column headline is a working voice choice |
| `revise-column-sv-r2-b` | B | 3 recorded |  | #429 | the same statement as the row above | a genre or anatomy preference, not a defect visible in the input |
| `revise-opinion-en_GB-r1-b` | A | 3 recorded |  |  | "the council executive board" didn't say which council; only the headline did | true, but leaves out that section 1 also names Lervik ("Lervik's residents"); what it calls a defect is not a real one |
| `revise-opinion-en_GB-r1-b` | A | 3 recorded |  | #429 | [third subheading] a list of nouns with no verb; repeated the first sentence under it | preferences, not defects |
| `revise-opinion-en_GB-r1-b` | B | 3 recorded |  |  | "Öppna beslut" (and the "We") appeared in section 3 without having been introduced | overstated: Öppna beslut is introduced where it first appears ("Öppna beslut proposes …") |
| `revise-opinion-en_GB-r1-b` | B | 3 recorded |  | #429 | the new heading states the author's demand, which the section's last sentence already makes | the last sentence is a condition, not a demand; its wording ("set the work each route costs staff against what it is worth") is in that sentence |
| `revise-opinion-en_GB-r1-b` | B | 3 recorded |  | #429 | a list of nouns with no verb | applies equally to the second subheading, which was kept; a preference, not a visible defect |
| `revise-opinion-en_GB-r2-b` | B | **2 counted** | count |  | The final text measures as follows: … no paragraph is over 65 words | the returned final paragraph is 66 words (65 in the input); the measuring script gives 66 on the returned text |
| `revise-opinion-en_GB-r2-b` | A | 3 recorded |  | #429 | [byline] read like a caption, not a byline | the description of the change is accurate; the reply frames taste as a defect |
| `revise-opinion-en_GB-r2-b` | B | 3 recorded |  | #429 | the same statement as the row above | "read like a caption" cannot be checked against the input; a taste change presented as a repair |
| `revise-control-web-copy-flawed` | A | **2 counted** | count |  | Seven headings became two | the input has seven headings (one H1, six H2s); the output has three (one H1, two H2s) |
| `revise-control-web-copy-flawed` | B | **2 counted** | count |  | the same statement as the row above | mixes two bases: seven counting the H1, or six H2s; after it there are three, or two H2s |
| `revise-control-web-copy-flawed` | B | 3 recorded |  |  | I made one correction | ambiguous beside "all six fixed"; it appears to mean one correction round |

## The shares

A run carries a counted miss where either judge records a class 2 miss in it. Every run that carries one carries exactly one distinct false statement.

| Reading | Runs carrying a counted miss | Share |
| --- | --- | --- |
| Pre-change arm | `pre-opinion-en_GB-r1`, `pre-opinion-en_GB-r2` | 2 of 14, 14.3% |
| Candidate arm, first wording | `post-opinion-en_GB-r1-a`, `post-column-sv-r1-b`, `post-opinion-en_GB-r1-b`, `post-opinion-en_GB-r2-b`, `post-control-opinion-clean`, `post-control-web-copy-flawed` | 6 of 18, 33.3% |
| Candidate arm, revised wording read in place of the first on the revised inputs | `revise-opinion-en_GB-r2-a`, `revise-opinion-en_GB-r2-b`, `revise-control-web-copy-flawed` | 3 of 18, 16.7% |

The revised reading's eighteen runs are the eleven revise runs and the first wording's seven runs on the inputs the round did not revisit: `article-clean`, `article-flawed`, `case-study-clean`, `case-study-flawed`, `column-flawed`, `opinion-flawed` and `web-copy-clean`. None of those seven carries a counted miss.

## The Target

**Missed, on both wordings.**

- **The share.** The first wording's share, 6 of 18, is higher than the pre-change arm's 2 of 14. The revised reading's share, 3 of 18, is 16.7% against 14.3%, which is not lower.
- **No false count, length, label, placement or round statement about the delivered text.** Both wordings miss this clause.
  - First wording: *Resten av texten är orörd* (`post-column-sv-r1-b`, a round), *This wording is drawn from the rest of the section* (`post-opinion-en_GB-r1-b`, a placement), and *is word for word what it was* (`post-control-web-copy-flawed`, a round).
  - Revised reading: *no paragraph is over 65 words* (`revise-opinion-en_GB-r2-b`, a count), and *Seven headings became two* (`revise-control-web-copy-flawed`, a count).

The revised wording's paragraph did what it was written for. No revise run said that a passage was unchanged, that the rest was untouched, or that a name stood nowhere else, where the text had an exception. What remains are two counts:

- `revise-opinion-en_GB-r2-b` ran the measuring script on the final text after the mechanical pass. It printed only the output's `failures`, `norms` and `typical` fields, and then stated a paragraph maximum of 65 words. That figure came from its measurement of the text under review, before its round added a word to the last paragraph. The script gives 66 on the returned text.
- `revise-control-web-copy-flawed` counted seven headings before, including the H1, and two after, excluding it.

The third revise miss is a finding's description of the text as received: *The body didn't say whose proposal it was* (`revise-opinion-en_GB-r2-a`), where the input's body says *Öppna beslut proposes*.

## The Control

The Control is matched per input and per kind. The kinds are the sentence about the claims as a whole, a removed claim, a changed claim and an added claim. A class 1 miss counts unless the whose-miss rule assigns it to an open ticket, and no class 1 miss here is assigned to one.

| Input | Pre-change kinds | First wording | Revised wording |
| --- | --- | --- | --- |
| `column-sv-r1` | none | **changed** (`post-column-sv-r1-b`, both judges: the headline's *en ruta* → *rutor* not said) | **changed** (`revise-column-sv-r1-b`, judge A: the entry does not say that *poängen* → *syftet* moves the claim's sense) |
| `column-sv-r2` | changed | **added** (`post-column-sv-r2-a`, judge A: *Borttagna eller tillagda påståenden: inga* over a headline that adds a normative claim) | changed only, not new |
| `opinion-en_GB-r1` | changed | changed only | changed only |
| `opinion-en_GB-r2` | none | none | none |
| `column-clean` | none | **added** (`post-control-column-clean`, both judges: the new subheading called neutral while it adds a heading-level claim) | none (the text came back unchanged) |
| `opinion-clean`, `web-copy-flawed` | none | none | none |
| `article-clean`, `case-study-clean` | changed | `article-clean` none; `case-study-clean` changed | not revisited |
| `article-flawed` | changed | changed | not revisited |
| the other controls | none | none | not revisited |

The first wording misses the Control on `column-sv-r1`, `column-sv-r2` and `column-clean`. The revised reading misses it on `column-sv-r1` only. The pre-change run on that draft changed only the headline's subject and drew no class 1 miss. The two runs that missed also changed another word of it, *en ruta* → *rutor* and *poängen* → *syftet*, and their entries named the change without saying all it did. The wording under test does not touch what the claim account itemises, which #398 and #400 settled and this ticket puts out of scope. So this most likely reads as run-to-run variation in how far a headline was rewritten, and not as something either wording caused. It is recorded and filed as measured.

## The revise round, and which wording ships

The first wording missed both the Target and the Control. The inputs whose candidate runs carried a counted miss or a Control miss were:

- `column-sv-r1`, with both;
- `column-sv-r2` and `column-clean`, each with a Control miss;
- `opinion-en_GB-r1`, `opinion-en_GB-r2`, `opinion-clean` and `web-copy-flawed`, each with a counted miss.

One round was run on those seven inputs, eleven runs in all: two on each draft and one on each control, as many as each has in the candidate arm. It ran against the revised wording, committed as `77dd847a` before its install was staged.

The revised wording misses both the Target and the Control, so the ship rule compares the two wordings over the revised inputs. The first wording's runs on them carry a counted miss in 6 of 11. The revised wording's runs carry one in 3 of 11. **The revised wording ships.** It is the tree as committed, and nothing is reverted. As the readiness addendum settles, the `delivery.md` change and the Skill changes ship whatever the reading, and no decision record is written. The reserved number `0227` is left unused.

## Whose miss

The plan names the open tickets whose behaviour a run of these inputs can show: #429, #432 and #433. A closed ticket takes no miss.

- **#429**, a working heading rewritten as if the headline rules made it a finding. Most class 3 rows are recorded here. In them the judge accepts the reply's description of a headline, subheading or byline change and disputes only its framing as the repair of a defect. The class 2 misses marked *#429(change)* count here, and the rewrite each describes is recorded under #429.
- **#432**, `web-copy-clean`'s heading fact copied into the body, and a form link reported as missing. These are recorded under #432 in both arms: the *svarstiden stod bara i underrubriken* framing and the *formuläret* false positive.
- **#433** carries none of this evaluation's misses.
- **Filed from this evaluation.** These are every class 2 miss of the shipped wording's runs, and every class 1 or class 4 miss in the shipped reading that no open ticket carries. Each is its own `needs-triage` issue naming #435:
  - class 2: #451 (*The body didn't say whose proposal it was*), #452 (*no paragraph is over 65 words*) and #453 (*Seven headings became two*);
  - class 1: #454 (*poängen* → *syftet*), #455 (a column headline's framing change), #456 (*Brödtexten bär det påståendet*), #457 (*why people ring* and *First*), #458 (*medan* → *och*'s chronology), and #459, #460 and #461 (`case-study-clean`'s headline condition, its *egna*, and *få ut av* → *se … i*);
  - class 4: #462 (the lost play on *poängen*).

  The shipped reading is the eleven revise runs and the first wording's runs on the seven inputs not revisited. The pre-change arm's class 1 and class 4 misses, and the first wording's on the revised inputs, belong to wordings that did not ship. They are recorded above and not filed.

## What the shared sentence reaches

`grep -l 'references/delivery.md' skills/editorial/*/SKILL.md` names the same five Skills at `<start>` and on this branch: Brief, Proofread, Redline, Unslop and Write. The shared section reaches all five, because each delivers by `delivery.md`.

- **Redline** alone was changed and measured.
- **Unslop** was changed, with its step 9 pointing at the section and its help page stating the duty, but not run.
- **Write, Proofread and Brief** are reached without being changed or run. Nothing here says how their replies fare under the section.

## Also recorded: `R1` and `C1`

Recorded as the judges gave them, and not scored; the pairs are judge A / judge B.

- **Drafts, `R1`.**
  - Pre-change: pass / pass on `column-sv-r1` and `opinion-en_GB-r2`, and fail / fail on the other two.
  - First wording: split or failing on five of its eight draft runs.
  - Revise round: fail / fail on all six column and `opinion-en_GB-r1` runs, and pass / pass on both `opinion-en_GB-r2` runs.
  - The failures are #429's working headings and subheadings reworded.
- **Controls, `C1`.**
  - Pre-change: pass / pass on 6 of 10. `article-clean`, `case-study-clean`, `column-clean` and `web-copy-clean` fail.
  - First wording: pass / pass on 6 of 10. `article-clean` passes, and `opinion-clean` fails on its *antagandet* change, beside `case-study-clean`, `column-clean` and `web-copy-clean`.
  - Revise round: pass / pass on all three controls, `column-clean`, `opinion-clean` and `web-copy-flawed`.

Neither criterion is this ticket's.

## Side effects

`O1` is met on all forty-three counted runs, and `S1` with it. Each packet's `filesystem-changes.json` is computed from the runner's before-and-after inventories of the run's private root. It shows no created, removed or changed path outside the Harness's own configuration directory and the caches. `work/input.md` is unchanged, nothing was created beside it, and the staged Skills are byte-identical before and after. The runner removed every private root (`cleanup.json`).

Scopes 3 to 5 were read around each wave, into `runs/wave-<n>-before-*.txt` and `runs/wave-<n>-after-*.txt`. Wave 1 is the pre-change arm, wave 2 the candidate arm, wave 3 the revise round's first attempt, and wave 4 the six void runs made again. Every change they show is attributed by path, and none is a run's:

- **Wave 1.** This working tree's `HEAD` moved to the builder's own candidate commit.
- **Wave 2.** The main checkout's `HEAD` moved from `e7773344` to `96e6b3b1`: the run integrated #432 into its branch. The session scratchpad gained or changed four files named for #432's gate, integration, metrics and verification.
- **Wave 3.** The session scratchpad gained two resume briefs, one for #429 and one for #435, written by the orchestrating session after the interruption.
- **Wave 4.** No change in the repository or the session scratchpad.

The scratch root's after-listings hold this build's packets, logs, driver scripts and judge bookkeeping, and nothing else. No judge's directory held anything but its two inputs and its judgement when it was collected, and each was removed once its judgement was copied. Before the interruption, the build kept byte copies of the two briefs for its judges under a neutral temporary path, and `cmp` finds them identical to the briefs beside this file. After it, each judge was given the brief's text, unchanged, in the message that dispatched it.

## What is not measured

- Unslop receives the change and is not run. Write, Proofread and Brief are reached by the shared section and neither changed nor run.
- `T1` and `R2` are `skipped`. Every packet keeps its trace, so they can be judged from it later.
- `A1`, `N1`, `N2`, `C2`, `F1`, `G1`, `G2`, `P1`, `W1`, `L1`, `L2` and `T2` are `skipped`, because `A2`, `O1` and `S1` are this evaluation's criteria.
- A clean control was run once per arm, to a response target, as the plan declares. The protocol's file-target run was not made.
- The *med mellanrum* / *med mellanslag* note, which the triage comment puts out of scope, recurs in both arms and is recorded as class 3.
