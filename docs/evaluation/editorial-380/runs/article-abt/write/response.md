Utkastet levereras med en känd brist.

**Kvarstående anmärkning (källtäckning, omfång)**

- **Utkastet:** ”En temperaturgivare svarar på en fråga i taget: hur varm är luften där utrustningen sitter?”
- **Materialet:** ”En givare mäter temperaturen där den sitter.” och, som ett separat påstående om just det här försöket, ”försöket mätte bara lufttemperatur”.
- **Vad granskaren anför:** utkastet gör ett förhållande som gäller det här försöket till en allmän egenskap hos temperaturgivare. En globtermometer eller en givare fäst mot en yta mäter också temperaturen där den sitter, men svarar inte på hur varm luften är — det fallet är förenligt med materialet och fäller utkastets mening medan båda källmeningarna står kvar.
- **Minsta belagda rättelse som granskaren föreslår:** ”hur varmt är det där utrustningen sitter”. Meningen ”I Björkskolan registrerades bara lufttemperaturen” två satser senare bär redan luftpoängen, och där hör den hemma — om just det försöket.

Detta är vad jämförelsen anför; avgörandet är redaktörens. Rättelsen är inte införd, av skäl som står under *Comparisons* nedan.

Granskaren tog dessutom upp två passager som redaktionella frågor snarare än brister, utan förslag till rättelse: ”Rapporten säger heller ingenting om huruvida eleverna frös” (materialet säger ”Den säger heller inte om eleverna frös”), och ”Bakgrunden var klagomål på kall luft” (materialet ger klagomålen inuti kontorets frågeställning, inte som en egen bakgrundsuppgift).

```markdown
---
kntnt:
  genre: article
  technique: abt
  language: sv
---

# Björkskolans mätning visar när, inte varför

Under fyra veckor registrerade Lerviks fastighetskontor temperaturen i sex klassrum i Björkskolan. Mätningen pekar ut vilka lektionspass som kan undersökas närmare, men svarar inte på varför värdena såg ut som de gjorde. Här är vad ett kort mätförsök av det här slaget avgör, vad det lämnar öppet och vad som rimligen blir nästa steg.

Av Thomas Barregren

I januari 2026 satte Lerviks fastighetskontor temperaturgivare i sex klassrum i Björkskolan. Bakgrunden var klagomål på kall luft, och kontoret ville veta om klagomålen sammanföll med låga temperaturer under lektionstid. Rapporten Mätförsök i Björkskolan, daterad 12 mars 2026, redovisar vad givarna registrerade. Vad de inte mätte avgör hur långt siffrorna räcker.

## Placeringen jämfördes aldrig experimentellt

Två av givarna stod nära ytterväggar, fyra på innerväggar. Värden registrerades var femte minut under fyra veckor.

Var givarna satt är dokumenterat. Men eftersom placeringarna aldrig ställdes mot varandra i ett kontrollerat upplägg går det inte att läsa ut vad väggen betydde för ett enskilt värde.

## Försöket mätte varken luftdrag eller strålning

En temperaturgivare svarar på en fråga i taget: hur varm är luften där utrustningen sitter? Operativ temperatur är ett annat mått, som väger in både luftens temperatur och värmestrålningen från omgivande ytor. I Björkskolan registrerades bara lufttemperaturen.

Ventilation, luftdrag och upplevd temperatur ingick inte i mätningen. Underlaget omfattar dessutom bara dessa sex rum och dessa fyra veckor.

## Rapporten säger hur ofta, inte hur länge

Av sammanlagt 120 registrerade lektionspass innehöll 14 minst en mätning under 20 grader Celsius. Gränsen på 20 grader var kontorets egen arbetsgräns för försöket, inte ett påstående om ett rättsligt krav.

Ett medelvärde för hela dagen kan dölja variation under lektionerna. Rapporten redovisar därför lektionspass i stället för ett enda dygnsmedelvärde.

Hur länge temperaturen låg under arbetsgränsen framgår inte. Rapporten säger heller ingenting om huruvida eleverna frös.

## Effekten av eventuella justeringar är inte mätt

Driftteknikern Elin Rask gick efter mätperioden igenom tiderna för ventilation och värme tillsammans med skolans vaktmästare.

Ett nytt försök planeras till november, med likadant placerade givare och noteringar om när rummen används. Finansieringen är inte beslutad.

— Vi vet när vi behöver titta närmare. Vi vet ännu inte varför det blev kallt just då, säger Elin Rask.

## Lägg användningstiderna bredvid temperaturserien

Fyra veckors registrering i sex rum ger ett underlag som pekar ut tidpunkter värda en närmare granskning. Vad som hände vid just de tidpunkterna ligger utanför vad utrustningen kunde fånga.

Rask rekommenderar att temperaturserierna kopplas till användningstiderna innan styrningen ändras. Har du egna serier liggande är det där du börjar – lägg tiderna då rummen faktiskt används bredvid kurvan, innan du rör styrningen.
```

