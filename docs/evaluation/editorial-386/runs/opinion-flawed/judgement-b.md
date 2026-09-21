# Judgement B — `opinion-flawed`

## Changes

1. **Headline.** Before: `Kommunledningen hatar människor`. After: `Telefonbokningen bör finnas kvar ett halvår till`. Repair of a visible defect *and* a change to what a claim says: the assertion that the leadership hates people — which the text carries nowhere — is gone, replaced by the position the lead already states, at the same modality (`borde` → `bör`).
2. **Standfirst added.** Before: absent. After: `Ett pilotförsök i kommunen har gett 120 bokningar, en invändning från förvaltningen och en rapport som pekar ut sina egna luckor. Öppna beslut går igenom vad underlaget om webb- och telefonbokning bär, var det tar slut och vad kommunen behöver mäta för att veta mer.` Repair of a visible defect (a required part was missing; `anatomy-input.json` `failures[0]`: `part: standfirst`, `measured: absent`). Built from figures the text already carries — 120 is the text's own 96 and 24 — and from the byline's organisation.
3. **Byline position.** Before: directly under the headline. After: under the standfirst. A consequence of change 2, not an independent edit; the byline text `Sanna Ek, Öppna beslut` is unchanged (both JSONs, `parts.byline`).
4. **Lead, second sentence removed.** Before: `Alla vet att politikerna vill stänga ute äldre för att spara miljoner.` After: nothing. Repair of a visible defect and a removal of claims: empty authority (`Alla vet`), an invented motive (shutting out the elderly), an invented purpose (saving money) and an invented magnitude (`miljoner`), none of which the text supports. Lead falls from 24 words to 12 (`parts.lead.words`).
5. **First subheading.** Before: `Bakgrund`. After: `Siffrorna säger inte hur många personer som står bakom`. Repair of a visible defect: a bare label becomes a statement of its own section's point.
6. **The proportion claim.** Before: `Det bevisar att 20 procent av kommunens invånare inte kan använda internet.` After: `Var femte bokning gjordes alltså per telefon.` A change to what the claim says — subject (inhabitants → bookings), scope (the municipality's population → the 120 bookings) and modality (`bevisar` → `alltså`). The proportion itself is unchanged and arithmetically sound against the text's 24 of 120.
7. **Second subheading.** Before: `Diskussion`. After: `Kostnaden för två bokningsvägar är inte räknad`. Repair of a visible defect, as change 5.
8. **Cost inference removed.** Before: `Därför kostar det ingenting att behålla telefonbokningen.` After: nothing. Repair of a visible defect and a removal of a claim: the conclusion did not follow from the missing time measurement, and it contradicted the section's own closing sentence `Försökets kostnad är inte beräknad.`
9. **Referent named.** Before: `Föreningen vill att förvaltningen mäter…`. After: `Föreningen Öppna beslut vill att förvaltningen mäter…`. Repair of a visible defect — the body's bare `Föreningen` had no antecedent outside the byline. No new fact; the name comes from the byline.
10. **Ending.** Before: `Nu är det dags att agera.` After: `Det är kommunstyrelsen som kan säga ja till halvårsförsöket i alla sju lokaler, och till att tidsåtgången mäts och användarna tillfrågas under tiden.` Repair of a visible defect: the exhortation named no act and no actor; both the act and the actor are taken from the lead and the body.

Nothing else differs. The three sentences that state what the evidence does *not* show, the figures 96 and 24, the proposal, and the administration's objection stand verbatim.

## Headings

### Input

- `# Kommunledningen hatar människor` — **statement**, **overclaim** (no sentence in the text says anything about the leadership's feelings or intentions)
- `## Bakgrund` — **label**
- `## Diskussion` — **label**

### Returned text

- `# Telefonbokningen bör finnas kvar ett halvår till` — **statement**
- `## Siffrorna säger inte hur många personer som står bakom` — **statement**
- `## Kostnaden för två bokningsvägar är inte räknad` — **statement**

No returned heading carries **colon**, **question**, **echo** or **overclaim**. On echo: the standfirst opens `Ett pilotförsök…` and shares no phrasing with the headline; the first sentence under each H2 (`Det gjordes 96 bokningar…`, `Förvaltningen invänder…`) shares no phrasing with its heading. The second H2 is close in wording to its section's *last* sentence, `Försökets kostnad är inte beräknad.`, which is not what the echo mark covers and which does no reader harm — the heading answers what the section is for before the reader enters it.

## Against the expectation

- **Detect unsupported motives** — detected and repaired. The lead sentence `Alla vet att politikerna vill stänga ute äldre för att spara miljoner.` is gone (change 4) and the account's second bullet under *Borttagna påståenden* names all three unsupported limbs; the headline's motive claim is gone too (change 1, first bullet).
- **Detect the population inference contradicted by the booking denominator** — detected and repaired. `Det bevisar att 20 procent av kommunens invånare…` became `Var femte bokning gjordes alltså per telefon.` (change 6), and the account explains the denominator correction explicitly.
- **Detect the cost contradiction** — detected and repaired. `Därför kostar det ingenting…` removed (change 8); the account names both the broken inference and the contradiction two sentences later.
- **Detect the vague final exhortation** — detected and repaired. `Nu är det dags att agera.` became a named act with a named actor (change 10).
- **Anatomy: no standfirst** — detected and repaired. `anatomy-input.json` `failures` holds exactly one entry, `standfirst … measured: absent`; `anatomy-delivered.json` reports `conforms: true`, `failures: []`, with `parts.standfirst.words: 45` and `paragraphs: 1`.
- **Anatomy: `Bakgrund` and `Diskussion` label rather than describe** — detected and repaired (changes 5 and 7). Both new subheadings are within the counted limit: 54 and 46 characters (`anatomy-delivered.json`, `parts.sections[*].subheading.characters`).
- **Anatomy: no ending section, the closing exhortation inside the last one, naming no act** — the naming is repaired; the placement is not. The closing sentence is still the last section's second paragraph (`anatomy-delivered.json`, `parts.sections[1].paragraphs[1]`), but the script reports the delivered text as `conforms: true` with no failure and no norm departure, so on the measurement this is not a counted failure, and the expectation's own remedy — "Existing action/actor in body can repair the ending" — is what the run did.
- **Keep qualified facts and the proposal** — preserved. `Kommunens pilotrapport från den 8 april 2026 säger samtidigt att bokningarna inte räknar unika personer och att digital vana inte undersöktes.`, `Handlingarna saknar tidsmätning.` and `Försökets kostnad är inte beräknad.` stand word for word, as does the proposal `Kommunstyrelsen borde behålla telefonbokning under ett halvårs försök i alla sju lokaler.`
- **Findings the expectation rejects** — none. Every finding the run acted on is one of the items above.

## G1 — pass

The genre does its job. The returned text puts its position in the lead — `Kommunstyrelsen borde behålla telefonbokning under ett halvårs försök i alla sju lokaler.` — and keeps one recognisable angle throughout: the material does not yet answer the question the decision turns on. A reader interested in the municipal decision learns what the pilot measured (`Det gjordes 96 bokningar på webben och 24 via telefon`), what it explicitly did not (`bokningarna inte räknar unika personer och … digital vana inte undersöktes`), and what the administration objects (`dubbla kanaler innebär dubbel administration`). The craft the genre asks for is present and, where the input faked it, the run stopped faking it: the piece now argues from an acknowledged gap in the evidence rather than from `Alla vet`.

## G2 — pass

All parts are present in order, and `anatomy-delivered.json` reports `conforms: true` with `failures: []`. Each does its own job. Headline: states the angle and claims no more than the lead (`bör finnas kvar ett halvår` against the lead's `borde behålla … under ett halvårs försök`), 48 characters within the 20–70 requirement. Standfirst: stands alone at 45 words, inside the 60-word requirement, and promises exactly the three things the body delivers — what the material carries, where it stops, what must be measured. Byline: `Sanna Ek, Öppna beslut`, the author the text itself names, carried over unchanged; nothing was left unfilled or invented. Lead: one paragraph before the first H2 (`parts.lead.paragraphs: 1`), and it begins the work by stating the position. Sections: two, each with at least one paragraph, each headed by a statement of its own point. Ending: `Det är kommunstyrelsen som kan säga ja till halvårsförsöket i alla sju lokaler, och till att tidsåtgången mäts och användarna tillfrågas under tiden.` — the lead's expectation shown met.

For `opinion` in particular: the position is early (the lead, 12 words), the support is the booking split and the report's own stated gaps, the real objection is the administration's `dubbla kanaler innebär dubbel administration`, and the call to action is the stance itself addressed to an identifiable actor, `kommunstyrelsen`, which is the body that can grant it. The objection is not defeated — the text answers that the cost has not been calculated — but that is an honest handling of what the text carries, not a missing part.

## P1 — pass

The reasoning is now followable and the conclusions are proportionate to visible support. The chain is: 24 of 120 bookings came by phone → the material does not say how many people that is, because it counts bookings, not persons → the administration's cost objection cannot be weighed, because no time measurement exists and the trial's cost is not calculated → therefore run the trial six more months and measure. Each step is visible in the text. The two places where the input broke this are gone: the leap from bookings to `20 procent av kommunens invånare` and the leap from a missing measurement to `kostar det ingenting`. Nothing is introduced before it is introduced — `pilotförsök`, `telefonbokning`, `webben` and `kommunstyrelsen` all arrive in the standfirst or the lead. The technical substance that matters — the two raw counts, the date of the pilot report, and the two named things to measure — all remains.

## W1 — pass

The reader can orient and enter. The headline gives the position, the standfirst gives the situation and the route, the two H2s let a scanner see the two arguments, and the continuous explanation survives between them. The body is complete when the standfirst is covered: the standfirst promises what the material carries, where it stops and what to measure, and the last paragraph of section two supplies the third. Standfirst and lead open on different first words (`Ett` / `Kommunstyrelsen`).

On the counts, `anatomy-delivered.json` reports `norms: []` — no paragraph over 80 words (the longest is 38, `parts.sections[0].paragraphs[0].words`), no section over three paragraphs (2 and 2 by `parts.sections`), no heading below the second level, and a headline of 7 words and 48 characters, inside both the 8-word and 60-character norms. The *most* statements are read across the whole text and are advisory: `typical.paragraphs_of_two_or_three_sentences` is 2 of `typical.paragraphs` 5, and `typical.sections_of_two_or_three_paragraphs` is 1 of `typical.sections` 2. The three paragraphs outside the two-or-three band are the lead and the ending, each one sentence by the anatomy's own design, and the four-sentence paragraph in section two. No reader loss follows from that rhythm; the script's own verdict on the text is `conforms: true`, and I do not turn a *most* statement into a failure against individual paragraphs.

## L1 — pass

The Swedish reads as Swedish written by a person. `Var femte bokning gjordes alltså per telefon.` is the idiomatic construction, not a translated `one in five of the bookings`. The cleft `Det är kommunstyrelsen som kan säga ja till …` is a natural Swedish emphasis. `en rapport som pekar ut sina egna luckor` is figurative but ordinary in Swedish reportage. `Siffrorna säger inte hur många personer som står bakom` keeps the Swedish subordinate `som`. Nothing in the added material — the standfirst, the two subheadings, the ending — shows English syntax or generic translationese, and the sentences carried over are untouched.

## L2 — pass

The locale is Swedish throughout and the run introduced no new factual date or conversion. The date form `den 8 april 2026` is Swedish and is the input's own, preserved verbatim. Numerals are unformatted integers (`96`, `24`, `120`) where Swedish separators do not arise. Headings are in sentence case with no terminal full stop, as Swedish practice has it. The one number the run added, 120 in the standfirst, is the sum of the text's own 96 and 24 and not a conversion. The removal of `20 procent` was a claim repair, not a mechanical one, so no locale mechanic was disturbed by it.

## R1 — pass

**Every removal and changed claim, against the account:**

- Headline claim that the leadership hates people (removed) — reported, first bullet of *Borttagna påståenden*, and accurately: it names where the claim sat and that the text asserts nothing about the leadership's feelings or intentions.
- `Alla vet att politikerna vill stänga ute äldre för att spara miljoner.` (removed) — reported, second bullet, and accurately: it separates the three limbs (motive, purpose, magnitude) and states that none appeared elsewhere in the text, which is true of `miljoner`.
- `Därför kostar det ingenting att behålla telefonbokningen.` (removed) — reported, third bullet, and accurately: both the non sequitur and the contradiction with `Försökets kostnad är inte beräknad.` are named.
- `20 procent av kommunens invånare` → `Var femte bokning` (changed claim) — reported under *Ändrade påståenden*, and accurately: it states that the proportion is unchanged, that the denominator moved from inhabitants to the 120 bookings, that `bevisar` is gone, and that nothing new about inhabitants or digital habit was added. All four hold against the delivered text.
- `Nu är det dags att agera.` → the named act and actor (changed claim) — reported, and accurately: the account claims no new proposal and no new addressee, and both the act and `kommunstyrelsen` are in the input's lead and body.
- `Föreningen` → `Föreningen Öppna beslut` (changed claim, referent) — reported, and accurately sourced to the byline.
- The rewritten headline and two subheadings, and the added standfirst — reported in the closing paragraphs, with the derivation of 120 from 96 and 24 stated outright.

No removal or changed claim is unreported, and no report misdescribes what happened.

**Voice, arguments, quotations and claims outside the findings:** preserved. The administration's objection, the two raw counts, the pilot report sentence with its date, `Handlingarna saknar tidsmätning.`, `Försökets kostnad är inte beräknad.`, the association's two requests and the proposal all stand — three of them verbatim, as the account's last paragraph claims and as comparison confirms. The register stays a civic-association opinion piece.

**Visible defects not addressed:** none of substance. What the run did not do is move the closing sentence out of the last section into an ending of its own; the script does not record that as a failure (`conforms: true`, `failures: []`), and the expectation's stated remedy for the ending was the act and actor, which the run supplied.

**Findings the expectation rejects:** none. The run made no finding against a requirement the text met, none against a *should* the text had reason to leave, and none from reading a *most* statement at a single paragraph or section. Nothing was rewritten to taste: each of the ten changes answers a defect visible in the input or a part the script measured as absent.

**No unavailable-source verification.** The standfirst and the ending are assembled only from material already in the text; the run at no point asserts something the text could not tell it. There are no irreparable findings left reported-but-unrepaired, and the delivered text carries no remaining quality problem that the reply attributes to missing material.
