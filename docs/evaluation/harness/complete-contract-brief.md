# Complete fixture validation

Read `text.md` in the neutral packet, every contract resource listed in
`contract-manifest.json`, and the complete supplied source material where the
packet lists it. Examine no repository, issue, other fixture or other report.
The manifest identifies resources by selected role, relative packet path and
SHA256. Report missing, unreadable or digest-mismatched resources as obstacles.

Write a report answering every item below. Validate the complete text against
its supplied contract rather than a preferred rewrite. No intended result or
classification has been supplied.

1. **Coverage.** List every resource read and applicable rule, by resource and
   heading. For each give the decisive passage or explicit absence and `holds`,
   `fails`, `inapplicable` with its reason, or `unresolved`. An omitted rule is
   unexamined.
2. **Anatomy.** Where required, run the supplied counting script on the whole
   text and retain its complete output. Examine semantic requirements separately.
   Read the standfirst alone, then cover it and read the entire body. Account
   for every person, thing and event the lead mentions and their introduction
   without the standfirst. Examine heading/section relationships and quoted
   speech in context. A counting pass establishes only what the script counts.
3. **Claims and support.** State relevant contextual propositions, their speaker,
   scope, certainty and source support. Distinguish supported inference, an
   asserted explanation and a promise of further information. Quote premises,
   commitment and follow-through, or the precise absence. A requested fact is
   not source evidence.
4. **Complete disposition.** Say whether the whole fixture conforms, each actual
   defect and unresolved question. Keep a supported target proposition separate
   from unrelated defects. Give no canonical replacement and do not edit text.

Finish with `Validation complete` only when every applicable rule is accounted
for and every supplied resource was available; otherwise finish `Validation
incomplete` with missing coverage. Return the complete report without a rewrite.
