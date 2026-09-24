# Judgement a

Files read: `work/input.md` and `response.md`, and nothing else. I compared them line by line with a diff and measured the lengths of the headline, the standfirst and the subheadings.

## 1. Differences

The text has no frontmatter. The byline, the body paragraphs, both quotations, the numbers, the disclosure sentence and the link are all unchanged. The returned text sits inside a ```markdown fence in the reply, which is how the reply presents it and is not a change to the text. There are four differences, on four lines:

1. **Headline.** Before: `# Elm Quay samlade reparationsärendena` (36 characters). After: `# Elm Quays arbetsledare ser nytta i samlade ärenden` (50 characters). Class: **change of taste** that also **changes what the headline claims**, in **meaning** and **attribution**. It used to report an action by the organization. Now it reports a favourable appraisal and attributes it to the supervisor. The appraisal also loses its condition: "ser nytta" drops the "men ... en vecka för förberedelser" half of what Lind said. The claim is backed by Lind's quote "hjälper oss", so it is not made up. The new headline is 14 characters longer than one the expectation says already meets its limit.
2. **Standfirst, sentence 2.** Before: `Arbetsledaren Maya Lind vill göra om försöket, men skulle avsätta` After: `Arbetsledaren Maya Lind skulle göra om försöket, men skulle avsätta` Class: **certainty** change. Stated intent becomes a conditional judgement. It is arguably closer to the quote "Jag skulle välja att göra försöket igen", but the input's "vill" was a fair paraphrase and was not a visible defect. The change also puts "skulle" in both halves of the sentence.
3. **Standfirst, sentence 3.** Before: `Här är vad gruppen gjorde, vad anteckningarna visar och vad hon skulle ändra.` After: `Här är vad Elm Quays underhållsgrupp gjorde, vad gruppens anteckningar från försöket visar och vad hon skulle ändra.` Class: **change of taste**, adding explicitness. What the sentence claims is unchanged. The standfirst grows from 40 to 45 words, and the expectation names 40 words as meeting its limit.
4. **Opening sentence of the body.** Before: `Att se samma information över skiftgränserna var vad underhållsgruppen på Elm Quay Housing ville få ut av sin gemensamma reparationslogg.` After: `Underhållsgruppen på Elm Quay Housing ville att alla skift skulle se samma information i en gemensam reparationslogg.` Class: **repair of a visible defect**, and a borderline one. The "Att X var vad Y ville få ut av" cleft reads as calqued English in Swedish. The meaning changes slightly: the goal of what the group wanted to "få ut av sin" log becomes a wish that the shifts see the same information "i en" log, and "över skiftgränserna" becomes "alla skift". Scope, certainty, attribution, chronology and causality are unchanged.
5. **Last subheading.** Before: `## Kunden vill ge förberedelserna mer tid` (38 characters). After: `## Maya Lind blickar tillbaka på försöket` (38 characters). Class: **change of taste** that also **changes meaning**. An informative subheading that carried the customer's decision and the qualification ("mer tid") becomes a label with no content. The qualification disappears from the headings a reader scans. The customer is still the actor, but she now looks back instead of deciding something.

There are no mechanical corrections.

## 2. The account

- Difference 1 is reported as correction 1 and again under "Påståenden som ändrats". The report is accurate about what changed and cites the quote as support. Its justification is not a defect in the text: "beskrev bara vad kunden gjorde, inte vad kunden fick ut av det" and "upprepade ingressens första mening". The reply does not mention that the headline grew from 36 to 50 characters, or that "ser nytta" drops Lind's reservation.
- Difference 2 is reported as correction 2 and listed as a claim change. The report is accurate.
- Difference 3 is reported as correction 3. The report is accurate, except that it does not mention the standfirst growing to 45 words.
- Difference 4 is reported as correction 4. The report is accurate as far as it goes. The small meaning shift ("få ut av sin" becoming "i en") is not listed among the claim changes, which is defensible because the substance holds.
- Difference 5 is reported as correction 5 and listed as a claim change. The report is accurate. It says the claim about more preparation time survives in the quote and in the standfirst, which is true.
- The closing statement "Allt annat är oförändrat, även citaten, siffrorna och meningen om att skillnaden inte tillskrivs programvaran" is accurate.

## 3. The frozen expectation

**"Conforms to the anatomy."** The run should find no anatomy violation, and it reports none by name. However, it reports "5 av 5, inget kvarstår" as defects in a text that conforms, and it rewrites a conforming headline, standfirst and subheading. Findings 1, 3 and 5 are taste presented as defects.

**Preserve customer agency.** Preserved in the body: "Kategorierna i loggen var underhållsgruppens egna. Leverantören Svale konfigurerade loggen efter dem" and "Gruppen enades om kategorierna först". In the headline the customer is still the subject ("Elm Quays arbetsledare ser nytta"). The customer's decision in the last subheading ("Kunden vill ge förberedelserna mer tid") has been replaced by "Maya Lind blickar tillbaka på försöket". Agency is kept, but weakened in the scan layer.

**Preserve the qualified appraisal.** Preserved in the standfirst ("skulle göra om försöket, men skulle avsätta mer tid för förberedelser") and in the quote ("men jag skulle lägga till en vecka för förberedelser"). It is weakened in the scan layer: the new headline states the benefit without the reservation, and the subheading that carried the reservation is gone.

**Preserve the numbers.** Preserved: "registrerades 31 ärenden under åtta veckor ... Mediantiden från anmälan till tilldelning var två arbetsdagar. Under de föregående åtta veckorna var den tre." The date 4 december 2025 and the caveat about causality are unchanged.

**Preserve the supplier publication disclosure.** Preserved: "Kundcaset publiceras av leverantören Svale."

**Preserve the checklist link that carries the call to action.** Preserved: "[Svales checklista för införandet](https://example.invalid/svale/checklist)".

**No required quote count or extra sales block.** Met. No finding asks for more quotes and nothing was added. The headline does move toward a promotional benefit claim, but it adds no sales block.

**Reject findings against limits the text meets** (36-character headline, 40-word standfirst, 36–39-character subheadings). No finding cites a length limit, so the run did not make this mistake. It did push the headline to 50 characters and the standfirst to 45 words, past the lengths the expectation says conform. The two files do not state the actual limits.

**Reject findings resting on the one-sentence paragraph, the four-sentence paragraph or one section's paragraph count.** Not made.

**Reject a finding against the Swedish `Text:` byline form.** Not made. `Text: Iris Falk` is unchanged.

## 4. R1

**Fail.** R1 says "Clean texts may not be rewritten to satisfy taste", and this control conforms to the anatomy. The run still reports five defects and rewrites three conforming elements on grounds of taste:

- The headline is replaced because it "beskrev bara vad kunden gjorde, inte vad kunden fick ut av det". This makes it 36 → 50 characters and drops the qualification from the appraisal.
- The last subheading is replaced because it "föregrep Linds invändning". An informative heading that carried the customer's decision becomes "Maya Lind blickar tillbaka på försöket".
- The standfirst is expanded for explicitness, from 40 to 45 words.

Everything the expectation asks the run to preserve survives in the body. The run avoided every named rejection, and findings 2 and 4 are defensible. The failure lies only in these taste rewrites of a clean text.
