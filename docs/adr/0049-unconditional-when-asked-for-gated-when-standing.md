# The template is unconditional when asked for, and gated when standing

`/brief` renders three sections — what happened, what I decided, what needs you — every time it is invoked. TL;DR mode renders them only above a gate. The asymmetry is deliberate, and it rests on a fact about how instructions to a model decay. This output contract is superseded by ADR-0080, which replaces both the fixed template and its gated standing counterpart with one content-selection policy and a natural form.

**"Use your judgment" is the one instruction that will not hold.** To a person it is reasonable guidance. To a model it is the first thing to erode: twenty turns into a session, with a full context and a hard problem, *be concise where appropriate* has no force, because this reply is always the appropriate exception. Instructions that survive are the ones that can be checked against the draft already written.

So the mode is built from named prohibitions rather than a disposition — lead with the answer, no process narration, no closing restatement, common word over precise-obscure word, and never mix a decision made on the user's behalf with a decision the user must make. Each is a rule a finished draft can be held against. None of them is a judgment call.

**The gate is structural for the same reason.** A line count invites estimation and estimation invites rationalising, so the trigger is what can be answered by looking: more than one list, or more than three paragraphs. A second and independent trigger catches the short-but-consequential case — any reply reporting work the user did not watch, whatever its length, since a four-line report that a migration ran needs the verdict as much as a long one does.

Below the gate there is no structure at all. Three headings wrapped around a one-line answer is a parody of what was asked for, and it is exactly how a standing instruction earns the reputation that gets it turned off. The command behaves differently because it was asked for by name: a user who types `/brief` has bought the full shape, and the only case it declines is a range too short to compress, where saying so is the honest answer.

**The mode governs replies and never files.** Left to inference a standing instruction reads as unconditional, and it would reach ADRs, `CONTEXT.md` entries, commit messages, and code comments. This repository's prose is deliberately dense and long-sentenced, and a brevity rule leaking into it would damage the thing it touched. `mode.md` therefore says so in its first line rather than leaving it to be worked out.

For the same reason `mode.md` is itself written plainly, against the register of the files around it. It is copied verbatim into a context file and read on every turn, so a block written in the house style would model the wrong thing continuously.
