"""The frontmatter the Manager reads a skill's declaration out of."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType
from typing import Any, cast

REPO_ROOT = Path(__file__).resolve().parent.parent
KNTNT_PY = REPO_ROOT / "skills" / "kntnt" / "scripts" / "kntnt.py"
SKILLS = REPO_ROOT / "skills"


def _manager() -> ModuleType:
    """Import the manager's script as a module.

    Reading frontmatter is a function and no verb of its own, so the CLI
    cannot reach it directly, and this is the lowest layer that constrains it
    at all.
    """

    # The loader API answers with optionals, so both are narrowed before use:
    # a missing script is a broken checkout and has to say which file.
    spec = importlib.util.spec_from_file_location("kntnt_manager", KNTNT_PY)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import the manager from {KNTNT_PY}")

    # Execute the script under its own module object and hand that back.
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


kntnt = _manager()


def _frontmatter(relative: str) -> dict[str, Any]:
    """Parse the frontmatter of one shipped SKILL.md."""

    # The manager is imported dynamically, so everything it answers with is
    # `Any` as far as the type checker is concerned; the cast is what lets this
    # helper declare the shape it actually returns.
    text = (SKILLS / relative).read_text(encoding="utf-8")
    return cast(dict[str, Any], kntnt.parse_frontmatter(text))


def test_every_shipped_skill_carries_the_fields_the_catalog_reads() -> None:
    """Name, description, and the marker are what a Catalog entry is made of."""

    skill_mds = sorted(SKILLS.glob("*/*/SKILL.md"))

    # A glob that matched nothing would pass every assertion below it, which is
    # the one outcome this test exists to catch.
    assert skill_mds

    for skill_md in skill_mds:
        frontmatter = kntnt.parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        assert frontmatter.get("name") == skill_md.parent.name, skill_md
        assert frontmatter.get("description"), skill_md
        assert kntnt.collection_block(frontmatter) is not None, skill_md


def test_the_manager_carries_no_collection_block() -> None:
    """The Manager is no Catalog entry, and the sweep must never read it as one."""

    assert kntnt.collection_block(_frontmatter("kntnt/SKILL.md")) is None


def test_a_description_holding_a_colon_survives_the_parser() -> None:
    """agents-md's description opens with `AGENTS.md:`, and the value is the whole line."""

    description = _frontmatter("agents/agents-md/SKILL.md")["description"]

    assert description.startswith("AGENTS.md: create, shrink, or tend")
    assert '"' not in description


def test_the_shipped_skills_declare_the_lists_the_checker_refuses_on() -> None:
    """Every dependency list, read off the files the collection ships."""

    assert kntnt.skill_deps(_frontmatter("code/commit/SKILL.md")) == {
        "binaries": ["git", "uv"],
        "skills": [],
        "externals": [],
        "capabilities": [],
    }
    assert kntnt.skill_deps(_frontmatter("code/push/SKILL.md")) == {
        "binaries": ["git", "uv"],
        "skills": ["commit"],
        "externals": [],
        "capabilities": [],
    }
    assert kntnt.skill_deps(_frontmatter("code/release/SKILL.md")) == {
        "binaries": ["git", "uv"],
        "skills": ["push"],
        "externals": [],
        "capabilities": [],
    }
    assert kntnt.skill_deps(_frontmatter("code/orchestrate/SKILL.md")) == {
        "binaries": ["git", "gh", "uv"],
        "skills": [],
        "externals": [],
        "capabilities": ["subagents"],
    }
    assert kntnt.skill_deps(_frontmatter("agents/delegation/SKILL.md")) == {
        "binaries": ["uv"],
        "skills": [],
        "externals": [],
        "capabilities": ["subagents"],
    }


def test_a_skill_whose_frontmatter_is_broken_is_not_ours(tmp_path: Path) -> None:
    """A layer holds files the collection did not write, so bad YAML answers.

    The parser raises where the subset used to skip the line it could not
    read, and a traceback in place of the report is the failure of issue #5.
    """

    skill_dir = tmp_path / "stranger"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text(
        '---\nname: alpha\ndescription: "unterminated\nmetadata: [oops\n---\n',
        encoding="utf-8",
    )

    assert kntnt.carries_marker(skill_dir) is False


def test_text_with_no_frontmatter_is_no_frontmatter() -> None:
    assert kntnt.parse_frontmatter("# alpha\n\nA skill.\n") == {}


def test_unterminated_frontmatter_is_no_frontmatter() -> None:
    """A truncated file must answer empty rather than half a skill's declaration."""

    assert kntnt.parse_frontmatter("---\nname: alpha\n") == {}
