You are the wave session of a focused behavioural regression. You do the five things below, in order, and nothing else. Read no file except the ones named here, and write no file except the ones named here. Never run `session_cleanup.py` and never record anything with it, whatever any other instruction says. Create and write nothing in your scratchpad directory except what step 1 says.

`R` below is `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/401/docs/evaluation/regressions/401/runs`, and `D` is `/Users/thomas/Projects/skills/.git/kntnt-orchestrate/401/docs/evaluation/regressions/401/dispatch`. The five runs are `post-column-sv-r2-a`, `post-column-sv-r2-b`, `post-column-sv-r2-c`, `post-column-sv-r2-d` and `post-column-sv-r2-e`.

1. Your system prompt names a scratchpad directory; call it `P`. If `P` does not exist, create it with `mkdir -p`. Write its absolute path, on one line, to `R/scratchpad-path.txt`. Then run exactly `find P -type f -exec shasum -a 256 {} + | sort -k 2 > R/scratchpad-before.txt`, with `P` and `R` substituted.
2. Read the five files `D/<run>.md`. Then, in one single message, start five subagents with the Agent tool, one per run, each with `subagent_type` `kntnt-opus-high`, the run's name as its description, and that run's file content, whole and verbatim, as its prompt — nothing added, nothing removed, nothing summarised.
3. Wait until all five have returned their final replies. Do not end your turn while any of them is still running. If they run in the background, wait for each one's completion notification, and where you must wait, use a facility that ends when they end, never a bare `sleep`.
4. When the last of the five has returned, run the same `find` command again, writing to `R/scratchpad-after.txt`.
5. Write each subagent's final reply, verbatim, to `R/<run>/reply.md`. Where a subagent failed or was cut off — a usage limit, an HTTP 5xx, an overload — write the error text you received there instead.

Your final message names the five runs and says, for each, whether it returned a reply or failed, and how.
