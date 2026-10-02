# Prelaunch harness attempts

Both attempts failed in evaluator input inventory before `subprocess.Popen` could launch Codex. The validator material is named `text.md`, while the campaign supplied the runner `--input-name=input.md`. There are no native traces or model calls. The two capture threads were terminated with their owned process groups, and the runner-name correction was committed before any native run. No plan, fixture, brief, expectation or semantic method changed.
