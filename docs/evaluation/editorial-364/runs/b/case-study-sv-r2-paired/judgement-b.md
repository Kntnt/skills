# Judgement — case-study-sv-r2-paired (run b)

Input: `work/input.md`. Delivered: `delivered.md`. Reply: `response.md`.
Seven differences, listed exhaustively. Frontmatter, byline, ingress, all three body sections, all numbers and dates, the link and every hedge are byte-identical.

## 1. Every difference, input → delivered

| # | Before | After | Class |
|---|---|---|---|
| 1 | `# Elm Quay fick en gemensam bild av felanmälningarna` | `# Elm Quay testade en ärendelogg i två hus` | Repair of a visible defect **and** a change to what a claim says (strength and scope: a completed outcome for the company becomes a test in two houses) |
| 2 | `I september 2025 bestämde … att pröva en gemensam felanmälningslogg i två av husen.` | `I september 2025 beslutade … att på prov samla felanmälningarna från två av husen i en enda logg.` | Repair of a visible defect (the clause `en gemensam felanmälningslogg i två av husen` repeated the ingress word for word); claim content unchanged — same actor, same month, same trial, same two houses, same modality (`pröva`→`på prov`) |
| 3 | `## Leverantören konfigurerade, teamet bestämde kategorierna` | `## Underhållsteamet bestämde hur felanmälningarna skulle sorteras` | Repair of a visible defect (the heading said the section's first sentence and the quotation under it in advance) |
| 4 | `## Arbetsledaren skulle göra om testet med mer förberedelse` | `## Arbetsledarens omdöme kommer med villkor` | Repair of a visible defect (the heading said the quotation under it in advance, in near-identical words) |
| 5 | `— Vi ville att kvällsskiftet…` (U+2014) | `– Vi ville att kvällsskiftet…` (U+2013) | Mechanical: locale form — Swedish pratminus is the en dash |
| 6 | `— Vi lade mer tid…` (U+2014) | `– Vi lade mer tid…` (U+2013) | Mechanical: same locale form |
| 7 | `— Jag skulle välja…` (U+2014) | `– Jag skulle välja…` (U+2013) | Mechanical: same locale form |

Differences 5–7 are the only changes the reply does not report anywhere. They touch punctuation only, not a word of the quotations, and they move the text toward the Swedish convention rather than away from it.

## 2. Bridges into quotations (input order)

### Q1 — "Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort…"

- **Bridge before (input):** `Svale Systems konfigurerade loggen och utbildade sex medarbetare vid två tillfällen. Telefonanmälan behölls för de boende.` — **class (c)**: it carries `utbildade sex medarbetare vid två tillfällen` and `Telefonanmälan behölls för de boende`, neither of which is in the quotation.
- **Bridge after (delivered):** identical, word for word — **class (c)**, same words.
- **Speech tag:** `säger Maya Lind, arbetsledare för underhållet` — carries her role besides the attribution, so **class (b)** before and after; unchanged.
- **Heading standing above that paragraph:** changed (difference 3). The input heading `Leverantören konfigurerade, teamet bestämde kategorierna` was itself **class (a)** toward this quotation — `teamet bestämde kategorierna` is `Kategorierna var våra` said first. The delivered heading `Underhållsteamet bestämde hur felanmälningarna skulle sorteras` still names the team as the decider but no longer hands over the quotation's own words; it leans **(a)/(b)**, nearer (b).
- **Reported?** Yes — "Åtgärdade fynd" bullet 3 names both halves (the verbatim `konfigurerade` echo and the heading saying the quotation's content in the writer's words).
- **New material supplied?** No. `sorteras` is a new word, not a new fact; the categories in a fault-report log are already in the text and in the quotation.
- **Lost?** `Leverantören konfigurerade` leaves the heading, but the body's own first sentence still says `Svale Systems konfigurerade loggen`, so nothing the quotation lacks is lost. The reply says exactly this, accurately.

### Q2 — "Vi lade mer tid på att enas om kategorierna än på att registrera de första anmälningarna…"

- **Bridge before (input):** none — the preceding paragraph is Q1 itself. Only the tag `säger hon` — **class (b)**, bare attribution.
- **Bridge after (delivered):** unchanged — **class (b)**.
- **Reported? / new material? / lost?** No change, so nothing to report, supply or lose.

### Q3 — "Jag skulle välja att göra testet igen. Att ha en samlad bild av anmälningarna hjälper oss, men jag skulle lägga in en extra vecka för förberedelser."

- **Bridge before (input):** the heading `## Arbetsledaren skulle göra om testet med mer förberedelse` stands immediately before the quotation with no narrative between — **class (a)**: `skulle göra om testet` is `Jag skulle välja att göra testet igen`, and `med mer förberedelse` is `en extra vecka för förberedelser`. The reader meets the quotation already told what it delivers.
- **Bridge after (delivered):** `## Arbetsledarens omdöme kommer med villkor` — **class (b)**: it names the subject (the supervisor's verdict) and the occasion of a reservation, without delivering the verdict.
- **Speech tag:** `säger Maya Lind` — bare attribution, **class (b)**, unchanged.
- **Reported?** Yes, twice and precisely: "Åtgärdade fynd" bullet 2 quotes both overlapping pairs, and remaining finding 3 concedes that the replacement now withholds the answer a heading should give.
- **New material supplied?** No. `omdöme` and `villkor` are the quotation's own "men"-clause plus `Lind rekommenderar inte Svale till alla bostadsföretag`; no event, name, figure or date enters the text.
- **Lost?** The input heading carried nothing the quotation does not carry, so nothing was lost with it.

## 3. The quotations themselves

All three came back with their wording, punctuation, semicolon, sentence order and internal hedges intact; only the leading dialogue dash changed form (differences 5–7), which is outside the quoted words.

- Q1: unchanged. Meaning, stance, certainty and Lind's voice (`Vi ville…`, `Kategorierna var våra`) survive; her role in the tag survives.
- Q2: unchanged. The comparison (`mer tid … än …`) and the forward-looking `skulle jag avsätta` survive.
- Q3: unchanged. The reservation `men jag skulle lägga in en extra vecka` and the conditional `skulle välja` survive intact.

The reply does not name the dash change. It is mechanical, it alters no quoted word, and it does not touch meaning, stance, certainty, reservation or voice.

## 4. R1 — **PASS**

Every defect it acted on is visible in the text without any source: a headline asserting a finished, company-wide outcome the body never supports; two headings that say their quotations before the reader reaches them; and a first body sentence repeating a seven-word run from the ingress. Nothing else was touched — no hedge softened, no quotation reworded, no number, date, name or link altered, and no working sentence rewritten to taste. The clean second section was left entirely alone.

**Removals and changed claims, and how the reply reports them:**

- *Headline claim removed* (`fick en gemensam bild av felanmälningarna`): reported, under "Påståenden", as the one claim that changed, with the reason and the new scope. Accurate on substance, with one overstatement — the reply says the old claim "finns inte kvar någonstans i texten", whereas Lind's quotation still says `Att ha en samlad bild av anmälningarna hjälper oss`. What genuinely disappeared is the completed, company-wide framing, not the idea of a shared view. The direction of the reporting is right; the wording is a shade too absolute.
- *`Leverantören konfigurerade` removed from heading 1*: reported, and reported accurately — the fact stands unchanged in the section's first sentence and in Lind's quotation.
- *Heading 3's paraphrase of the quotation removed*: reported, with the overlapping words quoted, and the cost of the replacement conceded as a new finding.
- *First body sentence reworded*: reported as finding 4, with the repeated phrase quoted. No claim moved.
- *Dialogue dashes*: **not reported**. A legitimate locale correction, but an unreported change; the sole reporting gap in the run.

**Irreparable finding:** remaining finding 1 (no denominator for `två av husen`, and the flat count in the ingress the body may not lean on) is correctly classed as needing material the Skill never had, and it is not used to excuse any change.

**Self-created defects:** the reply raises both itself — `ärendelogg` appearing only in the new headline against `felanmälningslogg`/`loggen` everywhere else, and heading 3 now withholding the verdict — and stops rather than spending a further round repairing its own repair. The account matches the delivered file in every particular I could check.
