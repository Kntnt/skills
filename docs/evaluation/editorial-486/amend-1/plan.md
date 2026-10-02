# Prospective path-blinding correction for #486

Attempt `ms-20261002-0085f2`, amend 1, 2026-10-02. This addendum and its two
adapter/runner files are committed before replacement native readers start.
The original plan, inputs, expectations, briefs, harness, runs, validations and
judgements remain byte-for-byte intact. `original-files.json` inventories them.
`original-readers.json` enumerates every affected reader, not just the examples
in the failed verdict: four validators and twenty judges.

The defect is a ticket-bearing ancestor in an otherwise anonymous path. The
observed red test is preserved in `checks/red.log`. It independently inspects
all twenty-four actual prompts, native session contexts and public tool/reply
traces. Every reader leaks the ticket in each of those surfaces. An anonymous
leaf or a relative prompt would leave the native cwd disclosure untreated.

## Neutral view within the assigned write confinement

Readers get the same byte-frozen briefs and material bytes as before. Only the
path view changes. A packet-specific stdio MCP file adapter presents `/run` with
exactly the named input/response/output files. It permits writing only that
reader's designated report. Its physical backing, private HOME, CODEX_HOME,
temporary files, RPC ledger and native logs remain beneath the resolved assigned
scratch alias. Nothing is created, changed or removed outside this ticket's
two allowed write roots. No host symlink or shared neutral scratch directory is
created. The existing read-only `/` is only a neutral native working-directory
context; it holds no staged material or generated file.

Native shell execution is disabled for these file readers; the adapter supplies
the frozen briefs' exact file-reading and report-writing operations. No editorial
instruction, source, expectation, output or judging criterion changes. Native
judges remain fresh top-level Codex sessions on `gpt-6.1-sol` / `xhigh`, CLI
0.160.0, using private authentication and no model-selection override. Preserve
complete native session traces, actual contexts, tool calls, input digests and
report bytes. Check their actual model/effort, not a runner's annotation.

Run four fresh independent validators first, with only their text and the neutral
brief. They repeat the original pre-review independent distinction validation;
this is an additional blind reading, not a claim that it happened before the
already-completed baseline. Both readers must confirm each original class before
new judges run. Then rejudge all ten authentic retained baseline runs with two
fresh independent judges each, using the byte-identical control briefs and
expectations. No Redline run is repeated: its product behavior and artifacts
passed verification and are untouched. No candidate arm is commissioned.

## Counting and preservation

The twenty replacement judgements become the counted independent R1/C1 readings.
Keep the twenty original judgements and their results as compromised-path history,
never edit or remove them. `counted-readers.json` maps every replacement to the
original packet. Keep every new completed adverse judgement and apply the original
split rule exactly; do not rerun it to improve an outcome. Keep headline ownership
with #480 and the frozen contrast conformance conflict with #493. Preserve P1's
separate six-run non-reproduction and all five observable stages.

An interrupted replacement reader is void: preserve its complete packet and
record the interruption before any repeat. A changed source byte or a validator
class disagreement stops this unattended amend. Do not revise a frozen input,
criterion or expectation to accommodate it. Audit all reader-visible paths in
prompts, actual native contexts, MCP schemas/calls/results, reports and replies.
The regression must turn green across all twenty-four replacement readers.

Run the four exact CONTRIBUTING commands without altering or narrowing them.
Only cache/temp paths move beneath physical scratch; HOME and CODEX_HOME of the
builder and gate stay unchanged. Stop every owned process and its descendants,
delete only explicitly named owned runtime paths, and preserve all deliverables.
Commit the completion evidence separately, without changing shipped product,
corpus, original prospective files, ADR-0238 or run-owned aggregate files.
