# Result for #490: stopped during contrast validation

The evaluation is incomplete. There is no fresh native Redline baseline, no isolated checker replay, no candidate wording, no implementation-role commit and no product change. Native reproduction is neither established nor rejected. The product revision remains `4cf05813f94c2fa7147898878027835e14d29859`; the catalog is unchanged because no shipped file changed.

## Prospective history

`41773ae9` froze the plan, five contrast pairs, independent briefs, input digests, historical #477 material and native capture harness before any native invocation. `55c7ace2` corrected the validator runner's input filename before Codex was launched: two evaluator prelaunch attempts looked for `input.md` instead of the neutral material's `text.md`. Their logs and inventories are in `prelaunch/`; `voided/` contains the campaign's partial copies of those same prelaunch packets, with no native transcript. The original plan, inputs, expectations and briefs were not rewritten.

## Independent contrast validation

The native validators ran in fresh sessions on `gpt-6.1-sol` at `xhigh`, through Codex CLI 0.160.0. Both readers of each contrast received only its text and reply under neutral physical host paths and the frozen validation brief. Expected readings, ticket, arm, producer identity and candidate hints were withheld. Each packet preserves its invocation, the complete native trace, identity audit, report and whole-root before/after inventory.

| Contrast | Frozen reading | Validator A | Validator B | Result |
| --- | --- | --- | --- | --- |
| q1: whole-text only, headline identifies trial object | false | false | false | supported |
| q2: body introduction before its first trial reference | true | true | true | supported |
| q3: intended true whole-text exclusivity | true | false | false | invalid contrast |
| q4: naming versus full explanation | both statements true | true / true | true / true | supported |
| q5: nowhere outside standfirst, contradicted by subheading | false | false | false | supported |

The q3 reply asserts: *I den mottagna texten anger bara ingressen att Elm Quay Housing prövade en gemensam reparationslogg.* Both validators read the body's *Försöket pågick i åtta veckor* in its surrounding text as asserting that the same log trial occurred. Validator A says *Brödtexten nämner alltså inte bara ett ämne utan lämnar en sakuppgift om samma genomförda försök*. Validator B likewise says the body communicates that the trial took place. Both distinguish that reading from q2's strictly limited observation about the text before the first trial reference. Their verdict is about semantics, not a keyword match.

The q4 readers distinguish *Loggförsöket*, which names the subject, from the complete proposition specifying the organisation, shared repair log, two buildings and eight-week duration. Both find the reply's naming statement and its exclusivity assertion about that complete explanation true. These supporting readings do not rescue the invalid q3 control under the frozen method, which requires both validators to support each frozen contrast's reading.

## Stop boundary

The frozen plan says that disagreement or ambiguity in a contrast is preserved and an invalid contrast halts dependent probes and candidate work. The intended true exclusivity fixture failed that gate, before any product wording or native baseline. A new prospective validation design is needed before work can continue; the contrast is not rewritten or relabelled in this evaluation. This is not a finding that the native fault failed to reproduce.

The six fresh pre-change native rows, six conditional candidate rows and all historical/contrast checker probes are skipped with this reason in the record. No drafted/checker/terminal native-state judgement exists, because no native Redline session was started. None of #489's application work, #491's article-review work or #478's declined second-list widening was built. No new product defect was measured or filed.

The historical #477 split remains distinct: reply judge A recorded two false terminal exclusivity statements; reply judge B and both correction judges did not. The saved checker named the summary's additional-change claim and did not name either exclusivity falsehood. Those saved states are historical diagnosis, never a substitute for the fresh baseline.

## Project gate

All four supplied CONTRIBUTING commands ran unchanged and completed; their exact commands, exits and durations are in `gate/summary.json`, and outputs in `gate/1.txt` through `gate/4.txt`. Ruff check, Ruff format check and mypy passed. Pytest returned 1: 2734 passed and one failed, `tests/test_adr.py::test_every_cited_number_has_a_record`. The prospective plan references the reserved decision-record number 0241 for the not-reproduced branch; stopping before native measurement means that branch was never reached and no decision record exists. That dangling reference is an unresolved gate failure. The frozen plan has not been edited after native validation started.

Evidence is committed with `Refs #490`. The native validators and gate supervisor finished; resource and scratch cleanup is recorded in `cleanup/`. The ticket is unfinished and no passing verification verdict is claimed.