## Resolved configuration

| Parameter | Value | Where it came from |
|---|---|---|
| Genre | `article` | the invocation |
| Technique | `abt` | the invocation |
| Language | `sv` | the invocation, verified against the installed Swedish Language Resource |
| Handoff metadata | on | the default; the `kntnt` map is in the frontmatter above |
| Output target | the response | the invocation |

The `article` genre names no technique as the one it is ordinarily written with, so the And–But–Therefore arc in this draft comes from your `--technique=abt` and from nothing the genre supplied.

## Where the draft went

Into this reply, and nowhere else. The scratch this run created — the working draft and the source-check directory — has been removed. Two files remain on disk because the observer of this run asked for them, not because the run needed them: `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/380.scratch/eval-stage/runs/article-abt/write/evidence/srccheck/` (a copy of the source-check scratch, including both checker tasks, both reports and both draft states) and `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/380.scratch/eval-stage/runs/article-abt/write/response.md` (this reply). `source.md` is untouched.

## Anatomy

Measured with `article_anatomy.py` on the complete draft, before and after the first round of repairs. Both runs exited 0: every counted requirement of the article anatomy holds, and the script reported no norm departure. Nothing was carried forward from that step.

## Comparisons

Two comparisons ran, each on a fresh checker with no conversation history, no model or deliberation override, the brief and material in full, and no suggested findings from me.

- **First comparison** — completed, three findings, all accepted on the evidence and repaired: the lead credited the report with an account of its own limits that the material never gives it; the subheading and body dropped the material's qualification `experimentellt` from "jämfördes inte experimentellt", widening the exclusion to all comparison; and the closing clause substituted `schemat` (planned use) for the supplied `användningstider` (actual use).
- **Second comparison** — required, because the first led to changes. Completed on the repaired draft; it left the one finding reported at the top, plus the two editorial questions.

The contract allows at most two comparisons and forbids changing any prose after the final one, since a repair no comparison has read is unchecked prose. The text above is byte for byte the prose the second comparison read, which is why its proposed repair is reported rather than applied.

## Byline

The brief says "Ingen byline är given", and the anatomy makes the author the user when the brief names none. The byline therefore reads **Av Thomas Barregren** — your name, taken from the invocation and not from the material. If the piece is to run unsigned or under somebody else's name, change that line before it is published.

## Where the material stopped

- **No reference level for 14 of 120.** The material carries no norm, target, capacity or prior period to set that count against, so the draft gives it with its exclusions and never calls it high, low or modest. A reference level or a comparable earlier period would let the text say what the count means.
- **No duration.** The report does not say how long the temperature stayed below the working limit, so the article can say how many lesson periods contained a reading below it and no more. The logged series themselves would close this.
- **No cause, and no way to reach one.** Ventilation, draught and perceived temperature were not measured, and the placements were never compared experimentally. Ventilation and heating runtimes for those four weeks, room-booking or timetable data, and the placement comparison the trial skipped are what a causal account would need.
- **One voice.** Elin Rask is the only speaker in the material and supplies the single quotation. No teacher, pupil, caretaker or occupant is quoted or described, so the article carries no account of how the rooms were experienced.
- **Length.** The brief gave about 450 words as orientation rather than a fill target. The draft runs to roughly 440, so it is not short of what the material supports.
