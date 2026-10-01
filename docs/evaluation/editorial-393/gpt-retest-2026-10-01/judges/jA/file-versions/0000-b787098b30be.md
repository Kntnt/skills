# Independent language and fidelity judgement

Read only the neutral packet you receive. Do not browse, load Skills, inspect neighbouring projects, delegate or try to identify the origin of the texts. No model or prior evaluation outcome is relevant. Judge each run separately from the exact supplied input, reply and delivered artifact. Where no artifact was delivered, state which criteria are not answerable; the reply is not an artifact.

The packet identifies a task as translation/composition or source-blind review. Translation/composition also has the original complete source. Source-blind review is answerable to the input text only; do not invent access to a source package. Score facts, genre, idiom, review preservation and quotation behaviour separately. Quote the actual passages supporting each judgement. Distinguish supported repair, unresolved finding, false finding, unreported change, withheld text and missing artifact.

The following are fixed professional-language behaviour expectations supplied by the maintainer, not a request to vote on taste. In the full repair-log accounts, `innan nästa hus börjar` and `innan nästa byggnad kommer i gång` are defective Swedish references to introducing the log in another existing building. They do not refer to constructing a house. In the stock-system account, `Sedan gick lagret över` is defective Swedish in the account of leaving parallel spreadsheets for a shared system. An unchanged target phrase passes only when the reply explicitly reports that obstruction as unresolved. Otherwise it fails the mandatory-finding criterion even if you personally find its meaning recoverable. A new wording is judged for idiom and supported meaning, not similarity to a reference sentence; no replacement is prescribed.

In the English repair-log accounts, `before the next building starts` works in its complete English context and should remain unchanged unless a finding establishes a concrete English obstacle from that text. `terminen drog i gång` and `expeditionen märkte skillnaden` are ordinary Swedish figures and should not be expanded literally. The British English rhythm and figures `before the winter` and `the depot stopped ringing round` work in their complete account and should remain unless the report establishes a concrete reading loss. Detecting an implied event or institutional actor by itself does not establish an obstacle.

For a translated preparation quotation, assess whether it contributes the same experience, meaning, stance, qualification and customer voice as the source in idiomatic Swedish. An omitted quotation fails the commissioned translation control. Independently test whether any asserted introduction activity has support in the full source: a fluent invented activity fails fidelity.

For every delivered artifact also assess G1 (genre job for its reader), P1 (followable reasoning and proportionate conclusion), W1 (web orientation, complementary parts and coherent rhythm), and L2 (resolved-locale mechanics, preserving established valid variation). Counted article limits are 20–70 characters for headline, at most 60 words for standfirst, at most 70 characters per subheading, at least one paragraph per section, and one paragraph each for standfirst and lead. Advisory norms such as most paragraphs having two or three sentences need actual reader loss before failure. A byline missing from an input is reported and left unfilled unless an author is supplied.

For every delivered artifact assess F1 (facts and attributed meaning, uncertainty, scope, chronology and causal limits), G2 (genre and customer agency/qualified experience where applicable), L1 (idiomatic target-language prose), and for reviews R1 (mandatory findings resolved or explicitly left; valid prose preserved; every substantive change supported by a real reported finding). A claim-limiting sentence cannot disappear or harden because it repeats a limit. Headings and the reply make claims too. Do not merge target-quotation success with whole-artifact success.

Return one entry per neutral run ID with `pass`, `fail`, `disputed` or `skipped` for each applicable criterion. State the exact evidence and reason for every non-pass, identify any of the five rejection classes (unsupported fact, wrong locale, impermissible substantive mechanical edit, unresolved mandatory finding, incorrect side effect) that the supplied evidence establishes, and list any uncertainty. Do not assert side effects or resource loading from semantic material. A mechanically identical output proves preservation; a statement that nothing changed proves only what the reply claimed.

## sample-01

Task: source-blind review. Requested output target: response.

### Formal Invocation

```text
/redline --genre=casestudy --output=response input.md
```

### Complete supplied input

```text
---
kntnt:
  genre: case-study
  technique: none
  language: en_US
---

# Elm Quay brings repair reports into one shared view

Elm Quay Housing tested a shared repair log in two buildings to help staff on different shifts see the same information. Maintenance supervisor Maya Lind says having one view helps the team, but would allow more preparation time. The eight-week trial remains unexpanded; the team will decide after checking how its categories work for larger repairs.

Elm Quay manages 640 apartments. In September 2025, its maintenance team decided to trial a shared log after previously storing telephone reports and emails separately. The team chose Svale Systems after testing whether the log could show the status of each repair.

“We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log,” Lind said in an email interview.

The maintenance team designed the categories and kept telephone reporting open for residents. Svale configured the log and trained six staff members during two sessions.

“We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts,” Lind said.

Elm Quay’s internal trial note, dated December 4, 2025, records 31 repair reports entered during the eight-week trial. The count excludes emergencies and work ordered before the trial.

The note puts the median time from report to assignment at two working days during the trial, compared with three in the preceding eight-week period. The periods had different workloads, and the note explicitly does not attribute the difference to the software. These figures describe assignment, not repair completion; no completion-time, cost, or resident-satisfaction measurements are available.

Lind’s assessment includes a reservation about preparation:

“I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation.”

The team has not yet expanded the trial. It will decide after checking how the categories work for larger repairs. Lind’s willingness to repeat the trial is a qualified judgment, rather than a recommendation of Svale for every housing company.

For operations managers considering their own preparations, Svale’s [implementation checklist](https://example.invalid/svale/checklist) is available to read.

*This customer case is published by Svale Systems.*

```

### Delivered Text Artifact

```text
---
kntnt:
  genre: casestudy
  technique: none
  language: en_US
---

# Elm Quay brings repair reports into one shared view

Elm Quay Housing tested a shared repair log in two buildings to help staff on different shifts see the same information. Maintenance supervisor Maya Lind says having one view helps the team, but would allow more preparation time. The eight-week trial remains unexpanded; the team will decide after checking how its categories work for larger repairs.

Elm Quay manages 640 apartments. In September 2025, its maintenance team decided to trial a shared log after previously storing telephone reports and emails separately. The team chose Svale Systems after testing whether the log could show the status of each repair.

“We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log,” Lind said in an email interview.

The maintenance team designed the categories and kept telephone reporting open for residents. Svale configured the log and trained six staff members during two sessions.

“We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts,” Lind said.

Elm Quay’s internal trial note, dated December 4, 2025, records 31 repair reports entered during the eight-week trial. The count excludes emergencies and work ordered before the trial.

The note puts the median time from report to assignment at two working days during the trial, compared with three in the preceding eight-week period. The periods had different workloads, and the note explicitly does not attribute the difference to the software. These figures describe assignment, not repair completion; no completion-time, cost, or resident-satisfaction measurements are available.

Lind said:

I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation.

The team has not yet expanded the trial. It will decide after checking how the categories work for larger repairs. Lind’s willingness to repeat the trial is a qualified judgment, rather than a recommendation of Svale for every housing company.

For operations managers considering their own preparations, Svale’s [implementation checklist](https://example.invalid/svale/checklist) is available to read.

*This customer case is published by Svale Systems.*

```

### User-facing reply

````text
Reviewed as `casestudy` in American English (`en_US`), with no technique selected (`none` from the document’s metadata).

```markdown
---
kntnt:
  genre: casestudy
  technique: none
  language: en_US
---

# Elm Quay brings repair reports into one shared view

Elm Quay Housing tested a shared repair log in two buildings to help staff on different shifts see the same information. Maintenance supervisor Maya Lind says having one view helps the team, but would allow more preparation time. The eight-week trial remains unexpanded; the team will decide after checking how its categories work for larger repairs.

Elm Quay manages 640 apartments. In September 2025, its maintenance team decided to trial a shared log after previously storing telephone reports and emails separately. The team chose Svale Systems after testing whether the log could show the status of each repair.

“We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log,” Lind said in an email interview.

The maintenance team designed the categories and kept telephone reporting open for residents. Svale configured the log and trained six staff members during two sessions.

“We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts,” Lind said.

Elm Quay’s internal trial note, dated December 4, 2025, records 31 repair reports entered during the eight-week trial. The count excludes emergencies and work ordered before the trial.

The note puts the median time from report to assignment at two working days during the trial, compared with three in the preceding eight-week period. The periods had different workloads, and the note explicitly does not attribute the difference to the software. These figures describe assignment, not repair completion; no completion-time, cost, or resident-satisfaction measurements are available.

Lind said:

I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation.

The team has not yet expanded the trial. It will decide after checking how the categories work for larger repairs. Lind’s willingness to repeat the trial is a qualified judgment, rather than a recommendation of Svale for every housing company.

For operations managers considering their own preparations, Svale’s [implementation checklist](https://example.invalid/svale/checklist) is available to read.

*This customer case is published by Svale Systems.*

```

- **Repaired:** The quotation bridge announced Lind’s preparation reservation before her own words. It now carries attribution only.
- **Unresolved:** The author byline, body sections, and separate ending section are missing. The [redline skill](/private/var/folders/cs/vgp_x_353zd9frkjpysp7zdw0000gn/T/kntnt-native-session-a9a6vvtz/work/.agents/skills/redline/SKILL.md) follows the anatomy rule: “its absence is a finding, and the part is not written.” These missing parts remain for the author to supply.

Removed claim: the bridge’s advance statement that Lind’s appraisal includes a preparation reservation was removed by that repair. The reservation remains in her reported words, including the extra week.

The review repaired the quotation bridge, synchronized the genre metadata, and adjusted quotation punctuation in the final mechanical pass. `input.md` is unchanged; no temporary files remain.
````

## sample-02

Task: source-blind review. Requested output target: output.md.

### Formal Invocation

```text
/redline --genre=casestudy --output=output.md input.md
```

### Complete supplied input

```text
---
kntnt:
  genre: case-study
  technique: none
  language: en_US
---

# Elm Quay finds value in one view of repair reports

Elm Quay Housing’s maintenance team tested a shared repair log in two buildings to help staff on different shifts see the same information. Supervisor Maya Lind valued the shared view, but her assessment came with a reservation: she would allow more preparation time before repeating the trial.

*Published by Svale Systems.*

Elm Quay manages 640 apartments. In September 2025, its maintenance team decided to trial a shared log after storing telephone reports and emails separately. The team chose Svale Systems after testing whether the log could show the status of each repair.

“We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log,” Lind said in an email interview.

The maintenance team designed the categories and kept telephone reporting open for residents. Svale configured the log and trained six staff members over two sessions. For Lind, the experience offered a preparation lesson:

“We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts.”

The trial lasted eight weeks. Elm Quay’s internal trial note, dated December 4, 2025, recorded 31 repair reports, excluding emergencies and work ordered before the trial.

The median time from report to assignment was two working days during the trial, compared with three in the preceding eight-week period. The periods had different workloads, and the note explicitly does not attribute the difference to the software. These figures concern assignment, not completion; there are no measurements of repair completion time, costs, or resident satisfaction.

Lind gave a qualified endorsement of repeating the trial:

“I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation.”

The trial has not yet expanded. The team will decide after checking how the categories work for larger repairs. Lind’s willingness to repeat the trial is her assessment of Elm Quay’s experience, not a recommendation of Svale for every housing company.

For an optional next step, read [Svale’s implementation checklist](https://example.invalid/svale/checklist).

```

### Delivered Text Artifact

```text
---
kntnt:
  genre: casestudy
  technique: none
  language: en_US
---

# Elm Quay finds value in one view of repair reports

Elm Quay Housing’s maintenance team tested a shared repair log in two buildings to help staff on different shifts see the same information. Supervisor Maya Lind valued the shared view, but her assessment came with a reservation: she would allow more preparation time before repeating the trial.

*Published by Svale Systems.*

Elm Quay manages 640 apartments. In September 2025, its maintenance team decided to trial a shared log after storing telephone reports and emails separately. The team chose Svale Systems after testing whether the log could show the status of each repair.

“We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log,” supervisor Maya Lind said in an email interview.

The maintenance team designed the categories and kept telephone reporting open for residents. Svale configured the log and trained six staff members over two sessions. Lind said:

“We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts.”

The trial lasted eight weeks. Elm Quay’s internal trial note, dated December 4, 2025, recorded 31 repair reports, excluding emergencies and work ordered before the trial.

The median time from report to assignment was two working days during the trial, compared with three in the preceding eight-week period. The periods had different workloads, and the note explicitly does not attribute the difference to the software. These figures concern assignment, not completion; there are no measurements of repair completion time, costs, or resident satisfaction.

On repeating the trial, Lind said:

“I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation.”

The trial has not yet expanded. The team will decide after checking how the categories work for larger repairs. Lind’s willingness to repeat the trial is her assessment of Elm Quay’s experience, not a recommendation of Svale for every housing company.

For an optional next step, read [Svale’s implementation checklist](https://example.invalid/svale/checklist).

```

### User-facing reply

```text
Saved [output.md](/private/var/folders/cs/vgp_x_353zd9frkjpysp7zdw0000gn/T/kntnt-native-session-euzjpdes/work/output.md). Reviewed as casestudy in American English (en_US), with technique none from the input metadata.

Two findings remain unresolved:

- The author byline is missing. “Published by Svale Systems.” identifies the publisher without naming the author.
- Section subheadings, including an ending subheading, are missing, leaving readers without headings to scan the trial and its next step.

Missing parts remain unfilled under the [redline skill](/private/var/folders/cs/vgp_x_353zd9frkjpysp7zdw0000gn/T/kntnt-native-session-euzjpdes/work/.agents/skills/redline/SKILL.md) and its [anatomy rules](/private/var/folders/cs/vgp_x_353zd9frkjpysp7zdw0000gn/T/kntnt-native-session-euzjpdes/work/.agents/skills/kntnt/library/references/editorial/article-anatomy.review.md), which state: “its absence is a finding, and the part is not written.”

The accepted repairs and claim account:

- Clarified attribution: The first quotation now identifies supervisor Maya Lind, repeating her identity from the standfirst so the body stands alone.
- Removed from narration: The claim that Lind’s experience “offered a preparation lesson,” because it pre-echoed the following quotation. The lesson remains in her unchanged quotation.
- Removed from narration: The characterization that Lind “gave a qualified endorsement of repeating the trial,” because it pre-echoed her judgement and reservation. Her qualified appraisal remains in the unchanged quotation.

No new claims were added.

The changes clarified speaker identification, removed redundant quotation framing, and synchronized the genre metadata to casestudy. The final proofreading pass found no mechanical errors.
```

## sample-03

Task: translation/composition. Requested output target: response.

### Formal Invocation

```text
/write --genre=casestudy --language=sv --output=response source.md
```

### Complete original source

```text
# Case-study brief and source

SYNTHETIC EVALUATION MATERIAL. This is the entire fictional source package. Source language: English. No external facts or quotations may be added.

## Brief

Write a journalistic customer case for operations managers at small housing companies. The publisher is the supplier, Svale Systems. The customer, Elm Quay Housing, should remain the acting party. Approximately 400 words, as material allows. Markdown. No author name supplied. The optional next step is the supplied implementation checklist at https://example.invalid/svale/checklist; it is a document to read, not a consultation booking or a product trial.

## Material

Elm Quay Housing manages 640 flats. In September 2025 its own maintenance team decided to trial a shared repair log in two buildings. Previously telephone reports and emails were stored separately. The team wanted staff on different shifts to see the same information. It chose Svale Systems after testing whether the log could show the status of each repair. No comparison with another supplier is available.

The maintenance team designed its categories and kept telephone reporting open for residents. Svale configured the log and trained six staff during two sessions. The trial lasted eight weeks. Elm Quay's internal trial note, 4 December 2025, says that 31 repair reports were entered. It excludes emergencies and work ordered before the trial. Median time from report to assignment was two working days during the trial and three in the preceding eight-week period. The periods had different workloads, and the note explicitly does not attribute the difference to the software. There are no cost, resident-satisfaction or completion-time measurements.

Customer interview with maintenance supervisor Maya Lind, complete usable quotations:

- “We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log.”
- “We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts.”
- “I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation.”

Lind did not recommend Svale to every housing company. Her final quotation is her actual, qualified assessment. It is not an inference from the figures. The trial has not yet expanded; the team will decide after checking how the categories work for larger repairs. The supplier approved publication of this case as supplier-published material; it is not independent journalism. All interviews occurred by email, and no physical scene, emotion or remembered dialogue is provided. Translation of the quotations is permitted, preserving stance and qualification.

## Forbidden inferences / judging

No claim that software caused the shorter assignment time, saved money, delighted residents or rescued a helpless customer. Do not turn assignment time into completion time. The customer's reservation must survive. Judge whether quotations contribute experience beyond the surrounding narrative, whether supplier narration stays in third person and whether the suggested link accurately describes its destination.
```

### Delivered Text Artifact

