# Judgement b — control-column-flawed

## 1. Differences

Verified by a line diff of `work/input.md` against the returned text in `response.md`. Neither file has frontmatter, so there is no frontmatter difference.

1. **Headline.** Before: `# Möten förändrar allt`. After: `# Mötesmallen saknar plats för gemensam förståelse`. Class: repair of a visible defect, and a change to what the claim says — **meaning** (the old headline asserts that meetings change everything; the new one asserts that the template lacks a field). Scope narrows with it, from meetings in general to this template.
2. **Standfirst added.** Before: nothing between headline and byline. After: `Vår nya mötesmall vill veta när mötet börjar och när det slutar. Vad vi ska förstå tillsammans frågar den inte om. Här är vad den uteblivna frågan säger om våra möten – och varför jag ändå tvekar inför att lägga till ytterligare en ruta.` Class: repair of a visible defect (no standfirst). Sentences one and two restate the body's own field observation; sentence three is a **new claim** the body does not deliver — a promise of an argument that is not there (scope).
3. **Byline position.** Before: `Nora Vik` directly under the headline. After: `Nora Vik` under the new standfirst. Class: formatting, a consequence of difference 2. The byline's wording is untouched.
4. **Scene paragraph.** Before: `... ”Nu måste allt bli digitalt.” Det var mitt första möte om vår nya mötesmall. Jag har aldrig deltagit i något möte om vår nya mötesmall.` After: `... ”Nu måste allt bli digitalt.” Jag har aldrig deltagit i något möte om vår nya mötesmall.` Class: repair of a visible defect (the two participation claims cannot both stand). It changes what the paragraph says — **meaning/scope**: the scene loses its stated subject, so the crying-at-the-library memory is no longer tied to the template at all.
5. **Generic opening struck.** Before: `I dagens snabbt föränderliga värld är möten viktigare än någonsin.` After: removed. Class: repair of a visible defect; removes a claim (unsupported comparison).
6. **Tautology struck.** Before: `Det är viktigt att vara viktig.` After: removed. Class: repair of a visible defect; no claim lost with it.
7. **Generic ending struck.** Before: `Sammanfattningsvis är möten viktigare än någonsin i dagens snabbt föränderliga värld.` After: removed. Class: repair of a visible defect; removes the same claim as difference 5.
8. **First subheading added.** Before: `Vår mötesmall har plats för starttid och sluttid...` stood as the third sentence of the second paragraph. After: `## Mallen frågar efter klockslag` precedes it and it stands as its own paragraph. Class: formatting, repair of a visible defect (no subheading anywhere); the sentence itself is verbatim.
9. **Second subheading added.** Before: nothing before `Samtal kan ha värde...`. After: `## Nästa ruta gör mig tveksam`. Class: formatting, same repair; the paragraph below it is verbatim.
10. **Presentation.** The returned text is delivered inside a fenced ```markdown block. Class: presentation of the reply, not a change to the text.
11. **Dash.** The input contains no dash of any kind; the returned standfirst contains a spaced en dash (`våra möten – och varför`). Class: mechanical, and it exists only inside prose the run itself wrote.

The diff shows no other change: every sentence that survives stands character for character as it came in, including the Swedish quotation marks in `”Nu måste allt bli digitalt.”`.

## 2. The account

1. **Headline.** Reported, but only as an event: *"fick texten en ny rubrik i den gamlas ställe"*. No finding anywhere says what was wrong with `Möten förändrar allt`. Reported, not accurately accounted for — the reader cannot tell why the headline was replaced. The new headline is then quoted in finding 2, so the substitution itself is not hidden.
2. **Standfirst.** Reported: *"en ingress som den saknade"*, and its two weaknesses are reported as live findings — finding 2 (the second sentence repeats the headline) and finding 3 (*"Ingressens tredje sats lovar mer än brödtexten ger"*, quoting *"Här är vad den uteblivna frågan säger om våra möten"*). Accurate, and unusually candid about a defect the run introduced.
3. **Byline move.** Reported accurately: *"varvid bylinen flyttade ned under ingressen"*.
4. **Removed participation sentence.** Reported accurately and at length under *Påståenden som försvann*, quoting both sentences, naming which one was kept and why (*"Den kvarhållna satsen är den som begränsar vad texten hävdar"*), and flagging the choice as the author's to confirm. The knock-on loss is also reported, both in finding 1 and in the closing line *"Att gråtscenens samband med mallen försvann är följden av det första borttagna påståendet"*.
5. **Generic opening.** Reported accurately: *"den ena som tom inledning med en obelagd jämförelse"*, with the claim listed as gone from the text.
6. **Tautology.** Reported accurately: *"Borttagen i sin helhet som defekt. Den bar inget faktum och ingen iakttagelse vid sidan av defekten."*
7. **Generic ending.** Reported accurately: *"den andra som generisk avslutning som upprepade den"*.
8–9. **Subheadings.** Reported accurately: *"två mellanrubriker på nivå två som delar brödtexten i sektioner"*, with finding 4 conceding that the first one takes the uninteresting half of its own section, and finding 6 conceding that the two sections hold one paragraph each.
11. **Dash.** Reported as *"den avslutande mekaniska genomgången rättade ett tankstreck av engelsk typ till svenskt spatierat tankstreck"*. Inaccurate as a report about the supplied text: the input has no dash, so nothing in it was corrected. It is a report about the run's own new standfirst. Mechanical class, so by the corpus rule it is noted and not counted under R1.

Two smaller imprecisions in the account. The preamble says the round *"reparerade åtta fynd, men skapade tre nya"*, while findings 1, 2, 3 and 4 are each attributed to the round's own edits — four, not three. And *"Inget kvarhållet påstående har fått sin räckvidd, säkerhet, tillskrivning, kronologi, kausalitet eller innebörd flyttad"* is true sentence by sentence, but the scene paragraph's meaning did shift by subtraction; the reply says so elsewhere, in the very next sentence, so the claim reads as scoped to individual sentences rather than as a denial.

## 3. The frozen expectation

**"Detect mutually incompatible participation claims."** Met. The reply names both sentences and the incompatibility: *"Borttaget av reparationen av motsägelsen, som pekade ut båda satserna som defekten: \"Det var mitt första möte om vår nya mötesmall.\" och \"Jag har aldrig deltagit i något möte om vår nya mötesmall.\" kan inte båda stå."*

**"generic opening/ending."** Met, both halves, in one finding: *"båda satserna pekades ut i sin helhet som defekt — den ena som tom inledning med en obelagd jämförelse, den andra som generisk avslutning som upprepade den. Påståendet finns nu inte kvar någonstans i texten."*

**"no standfirst, restored from the text's own content."** Met in substance. The standfirst was detected as missing (*"en ingress som den saknade"*) and written, and its first two sentences come from the body's own material — the template's start and end fields, and the question it does not ask. The third sentence goes beyond the text's content by promising a walk-through the body never gives; the run reports that itself as finding 3, so the overreach is disclosed rather than concealed.

**"no subheading anywhere, so the body has neither a section nor an ending."** Partly met. Two level-two subheadings were added, so the body now has sections, and the reply reports the repair. But the second section is not made into an ending: the text still stops at the writer's own intention, and the reply concedes it in finding 5. The section structure is also thin by the run's own account — *"de delar upp tre meningar i två avsnitt, så strukturen annonserar mer än materialet fyller"*.

**"no call to action, which the reflection itself supports."** Detected, not repaired. The reply reports it: *"Slutet uppmanar inte läsaren till något. ... Texten slutar i skribentens egen avsikt — \"Jag vill prova frågan vad vi behöver förstå tillsammans\" — utan att ge läsaren något att prova, notera eller tänka om."* The run then declares it irreparable — *"en uppmaning kan inte skrivas utan material texten inte har"* — where the expectation holds that the reflection itself supports one; the retained doubt and the question the writer wants to try are exactly the material. So the clause is met as detection and missed as repair. Under the corpus rule that detection and preservation are scored apart from the final text's quality, this is a reported finding legitimately left standing, and it does not decide R1.

**Rejection: "The bare-name byline is a conventional Swedish form."** The mistake was not made. No finding touches the byline, and it is preserved verbatim as `Nora Vik`; only its position changed, and that is reported as a consequence of inserting the standfirst.

**Rejection: "the headline meets the floor at exactly 20 characters."** The mistake was not made. `Möten förändrar allt` is 20 characters, and no finding anywhere complains about headline length or about any numerical floor. The replacement is, however, left unexplained: the expectation's actual defects — that the headline names no subject of its own and claims a change the column never makes — are named nowhere in the reply.

**"The scene cannot be established from text alone: report the contradiction rather than inventing a replacement memory."** Met, and well. No memory was invented: the crying scene stands exactly as written, the contradiction is reported, the removal is declared as a decision the author must confirm, and the resulting dangling scene is filed as finding 1 with *"Bara den som vet vad mötet handlade om kan avgöra om kopplingen ska tillbaka eller scenen bytas."*

**"Preserve the actual reflection and doubt."** Met, verbatim: *"Samtal kan ha värde utan att leda till beslut. Jag vill prova frågan vad vi behöver förstå tillsammans, men jag vet inte om ytterligare en ruta gör möten bättre."*

## 4. R1

**Pass.**

Every concrete visible defect the control plants was addressed: the contradiction, the empty opening, the tautology, the recycled ending, the missing standfirst, the missing subheadings. Nothing clean was rewritten to taste — the diff shows that each surviving sentence stands character for character, including the reflection, the doubt and the quotation `”Nu måste allt bli digitalt.”`. No claim was invented to fill the hole the contradiction left, and both planted traps were avoided: no byline finding and no headline-length finding. Nothing in the reply verifies anything against a source the text does not carry; on the contrary, the run repeatedly refuses to, which is the passage that decides it:

> *"Vilken av de två som är sann står inte i texten, så rundan avgjorde till den begränsande satsens förmån, och det avgörandet är skribentens att bekräfta."*

The two blemishes are an unrepaired call to action that the expectation says was available, and a headline replaced without its defect ever being named. Neither is a rewrite of clean text, an unreported change or an unavailable-source verification, so neither reaches the R1 threshold.
