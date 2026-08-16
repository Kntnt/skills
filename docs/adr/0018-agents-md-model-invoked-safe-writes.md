# `agents-md` is a Model-invoked skill with a safe write set

`agents-md` is a Model-invoked skill so a Harness can start it without the user typing `/agents-md`. It must not write during other work. After the work is complete it may add an agent file or pointer, shorten text without changing meaning, remove a line only when a named source shows the fact, and rebuild the pointer list. It must not remove a fact because this session did not use it, remove a fact with no named source, or change `docs/`. Those cases get one concrete question after the work — not a prompt to run `/agents-md`.
