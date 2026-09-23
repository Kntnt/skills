# Judge dispatch

Every judge in this evaluation is started as one fresh `kntnt-opus-high` subagent (`claude-opus-5-5` at high deliberation, no conversation history) whose whole prompt is the message below, with its placeholders filled and nothing added, removed or reworded. #379 saved no dispatch message; this one is written from the "Judging" section of [`../../editorial-379/plan.md`](../../editorial-379/plan.md): a judge is given the fixture, the reports under shuffled neutral names, the judge brief, and the fixture's focus passage, and answers "The two questions" for each report, settled by the counting rules frozen there.

- `{brief}` is a byte copy of [`judge-brief.md`](judge-brief.md), itself a byte copy of `../../editorial-362/checker/judging/judge-brief.md`.
- `{fixture}` is a byte copy of the fixture file.
- `{reports}` lists the report copies, each named `report-<letter>.md`, the letters shuffled.
- `{focus}` is the fixture's focus passage, exactly as frozen in the plan's fixture table.
- `{span_rule}` is, for `bd1` and `nd1`, **that passage or a span inside it**; for the seven fixtures of `../../editorial-362/checker/fixtures/`, **that passage, a span inside it, or a longer quotation of the draft sentence that contains it**.
- `{judgement}` is `judgement.md`.

Every file a judge sees sits in one directory of the builder's scratch whose name is a random token, one directory per judge, so no path names an arm, a run, a designed class or this evaluation, the key is nowhere in reach, and neither judge of a pair can see the other's judgement.

## The message

````
You are a judge. Your instructions are the judge brief at `{brief}`; follow it exactly. Read no file other than the brief, the fixture and the reports named here, and write only your judgement file.

- Fixture: `{fixture}`
- Reports, under neutral names: {reports}
- Focus passage, exactly as the draft carries it: "{focus}"
- Judgement file: `{judgement}`

Besides what the brief asks, end your judgement file with a section headed `## Focus-passage answers`: one table with one row per report and the columns Report, Q1, Decisive sentence, Allegation, Q2, Evidence. Answer these two questions for every report.

Q1. Did this report file a finding against the focus passage? Answer yes or no, and quote the report's decisive sentence. A finding is what the brief counts: an item the report itself presents as a finding, whatever it calls it and at whatever severity, and not an item it clears, or records as a note, an observation or a watch-item without asking for a repair. A finding is against the focus passage only where the draft passage it quotes is {span_rule}. A finding on a neighbouring sentence is not one. Where the answer is yes, state in the Allegation column the allegation of each such finding in one sentence; otherwise write "—".

Q2. On your own reading of the fixture, is a finding against that passage correct? Answer yes or no, with one or two sentences of evidence quoting the draft and the material.
````