```text
---
kntnt:
  genre: casestudy
  technique: none
  language: sv
---

# Elm Quay Housing samlar anmälningar i reparationsloggen

Efter åtta veckors test i två byggnader har Elm Quay Housing både siffror och en egen bedömning att utgå från. Arbetsledaren för underhåll, Maya Lind, berättar om förberedelserna, och bolagets anteckning sätter gränserna för vilka slutsatser som kan dras. Kundfallet publiceras av leverantören Svale Systems.

Av [ditt namn]

Elm Quay Housing förvaltar 640 lägenheter. I september 2025 beslutade bolagets eget underhållsteam att testa en gemensam reparationslogg i två byggnader. Telefonanmälningar och mejl hade tidigare sparats var för sig. Teamet ville att personal på olika skift skulle kunna se samma information.

## Teamet behåller telefonanmälan för de boende

Teamet valde Svale Systems efter att ha testat om loggen kunde visa status för varje reparation. Det utformade också sina egna kategorier och höll telefonanmälan öppen för de boende.

Svale konfigurerade loggen och utbildade sex medarbetare under två tillfällen. I en mejlintervju beskriver arbetsledaren för underhåll, Maya Lind, arbetet med att komma igång:

– Vi lade mer tid på att komma överens om kategorierna än på att lägga in de första anmälningarna. Jag skulle avsätta den tiden innan nästa byggnad börjar använda loggen.

## Anteckningen jämför två perioder

Försöket pågick i åtta veckor. Enligt Elm Quay Housings interna försöksanteckning, daterad den 4 december 2025, registrerades 31 reparationsanmälningar. Akuta ärenden och arbeten som beställts före försöket ingår inte i underlaget.

Mediantiden från anmälan till tilldelning var två arbetsdagar under försöket, jämfört med tre under den föregående åttaveckorsperioden. Arbetsbelastningen skilde sig mellan perioderna. Anteckningen pekar uttryckligen inte ut programvaran som orsak till skillnaden.

Det finns inga mätningar av kostnader, de boendes nöjdhet eller tiden till slutförd reparation. Siffrorna beskriver tiden till tilldelning av arbetet.

## Maya Lind bedömer försöket inför nästa beslut

Elm Quay Housing har ännu inte utökat försöket. Teamet ska först kontrollera hur kategorierna fungerar för större reparationer och därefter besluta om försöket ska utökas.

I mejlintervjun ger Lind sin bedömning:

– Jag skulle välja att göra försöket igen. Att ha en gemensam vy över anmälningarna hjälper oss, men jag skulle avsätta en extra vecka för förberedelser.

## Läs vidare i Svale Systems checklista

För ett eget test är tiden för förberedelser en fråga att ta ställning till. Som ett frivilligt nästa steg kan du läsa [Svale Systems checklista för införande](https://example.invalid/svale/checklist).
```

### User-facing reply

````text
Utkastet levereras med en känd källstödsbrist: ”tilldelning av arbetet” preciserar källans ospecificerade ”assignment”. Föreslagen reparation: ”Siffrorna beskriver tiden från anmälan till tilldelning.”

Skillen [write](/private/var/folders/cs/vgp_x_353zd9frkjpysp7zdw0000gn/T/kntnt-native-session-h3gc8vnj/work/.agents/skills/write/SKILL.md) kräver ”never reopen the prose after its final source comparison”, så förslaget lämnas utanför den kontrollerade texten.

Fallstudien är på svenska, med teknik `none` enligt genren `casestudy`. Författarnamn saknas; bylinen har en platshållare. Det fiktiva underlaget saknar kostnads-, nöjdhets- och slutförandetidsmått samt leverantörsjämförelser. Inga nya filer lämnades kvar.

```markdown
---
kntnt:
  genre: casestudy
  technique: none
  language: sv
---

# Elm Quay Housing samlar anmälningar i reparationsloggen

Efter åtta veckors test i två byggnader har Elm Quay Housing både siffror och en egen bedömning att utgå från. Arbetsledaren för underhåll, Maya Lind, berättar om förberedelserna, och bolagets anteckning sätter gränserna för vilka slutsatser som kan dras. Kundfallet publiceras av leverantören Svale Systems.

Av [ditt namn]

Elm Quay Housing förvaltar 640 lägenheter. I september 2025 beslutade bolagets eget underhållsteam att testa en gemensam reparationslogg i två byggnader. Telefonanmälningar och mejl hade tidigare sparats var för sig. Teamet ville att personal på olika skift skulle kunna se samma information.

## Teamet behåller telefonanmälan för de boende

Teamet valde Svale Systems efter att ha testat om loggen kunde visa status för varje reparation. Det utformade också sina egna kategorier och höll telefonanmälan öppen för de boende.

Svale konfigurerade loggen och utbildade sex medarbetare under två tillfällen. I en mejlintervju beskriver arbetsledaren för underhåll, Maya Lind, arbetet med att komma igång:

– Vi lade mer tid på att komma överens om kategorierna än på att lägga in de första anmälningarna. Jag skulle avsätta den tiden innan nästa byggnad börjar använda loggen.

## Anteckningen jämför två perioder

Försöket pågick i åtta veckor. Enligt Elm Quay Housings interna försöksanteckning, daterad den 4 december 2025, registrerades 31 reparationsanmälningar. Akuta ärenden och arbeten som beställts före försöket ingår inte i underlaget.

Mediantiden från anmälan till tilldelning var två arbetsdagar under försöket, jämfört med tre under den föregående åttaveckorsperioden. Arbetsbelastningen skilde sig mellan perioderna. Anteckningen pekar uttryckligen inte ut programvaran som orsak till skillnaden.

Det finns inga mätningar av kostnader, de boendes nöjdhet eller tiden till slutförd reparation. Siffrorna beskriver tiden till tilldelning av arbetet.

## Maya Lind bedömer försöket inför nästa beslut

Elm Quay Housing har ännu inte utökat försöket. Teamet ska först kontrollera hur kategorierna fungerar för större reparationer och därefter besluta om försöket ska utökas.

I mejlintervjun ger Lind sin bedömning:

– Jag skulle välja att göra försöket igen. Att ha en gemensam vy över anmälningarna hjälper oss, men jag skulle avsätta en extra vecka för förberedelser.

## Läs vidare i Svale Systems checklista

För ett eget test är tiden för förberedelser en fråga att ta ställning till. Som ett frivilligt nästa steg kan du läsa [Svale Systems checklista för införande](https://example.invalid/svale/checklist).
```
````

## sample-04

Task: source-blind review. Requested output target: response.

### Formal Invocation

```text
/redline --genre=casestudy --output=response input.md
```

### Complete supplied input

```text
---
kntnt:
  genre: case-study
  technique: none
  language: en_US
---

# Elm Quay finds value in one view of repair reports

Elm Quay Housing’s maintenance team tested a shared repair log in two buildings to help staff on different shifts see the same information. Supervisor Maya Lind valued the shared view, but her assessment came with a reservation: she would allow more preparation time before repeating the trial.

*Published by Svale Systems.*

Elm Quay manages 640 apartments. In September 2025, its maintenance team decided to trial a shared log after storing telephone reports and emails separately. The team chose Svale Systems after testing whether the log could show the status of each repair.

“We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log,” Lind said in an email interview.

The maintenance team designed the categories and kept telephone reporting open for residents. Svale configured the log and trained six staff members over two sessions. For Lind, the experience offered a preparation lesson:

“We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts.”

The trial lasted eight weeks. Elm Quay’s internal trial note, dated December 4, 2025, recorded 31 repair reports, excluding emergencies and work ordered before the trial.

The median time from report to assignment was two working days during the trial, compared with three in the preceding eight-week period. The periods had different workloads, and the note explicitly does not attribute the difference to the software. These figures concern assignment, not completion; there are no measurements of repair completion time, costs, or resident satisfaction.

Lind gave a qualified endorsement of repeating the trial:

“I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation.”

The trial has not yet expanded. The team will decide after checking how the categories work for larger repairs. Lind’s willingness to repeat the trial is her assessment of Elm Quay’s experience, not a recommendation of Svale for every housing company.

For an optional next step, read [Svale’s implementation checklist](https://example.invalid/svale/checklist).

```

### Delivered Text Artifact

```text
---
kntnt:
  genre: casestudy
  technique: none
  language: en_US
---

# Elm Quay finds value in one view of repair reports

Elm Quay Housing’s maintenance team tested a shared repair log in two buildings to help staff on different shifts see the same information. Supervisor Maya Lind valued the shared view, but her assessment came with a reservation: she would allow more preparation time before repeating the trial.

*Published by Svale Systems.*

Elm Quay manages 640 apartments. In September 2025, its maintenance team decided to trial a shared log after storing telephone reports and emails separately. The team chose Svale Systems after testing whether the log could show the status of each repair.

“We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log,” Lind said in an email interview.

The maintenance team designed the categories and kept telephone reporting open for residents. Svale configured the log and trained six staff members over two sessions. For Lind, the experience offered a preparation lesson:

“We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the trial in the next building starts.”

The trial lasted eight weeks. Elm Quay’s internal trial note, dated December 4, 2025, recorded 31 repair reports, excluding emergencies and work ordered before the trial.

The median time from report to assignment was two working days during the trial, compared with three in the preceding eight-week period. The periods had different workloads, and the note explicitly does not attribute the difference to the software. These figures concern assignment, not completion; there are no measurements of repair completion time, costs, or resident satisfaction.

On repeating the trial, Lind said:

“I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation.”

The trial has not yet expanded. The team will decide after checking how the categories work for larger repairs. Lind’s willingness to repeat the trial is her assessment of Elm Quay’s experience, not a recommendation of Svale for every housing company.

For an optional next step, read [Svale’s implementation checklist](https://example.invalid/svale/checklist).

```

### User-facing reply

````text
Reviewed as `casestudy` in American English (`en_US`), with no technique. The explicit genre overrides the supplied `case-study` metadata.

```markdown
---
kntnt:
  genre: casestudy
  technique: none
  language: en_US
---

# Elm Quay finds value in one view of repair reports

Elm Quay Housing’s maintenance team tested a shared repair log in two buildings to help staff on different shifts see the same information. Supervisor Maya Lind valued the shared view, but her assessment came with a reservation: she would allow more preparation time before repeating the trial.

*Published by Svale Systems.*

Elm Quay manages 640 apartments. In September 2025, its maintenance team decided to trial a shared log after storing telephone reports and emails separately. The team chose Svale Systems after testing whether the log could show the status of each repair.

“We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log,” Lind said in an email interview.

The maintenance team designed the categories and kept telephone reporting open for residents. Svale configured the log and trained six staff members over two sessions. For Lind, the experience offered a preparation lesson:

“We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the trial in the next building starts.”

The trial lasted eight weeks. Elm Quay’s internal trial note, dated December 4, 2025, recorded 31 repair reports, excluding emergencies and work ordered before the trial.

The median time from report to assignment was two working days during the trial, compared with three in the preceding eight-week period. The periods had different workloads, and the note explicitly does not attribute the difference to the software. These figures concern assignment, not completion; there are no measurements of repair completion time, costs, or resident satisfaction.

On repeating the trial, Lind said:

“I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation.”

The trial has not yet expanded. The team will decide after checking how the categories work for larger repairs. Lind’s willingness to repeat the trial is her assessment of Elm Quay’s experience, not a recommendation of Svale for every housing company.

For an optional next step, read [Svale’s implementation checklist](https://example.invalid/svale/checklist).

```

Repaired findings and changed claims:

- In the original text, the appraisal bridge previewed Lind’s endorsement and reservation. It now introduces her remarks about repeating the trial without that advance characterization; her endorsement and reservation remain in her quotation.
- In the original quotation, “before the next building starts” left the referent unclear. It now explicitly identifies the trial in the next building as what starts, retaining Lind’s preparation recommendation.

Unresolved: the author byline, headed sections, and separate ending section are missing. The publisher notice identifies no author; the closing paragraphs and checklist call to action are present. The [redline skill](/private/var/folders/cs/vgp_x_353zd9frkjpysp7zdw0000gn/T/kntnt-native-session-qev9bmaz/work/.agents/skills/redline/SKILL.md) applies its [anatomy review rule](/private/var/folders/cs/vgp_x_353zd9frkjpysp7zdw0000gn/T/kntnt-native-session-qev9bmaz/work/.agents/skills/kntnt/library/references/editorial/article-anatomy.review.md): “A part the text does not have is reported, and a part it has is repaired.” These missing parts are left for the writer.

The review removed a quotation pre-echo, clarified a quoted reference, and synchronized the genre metadata. The closing proofreading pass required no mechanical corrections.
````

## sample-05

Task: source-blind review. Requested output target: output.md.

### Formal Invocation

```text
/redline --genre=casestudy --output=output.md input.md
```

### Complete supplied input

```text
---
kntnt:
  genre: case-study
  technique: none
  language: en_US
---

# Elm Quay brings repair reports into one shared view

Elm Quay Housing tested a shared repair log in two buildings to help staff on different shifts see the same information. Maintenance supervisor Maya Lind says having one view helps the team, but would allow more preparation time. The eight-week trial remains unexpanded; the team will decide after checking how its categories work for larger repairs.

Elm Quay manages 640 apartments. In September 2025, its maintenance team decided to trial a shared log after previously storing telephone reports and emails separately. The team chose Svale Systems after testing whether the log could show the status of each repair.

“We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log,” Lind said in an email interview.

The maintenance team designed the categories and kept telephone reporting open for residents. Svale configured the log and trained six staff members during two sessions.

“We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts,” Lind said.

Elm Quay’s internal trial note, dated December 4, 2025, records 31 repair reports entered during the eight-week trial. The count excludes emergencies and work ordered before the trial.

The note puts the median time from report to assignment at two working days during the trial, compared with three in the preceding eight-week period. The periods had different workloads, and the note explicitly does not attribute the difference to the software. These figures describe assignment, not repair completion; no completion-time, cost, or resident-satisfaction measurements are available.

Lind’s assessment includes a reservation about preparation:

“I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation.”

The team has not yet expanded the trial. It will decide after checking how the categories work for larger repairs. Lind’s willingness to repeat the trial is a qualified judgment, rather than a recommendation of Svale for every housing company.

For operations managers considering their own preparations, Svale’s [implementation checklist](https://example.invalid/svale/checklist) is available to read.

*This customer case is published by Svale Systems.*

```

### Delivered Text Artifact

```text
---
kntnt:
  genre: casestudy
  technique: none
  language: en_US
---

# Elm Quay brings repair reports into one shared view

Elm Quay Housing tested a shared repair log in two buildings to help staff on different shifts see the same information. Maintenance supervisor Maya Lind says having one view helps the team, but would allow more preparation time. The eight-week trial remains unexpanded; the team will decide after checking how its categories work for larger repairs.

Elm Quay manages 640 apartments. In September 2025, its maintenance team decided to trial a shared log after previously storing telephone reports and emails separately. The team chose Svale Systems after testing whether the log could show the status of each repair.

“We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log,” Lind said in an email interview.

The maintenance team designed the categories and kept telephone reporting open for residents. Svale configured the log and trained six staff members during two sessions.

“We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts,” Lind said.

Elm Quay’s internal trial note, dated December 4, 2025, records 31 repair reports entered during the eight-week trial. The count excludes emergencies and work ordered before the trial.

The note puts the median time from report to assignment at two working days during the trial, compared with three in the preceding eight-week period. The periods had different workloads, and the note explicitly does not attribute the difference to the software. These figures describe assignment, not repair completion; no completion-time, cost, or resident-satisfaction measurements are available.

Lind’s assessment:

“I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation.”

The team has not yet expanded the trial. It will decide after checking how the categories work for larger repairs. Lind’s willingness to repeat the trial is a qualified judgment, rather than a recommendation of Svale for every housing company.

For operations managers considering their own preparations, Svale’s [implementation checklist](https://example.invalid/svale/checklist) is available to read.

*This customer case is published by Svale Systems.*

```

### User-facing reply

```text
Saved [output.md](/private/var/folders/cs/vgp_x_353zd9frkjpysp7zdw0000gn/T/kntnt-native-session-dujnnokn/work/output.md). Reviewed as `casestudy` in `en_US`; the input metadata selects no technique.

- **Repaired:** the original quotation bridge previewed Lind’s preparation reservation.
- **Claim account:** the bridge now reads “Lind’s assessment:”, removing that advance statement. The reservation remains unchanged in her quotation.
- **Unresolved:** the author byline, body sections and separate ending section are missing. The measurement misidentifies the quotation bridge as a byline, producing misleading standfirst and lead boundaries.

The [redline skill](/private/var/folders/cs/vgp_x_353zd9frkjpysp7zdw0000gn/T/kntnt-native-session-dujnnokn/work/.agents/skills/redline/SKILL.md) applies this [anatomy rule](/private/var/folders/cs/vgp_x_353zd9frkjpysp7zdw0000gn/T/kntnt-native-session-dujnnokn/work/.agents/skills/kntnt/library/references/editorial/article-anatomy.review.md): “A part the text does not have is reported, and a part it has is repaired.” Those missing parts were left for the writer.

The edit removed the quotation pre-echo and synchronized the genre metadata to `casestudy`. The final proofread found no mechanical errors.
```

## sample-06

Task: source-blind review. Requested output target: response.

### Formal Invocation

```text
/redline --output=response input.md
```

### Complete supplied input

```text
# Elm Quay samlade reparationsärendena

**Elm Quay Housing provade en gemensam reparationslogg i två hus. Arbetsledaren Maya Lind vill göra om försöket, men skulle avsätta mer tid för förberedelser.**

För Elm Quays underhållsgrupp handlade försöket om att se samma information över skiftgränserna. Gruppen valde kategorierna; leverantören Svale konfigurerade loggen och utbildade sex medarbetare.

– Vi lade mer tid på att enas om kategorierna än på att lägga in de första ärendena. Den tiden skulle jag avsätta innan nästa hus börjar, säger Maya Lind.

## Två perioder med olika arbetsbelastning

Enligt Elm Quays interna försöksanteckning från den 4 december 2025 registrerades 31 ärenden under åtta veckor. Akuta ärenden och tidigare beställda arbeten ingick inte. Mediantiden från anmälan till tilldelning var två arbetsdagar, jämfört med tre under de föregående åtta veckorna.

Perioderna hade olika arbetsbelastning. Anteckningen tillskriver därför inte skillnaden programvaran.

## Kunden vill ge förberedelserna mer tid

– Jag skulle välja att göra försöket igen. Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Lind.

Kundcaset publiceras av leverantören Svale. [Läs Svales checklista för införandet](https://example.invalid/svale/checklist).
```

### Delivered Text Artifact

