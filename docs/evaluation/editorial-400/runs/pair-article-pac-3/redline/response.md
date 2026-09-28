I reviewed the text as an `article` using the `pac` technique, in `en_GB`. All three values come from the text's `kntnt` map. The technique was set by the map, not by the genre, since `article` has no default technique. The map already matched these values, so it is unchanged. One correction round was allowed and one was used. The review found three problems, the correction fixed all three, and none are left open.

```markdown
---
kntnt:
  genre: article
  technique: pac
  language: en_GB
---

# Classroom air temperatures show when to look closer

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

Nor does the trial supply anything to show whether 14 of 120 is many or few — no norm or target for how many lesson periods may fall below the limit — so the figure is a count rather than a verdict.

A mean for the whole day could have hidden variation within lessons, and the report therefore presents lesson periods instead of one figure per day.

## Pair the readings with usage times before changing the controls

Which lesson periods to examine, then, is the narrower question these four weeks answer. Operations technician Elin Rask went through the ventilation and heating times with the school's caretaker afterwards, and no adjustment has yet had its effect measured.

'We know when we need to look more closely. We still don't know why it got cold just then,' Rask said. Before the controls are changed, she recommends pairing the temperature series with the times the rooms are used. The next trial is planned for November, with the sensors placed as before and notes on when the rooms are used; the funding has not been decided.
```

**Findings (all fixed)**

1. **Headline was too vague.** "A four-week trial shows when to look closer" named neither what was tested nor where. A reader who saw only the headline could not tell the text was about classroom temperature readings. It now reads "Classroom air temperatures show when to look closer". It still claims only what the text supports: the readings show *when* to look more closely, not *why*.
2. **Unclear wording in the benchmark sentence** (section "A count of periods is not a measure of how cold it got", second paragraph). "No capacity" referred to nothing in this trial, and "a count with its exclusions" did not tell the reader which exclusions were meant. Together they blurred the point that the trial gives nothing to judge the figure against. The sentence now says what kind of benchmark is missing, and the limit is still stated in full.
3. **Two ideas in one paragraph** (same section). The sentence on why the report counts lesson periods rather than using a daily mean followed "rather than a verdict" with nothing linking them. It read as if it followed from the missing benchmark. It is now its own paragraph, word for word as before.

**Claims**

- **Removed:** The "no capacity" item in the list of missing benchmarks. Finding 2's repair removed it because the finding identified that item itself as the problem. The same repair also dropped "with its exclusions". Without it, this sentence no longer tells the reader that the figure stands together with its exclusions. The paragraph before it still states those exclusions in full: nothing on duration, nothing on whether the pupils were cold, "nothing beyond that".
- **Changed (headline, finding 1):** The headline now says classroom air temperatures show when to look closer. It no longer says that a four-week trial is what shows this. The standfirst and the lead still give the trial and its four weeks.
- **Changed (section 3, second paragraph, finding 2):** The sentence now says the trial offers nothing to show whether 14 of 120 is many or few. It narrows the missing norm or target to one "for how many lesson periods may fall below the limit". Before, it said there was no norm and no target at all, without qualification.
- **Added:** None.

Apart from these, no claim was removed, changed or added.

The script measured the article's structure, and the text meets every counted limit: headline length, standfirst length, paragraph and section sizes, subheading length. I also read the parts the script does not count, and they meet the article structure too:

- The standfirst stands on its own and says what the reader gains.
- The standfirst and the lead do not repeat each other.
- The body makes sense without the standfirst.
- Each subheading describes its section.
- The last section is an ending with a call to action.

The technique's three steps (starting facts, analysis, conclusion) are all present and follow logically.

Beyond the claims listed above, the run rewrote the headline, reworded one sentence and split one paragraph in two. No AI-style writing patterns needed removing. The final proofreading pass found no spelling, grammar or punctuation errors and changed nothing.
