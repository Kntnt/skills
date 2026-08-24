# Record template

Copy this file into [`records/`](records/README.md), name it `<skill>-<provider-family>-<YYYY-MM-DD>.md`, and fill it in as the run goes rather than afterwards. The fields are defined in [`protocol.md`](protocol.md); this is only their skeleton.

Keep one fixture section per fixture run, including the ones that were skipped. A fixture missing from a record reads later as a fixture that passed.

---

- **record** — `<skill>-<provider-family>-<YYYY-MM-DD>`
- **date** — `YYYY-MM-DD`
- **ticket** — `#NNN`
- **skill** — `write` | `redline` | `proofread`
- **provider family** — `claude` | `gpt`
- **model** — as the Harness names it
- **harness** — name, and version where it exposes one
- **corpus commit** — short commit of this repository the corpus was taken from

## `<fixture name>`

- **fixture** — the name from the corpus index
- **invocation** — verbatim, as typed
- **contextual instruction** — verbatim, or `none`
- **output target** — path, or `response`
- **observed delivery** — what came back and where it landed, in a sentence
- **side effects** — every file created, replaced, or removed, read from the filesystem; or `none`
- **criteria** —
  - `<criterion>` — `pass` | `fail` | `skipped` — one sentence of evidence; a `fail` names which of the five rejections it is
- **unresolved findings** — delivered with the artifact and left unresolved, or `none`
- **defects filed** — issue numbers, or `none`
- **notes** — what a later reader needs and the fields above do not hold

## `<next fixture name>`

- **fixture** —
- **invocation** —
- **contextual instruction** —
- **output target** —
- **observed delivery** —
- **side effects** —
- **criteria** —
- **unresolved findings** —
- **defects filed** —
- **notes** —
