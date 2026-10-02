# Reply state judge

Read exactly `input.md`, `delivered.md`, `draft.md`, `check.md` and `response.md` in the run directory supplied below. Judge the statements against the text they name, independently of what the checker says. You are not told the producer, arm, ticket, intended outcome or another judge's reading; do not look for them. A statement about the received text is tested against `input.md`; other statements are tested against `delivered.md`. A quality judgement is not a factual statement. Assess the scope and predicate actually asserted, including the difference between naming a subject and explaining it. A body-only statement covers the body it names; a statement about the whole text covers headings and other passages too.

Write `judgement-<your letter>.md` in that directory, answering all headings:

**1. Drafted statements.** For every factual statement in `draft.md` that the named text contradicts, quote it, identify its scope, quote the contradicting passage and state what is true. Write `none` if there is none.

**2. Checker return.** For every false drafted statement under heading 1, say whether `check.md` names the falsehood and the correct contradicting passage. Quote its treatment or say `not named`. Also list any checker item that faults a true statement, with its statement and supporting text. Do not equate a quoted statement with an item that actually names its falsehood.

**3. Terminal statements.** Test `response.md` independently against the named texts. Quote every false factual statement and its contradicting passage; say whether its falsehood was already present in the draft or arose after the check. Write `none` if there is none.

**4. Scope observations.** Quote every exclusivity or absence claim from the draft and the terminal reply; give its actual scope, the predicate tested, and whether it is true or false. Do not count a true body-only observation as false because a heading names its subject. Do not read a heading naming a subject as a complete explanation unless it supports the proposition actually asserted.

Reply with the report path and counts under headings 1 and 3, at most 120 words. Write no other file.