```text
# Elm Quay samlade reparationsärendena

**Elm Quay Housing provade en gemensam reparationslogg i två hus. Arbetsledaren Maya Lind vill göra om försöket, men skulle avsätta mer tid för förberedelser.**

För Elm Quays underhållsgrupp handlade försöket med en gemensam reparationslogg om att se samma information över skiftgränserna. Gruppen valde kategorierna; leverantören Svale konfigurerade loggen och utbildade sex medarbetare.

## Maya Lind om förberedelserna

– Vi lade mer tid på att enas om kategorierna än på att lägga in de första ärendena. Den tiden skulle jag avsätta innan nästa hus börjar, säger Maya Lind.

## Två perioder med olika arbetsbelastning

Enligt Elm Quays interna försöksanteckning från den 4 december 2025 registrerades 31 ärenden under åtta veckor. Akuta ärenden och tidigare beställda arbeten ingick inte. Mediantiden från anmälan till tilldelning var två arbetsdagar, jämfört med tre under de föregående åtta veckorna.

Perioderna hade olika arbetsbelastning. Anteckningen tillskriver därför inte skillnaden programvaran.

## Maya Lind om försöket

– Jag skulle välja att göra försöket igen. Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Lind.

Kundcaset publiceras av leverantören Svale. [Läs Svales checklista för införandet](https://example.invalid/svale/checklist).
```

### User-facing reply

````text
Granskad som kundcase på svenska, utan särskild teknik.

```markdown
# Elm Quay samlade reparationsärendena

**Elm Quay Housing provade en gemensam reparationslogg i två hus. Arbetsledaren Maya Lind vill göra om försöket, men skulle avsätta mer tid för förberedelser.**

För Elm Quays underhållsgrupp handlade försöket med en gemensam reparationslogg om att se samma information över skiftgränserna. Gruppen valde kategorierna; leverantören Svale konfigurerade loggen och utbildade sex medarbetare.

## Maya Lind om förberedelserna

– Vi lade mer tid på att enas om kategorierna än på att lägga in de första ärendena. Den tiden skulle jag avsätta innan nästa hus börjar, säger Maya Lind.

## Två perioder med olika arbetsbelastning

Enligt Elm Quays interna försöksanteckning från den 4 december 2025 registrerades 31 ärenden under åtta veckor. Akuta ärenden och tidigare beställda arbeten ingick inte. Mediantiden från anmälan till tilldelning var två arbetsdagar, jämfört med tre under de föregående åtta veckorna.

Perioderna hade olika arbetsbelastning. Anteckningen tillskriver därför inte skillnaden programvaran.

## Maya Lind om försöket

– Jag skulle välja att göra försöket igen. Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Lind.

Kundcaset publiceras av leverantören Svale. [Läs Svales checklista för införandet](https://example.invalid/svale/checklist).
```

- **Kvarstår:** Byline saknas. Ingen författare är namngiven, så den har lämnats ofylld.
- **Reparerat:** Brödtextens inledning introducerar nu reparationsloggen. Mellanrubriken ”Maya Lind om förberedelserna” skiljer ut citatet som tidigare låg före första mellanrubriken, så inledningen omfattar ett stycke.
- **Reparerat:** Slutrubriken ”Kunden vill ge förberedelserna mer tid” föregrep citatets förbehåll. ”Maya Lind om försöket” lämnar det åt citatet.

**Ändrat rubrikpåstående:** Slutrubriken anger nu Maya Lind och försöket som ämne, i stället för kundens vilja att ge förberedelserna mer tid. Kundens bedömning och önskemål om längre förberedelsetid finns kvar i citatet.

Den nya mellanrubriken anger det första citatets talare och ämne, förberedelserna. Upplysningen om den gemensamma reparationsloggen har upprepats från ingressen i brödtextens inledning.

Brödtextens inledning har förtydligats och sektionsindelningen reparerats med en ny mellanrubrik och en ändrad slutrubrik. Den avslutande korrekturläsningen gav inga ändringar.
````

## sample-07

Task: source-blind review. Requested output target: response.

### Formal Invocation

```text
/redline --genre=casestudy --output=response input.md
```

### Complete supplied input

```text
---
kntnt:
  genre: case-study
  technique: none
  language: sv
---

# Hamnfrakt flyttade lagersaldot till ett system

**Två av Hamnfrakt AB:s lager fick ett gemensamt system för lagersaldot. Överföringen tog sex veckor med dubbel registrering. Lagerchefen Ove Ranneby skulle göra om den, men börja med färre artikelgrupper.**

Text: Redaktionen

Hamnfrakt AB hanterar reservdelar åt verkstäder i Norrland och har omkring 9 000 artiklar i sitt sortiment. Tidigare fördes saldot för de två lagren i varsitt kalkylark, och den som ringde fick vänta medan någon slog upp siffran på rätt ställe.

## Sex veckor med dubbel registrering

Hamnfrakt valde Saldo Nord efter att ha provat om systemet kunde visa samma saldo för båda lagren. Någon jämförelse med en annan leverantör finns inte i underlaget.

Under sex veckor registrerade personalen varje uttag både i kalkylarken och i det nya systemet. Därefter fördes kalkylarken över och stängdes.

– Vi körde parallellt i sex veckor. Sedan gick lagret över, och först då såg vi hur mycket som hade legat i pärmar, säger Ove Ranneby.

## Vad överföringen visade

Enligt Hamnfrakts egen överföringsanteckning från den 12 januari 2026 saknade 340 av artiklarna en plats i det nya systemet. Artiklar som redan var utgångna ingår inte i den siffran.

Anteckningen redovisar ingen mätning av hur lång tid en förfrågan tar i dag, och ingen jämförelse med tiden före överföringen. Företaget har inte heller följt upp vad överföringen kostade.

## Företaget vill börja mindre nästa gång

– Jag skulle göra om det. Att se samma saldo för båda lagren hjälper oss, men jag skulle ta en artikelgrupp i taget, säger Ranneby.

Det tredje lagret är ännu inte överfört. Hamnfrakt ska först se hur de 340 artiklarna faller på plats. [Läs Saldo Nords checklista för överföringen](https://example.invalid/saldonord/checklista).
```

### Delivered Text Artifact

```text
---
kntnt:
  genre: casestudy
  technique: none
  language: sv
---

# Hamnfrakt flyttade lagersaldot till ett system

**Två av Hamnfrakt AB:s lager fick ett gemensamt system för lagersaldot. Överföringen tog sex veckor med dubbel registrering. Lagerchefen Ove Ranneby skulle göra om den, men börja med färre artikelgrupper.**

Text: Redaktionen

Hamnfrakt AB hanterar reservdelar åt verkstäder i Norrland och har omkring 9 000 artiklar i sitt sortiment. Tidigare fördes saldot för de två lagren i varsitt kalkylark, och den som ringde fick vänta medan någon slog upp siffran på rätt ställe.

## Ove Ranneby beskriver övergången

Hamnfrakt valde Saldo Nord efter att ha provat om systemet kunde visa samma saldo för båda lagren. Någon jämförelse med en annan leverantör finns inte i underlaget.

– Vi körde parallellt i sex veckor. Sedan gick lagret över till det nya systemet, och först då såg vi hur mycket som hade legat i pärmar, säger lagerchefen Ove Ranneby.

Under de veckorna registrerade personalen varje uttag både i kalkylarken och i det nya systemet. Därefter fördes kalkylarken över och stängdes.

## Hamnfrakt har inte följt upp kostnaden

Enligt Hamnfrakts egen överföringsanteckning från den 12 januari 2026 saknade 340 av artiklarna en plats i det nya systemet. Artiklar som redan var utgångna ingår inte i den siffran.

Anteckningen redovisar ingen mätning av hur lång tid en förfrågan tar i dag, och ingen jämförelse med tiden före överföringen. Företaget har inte heller följt upp vad överföringen kostade.

## Det tredje lagret är ännu inte överfört

– Jag skulle göra om det. Att se samma saldo för båda lagren hjälper oss, men jag skulle ta en artikelgrupp i taget, säger Ranneby.

Det tredje lagret är ännu inte överfört. Hamnfrakt ska först se hur de 340 artiklarna faller på plats. [Läs Saldo Nords checklista för överföringen](https://example.invalid/saldonord/checklista).
```

### User-facing reply

````text
Granskad som `casestudy` på svenska, utan berättarteknik enligt textens metadata. Inga olösta fynd återstår. Texten följer artikelanatomin.

```markdown
---
kntnt:
  genre: casestudy
  technique: none
  language: sv
---

# Hamnfrakt flyttade lagersaldot till ett system

**Två av Hamnfrakt AB:s lager fick ett gemensamt system för lagersaldot. Överföringen tog sex veckor med dubbel registrering. Lagerchefen Ove Ranneby skulle göra om den, men börja med färre artikelgrupper.**

Text: Redaktionen

Hamnfrakt AB hanterar reservdelar åt verkstäder i Norrland och har omkring 9 000 artiklar i sitt sortiment. Tidigare fördes saldot för de två lagren i varsitt kalkylark, och den som ringde fick vänta medan någon slog upp siffran på rätt ställe.

## Ove Ranneby beskriver övergången

Hamnfrakt valde Saldo Nord efter att ha provat om systemet kunde visa samma saldo för båda lagren. Någon jämförelse med en annan leverantör finns inte i underlaget.

– Vi körde parallellt i sex veckor. Sedan gick lagret över till det nya systemet, och först då såg vi hur mycket som hade legat i pärmar, säger lagerchefen Ove Ranneby.

Under de veckorna registrerade personalen varje uttag både i kalkylarken och i det nya systemet. Därefter fördes kalkylarken över och stängdes.

## Hamnfrakt har inte följt upp kostnaden

Enligt Hamnfrakts egen överföringsanteckning från den 12 januari 2026 saknade 340 av artiklarna en plats i det nya systemet. Artiklar som redan var utgångna ingår inte i den siffran.

Anteckningen redovisar ingen mätning av hur lång tid en förfrågan tar i dag, och ingen jämförelse med tiden före överföringen. Företaget har inte heller följt upp vad överföringen kostade.

## Det tredje lagret är ännu inte överfört

– Jag skulle göra om det. Att se samma saldo för båda lagren hjälper oss, men jag skulle ta en artikelgrupp i taget, säger Ranneby.

Det tredje lagret är ännu inte överfört. Hamnfrakt ska först se hur de 340 artiklarna faller på plats. [Läs Saldo Nords checklista för överföringen](https://example.invalid/saldonord/checklista).
```

Reparerade fynd och ändrade påståenden:

- Första mellanrubriken föregrep citatets tidsuppgift. Den anger nu att Ove Ranneby beskriver övergången. Registreringsstycket står efter citatet och hänvisar till dess sex veckor i stället för att föregripa uppgiften.
- Första citatet saknade ett uttryckligt mål för övergången. Det anger nu att lagret gick över till det nya systemet. Attributionen presenterar också Ranneby som lagerchef, så att brödtexten fungerar utan ingressens presentation.
- ”Vad överföringen visade” gav inget konkret besked om avsnittets innehåll. Mellanrubriken anger nu att Hamnfrakt inte har följt upp kostnaden; den uppgiften finns också kvar i brödtexten.
- Sista mellanrubriken föregrep Rannebys bedömning och tillskrev företaget hans personliga vilja. Den anger nu att det tredje lagret ännu inte är överfört; den uppgiften finns också kvar i avslutningsstycket.

Borttagna rubrikpåståenden:

- Uppgiften om sex veckor med dubbel registrering har tagits bort ur första mellanrubriken. Den finns kvar i ingressen och utvecklas i citatet och registreringsstycket.
- Påståendet att företaget vill börja mindre nästa gång har tagits bort vid reparationen av sista mellanrubriken. Rannebys egen villkorade bedömning står kvar.

Jag har reparerat mellanrubrikerna, flyttat registreringsstycket, förtydligat citatets syftning och presenterat talarens roll i brödtexten. Genremetadata har synkroniserats till `casestudy`. Den avslutande korrekturläsningen gav inga ytterligare ändringar. Originalfilen är oförändrad och arbetsfilerna är borttagna.
````

## sample-08

Task: source-blind review. Requested output target: response.

### Formal Invocation

```text
/redline --output=response input.md
```

### Complete supplied input

```text
---
kntnt:
  genre: casestudy
  technique: none
  language: sv
---

# Elm Quay Housing samlar reparationsanmälningarna i en vy

Under åtta veckor prövade Elm Quay Housing en reparationslogg från Svale Systems i två hus. Bolagets uppföljning visar en tidsskillnad mellan två perioder, utan att tillskriva den programvaran. Svale Systems publicerar kundfallet som leverantör.

Av [ditt namn]

Telefonanmälningar och mejl hade tidigare sparats var för sig hos Elm Quay Housing, som förvaltar 640 lägenheter. I september 2025 beslutade bolagets eget underhållsteam att testa en gemensam logg så att personal på olika skift skulle se samma information.

## Teamet behöll telefonanmälningarna

Valet föll på Svale Systems efter att teamet hade testat om loggen kunde visa status för varje reparation. Någon jämförelse med en annan leverantör finns inte i underlaget. Arbetsledaren för underhåll, Maya Lind, beskriver utgångspunkten i en mejlintervju:

– Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort. Kategorierna var våra; Svale hjälpte oss att lägga in dem i loggen.

De boende kunde fortsätta att göra anmälningar per telefon.

## Teamet prövade arbetssättet i åtta veckor

Svale konfigurerade loggen och utbildade sex medarbetare vid två tillfällen. I intervjun beskriver Maya Lind också förberedelserna:

– Vi lade mer tid på att komma överens om kategorierna än på att registrera de första anmälningarna. Jag skulle avsätta den tiden innan det är dags för nästa hus.

## Uppföljningen lämnar programvarans effekt öppen

Elm Quay Housings interna anteckning om försöket, daterad den 4 december 2025, anger att 31 reparationsanmälningar registrerades. Akuta ärenden och arbeten som beställts före försöket ingår inte.

Mediantiden från anmälan till tilldelning av ärendet var två arbetsdagar under försöket, jämfört med tre under de föregående åtta veckorna. Perioderna hade olika arbetsbelastning. Anteckningen tillskriver uttryckligen inte programvaran skillnaden.

Det saknas mätningar av kostnader, de boendes nöjdhet och tiden till färdig reparation.

## Elm Quay Housing avvaktar en utökning

Nästa fråga för teamet är hur kategorierna fungerar för större reparationer. Först efter den kontrollen beslutar teamet om en utökning. Maya Lind ger sin egen bedömning av försöket:

– Jag skulle välja att göra försöket igen. Att ha en samlad vy över anmälningarna hjälper oss, men jag skulle avsätta en extra vecka för förberedelser.

## Du kan läsa vidare inför ett införande

För ett eget upplägg är både förberedelserna och uppföljningens begränsningar värda att ta med i planeringen. Du kan läsa [Svale Systems checklista för införande](https://example.invalid/svale/checklist).
```

### Delivered Text Artifact

```text
---
kntnt:
  genre: casestudy
  technique: none
  language: sv
---

# Elm Quay Housing samlar reparationsanmälningarna i en vy

Under åtta veckor prövade Elm Quay Housing en reparationslogg från Svale Systems i två hus. Bolagets uppföljning visar en tidsskillnad mellan två perioder, utan att tillskriva den programvaran. Svale Systems publicerar kundfallet som leverantör.

Av [ditt namn]

Telefonanmälningar och mejl hade tidigare sparats var för sig hos Elm Quay Housing, som förvaltar 640 lägenheter. I september 2025 beslutade bolagets eget underhållsteam att testa en gemensam logg så att personal på olika skift skulle se samma information.

## Teamet behöll telefonanmälningarna

Valet föll på Svale Systems efter att teamet hade testat om loggen kunde visa status för varje reparation. Någon jämförelse med en annan leverantör finns inte i underlaget. Arbetsledaren för underhåll, Maya Lind, beskriver utgångspunkten i en mejlintervju:

– Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort. Kategorierna var våra; Svale hjälpte oss att lägga in dem i loggen.

De boende kunde fortsätta att göra anmälningar per telefon.

## Teamet prövade arbetssättet i åtta veckor

Svale konfigurerade loggen och utbildade sex medarbetare vid två tillfällen. I intervjun beskriver Maya Lind också förberedelserna:

– Vi lade mer tid på att komma överens om kategorierna än på att registrera de första anmälningarna. Jag skulle avsätta den tiden innan det är dags för nästa hus.

## Uppföljningen lämnar programvarans effekt öppen

Elm Quay Housings interna anteckning om försöket, daterad den 4 december 2025, anger att 31 reparationsanmälningar registrerades. Akuta ärenden och arbeten som beställts före försöket ingår inte.

Mediantiden från anmälan till tilldelning av ärendet var två arbetsdagar under försöket, jämfört med tre under de föregående åtta veckorna. Perioderna hade olika arbetsbelastning. Anteckningen tillskriver uttryckligen inte programvaran skillnaden.

Det saknas mätningar av kostnader, de boendes nöjdhet och tiden till färdig reparation.

## Elm Quay Housing avvaktar en utökning

Nästa fråga för teamet är hur kategorierna fungerar för större reparationer. Först efter den kontrollen beslutar teamet om en utökning. Maya Lind ger sin egen bedömning av försöket:

– Jag skulle välja att göra försöket igen. Att ha en samlad vy över anmälningarna hjälper oss, men jag skulle avsätta en extra vecka för förberedelser.

## Du kan läsa vidare inför ett införande

För ett eget upplägg är både förberedelserna och uppföljningens begränsningar värda att ta med i planeringen. Du kan läsa [Svale Systems checklista för införande](https://example.invalid/svale/checklist).
```

### User-facing reply

````text
Granskad som kundfall (casestudy) på svenska (sv), utan skrivteknik enligt textens metadata.

**Olöst:** Bylinen ”Av [ditt namn]” saknar författarens namn, som artikelanatomins bylinekrav kräver. Läsaren får därför inte veta vem som har skrivit texten. Författarnamnet behöver fyllas i; det kan inte fastställas utifrån texten eller anropet.

Texten är oförändrad efter granskning och korrekturläsning.

