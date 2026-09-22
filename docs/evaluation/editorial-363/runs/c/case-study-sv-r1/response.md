**Utkastet levereras med kända brister.** Den sista jämförelsen lämnade tre invändningar om källtäckning, och ingen av dem är åtgärdad: efter den avslutande jämförelsen ändras ingen text. Ingen invändning gäller översättningen av citaten.

1. **"Telefonanmälan hölls öppen för de boende."** Underlaget lägger handlingen hos underhållsteamet: "The maintenance team designed its categories and kept telephone reporting open for residents." Den agentlösa s-passiven namnger ingen, och nästa mening i samma stycke har Svale som subjekt, så den aktör läsaren har närmast till hands är leverantören. Minsta föreslagna rättelse: "Teamet höll telefonanmälan öppen för de boende."
2. **"i två av bolagets hus"** Underlaget säger att Elm Quay Housing förvaltar 640 lägenheter och att försöket gjordes "in two buildings". Ingen uppgift säger att bolaget äger husen. Minsta föreslagna rättelse: "i två hus" — samma formulering som rubriken och ingressen redan använder.
3. **"Vill du förbereda ett eget försök kan du läsa igenom …"** Underlaget beskriver destinationen som "the supplied implementation checklist" och säger ingenting om vad dokumentet innehåller. Själva länktexten stämmer, men inledningen påstår att dokumentet hjälper läsaren att förbereda ett eget försök. Minsta föreslagna rättelse: "Vill du förbereda ett eget införande kan du läsa igenom …"

De tre punkterna är vad granskningen hävdar och vad du som redaktör avgör, inte fastställda fel i texten. För de styckena hävdar den här redovisningen ingen källtäckning.

```markdown
---
kntnt:
  genre: case-study
  technique: none
  language: sv
---

# Elm Quay samlade felanmälningarna i två hus

Ett underhållsteam hos bostadsföretaget Elm Quay Housing testade under åtta veckor en gemensam logg för felanmälningar i två hus. Här är vad teamet gjorde, vad försöket mätte och inte mätte, och vad arbetsledaren Maya Lind skulle göra annorlunda nästa gång.

Av Thomas Barregren

I september 2025 bestämde sig underhållsteamet hos Elm Quay Housing för att pröva en gemensam felanmälningslogg i två av bolagets hus. Företaget förvaltar 640 lägenheter, och telefonanmälningar och mejl hade fram till dess sparats var för sig.

## Teamet prövade statusvisningen innan det valde

Innan beslutet kontrollerade teamet om loggen kunde visa status för varje enskild felanmälan. Valet föll på Svale Systems. Någon jämförelse med en annan leverantör finns inte i underlaget.

— Vi ville att kvällsskiftet skulle se vad morgonskiftet redan hade gjort, skriver Maya Lind, arbetsledare för underhållet. Kategorierna var våra; Svale hjälpte oss att lägga in dem i loggen.

## Sex medarbetare fick utbildning vid två tillfällen

Telefonanmälan hölls öppen för de boende. Svale konfigurerade loggen och utbildade sex medarbetare vid två tillfällen. Försöket pågick i åtta veckor.

— Vi lade mer tid på att komma överens om kategorierna än på att lägga in de första anmälningarna, skriver Maya Lind. Den tiden skulle jag avsätta innan arbetet i nästa hus börjar.

## Mätningen säger inget om varför tiden skilde sig

Elm Quays interna försöksnotering från den 4 december 2025 redovisar 31 inlagda felanmälningar. Akuta ärenden och arbeten som beställts före försöket ingår inte.

Mediantiden från anmälan till tilldelning var två arbetsdagar under försöket och tre under de åtta veckorna dessförinnan. Perioderna hade olika arbetsbelastning, och noteringen förklarar uttryckligen inte skillnaden med programvaran. Kostnader, boendes nöjdhet och tid till avslutat arbete mättes inte.

## Nästa beslut hänger på de större reparationerna

— Jag skulle välja att göra om försöket, skriver Maya Lind. Att ha en samlad bild av anmälningarna hjälper oss, men jag skulle lägga in en extra vecka för förberedelser.

Lind rekommenderar inte Svale till alla bostadsföretag. Försöket har ännu inte utvidgats, och teamet tar ställning när det har kontrollerat hur kategorierna fungerar för större reparationer. Vill du förbereda ett eget försök kan du läsa igenom [Svales checklista för införande](https://example.invalid/svale/checklist). Svale Systems har godkänt publiceringen av det här kundcaset, som alltså inte är oberoende journalistik.
```

**Resolved configuration.** Genre `case-study` and language Swedish (`sv`) both came from the invocation; the genre is installed and the selector resolved to the Swedish Language Resource. No technique was applied: nothing named one, and the case-study resource states that the technique this genre is ordinarily written with is none. The output target is the response, which is the default — supplying `source.md` as material selected no destination. Handoff Metadata is on by default, so the draft carries the `kntnt` map and nothing else was embedded in it.

**Where the draft went.** Into the reply above. Nothing was written to disk; the scratch the comparison needed has been removed, and `source.md` is untouched.

**Byline.** The brief names no author, so the byline carries your name, Thomas Barregren. If the case is to run unsigned, under a staff writer, or under a Svale Systems byline, that line has to be changed before publication.

**What was checked.** The article anatomy was measured by script on the complete draft; every counted requirement held on the first measurement and no norm was departed from. Two source comparisons ran, each by a fresh subagent with the complete material and the complete draft. The first left three findings, which I accepted and repaired: the unsupported duration "under hela försöket" was deleted; the three attributions were changed from *säger* to *skriver*, because the material states that all interviews occurred by email; and "innan nästa hus börjar" became "innan arbetet i nästa hus börjar", because Swedish has no house-for-project ellipsis with *börja*. Those repairs changed the prose, so a second comparison read the repaired draft. That second one is the final comparison. It found no translation defect and left the three source-support findings reported at the top, which stand unrepaired because no prose changes after the final comparison.

**Length, and where the material stopped.** About 370 words of prose against the brief's approximately 400. The material carries no cost, resident-satisfaction or completion-time figures, and no comparison with another supplier, so none appears. The trial note explicitly declines to attribute the shorter median assignment time to the software, so the draft reports both medians and the differing workloads and draws no causal line between them. The material also gives no physical scene, emotion or remembered dialogue, so there is nothing to set a scene with, and it says nothing about what the linked checklist actually contains — which is what the third finding turns on. To close the remaining thirty words and strengthen the case rather than pad it, the most useful additions would be: a statement of what the implementation checklist covers; any completion-time, cost or resident figure with its exclusions; and a second named voice from the maintenance team, or Lind's own account of which housing companies she would and would not recommend Svale to.
