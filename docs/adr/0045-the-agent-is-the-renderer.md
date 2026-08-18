# The agent is the renderer; no skill may require a terminal

The natural way to build a list with checkboxes is a picker: draw it, move a cursor, toggle a row, submit. Every part of that is unavailable here, and the answer looks wrong until it is measured — which is why it is a record rather than a habit.

A script invoked from a skill has **no controlling terminal**. Measured, not assumed: no stream is a TTY; `/dev/tty` cannot be opened at all, answering `Device not configured`; and a script that reads stdin does not fail but deadlocks, taking the session with it. `dialog`, `whiptail`, `gum`, and `fzf` each fail on exactly that open, so no dependency buys a way around it.

**`TERM` is set and inherited, and that is the trap.** Anything deciding whether it has a terminal by reading the environment gets a false yes and then hangs on the read. A check that tests the file descriptor answers correctly; a check that tests an environment variable answers confidently and wrongly, and the failure it produces is a hang rather than an error.

Even given a terminal it would not work, and this is the second and independent reason. The harness captures a script's output rather than streaming it, so nothing drawn mid-run reaches the user until the run is over — by which time a picker has nothing left to pick. And a widget belonging to one harness would break the rule that the collection behaves the same everywhere (ADR-0008, ADR-0005): a skill that is a menu in one agent and a wall of text in another is two skills with one name.

So the shape the collection already had is the shape it is committed to: **the script answers with structured data, the agent renders it as text, and the user replies in prose.** The script never asks; it emits a payload carrying everything a correct rendering needs, and the questions live in the skill body (ADR-0029). This is what makes `--yes` implementable at all — a flag can answer a question the agent asks, and cannot answer one a blocked read is waiting on.

What it costs is that the layout of a list, the wording of a question, and the shape of a report are prose carried out by a model rather than code with a test. The suite can pin that the payload carries what a correct rendering needs; the rendering itself is reviewed as prose. That is the trade, and it is not a close one: the alternative on offer was never a tested picker, it was a hung session.