```markdown
---
kntnt:
  genre: casestudy
  technique: none
  language: sv
---

# Elm Quay Housing samlar reparationsanmälningarna i en vy

Under åtta veckor prövade Elm Quay Housing en reparationslogg från Svale Systems i två hus. Bolagets uppföljning visar en tidsskillnad mellan två perioder, utan att tillskriva den programvaran. Svale Systems publicerar kundfallet som leverantör.

Av [ditt namn]

Telefonanmälningar och mejl hade tidigare sparats var för sig hos Elm Quay Housing, som förvaltar 640 lägenheter. I september 2025 beslutade bolagets eget underhållsteam att testa en gemensam logg så att personal på olika skift skulle se samma information.

## Teamet behöll telefonanmälningarna

Valet föll på Svale Systems efter att teamet hade testat om loggen kunde visa status för varje reparation. Någon jämförelse med en annan leverantör finns inte i underlaget. Arbetsledaren för underhåll, Maya Lind, beskriver utgångspunkten i en mejlintervju:

– Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort. Kategorierna var våra; Svale hjälpte oss att lägga in dem i loggen.

De boende kunde fortsätta att göra anmälningar per telefon.

## Teamet prövade arbetssättet i åtta veckor

Svale konfigurerade loggen och utbildade sex medarbetare vid två tillfällen. I intervjun beskriver Maya Lind också förberedelserna:

– Vi lade mer tid på att komma överens om kategorierna än på att registrera de första anmälningarna. Jag skulle avsätta den tiden innan det är dags för nästa hus.

## Uppföljningen lämnar programvarans effekt öppen

Elm Quay Housings interna anteckning om försöket, daterad den 4 december 2025, anger att 31 reparationsanmälningar registrerades. Akuta ärenden och arbeten som beställts före försöket ingår inte.

Mediantiden från anmälan till tilldelning av ärendet var två arbetsdagar under försöket, jämfört med tre under de föregående åtta veckorna. Perioderna hade olika arbetsbelastning. Anteckningen tillskriver uttryckligen inte programvaran skillnaden.

Det saknas mätningar av kostnader, de boendes nöjdhet och tiden till färdig reparation.

## Elm Quay Housing avvaktar en utökning

Nästa fråga för teamet är hur kategorierna fungerar för större reparationer. Först efter den kontrollen beslutar teamet om en utökning. Maya Lind ger sin egen bedömning av försöket:

– Jag skulle välja att göra försöket igen. Att ha en samlad vy över anmälningarna hjälper oss, men jag skulle avsätta en extra vecka för förberedelser.

## Du kan läsa vidare inför ett införande

För ett eget upplägg är både förberedelserna och uppföljningens begränsningar värda att ta med i planeringen. Du kan läsa [Svale Systems checklista för införande](https://example.invalid/svale/checklist).
```
````

## sample-09

Task: source-blind review. Requested output target: response.

### Formal Invocation

```text
/redline --output=response input.md
```

### Complete supplied input

```text
---
kntnt:
  genre: casestudy
  technique: none
  language: sv
---

# Elm Quay Housing samlar reparationsanmälningarna i en vy

Egna kategorier och fortsatt telefonanmälan präglade Elm Quay Housings försök med en gemensam reparationslogg i två byggnader. Arbetsledaren Maya Lind ger sin bedömning av försöket, och den interna anteckningen sätter gränser för vad tidsuppgifterna kan säga.

Av användaren · Publicerat av Svale Systems

Elm Quay Housing förvaltar 640 lägenheter. I september 2025 beslutade bolagets eget underhållsteam att prova en gemensam logg för reparationer i två byggnader. Telefonanmälningar och mejl hade tidigare lagrats var för sig, och teamet ville att personal på olika skift skulle kunna se samma information.

## Underhållsteamet väljer arbetssättet

Teamet valde Svale Systems efter att ha testat om loggen kunde visa status för varje reparation. Någon jämförelse med en annan leverantör finns inte i underlaget.

De boende kunde fortsätta att anmäla per telefon. Svale konfigurerade loggen och utbildade sex medarbetare vid två tillfällen. Maya Lind, arbetsledare för underhållet, beskriver utgångspunkten i en mejlintervju:

– Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort. Kategorierna var våra; Svale hjälpte oss att lägga in dem i loggen.

## Försöksanteckningen avgränsar resultaten

Försöket pågick i åtta veckor. Enligt Elm Quays interna försöksanteckning från den 4 december 2025 registrerades 31 reparationsanmälningar. Siffran omfattar inte akuta ärenden eller arbete som beställts före försöket.

Mediantiden från anmälan till tilldelning av ärendet var två arbetsdagar under försöket, jämfört med tre under den föregående åttaveckorsperioden. Arbetsbelastningen skilde sig mellan perioderna, och anteckningen tillskriver uttryckligen inte skillnaden programvaran.

Det finns inga mätningar av kostnader, boendes nöjdhet eller tid till färdig reparation.

## Maya Lind bedömer försöket

Teamet har ännu inte utökat försöket. Beslutet ska fattas efter att teamet har kontrollerat hur kategorierna fungerar för större reparationer. Om förberedelserna skriver Maya Lind:

– Vi lade mer tid på att komma överens om kategorierna än på att registrera de första anmälningarna. Jag skulle avsätta den tiden innan försöket startar i nästa byggnad.

– Jag skulle välja att göra försöket igen. Att ha en samlad vy över anmälningarna hjälper oss, men jag skulle avsätta en extra vecka för förberedelser.

## Läs checklistan inför ett eget införande

Inför ett eget försök kan du ta med dig Linds reservation om förberedelsetiden. Vill du planera ett införande kan du läsa [Svale Systems checklista för införande](https://example.invalid/svale/checklist) som nästa steg.
```

No Text Artifact was delivered.

### User-facing reply

```text
Inga ändringar behövdes efter granskning och korrekturläsning. Texten granskades som kundcase på svenska, utan särskild teknik enligt textens metadata.
```

## sample-10

Task: source-blind review. Requested output target: response.

### Formal Invocation

```text
/redline --output=response input.md
```

### Complete supplied input

```text
---
kntnt:
  genre: casestudy
  technique: none
  language: sv
---

# Elm Quay Housing samlar anmälningar i reparationsloggen

Efter åtta veckors test i två byggnader har Elm Quay Housing både siffror och en egen bedömning att utgå från. Arbetsledaren för underhåll, Maya Lind, berättar om förberedelserna, och bolagets anteckning sätter gränserna för vilka slutsatser som kan dras. Kundfallet publiceras av leverantören Svale Systems.

Av [ditt namn]

Elm Quay Housing förvaltar 640 lägenheter. I september 2025 beslutade bolagets eget underhållsteam att testa en gemensam reparationslogg i två byggnader. Telefonanmälningar och mejl hade tidigare sparats var för sig. Teamet ville att personal på olika skift skulle kunna se samma information.

## Teamet behåller telefonanmälan för de boende

Teamet valde Svale Systems efter att ha testat om loggen kunde visa status för varje reparation. Det utformade också sina egna kategorier och höll telefonanmälan öppen för de boende.

Svale konfigurerade loggen och utbildade sex medarbetare under två tillfällen. I en mejlintervju beskriver arbetsledaren för underhåll, Maya Lind, arbetet med att komma igång:

– Vi lade mer tid på att komma överens om kategorierna än på att lägga in de första anmälningarna. Jag skulle avsätta den tiden innan nästa byggnad börjar använda loggen.

## Anteckningen jämför två perioder

Försöket pågick i åtta veckor. Enligt Elm Quay Housings interna försöksanteckning, daterad den 4 december 2025, registrerades 31 reparationsanmälningar. Akuta ärenden och arbeten som beställts före försöket ingår inte i underlaget.

Mediantiden från anmälan till tilldelning var två arbetsdagar under försöket, jämfört med tre under den föregående åttaveckorsperioden. Arbetsbelastningen skilde sig mellan perioderna. Anteckningen pekar uttryckligen inte ut programvaran som orsak till skillnaden.

Det finns inga mätningar av kostnader, de boendes nöjdhet eller tiden till slutförd reparation. Siffrorna beskriver tiden till tilldelning av arbetet.

## Maya Lind bedömer försöket inför nästa beslut

Elm Quay Housing har ännu inte utökat försöket. Teamet ska först kontrollera hur kategorierna fungerar för större reparationer och därefter besluta om försöket ska utökas.

I mejlintervjun ger Lind sin bedömning:

– Jag skulle välja att göra försöket igen. Att ha en gemensam vy över anmälningarna hjälper oss, men jag skulle avsätta en extra vecka för förberedelser.

## Läs vidare i Svale Systems checklista

För ett eget test är tiden för förberedelser en fråga att ta ställning till. Som ett frivilligt nästa steg kan du läsa [Svale Systems checklista för införande](https://example.invalid/svale/checklist).
```

### Delivered Text Artifact

```text
---
kntnt:
  genre: casestudy
  technique: none
  language: sv
---

# Elm Quay Housing samlar anmälningar i reparationsloggen

Efter åtta veckors test i två byggnader har Elm Quay Housing både siffror och en egen bedömning att utgå från. Arbetsledaren för underhåll, Maya Lind, berättar om förberedelserna, och bolagets anteckning sätter gränserna för vilka slutsatser som kan dras. Kundfallet publiceras av leverantören Svale Systems.

Av [ditt namn]

Elm Quay Housing förvaltar 640 lägenheter. I september 2025 beslutade bolagets eget underhållsteam att testa en gemensam reparationslogg i två byggnader. Telefonanmälningar och mejl hade tidigare sparats var för sig. Teamet ville att personal på olika skift skulle kunna se samma information.

## Teamet behåller telefonanmälan för de boende

Teamet valde Svale Systems efter att ha testat om loggen kunde visa status för varje reparation. Det utformade också sina egna kategorier och höll telefonanmälan öppen för de boende.

Svale konfigurerade loggen och utbildade sex medarbetare under två tillfällen. I en mejlintervju beskriver arbetsledaren för underhåll, Maya Lind, arbetet med att komma igång:

– Vi lade mer tid på att komma överens om kategorierna än på att lägga in de första anmälningarna. Jag skulle avsätta den tiden innan nästa byggnad börjar använda loggen.

## Anteckningen jämför två perioder

Försöket pågick i åtta veckor. Enligt Elm Quay Housings interna försöksanteckning, daterad den 4 december 2025, registrerades 31 reparationsanmälningar. Akuta ärenden och arbeten som beställts före försöket ingår inte i underlaget.

Mediantiden från anmälan till tilldelning var två arbetsdagar under försöket, jämfört med tre under den föregående åttaveckorsperioden. Arbetsbelastningen skilde sig mellan perioderna. Anteckningen pekar uttryckligen inte ut programvaran som orsak till skillnaden.

Det finns inga mätningar av kostnader, de boendes nöjdhet eller tiden till slutförd reparation. Siffrorna beskriver tiden till tilldelning av arbetet.

## Maya Lind bedömer försöket inför nästa beslut

Elm Quay Housing har ännu inte utökat försöket. Teamet ska först kontrollera hur kategorierna fungerar för större reparationer och därefter besluta om försöket ska utökas.

I mejlintervjun ger Lind sin bedömning:

– Jag skulle välja att göra försöket igen. Att ha en gemensam vy över anmälningarna hjälper oss, men jag skulle avsätta en extra vecka för förberedelser.

## Läs vidare i Svale Systems checklista

För ett eget test är tiden för förberedelser en fråga att ta ställning till. Som ett frivilligt nästa steg kan du läsa [Svale Systems checklista för införande](https://example.invalid/svale/checklist).
```

### User-facing reply

````text
Granskat som kundfall (casestudy) på svenska, utan skrivteknik enligt textens metadata. Texten är oförändrad efter granskning och korrekturläsning.

Två fynd är olösta:

- Författarnamn saknas: ”Av [ditt namn]” namnger ingen författare. Bylinen behöver ett namn för att läsaren ska veta vem som skrivit texten; inget namn finns att fylla i.
- Checklistelänken använder platshållaradressen `https://example.invalid/svale/checklist`. Nästa steg går därför inte att följa via länken; någon ersättningsadress är inte angiven.

Inga påståenden har tagits bort, ändrats eller lagts till.

```markdown
---
kntnt:
  genre: casestudy
  technique: none
  language: sv
---

# Elm Quay Housing samlar anmälningar i reparationsloggen

Efter åtta veckors test i två byggnader har Elm Quay Housing både siffror och en egen bedömning att utgå från. Arbetsledaren för underhåll, Maya Lind, berättar om förberedelserna, och bolagets anteckning sätter gränserna för vilka slutsatser som kan dras. Kundfallet publiceras av leverantören Svale Systems.

Av [ditt namn]

Elm Quay Housing förvaltar 640 lägenheter. I september 2025 beslutade bolagets eget underhållsteam att testa en gemensam reparationslogg i två byggnader. Telefonanmälningar och mejl hade tidigare sparats var för sig. Teamet ville att personal på olika skift skulle kunna se samma information.

## Teamet behåller telefonanmälan för de boende

Teamet valde Svale Systems efter att ha testat om loggen kunde visa status för varje reparation. Det utformade också sina egna kategorier och höll telefonanmälan öppen för de boende.

Svale konfigurerade loggen och utbildade sex medarbetare under två tillfällen. I en mejlintervju beskriver arbetsledaren för underhåll, Maya Lind, arbetet med att komma igång:

– Vi lade mer tid på att komma överens om kategorierna än på att lägga in de första anmälningarna. Jag skulle avsätta den tiden innan nästa byggnad börjar använda loggen.

## Anteckningen jämför två perioder

Försöket pågick i åtta veckor. Enligt Elm Quay Housings interna försöksanteckning, daterad den 4 december 2025, registrerades 31 reparationsanmälningar. Akuta ärenden och arbeten som beställts före försöket ingår inte i underlaget.

Mediantiden från anmälan till tilldelning var två arbetsdagar under försöket, jämfört med tre under den föregående åttaveckorsperioden. Arbetsbelastningen skilde sig mellan perioderna. Anteckningen pekar uttryckligen inte ut programvaran som orsak till skillnaden.

Det finns inga mätningar av kostnader, de boendes nöjdhet eller tiden till slutförd reparation. Siffrorna beskriver tiden till tilldelning av arbetet.

## Maya Lind bedömer försöket inför nästa beslut

Elm Quay Housing har ännu inte utökat försöket. Teamet ska först kontrollera hur kategorierna fungerar för större reparationer och därefter besluta om försöket ska utökas.

I mejlintervjun ger Lind sin bedömning:

– Jag skulle välja att göra försöket igen. Att ha en gemensam vy över anmälningarna hjälper oss, men jag skulle avsätta en extra vecka för förberedelser.

## Läs vidare i Svale Systems checklista

För ett eget test är tiden för förberedelser en fråga att ta ställning till. Som ett frivilligt nästa steg kan du läsa [Svale Systems checklista för införande](https://example.invalid/svale/checklist).
```
````

## sample-11

Task: source-blind review. Requested output target: response.

### Formal Invocation

```text
/redline --output=response input.md
```

### Complete supplied input

```text
---
kntnt:
  genre: article
  technique: none
  language: en_GB
---

# Night buses return to the Kirkwell valley route

**Kirkwell's council put four late services back on the valley route for a six-month trial. It counted 2 140 boardings, 41 per cent of them on Fridays. A decision on a permanent timetable is due in June.**

By The Newsroom

Four late buses ran between Kirkwell and Ardfern from November to April. They had left the timetable in 2023. The council paid for the trial out of its transport reserve, changed no fares, and rostered the drivers from the existing depot.

## What the counts show

The council counted 2 140 boardings on the four services over the six months. Friday accounted for 41 per cent of them. The counts exclude concessionary travel, which the operator records separately.

Passenger numbers on the daytime services did not change over the same period. The council's report does not say whether the late services drew new travellers or moved existing ones.

## Staffing the four services

The depot rostered the trial from its own drivers. No overtime figure is published.

“We wanted the rotas settled before the winter. They were, just about. After that the depot stopped ringing round at six in the morning,” said depot manager Ruth Calder.

Calder said the four services had been straightforward to staff over the trial. She would not say whether that would hold across a full year.

## What happens in June

The council decides in June whether the services stay. Its report is open for comment until 30 April, and the comments go to the committee that takes the decision. [Read the trial report and leave a comment](https://example.invalid/kirkwell/night-buses).
```

### Delivered Text Artifact

```text
---
kntnt:
  genre: article
  technique: none
  language: en_GB
---

# Night buses return to the Kirkwell valley route

**Kirkwell's council put four late services back on the valley route for a six-month trial. It counted 2,140 boardings, 41 per cent of them on Fridays. A decision on a permanent timetable is due in June.**

By The Newsroom

Four late buses ran between Kirkwell and Ardfern from November to April. They had left the timetable in 2023. The council paid for the trial out of its transport reserve, changed no fares, and rostered the drivers from the existing depot.

## Counts exclude concessionary travel

The council counted 2,140 boardings on the four services over the six months. Friday accounted for 41 per cent of them. The counts exclude concessionary travel, which the operator records separately.

Passenger numbers on the daytime services did not change over the same period. The council's report does not say whether the late services drew new travellers or moved existing ones.

## Staffing the four services

The depot rostered the trial from its own drivers. No overtime figure is published.

“We wanted the rotas settled before the winter. They were, just about. After that the depot stopped ringing round at six in the morning,” said depot manager Ruth Calder.

Calder said the four services had been straightforward to staff over the trial. She would not say whether that would hold across a full year.

## Readers can comment until 30 April

The council decides in June whether the services stay. Its report is open for comment until 30 April, and the comments go to the committee that takes the decision. [Read the trial report and leave a comment](https://example.invalid/kirkwell/night-buses).
```

### User-facing reply

````text
```markdown
---
kntnt:
  genre: article
  technique: none
  language: en_GB
---

# Night buses return to the Kirkwell valley route

**Kirkwell's council put four late services back on the valley route for a six-month trial. It counted 2,140 boardings, 41 per cent of them on Fridays. A decision on a permanent timetable is due in June.**

By The Newsroom

Four late buses ran between Kirkwell and Ardfern from November to April. They had left the timetable in 2023. The council paid for the trial out of its transport reserve, changed no fares, and rostered the drivers from the existing depot.

## Counts exclude concessionary travel

The council counted 2,140 boardings on the four services over the six months. Friday accounted for 41 per cent of them. The counts exclude concessionary travel, which the operator records separately.

Passenger numbers on the daytime services did not change over the same period. The council's report does not say whether the late services drew new travellers or moved existing ones.

## Staffing the four services

The depot rostered the trial from its own drivers. No overtime figure is published.

“We wanted the rotas settled before the winter. They were, just about. After that the depot stopped ringing round at six in the morning,” said depot manager Ruth Calder.

Calder said the four services had been straightforward to staff over the trial. She would not say whether that would hold across a full year.

## Readers can comment until 30 April

The council decides in June whether the services stay. Its report is open for comment until 30 April, and the comments go to the committee that takes the decision. [Read the trial report and leave a comment](https://example.invalid/kirkwell/night-buses).
```

