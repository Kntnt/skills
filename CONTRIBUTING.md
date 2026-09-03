# Contributing to Kntnt Skills

Thanks for considering a contribution. kntnt/skills is open source, so anyone is free to fork it and adapt it for their own purposes. This document describes the *project norm* — what kinds of contribution are likely to be welcomed into the upstream repository at [Kntnt/skills](https://github.com/Kntnt/skills). It is editorial guidance on what is likely to be merged, not a legal restriction on what you may do with the code.

## Contribution scope

| Category | Examples | Reception |
|---|---|---|
| Welcomed without question | Bug reports; bug fixes against existing behaviour; corrections to broken examples; typo and grammar fixes in prose; clarifications that do not change behaviour. | Open a PR. If the change is small and self-evidently correct, it is usually merged quickly. |
| Accepted but discussed first | New features; changes to existing behaviour, scope, or a public interface; new dependencies. | Open an issue first to align on intent before writing code. A PR without prior discussion may still land, but expect feedback rounds. |
| Unlikely to be merged but free to fork | Changes that alter the project's direction or restructure its architecture in a way that conflicts with its goals. | The licence makes forking explicit and lawful. If you want a different direction, build it in your fork. |

## Inbound licensing

By submitting a contribution, you agree it is licensed under the Apache License 2.0 by virtue of its §5 *Submission of Contributions* — any contribution intentionally submitted for inclusion is under the terms of that licence unless you state otherwise. No separate contributor licence agreement is required.

## Behaviour

Be respectful and constructive in issues, pull requests, and discussions. Assume good faith, keep criticism about the work rather than the person, and help keep this a project people want to contribute to.

## How to contribute

1. **Open an issue first** for anything in the *discussed* row above. For *welcomed* items, you can open a PR directly. Use the issue tracker at <https://github.com/Kntnt/skills/issues>.
2. **One concern per PR.** Smaller PRs land faster.
3. **Follow the project's coding standard.** It is materialised under [`docs/coding-standard/`](docs/coding-standard/) — read `general.md` plus the module(s) for what you touch before changing anything: `python.md` for the language, and [`skills.md`](docs/coding-standard/skills.md) for the files a skill itself ships. Read that last one before adding a skill. Its `SKILL.md` and its `help.md` each have to carry things the suite enforces and nothing else states, and the fourth check below is where you find out otherwise.
4. **Regenerate the catalog** when you change any shipped file under `skills/`. Each Catalog entry carries a content Digest of its Skill directory, and the top-level `manager_digest` covers every file under `skills/kntnt/` except the recursively generated Catalog itself, so a Catalog left as it was no longer describes the Collection:

   ```
   KNTNT_SOURCE=. uv run skills/kntnt/scripts/kntnt.py catalog --write
   ```

   Nothing is authored by hand and no version is bumped — the digest is computed from the files. The fourth check below fails on a catalog that has fallen behind.

   That same line is declared in `.kntnt-orchestrate/generated.json`, which is where an unattended `/orchestrate` run reads what this repository generates. Two branches that each regenerated the catalog honestly cannot merge, so the run answers a collision confined to it by running the line above on the merged tree rather than by asking somebody to settle a file nobody wrote ([ADR-0106](docs/adr/0106-a-collision-in-generated-files-is-regenerated-not-repaired.md)). A generated file added later belongs in that declaration beside this instruction.

   Because that digest is computed over the files' bytes, the repository pins line endings to LF in `.gitattributes` — a checkout that normalises them would regenerate every digest and fail that same check.
5. **Run the tests.** The Python engines under a Skill's `scripts/` or the Collection Library's `library/scripts/` are covered by a pytest suite under `tests/`. Four commands verify a change, each provisioning its tool through `uv`:

   ```
   uvx ruff check .
   uvx ruff format --check .
   uvx --with types-PyYAML --with pytest mypy skills/kntnt/scripts/kntnt.py skills/kntnt/library/scripts/ship.py skills/kntnt/library/scripts/integrations.py skills/kntnt/library/scripts/languages.py skills/kntnt/library/scripts/routed_observations.py skills/kntnt/library/scripts/standing_policy.py skills/models/model-selector/scripts/context.py skills/code/orchestrate/scripts/run.py skills/producivity/rename-invoices/scripts/rename_invoices.py tests
   uv run --with pytest --with pyyaml pytest
   ```

   The manager's script declares PyYAML in its PEP 723 block, so `uv run` gives it that package on its own; the last two commands name it because they do not go through the script — mypy needs the stubs, its test surface needs pytest's types, and the tests import the script into their own interpreter.

   These are the same four checks CI runs on every pull request, so a green run locally means a green run there.

6. **Compare a skill against the reference validator** when you add one or change the frontmatter of one. `skills-ref` is the reference implementation shipped with the Agent Skills specification itself. It is not on `PATH`, nothing above installs it, and it is not obtainable under the name `agentskills` that some of this repository's older tickets gave it — no command exists under that name. `uvx` fetches it from a subdirectory of the specification's repository, and a skill directory is `skills/<category>/<skill>/`:

   ```
   uvx --from git+https://github.com/agentskills/agentskills#subdirectory=skills-ref skills-ref validate <skill-directory>
   uvx --from git+https://github.com/agentskills/agentskills#subdirectory=skills-ref skills-ref read-properties <skill-directory>
   ```

   `validate` holds a skill to the specification. `read-properties` prints the skill's declaration as a reader outside this collection resolves it, which is the answer to *what does anybody else actually get from this skill* — it is what issue #52 was verified with, and the one command that shows a `metadata` value coerced into something nothing can read back out. The tool is also published to PyPI as `skills-ref`, if you would rather install it than fetch it on each run.

   **A red run is expected, and is not something you caused.** `validate` rejects every skill this collection ships, and always has, over frontmatter fields the collection carries knowingly. [ADR-0066](docs/adr/0066-the-reference-validator-is-a-baseline-not-a-gate.md) is the record that settles which fields those are, why they stay, and how the tool may be cited: as a baseline that must not regress, never as a gate that must pass. So this step is a comparison rather than a check — what has to hold is that your change draws no complaint the record does not already account for. It is deliberately absent from the four checks above and from CI, a check red on every run being no gate at all.

## Questions

Open an issue or start a discussion. Conversation happens in the open.
