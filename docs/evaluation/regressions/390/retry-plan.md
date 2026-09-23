# Native retry, fixed before execution

Attempt `ms-20260922-59e6c1` resumes the uncommitted implementation from
`ms-20260922-37af51`. The fixtures, tasks and semantic criteria in [plan.md](plan.md)
are unchanged. The earlier startup failure and its mechanical evidence remain
in the packet. This retry uses Codex CLI 0.155.1, the configured `gpt-5.6-sol`
with `xhigh` effort and default service tier. Native execution uses
`danger-full-access` because the prior sandbox prevented service access;
workspace instructions still confine effects to each private run directory.

Each run stages the working-tree Write, Redline, Proofread and Manager. Its
private Codex configuration holds only the chosen model settings and a copy of
the existing authentication; secrets never enter the packet. Kntnt state,
temporary files and tool caches live in the ticket's assigned scratch directory.
No global configuration is edited. The runner preserves parent and child native
session records, exact argv and invocation, input/instruction hashes, response,
and before/after workspace inventories. A 1,200-second limit bounds each native
run; the runner terminates and reaps its process group on every exit.

Results go under `retry-59e6c1/`. Run each frozen case once; preserve failures
without retuning fixtures or criteria. Read actual traces and artifacts against
the six criteria in the original plan. No exact generated wording is required.
The four CONTRIBUTING checks also run again with tool caches and temporary
storage under the assigned scratch path. These operations change execution
conditions, not the product or its acceptance criteria.
