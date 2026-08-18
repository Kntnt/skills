# The skill body carries only what the agent executes

Help moved out of `SKILL.md` because it drifted (ADR-0044). It should have moved out for a second reason, and that reason binds more than help: **every line of a skill body is paid on every invocation, and a line the agent does not act on buys nothing.** A description of a flag is not an instruction. It is documentation that happens to be stored where the instructions are, and the harness reads the whole file to find out what to do.

So audience decides placement inside a skill, exactly as it decides placement inside a repository (ADR-0016). `SKILL.md` points; it does not copy.

- **What the agent executes** stays in the body — the Steps, the dependency check, the parse rules it carries out.
- **What a user reads** is `help.md`, and `--help` is its route (ADR-0044). Nothing in the body restates it.
- **What the agent needs only sometimes** is a sibling file the body names, opened when the situation arises: `gates.md`, `placement.md`, `writes.md`, `mode.md`, `persist.md`, `changelog.md`, and the Manager's `steps/<verb>.md`.

The test is whether removing a passage changes what the agent does. An `## Arguments` section that describes flags the Steps already act on fails it: the Steps say *wait unless `--yes`*, and the description above them says the same thing to nobody who will act on it. `delegation` keeps its `## Arguments`, and the distinction is the whole rule — its entries are not descriptions of flags but the parse rules themselves, and step 1 has nothing to carry out without them. Four skills lost the section; one kept it; neither outcome was about length.

The frontmatter already carries `argument-hint`, so the harness has a usage line whether or not the body repeats it.

**What this costs.** Someone reading a `SKILL.md` on its own no longer finds out what the skill takes. That is deliberate: the body is not written for that reader, and the file that is — `help.md` — sits next to it. The drift this trades into is a manpage that can fall behind the Steps, which is a file a reviewer can diff, rather than a regenerated text nobody can.
