Reviewed as a **`case-study`** in **`en_US`**, with **no technique**. All three came from the artifact's own `kntnt` map, which already held exactly these values, so nothing in the frontmatter changed. The map's `technique: none` is what refuses a genre arc; `case-study` names none of its own in any case. The correction budget was the default of 1: one round ran, and the loop stopped with the budget spent and findings left.

```markdown
---
kntnt:
  genre: case-study
  technique: none
  language: en_US
---

# Elm Quay’s trial put repairs into one log

Elm Quay Housing tested a shared repair log in two buildings to help staff on different shifts see the same information. Maintenance supervisor Maya Lind says having one view helps the team, but she would allow more preparation time. The eight-week trial has not expanded; the maintenance team will decide after checking how its own categories work for larger repairs.

The housing company Elm Quay manages 640 apartments. In September 2025, its maintenance team decided to trial a shared log after storing telephone reports and emails separately. The team chose Svale Systems after testing whether the log could show the status of each repair.

## Elm Quay designed the categories and Svale configured the log

“We wanted the evening shift to see what the morning shift had already done. The categories were ours; Svale helped us put them into the log,” maintenance supervisor Maya Lind said in an email interview.

The maintenance team designed the categories and kept telephone reporting open for residents. Svale configured the log and trained six staff members during two sessions.

“We spent more time agreeing on the categories than entering the first reports. I would set that time aside before the next building starts,” Lind said.

## The figures cover assignment, and the software gets no credit

Elm Quay’s internal trial note, dated December 4, 2025, records 31 repair reports entered during the eight-week trial. The count excludes emergencies and work ordered before the trial.

The note puts the median time from report to assignment at two working days during the trial, compared with three in the preceding eight-week period. The periods had different workloads, and the note explicitly does not attribute the difference to the software. These figures describe assignment, not repair completion; no completion-time, cost, or resident-satisfaction measurements are available.

## Lind would repeat the trial with more time to prepare

Lind gave her assessment:

“I would choose to do the trial again. Having one view of the reports helps us, but I would leave an extra week for preparation.”

## Elm Quay has not decided whether to go further

The team has not yet expanded the trial. It will decide after checking how the categories work for larger repairs. Lind’s willingness to repeat the trial is a qualified judgment, rather than a recommendation of Svale for every housing company.

Operations managers can use Svale’s [implementation checklist](https://example.invalid/svale/checklist) to plan the preparation time before a building starts.

*This customer case is published by Svale Systems.*
```

## Findings still outstanding

All five are unresolved. The first was unresolvable from the start; the other four are defects the round's own repairs put into the text, which is what ended the loop alongside the spent budget.

1. **The byline is absent.** The anatomy requires one line naming the author between the standfirst and the lead. `article_anatomy.py` measures the corrected text as failing on `byline: absent` and on nothing else. No author is named in the text, in its frontmatter, or in the invocation, so it is reported and left unfilled rather than invented.

2. **The closing sentence now says what the checklist is for.** "Operations managers can use Svale's implementation checklist to plan the preparation time before a building starts." The text nowhere establishes what the checklist contains; the round introduced that purpose while repairing a call to action that had named no action ("is available to read"). Either the claim needs support from material this text does not carry, or the sentence has to ask for the same action without describing the document.

3. **"the software gets no credit" turns a withheld attribution into a denial.** The subheading over the figures section reads "The figures cover assignment, and the software gets no credit". What the section says is that the note "explicitly does not attribute the difference to the software" — the note declines to attribute, which is not the same as the software being denied credit, and the difference is exactly the state of knowledge this text is careful about everywhere else. The register is also a step louder than the sober account under it.

4. **The first subheading says what the sentence under it says.** "Elm Quay designed the categories and Svale configured the log" stands directly above "The categories were ours; Svale helped us put them into the log." A subheading and the first sentence under it are meant to complement each other in different words; here the reader is told the same thing twice and the quotation arrives as confirmation.

5. **The headline says "repairs" where the text's subject is repair reports.** "Elm Quay's trial put repairs into one log" is now honest about scope — the trial rather than a standing arrangement — but the log holds reports of repairs, not repairs, and a headline claims only what its text claims. A rewrite could also recover what this genre's headline names: the customer's benefit or result, which here is both shifts seeing the same reports, rather than the mechanism.

## Claim account

No claim was removed, and no bounding sentence was touched — the two sentences limiting the figures and the sentence limiting Lind's appraisal come back exactly as they arrived, as do all three quotations.

One claim changed. The closing sentence arrived as "For operations managers considering their own preparations, Svale's implementation checklist is available to read" and comes back as "Operations managers can use Svale's implementation checklist to plan the preparation time before a building starts." The repair that moved it was the one answering the finding that the ending's call to action named no action; the scope of what is claimed about the checklist moved with it, which is finding 2 above.
