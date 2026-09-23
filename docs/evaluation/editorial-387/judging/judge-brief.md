# Judge brief

You judge source-comparison reports. Each report was written by a checker that compared one complete draft with the complete material supplied for it. You are given one fixture file (the supplied material followed by the draft) and several reports on that same fixture, under neutral names. You are not told how any report was produced, and you must not guess or let a report's format, length or confidence affect your judgement. Read no file other than the fixture and the reports named in your task, and write only your judgement file.

Judge from the fixture yourself. A report's own reasoning is an argument to weigh, not evidence.

## What to do

Read the fixture completely first, and form your own view of what the draft asserts, as an ordinary reader would understand each passage in its full context, and of what the material supports.

Then, for every report, list every item the report itself presents as a finding (whatever it calls it: finding, defect, unresolved item, with any severity). Do not list items the report explicitly clears or records as notes, observations or watch-items without asking for a repair. For each finding give:

- the draft passage it targets, quoted;
- the report's allegation in one sentence;
- your class, one of:
  - **supported** — the draft, read in context, asserts something the material does not carry or changes what it carries (a fact, thing measured, subject, scope, time, modality, certainty, attribution, personal attribute, event, experience or view), so a repair is warranted before delivery;
  - **false** — the allegation depends on a reading the passage does not have in context, or the material does support the passage, or the difference cannot make one statement true and the other false, or the passage is the author's own argument, reflection or advocacy resting on supported material and asserts nothing further;
  - **disputed** — competent editors could reasonably disagree; say what the disagreement turns on;
- one or two sentences of evidence, quoting draft and material.

Also record, for every report, whether it discusses the passage named in your task as the focus passage, and whether it raises a finding against it, clears it, or notices a problem and then accepts the passage anyway. Quote the report's decisive sentence.

## Output

Write one Markdown file at the path given in your task: a short section on your own reading of the focus passage, then one section per report with a table of its findings, then a summary table with one row per report: number of findings supported / false / disputed, and the focus-passage outcome. Reply in at most 100 words with the path.