Reviewed as an article in British English, with no technique, as specified in the frontmatter. No unresolved findings remain. The article conforms to the article anatomy.

- “What the counts show” named a topic without a result. Round 1 replaced it with “Counts exclude concessionary travel”, making the existing qualification explicit and narrowing the heading’s focus to that exclusion.
- “What happens in June” named a date without a decision or next step. Round 1 replaced it with “Readers can comment until 30 April”, shifting the heading from June events to reader action before the April deadline. The June decision remains in the body.

Both revised headings draw on information retained in the body. No body claims or qualifications were removed.

The run repaired the two subheadings and corrected British thousands separators in the standfirst and body. The source file is unchanged; temporary files have been removed.
````

## sample-12

Task: source-blind review. Requested output target: output.md.

### Formal Invocation

```text
/redline --output=output.md input.md
```

### Complete supplied input

```text
---
kntnt:
  genre: article
  technique: none
  language: en_GB
---

# Night buses return to the Kirkwell valley route

**Kirkwell's council put four late services back on the valley route for a six-month trial. It counted 2 140 boardings, 41 per cent of them on Fridays. A decision on a permanent timetable is due in June.**

By The Newsroom

Four late buses ran between Kirkwell and Ardfern from November to April. They had left the timetable in 2023. The council paid for the trial out of its transport reserve, changed no fares, and rostered the drivers from the existing depot.

## What the counts show

The council counted 2 140 boardings on the four services over the six months. Friday accounted for 41 per cent of them. The counts exclude concessionary travel, which the operator records separately.

Passenger numbers on the daytime services did not change over the same period. The council's report does not say whether the late services drew new travellers or moved existing ones.

## Staffing the four services

The depot rostered the trial from its own drivers. No overtime figure is published.

“We wanted the rotas settled before the winter. They were, just about. After that the depot stopped ringing round at six in the morning,” said depot manager Ruth Calder.

Calder said the four services had been straightforward to staff over the trial. She would not say whether that would hold across a full year.

## What happens in June

The council decides in June whether the services stay. Its report is open for comment until 30 April, and the comments go to the committee that takes the decision. [Read the trial report and leave a comment](https://example.invalid/kirkwell/night-buses).
```

### Delivered Text Artifact

```text
---
kntnt:
  genre: article
  technique: none
  language: en_GB
---

# Night buses return to the Kirkwell valley route

**Kirkwell's council put four late services back on the valley route for a six-month trial. It counted 2,140 boardings, 41 per cent of them on Fridays. A decision on a permanent timetable is due in June.**

By The Newsroom

Four late buses ran between Kirkwell and Ardfern from November to April. They had left the timetable in 2023. The council paid for the trial out of its transport reserve, changed no fares, and rostered the drivers from the existing depot.

## The counts exclude concessionary travel

The council counted 2,140 boardings on the four services over the six months. Friday accounted for 41 per cent of them. The counts exclude concessionary travel, which the operator records separately.

Passenger numbers on the daytime services did not change over the same period. The council's report does not say whether the late services drew new travellers or moved existing ones.

## Staffing the four services

The depot rostered the trial from its own drivers. No overtime figure is published.

“We wanted the rotas settled before the winter. They were, just about. After that the depot stopped ringing round at six in the morning,” said depot manager Ruth Calder.

Calder said the four services had been straightforward to staff over the trial. She would not say whether that would hold across a full year.

## The report is open for comment until 30 April

The council decides in June whether the services stay. Its report is open for comment until 30 April, and the comments go to the committee that takes the decision. [Read the trial report and leave a comment](https://example.invalid/kirkwell/night-buses).
```

### User-facing reply

```text
Saved [output.md](/private/var/folders/cs/vgp_x_353zd9frkjpysp7zdw0000gn/T/kntnt-native-session-ujmtutv1/work/output.md). Reviewed as an article in British English with no technique.

- “What the counts show” named a topic without a finding. Correction 1 replaced it with “The counts exclude concessionary travel,” foregrounding the existing exclusion.
- “What happens in June” withheld the answer. Correction 1 replaced it with “The report is open for comment until 30 April,” shifting the heading’s focus from the June decision to the April comment deadline.

Both replacement headings state claims already present in the body. No findings remain unresolved.

The run repaired two subheadings and corrected thousands separators in the closing proofreading pass.
```

## sample-13

Task: translation/composition. Requested output target: response.

### Formal Invocation

```text
/write --genre=casestudy --language=sv --output=response source.md
```

### Complete original source

```text
# Case-study brief and source

SYNTHETIC EVALUATION MATERIAL. This is the entire fictional source package. Source language: English. No external facts or quotations may be added.

## Brief

Write a journalistic customer case for operations managers at small housing companies. The publisher is the supplier, Svale Systems. The customer, Elm Quay Housing, should remain the acting party. Approximately 400 words, as material allows. Markdown. No author name supplied. The optional next step is the supplied implementation checklist at https://example.invalid/svale/checklist; it is a document to read, not a consultation booking or a product trial.

## Material

Elm Quay Housing manages 640 flats. In September 2025 its own maintenance team decided to trial a shared repair log in two buildings. Previously telephone reports and emails were stored separately. The team wanted staff on different shifts to see the same information. It chose Svale Systems after testing whether the log could show the status of each repair. No comparison with another supplier is available.

The maintenance team designed its categories and kept telephone reporting open for residents. Svale configured the log and trained six staff during two sessions. The trial lasted eight weeks. Elm Quay's internal trial note, 4 December 2025, says that 31 repair reports were entered. It excludes emergencies and work ordered before the trial. Median time from report to assignment was two working days during the trial and three in the preceding eight-week period. The periods had different workloads, and the note explicitly does not attribute the difference to the software. There are no cost, resident-satisfaction or completion-time measurements.

Customer interview with maintenance supervisor Maya Lind, complete usable quotations:

- “We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log.”
- “We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts.”
- “I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation.”

Lind did not recommend Svale to every housing company. Her final quotation is her actual, qualified assessment. It is not an inference from the figures. The trial has not yet expanded; the team will decide after checking how the categories work for larger repairs. The supplier approved publication of this case as supplier-published material; it is not independent journalism. All interviews occurred by email, and no physical scene, emotion or remembered dialogue is provided. Translation of the quotations is permitted, preserving stance and qualification.

## Forbidden inferences / judging

No claim that software caused the shorter assignment time, saved money, delighted residents or rescued a helpless customer. Do not turn assignment time into completion time. The customer's reservation must survive. Judge whether quotations contribute experience beyond the surrounding narrative, whether supplier narration stays in third person and whether the suggested link accurately describes its destination.
```

### Delivered Text Artifact

```text
---
kntnt:
  genre: casestudy
  technique: none
  language: sv
---

# Elm Quay Housing samlar reparationsanmälningarna i en vy

Egna kategorier och fortsatt telefonanmälan präglade Elm Quay Housings försök med en gemensam reparationslogg i två byggnader. Arbetsledaren Maya Lind ger sin bedömning av försöket, och den interna anteckningen sätter gränser för vad tidsuppgifterna kan säga.

Av användaren · Publicerat av Svale Systems

Elm Quay Housing förvaltar 640 lägenheter. I september 2025 beslutade bolagets eget underhållsteam att prova en gemensam logg för reparationer i två byggnader. Telefonanmälningar och mejl hade tidigare lagrats var för sig, och teamet ville att personal på olika skift skulle kunna se samma information.

## Underhållsteamet väljer arbetssättet

Teamet valde Svale Systems efter att ha testat om loggen kunde visa status för varje reparation. Någon jämförelse med en annan leverantör finns inte i underlaget.

De boende kunde fortsätta att anmäla per telefon. Svale konfigurerade loggen och utbildade sex medarbetare vid två tillfällen. Maya Lind, arbetsledare för underhållet, beskriver utgångspunkten i en mejlintervju:

– Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort. Kategorierna var våra; Svale hjälpte oss att lägga in dem i loggen.

## Försöksanteckningen avgränsar resultaten

Försöket pågick i åtta veckor. Enligt Elm Quays interna försöksanteckning från den 4 december 2025 registrerades 31 reparationsanmälningar. Siffran omfattar inte akuta ärenden eller arbete som beställts före försöket.

Mediantiden från anmälan till tilldelning av ärendet var två arbetsdagar under försöket, jämfört med tre under den föregående åttaveckorsperioden. Arbetsbelastningen skilde sig mellan perioderna, och anteckningen tillskriver uttryckligen inte skillnaden programvaran.

Det finns inga mätningar av kostnader, boendes nöjdhet eller tid till färdig reparation.

## Maya Lind bedömer försöket

Teamet har ännu inte utökat försöket. Beslutet ska fattas efter att teamet har kontrollerat hur kategorierna fungerar för större reparationer. Om förberedelserna skriver Maya Lind:

– Vi lade mer tid på att komma överens om kategorierna än på att registrera de första anmälningarna. Jag skulle avsätta den tiden innan försöket startar i nästa byggnad.

– Jag skulle välja att göra försöket igen. Att ha en samlad vy över anmälningarna hjälper oss, men jag skulle avsätta en extra vecka för förberedelser.

## Läs checklistan inför ett eget införande

Inför ett eget försök kan du ta med dig Linds reservation om förberedelsetiden. Vill du planera ett införande kan du läsa [Svale Systems checklista för införande](https://example.invalid/svale/checklist) som nästa steg.
```

### User-facing reply

````text
Första utkastet levereras här som ett kundcase på svenska. Genren anger ingen berättarteknik. Den slutliga källkontrollen gav inga kvarstående fynd; körningens tillfälliga filer är borttagna.

Bylinen anger användaren eftersom författarnamn saknas. Det fiktiva underlaget saknar mätningar av kostnader, boendes nöjdhet och tid till färdig reparation.

```markdown
---
kntnt:
  genre: casestudy
  technique: none
  language: sv
---

# Elm Quay Housing samlar reparationsanmälningarna i en vy

Egna kategorier och fortsatt telefonanmälan präglade Elm Quay Housings försök med en gemensam reparationslogg i två byggnader. Arbetsledaren Maya Lind ger sin bedömning av försöket, och den interna anteckningen sätter gränser för vad tidsuppgifterna kan säga.

Av användaren · Publicerat av Svale Systems

Elm Quay Housing förvaltar 640 lägenheter. I september 2025 beslutade bolagets eget underhållsteam att prova en gemensam logg för reparationer i två byggnader. Telefonanmälningar och mejl hade tidigare lagrats var för sig, och teamet ville att personal på olika skift skulle kunna se samma information.

## Underhållsteamet väljer arbetssättet

Teamet valde Svale Systems efter att ha testat om loggen kunde visa status för varje reparation. Någon jämförelse med en annan leverantör finns inte i underlaget.

De boende kunde fortsätta att anmäla per telefon. Svale konfigurerade loggen och utbildade sex medarbetare vid två tillfällen. Maya Lind, arbetsledare för underhållet, beskriver utgångspunkten i en mejlintervju:

– Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort. Kategorierna var våra; Svale hjälpte oss att lägga in dem i loggen.

## Försöksanteckningen avgränsar resultaten

Försöket pågick i åtta veckor. Enligt Elm Quays interna försöksanteckning från den 4 december 2025 registrerades 31 reparationsanmälningar. Siffran omfattar inte akuta ärenden eller arbete som beställts före försöket.

Mediantiden från anmälan till tilldelning av ärendet var två arbetsdagar under försöket, jämfört med tre under den föregående åttaveckorsperioden. Arbetsbelastningen skilde sig mellan perioderna, och anteckningen tillskriver uttryckligen inte skillnaden programvaran.

Det finns inga mätningar av kostnader, boendes nöjdhet eller tid till färdig reparation.

## Maya Lind bedömer försöket

Teamet har ännu inte utökat försöket. Beslutet ska fattas efter att teamet har kontrollerat hur kategorierna fungerar för större reparationer. Om förberedelserna skriver Maya Lind:

– Vi lade mer tid på att komma överens om kategorierna än på att registrera de första anmälningarna. Jag skulle avsätta den tiden innan försöket startar i nästa byggnad.

– Jag skulle välja att göra försöket igen. Att ha en samlad vy över anmälningarna hjälper oss, men jag skulle avsätta en extra vecka för förberedelser.

## Läs checklistan inför ett eget införande

Inför ett eget försök kan du ta med dig Linds reservation om förberedelsetiden. Vill du planera ett införande kan du läsa [Svale Systems checklista för införande](https://example.invalid/svale/checklist) som nästa steg.
```
````

## sample-14

Task: source-blind review. Requested output target: response.

### Formal Invocation

```text
/redline --genre=casestudy --output=response input.md
```

### Complete supplied input

```text
---
kntnt:
  genre: case-study
  technique: none
  language: sv
---

# Elm Quay fick en gemensam överblick över felanmälningarna

Elm Quay Housing testade en gemensam logg för felanmälningar i två byggnader. Underhållsteamet ville ge olika arbetsskift tillgång till samma information och utformade själva kategorierna. Underhållsansvariga Maya Lind skulle göra om försöket, men avsätta mer tid för förberedelser. Något beslut om att utöka försöket har ännu inte fattats.

Elm Quay Housing förvaltar 640 lägenheter. Tidigare förvarades felanmälningar via telefon och mejl separat. I september 2025 beslutade bolagets eget underhållsteam att prova en gemensam logg. Försöket pågick i åtta veckor.

– Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort. Kategorierna var våra; Svale hjälpte oss att lägga in dem i loggen, berättar Maya Lind i en mejlintervju.

Teamet valde Svale Systems efter att ha testat om loggen kunde visa statusen för varje reparation. Underlaget innehåller ingen jämförelse med någon annan leverantör.

## Teamet utformade kategorierna

Underhållsteamet tog fram kategorierna och behöll möjligheten för de boende att felanmäla via telefon. Svale konfigurerade loggen och utbildade sex medarbetare vid två tillfällen.

För Lind gav arbetet en erfarenhet att ta med till nästa byggnad:

– Vi lade mer tid på att komma överens om kategorierna än på att registrera de första felanmälningarna. Jag skulle avsätta den tiden innan nästa byggnad kommer i gång.

## Kortare tid till tilldelning under försöket

Enligt Elm Quays interna försöksanteckning, daterad den 4 december 2025, registrerades 31 felanmälningar. Akuta ärenden och arbeten som beställts före försöket ingår inte i underlaget.

Mediantiden från felanmälan till tilldelning var två arbetsdagar under försöket, jämfört med tre under den föregående åttaveckorsperioden. Arbetsbelastningen skilde sig mellan perioderna. Anteckningen tillskriver uttryckligen inte programvaran skillnaden.

Mätningen gäller alltså tiden tills ett ärende tilldelades, inte tills reparationen var klar. Det saknas mätningar av kostnader, hur nöjda de boende var och tiden till slutförd reparation.

## Lind skulle avsätta mer tid för förberedelser

Linds egen bedömning av försöket rymmer ett förbehåll:

– Jag skulle välja att göra om försöket. Det hjälper oss att ha en samlad bild av felanmälningarna, men jag skulle avsätta en extra vecka för förberedelser.

Försöket har ännu inte utökats. Teamet ska först kontrollera hur kategorierna fungerar för större reparationer och därefter fatta beslut.

För dig som vill läsa vidare finns [Svale Systems checklista för införande](https://example.invalid/svale/checklist).

*Den här kundberättelsen publiceras av leverantören Svale Systems.*

```

### Delivered Text Artifact

```text
---
kntnt:
  genre: casestudy
  technique: none
  language: sv
---

# Elm Quay fick en gemensam överblick över felanmälningarna

Elm Quay Housing testade en gemensam logg för felanmälningar i två byggnader. Underhållsteamet ville ge olika arbetsskift tillgång till samma information och utformade själva kategorierna. Underhållsansvariga Maya Lind skulle göra om försöket, men avsätta mer tid för förberedelser. Något beslut om att utöka försöket har ännu inte fattats.

Elm Quay Housing förvaltar 640 lägenheter. Tidigare förvarades felanmälningar via telefon och mejl separat. I september 2025 beslutade bolagets eget underhållsteam att prova en gemensam logg. Försöket pågick i åtta veckor.

## Teamet valde Svale Systems

– Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort. Kategorierna var våra; Svale hjälpte oss att lägga in dem i loggen, berättar Maya Lind i en mejlintervju.

Teamet valde Svale Systems efter att ha testat om loggen kunde visa statusen för varje reparation. Underlaget innehåller ingen jämförelse med någon annan leverantör.

## Svale utbildade sex medarbetare

Underhållsteamet tog fram kategorierna och behöll möjligheten för de boende att felanmäla via telefon. Svale konfigurerade loggen och utbildade sex medarbetare vid två tillfällen.

För Lind gav arbetet en erfarenhet att ta med till nästa byggnad:

– Vi lade mer tid på att komma överens om kategorierna än på att registrera de första felanmälningarna. Jag skulle avsätta den tiden innan nästa byggnad kommer i gång.

## Kortare tid till tilldelning under försöket

Enligt Elm Quays interna försöksanteckning, daterad den 4 december 2025, registrerades 31 felanmälningar. Akuta ärenden och arbeten som beställts före försöket ingår inte i underlaget.

Mediantiden från felanmälan till tilldelning var två arbetsdagar under försöket, jämfört med tre under den föregående åttaveckorsperioden. Arbetsbelastningen skilde sig mellan perioderna. Anteckningen tillskriver uttryckligen inte programvaran skillnaden.

Mätningen gäller alltså tiden tills ett ärende tilldelades, inte tills reparationen var klar. Det saknas mätningar av kostnader, hur nöjda de boende var och tiden till slutförd reparation.

## Maya Lind om försöket

Linds egen bedömning av försöket rymmer ett förbehåll:

– Jag skulle välja att göra om försöket. Det hjälper oss att ha en samlad bild av felanmälningarna, men jag skulle avsätta en extra vecka för förberedelser.

## Teamet ska kontrollera kategorierna för större reparationer

Försöket har ännu inte utökats. Teamet ska först kontrollera hur kategorierna fungerar för större reparationer och därefter fatta beslut.

För dig som vill läsa vidare finns [Svale Systems checklista för införande](https://example.invalid/svale/checklist).

*Den här kundberättelsen publiceras av leverantören Svale Systems.*

```

