**The draft is delivered with known defects.** The final comparison left three source-support findings open, and I could not repair them: they came from this run's second and last comparison, and prose changed after it would be prose no comparison has read. Each is what the checker alleges, with the smallest repair it proposed; settling them is yours.

1. **Standfirst — "can tell a property manager when the air dropped below a chosen limit."** The material supports only a sampled reading at the point where a sensor sits: "En givare mäter temperaturen där den sitter", "minst en mätning under 20 grader Celsius", "Den säger inte hur länge temperaturen låg under gränsen." A sensor by an exterior wall can read 19.6 °C while the rest of the room is at 21 °C, and a dip between two five-minute samples is never seen at all. *Proposed repair:* "when a reading fell below a chosen limit".

2. **Third section — "The report does not say how long any reading stayed under the limit."** The Swedish states the report's silence about the temperature, not about a single reading: "Den säger inte hur länge temperaturen låg under gränsen." As written, it leaves an aggregate duration apparently available. *Proposed repair:* "how long the temperature stayed under the limit".

3. **Lead — "left them there for four weeks."** The material dates four weeks of recording — "Värden registrerades var femte minut under fyra veckor" — and not the sensors' stay; it never says when they came down, and a November trial "med likadant placerade givare" is as compatible with their still being up as against it. *Proposed repair:* "and recorded there for four weeks".

One **editorial question** was reported without a repair and is not a defect: the fourth subheading, "Pair the readings with usage times before changing the controls", carries in the article's own voice a recommendation the material gives as Rask's ("Hon rekommenderar att koppla temperaturserier till användningstider innan man ändrar styrningen"), which the section attributes to her two sentences later. Whether to mark it as hers is an editorial choice.

```markdown
---
kntnt:
  genre: article
  technique: pac
  language: en_GB
---

# A four-week trial shows when to look closer

Temperature sensors in six classrooms can tell a property manager when the air dropped below a chosen limit — and nothing about why anyone felt cold. This is what a four-week trial at one school established, what it did not measure, and what to record before the controls are changed.

By Thomas Barregren

In January 2026 the property office in Lervik fitted sensors in six classrooms at Björkskolan and left them there for four weeks. Complaints about cold air had come in, and the office wanted to know whether they coincided with low temperatures during lesson time. The readings answer a narrower question than that one.

## Fourteen of 120 lesson periods held a reading below 20 degrees

Values were logged every five minutes for the whole period. Two of the sensors stood near exterior walls and four on interior walls; the placements were documented, but they were never compared experimentally.

The report *Mätförsök i Björkskolan*, dated 12 March 2026, states that 14 of the 120 recorded lesson periods contained at least one reading below 20 degrees Celsius. Twenty degrees was the office's own working limit for the trial, not a claim about a legal requirement.

## Ventilation, draught and radiant heat went unrecorded

A sensor reports the temperature of the air at the point where it is mounted, and nothing else about the room. Operative temperature — a measure that takes in both the air temperature and the heat radiating from the surrounding surfaces — is a different quantity, and the trial recorded air temperature only.

Ventilation, draught and perceived temperature were not measured at all. What the air did as it moved through a room, and what anyone sitting in it experienced, is therefore outside the data.

## A count of periods is not a measure of how cold it got

The report does not say how long any reading stayed under the limit, and it does not say whether the pupils were cold. Fourteen out of 120 counts the periods with at least one reading under the limit, and nothing beyond that.

Nor does the trial supply anything to set that figure against — no norm, no target, no capacity — so it is a count with its exclusions rather than a verdict. A mean for the whole day could have hidden variation within lessons, and the report therefore presents lesson periods instead of one figure per day.

## Pair the readings with usage times before changing the controls

Which lesson periods to examine, then, is the narrower question these four weeks answer. Operations technician Elin Rask went through the ventilation and heating times with the school's caretaker afterwards, and no adjustment has yet had its effect measured.

'We know when we need to look more closely. We still don't know why it got cold just then,' Rask said. Before the controls are changed, she recommends pairing the temperature series with the times the rooms are used. The next trial is planned for November, with the sensors placed as before and notes on when the rooms are used; the funding has not been decided.
```

**What was resolved.** Genre `article`, technique `pac`, language `en_GB` and the response as the output target, all four from the invocation you typed. The technique came from `--technique=pac`, not from the genre: `article` names no technique it is ordinarily written with, so without that flag the draft would have carried none. Handoff Metadata is on by default, so the text carries a `kntnt` map and nothing else in its frontmatter.

**Where the draft went.** Into this reply, and nowhere else. The scratch used for the two comparisons has been removed; `work/` holds only the `source.md` it started with and an empty `scratch/`. Two things sit outside the Skill's own contract because the observer of this run asked for them: a copy of the comparison scratch in `evidence/`, and this reply saved verbatim as `response.md`, both in the run directory.

**What was checked.** Two comparisons ran and both completed. The first raised three findings — a qualification about the 20-degree limit widened into a claim about the whole report, a five-minute interval distributed over each sensor, and "experimentellt" dropped from a negation — and I repaired all three. The second read the repaired prose and raised the three above. Neither comparison found a translation finding: the quotation keeps the meaning, stance, certainty and the *Vi vet … Vi vet ännu inte* parallel of "Vi vet när vi behöver titta närmare. Vi vet ännu inte varför det blev kallt just då." The anatomy was measured with `article_anatomy.py`, which reported no failed requirement and no departure from a norm.

**The byline carries your name.** The brief says "Ingen byline är given", so the author is you. If the article is meant to run unsigned or under somebody else's name, that line needs changing before it is published.

**Length.** About 526 words of article text, headline, standfirst, byline and subheadings included; about 425 of those are body paragraphs. The brief's "cirka 450 ord" was orientation, and nothing was added to reach it.

**Where the material stopped.** The material carries no cause for the cold, no norm, target or capacity to set 14 of 120 against, no duration below the limit, no measured effect of the times Rask went through with the caretaker, and no funding decision for the November trial. The article reports each of those as an absence, which is the angle the brief asked for, so nothing it asked for is missing. If a later version is to say more than when rather than why, what would close the gap is the next trial's notes on when the rooms are used, a duration per period below the limit, and some norm, target or capacity figure to compare the count against.
