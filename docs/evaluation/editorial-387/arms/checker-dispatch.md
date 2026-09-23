# Checker dispatch

Every checker in this evaluation, in either arm and on any fixture, is started as one fresh `kntnt-opus-high` subagent (`claude-opus-5-5` at high deliberation, no conversation history) whose whole prompt is the message below, with its four placeholders filled and nothing added, removed or reworded. #379 saved no dispatch message; this one is written from its plan's prose — a checker receives one fixture file, the resolved language, and one arm's prompt file, and writes one report — and from the arm file's own words, which say that the resolved language, the fixture path and the report path "are given in the message that sent you here".

- `{task}` is a byte copy of the arm's prompt file ([`shipped-task.md`](shipped-task.md) or `reworded-task.md`), named `task.md`.
- `{fixture}` is a byte copy of the fixture file, named `fixture.md`.
- `{language}` is the fixture draft's `kntnt.language`, as the plan's fixture table gives it.
- `{report}` is `report.md`.

All three files sit in one directory of the builder's scratch whose name is a random token, so no path a checker sees names the arm, the fixture's designed class or this evaluation. The report is copied from there, with its modification time, to `runs/<arm>/<fixture id>-r<n>.md`.

## The message

````
Read the prompt file at `{task}` and do what it says. It is your whole task.

- Fixture path: `{fixture}`
- Resolved language of the draft: `{language}`
- Report path: `{report}`
````