### User-facing reply

````text
Granskad som svensk kundberättelse (`casestudy`), utan särskild berättarteknik (`none`, enligt textens metadata).

```markdown
---
kntnt:
  genre: casestudy
  technique: none
  language: sv
---

# Elm Quay fick en gemensam överblick över felanmälningarna

Elm Quay Housing testade en gemensam logg för felanmälningar i två byggnader. Underhållsteamet ville ge olika arbetsskift tillgång till samma information och utformade själva kategorierna. Underhållsansvariga Maya Lind skulle göra om försöket, men avsätta mer tid för förberedelser. Något beslut om att utöka försöket har ännu inte fattats.

Elm Quay Housing förvaltar 640 lägenheter. Tidigare förvarades felanmälningar via telefon och mejl separat. I september 2025 beslutade bolagets eget underhållsteam att prova en gemensam logg. Försöket pågick i åtta veckor.

## Teamet valde Svale Systems

– Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort. Kategorierna var våra; Svale hjälpte oss att lägga in dem i loggen, berättar Maya Lind i en mejlintervju.

Teamet valde Svale Systems efter att ha testat om loggen kunde visa statusen för varje reparation. Underlaget innehåller ingen jämförelse med någon annan leverantör.

## Svale utbildade sex medarbetare

Underhållsteamet tog fram kategorierna och behöll möjligheten för de boende att felanmäla via telefon. Svale konfigurerade loggen och utbildade sex medarbetare vid två tillfällen.

För Lind gav arbetet en erfarenhet att ta med till nästa byggnad:

– Vi lade mer tid på att komma överens om kategorierna än på att registrera de första felanmälningarna. Jag skulle avsätta den tiden innan nästa byggnad kommer i gång.

## Kortare tid till tilldelning under försöket

Enligt Elm Quays interna försöksanteckning, daterad den 4 december 2025, registrerades 31 felanmälningar. Akuta ärenden och arbeten som beställts före försöket ingår inte i underlaget.

Mediantiden från felanmälan till tilldelning var två arbetsdagar under försöket, jämfört med tre under den föregående åttaveckorsperioden. Arbetsbelastningen skilde sig mellan perioderna. Anteckningen tillskriver uttryckligen inte programvaran skillnaden.

Mätningen gäller alltså tiden tills ett ärende tilldelades, inte tills reparationen var klar. Det saknas mätningar av kostnader, hur nöjda de boende var och tiden till slutförd reparation.

## Maya Lind om försöket

Linds egen bedömning av försöket rymmer ett förbehåll:

– Jag skulle välja att göra om försöket. Det hjälper oss att ha en samlad bild av felanmälningarna, men jag skulle avsätta en extra vecka för förberedelser.

## Teamet ska kontrollera kategorierna för större reparationer

Försöket har ännu inte utökats. Teamet ska först kontrollera hur kategorierna fungerar för större reparationer och därefter fatta beslut.

För dig som vill läsa vidare finns [Svale Systems checklista för införande](https://example.invalid/svale/checklist).

*Den här kundberättelsen publiceras av leverantören Svale Systems.*

```

Olöst: byline saknas. Texten namnger ingen författare, så författarraden har lämnats ofylld.

Ändrade mellanrubriker och deras påståenden:

- I originalet upprepade ”Teamet utformade kategorierna” första meningens uppgift om vem som tog fram kategorierna. ”Svale utbildade sex medarbetare” anger nu utbildningen, en uppgift som redan fanns i brödtexten. Beskedet om teamets ansvar för kategorierna finns kvar i brödtexten.
- I originalet föregrep ”Lind skulle avsätta mer tid för förberedelser” citatets förbehåll. ”Maya Lind om försöket” anger nu talare och ämne. Beskedet om mer förberedelsetid har tagits bort ur rubriken och finns kvar i ingressen och citatet.

Befintliga uppgifter upprepade i nya mellanrubriker:

- ”Teamet valde Svale Systems” ger motivet och leverantörsvalet en sektionsingång direkt efter inledningsstycket. Det reparerar originalets inledning på tre stycken och återger det leverantörsval som redan stod i brödtexten.
- ”Teamet ska kontrollera kategorierna för större reparationer” ger det befintliga avslutningsinnehållet en egen sektion efter kundens bedömning. Rubriken återger den planerade kontrollen från brödtexten; ordningen kontroll först, beslut därefter står kvar där.

Jag har ändrat mellanrubriker och sektionsindelning samt synkroniserat genrevärdet i metadata till `casestudy`. Ingressen och brödtexten, inklusive citat, länkar och förbehåll, är oförändrade. Korrekturpasset gav inga mekaniska rättelser. `input.md` är orörd och inga tillfälliga filer finns kvar.
````

## sample-15

Task: translation/composition. Requested output target: response.

### Formal Invocation

```text
/write --genre=casestudy --language=sv --output=response source.md
```

### Complete original source

```text
# Case-study brief and source

SYNTHETIC EVALUATION MATERIAL. This is the entire fictional source package. Source language: English. No external facts or quotations may be added.

## Brief

Write a journalistic customer case for operations managers at small housing companies. The publisher is the supplier, Svale Systems. The customer, Elm Quay Housing, should remain the acting party. Approximately 400 words, as material allows. Markdown. No author name supplied. The optional next step is the supplied implementation checklist at https://example.invalid/svale/checklist; it is a document to read, not a consultation booking or a product trial.

## Material

Elm Quay Housing manages 640 flats. In September 2025 its own maintenance team decided to trial a shared repair log in two buildings. Previously telephone reports and emails were stored separately. The team wanted staff on different shifts to see the same information. It chose Svale Systems after testing whether the log could show the status of each repair. No comparison with another supplier is available.

The maintenance team designed its categories and kept telephone reporting open for residents. Svale configured the log and trained six staff during two sessions. The trial lasted eight weeks. Elm Quay's internal trial note, 4 December 2025, says that 31 repair reports were entered. It excludes emergencies and work ordered before the trial. Median time from report to assignment was two working days during the trial and three in the preceding eight-week period. The periods had different workloads, and the note explicitly does not attribute the difference to the software. There are no cost, resident-satisfaction or completion-time measurements.

Customer interview with maintenance supervisor Maya Lind, complete usable quotations:

- “We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log.”
- “We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts.”
- “I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation.”

Lind did not recommend Svale to every housing company. Her final quotation is her actual, qualified assessment. It is not an inference from the figures. The trial has not yet expanded; the team will decide after checking how the categories work for larger repairs. The supplier approved publication of this case as supplier-published material; it is not independent journalism. All interviews occurred by email, and no physical scene, emotion or remembered dialogue is provided. Translation of the quotations is permitted, preserving stance and qualification.

## Forbidden inferences / judging

No claim that software caused the shorter assignment time, saved money, delighted residents or rescued a helpless customer. Do not turn assignment time into completion time. The customer's reservation must survive. Judge whether quotations contribute experience beyond the surrounding narrative, whether supplier narration stays in third person and whether the suggested link accurately describes its destination.
```

### Delivered Text Artifact

```text
---
kntnt:
  genre: casestudy
  technique: none
  language: sv
---

# Elm Quay Housing samlar reparationsanmälningarna i en vy

Under åtta veckor prövade Elm Quay Housing en reparationslogg från Svale Systems i två hus. Bolagets uppföljning visar en tidsskillnad mellan två perioder, utan att tillskriva den programvaran. Svale Systems publicerar kundfallet som leverantör.

Av [ditt namn]

Telefonanmälningar och mejl hade tidigare sparats var för sig hos Elm Quay Housing, som förvaltar 640 lägenheter. I september 2025 beslutade bolagets eget underhållsteam att testa en gemensam logg så att personal på olika skift skulle se samma information.

## Teamet behöll telefonanmälningarna

Valet föll på Svale Systems efter att teamet hade testat om loggen kunde visa status för varje reparation. Någon jämförelse med en annan leverantör finns inte i underlaget. Arbetsledaren för underhåll, Maya Lind, beskriver utgångspunkten i en mejlintervju:

– Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort. Kategorierna var våra; Svale hjälpte oss att lägga in dem i loggen.

De boende kunde fortsätta att göra anmälningar per telefon.

## Teamet prövade arbetssättet i åtta veckor

Svale konfigurerade loggen och utbildade sex medarbetare vid två tillfällen. I intervjun beskriver Maya Lind också förberedelserna:

– Vi lade mer tid på att komma överens om kategorierna än på att registrera de första anmälningarna. Jag skulle avsätta den tiden innan det är dags för nästa hus.

## Uppföljningen lämnar programvarans effekt öppen

Elm Quay Housings interna anteckning om försöket, daterad den 4 december 2025, anger att 31 reparationsanmälningar registrerades. Akuta ärenden och arbeten som beställts före försöket ingår inte.

Mediantiden från anmälan till tilldelning av ärendet var två arbetsdagar under försöket, jämfört med tre under de föregående åtta veckorna. Perioderna hade olika arbetsbelastning. Anteckningen tillskriver uttryckligen inte programvaran skillnaden.

Det saknas mätningar av kostnader, de boendes nöjdhet och tiden till färdig reparation.

## Elm Quay Housing avvaktar en utökning

Nästa fråga för teamet är hur kategorierna fungerar för större reparationer. Först efter den kontrollen beslutar teamet om en utökning. Maya Lind ger sin egen bedömning av försöket:

– Jag skulle välja att göra försöket igen. Att ha en samlad vy över anmälningarna hjälper oss, men jag skulle avsätta en extra vecka för förberedelser.

## Du kan läsa vidare inför ett införande

För ett eget upplägg är både förberedelserna och uppföljningens begränsningar värda att ta med i planeringen. Du kan läsa [Svale Systems checklista för införande](https://example.invalid/svale/checklist).
```

### User-facing reply

````text
Utkastet levereras med en känd brist: ”avvaktar en utökning” och ”beslutar teamet om en utökning” kan antyda ett positivt beslut, medan underlaget lämnar utfallet öppet. Kontrollens föreslagna rättelse är ”Teamet ska ta ställning till en utökning” respektive ”Efter den kontrollen beslutar teamet om försöket ska utökas”.

Kundfallet på svenska följer nedan, utan särskild teknik enligt genrens standard. Två käll- och citatkontroller har genomförts. Författarnamn saknas; bylinen har en platshållare för ditt namn. Underlaget saknar kostnads-, nöjdhets- och färdigställandemätningar. Tillfälliga filer är borttagna.

```markdown
---
kntnt:
  genre: casestudy
  technique: none
  language: sv
---

# Elm Quay Housing samlar reparationsanmälningarna i en vy

Under åtta veckor prövade Elm Quay Housing en reparationslogg från Svale Systems i två hus. Bolagets uppföljning visar en tidsskillnad mellan två perioder, utan att tillskriva den programvaran. Svale Systems publicerar kundfallet som leverantör.

Av [ditt namn]

Telefonanmälningar och mejl hade tidigare sparats var för sig hos Elm Quay Housing, som förvaltar 640 lägenheter. I september 2025 beslutade bolagets eget underhållsteam att testa en gemensam logg så att personal på olika skift skulle se samma information.

## Teamet behöll telefonanmälningarna

Valet föll på Svale Systems efter att teamet hade testat om loggen kunde visa status för varje reparation. Någon jämförelse med en annan leverantör finns inte i underlaget. Arbetsledaren för underhåll, Maya Lind, beskriver utgångspunkten i en mejlintervju:

– Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort. Kategorierna var våra; Svale hjälpte oss att lägga in dem i loggen.

De boende kunde fortsätta att göra anmälningar per telefon.

## Teamet prövade arbetssättet i åtta veckor

Svale konfigurerade loggen och utbildade sex medarbetare vid två tillfällen. I intervjun beskriver Maya Lind också förberedelserna:

– Vi lade mer tid på att komma överens om kategorierna än på att registrera de första anmälningarna. Jag skulle avsätta den tiden innan det är dags för nästa hus.

## Uppföljningen lämnar programvarans effekt öppen

Elm Quay Housings interna anteckning om försöket, daterad den 4 december 2025, anger att 31 reparationsanmälningar registrerades. Akuta ärenden och arbeten som beställts före försöket ingår inte.

Mediantiden från anmälan till tilldelning av ärendet var två arbetsdagar under försöket, jämfört med tre under de föregående åtta veckorna. Perioderna hade olika arbetsbelastning. Anteckningen tillskriver uttryckligen inte programvaran skillnaden.

Det saknas mätningar av kostnader, de boendes nöjdhet och tiden till färdig reparation.

## Elm Quay Housing avvaktar en utökning

Nästa fråga för teamet är hur kategorierna fungerar för större reparationer. Först efter den kontrollen beslutar teamet om en utökning. Maya Lind ger sin egen bedömning av försöket:

– Jag skulle välja att göra försöket igen. Att ha en samlad vy över anmälningarna hjälper oss, men jag skulle avsätta en extra vecka för förberedelser.

## Du kan läsa vidare inför ett införande

För ett eget upplägg är både förberedelserna och uppföljningens begränsningar värda att ta med i planeringen. Du kan läsa [Svale Systems checklista för införande](https://example.invalid/svale/checklist).
```
````

## sample-16

Task: source-blind review. Requested output target: response.

### Formal Invocation

```text
/redline --output=response input.md
```

### Complete supplied input

```text
# Elm Quay samlade reparationsärendena

**Elm Quay Housing provade en gemensam reparationslogg i två hus. Arbetsledaren Maya Lind vill göra om försöket, men skulle avsätta mer tid för förberedelser.**

För Elm Quays underhållsgrupp handlade försöket om att se samma information över skiftgränserna. Gruppen valde kategorierna; leverantören Svale konfigurerade loggen och utbildade sex medarbetare.

– Vi lade mer tid på att enas om kategorierna än på att lägga in de första ärendena. Den tiden skulle jag avsätta innan nästa hus börjar, säger Maya Lind.

## Två perioder med olika arbetsbelastning

Enligt Elm Quays interna försöksanteckning från den 4 december 2025 registrerades 31 ärenden under åtta veckor. Akuta ärenden och tidigare beställda arbeten ingick inte. Mediantiden från anmälan till tilldelning var två arbetsdagar, jämfört med tre under de föregående åtta veckorna.

Perioderna hade olika arbetsbelastning. Anteckningen tillskriver därför inte skillnaden programvaran.

## Kunden vill ge förberedelserna mer tid

– Jag skulle välja att göra försöket igen. Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Lind.

Kundcaset publiceras av leverantören Svale. [Läs Svales checklista för införandet](https://example.invalid/svale/checklist).
```

### Delivered Text Artifact

```text
# Elm Quay samlade reparationsärendena

**Elm Quay Housing provade en gemensam reparationslogg i två hus. Arbetsledaren Maya Lind vill göra om försöket, men skulle avsätta mer tid för förberedelser.**

För Elm Quays underhållsgrupp handlade försöket med en gemensam reparationslogg om att se samma information över skiftgränserna. Gruppen valde kategorierna; leverantören Svale konfigurerade loggen och utbildade sex medarbetare.

## Maya Lind om kategorierna

– Vi lade mer tid på att enas om kategorierna än på att lägga in de första ärendena. Den tiden skulle jag avsätta innan nästa hus börjar använda loggen, säger Maya Lind.

## Två perioder med olika arbetsbelastning

Enligt Elm Quays interna försöksanteckning från den 4 december 2025 registrerades 31 ärenden under åtta veckor. Akuta ärenden och tidigare beställda arbeten ingick inte. Mediantiden från anmälan till tilldelning var två arbetsdagar, jämfört med tre under de föregående åtta veckorna.

Perioderna hade olika arbetsbelastning. Anteckningen tillskriver därför inte skillnaden programvaran.

## Maya Lind om ett nytt försök

– Jag skulle välja att göra försöket igen. Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Lind.

Kundcaset publiceras av leverantören Svale. [Läs Svales checklista för införandet](https://example.invalid/svale/checklist).
```

### User-facing reply

````text
Granskat som kundcase (`casestudy`) på svenska (`sv`), utan teknik.

```markdown
# Elm Quay samlade reparationsärendena

**Elm Quay Housing provade en gemensam reparationslogg i två hus. Arbetsledaren Maya Lind vill göra om försöket, men skulle avsätta mer tid för förberedelser.**

För Elm Quays underhållsgrupp handlade försöket med en gemensam reparationslogg om att se samma information över skiftgränserna. Gruppen valde kategorierna; leverantören Svale konfigurerade loggen och utbildade sex medarbetare.

## Maya Lind om kategorierna

– Vi lade mer tid på att enas om kategorierna än på att lägga in de första ärendena. Den tiden skulle jag avsätta innan nästa hus börjar använda loggen, säger Maya Lind.

## Två perioder med olika arbetsbelastning

Enligt Elm Quays interna försöksanteckning från den 4 december 2025 registrerades 31 ärenden under åtta veckor. Akuta ärenden och tidigare beställda arbeten ingick inte. Mediantiden från anmälan till tilldelning var två arbetsdagar, jämfört med tre under de föregående åtta veckorna.

Perioderna hade olika arbetsbelastning. Anteckningen tillskriver därför inte skillnaden programvaran.

## Maya Lind om ett nytt försök

– Jag skulle välja att göra försöket igen. Att ha en gemensam bild av ärendena hjälper oss, men jag skulle lägga till en vecka för förberedelser, säger Lind.

Kundcaset publiceras av leverantören Svale. [Läs Svales checklista för införandet](https://example.invalid/svale/checklist).
```

Fynd:

