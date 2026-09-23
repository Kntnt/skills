# The three ways a trace is not whole, checked

A packet reports an incomplete trace as incomplete, keeps what it has, and never reads the run's own reply as evidence that the missing part happened. These are the checks, each made over real run material rather than a fabricated packet, and each repeatable from what is committed here.

The unit coverage of the same behaviour is `tests/test_evaluation_trace.py`, which fixes the shapes; these checks are what the shapes look like when the material is a run that actually happened.

## 1. A child transcript that is not there

Copy the Redline packet, remove the correction agent's own transcript — leaving its `.meta.json`, as a run interrupted between the two would — and index the copy:

```
cp -R docs/evaluation/editorial-388/runs/redline-web-copy-flawed /tmp/missing-child
rm /tmp/missing-child/transcripts/subagents/agent-ac4e06f8cdb919a0f.jsonl
uv run docs/evaluation/editorial-388/harness/trace_index.py /tmp/missing-child
```

```json
{"status": "incomplete", "reasons": ["delegation-without-child"],
 "delegations_without_child": ["toolu_012h2yj3AC8mkUSBpGXwHLSm"],
 "agents": 1, "calls": 19}
```

The call that started the agent is named, so the gap is locatable rather than merely counted, and the 19 calls the session itself made are still indexed.

## 2. A transcript that ends mid-write

Copy the same packet and cut its parent transcript's last line in half, which is what a session killed while writing leaves behind:

```
cp -R docs/evaluation/editorial-388/runs/redline-web-copy-flawed /tmp/truncated
python3 -c 'import sys; from pathlib import Path; p = Path(sys.argv[1]); \
  lines = p.read_text().splitlines(); lines[-1] = lines[-1][: len(lines[-1]) // 2]; \
  p.write_text("\n".join(lines) + "\n")' /tmp/truncated/transcripts/parent.jsonl
uv run docs/evaluation/editorial-388/harness/trace_index.py /tmp/truncated
```

```json
{"status": "incomplete", "reasons": ["unparsable-line"],
 "unparsable_lines": {"transcripts/parent.jsonl": 1},
 "agents": 2, "calls": 25}
```

The count is per file, and every line before the broken one is indexed: the whole run is still readable, with one line declared lost.

## 3. A run that did not finish

[`runs/interrupted/`](runs/interrupted/) is a real run stopped by its own 45-second timeout, kept as it came:

```json
{"status": "incomplete", "reasons": ["run-did-not-finish"],
 "run_outcome": {"returncode": 143, "timed_out": true, "interrupted": false},
 "agents": 1, "calls": 12}
```

`result.json` records `process_group_gone: true` and `cleanup.json` names the one private root removed, so the check also establishes that a run stopped mid-flight leaves neither a process nor a directory behind. The 12 calls it had made — `base.md`, `genres/web-copy.md`, `web-craft.md` and `delivery.md` among them — are all in the index.

## 4. What the three runs left on the machine

The criterion is that no run-owned process survives and nothing else is removed, and neither is a thing a runner can be believed about on its own word. Checked from outside it, after all three runs above had ended:

```
ls -d "$TMPDIR"kntnt-editorial-388-run-*   # No such file or directory
ps -eo pid,command | grep -c '[c]laude --print'   # 0
```

No private root is left under the system temporary directory and no `claude --print` process from any of the three is still running. The runner removes exactly one path — the `mkdtemp` directory it made itself, named in each packet's `cleanup.json` under `removed_only` — and it registers nothing with any sweep, so nothing of anybody else's is in reach of it. `tests/test_evaluation_harness.py` holds the same contract as a test: a root made beside the run's own survives the run's teardown, and the teardown happens even when the run raises.

## What the first two checks also establish

Both copies still carry the original `response.txt`, in which the run states that the correction round completed and the closing Proofread pass ran. Neither status moves: the reasons come from the transcripts and the runner's exit, and a reply saying a thing happened is not a record of it having happened. That is the difference between a trace and a summary, and it is why `trace-status.json` says of itself that it is read from *transcripts and runner outcome only; never the run's reply*.
