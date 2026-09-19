"""Where the agents-md Skill puts a Project's agent-only documents.

The Skill is prose an agent executes, so what is held here is that every
surface of it names the same home, the same write boundary, and the same
migration of the retired directory (issue #326). Whether an agent following the
prose actually migrates a Project is exercised by running it, not here.
"""

from __future__ import annotations

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL = REPO_ROOT / "skills" / "agents" / "agents-md"
HOME = "docs/agents/"
RETIRED = "agents.d/"

# Every file of the Skill that states where its documents go. A surface left
# naming the old directory tells its reader to create it again.
SURFACES = (
    "SKILL.md",
    "help.md",
    "agents/openai.yaml",
    "references/placement.md",
    "references/writes.md",
    "references/gates.md",
)


def _read(name: str) -> str:
    return (SKILL / name).read_text(encoding="utf-8")


def test_every_surface_names_docs_agents_as_the_home() -> None:
    """Body, help, sidecar, and references agree on one directory."""

    missing = [name for name in SURFACES if HOME not in _read(name)]

    assert missing == []


def test_the_retired_directory_is_named_only_as_migration_input() -> None:
    """The old name survives only where it is the thing being migrated."""

    for name in ("agents/openai.yaml", "references/placement.md"):
        assert RETIRED not in _read(name), name

    description = yaml.safe_load(_read("SKILL.md").split("---")[1])["description"]
    assert RETIRED not in description
    assert HOME in description

    for name in ("SKILL.md", "help.md", "references/writes.md", "references/gates.md"):
        for line in _read(name).splitlines():
            if RETIRED in line:
                assert "legacy" in line.lower(), (name, line)


def test_the_write_boundary_opens_docs_agents_and_nothing_else_under_docs() -> None:
    """`docs/agents/` is the Skill's; the rest of `docs/` stays a proposal."""

    body = _read("SKILL.md")
    placement = _read("references/placement.md")
    writes = _read("references/writes.md")
    help_page = _read("help.md")

    assert "`docs/` outside `docs/agents/` is untouched" in body
    assert "`docs/agents/.gitkeep` if the directory is empty" in body
    assert "| `docs/` outside `docs/agents/` |" in placement
    assert "This skill never writes these files." in placement
    assert "| `docs/agents/` | Agent-only content." in placement
    assert "Change `docs/` outside `docs/agents/` — propose the text" in writes
    assert "outside `docs/agents/`" in help_page
    assert "an empty `docs/agents/` directory" in help_page
    assert "total including `docs/agents/`" in body
    assert "total including `docs/agents/`" in help_page


def test_the_body_sends_a_legacy_directory_to_the_migration() -> None:
    """A Project still holding `agents.d/` is migrated, not written beside."""

    body = _read("SKILL.md")

    assert "[`migrate.md`](references/migrate.md)" in body
    assert "legacy `agents.d/`" in body
    assert "Migrate a legacy `agents.d/`" in _read("references/writes.md")


def test_the_migration_settles_every_case_a_project_can_be_in() -> None:
    """Legacy-only, migrated, coexisting, duplicated, and colliding.

    A collision is the case that must change nothing: a version silently
    chosen, or a file overwritten, is a document lost with no one told.
    """

    migrate = _read("references/migrate.md")

    for fragment in (
        # Legacy-only and coexisting: move what the destination lacks.
        "Absent under `docs/agents/` → move it",
        "Keep every file already under `docs/agents/` as it is",
        # Identical duplicates coalesce to one copy.
        "Same bytes (`cmp`) → delete the `agents.d/` copy",
        # Conflicting destinations stop everything before anything changes.
        "Different bytes → collision",
        "change neither directory nor any reference to either",
        "Name both paths",
        "Never choose a version, merge the two texts, or overwrite a file",
        "`--yes` does not choose",
        # References follow the moved file, and nothing is left behind.
        "Rewrite every reference to an `agents.d/` path",
        "relative links inside each moved file",
        # A human document keeps its restriction even when its link breaks.
        "A reference in `docs/` outside `docs/agents/` stays a proposal, even under `--yes`",
        "Remove the emptied `agents.d/`",
        # Already migrated, and a repeated run.
        "No `agents.d/` → nothing to migrate",
    ):
        assert fragment in migrate, fragment