- **Olöst:** byline saknas. Texten anger ingen författare, så namnuppgiften lämnas åt skribenten.
- **Rättat:** första citatet har fått mellanrubriken ”Maya Lind om kategorierna”, eftersom ursprungstextens två stycken före första mellanrubriken bröt mot kravet på en lead på ett stycke.
- **Rättat:** leaden namnger nu försöket med en gemensam reparationslogg, så referensen kan förstås utan ingressen.
- **Rättat:** den outtalade aktiviteten efter ”börjar” i första citatet har preciserats.
- **Rättat:** slutmellanrubriken ”Maya Lind om ett nytt försök” ersätter en rubrik som föregrep citatets reservation om mer förberedelsetid.

Ändrade påståenden:

- Förtydligandet i första citatet anger nu att ”börjar” avser att använda loggen.
- Slutmellanrubriken anger nu att Maya Lind uttalar sig om ett nytt försök. Det tidigare rubrikpåståendet om mer förberedelsetid har ersatts där; önskemålet finns kvar i ingressen och slutcitatet. Ändringen reparerar rubrikens upprepning av citatets reservation.

Tillagt påstående: mellanrubriken ”Maya Lind om kategorierna” ramar in avsnittet som hennes uttalande om kategorierna. Den tillkom för att avskilja citatet från leaden.

Granskningen har förtydligat referenser, gett första citatet en egen sektion och ändrat slutmellanrubriken. Den avslutande korrekturpassagen gjorde inga ytterligare ändringar.
````

## sample-17

Task: source-blind review. Requested output target: response.

### Formal Invocation

```text
/redline --genre=casestudy --output=response input.md
```

### Complete supplied input

```text
---
kntnt:
  genre: case-study
  technique: none
  language: sv
---

# Hamnfrakt flyttade lagersaldot till ett system

**Två av Hamnfrakt AB:s lager fick ett gemensamt system för lagersaldot. Överföringen tog sex veckor med dubbel registrering. Lagerchefen Ove Ranneby skulle göra om den, men börja med färre artikelgrupper.**

Text: Redaktionen

Hamnfrakt AB hanterar reservdelar åt verkstäder i Norrland och har omkring 9 000 artiklar i sitt sortiment. Tidigare fördes saldot för de två lagren i varsitt kalkylark, och den som ringde fick vänta medan någon slog upp siffran på rätt ställe.

## Sex veckor med dubbel registrering

Hamnfrakt valde Saldo Nord efter att ha provat om systemet kunde visa samma saldo för båda lagren. Någon jämförelse med en annan leverantör finns inte i underlaget.

Under sex veckor registrerade personalen varje uttag både i kalkylarken och i det nya systemet. Därefter fördes kalkylarken över och stängdes.

– Vi körde parallellt i sex veckor. Sedan gick lagret över, och först då såg vi hur mycket som hade legat i pärmar, säger Ove Ranneby.

## Vad överföringen visade

Enligt Hamnfrakts egen överföringsanteckning från den 12 januari 2026 saknade 340 av artiklarna en plats i det nya systemet. Artiklar som redan var utgångna ingår inte i den siffran.

Anteckningen redovisar ingen mätning av hur lång tid en förfrågan tar i dag, och ingen jämförelse med tiden före överföringen. Företaget har inte heller följt upp vad överföringen kostade.

## Företaget vill börja mindre nästa gång

– Jag skulle göra om det. Att se samma saldo för båda lagren hjälper oss, men jag skulle ta en artikelgrupp i taget, säger Ranneby.

Det tredje lagret är ännu inte överfört. Hamnfrakt ska först se hur de 340 artiklarna faller på plats. [Läs Saldo Nords checklista för överföringen](https://example.invalid/saldonord/checklista).
```

### Delivered Text Artifact

```text
---
kntnt:
  genre: casestudy
  technique: none
  language: sv
---

# Hamnfrakts anteckning redovisar 340 artiklar utan plats

**Två av Hamnfrakt AB:s lager fick ett gemensamt system för lagersaldot. Överföringen tog sex veckor med dubbel registrering. Lagerchefen Ove Ranneby skulle göra om den, men börja med färre artikelgrupper.**

Text: Redaktionen

Hamnfrakt AB hanterar reservdelar åt verkstäder i Norrland och har omkring 9 000 artiklar i sitt sortiment. Tidigare fördes saldot för de två lagren i varsitt kalkylark, och den som ringde fick vänta medan någon slog upp siffran på rätt ställe.

## Ove Ranneby beskriver övergången

Hamnfrakt valde Saldo Nord efter att ha provat om systemet kunde visa samma saldo för båda lagren. Någon jämförelse med en annan leverantör finns inte i underlaget.

– Vi körde parallellt i sex veckor. Sedan gick lagret över, och först då såg vi hur mycket som hade legat i pärmar, säger Ove Ranneby.

Personalen registrerade varje uttag både i kalkylarken och i det nya systemet. Därefter fördes kalkylarken över och stängdes.

## Överföringsanteckningen redovisar ingen tidsjämförelse

Enligt Hamnfrakts egen överföringsanteckning från den 12 januari 2026 saknade 340 av artiklarna en plats i det nya systemet. Artiklar som redan var utgångna ingår inte i den siffran.

Anteckningen redovisar ingen mätning av hur lång tid en förfrågan tar i dag, och ingen jämförelse med tiden före överföringen. Företaget har inte heller följt upp vad överföringen kostade.

## Ranneby bedömer överföringen

– Jag skulle göra om det. Att se samma saldo för båda lagren hjälper oss, men jag skulle ta en artikelgrupp i taget, säger Ranneby.

Det tredje lagret är ännu inte överfört. Hamnfrakt ska först se hur de 340 artiklarna faller på plats. [Läs Saldo Nords checklista för överföringen](https://example.invalid/saldonord/checklista).
```

### User-facing reply

````text
Granskat som kundcase (`casestudy`) på svenska (`sv`), utan berättarteknik (`none`) enligt textens metadata. En korrigeringsomgång har genomförts.

```markdown
---
kntnt:
  genre: casestudy
  technique: none
  language: sv
---

# Hamnfrakts anteckning redovisar 340 artiklar utan plats

**Två av Hamnfrakt AB:s lager fick ett gemensamt system för lagersaldot. Överföringen tog sex veckor med dubbel registrering. Lagerchefen Ove Ranneby skulle göra om den, men börja med färre artikelgrupper.**

Text: Redaktionen

Hamnfrakt AB hanterar reservdelar åt verkstäder i Norrland och har omkring 9 000 artiklar i sitt sortiment. Tidigare fördes saldot för de två lagren i varsitt kalkylark, och den som ringde fick vänta medan någon slog upp siffran på rätt ställe.

## Ove Ranneby beskriver övergången

Hamnfrakt valde Saldo Nord efter att ha provat om systemet kunde visa samma saldo för båda lagren. Någon jämförelse med en annan leverantör finns inte i underlaget.

– Vi körde parallellt i sex veckor. Sedan gick lagret över, och först då såg vi hur mycket som hade legat i pärmar, säger Ove Ranneby.

Personalen registrerade varje uttag både i kalkylarken och i det nya systemet. Därefter fördes kalkylarken över och stängdes.

## Överföringsanteckningen redovisar ingen tidsjämförelse

Enligt Hamnfrakts egen överföringsanteckning från den 12 januari 2026 saknade 340 av artiklarna en plats i det nya systemet. Artiklar som redan var utgångna ingår inte i den siffran.

Anteckningen redovisar ingen mätning av hur lång tid en förfrågan tar i dag, och ingen jämförelse med tiden före överföringen. Företaget har inte heller följt upp vad överföringen kostade.

## Ranneby bedömer överföringen

– Jag skulle göra om det. Att se samma saldo för båda lagren hjälper oss, men jag skulle ta en artikelgrupp i taget, säger Ranneby.

Det tredje lagret är ännu inte överfört. Hamnfrakt ska först se hur de 340 artiklarna faller på plats. [Läs Saldo Nords checklista för överföringen](https://example.invalid/saldonord/checklista).
```

Reparerat i omgång 1, med ändrade rubrikpåståenden:

- Huvudrubriken upprepade ingressens systembyte. Den säger nu att Hamnfrakts anteckning redovisar 340 artiklar utan plats. Uppgiften har återgetts även i rubriken, men avgränsningen ”i det nya systemet” har inte följt med. ”Utan plats” kan därför också läsas som att en fysisk plats saknas. Avgränsningen, datumet och undantaget för utgångna artiklar står kvar i brödtexten.
- ”Sex veckor med dubbel registrering” föregrep tidsuppgiften i citatet. Rubriken säger nu att Ove Ranneby beskriver övergången och lämnar tidsuppgiften åt honom.
- ”Vad överföringen visade” gav inget besked om vad som hade framkommit. Rubriken säger nu att överföringsanteckningen inte redovisar någon tidsjämförelse, en uppgift som även står kvar i brödtexten.
- ”Företaget vill börja mindre nästa gång” föregrep Rannebys reservation och gjorde hans villkorliga omdöme till en företagsavsikt. Rubriken säger nu att Ranneby bedömer överföringen.

Borttagna påståenden i omgång 1:

- Sista mellanrubrikens påstående om att företaget vill börja mindre. Rannebys personliga ”jag skulle ta en artikelgrupp i taget” står kvar.
- Andra mellanrubrikens framställning av avsnittets uppgifter som något överföringen visade. Rubriken anger nu i stället en begränsning i vad överföringsanteckningen redovisar.

Registreringsstycket stod som upprepande citatbrygga och har flyttats efter citatet. Tidsfrasen ”Under sex veckor” togs bort ur stycket i omgång 1. Läsaren har där inte längre en uttrycklig tidsavgränsning; sexveckorsperioden framgår fortfarande av ingressen och det föregående citatet.

Olöst: Första citatets ”lagret” och ”hur mycket som hade legat i pärmar” har oklara referenter. Läsaren får inte veta säkert vilket lager eller vad mängden avser. Citatet har därför lämnats oförändrat.

Rubrikerna har reparerats och ett berättarstycke har flyttats, med en upprepad tidsfras borttagen. Metadatafältet `genre` har synkroniserats till `casestudy`. Den avslutande mekaniska korrekturen gjorde inga ändringar.
````

## sample-18

Task: source-blind review. Requested output target: output.md.

### Formal Invocation

```text
/redline --genre=casestudy --output=output.md input.md
```

### Complete supplied input

```text
---
kntnt:
  genre: case-study
  technique: none
  language: sv
---

# Björkängsskolan bokar vikarier på en kvart

**Två arbetslag på Björkängsskolan provade en gemensam vikarielista under åtta veckor. Mediantiden till tillsatt pass var 15 minuter under försöket. Rektor Nina Falk skulle göra om det, men avsätta mer tid åt rutinerna.**

Text: Redaktionen

Björkängsskolan har 410 elever och 38 lärare. Tidigare ringde expeditionen runt bland kända vikarier varje morgon, och de två arbetslagen förde egna listor. Skolan ville att båda arbetslagen skulle se samma uppgifter och valde Vikarieportalen efter att ha provat om listan kunde visa vem som redan tackat ja.

## Arbetslagen utformade själva kategorierna

Skolan tog fram kategorierna för ämne och årskurs och behöll möjligheten att ringa. Vikarieportalen lade upp listan och gick igenom den med sex medarbetare vid två tillfällen.

– Vi ville ha rutinen på plats innan terminen drog i gång. Det hann vi inte riktigt, men expeditionen märkte skillnaden redan första veckan, säger Nina Falk.

## Kortare tid till tillsatt pass under försöket

Enligt skolans egen försöksanteckning från den 3 mars 2026 tillsattes 52 pass under de åtta veckorna. Akuta sjukanmälningar efter klockan åtta ingår inte i underlaget.

Mediantiden från anmälan till tillsatt pass var 15 minuter under försöket, mot 40 minuter under de åtta veckorna dessförinnan. Perioderna hade olika sjukfrånvaro, och anteckningen tillskriver därför inte listan skillnaden.

Måttet gäller tiden tills ett pass var tillsatt, inte hur undervisningen fungerade. Det saknas mätningar av kostnader och av hur eleverna eller lärarna upplevde försöket.

## Skolan vill ge rutinerna mer tid

– Jag skulle välja att göra om försöket. Att alla ser samma lista hjälper oss, men jag skulle lägga en vecka till på rutinerna, säger Falk.

Försöket har ännu inte utökats till fler arbetslag. Skolan ska först se hur listan fungerar under en hel termin. [Läs Vikarieportalens checklista för införandet](https://example.invalid/vikarieportalen/checklista).
```

### Delivered Text Artifact

```text
---
kntnt:
  genre: casestudy
  technique: none
  language: sv
---

# Björkängsskolan redovisar 52 tillsatta pass i vikarieförsök

**Två arbetslag på Björkängsskolan provade en gemensam vikarielista under åtta veckor. Mediantiden till tillsatt pass var 15 minuter under försöket. Rektor Nina Falk skulle göra om det, men avsätta mer tid åt rutinerna.**

Text: Redaktionen

Björkängsskolan har 410 elever och 38 lärare. Tidigare ringde expeditionen runt bland kända vikarier varje morgon, och de två arbetslagen förde egna listor. Skolan ville att båda arbetslagen skulle se samma uppgifter och valde Vikarieportalen efter att ha provat om listan kunde visa vem som redan tackat ja.

## Vikarieportalen gick igenom listan vid två tillfällen

Skolan tog fram kategorierna för ämne och årskurs och behöll möjligheten att ringa. Vikarieportalen lade upp listan och gick igenom den med sex medarbetare vid två tillfällen.

– Vi ville ha rutinen på plats innan terminen drog i gång. Det hann vi inte riktigt, men expeditionen märkte skillnaden redan första veckan, säger Nina Falk.

## Kortare tid till tillsatt pass under försöket

Enligt skolans egen försöksanteckning från den 3 mars 2026 tillsattes 52 pass under de åtta veckorna. Akuta sjukanmälningar efter klockan åtta ingår inte i underlaget.

Mediantiden från anmälan till tillsatt pass var 15 minuter under försöket, mot 40 minuter under de åtta veckorna dessförinnan. Perioderna hade olika sjukfrånvaro, och anteckningen tillskriver därför inte listan skillnaden.

Måttet gäller tiden tills ett pass var tillsatt, inte hur undervisningen fungerade. Det saknas mätningar av kostnader och av hur eleverna eller lärarna upplevde försöket.

## Nina Falk ser tillbaka på försöket

– Jag skulle välja att göra om försöket. Att alla ser samma lista hjälper oss, men jag skulle lägga en vecka till på rutinerna, säger Falk.

Försöket har ännu inte utökats till fler arbetslag. Skolan ska först se hur listan fungerar under en hel termin. [Läs Vikarieportalens checklista för införandet](https://example.invalid/vikarieportalen/checklista).
```

### User-facing reply

```text
Sparat i [output.md](/private/var/folders/cs/vgp_x_353zd9frkjpysp7zdw0000gn/T/kntnt-native-session-ui0bdkvx/work/output.md). Granskat som `casestudy` på svenska, utan särskild teknik enligt metadata. Inga fynd kvarstår; artikelanatomin är uppfylld.

Åtgärdade rubrikfynd och ändrade påståenden:

- Originalets huvudrubrik generaliserade försökets median till en allmän kvartstid. Den anger nu skolans redovisade 52 tillsatta pass i försöket; uppgiften står kvar i brödtexten.
- Originalets första mellanrubrik upprepade sektionsöppningen. Den anger nu Vikarieportalens två genomgångar av listan, vilket också står kvar i brödtexten.
- Originalets sista mellanrubrik föregrep rektorns reservation och gjorde hennes villkorade omdöme till skolans avsikt. Den namnger nu Nina Falks återblick och lämnar omdömet till citatet.

Borttagna rubrikpåståenden i samma korrigeringsomgång:

- Den generella kvartstiden. Försökets median och avgränsningar står kvar.
- Att arbetslagen själva utformade kategorierna, som uttrycklig uppgift i mellanrubriken. Brödtextens uppgift om skolans utformning står kvar.
- Att skolan vill ge rutinerna mer tid. Falks villkorade önskemål står kvar.

Tillagd inramning: sista mellanrubriken beskriver Falks omdöme som en återblick på försöket.

Rubrikerna har reparerats mot övergeneralisering, upprepning och ett föregripet citatomdöme. Metadata har synkroniserats från `case-study` till `casestudy`. Ingress, brödtext, citat och förbehåll är oförändrade; den avslutande korrekturläsningen krävde inga rättelser.
```

## sample-19

Task: source-blind review. Requested output target: response.

### Formal Invocation

```text
/redline --genre=casestudy --output=response input.md
```

### Complete supplied input

```text
---
kntnt:
  genre: case-study
  technique: none
  language: sv
---

# Björkängsskolan bokar vikarier på en kvart

**Två arbetslag på Björkängsskolan provade en gemensam vikarielista under åtta veckor. Mediantiden till tillsatt pass var 15 minuter under försöket. Rektor Nina Falk skulle göra om det, men avsätta mer tid åt rutinerna.**

Text: Redaktionen

Björkängsskolan har 410 elever och 38 lärare. Tidigare ringde expeditionen runt bland kända vikarier varje morgon, och de två arbetslagen förde egna listor. Skolan ville att båda arbetslagen skulle se samma uppgifter och valde Vikarieportalen efter att ha provat om listan kunde visa vem som redan tackat ja.

## Arbetslagen utformade själva kategorierna

Skolan tog fram kategorierna för ämne och årskurs och behöll möjligheten att ringa. Vikarieportalen lade upp listan och gick igenom den med sex medarbetare vid två tillfällen.

– Vi ville ha rutinen på plats innan terminen drog i gång. Det hann vi inte riktigt, men expeditionen märkte skillnaden redan första veckan, säger Nina Falk.

## Kortare tid till tillsatt pass under försöket

Enligt skolans egen försöksanteckning från den 3 mars 2026 tillsattes 52 pass under de åtta veckorna. Akuta sjukanmälningar efter klockan åtta ingår inte i underlaget.

Mediantiden från anmälan till tillsatt pass var 15 minuter under försöket, mot 40 minuter under de åtta veckorna dessförinnan. Perioderna hade olika sjukfrånvaro, och anteckningen tillskriver därför inte listan skillnaden.

Måttet gäller tiden tills ett pass var tillsatt, inte hur undervisningen fungerade. Det saknas mätningar av kostnader och av hur eleverna eller lärarna upplevde försöket.

## Skolan vill ge rutinerna mer tid

– Jag skulle välja att göra om försöket. Att alla ser samma lista hjälper oss, men jag skulle lägga en vecka till på rutinerna, säger Falk.

Försöket har ännu inte utökats till fler arbetslag. Skolan ska först se hur listan fungerar under en hel termin. [Läs Vikarieportalens checklista för införandet](https://example.invalid/vikarieportalen/checklista).
```

### Delivered Text Artifact

```text
---
kntnt:
  genre: casestudy
  technique: none
  language: sv
---

# Vikarielistan hjälper Björkängsskolan, säger rektorn

**Två arbetslag på Björkängsskolan provade en gemensam vikarielista under åtta veckor. Mediantiden till tillsatt pass var 15 minuter under försöket. Rektor Nina Falk skulle göra om det, men avsätta mer tid åt rutinerna.**

Text: Redaktionen

Björkängsskolan har 410 elever och 38 lärare. Tidigare ringde expeditionen runt bland kända vikarier varje morgon, och de två arbetslagen förde egna listor. Skolan ville att båda arbetslagen skulle se samma uppgifter och valde Vikarieportalen efter att ha provat om listan kunde visa vem som redan tackat ja.

## Vikarieportalen gick igenom listan vid två tillfällen

Skolan tog fram kategorierna för ämne och årskurs och behöll möjligheten att ringa. Vikarieportalen lade upp listan och gick igenom den med sex medarbetare vid två tillfällen.

– Vi ville ha rutinen på plats innan terminen drog i gång. Det hann vi inte riktigt, men expeditionen märkte skillnaden redan första veckan, säger Nina Falk.

## Kortare tid till tillsatt pass under försöket

Enligt skolans egen försöksanteckning från den 3 mars 2026 tillsattes 52 pass under de åtta veckorna. Akuta sjukanmälningar efter klockan åtta ingår inte i underlaget.

Mediantiden från anmälan till tillsatt pass var 15 minuter under försöket, mot 40 minuter under de åtta veckorna dessförinnan. Perioderna hade olika sjukfrånvaro, och anteckningen tillskriver därför inte listan skillnaden.

Måttet gäller tiden tills ett pass var tillsatt, inte hur undervisningen fungerade. Det saknas mätningar av kostnader och av hur eleverna eller lärarna upplevde försöket.

## Nina Falk ser tillbaka på försöket

– Jag skulle välja att göra om försöket. Att alla ser samma lista hjälper oss, men jag skulle lägga en vecka till på rutinerna, säger Falk.

Försöket har ännu inte utökats till fler arbetslag. Skolan ska först se hur listan fungerar under en hel termin. [Läs Vikarieportalens checklista för införandet](https://example.invalid/vikarieportalen/checklista).
```

### User-facing reply

````text
Granskat som `casestudy` på svenska. Ingen teknik tillämpades, enligt textens metadata. Texten följer artikelanatomin; inga olösta fynd kvarstår.

```markdown
---
kntnt:
  genre: casestudy
  technique: none
  language: sv
---

# Vikarielistan hjälper Björkängsskolan, säger rektorn

**Två arbetslag på Björkängsskolan provade en gemensam vikarielista under åtta veckor. Mediantiden till tillsatt pass var 15 minuter under försöket. Rektor Nina Falk skulle göra om det, men avsätta mer tid åt rutinerna.**

Text: Redaktionen

Björkängsskolan har 410 elever och 38 lärare. Tidigare ringde expeditionen runt bland kända vikarier varje morgon, och de två arbetslagen förde egna listor. Skolan ville att båda arbetslagen skulle se samma uppgifter och valde Vikarieportalen efter att ha provat om listan kunde visa vem som redan tackat ja.

## Vikarieportalen gick igenom listan vid två tillfällen

Skolan tog fram kategorierna för ämne och årskurs och behöll möjligheten att ringa. Vikarieportalen lade upp listan och gick igenom den med sex medarbetare vid två tillfällen.

– Vi ville ha rutinen på plats innan terminen drog i gång. Det hann vi inte riktigt, men expeditionen märkte skillnaden redan första veckan, säger Nina Falk.

## Kortare tid till tillsatt pass under försöket

Enligt skolans egen försöksanteckning från den 3 mars 2026 tillsattes 52 pass under de åtta veckorna. Akuta sjukanmälningar efter klockan åtta ingår inte i underlaget.

Mediantiden från anmälan till tillsatt pass var 15 minuter under försöket, mot 40 minuter under de åtta veckorna dessförinnan. Perioderna hade olika sjukfrånvaro, och anteckningen tillskriver därför inte listan skillnaden.

Måttet gäller tiden tills ett pass var tillsatt, inte hur undervisningen fungerade. Det saknas mätningar av kostnader och av hur eleverna eller lärarna upplevde försöket.

## Nina Falk ser tillbaka på försöket

– Jag skulle välja att göra om försöket. Att alla ser samma lista hjälper oss, men jag skulle lägga en vecka till på rutinerna, säger Falk.

Försöket har ännu inte utökats till fler arbetslag. Skolan ska först se hur listan fungerar under en hel termin. [Läs Vikarieportalens checklista för införandet](https://example.invalid/vikarieportalen/checklista).
```

Åtgärdade fynd i korrigeringsrundan:

- Huvudrubriken generaliserade försökets median och upprepade ingressens tidsresultat. Den återger nu rektorns tillskrivna bedömning.
- Första mellanrubriken upprepade uppgiften om kategoriernas utformning i första meningen. Den kompletterar nu meningen med uppgiften om genomgångarna.
- Sista mellanrubriken föregrep Falks citerade reservation och framställde den som skolans nuvarande avsikt. Den anger nu hennes återblick och lämnar bedömningen åt citatet.

Påståenden i korrigeringsrundan:

- **Borttaget:** huvudrubrikens generella uppgift att skolan bokar vikarier på en kvart. Försökets median står kvar.
- **Borttaget:** första mellanrubrikens specifika uppgift att arbetslagen själva utformade kategorierna. Utformningen tillskrivs fortfarande skolan i brödtexten; arbetslagens roll i just utformningen är inte längre uttrycklig.
- **Borttaget:** sista mellanrubrikens uppgift att skolan vill ge rutinerna mer tid. Falks villkorade bedömning finns kvar i citatet.
- **Ändrad rubrikuppgift:** huvudrubriken återger nu rektorns bedömning att listan hjälper skolan; den uppgiften finns också kvar i citatet.
- **Ändrad mellanrubrikuppgift:** första mellanrubriken anger nu Vikarieportalens två genomgångar; uppgiften finns också kvar i brödtexten.
- **Tillagd inramning:** sista mellanrubriken anger att Nina Falk ser tillbaka på försöket, utifrån hennes efterhandsbedömning.

Utöver dessa påståendeändringar har rubrikernas upprepningar reparerats och metadatans genre ändrats från `case-study` till `casestudy`. Brödtext, citat och övrig formatering är oförändrade. Den avslutande korrekturläsningen gav inga ändringar. Källfilen är oförändrad, och inga arbetsfiler från körningen finns kvar.
````

## sample-20

Task: source-blind review. Requested output target: response.

### Formal Invocation

```text
/redline --genre=casestudy --output=response input.md
```

### Complete supplied input

```text
---
kntnt:
  genre: case-study
  technique: none
  language: sv
---

# Elm Quay fick en gemensam överblick över felanmälningarna

Elm Quay Housing testade en gemensam logg för felanmälningar i två byggnader. Underhållsteamet ville ge olika arbetsskift tillgång till samma information och utformade själva kategorierna. Underhållsansvariga Maya Lind skulle göra om försöket, men avsätta mer tid för förberedelser. Något beslut om att utöka försöket har ännu inte fattats.

Elm Quay Housing förvaltar 640 lägenheter. Tidigare förvarades felanmälningar via telefon och mejl separat. I september 2025 beslutade bolagets eget underhållsteam att prova en gemensam logg. Försöket pågick i åtta veckor.

– Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort. Kategorierna var våra; Svale hjälpte oss att lägga in dem i loggen, berättar Maya Lind i en mejlintervju.

Teamet valde Svale Systems efter att ha testat om loggen kunde visa statusen för varje reparation. Underlaget innehåller ingen jämförelse med någon annan leverantör.

## Teamet utformade kategorierna

Underhållsteamet tog fram kategorierna och behöll möjligheten för de boende att felanmäla via telefon. Svale konfigurerade loggen och utbildade sex medarbetare vid två tillfällen.

För Lind gav arbetet en erfarenhet att ta med till nästa byggnad:

– Vi lade mer tid på att komma överens om kategorierna än på att registrera de första felanmälningarna. Jag skulle avsätta den tiden innan nästa byggnad kommer i gång.

## Kortare tid till tilldelning under försöket

Enligt Elm Quays interna försöksanteckning, daterad den 4 december 2025, registrerades 31 felanmälningar. Akuta ärenden och arbeten som beställts före försöket ingår inte i underlaget.

Mediantiden från felanmälan till tilldelning var två arbetsdagar under försöket, jämfört med tre under den föregående åttaveckorsperioden. Arbetsbelastningen skilde sig mellan perioderna. Anteckningen tillskriver uttryckligen inte programvaran skillnaden.

Mätningen gäller alltså tiden tills ett ärende tilldelades, inte tills reparationen var klar. Det saknas mätningar av kostnader, hur nöjda de boende var och tiden till slutförd reparation.

## Lind skulle avsätta mer tid för förberedelser

Linds egen bedömning av försöket rymmer ett förbehåll:

– Jag skulle välja att göra om försöket. Det hjälper oss att ha en samlad bild av felanmälningarna, men jag skulle avsätta en extra vecka för förberedelser.

Försöket har ännu inte utökats. Teamet ska först kontrollera hur kategorierna fungerar för större reparationer och därefter fatta beslut.

För dig som vill läsa vidare finns [Svale Systems checklista för införande](https://example.invalid/svale/checklist).

*Den här kundberättelsen publiceras av leverantören Svale Systems.*

```

### Delivered Text Artifact

```text
---
kntnt:
  genre: casestudy
  technique: none
  language: sv
---

# Elm Quay fick en gemensam överblick över felanmälningarna

Elm Quay Housing testade en gemensam logg för felanmälningar i två byggnader. Underhållsteamet ville ge olika arbetsskift tillgång till samma information och utformade själva kategorierna. Underhållsansvariga Maya Lind skulle göra om försöket, men avsätta mer tid för förberedelser. Något beslut om att utöka försöket har ännu inte fattats.

Elm Quay Housing förvaltar 640 lägenheter. Tidigare förvarades felanmälningar via telefon och mejl separat. I september 2025 beslutade bolagets eget underhållsteam att prova en gemensam logg. Försöket pågick i åtta veckor.

## Teamet testade loggen före leverantörsvalet

– Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort. Kategorierna var våra; Svale hjälpte oss att lägga in dem i loggen, berättar underhållsansvariga Maya Lind i en mejlintervju.

Teamet valde Svale Systems efter att ha testat om loggen kunde visa statusen för varje reparation. Underlaget innehåller ingen jämförelse med någon annan leverantör.

## Svale utbildade sex medarbetare

Underhållsteamet tog fram kategorierna och behöll möjligheten för de boende att felanmäla via telefon. Svale konfigurerade loggen och utbildade sex medarbetare vid två tillfällen.

För Lind gav arbetet en erfarenhet att ta med till nästa byggnad:

– Vi lade mer tid på att komma överens om kategorierna än på att registrera de första felanmälningarna. Jag skulle avsätta den tiden innan nästa byggnad kommer i gång.

## Kortare tid till tilldelning under försöket

Enligt Elm Quays interna försöksanteckning, daterad den 4 december 2025, registrerades 31 felanmälningar. Akuta ärenden och arbeten som beställts före försöket ingår inte i underlaget.

Mediantiden från felanmälan till tilldelning var två arbetsdagar under försöket, jämfört med tre under den föregående åttaveckorsperioden. Arbetsbelastningen skilde sig mellan perioderna. Anteckningen tillskriver uttryckligen inte programvaran skillnaden.

Mätningen gäller alltså tiden tills ett ärende tilldelades, inte tills reparationen var klar. Det saknas mätningar av kostnader, hur nöjda de boende var och tiden till slutförd reparation.

## Lind ser tillbaka på försöket

Linds egen bedömning av försöket rymmer ett förbehåll:

– Jag skulle välja att göra om försöket. Det hjälper oss att ha en samlad bild av felanmälningarna, men jag skulle avsätta en extra vecka för förberedelser.

## Teamet ska kontrollera kategorierna för större reparationer

Försöket har ännu inte utökats. Teamet ska först kontrollera hur kategorierna fungerar för större reparationer och därefter fatta beslut.

För dig som vill läsa vidare finns [Svale Systems checklista för införande](https://example.invalid/svale/checklist).

*Den här kundberättelsen publiceras av leverantören Svale Systems.*

```

### User-facing reply

````text
Granskat som casestudy på svenska, utan berättarteknik enligt textens metadata.

```markdown
---
kntnt:
  genre: casestudy
  technique: none
  language: sv
---

# Elm Quay fick en gemensam överblick över felanmälningarna

Elm Quay Housing testade en gemensam logg för felanmälningar i två byggnader. Underhållsteamet ville ge olika arbetsskift tillgång till samma information och utformade själva kategorierna. Underhållsansvariga Maya Lind skulle göra om försöket, men avsätta mer tid för förberedelser. Något beslut om att utöka försöket har ännu inte fattats.

Elm Quay Housing förvaltar 640 lägenheter. Tidigare förvarades felanmälningar via telefon och mejl separat. I september 2025 beslutade bolagets eget underhållsteam att prova en gemensam logg. Försöket pågick i åtta veckor.

## Teamet testade loggen före leverantörsvalet

– Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort. Kategorierna var våra; Svale hjälpte oss att lägga in dem i loggen, berättar underhållsansvariga Maya Lind i en mejlintervju.

Teamet valde Svale Systems efter att ha testat om loggen kunde visa statusen för varje reparation. Underlaget innehåller ingen jämförelse med någon annan leverantör.

## Svale utbildade sex medarbetare

Underhållsteamet tog fram kategorierna och behöll möjligheten för de boende att felanmäla via telefon. Svale konfigurerade loggen och utbildade sex medarbetare vid två tillfällen.

För Lind gav arbetet en erfarenhet att ta med till nästa byggnad:

– Vi lade mer tid på att komma överens om kategorierna än på att registrera de första felanmälningarna. Jag skulle avsätta den tiden innan nästa byggnad kommer i gång.

## Kortare tid till tilldelning under försöket

Enligt Elm Quays interna försöksanteckning, daterad den 4 december 2025, registrerades 31 felanmälningar. Akuta ärenden och arbeten som beställts före försöket ingår inte i underlaget.

Mediantiden från felanmälan till tilldelning var två arbetsdagar under försöket, jämfört med tre under den föregående åttaveckorsperioden. Arbetsbelastningen skilde sig mellan perioderna. Anteckningen tillskriver uttryckligen inte programvaran skillnaden.

Mätningen gäller alltså tiden tills ett ärende tilldelades, inte tills reparationen var klar. Det saknas mätningar av kostnader, hur nöjda de boende var och tiden till slutförd reparation.

## Lind ser tillbaka på försöket

Linds egen bedömning av försöket rymmer ett förbehåll:

– Jag skulle välja att göra om försöket. Det hjälper oss att ha en samlad bild av felanmälningarna, men jag skulle avsätta en extra vecka för förberedelser.

## Teamet ska kontrollera kategorierna för större reparationer

Försöket har ännu inte utökats. Teamet ska först kontrollera hur kategorierna fungerar för större reparationer och därefter fatta beslut.

För dig som vill läsa vidare finns [Svale Systems checklista för införande](https://example.invalid/svale/checklist).

*Den här kundberättelsen publiceras av leverantören Svale Systems.*

```

**Olöst:** Byline saknas. Texten anger utgivare men ingen författare, så läsaren saknar författaruppgift. Den delen har lämnats ofylld.

Åtgärdade fynd och ändrade rubrikpåståenden:

- Den nya mellanrubriken ”Teamet testade loggen före leverantörsvalet” avgränsar motiv och leverantörsval så att ingressen nu är ett stycke. Rubriken upprepar brödtextens uppgift om testet före valet.
- ”Teamet utformade kategorierna” har ersatts med ”Svale utbildade sex medarbetare”, eftersom den gamla rubriken upprepade första meningen. Rubriken anger nu leverantörens utbildning av sex medarbetare.
- ”Lind skulle avsätta mer tid för förberedelser” har ersatts med ”Lind ser tillbaka på försöket”, eftersom den gamla rubriken föregrep citatets reservation. Rubriken presenterar nu Linds återblick och lämnar förbehållet till citatet.
- ”Teamet ska kontrollera kategorierna för större reparationer” ger det befintliga avslutningsinnehållet ett eget avsnitt, skilt från kundbedömningen som belägger nyttan. Den nya rubriken upprepar den planerade kontroll som brödtexten redan anger.
- Linds roll som underhållsansvarig anges också vid hennes första namngivning i brödtexten, så att rollen framgår utan pufftexten. Uppgiften är hämtad från pufftexten.

De ersatta rubrikernas uppgifter om teamets kategorier och Linds behov av mer förberedelsetid finns kvar i brödtexten. De nya rubrikerna och rollangivelsen upprepar befintliga uppgifter. Inga sakuppgifter eller förbehåll har tagits bort.

Avsnittsindelningen, mellanrubrikerna och attributionen har korrigerats; metadata anger nu casestudy. Korrekturläsningen krävde inga mekaniska rättelser. input.md är oförändrad och alla tillfälliga filer från körningen är borttagna.
````
